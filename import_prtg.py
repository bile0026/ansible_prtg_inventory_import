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

search_payload = "content=devices&columns=objid,device,status,name,active,host,group,tags&filter_tags=@tag("+tag+")&username="+user+"&passhash="+password+""

headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

url = "https://"+server+"/api/table.json?"
api_search_string = url + search_payload
req = requests.get(api_search_string, params=search_payload, headers=headers, verify=False)

#print(api_search_string)
#print(req.text)

jsonget = req.json()
devices = jsonget["devices"]

#print(jsonget.values())
print(devices)

for a in devices:
    print(a["host"]+" "+ a["name"])

use_groups = False

# class prtgInventory(object):
#     #CLI parameters
#     def read_cli(self):
#         parser = argparse.ArgumentParser()
#         parser.add_argument('--host')
#         parser.add_argument('--list', action='store_true')
#         self.options = parser.parse_args()

#     def __init__(self):
#         self.inventory = {}
#         self.read_cli_args()

#         # Called with `--list`.
#         if self.args.list:
#             self.inventory = self.get_list()
#             if use_groups:
#                 self.groups = self.get_groups()
#                 self.add_groups_to_hosts(self.groups)
#         # Called with `--host [hostname]`.
#         elif self.args.host:
#             # Not implemented, since we return _meta info `--list`.
#             self.inventory = self.empty_inventory()
#         # If no groups or vars are present, return empty inventory.
#         else:
#             self.inventory = self.empty_inventory()

#         print(json.dumps(self.inventory, indent=2))

#     def get_list(self):
#         hostsData = jsonget
#         data_dump = eval(json.dumps(jsonget))

#         # Inject data below to speed up script
#         final_dict = {'_meta': {'hostvars': {}}}

#         # Loop hosts in groups and remove special chars from group names
#         for m in data_dump['results']:
#             # Allow Upper/lower letters and numbers. Replace everything else with underscore
#             m[groupField] = self.clean_inventory_item(m[groupField])
#             if m[groupField] in final_dict:
#                 final_dict[m[groupField]]['hosts'].append(m[hostField])
#             else:
#                 final_dict[m[groupField]] = {'hosts': [m[hostField]]}
#         return final_dict

#             #if self.args.groups:
#     def get_groups(self):
#         req = requests.get(url, params=group_payload, verify=False, auth=(user, password))
#         hostsData = req.json()
#         data_dump = eval(json.dumps(hostsData))

#         parentField = 'ParentGroupName'
#         childField = 'ChildGroupName'
#         final_dict = {}
#         for m in data_dump['results']:
#             # Allow Upper/lower letters and numbers. Replace everything else with underscore
#             m[parentField] = self.clean_inventory_item(m[parentField])
#             m[childField] = self.clean_inventory_item(m[childField])
#             if m[parentField] in final_dict:
#                 final_dict[m[parentField]]['children'].append(m[childField])
#             else:
#                 final_dict[m[parentField]] = {'children': [m[childField]]}
#         return final_dict


#     def add_groups_to_hosts (self, groups):
#         self.inventory.update(groups)

#     @staticmethod
#     def clean_inventory_item(item):
#         item = re.sub('[^A-Za-z0-9]+', '_', item)
#         return item

#     # Empty inventory for testing.
#     def empty_inventory(self):
#         return {'_meta': {'hostvars': {}}}

#     # Read the command line args passed to the script.
#     def read_cli_args(self):
#         parser = argparse.ArgumentParser()
#         parser.add_argument('--list', action='store_true')
#         parser.add_argument('--host', action='store')
#         self.args = parser.parse_args()

# # Get the inventory.
# prtgInventory()
