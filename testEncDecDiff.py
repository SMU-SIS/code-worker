#!/usr/bin/env python
# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Author: Karthik Muthuswamy
# Test for encrpyt/decrypt

import encryptData, findDiff
from encryptData import encryptDESAndWriteData
from findDiff  import findDiffOfDirs

# Test inputs for GAppID and SPwd - success
#print encryptDESAndWriteData('', '', 'keys.txt', 'code-comparison')
appid,uname = encryptData.readDataAndDecryptDES('keys.txt', 'code-comparison')

# Test inputs for dir1 and dir2 - success
#print findDiff.findDiffOfDirs('code-worker','code-worker/code-worker','log')
=======

import urllib2, json
f = urllib2.urlopen('http://dl.dropbox.com/u/4972572/get_next_job')
#f = urllib2.urlopen('http://www.reddit.com/.json')

jsonStr = json.load(f)

print jsonStr
print jsonStr['repo']
print jsonStr['command']
print jsonStr['job_type']
f.close()
>>>>>>> 2715950050cbe39d6f0d7e8c57aea77daeaa3a1a
