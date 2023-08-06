import numpy
import sys
import logging
from io import StringIO, BytesIO
from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils as ligolw_utils

from ligo.segments import segment
from ligo.scald.utils import floor_div

import yaml
from yaml.loader import SafeLoader

from optparse import OptionParser

from lal import G_SI, MSUN_SI, C_SI

class LIGOLWContentHandler(ligolw.LIGOLWContentHandler):
    pass

lsctables.use_in(LIGOLWContentHandler)

all_sngl_rows = ("process:process_id", "ifo", "search", "channel", "end_time", "end_time_ns", "end_time_gmst", "impulse_time", "impulse_time_ns", "template_duration", "event_duration", "amplitude", "eff_distance", "coa_phase", "mass1", "mass2", "mchirp", "mtotal", "eta", "kappa", "chi", "tau0", "tau2", "tau3", "tau4", "tau5", "ttotal", "psi0", "psi3", "alpha", "alpha1", "alpha2", "alpha3", "alpha4", "alpha5", "alpha6", "beta", "f_final", "snr", "chisq", "chisq_dof", "bank_chisq", "bank_chisq_dof", "cont_chisq", "cont_chisq_dof", "sigmasq", "rsqveto_duration", "Gamma0", "Gamma1", "Gamma2", "Gamma3", "Gamma4", "Gamma5", "Gamma6", "Gamma7", "Gamma8", "Gamma9", "spin1x", "spin1y", "spin1z", "spin2x", "spin2y", "spin2z", "event_id")

all_coinc_rows = ("coinc_event:coinc_event_id", "combined_far", "end_time", "end_time_ns", "false_alarm_rate", "ifos", "mass", "mchirp", "minimum_duration", "snr")

all_coinc_event_rows = ("coinc_definer:coinc_def_id", "coinc_event_id", "instruments", "likelihood", "nevents", "process:process_id", "time_slide:time_slide_id")

all_coinc_map_rows = {"coinc_event:coinc_event_id", "event_id", "table_name"}

all_process_rows = ("comment", "cvs_entry_time", "cvs_repository", "domain", "end_time", "ifos", "is_online", "jobid", "node" , "process_id", "program", "start_time", "unix_procid", "username", "version")

### GLOBAL CONSTANTS ###
SUBTHRESHOLD = 1.
ONE_PER_HOUR = 1. / 3600.
TWO_PER_DAY = 2. / 3600. / 24.
ONE_PER_MONTH = 1. / 3600. / 24. / 30.
TWO_PER_YEAR = 1. / 3600. / 24. / 365.25

FARSTRINGS_DICT = {
	SUBTHRESHOLD: 'subthreshold',
	ONE_PER_HOUR: 'oneperhour',
	TWO_PER_DAY: 'twoperday',
	ONE_PER_MONTH: 'onepermonth',
	TWO_PER_YEAR: 'twoperyear',
}
#########################

def add_general_opts():
	parser = OptionParser()
	parser.add_option('--data-source', metavar = 'string', action = 'append', help = 'Source of test suite data. Options: fake-data, gstlal, mbta, pycbc, superevents. Can only be given once (FIXME).')
	parser.add_option('--tag', help = 'The tag used to uniquely identify the analysis you wish to process metrics from. Used as Kafka group ID.')
	parser.add_option('--kafka-server', metavar = 'string', help = 'Sets the url for the kafka broker.')
	parser.add_option('--analysis-dir', metavar='path', help = '')
	parser.add_option('--inj-file', metavar='file', help='')
	parser.add_option('--input-topic', metavar = 'string', action='append', help = 'The Kafka topic(s) to subscribe to.')
	parser.add_option('--gracedb-server', metavar='string', help = 'GraceDb server to use. Valid options are gracedb, gracedb-playground, and gracedb-test.')
	parser.add_option('--verbose', default=False, action="store_true", help = 'Be verbose.')

	return parser

def set_up_logger(verbose):
	logging.getLogger()
	if verbose:
		log_level = logging.DEBUG
	else:
		log_level = logging.INFO

	handler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logging.getLogger('').addHandler(handler)
	logging.getLogger('').setLevel(log_level)

def load_xml(f):
	if isinstance(f, str):
		f = BytesIO(f.encode("utf-8"))
	xmldoc = ligolw_utils.load_fileobj(f, contenthandler = LIGOLWContentHandler)

	return xmldoc

def load_filename(f):
	xmldoc = ligolw_utils.load_filename(f, contenthandler = LIGOLWContentHandler)

	return xmldoc

def event_window(t):
	"""
	returns the event window representing the event
	"""
	dt = 0.2
	return segment(floor_div(t - dt, 0.5), floor_div(t + dt, 0.5) + 0.5)

def get_ifos(sngltable):
	ifos = ''
	for row in sngltable:
		if not row.ifo in ifos:
			ifos += str(row.ifo)

	return ifos

def source_tag(simtable):
	mass1 = simtable[0].mass1
	mass2 = simtable[0].mass2
	cutoff = 3 # minimum BH mass

	if mass1 < cutoff and mass2 < cutoff: source = 'BNS'
	elif mass1 >= cutoff and mass2 >= cutoff: source = 'BBH'
	else: source = 'NSBH'
	return source

def parse_msg_topic(message):
	datasource, tag, _, topic = message.topic().split('.')
	return datasource, tag, topic

def parse_msg_key(message):
	try:
		key = message.key().decode("utf-8")
	except AttributeError:
		key = "None"
	return key

