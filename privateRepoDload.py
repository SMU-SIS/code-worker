#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Download private repos

import encryptData, os

from commands import getoutput as cmd
from github2.client import Github
from encryptData import encryptDESAndWriteData

appid,uname = encryptData.readDataAndDecryptDES('keys.txt', 'code-comparison')

# GitHub configurations
GITHUB_USER = uname
GITHUB_TOKEN = appid

# API Object
github = Github(username=GITHUB_USER, api_token=GITHUB_TOKEN)


