###################################################
# Workflow: delete device groups, delete devices
###################################################

###################################################
# requirements: pip install requests
###################################################

###################################################
# usage:
# vi variable.yml
# python ./delete_healthbot_configuration
###################################################

###################################################
# This block indicates the various imports
###################################################

import os
import json
import yaml
import requests
from jinja2 import Template
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint

##################################################
# This block defines the functions we will use
###################################################

def import_variables_from_file():
    my_variables_file=open('variables.yml', 'r')
    my_variables_in_string=my_variables_file.read()
    my_variables_in_yaml=yaml.load(my_variables_in_string)
    my_variables_file.close()
    return my_variables_in_yaml

def get_devices_name_in_running_configuration():
    r = requests.get(url + '/device/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the list of devices in the running configuration"
    pprint(r.json())
    return r.json()

def get_devices_details_in_running_configuration():
    r = requests.get(url + '/devices/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the devices details in the running configuration "
    pprint (r.json())
    return r.status_code

def get_devices_name_in_candidate_configuration():
    r = requests.get(url + '/device/?working=true', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the list of devices in the candidate configuration"
    pprint(r.json())
    return r.status_code

def get_devices_details_in_candidate_configuration():
    r = requests.get(url + '/devices/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the devices details in the candidate configuration "
    pprint (r.json())
    return r.status_code

def commit():
    r = requests.post(url + '/configuration', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print 'healthbot configuration commited'
    return r.status_code

def delete_device(dev):
    r = requests.delete(url + '/device/' + dev + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print 'deleted the healthbot configuration for device_' + dev
    return r.status_code

def get_device_groups():
    r = requests.get(url + '/device-group/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the list of device groups in the running configuration"
    pprint (r.json())
    return (r.json())

def delete_device_group(group):
    r = requests.delete(url + '/device-group/'+ group + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    return r.status_code

def get_notifications():
    r = requests.get(url + '/notification/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    print "here's the notifications in the ruuning configuration "
    pprint (r.json())
    return (r.json())


def delete_notification(notification):
    r = requests.delete(url + '/notification/' + notification + '/', auth=HTTPBasicAuth(authuser, authpwd), headers=headers, verify=False)
    return r.status_code


######################################################
# Below blocks are REST calls to configure healthbot
######################################################

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
my_variables_in_yaml=import_variables_from_file()
server = my_variables_in_yaml['server']
authuser = my_variables_in_yaml['authuser']
authpwd = my_variables_in_yaml['authpwd']
url = 'https://'+ server + ':8080/api/v1'
headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json' }


######################################################
# This block is to remove device groups from healthbot
######################################################

print '########### Removing device groups  ############'


device_group_in_running_configuration = get_device_groups()

print "removing device groups from healthbot"

for item in device_group_in_running_configuration:
     delete_device_group(item)

commit ()

get_device_groups()


######################################################
# This block is to remove notifications from healthbot
######################################################

print '###########  Removing notifications  ############'


notifications_in_running_configuration = get_notifications()

for item in notifications_in_running_configuration: 
    delete_notification(item)

commit()

get_notifications()



######################################################
# This block is to remove devices from healthbot
######################################################

print '###########  Removing devices  ############'


devices_name_in_running_configuration = get_devices_name_in_running_configuration()

print "removing devices from healthbot"

for dev in devices_name_in_running_configuration:
    delete_device(dev)

get_devices_name_in_candidate_configuration()

commit()

get_devices_name_in_running_configuration()

