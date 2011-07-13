#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Reads jobs and models from the given URL
# Clones a repo retrieved from data retrieved from the URL
# Executes a file and logs the result from the downloaded repo

import urllib2, json, os, math, time, subprocess
from commands import getoutput as cmd

baseURL = 'http://code-comparison.appspot.com/rest/'

# The main worker thread that fetches a job
def mainWorker():
	URL = baseURL + 'metadata'
	f = urllib2.urlopen(URL)

	jsonStr = json.load(f)
	for i in range(0, len(jsonStr['type'])):
		# Set this condition as there are no test jobs for Worker
		if jsonStr['type'][i].strip().lower() != 'Worker':
			fetchJobFromURL(jsonStr['type'][i])
	f.close()

# Fetches a job from a given URL
# Params: job - the type of the job as string, to be retrieved
def fetchJobFromURL(job):
	# Concatenate with the base URL
	URL = baseURL + job + '?feq_jobType=TEST&fne_status=PROCESSED'
	itr = 0
	while True:
		itr = itr + 1
		f = urllib2.urlopen(URL)
		req = f.read()

		jobStr = json.loads(req)
		numJobs = len(jobStr)
		print 'There are ' + str(numJobs) + ' TEST jobs pending'
		# There are no jobs pending, hence sleep and check again
		if numJobs == 0:
			# Checks to see if there are jobs available every 2^iteration
			# Once time reaches 64, it checks constantly every minute
			sleepTime = math.pow(2,itr)
			if sleepTime < 64:
				print 'Checking back in ' + str(sleepTime) + ' seconds'
				time.sleep(sleepTime)
				continue
			else:
				print 'Checking back every minute'
				time.sleep(60)
				continue

		for i in range(0, numJobs):
			itr = 0
			if jobStr[i]['jobType'] != 'KEVIN':
				fetchURL = baseURL + job + '/' + jobStr[i]['key']
				fetchModelFromURL(fetchURL)

# Fetches a job from a given URL using the key
# Params: URL - the URL as string, of the job to be retrieved
def fetchModelFromURL(URL):
	print 'Processing job from : ' + URL
	u = urllib2.urlopen(URL)
	req = u.read()

	modelStr = json.loads(req)
	# Obtain the repository and command strings

	tarRepos = modelStr['target'].strip()
	masRepos = modelStr['master'].strip()
	fExecute = modelStr['command']

	# Obtain the folder from the git URL
	sp = tarRepos.partition('/')
	tarRepoFolder = sp[2].replace('.git','')
	sp = masRepos.partition('/')
	masRepoFolder = sp[2].replace('.git','')

	# Clone the master and target repos
	print '----------Master:' + masRepos
	gitCloneUpdateRepo(masRepos, 'master', masRepoFolder, fExecute)
	print '----------Target:' + tarRepos
	gitCloneUpdateRepo(tarRepos, 'target', tarRepoFolder, fExecute)

	# Execute the command retrieved from the JSON string
	# Execute the command above the master, target dir
	fContents = ''
	JSONValid = False
	print os.path.abspath('.') + '<------------'
	print('Executing \"' + fExecute + '\"')

	# Capturing output of the device on log.txt
	fnull = open('log.txt', 'w')
	result = subprocess.call(fExecute, shell = True, stdout = fnull, stderr = fnull)
	fnull.close()

	if os.path.isfile('ccresult.json'):
		f = open('ccresult.json','r+')
		fContents = f.read()
		f.write('')
		f.close()
		JSONValid = checkForJSONValidity(fContents)

	f = open('log.txt', 'r+')
	log = f.read()
	f.write('')
	#print 'Log: ' + log
	f.close

	if JSONValid:
		data = json.dumps({'status':'PROCESSED', 'log':log, 'jsonResult':fContents})
	else:
		data = json.dumps({'status':'PROCESSED', 'log':log, 'jsonResult':'Invalid JSON'})
	fContents = ''
	#print 'Data: ' + data
	result = json.loads(urllib2.urlopen(urllib2.Request(URL, data, {'Content-Type': 'application/json'})).read())
	print 'Logs updated'


def gitCloneUpdateRepo(repoFolder, parentName, folderName, fExecute):
	# Master or target?
	os.chdir(parentName)

	# If the directory exists, update the folder with
	# the latest code from git
	# Else clone the repository
	if os.path.exists(folderName):
		os.chdir(folderName)
		print('Updating git repository to latest version: %s' % (folderName))
		os.system('git pull')
		os.chdir('..')
	else:
		print('Cloning git repository: %s' % (folderName))
		os.system('git clone ' + repoFolder + ' ' + folderName)

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
