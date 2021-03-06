#!/usr/bin/env python3

'''
Custom dynamic inventory script for Ansible and PRTG, in Python.
This was tested on Python 3.6.8, PRTG 16.1.21.1924, and Ansible  2.9.10.
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
# FQDN for hostname manipulation
domain = config.get('prtg', 'prtg_domain').lower()

# string to be attached to the server url on what to pull back from PRTG.
search_payload = "content=devices&columns=objid,device,status,name,active,host,group,tags& \
    filter_tags=@tag("+tag+")&username="+user+"&passhash="+password+""

# headers
headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

# beginning of API URL
url = "https://"+server+"/api/table.json?"
api_search_string = url + search_payload
req = requests.get(api_search_string, params=search_payload, headers=headers, verify=False)

jsonget = req.json()
devices = jsonget["devices"]

class prtgInventory(object):
    #CLI parameters
    def read_cli(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--host')
        parser.add_argument('--list', action='store_true')
        self.options = parser.parse_args()

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.get_list()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory, indent=2))

    # get list
    def get_list(self):
        hostsData = jsonget

        # Inject data below to speed up script
        final_dict = {'_meta': {'hostvars': {}}}
        #use the one below to overwrite an existing static inventory
        #final_dict = {'_meta': {'hostvars': {}}, 'all': {'children': ['ungrouped']}}

        # Loop hosts in groups and remove special chars from group names
        for m in hostsData['devices']:
            # check for active/available devices and import those
            if m["status"] == "Up":
                # Allow Upper/lower letters and numbers. Replace everything else with underscore
                m["name"] = self.clean_inventory_item(m["name"])
                m["group"] = self.clean_group_name(m["group"])
                #if self.validate_host_string((m["name"])) is True:
                if m["group"] in final_dict:
                    final_dict[m["group"]]['hosts'].append(m["name"])
                else:
                    final_dict[m["group"]] = {'hosts': [m["name"]]}
        return final_dict

    # cleanup hostnames so they are proper
    @staticmethod
    def clean_inventory_item(item):
        # register regex string for valid FQDN
        regex = re.compile(r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)')

        #if ip has no hostname don't add the domain to the end
        result = re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$', item)
        if result:
            return item

        # check for FQDN format, and replace anything else with underscore
        if domain.casefold() in item.casefold():
            # check for match that hostname is already in proper format
            result = re.match(r'^.+[A-Za-z0-9\-\.]\.[A-Za-z]+$', item)
            if result:
                return item.upper()
            else:
                #cleanup the hostname string
                item = re.sub('[_]+', '-', item)
                item = item.replace(" ","")
                # check if there is a properly formatted hostname in ()
                result = re.match(r'.*([\(])([A-Za-z0-9\-\.]+\.[A-Za-z]+[^\)])', item)
                if result:
                    # if hostname is in (), process the string and return it
                    item = re.findall(r'(.+\(([A-Za-z0-9\-\.]+\.[A-Za-z]+[^\)]))', item)
                    item = item[0][1]
                    #check if valid FQDN
                    result = re.match(regex, item)
                    if result:
                        return item.upper()
                else:
                    # if hostname is at the beginning, process the string and return it
                    item = re.findall(r'(^[A-Za-z0-9\-\.]+\.[A-Za-z]+)', item)
                    item = item[0]
                    #check if valid FQDN
                    result = re.match(regex, item)
                    if result:
                        return item.upper()
        else:
            #cleanup the hostname string
            item = re.sub('[^A-Za-z0-9\-\.]+', '_', item)
            item = item.replace(" ","")
            # add domain to the string and try and parse it
            item = item + "." + domain
            # check if valid FQDN
            result = re.match(regex, item)
            if result:
                return item.upper()
            else:
                return "bad_hostname_delete_me_" + item
                print(item + " is not a proper FQDN hostname")

    @staticmethod
    def validate_host_string(item):
        # regex to check for FQDN
        fqdn_result = re.search(r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', item)
        if fqdn_result:
            result = process(fqdn_result)
            return bool(result)

    # cleanup whitespace in group names
    @staticmethod
    def clean_group_name(item):
        item = item.replace(" ", "_")
        return item

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()

# Get the inventory.
prtgInventory()