def find_nearest_msg(msgs, t):
	# get injections close to the event end time
	delta = 1.0

	# construct a list of tuples (msg, Delta_t) where Delta_t is the difference in time
	# between this msg and the input time, sort by Delta_t, and take the first element
	# in the list which corresponds to the msg closest to the input time
	nearest_msg = None
	try:
		near_msgs = list((msg, abs(msg['time'] - t)) for msg in msgs if t - delta <= msg['time'] <= t + delta)
		if near_msgs:
			nearest_msg = sorted(near_msgs, key = lambda x: x[1])[0][0]

			logging.debug(f'Time to search for: {t} | Nearest msg time: {nearest_msg["time"]}')
	except Exception as e:
		logging.debug(f'Error: {e}')
	return nearest_msg

def decisive_snr(sngl_snrs, ifos):
	# if no ifos, assume all were off
	if ifos == 'None':
		return 0.

	ifos = ifos.split(',')
	sngl_snrs = [sngl_snrs[ifo] for ifo in ifos]

	# for single time, use the most sensitive IFO
	if len(ifos) == 1:
		return sorted(sngl_snrs, reverse=True)[0]
	# for coinc time, use the SNR of the second most sensitive IFO
	elif len(ifos) >= 2:
		return sorted(sngl_snrs, reverse=True)[1]

def network_snr(snrs):
	return numpy.linalg.norm([x for x in snrs if x])

def effective_spin(m1, m2, s1z, s2z):
	return (m1 * s1z + m2 * s2z) / (m1 + m2)

def effective_precession_spin(m1, m2, s1x, s1y, s2x, s2y):
	### see 10.1103/PhysRevD.91.024043
	# determine the primary mass
	if m2 >= m1:
		m_pri = m2
		m_sec = m1
		s_pri = numpy.sqrt(s2x**2. + s2y**2.)
		s_sec = numpy.sqrt(s1x**2. + s1y**2.)
	else:
		m_pri = m1
		m_sec = m2
		s_pri = numpy.sqrt(s1x**2. + s1y**2.)
		s_sec = numpy.sqrt(s2x**2. + s2y**2.)

	q = m_pri / m_sec # mass ratio >= 1
	a_pri= 2. + 3. / (2. * q)
	a_sec = 2. + 3. * q / 2.

	# equation (3.3)
	sp = max(a_pri * s_pri, a_sec * s_sec)

	# equation (3.4)
	return sp / (a_pri * m_pri**2.)

def calc_mu(mass1, mass2, spin1z, spin2z):
	# Calculate the first orthogonal PN phase coefficient
	# see https://arxiv.org/abs/2007.09108

	M = mass1 + mass2
	mchirp = (mass1 * mass2)**0.6/M**0.2
	eta = mass1 * mass2 / M**2
	beta = ((113. * (mass1 / M)**2 + 75. * eta) * spin1z + (113. * (mass2 / M)**2 + 75. * eta) * spin2z) / 12.

	# the reference frequency below is taken from the literature. Please note
	# that the coefficients in the resultant linear combination depend on the
	# fref.
	fref = 200
	norm = G_SI * MSUN_SI / C_SI**3
	v = numpy.pi * mchirp * fref * norm
	psi0 = 3. / 4 / (8 * v)**(5./3)
	psi2 = 20. / 9 * (743./ 336 + 11. / 4 * eta) / eta**(0.4) * v**(2./3) * psi0
	psi3 = (4 * beta - 16 * numpy.pi) / eta**0.6 * v * psi0

	# FIXME : the following linear combinations are taken from the ones in the
	# paper above, but this will need to be re-computed with o4 representitive
	# psd.
	mu1 = 0.974 * psi0 + 0.209 * psi2 + 0.0840 * psi3
	mu2 = -0.221 * psi0 + 0.823 * psi2 + 0.524 * psi3
	return mu1, mu2, beta

def eta_from_m1_m2(m1, m2):
	# symmetric mass ratio from component masses
	m1 = float(m1)
	m2 = float(m2)
	return (m1 * m2) / (m1 + m2)**2.

def mchirp_from_m1_m2(m1, m2):
	# chirp mass from component masses
	m1 = float(m1)
	m2 = float(m2)
	return (m1 * m2)**(3./5.) / (m1 + m2)**(1./5.)

def preferred_event_func(func):
	if func == 'max' or func == 'latest':
		return max
	elif func == 'min' or func == 'first':
		return min
	else:
		raise NotImplementedError

def parse_dq_topic(topic):
	pipeline, tag, topic = topic.split('.')
	ifo, topic = topic.split('_')

	return pipeline, tag, ifo, topic

def participating_ifos(sngltable):
	ifos = ''
	for r in sngltable:
		if r.snr >= 4.:
			ifos += r.ifo
	return sort_ifos(ifos)

def sort_ifos(string):
	if not string:
		return 'None'
	else:
		# return the sorted string of IFOs in alphabetical order
		list = string.split(',')
		list.sort()
		return ','.join(list)

def far_string(far, to_float = False):
	"""
	we want to tag all of the event messages
	with a string indicated their FAR.
	Thresholds are:
		* 1 per hour
		* 2 per day
		* 1 per month
		* 2 per year
	The far tag is a comma delimited string of
	each threshold that is passed.

	Input:
		far: can be a string "oneperhour", "twoperday", "onepermonth", "twoperday". or a float
		to_float: if True, convert far string to float and return
	"""

	print(f'far: {far} | type: {type(far)}', file = sys.stderr)
	if isinstance(far, str):
		# convert to float
		far = list(FARSTRINGS_DICT.keys())[list(FARSTRINGS_DICT.values()).index(far)]
		print(f'float far: {far}')
		if to_float:
			return far

	far_string = []
	for key, value in FARSTRINGS_DICT.items():
		print(f'thresh: {key}', file = sys.stderr)
		if far <= key:
			far_string.append(value)
			print(f'far string: {far_string}', file = sys.stderr)

	return ' '.join(far_string)
