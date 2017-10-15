#!/usr/bin/python3
import sys
import unittest
import subprocess


MODULE = sys.modules['__main__'].__file__
__version__ = "0.0.1"
DESCRIPTION = MODULE+""":
High level test: Run the main program and check for correct output
"""
EXAMPLE_USAGE = """"""


class TestProgram(unittest.TestCase):
	PROGRAM_NAME = "template_main.py"
	ARG_INVALID = "--invalidargument"
	ARG_HELP = "--help"
	ARG_VERSION = "--version"
	ARG_CFGF = "--config"
	ARG_INPUT = "-i"
	ARG_OUTPUT = "-o"
	TEST_CONFIG_FILE = ""
	INVALID_CONFIG_FILE = "nonexistantfile"

	def test_emptyInput(self):
		self.assertEqual(subprocess.run(["python3",
		                                 TestProgram.PROGRAM_NAME],
		                                stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode, 0)

	def test_invalidArg(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_INVALID], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, 2)
		self.assertTrue(res.stderr.decode("utf-8").startswith("usage: "+TestProgram.PROGRAM_NAME))
		
	def test_help(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_HELP], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, 0)
		self.assertTrue(res.stdout.decode("utf-8").startswith("usage: "+TestProgram.PROGRAM_NAME))

	def test_version(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_VERSION], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, 0)
		self.assertTrue(res.stdout.decode("utf-8"))

	def test_noConfig(self):
		res = subprocess.run(["python3",
		                      TestProgram.PROGRAM_NAME,
		                      TestProgram.ARG_CFGF,TestProgram.INVALID_CONFIG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.assertEqual(res.returncode, 2)
		self.assertTrue(res.stderr.decode("utf-8").startswith("usage: "+TestProgram.PROGRAM_NAME))
		self.assertTrue(res.stderr.decode("utf-8").endswith(TestProgram.PROGRAM_NAME+": error: File not found: "+TestProgram.INVALID_CONFIG_FILE+"\n"))


if __name__ == '__main__':
	unittest.main()
