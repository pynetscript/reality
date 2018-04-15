[![Build Status](https://travis-ci.org/pynetscript/reality.svg?branch=master)](https://travis-ci.org/pynetscript/reality)
[![GitHub release](https://img.shields.io/badge/version-1.2-blue.svg)](https://github.com/pynetscript/reality)
[![license](https://img.shields.io/github/license/pynetscript/reality.svg)](https://github.com/pynetscript/reality/blob/master/LICENSE)

# reality

```
Written by:           Aleks Lambreca
Creation date:        24/03/2018
Last modified date:   15/04/2018
Version:              v1.2

Script use:           SSH into Cisco IOS devices and run config/show commands
                      Note: Commands are run one by one (not all at once)
                            Supports both IPv4 and IPv6 addresses and FQDNs
                            Both Py2 and Py3 compatible
                      The script needs 3 arguments to work:
                      - 1st argument: cmdrunner.py
                      - 2nd argument: /x.json
                      - 3rd argument: /x.txt
                      Note: A full command looks like:
                      ./cmdrunner.py router/7200.json router/cmd.txt

Script input:         SSH Username/Password
                      Specify devices as a .json file
                      Note: See "router/7200.json" as an example
                      Specify show/config commands as a .txt file
                      Note: Show commands need "do" in the front
                            See "router/cmd.txt" as an example

Script output:        Cisco IOS command output
                      Errors in screen
                      Progress bar
                      Statistics
                      Log erros in cmdrunner.log
                      Travis CI build notification to Slack private channel
```


# Prerequisites

- SSH (TCP/22) reachability to devices.    
- Local username with privilege 15 (example: `user a.lambreca priv 15 secret cisco`).
- Alias command to save configuration: `alias exec wr copy run start`


# Installation

```
mkdir /reality/ && cd /reality/
sudo apt-get install -y git
git clone -b https://github.com/pynetscript/reality.git . 
pip install -r requirements.txt
```

# .travis.yml

- [Travis CI](https://travis-ci.org/pynetscript/reality)
- What language: **Python**
- What versions: **2.7** , **3.4** , **3.5** , **3.6**
- What to install: **pip install -r requirements.txt**
- What to run: **python cmdrunner.py**
- Where to send notifications: **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** 
  - Install Travis CI on [Slack](https://pynetscript.slack.com) and at some point it will output a slack channel to use.
  - Replace **pynetscript:3GF5L6jlBvYl9TA5mrcJ87rq** with your own channel.
  - Supports private channels.


# tools.py

- tools.py is going to be imported on our main script (cmdrunner.py).
- This way we have a cleaner main script.
- Function (get_input)
    - Get input that is both Py2 and Py3 compatible
- Function (get_credentials) 
    - Prompts for username
    - Prompts for password twice but doesn't show it on screen (getpass)
        - If passwords match each other the script will continue to run
        - If password don't match each other you will get an error message `>> Passwords do not match. Try again. ` but the script will continue to run. Use Ctrl + C to cancel the script and run it again.
        

# 2nd argument (.json)

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

- Finally i copy/pasted the output into router/7200.json which is going to be used by cmdrunner.py as the <2nd_argument>.   


# 3rd argument (.txt)

Create a txt file with the config/show commands that you want to run on the devices:    
Note: Show commands need "do" in the front.

```
do sh ip int b | i up
do sh clock
```

# 1st argument (cmdrunner.py)

This is the main script that we will run.   
Legal examples:   
- `python2 <1st_argument> <2nd_argument> <3rd_argument>`
- `python3 <1st_argument> <2nd_argument> <3rd_argument>`

Let's use the following example to explain the script:    
- `python3 cmdrunner.py router/7200.json router/cmd.txt`

First the script will:     
- Create a log file named "cmdrunner.log".
- Prompt us for a username and a password (password required twice).
- Show progress bar

```
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
                                                                               
N/A% [                                            ] [0 of 3] [ETA:  --:--:--]
===============================================================================
```
  
Then the script will:    
- Timestamp the date & time the script started in D/M/Y H:M:S format. 
- SSH to the first device in the <2nd_argument> (.json). 
- Run all the commands from the <3rd argument> (.txt) one by one.  
  - Don't run empty line as command.  
- Save the running-config to startup-config.  
- Disconnect the SSH session.  
- Show progress bar

Errors:
- If there is an authentication error we will get an error message `15/04/2018 14:37:16 - Authentication error - r1.a-corp.com`
- If there is an connectivity (TCP/22) error we will get an error message `15/04/2018 14:37:34 - TCP/22 connectivity error - 192.168.1.120`
- Errors are logged in cmdrunner.log

Finally the script will:
- Repeat the process for all devices in <2nd_argument> (.json) 
- Timestamp the date & time the script ended in D/M/Y H:M:S format.
- Subtract start timestamp and end timstamp to get the time (in H:M:S format) of how long the script took to run.
- Print SCRIPT STATISTICS

```
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           15/04/2018 14:34:40                               |
| Script ended:             15/04/2018 14:36:31                               |
| Script duration (h:m:s):  0:01:51                                           |
+-----------------------------------------------------------------------------+
```

# Successful demo

```
aleks@acorp:~/reality$ python3 cmdrunner.py router/7200.json router/cmd.txt
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
                                                                               
N/A% [                                            ] [0 of 3] [ETA:  --:--:--]
===============================================================================
15/04/2018 14:34:40 - Connecting to device: r1.a-corp.com
15/04/2018 14:34:46 - Successfully connected - r1.a-corp.com
-------------------------------------------------------------------------------
[R1] [r1.a-corp.com] >> do sh ip int b | i up


config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#do sh ip int b | i up
FastEthernet0/0        192.168.1.110   YES NVRAM  up                    up      
R1(config)#end
R1#
-------------------------------------------------------------------------------
[R1] [r1.a-corp.com] >> do sh clock

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#do sh clock
*14:35:01.311 UTC Sun Apr 15 2018
R1(config)#end
R1#
-------------------------------------------------------------------------------
[R1] [r1.a-corp.com] >> write memory

Building configuration...
[OK]
                                                                               
 33% [##############                              ] [1 of 3] [ETA:   0:01:11]
===============================================================================
15/04/2018 14:35:16 - Connecting to device: 192.168.1.120
15/04/2018 14:35:23 - Successfully connected - 192.168.1.120
-------------------------------------------------------------------------------
[R2] [192.168.1.120] >> do sh ip int b | i up


config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#do sh ip int b | i up
FastEthernet0/0        192.168.1.120   YES NVRAM  up                    up      
Loopback0              10.2.0.1        YES NVRAM  up                    up      
R2(config)#end
R2#
-------------------------------------------------------------------------------
[R2] [192.168.1.120] >> do sh clock

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#do sh clock
*14:35:39.275 UTC Sun Apr 15 2018
R2(config)#end
R2#
-------------------------------------------------------------------------------
[R2] [192.168.1.120] >> write memory


Building configuration...
[OK]
                                                                               
 66% [#############################               ] [2 of 3] [ETA:   0:00:37]
===============================================================================
15/04/2018 14:35:55 - Connecting to device: 2001:db8:acab:a001::130
15/04/2018 14:36:01 - Successfully connected - 2001:db8:acab:a001::130
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> do sh ip int b | i up


config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#do sh ip int b | i up
FastEthernet0/0        192.168.1.130   YES NVRAM  up                    up      
R3(config)#end
R3#
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> do sh clock

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#do sh clock
*14:36:16.767 UTC Sun Apr 15 2018
R3(config)#end
R3#
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> write memory

Building configuration...
[OK]
                                                                               
100% [############################################] [3 of 3] [Time:  0:01:50]

===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           15/04/2018 14:34:40                               |
| Script ended:             15/04/2018 14:36:31                               |
| Script duration (h:m:s):  0:01:51                                           |
+-----------------------------------------------------------------------------+
```

# Unsuccessful demo

- R1 (r1.a-corp.com): I have misconfigured authentication.
- R2 (192.168.1.120): I have no SSH (TCP/22) reachability.
- R3 (2001:db8:acab:a001::130): This router is configured correctly.

```
aleks@acorp:~/reality$ python3 cmdrunner.py router/7200.json router/cmd.txt
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
                                                                               
N/A% [                                            ] [0 of 3] [ETA:  --:--:--]
===============================================================================
15/04/2018 14:37:13 - Connecting to device: r1.a-corp.com
15/04/2018 14:37:16 - Authentication error - r1.a-corp.com
                                                                               
 33% [##############                              ] [1 of 3] [ETA:   0:00:06]
===============================================================================
15/04/2018 14:37:16 - Connecting to device: 192.168.1.120
15/04/2018 14:37:34 - TCP/22 connectivity error - 192.168.1.120
                                                                               
 66% [#############################               ] [2 of 3] [ETA:   0:00:10]
===============================================================================
15/04/2018 14:37:34 - Connecting to device: 2001:db8:acab:a001::130
15/04/2018 14:37:39 - Successfully connected - 2001:db8:acab:a001::130
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> do sh ip int b | i up


config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#do sh ip int b | i up
FastEthernet0/0        192.168.1.130   YES NVRAM  up                    up      
R3(config)#end
R3#
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> do sh clock

config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#do sh clock
*14:37:55.159 UTC Sun Apr 15 2018
R3(config)#end
R3#
-------------------------------------------------------------------------------
[R3] [2001:db8:acab:a001::130] >> write memory

Building configuration...
[OK]
                                                                               
100% [############################################] [3 of 3] [Time:  0:00:56]

===============================================================================
+-----------------------------------------------------------------------------+
|                              SCRIPT STATISTICS                              |
|-----------------------------------------------------------------------------|
| Script started:           15/04/2018 14:37:12                               |
| Script ended:             15/04/2018 14:38:09                               |
| Script duration (h:m:s):  0:00:57                                           |
+-----------------------------------------------------------------------------+
```

# cmdrunner.log

```
15/04/2018 14:37:16 - WARNING - Authentication failure: unable to connect cisco_ios r1.a-corp.com:22
Authentication failed.
15/04/2018 14:37:34 - WARNING - Connection to device timed-out: cisco_ios 192.168.1.120:22
```
