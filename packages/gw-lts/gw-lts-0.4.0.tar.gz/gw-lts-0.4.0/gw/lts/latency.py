#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import logging

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables

from lal import GPSTimeNow

from ligo.scald.io import kafka

from gw.lts import utils

def parse_command_line():

	parser = utils.add_general_opts()
	opts, args = parser.parse_args()

	return opts, args

def main():
	opts, args = parse_command_line()
	
	tag = opts.tag
	
	# set up Kafka client
	client = kafka.Client(f'kafka://{tag}@{opts.kafka_server}')
	
	# set up logging
	utils.set_up_logger(opts.verbose)
	
	# create a job service using cronut
	app = App('latency', broker=f'kafka://{tag}_latency@{opts.kafka_server}')
	
	# subscribes to a topic
	@app.process(opts.input_topic)
	def process(message): 
		mdatasource, mtag, mtopic = utils.parse_msg_topic(message)
		farstring = utils.parse_msg_key(message)
		logging.debug(f'Read message from {mdatasource} {mtopic}.')
	
		# parse event info
		event = json.loads(message.value())
	
		time = event['time'] + event['time_ns'] * 10**-9.
		latency = event['latency']
	
		if latency:
			# construct output message
			output = {
				'time': [ float(time) ],
				'data': [ float(latency) ]
			}
	
			# send message to output topics
			client.write(f'{mdatasource}.{tag}.testsuite.latency', output, tags = farstring)
			logging.info(f'Sent msg to: {mdatasource}.{tag}.testsuite.latency')

	# start up
	logging.info('Starting up...')
	app.start()

if __name__ == '__main__':
	main()
