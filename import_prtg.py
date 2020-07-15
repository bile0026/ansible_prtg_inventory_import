#!/usr/bin/env python


'''
Custom dynamic inventory script for Ansible and PRTG, in Python.
This was tested on Python 3.8.6, PRTG 16.1.21.1924, and Ansible  2.9.10.
Zachary Biles (zacharybiles@gmail.com)
https://github.com/bile0026/

NOTE:  This software is free to use for any reason or purpose. That said, the
author request that improvements be submitted back to the repo or forked
to something public.
'''

import argparse
import configparser
import requests
import re

try:
    import json
except ImportError:
    import simplejson as json

config_file = 'prtg.ini'

# Read in configuration variables
config = configparser.ConfigParser()
config.readfp(open(config_file))

# PRTG Server IP or DNS/hostname
server = config.get('prtg', 'prtg_server')
# PRTG Username
user = config.get('prtg', 'prtg_user')
# PRTG Password
password = config.get('prtg', 'prtg_passhash')
# PRTG Tag
tag = config.get('prtg', 'prtg_tag')
# Field for groups
groupField = 'GroupName'
# Field for host
hostField = 'SysName'

search_payload = "content=devices&columns=objid,device,status,name,active,host&filter_tags=@tag("+tag+")&username="+user+"&passhash="+password+""

headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

url = "https://"+server+"/api/table.json?"
api_search_string = url + search_payload
req = requests.get(api_search_string, params=search_payload, headers=headers, verify=False)

#print(api_search_string)
#print(req.text)

jsonget = req.json()

print(jsonget)