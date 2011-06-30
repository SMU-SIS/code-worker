#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, json
f = urllib2.urlopen('http://dl.dropbox.com/u/4972572/get_next_job')
#f = urllib2.urlopen('http://www.reddit.com/.json')

jsonStr = json.load(f)

print jsonStr
print jsonStr['repo']
print jsonStr['command']
print jsonStr['job_type']
f.close()
