#!/usr/bin/env python
# encoding: utf-8

"""Minimal python commad line template."""

# System packages
import os
import sys
import logging as globalLogger
import logging.handlers
import logging.config

# Logging (see https://pypi.python.org/pypi/logging_levels):
from logging_levels import isolated_logging, log_exceptions
from logging_levels.standards import add_standards
import json
# Commandline parameters & Config file
import configargparse


PROGRAM = "Template"
MODULE = sys.modules['__main__'].__file__
__version__ = "0.0.1"
DESCRIPTION = MODULE+""":
TODO
"""
EXAMPLE_USAGE = """"""


def setupLogger(configfile="./logger.cfg", consoleLevel="INFO", logDir="./", logFile=PROGRAM+".log"):
	""" Setup a console and file logger
	:param consolelevel: Sets the loglevel for the console (string). The file log
	 level is always DEBUG
	:param logDir: Set the destination dir for the logfile.
	:param logFile: The filename of the logfile. If no extension is given '.log'
	 will be appended
	"""
	# Setup directories
	logDir = logDir if logDir.endswith('/') else logDir + '/'
	logFile = logFile if '.' in logFile else logFile + '.log'
	if not os.path.exists(logDir): os.mkdir(logDir)

	# Add more log levels
	add_standards(globalLogger)

	if os.path.exists(configfile):  # load configuration form file
		with open(configfile, "rt") as f:
			cfg = json.load(f)
			# Set logfile location if not in config:
			if not cfg["handlers"]["file"].get("filename"): cfg["handlers"]["file"]["filename"] = logDir+logFile
			# Overwrite console log level
			if cfg["handlers"].get("console"): cfg["handlers"]["console"]["level"] = consoleLevel
			# Set config
			globalLogger.config.dictConfig(cfg)
	else:
		globalLogger.basicConfig()
	log = logging.getLogger(sys.modules['__main__'].__file__)
	log.trace("Logger set up")
	return log


def setupArguments():
	"""Setup argument parser for commandline arguments.
	and Config file. The priority is (low to high):
	Default value, config file value, commandline value
	"""

	formatter_class = configargparse.RawDescriptionHelpFormatter
	p = configargparse.ArgParser(description=DESCRIPTION,
	                             epilog=EXAMPLE_USAGE,
	                             default_config_files=[PROGRAM+".cfg"],
	                             formatter_class=formatter_class)
	p.add("--version", action="version", version="%(prog)s {}".format(__version__))
	p.add("--config", required=False, is_config_file=True, help="Config file for this program")
	p.add("--logger-config", required=False, dest="logconfig", default="./logger.cfg", type=str, help="Logger config file for this program")
	p.add("--log-level", metavar="LEVEL", dest="loglevel", type=str,
	      default="INFO", help="Sets console log level. Valid Values are TRACE, VERBOSE, DEBUG, INFO, NOTICE, WARNING, SUPPRESSED, ERROR, CRITICAL, ALERT, EMERGENCY")

	p.add('-o', "--output", metavar="OUTPUT FILE", dest="outfile", type=configargparse.FileType('w'),
	      default=sys.stdout, help="Set output to a file")
	p.add("-i", "--input", metavar="INPUT FILES", dest="infile", type=configargparse.FileType('r'), nargs='+',
	      help="A list of input files")
	return p.parse_args()

def main():
	"""Main routine"""
	try:
		args = setupArguments()
		log = setupLogger(configfile=args.logconfig, consoleLevel=args.loglevel)
		log.debug(PROGRAM+" started with the following arguments "+str(args))

		log.info("EOP")
		return 0
	except KeyboardInterrupt:
		log.info('Program interrupted!', exc_info=True)
	finally:
		logging.shutdown()

if __name__ == "__main__":
	sys.exit(main())
