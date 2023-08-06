#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import numpy
import copy
import logging

from time import sleep
from collections import defaultdict, deque
from confluent_kafka import Producer

from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables
from lal import GPSTimeNow
from lal import LIGOTimeGPS

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()
	parser.add_option('--ifo', action = 'append', help = 'Interferometer(s) to get data from')
	opts, args = parser.parse_args()

	return opts, args

class SNRConsistency(object):
	def __init__(self, options):
		self.ifos = options.ifo
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.topics = options.input_topic

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{self.kafka_server}')

		# create a job service using cronut
		self.app = App('snr_consistency', broker=f'kafka://{self.tag}_snr_consistency@{self.kafka_server}')

		# subscribes to a topic
		@self.app.process(self.topics)
		def process(message):
			mdatasource, mtag, mtopic = utils.parse_msg_topic(message)
			farstring = utils.parse_msg_key(message)

			# unpack information from the message
			event = json.loads(message.value())
			time = event['time'] + event['time_ns'] * 10**-9.
			coinc_file = utils.load_xml(event['coinc'])

			# get sim table and injected ifo snrs
			simtable = lsctables.SimInspiralTable.get_table(coinc_file)

			inj_snrs = defaultdict(lambda: None)
			inj_snrs['H1'] = simtable[0].alpha4
			inj_snrs['L1'] = simtable[0].alpha5
			inj_snrs['V1'] = simtable[0].alpha6

			# get coinc table and recovered ifo snrs
			sngltable = lsctables.SnglInspiralTable.get_table(coinc_file)

			rec_snrs = defaultdict(lambda: None)
			for r in sngltable:
				if r.snr:
					rec_snrs[r.ifo] = r.snr

			# for each ifo, compute accuracy and send off a message
			for ifo in self.ifos:
				if ifo in inj_snrs.keys() and ifo in rec_snrs.keys():
					accuracy = (inj_snrs[ifo] - rec_snrs[ifo]) / inj_snrs[ifo]
					output = {
							'time': [ time ],
							'data': [ accuracy ]
					}

					self.client.write(f'{mdatasource}.{self.tag}.testsuite.{ifo}_snr_accuracy', output, tags = farstring)
					logging.info(f'Sent msg to: {mdatasource}.{self.tag}.testsuite.{ifo}_snr_accuracy')


	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


def main():
	opts, args = parse_command_line()

	# sanity check input options
	required_opts = ['ifo', 'tag', 'input_topic', 'kafka_server']
	for r in required_opts:
		if not getattr(opts, r):
			raise ValueError(f'Missing option: {r}.')

	# set up logging
	utils.set_up_logger(opts.verbose)

	# start up processor
	processor = SNRConsistency(opts)
	processor.start()

if __name__ == '__main__':
	main()
