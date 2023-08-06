#!/usr/bin/env python3

from optparse import OptionParser
import json
import logging
import copy
import numpy

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from gw.lts import utils
from gw.lts.utils.gracedb_helper import GraceDbHelper

from ligo.scald.io import kafka

from ligo.lw import lsctables

from ligo.em_bright import computeDiskMass

def parse_command_line():
	parser = utils.add_general_opts()
	opts, args = parser.parse_args()

	return opts, args

class EMBright(object):
	def __init__(self, options):
		self.tag = options.tag
		self.kafka_server = options.kafka_server

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{options.kafka_server}')

		self.gracedb_helper = GraceDbHelper(options.gracedb_server)

		# initialize output dict
		self.events = deque(maxlen=50)

		# create a job service using cronut
		self.app = App('em_bright', broker=f'kafka://{self.tag}_em_bright@{self.kafka_server}')

		# subscribes to a topic
		@self.app.process(options.input_topic)
		def process(message):
			mdatasource, mtag, mtopic = utils.parse_msg_topic(message)
			farstring = utils.parse_msg_key(message)
			logging.info(f'Read message from {mdatasource} {mtopic}.')

			# parse message value
			event = json.loads(message.value())
			event.update({
				'datasource': mdatasource,
				'farstring': farstring,
			})

			response = self.process_event(event)
			if not response:
				# keep track of events that failed
				# to get a em_bright on the first try
				# this can happen if the embright isnt 
				# uploaded immediately
				times = [e["time"] for e in self.events]
				if not event["time"] in times:
					self.events.append(event)

			# iterate over events and try again to grab a
			# em_bright for each one. On success, remove
			# the event from the deque
			for e in copy.deepcopy(self.events):
				response = self.process_event(e)
				if response:
					self.events.remove(e)

	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def process_event(self, event):
		file = self.gracedb_helper.query_file(event['uid'], filename='em_bright.json')
		if file:
			em_bright_dict = json.loads(file.read())
			logging.info(f'Received em_bright.json from event {event["uid"]}')
		else:
			logging.info(f'Failed to receive em_bright.json from {event["uid"]}')
			em_bright_dict = None

		if em_bright_dict:
			output = {}
			time = event["time"]
			datasource = event["datasource"]
			farstring = event["farstring"]

			# determine source from inspiral table
			coinc_file = utils.load_xml(event['coinc'])
			simtable = lsctables.SimInspiralTable.get_table(coinc_file)
			source = utils.source_tag(simtable)

			# get masses and spins to use in computing the disk mass
			mass1 = simtable[0].mass1
			mass2 = simtable[0].mass2
			spin1z = simtable[0].spin1z
			spin2z = simtable[0].spin2z

			M_rem = computeDiskMass.computeDiskMass(mass1, mass2, spin1z, spin2z, eosname='2H', kerr=False, R_ns=None, max_mass=None)
			hasNS = "True" if M_rem else "False"

			logging.debug(f'Source: {source} | Remnant disk mass: {M_rem} | hasNS: {hasNS}')

			for key, value in em_bright_dict.items():
				output[f'p_{key}'] = {
					'time': [ time ],
					'data': [ value ]
				}

			# send message to output topics
			for topic, data in output.items():
				self.client.write(f'{datasource}.{self.tag}.testsuite.{topic}', data, tags = [farstring, source, hasNS])
				logging.info(f'Sent output message to output topic: {datasource}.{self.tag}.testsuite.{topic}.')

			return True

		else:
			return False


def main():
	opts, args = parse_command_line()

	# call computeDiskMass for the first time
	# to download all the necessary files
	_ = computeDiskMass.computeDiskMass(2.6, 1.6, 0, 0, eosname='2H', kerr=False, R_ns=None, max_mass=None)

	# set up logging
	utils.set_up_logger(opts.verbose)

	processor = EMBright(opts)
	processor.start()

if __name__ == '__main__':
	main()
