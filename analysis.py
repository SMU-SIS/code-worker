#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

fName = "ccresult.json"
textToWrite = "{'answer' : 42}"
FILE = open(fName, "w")
FILE.writelines(textToWrite)
FILE.close()

print 'This is an output log from test.py'

