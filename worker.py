#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Reads jobs and models from the given URL
# Clones a repo retrieved from data retrieved from the URL
# Executes a file and logs the result from the downloaded repo

import urllib2, json, os
from commands import getoutput as cmd

baseURL = 'http://code-comparison.appspot.com/rest/'

# The main worker thread that fetches a job
def mainWorker():
	URL = baseURL + 'metadata'
	f = urllib2.urlopen(URL)

	jsonStr = json.load(f)
	for i in range(0, len(jsonStr['type'])):
		fetchJobFromURL(jsonStr['type'][i])
	f.close()

# Fetches a job from a given URL
# Params: job - the type of the job as string, to be retrieved
def fetchJobFromURL(job):
	print 'Processing job: ' + job
	# Concatenate with the base URL
	URL = baseURL + job
	f = urllib2.urlopen(URL)
	req = f.read()

	jobStr = json.loads(req)
	for i in range(0, len(jobStr)):
		fetchURL = URL + '/' + jobStr[i]['key']
		fetchModelFromURL(fetchURL)

# Fetches a job from a given URL using the key
# Params: URL - the URL as string, of the job to be retrieved
def fetchModelFromURL(URL):
	data = None
	print 'Processing model from : ' + URL
	u = urllib2.urlopen(URL)
	req = u.read()

	modelStr = json.loads(req)
	# Obtain the repository and command strings
	repos = modelStr['target'].strip()
	fExecute = modelStr['command'].replace('python ','').strip()

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
		if os.path.isfile(fExecute):
			os.system('python ' + fExecute + ' > log.txt')
			if os.path.isfile('ccresult.json'):
				f = open('ccresult.json','r')
				fContents = f.read()
				if checkForJSONValidity(fContents):
					print 'JSON Validity Approved'
				else:
					print 'JSON Validity Not Approved'
	except OSError:
		pass

	os.chdir('..')

# Tests the JSON validity 
# Params: jsonContent - the data as string, which is tested for validity
def checkForJSONValidity(jsonContent):
	try:
		json.loads(jsonContent)
		return True
	except ValueError:
		return False

mainWorker()
