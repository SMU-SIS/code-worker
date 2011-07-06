#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, json

baseurl = 'http://code-comparison.appspot.com/rest/'                        

def get_unprocessed_test_jobs():
  url = baseurl+'Job?feq_jobType=TEST&fne_status=PROCESSED'                   
  data = None                                                                 
  result = json.loads(urllib2.urlopen(urllib2.Request(url, data, {'Content-Type': 'application/json'})).read())
  print 'There are currently', len(result), 'unprocessed TEST jobs.'
  return result

#You can filter results on the REST interface using feq_ and fne_. 
#This means that we can make sure that there are no jobs of jobType=TEST& status!=PROCESSED. If there are, we can mark all the TEST jobs as PROCESSED.  

result = get_unprocessed_test_jobs()

for k in result:
  data = json.dumps({'status':'PROCESSED'})
  url = baseurl + 'Job/'+k['key']
  result = json.loads(urllib2.urlopen(urllib2.Request(url, data, {'Content-Type': 'application/json'})).read())
  print 'Marking existing TEST job as PROCESSED'
  
#Now that we now that there are no TEST jobs that have not been marked as PROCESSED, we can create some new TEST jobs for the worker to process. 
result = get_unprocessed_test_jobs()

test_jobs = [{'command':'python -V', 'jobType':'TEST'}, 
			 {'command':'java -version', 'jobType':'TEST'}, 
			 {'command':'git --version', 'jobType':'TEST'}, 
			 {'command':'python code-worker/tasks/pep8/pep8.py -h', 'jobType':'TEST'},
			 {'command':'python code-worker/tasks/clonedigger/clonedigger.py -h', 'jobType':'TEST'}, 
			 #{'command':'code-worker/tasks/pep8/pep8.py -h', 'jobType':'TEST'}, #let pep8.py be executible without typing python or path
			 #{'command':'code-worker/tasks/clonedigger/clonedigger.py -h', 'jobType':'TEST'}, 
			 {'command':'python code-worker/tasks/pep8/pep8.py target --count -qq', #target repo should be downloaded to target directory. master repo should be downloaded to master directory
			  'target':'git@github.com:SMU-SIS/code-worker.git',
			  'jobType':'TEST'},
			 ]

for job in test_jobs:
  url = baseurl+'Job'
  data = json.dumps(job)
  print 'Creating job to run command', url, data                  
  result = json.loads(urllib2.urlopen(urllib2.Request(url, data, {'Content-Type': 'application/json'})).read())

result = get_unprocessed_test_jobs()

# Now check back every 10 seconds to see if the TEST jobs have been processed by the worker. If they don't all get processed in a minute or two, the integration test would fail.   
# The next time this script is run, all these TEST jobs well be marked as PROCESSED
