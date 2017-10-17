#!/usr/bin/python3
import os
import sys
import logging
from logging_levels.standards import add_standards
import unittest
import subprocess
from pathlib import Path

MODULE = sys.modules['__main__'].__file__
__version__ = "0.0.1"
DESCRIPTION = MODULE+""":
High level test: Run the main program and check for correct output
"""
EXAMPLE_USAGE = """"""
add_standards(logging)

class TestProgram(unittest.TestCase):
	PROGRAM_NAME = "template_main.py"
	RET_OK = 0
	RET_ARGERR = 2
	ARG_INVALID = "--invalidargument"
	ARG_HELP = "--help"
	ARG_VERSION = "--version"
	ARG_CFGF = "--config"
	ARG_INPUT = "-i"
	ARG_OUTPUT = "-o"
	INVALID_FILE = "nonexistantfile"
	TMP_INPUT_FILE = "tmpinput.tmp"
	TMP_OUTPUT_FILE = "tmpoutput.tmp"
	TEST_CONFIG_FILE = ""
	TEST_PW_FILE = "./testpwfile.txt"
	log = logging.getLogger(__name__)

	def setUp(self):
		pass  # TODO: setupLogger

	def test_emptyInput(self):
		self.assertEqual(subprocess.run(["python3",
		                                 TestProgram.PROGRAM_NAME],
		                                stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode, TestProgram.RET_OK)

	def test_invalidArg(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_INVALID], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, TestProgram.RET_ARGERR)
		self.assertTrue(res.stderr.decode("utf-8").startswith("usage: "+TestProgram.PROGRAM_NAME))
		
	def test_help(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_HELP], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, TestProgram.RET_OK)
		self.assertTrue(res.stdout.decode("utf-8").startswith("usage: "+TestProgram.PROGRAM_NAME))

	def test_version(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_VERSION], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, TestProgram.RET_OK)
		self.assertTrue(res.stdout.decode("utf-8"))

	def test_noConfig(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_CFGF, TestProgram.INVALID_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, TestProgram.RET_ARGERR)
		self.assertTrue(res.stderr.decode("utf-8").startswith("usage: "+TestProgram.PROGRAM_NAME))
		self.assertTrue(res.stderr.decode("utf-8").endswith(TestProgram.PROGRAM_NAME+": error: File not found: "+TestProgram.INVALID_FILE+"\n"))


	def test_loadBadInputFile(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_INPUT, TestProgram.INVALID_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, TestProgram.RET_ARGERR)
		self.assertTrue(res.stderr.decode("utf-8").startswith("usage: "+TestProgram.PROGRAM_NAME))
		self.assertTrue(res.stderr.decode("utf-8").endswith(TestProgram.PROGRAM_NAME+": error: argument -i/--input: can't open '"+TestProgram.INVALID_FILE+"': [Errno 2] No such file or directory: '"+TestProgram.INVALID_FILE+"'\n"))

	def test_loadBadInputContent(self):
		# Load empty file:
		with open(TestProgram.TMP_INPUT_FILE, 'a'): pass  # Create empty file
		try:
			res = subprocess.run(["python3",
								  TestProgram.PROGRAM_NAME,
								  TestProgram.ARG_INPUT, TestProgram.TMP_INPUT_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			self.assertEqual(res.returncode, TestProgram.RET_OK)  # TODO other / further handling

			# Load empty file with linebreak:
			with open(TestProgram.TMP_INPUT_FILE, 'a') as tmpfile: tmpfile.write("\n")
			res = subprocess.run(["python3",
								  TestProgram.PROGRAM_NAME,
								  TestProgram.ARG_INPUT, TestProgram.TMP_INPUT_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			self.assertEqual(res.returncode, TestProgram.RET_OK)  # TODO other / further handling

			#TODO: Check other bad formats
			
		finally:
			# Delete temporary file
			os.remove(TestProgram.TMP_INPUT_FILE)

	def test_loadInput(self):
		#TODO: Check handling of example input
		pass
	
	def test_output(self):
		try:
			res = subprocess.run(["python3",
			                      TestProgram.PROGRAM_NAME,
			                      TestProgram.ARG_OUTPUT, TestProgram.TMP_OUTPUT_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			self.assertEqual(res.returncode, TestProgram.RET_OK)
			self.assertTrue(Path(TestProgram.TMP_OUTPUT_FILE).is_file())
			with open(TestProgram.TMP_OUTPUT_FILE, 'r') as outfile:
				self.assertNotEqual(outfile.read(), "")  # TODO: check content
		finally:
			# Delete test file
			os.remove(TestProgram.TMP_OUTPUT_FILE)
			
if __name__ == '__main__':
	unittest.main()
