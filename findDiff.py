#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Finds the diff of two directories

import os
from commands import getoutput as cmd

# Params: dir1 - string - path of directory 1 to be compared, dir2 - path of directory 2 to be compared
# logFileName - string - full path of the file, which stores the log for the diff operation
def findDiffOfDirs(dirName1, dirName2, logFileName):
	if os.path.exists(dirName1) and os.path.exists(dirName2):
		os.system('diff -r -N ' + dirName1 + ' ' + dirName2 + '>' + logFileName)
		return 'Diff completed and stored in ' + logFileName
	else:
		return 'Please check folders which need comparison'
