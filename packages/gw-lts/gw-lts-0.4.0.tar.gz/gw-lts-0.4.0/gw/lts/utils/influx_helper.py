#!/usr/bin/env python3

import sys
import yaml
from collections import defaultdict, deque

from ligo.scald.io import influx, kafka
from lal import GPSTimeNow

class InfluxHelper(object):
	def __init__(self, config_path=None, routes={}):
		# set up dicts to store trigger information
		self.routes = list(routes.keys())
		agg = {}
		for route, value in routes.items():
			agg[route] = value['aggregate']
		self.aggregate = agg
		self.triggers = {route: defaultdict(lambda: {'time': deque(maxlen = 1000), 'fields': defaultdict(lambda: deque(maxlen=1000))}) for route in self.routes}
		self.last_trigger_snapshot = None

		# set up influx configuration
		with open(config_path, 'r') as f:
			config = yaml.safe_load(f)

		self.influx_sink = influx.Aggregator(**config["backends"]["default"])
		self.influx_sink.load(path=config_path)

	def store_triggers(self, time, data, route=None, tags=None):
		self.triggers[route][tags]['time'].append(time)
		this_triggers = self.triggers[route][tags]['fields']
		for key, value in data.items():
			this_triggers[key].append(value)
	
		# output data to influx every 100 seconds
		now = float(GPSTimeNow())
		if not self.last_trigger_snapshot or (now - self.last_trigger_snapshot >= 100.):
			self.last_trigger_snapshot = now
	
			# cast data from deques to lists to output
			outdata = {}
			for key in self.triggers:
				outdata[key] = {}
				for tag in self.triggers[key]:
					outdata[key][tag] = {
						'time': list(self.triggers[key][tag]['time']),
						'fields': {
							dataname: list(datadeq) for dataname, datadeq in self.triggers[key][tag]['fields'].items()
						}
					}
	
			## First store triggers, these get aggregated by combined_far
			for route in self.routes:
				if outdata[route]:
					print(f'Writing {route} to influx...', file=sys.stderr)
					self.influx_sink.store_columns(route, outdata[route], aggregate = self.aggregate[route])
	
