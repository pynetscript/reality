#!/usr/bin/python

###############################################################################
# Written by:           Aleks Lambreca
# Creation date:        24/03/2018
# Last modified date:   19/08/2018
# Version:              v1.3
#
# Script use:           SSH into Cisco IOS devices and run show commands
#                       Note: Commands are run one by one (not all at once)
#                             Supports both IPv4 and IPv6 addresses and FQDNs
#                             Both Py2 and Py3 compatible
#                       The script needs 3 arguments to work:
#                       - 1st argument: cmdrunner.py
#                       - 2nd argument: x.json
#                       - 3rd argument: x.txt
#                       Note: A full command looks like:
#                       ./cmdrunner.py router/7200.json router/cmd.txt
#                       ./cmdrunner.py netbox.json cmd.txt
#
# Script input:         Option 1) Local devices
#                       - Specify devices as a .json file
#                       - Note: See "router/7200.json" as an example
#                       - Specify show commands as a .txt file
#                       - Note: See "router/cmd.txt" as an example
#                       - Username/Password
#                       Option 2) GET devices from Netbox API
#                       - Needs ./cmdrunner.py netbox.json cmd.txt to be used.
#                       - Specify Netbox server IP/FQDN
#                       - Specify API Token
#                       - Specify what to GET
#                       - Username/Password
#                            
# Script output:        Cisco IOS command output
#                       Errors in screen
#                       Progress bar
#                       Statistics
#                       Log success/erros in cmdrunner.log
#                       Travis CI build notification to Slack private channel
###############################################################################


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Standard library modules
import netmiko
import json
import sys                      
import datetime
import time
import logging
import os
import re

from colorama import init
from colorama import Fore
from colorama import Style
from progressbar import *

# Local modules
import tools


# Logs on the working directory on the file named cmdrunner.log
logger = logging.getLogger('__name__')
hdlr = logging.FileHandler('runner.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


# If connection times out, the script will continue to run.
# If authentication fails, the script will continue to run.
netmiko_ex_time = (netmiko.ssh_exception.NetMikoTimeoutException)
netmiko_ex_auth = (netmiko.ssh_exception.NetMikoAuthenticationException)


# If arguments not equal to 3 we get an error.
if len(sys.argv) != 3:
    print(Fore.RED + '>> Usage:', '"' + sys.argv[0].split('/')[-1], 'x.json x.txt"' + Style.RESET_ALL)
    exit()


with open(sys.argv[1]) as dev_file:
    if sys.argv[1].split('/')[-1] == 'netbox.json':
        tools.get_netbox_devices()
        netbox_json = sys.argv[1].split('/')[-1]
        with open(netbox_json, 'r') as devices_tmp:
            devices = json.load(devices_tmp)
    else:
        devices = json.load(dev_file)


with open(sys.argv[2]) as cmd_file:
    commands = cmd_file.readlines()


# Prompt for username and password
print(Fore.WHITE + '='*79 + Style.RESET_ALL)
username, password = tools.get_credentials()


# Script start timestamp and formatting
start_timestamp = datetime.datetime.now()
start_time = start_timestamp.strftime('%d/%m/%Y %H:%M:%S')


# Progress Bar
widgets = ['\n',
           Percentage(), ' ', Bar(marker='#', left='[', right=']'),
           ' ', '[',SimpleProgress(),']',' ' '[', ETA(),']', '\n']

pbar = ProgressBar(widgets=widgets)


for device in pbar(devices):
    device['username'] = username
    device['password'] = password
    try:
        print(Fore.WHITE + '='*79 + Style.RESET_ALL)
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(current_time, '- Connecting to device:', device['ip'])

        # SSH into each device from "x.json" (2nd argument).
        connection = netmiko.ConnectHandler(**device)

        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        #success_connected = (current_time, '- Successfully connected -', device['ip'])
        success_connected = (current_time, '- Connection to device successful:', device['ip'])
        success_connected_str = ' '.join(success_connected)
        print(success_connected_str)
        print('-'*79)

        # Log the successful connection on the working directory in cmdrunner.log
        # Parse out the datestamp
        regex = r'(\d+/\d+/\d+\s+\d+:\d+:\d+\s+-\s+)(.*)'
        m_conn = re.match(regex, success_connected_str)
        logger.info(m_conn.group(2))

        # Get device's "hostname" from netmiko, and "ip" from .json
        hostname = connection.base_prompt
        ip = (device['ip'])

        # Log "start" locally on the device.
        sysargv = ' '.join(sys.argv)
        connection.send_command('send log 6 "Begin script: {}"'.format(sysargv))
        
        # Send each command from "x.txt" to device (3rd argument).
        for command in commands:
            # If only whitespace in line do nothing and continue.
            if command in ['\n', '\r\n']:
                pass
            else:
                print('[{0}] [{1}] >> {2}'.format(hostname, ip, command) + '\n')
                print(connection.send_command(command))
                print('\n' + '-'*79)

        # Log "end" locally on the device.
        connection.send_command('send log 6 "End script: {}"'.format(sysargv))

        # Disconnect SSH session.
        connection.disconnect()

        # Log the successful configuration on the working directory in cmdrunner.log
        success_configured = ('Configuration to device successful:', device['ip'])
        success_configured_str = ' '.join(success_configured)
        logger.info(success_configured_str)


    except netmiko_ex_auth as ex_auth:
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(Fore.RED + current_time, '- Authentication error:', device['ip'] + Style.RESET_ALL)
        # Log the authentication error on the working directory in cmdrunner.log
        logger.warning(ex_auth)

    except netmiko_ex_time as ex_time:
        current_timestamp = datetime.datetime.now()
        current_time = current_timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print(Fore.RED + current_time, '- TCP/22 connectivity error:', device['ip'] + Style.RESET_ALL)
        # Log the TCP/22 connectivity error on the working directory in cmdrunner.log
        logger.warning(ex_time)


# Script end timestamp and formatting
end_timestamp = datetime.datetime.now()
end_time = end_timestamp.strftime('%d/%m/%Y %H:%M:%S')

# Script duration and formatting
total_time = end_timestamp - start_timestamp
total_time = str(total_time).split(".")[0]


# SCRIPT STATISTICS
print(Fore.WHITE + '='*79 + Style.RESET_ALL)
print("+" + "-"*77 + "+")
print("|" + " "*30 + "SCRIPT STATISTICS" +      " "*30 + "|")
print("|" + "-"*77 + "|")
print("| Script started:         ", start_time, " "*31 + "|")
print("| Script ended:           ", end_time,   " "*31 + "|")
print("| Script duration (h:m:s):", total_time, " "*43 + "|")
print("+" + "-"*77 + "+")
