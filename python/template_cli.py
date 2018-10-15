#!/usr/bin/env python
# encoding: utf-8

"""Minimal python commad line template."""

# System packages
import os
import sys
import logging
# Commandline parameters & Config file
import configargparse

# Custom packages
from logsetup import setupLogger


PROGRAM = "Template"
MODULE = sys.modules['__main__'].__file__
__version__ = "0.0.1"
DESCRIPTION = MODULE+""":
TODO
"""
EXAMPLE_USAGE = """"""



def setupArguments():
	"""Setup argument parser for commandline arguments.
	and Config file. The priority is (low to high):
	Default value, config file value, commandline value
	"""

	LOGGER_LEVELS = ["TRACE", "VERBOSE", "DEBUG", "INFO", "NOTICE", "WARNING", "SUPPRESSED", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"]
	formatter_class = configargparse.RawDescriptionHelpFormatter
	p = configargparse.ArgParser(description=DESCRIPTION,
	                             epilog=EXAMPLE_USAGE,
	                             default_config_files=[PROGRAM+".cfg"],
	                             formatter_class=formatter_class)
	p.add("--version", action="version", version="%(prog)s {}".format(__version__))
	p.add("--config", required=False, is_config_file=True, help="Config file for this program")
	p.add("--logger-config", required=False, dest="logconfig", default="./logger.cfg", type=str, help="Logger config file for this program")
	p.add("--log-level", metavar="LEVEL", dest="loglevel", type=str, choices=LOGGER_LEVELS,
	      default="INFO", help="Sets console log level. Valid Values are "+', '.join(LOGGER_LEVELS))

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
