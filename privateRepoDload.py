#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Karthik Muthuswamy
# Download private repos

import encryptData, os

from commands import getoutput as cmd
from github2.client import Github
from encryptData import encryptDESAndWriteData

appid,uname = encryptData.readDataAndDecryptDES('keys.txt', '')

# GitHub configurations
GITHUB_USER = uname
GITHUB_TOKEN = appid

# API Object
github = Github(username=GITHUB_USER, api_token=GITHUB_TOKEN)

# repo slots
repos = {}
repos['private'] = []
repos['public'] = []

# Collect GitHub repos via API
for repo in github.repos.list():

    if repo.private:
        repos['private'].append(repo)
    else:
        repos['public'].append(repo)


for org, repos in repos.iteritems():
    for repo in repos:

        try:
            os.makedirs(org)
        except OSError:
            pass

        os.chdir(org)

        private = True if org in ('private') else False

        # just `git pull` if it's already there
        if os.path.exists(repo.name):
            os.chdir(repo.name)
            print('Updating repo: %s' % (repo.name))
            os.system('git pull')
            os.chdir('..')
        else:
            if private:
                print('Cloning private repo: %s' % (repo.name))
                os.system('git clone git@github.com:%s/%s.git' % (repo.owner, repo.name))
            else:
                print('Cloning repo: %s' % (repo.name))
                os.system('git clone git://github.com/%s/%s.git' % (repo.owner, repo.name))

        os.chdir('..')
        print

