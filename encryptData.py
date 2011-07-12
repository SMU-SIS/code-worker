#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Module definition for encrypting/decrypting data using JSON

import json
# Assuming appID and sPwd would be encrypted
def encryptDESAndWriteData(appID, sPwd, fileName, key):
	ciphAppID = encrypt(key, appID)
	ciphPwd = encrypt(key, sPwd)

	f = open(fileName, "w")
	fString = json.dumps({"GAppID":ciphAppID, "ServPwd": ciphPwd})
	print fString
	f.write(fString)
	f.close()
	return 'Successful write'

def readDataAndDecryptDES(fileName, key):
	f = open(fileName, "r")
	decStr = json.loads(f.read())
	appid = decrypt(key, decStr['GAppID'])
	uname = decrypt(key, decStr['ServPwd'])
	f.close()
	return appid,uname

def encrypt(key, msg):
	encrypted = []
	for i, c in enumerate(msg):
		key_c = ord(key[i % len(key)])
		msg_c = ord(c)
		encrypted.append(chr((msg_c + key_c) % 127))
	return ''.join(encrypted)

def decrypt(key, encrypted):
	msg = []
	for i, c in enumerate(encrypted):
		key_c = ord(key[i % len(key)])
		enc_c = ord(c)
		msg.append(chr((enc_c - key_c) % 127))
	return ''.join(msg)
