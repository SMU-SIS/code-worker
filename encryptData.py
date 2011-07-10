#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Module definition for encrypting/decrypting data using JSON

import base64, json
# Assuming appID and sPwd would be encrypted
def encryptBZ2AndWriteData(appID, sPwd, fileName):
	encAppID = base64.b64encode(appID)
	encSPwd = base64.b64encode(sPwd)
	f = open(fileName, "w")
	fString = json.dumps({"GAppID":encAppID, "ServPwd": encSPwd})
	print fString
	f.write(fString)
	f.close()
	return 'Successful write'

def readDataAndDecryptBZ2(fileName):
	f = open(fileName, "r")
	decStr = json.loads(f.read())
	print base64.b64decode(decStr['GAppID'])
	print base64.b64decode(decStr['ServPwd'])
	f.close()
	return 'Successful read'
