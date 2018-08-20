[![Build Status](https://travis-ci.org/pynetscript/reality.svg?branch=master)](https://travis-ci.org/pynetscript/reality)
[![GitHub release](https://img.shields.io/badge/version-1.3-blue.svg)](https://github.com/pynetscript/reality)


# reality

### Script use
- SSH into Cisco IOS devices and run show commands
  - Commands are run one by one (not all at once)
  - Supports both IPv4 and IPv6 addresses and FQDNs
  - Both Py2 and Py3 compatible
- The script needs 3 arguments to work:
  - 1st argument: `cmdrunner.py`
  - 2nd argument: `x.json`
  - 3rd argument: `x.txt`
  - A full command looks like:
    - `./runner.py router/7200.json router/cmd.txt`
    - `./runner.py netbox.json cmd.txt`


### Script input (Option 1: Get devices via local .json file)
- Specify devices as a .json file
  - See `router/7200.json` as an example
- Specify show commands as a .txt file
  - See `router/cmd.txt` as an example
- Username/Password
  
  
### Script input (Option 2: GET devices via Netbox API)
- Needs `./runner.py netbox.json cmd.txt` command to be used
- Specify Netbox server IP/FQDN
- Specify API Token
- Specify URL to GET
- Username/Password
  
  
### Script output
- Cisco IOS command output
- Errors in screen
- Progress bar
- Statistics
- Log success/erros in `cmdrunner.log`
- Travis CI build notification to Slack private channel


# Prerequisites

- SSH (TCP/22) reachability to devices.    
- Username with privilege 15 (example: `user a.lambreca priv 15 secret cisco`).
- Alias command to save configuration: `alias exec wr copy run start`


# Installation

```
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y python-pip
sudo apt-get install -y python3-pip
sudo python -m pip install -U pip
sudo python3 -m pip install -U pip
cd ~ && git clone https://github.com/pynetscript/reality.git && cd reality
sudo python -m pip install -r requirements.txt
sudo python3 -m pip install -r requirements.txt
```

# .travis.yml

- [Travis CI](https://travis-ci.org/pynetscript/reality)
- What language: **Python**
- What versions: **2.7** , **3.4** , **3.5** , **3.6**
- What to install: **pip install -r requirements.txt**
- What to run: **python runner.py**
- Where to send notifications: **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** 
  - Install Travis CI on [Slack](https://pynetscript.slack.com) and at some point it will output a slack channel to use.
  - Replace **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** with your own channel.
  - Supports private channels.


# tools.py

- "tools.py" is going to be imported on our main script (runner.py) so we have a cleaner main script.
- This way we have a cleaner main script.


# 3rd argument (.txt)

Create a txt file with the show commands that you want to run on the devices:    

```
sh ip int b | i up
sh clock
```


# 2nd argument (Option 1: Get devices via local .json file)

- Create a csv file like this example:  

```CSV
device_type,ip
cisco_ios,r1.a-corp.com
cisco_ios,192.168.1.120
cisco_ios,2001:db8:acab:a001::130
```

- Go to [Mr. Data Converter](https://shancarter.github.io/mr-data-converter/).
- Copy/paste the CSV input into the **Input CSV or tab-delimited data**.
- On the bottom, in the **Output as** choose  **JSON - Properties**.
- On the left, in the **Delimiter** and in the **Decimal Sign** choose **Comma**.
- This is what you should get from the example above.

```
[{"device_type":"cisco_ios","ip":"r1.a-corp.com"},
{"device_type":"cisco_ios","ip":"192.168.1.120"},
{"device_type":"cisco_ios","ip":"2001:db8:acab:a001::130"}]
```

- Copy/paste the output into router/7200.json which is going to be used by runner.py as the <2nd_argument>.   


# 2nd argument (Option 2: GET devices via Netbox API)

- This will only be used if the 2nd argument is exactly "netbox.json" and the file netbox.json exists.
- Need to add the API token in the environment variable with the `export NETBOX_TOKEN=0123456789a0123456789b0123456789c0123456` command.
  - Token created at https://netbox.a-corp.com/user/api-tokens/
- Additionally for the script to work correctly we need to modify in Netbox > Devices > Platforms, the slugs to be netmiko compatible.
  - Here is a [screenshot](https://imgur.com/defEoHu) 

- For example these command are legal:
  - `python2 runner.py netbox.json cmd.txt`
  - `python3 runner.py netbox.json cmd.txt`
- For example these command are not legal:
  - `python2 runner.py /netbox.json cmd.txt`
  - `python3 runner.py /netbox.json cmd.txt`
 
 - https://netbox.readthedocs.io/en/stable/api/overview/
 
**Common URLs:** 
- Get all devices from site "a-corp-hq":
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0

- Get a specific role from site "a-corp-hq":
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&role=core-switch
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&role=distribution-switch
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&role=access-switch
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&role=router
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&role=firewall

- Get a specific tag from site "a-corp-hq":
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&tag=switch
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&tag=router
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&tag=firewall

- Get a specific platform from site "a-corp-hq":
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&platform=cisco_asa
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&platform=cisco_ios
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&platform=cisco_xe
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&platform=cisco_xr
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&platform=cisco_nxos
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&platform=cisco_wlc

- Get a specific model (device type) from site "a-corp-hq":
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&model=asa5545-x
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&model=isr4331
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&model=ws-c2960x-48fps-l
  - https://netbox.a-corp.com/api/dcim/devices/?site=a-corp-hq&limit=0&model=ws-c3850-48f-s

**Note**: If you want data from all sites just remove "site=a-corp-hq" from the URL. Also the maximum number of objects that can be returned is 1000 by default. Setting this to "limit=0" or "limit=None" will remove the maximum limit so we can retrieve all matching objects with a single request - [source](https://netbox.readthedocs.io/en/stable/api/overview/#pagination).



# 1st argument (runner.py)

This is the main script that we will run.  

Legal examples:   
- `python2 <1st_argument> <2nd_argument> <3rd_argument>`
- `python3 <1st_argument> <2nd_argument> <3rd_argument>`

## (Option 1: Get devices via local .json file)

Let's use the following example to explain the script: 
- `python3 runner.py router/7200.json router/cmd.txt`

First the script will:     
- Create a log file named "runner.log".
- Prompt us for a username and a password
- Show progress bar

```
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
                                                                               
N/A% [                                            ] [0 of 3] [ETA:  --:--:--]
===============================================================================
```
  
Then the script will run main() function:
- Timestamp the date & time the script started in D/M/Y H:M:S format. 
- SSH to the first device in the <2nd_argument> (.json). 
  - Log the successful connection in runner.log
- Send "log" command to log "begin timestamp" & "script used" locally on the device.
- Run all the commands from the <3rd argument> (.txt) one by one.  
  - Don't run empty line as command.  
- Send "log" command to log "end timestamp" & "script used" locally on the device.
- Disconnect the SSH session.  
- Log the successful configuration in runner.log
- Show progress bar

Errors:
- If there is an authentication error we will get an error message `23/04/2018 19:07:55 - Authentication error: r1.a-corp.com`
- If there is a connectivity (TCP/22) error we will get an error message `23/04/2018 19:08:13 - TCP/22 connectivity error: 192.168.1.120`
- Errors are logged in runner.log

Finally the script will:
- Repeat the process for all devices in <2nd_argument> (.json) 
- Timestamp the date & time the script ended in D/M/Y H:M:S format.
- Subtract start timestamp and end timstamp to get the time (in H:M:S format) of how long the script took to run.
- Print SCRIPT STATISTICS

```
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:          23/04/2018 19:05:39                                |
| Script ended:            23/04/2018 19:06:10                                |
| Script duration (h:m:s): 0:00:31                                            |
+-----------------------------------------------------------------------------+
```

### runner.py (successful)

```
aleks@acorp:~/reality$ python3 runner.py router/7200.json router/cmd.txt 
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
                                                                               
N/A% [                                            ] [0 of 3] [ETA:  --:--:--]
===============================================================================
23/04/2018 19:05:39 - Connecting to device: r1.a-corp.com
23/04/2018 19:05:45 - Connection to device successful: r1.a-corp.com
-------------------------------------------------------------------------------
[R1] [r1.a-corp.com] >> sh ip int b | i up


FastEthernet0/0        192.168.1.110   YES NVRAM  up                    up      

-------------------------------------------------------------------------------
[R1] [r1.a-corp.com] >> sh clock


*19:05:46.719 UTC Mon Apr 23 2018

-------------------------------------------------------------------------------
                                                                               
 33% [##############                              ] [1 of 3] [ETA:   0:00:21]
===============================================================================
23/04/2018 19:05:50 - Connecting to device: 192.168.1.120
23/04/2018 19:05:55 - Connection to device successful: 192.168.1.120
-------------------------------------------------------------------------------
[R2] [192.168.1.120] >> sh ip int b | i up


FastEthernet0/0        192.168.1.120   YES NVRAM  up                    up      
Loopback0              10.2.0.1        YES NVRAM  up                    up      

-------------------------------------------------------------------------------
[R2] [192.168.1.120] >> sh clock


*19:05:57.687 UTC Mon Apr 23 2018

-------------------------------------------------------------------------------
                                                                               
 66% [#############################               ] [2 of 3] [ETA:   0:00:10]
===============================================================================
23/04/2018 19:06:00 - Connecting to device: 2001:db8:acab:a001::130
23/04/2018 19:06:05 - Connection to device successful: 2001:db8:acab:a001::130
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> sh ip int b | i up


FastEthernet0/0        192.168.1.130   YES NVRAM  up                    up      

-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> sh clock


*19:06:07.903 UTC Mon Apr 23 2018

-------------------------------------------------------------------------------
                                                                               
100% [############################################] [3 of 3] [Time:  0:00:30]

===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:          23/04/2018 19:05:39                                |
| Script ended:            23/04/2018 19:06:10                                |
| Script duration (h:m:s): 0:00:31                                            |
+-----------------------------------------------------------------------------+
```

### syslog (successful)

```
*Apr 23 2018 19:05:45: %SYS-6-USERLOG_INFO: Message from tty2(user id: a.lambreca): "Begin script: runner.py router/7200.json router/cmd.txt"
*Apr 23 2018 19:05:47: %SYS-6-USERLOG_INFO: Message from tty2(user id: a.lambreca): "End script: runner.py router/7200.json router/cmd.txt"
```

### runner.log (successful)

```
23/04/2018 19:05:45 - INFO - Connection to device successful: r1.a-corp.com
23/04/2018 19:05:50 - INFO - Configuration to device successful: r1.a-corp.com
23/04/2018 19:05:55 - INFO - Connection to device successful: 192.168.1.120
23/04/2018 19:06:00 - INFO - Configuration to device successful: 192.168.1.120
23/04/2018 19:06:05 - INFO - Connection to device successful: 2001:db8:acab:a001::130
23/04/2018 19:06:10 - INFO - Configuration to device successful: 2001:db8:acab:a001::130
```

#### runner.py (unsuccessful)

- R1 (r1.a-corp.com): I have misconfigured authentication.
- R2 (192.168.1.120): I have no SSH (TCP/22) reachability.
- R3 (2001:db8:acab:a001::130): This router is configured correctly.

```
aleks@acorp:~/reality$ python3 runner.py router/7200.json router/cmd.txt 
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
                                                                               
N/A% [                                            ] [0 of 3] [ETA:  --:--:--]
===============================================================================
23/04/2018 19:07:52 - Connecting to device: r1.a-corp.com
23/04/2018 19:07:55 - Authentication error: r1.a-corp.com
                                                                               
 33% [##############                              ] [1 of 3] [ETA:   0:00:06]
===============================================================================
23/04/2018 19:07:55 - Connecting to device: 192.168.1.120
23/04/2018 19:08:13 - TCP/22 connectivity error: 192.168.1.120
                                                                               
 66% [#############################               ] [2 of 3] [ETA:   0:00:10]
===============================================================================
23/04/2018 19:08:13 - Connecting to device: 2001:db8:acab:a001::130
23/04/2018 19:08:18 - Connection to device successful: 2001:db8:acab:a001::130
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> sh ip int b | i up


FastEthernet0/0        192.168.1.130   YES NVRAM  up                    up      

-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> sh clock


*19:08:20.263 UTC Mon Apr 23 2018

-------------------------------------------------------------------------------
                                                                               
100% [############################################] [3 of 3] [Time:  0:00:31]

===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:          23/04/2018 19:07:51                                |
| Script ended:            23/04/2018 19:08:23                                |
| Script duration (h:m:s): 0:00:31                                            |
+-----------------------------------------------------------------------------+
```

### syslog (unsuccessful)

```
*Apr 23 2018 19:08:19: %SYS-6-USERLOG_INFO: Message from tty2(user id: a.lambreca): "Begin script: runner.py router/7200.json router/cmd.txt"
*Apr 23 2018 19:08:20: %SYS-6-USERLOG_INFO: Message from tty2(user id: a.lambreca): "End script: runner.py router/7200.json router/cmd.txt"
```

### cmdrunner.log (unsuccessful)

```
23/04/2018 19:07:55 - WARNING - Authentication failure: unable to connect cisco_ios r1.a-corp.com:22
Authentication failed.
23/04/2018 19:08:13 - WARNING - Connection to device timed-out: cisco_ios 192.168.1.120:22
23/04/2018 19:08:18 - INFO - Connection to device successful: 2001:db8:acab:a001::130
23/04/2018 19:08:23 - INFO - Configuration to device successful: 2001:db8:acab:a001::130
```

## (Option 2: GET devices via Netbox API)

Let's use the following example to explain the script: 
- `python3 runner.py netbox.json cmd.txt`

First the script will:     
- Create a log file named "runner.log".
- Prompt us for Netbox server IP/FQDN
- Prompt us for URL to GET?
- Run function "get_netbox_devices()" found in tools.py
- Prompt us for a username and a password
- Show progress bar

```
aleks@acorp:~/netbox$ python3 runner.py netbox.json cmd.txt
===============================================================================
Netbox server IP/FQDN?: netbox.a-corp.com
URL to GET?: /api/dcim/devices/?site=a-corp-hq&tag=router
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
                                                                                            
N/A% [                                                         ] [0 of 2] [ETA:  --:--:--]
===============================================================================
```
  
Then the script will run main() function:
- Timestamp the date & time the script started in D/M/Y H:M:S format. 
- SSH to the first device in the <2nd_argument> (netbox.json). 
  - Log the successful connection in runner.log
- Send "log" command to log "begin timestamp" & "script used" locally on the device.
- Run all the commands from the <3rd argument> (.txt) one by one.  
  - Don't run empty line as command.  
- Send "log" command to log "end timestamp" & "script used" locally on the device.
- Disconnect the SSH session.  
- Log the successful configuration in runner.log
- Show progress bar

Errors:
- If "NETBOX_TOKEN" not found in environment variable an error will be raised "NetboxAPITokenNotFound".
- If there is an authentication error we will get an error message `19/08/2018 19:50:04 - Authentication error: ACORP-HQ-EU-GR-ATHENS-DC-R1.a-corp.com`
- If there is a connectivity (TCP/22) error we will get an error message `19/08/2018 19:50:22 - TCP/22 connectivity error: ACORP-HQ-EU-GR-ATHENS-DC-R2.a-corp.com`
- Errors are logged in runner.log

Finally the script will:
- Repeat the process for all devices in <2nd_argument> (netbox.json)
- Timestamp the date & time the script ended in D/M/Y H:M:S format.
- Subtract start timestamp and end timstamp to get the time (in H:M:S format) of how long the script took to run.
- Print SCRIPT STATISTICS

```
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:          23/04/2018 19:05:39                                |
| Script ended:            23/04/2018 19:06:10                                |
| Script duration (h:m:s): 0:00:31                                            |
+-----------------------------------------------------------------------------+
```

### runner.py (successful)

```
aleks@acorp:~/netbox$ python3 runner.py netbox.json cmd.txt
===============================================================================
Netbox server IP/FQDN?: netbox.a-corp.com
What to GET?: /api/dcim/devices/?site=a-corp-hq&tag=router
===============================================================================
Username: alambreca
Password: 
Retype password: 
                                                                                            
N/A% [                                                         ] [0 of 2] [ETA:  --:--:--]
===============================================================================
19/08/2018 18:43:28 - Connecting to device: ACORP-HQ-EU-GR-ATHENS-DC-R1.a-corp.com
19/08/2018 18:43:36 - Connection to device successful: ACORP-HQ-EU-GR-ATHENS-DC-R1.a-corp.com
-------------------------------------------------------------------------------
[ACORP-HQ-EU-GR-ATHENS-DC-R1] [ACORP-HQ-EU-GR-ATHENS-DC-R1.a-corp.com] >> sh ip int b | i up


FastEthernet0/0        192.168.1.51    YES manual up                    up      

-------------------------------------------------------------------------------
[ACORP-HQ-EU-GR-ATHENS-DC-R1] [ACORP-HQ-EU-GR-ATHENS-DC-R1.a-corp.com] >> sh clock

*18:43:37.215 UTC Sun Aug 19 2018

-------------------------------------------------------------------------------
                                                                                            
 50% [############################                             ] [1 of 2] [ETA:   0:00:12]
===============================================================================
19/08/2018 18:43:40 - Connecting to device: ACORP-HQ-EU-GR-ATHENS-DC-R2.a-corp.com
19/08/2018 18:43:45 - Connection to device successful: ACORP-HQ-EU-GR-ATHENS-DC-R2.a-corp.com
-------------------------------------------------------------------------------
[ACORP-HQ-EU-GR-ATHENS-DC-R2] [ACORP-HQ-EU-GR-ATHENS-DC-R2.a-corp.com] >> sh ip int b | i up


FastEthernet0/0        192.168.1.52    YES manual up                    up      
Loopback0              10.2.0.1        YES NVRAM  up                    up      

-------------------------------------------------------------------------------
[ACORP-HQ-EU-GR-ATHENS-DC-R2] [ACORP-HQ-EU-GR-ATHENS-DC-R2.a-corp.com] >> sh clock

*18:43:46.815 UTC Sun Aug 19 2018

-------------------------------------------------------------------------------
                                                                                            
100% [#########################################################] [2 of 2] [Time:  0:00:21]

===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:          19/08/2018 18:43:26                                |
| Script ended:            19/08/2018 18:43:50                                |
| Script duration (h:m:s): 0:00:23                                            |
+-----------------------------------------------------------------------------+
```
