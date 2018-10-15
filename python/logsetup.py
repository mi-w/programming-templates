import os
import sys
import json
import logging
import logging.handlers
import logging.config

# Logging (see https://pypi.python.org/pypi/logging_levels):
from logging_levels import isolated_logging, log_exceptions
from logging_levels.standards import add_standards

def setupLogger(configfile="./logger.cfg", consoleLevel="INFO", logDir="./", logFile="default.log"):
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
	add_standards(logging)

	if os.path.exists(configfile):  # load configuration form file
		with open(configfile, "rt") as f:
			cfg = json.load(f)
			# Set logfile location if not in config:
			if not cfg["handlers"]["file"].get("filename"): cfg["handlers"]["file"]["filename"] = logDir+logFile
			# Overwrite console log level
			if cfg["handlers"].get("console"): cfg["handlers"]["console"]["level"] = consoleLevel
			# Set config
			logging.config.dictConfig(cfg)
	else:
		logging.basicConfig()
	log = logging.getLogger(sys.modules['__main__'].__file__)
	log.trace("Logger set up")
	return log
