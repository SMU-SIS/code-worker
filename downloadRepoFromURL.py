#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Downloads files from a repo retrieved from the URL
# Locates the file in the downloaded repo by parsing the JSON

import urllib2, json, sys, os
from commands import getoutput as cmd

# Reads the arguments from the command prompt
# If there are 3 arguments then it contains the 
# 	repository name and the file to be executed
f = urllib2.urlopen('http://dl.dropbox.com/u/4972572/get_next_job')

# Decode the JSON string from URL
jsonStr = json.load(f)
f.close()

# Obtain the repository and command strings
repos = jsonStr['repo'].strip()
fExecute = jsonStr['command'].strip()

# Obtain the folder from the git URL
sp = repos.partition('/')
repoFolder = sp[2].replace('.git','')

# If the directory exists, update the folder with
# the latest code from git
# Else clone the repository
if os.path.exists(repoFolder):
	os.chdir(repoFolder)
	print('Updating git repository to latest version: %s' % (repoFolder))
	os.system('git pull')
else:
	print('Cloning git repository: %s' % (repoFolder))
	os.system('git clone ' + repos + ' ' + repoFolder)
	os.chdir(repoFolder);

# Execute the command retrieved from the JSON string
print('Executing \"' + fExecute + '\" with output...')
try:
	os.system(fExecute)
except OSError:
	pass
