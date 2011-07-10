#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Test for encrpyt/decrypt

import encryptData, findDiff
from encryptData import encryptBZ2AndWriteData, readDataAndDecryptBZ2
from findDiff  import findDiffOfDirs

# Test inputs for GAppID and SPwd - success
print encryptData.encryptBZ2AndWriteData('GoogleAppID', 'ServerPwd', 'keys.txt')
print encryptData.readDataAndDecryptBZ2('keys.txt')

# Test inputs for dir1 and dir2 - success
print findDiff.findDiffOfDirs('code-worker','code-worker/code-worker','log')
