###############################################################################
# Written by:           Aleks Lambreca
# Creation date:        24/03/2018
# Last modified date:   19/08/2018
###############################################################################


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Standard library modules
import requests
import json
import sys
import signal
import os
import readline
import atexit
from colorama import init
from colorama import Fore
from colorama import Style
from getpass import getpass
from collections import Counter
from pprint import pprint as pp
from requests.packages.urllib3.exceptions import InsecureRequestWarning


signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOERror: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)   # KeyboardInterrupt: Ctrl-C


def get_input(prompt=''):
    """
    Get input that is Py2/Py3 compatible and keep the input in a history file.
    """
    histfile = os.path.join(os.path.expanduser("~"), ".runnerhistory")

    try:
        #line = raw_input(prompt)
        readline.set_history_length(1000)
        readline.read_history_file(histfile)
        line = raw_input(prompt)
        readline.write_history_file(histfile)
    except NameError:
        #line = input(prompt)
        readline.set_history_length(1000)
        readline.read_history_file(histfile)
        line = input(prompt)
        readline.write_history_file(histfile)
        #line = input(prompt)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)
    return line


def get_credentials():
    """
    Prompts for, and returns a username and password.
    """
    username = get_input('Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype password: ')
        if password != password_verify:
            print(Fore.RED+'>> Passwords do not match. Please try again.' + Style.RESET_ALL)
            password = None
            continue
        return username, password


def count_letters(x):
    """
    Count how many chars are in a string
    """
    counter = Counter()
    for word in x.split():
        counter.update(word)
    return sum(counter.values())


def yes_or_no(input=''):
    """
    Usage: yer_or_no('Ask your y/n question here')
    """
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}

    choice = None
    while not choice:
        choice = get_input(input).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print(Fore.RED + ">> Please respond with 'yes' or 'no'" + Style.RESET_ALL)
            choice = None
            continue
        return choice


def get_netbox_devices():
    """
    """
    print(Fore.WHITE + '='*79 + Style.RESET_ALL)
    NETBOX = ('https://' + get_input('Netbox server IP/FQDN?: '))
    TOKEN = (get_input('API token?: '))
    GET = ( get_input('What to GET?: '))

    headers = {  
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Token ' + TOKEN
    }

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get(NETBOX + GET, headers=headers, verify=False).json()

    devices_raw = []
    counter = r['count']

    for i in range(counter):
        ip          = r['results'][i]['name']
        device_type = r['results'][i]['platform']['slug']
        devices_raw.append({'device_type': device_type, 'ip': ip})
        
    devices = json.dumps(devices_raw)

    datapath = '/home/aleks/netbox/netbox.json'

    with open(datapath, 'w') as file:
        file.write(devices)
        file.close()
    return file
