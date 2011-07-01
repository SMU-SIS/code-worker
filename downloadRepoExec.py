#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Downloads files from a repo. Param: argv[1]
# Locates the file in the downloaded repo to execute: Param argv[2]

import sys,os
from commands import getoutput as cmd

fileFound = False

# Reads the arguments from the command prompt
# If there are 3 arguments then it contains the 
# 	repository name and the file to be executed
# Else it sets to default values
args = sys.argv
if len(args)==3:
	repoFolder = args[1]
	fExecute = args[2]
else:
	repoFolder = 'downloadTestRepo'
	fExecute = 'hello.py'

# If the directory exists, update the folder with
# the latest code from git
if os.path.exists(repoFolder):
	os.chdir(repoFolder)
	print('Updating git repository to latest version: %s' % (repoFolder))
	os.system('git pull')
else:
	print('Cloning git repository: %s' % (repoFolder))
	os.system('git clone git@github.com:karthikmswamy/' + repoFolder + '.git ' + repoFolder)
	os.chdir(repoFolder);

dirList = os.listdir('.')

for fName in dirList:
	if fName.lower().strip() == fExecute:
		fileFound = True

if fileFound == True:
	print('File ' + fExecute + ' found in ' + repoFolder + '. Executing with output...')
	try:
		os.system('python ' + fExecute)
	except OSError:
		pass
else:
	print('No file named ' + fExecute + ' found in ' + repoFolder)
