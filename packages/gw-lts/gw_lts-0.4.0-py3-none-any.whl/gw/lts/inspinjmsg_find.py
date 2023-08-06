#!/usr/bin/env python3

from optparse import OptionParser
import os
import io
import sys
import json
import copy
import logging

from collections import defaultdict, deque, OrderedDict

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

from lal import GPSTimeNow

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--preferred-param', default = 'ifar', help = 'Parameter to use to determine preferred events in the case that multiple event messages are found for a single injection. ' +
		'Supported options are max ifar (default) or max snr')
	opts, args = parser.parse_args()

	return opts, args

class InspInjMsgFind(object):
	def __init__(self, options):
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.topics = options.input_topic
		self.preferred_param = options.preferred_param
		self.verbose = options.verbose

		# initialize data deques
		# if injections come every ~20 seconds this should correspond 
		# to keeping messages for about 3-4 minutes.
		self.maxlen = 10
		self.event_msgs = defaultdict(lambda: deque(maxlen=self.maxlen))
		self.inj_msgs = defaultdict(lambda: deque(maxlen=self.maxlen))

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{self.kafka_server}')

		# create a job service using cronut
		self.app = App('inspinjmsg_find', broker=f'kafka://{self.tag}_inspinjmsg_find@{self.kafka_server}')

		@self.app.process(self.topics)
		def process(message):
			mdatasource, mtag, mtopic = utils.parse_msg_topic(message)

			# unpack data from the message
			if mtopic == 'inj_events':
				# parse event info
				event = json.loads(message.value())

				# load the coinc table and
				# get event coalescence time
				coinc_file = utils.load_xml(event['coinc'])
				coinctable = lsctables.CoincInspiralTable.get_table(coinc_file)
				coincrow = coinctable[0]
				coinctime = coincrow.end_time + 10.**-9. * coincrow.end_time_ns

				# keep track of the preferred parameter
				# for this event
				val = self.get_preferred_param(coinctable)

				dict = {
					'time': coinctime,
					'coinc': coinc_file,
					'msg_time': int(GPSTimeNow()),
					'preferred_param': val,
				}

				logging.info(f'received {mdatasource} event with coalescence time: {coinctime} and {self.preferred_param} = {val}')

				# if there is already an event at the same time
				# check if this one is preferred, and only keep
				# the best event in the deque to process
				nearest_event = utils.find_nearest_msg(self.event_msgs[mdatasource], coinctime)
				if nearest_event:
					logging.info(f'Found previous event within 1 sec of this event.')
					if val > nearest_event['preferred_param']:
						logging.info(f'New event is preferred, removing previous event from the deque.')
						self.event_msgs[mdatasource].remove(nearest_event)
					else:
						logging.info(f'Previous event is preferred. Skipping this event.')
						return
				else:
					logging.info(f'No previous event in deque within 1 sec of this event.')

				# add optional keys - these may or may not
				# already be present depending on the data
				# source configuration
				for key in ('latency', 'p_astro', 'uid', 'pipeline'):
					try:
						dict.update({
							key: event[key]
						})
					except KeyError:
						dict.update({
							key: None
						})
				# add far class
				far_string = utils.far_string(float(coincrow.combined_far))
				dict.update({'farstring': far_string})
				logging.debug(f'combined far: {coincrow.combined_far} | far string: {far_string}')

				# store event data in the deque
				self.event_msgs[mdatasource].append(dict)

				# process the events in the deque
				self.process_events(mdatasource)

			elif mtopic == 'inj_stream':
				# parse inj info
				injection = json.loads(message.value())
				ifos = injection['onIFOs']

				# load the sim table
				simfile = utils.load_xml(injection['sim'])
				simrow = lsctables.SimInspiralTable.get_table(simfile)[0]

				# get injection coalescence time
				simtime = simrow.geocent_end_time + 10.**-9 * simrow.geocent_end_time_ns
				logging.info(f'received {mdatasource} injection with coalescence time: {simtime}')

				# store inj data
				self.inj_msgs[mdatasource].append({
					'time': simtime,
					'sim': simfile,
					'ifos': ifos,
					'preferred_event': None,
				})

				# process the events in the deque and then
				# check for stale msgs
				self.process_events(mdatasource)
				self.process_stale_msgs(mdatasource)

			else:
				# break
				logging.debug(f'Error: Found unexpected message from topic {mtopic}.')


	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def append_sim_table(self, coinc_file, sim_file):
		# init a new sim inspiral table
		this_sim_table = lsctables.SimInspiralTable.get_table(sim_file)
		coinc_file.childNodes[-1].appendChild(this_sim_table)

		return coinc_file


	def write_sim_file(self, sim, xmldoc):
		# open a new xml doc
		sim_msg = io.BytesIO()
		ligolw_elem = xmldoc.appendChild(ligolw.LIGO_LW())

		output_simtable = ligolw_elem.appendChild(lsctables.New(lsctables.SimInspiralTable))
		this_sim_table = lsctables.SimInspiralTable.get_table(sim)
		output_simtable.extend(this_sim_table)
		ligolw_utils.write_fileobj(xmldoc, sim_msg)

		return sim_msg


	def construct_event_ouput(self, xmldoc, event, injection, key=None):
		filename = f'coinc-{int(event["time"])}.xml' if not key else f'{key}-coinc-{int(event["time"])}.xml'

		coinc = event['coinc']
		coincrow = lsctables.CoincInspiralTable.get_table(coinc)[0]
		simrow = lsctables.SimInspiralTable.get_table(coinc)[0]

		ligolw_utils.write_filename(xmldoc, os.path.join('coincs', filename), verbose = self.verbose)
		coinc_msg = io.BytesIO()
		ligolw_utils.write_fileobj(xmldoc, coinc_msg)

		output = {
			'time': simrow.geocent_end_time,
			'time_ns': simrow.geocent_end_time_ns,
			'snr': coincrow.snr,
			'far': coincrow.combined_far,
			'p_astro': event['p_astro'],
			'coinc': coinc_msg.getvalue().decode(),
			'latency': event['latency'],
			'uid': event['uid'],
			'onIFOs': injection['ifos'],
			'pipeline': event['pipeline'],
		}

		return output


	def process_events(self, datasource):
		# for each event in the event_msgs deque, find the nearest injection in inj_msgs
		# within +/- delta_t (1 second) of the event coalescence time.
		# when an association is made, check to see if its better than any previous
		# event found. If so, add the sim inspiral table from injection to the 
		# event's coinc xml and send a message to the testsuite.events topic and remove
		# the processed event from the deque.
		events_copy = copy.copy(self.event_msgs[datasource])
		injections = self.inj_msgs[datasource]

		for event in events_copy:
			event_time = event['time']
			nearest_inj = utils.find_nearest_msg(injections, event_time)

			# if no associated injection was found, continue
			if not nearest_inj:
				logging.info(f'No injection found for event at time {event_time}')
				continue

			inj_idx = self.inj_msgs[datasource].index(nearest_inj)
			inj_time = nearest_inj['time']
			sim_file = nearest_inj['sim']
			prev_preferred_event = nearest_inj['preferred_event']
			coinc_file = event['coinc']
			this_coinc = lsctables.CoincInspiralTable.get_table(coinc_file)
			val = self.get_preferred_param(this_coinc)

			# if this is the first event found or 
			# this event is better than the previous,
			# send update event.
			# Note: this requires that aggregate by
			# "latest" works the way we would hope
			if not prev_preferred_event or val > prev_preferred_event:
				# update preferred event for this injection
				self.inj_msgs[datasource][inj_idx].update({
					'preferred_event': val
				})

				# proceed with sending event
				# add sim table to coinc file and write to disk
				logging.info(f'Sending event with {self.preferred_param} = {val} for injection at time {inj_time}')
				newxmldoc = self.append_sim_table(coinc_file, sim_file)
				output = self.construct_event_ouput(newxmldoc, event, nearest_inj)

				self.client.write(f'{datasource}.{self.tag}.testsuite.events', output, tags = event['farstring'])
				logging.info(f'Sent msg to: {datasource}.{self.tag}.testsuite.events | far string: {event["farstring"]}')

				# finally remove event from the deque
				self.event_msgs[datasource].remove(event)


	def process_stale_msgs(self, datasource):
		# process old messages: either messages that are about to be 
		# removed from the left of the deque, or have been in the deque
		# for 2 hours, and send a message with the necessary info
		# this is necessary in the case that:
			# 1) we receive an event from the search which is not
			# associated with an injection, ie a glitch or real gw 
			# candidate.
			# 2) there is an injection for which we never receive
			# an associated event from the search. ie the injection
			# was not recovered at even the GDB far threshold.
		stale_inj = self.stale_msgs(self.inj_msgs[datasource])
		if stale_inj:
			if not stale_inj['preferred_event']:
				sim_inspiral = stale_inj['sim']
				logging.info(f'Sending {datasource} missed injection msg for injection {stale_inj["time"]}')
				simrow= lsctables.SimInspiralTable.get_table(sim_inspiral)[0]
				newxmldoc = ligolw.Document()
				sim_msg = self.write_sim_file(sim_inspiral, newxmldoc)

				output = {
					'time': simrow.geocent_end_time,
					'time_ns': simrow.geocent_end_time_ns,
					'sim': sim_msg.getvalue().decode(),
					'onIFOs': stale_inj['ifos'],
				}

				farstring = "None"

				self.client.write(f'{datasource}.{self.tag}.testsuite.missed_inj', output, tags = farstring)
				logging.info(f'Sent msg to: {datasource}.{self.tag}.testsuite.missed_inj')
				newxmldoc.unlink()
			else:
				logging.debug(f'Injection at time {stale_inj["time"]} to be removed from the deque.')

		stale_event = self.stale_msgs(self.event_msgs[datasource])
		if stale_event:
			logging.info(f'{datasource} event from time {stale_event["time"]} to be removed from the queue - no associated injection found')


	def stale_msgs(self, deque):
		# FIXME dont hardcode wait time
		if deque and (len(deque) == self.maxlen or float(GPSTimeNow()) - deque[0]['time'] >= 7200.):
			return deque[0]

	def get_preferred_param(self, coinc):
		# get preferred param value for this event
		if self.preferred_param == 'ifar':
			# IFAR
			val = 1. / coinc.getColumnByName('combined_far')[0]
		elif self.preferred_param == 'snr':
			val = coinc.getColumnByName(self.preferred_param)[0]
		else:
			raise NotImplementedError

		return val


def main():
	# parse options from command line
	opts, args = parse_command_line()

	# set up logging
	utils.set_up_logger(opts.verbose)

	# set up dir for output coincs
	try:
		os.mkdir('coincs')
	except OSError as error:
		pass

	# initialize the processor
	processor = InspInjMsgFind(opts)
	processor.start()

if __name__ == '__main__':
	main()
