# reality

```
Written by:           Aleks Lambreca
Creation date:        20/03/2018
Last modified date:   24/03/2018
Version:              v1.1

Script use:           SSH into Cisco IOS devices and run config/show commands
                      Note: Supports both IPv4 and IPv6 devices
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
                      Statistics
                      Erros in cmdrunner.log
```

# Disclaimer

This isn't the best python script out there :)  

# Prerequisites

1. Box with [netmiko 2.1.0](https://github.com/ktbyers/netmiko) installed.  
2. SSH (TCP/22) reachability to devices.    
3. Local username with privilege 15 (example: `user a.lambreca priv 15 secret cisco`).
4. Alias command to save configuration: `alias exec wr copy run start`

# tools.py

- tools.py is going to be imported on our main script (cmdrunner.py). 
- This way we have a cleaner script.  
- Colorama (optional).  
- Getpass  

```Cython
sudo pip install colorama
sudo pip3 install colorama
```

- Function (get_input)
    - Get input that is both Py2 and Py3 compatible.st
- Function (get_credentials) 
    - Prompts for username
    - Prompts for password twice
        - If passwords match each other the script will continue to run
        - If password don't match each other you will get an error message `>> Passwords do not match. Try again. ` but the script will continue to run. Use Ctrl + C to cancel the script and run it again.
        
# 2nd argument (.json)

- Create an csv file like this example:  

```CSV
device_type,ip
cisco_ios,r1.a-corp.com
cisco_ios,r2.a-corp.com
```

- Copy paste everything from the csv file to [Mr. Data Converter](https://shancarter.github.io/mr-data-converter/#).  
- From the bottom, choose **Output as JSON - Properties**.  
- From the left, choose **Delimiter Comma** and **Decimal Sign Commad**.  
- This is what you should get from the example above.  

```
[{"device_type":"cisco_ios","ip":"r1.a-corp.com"},
{"device_type":"cisco_ios","ip":"r2.a-corp.com"}]
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

```
===============================================================================
Username: a.lambreca
Password: 
Retype password: 
===============================================================================
```
  
Then the script will:    
- Timestamp the date & time the script started in D/M/Y H:M:S format.
- SSH to the first device in the <2nd_argument> (.json)    
- Run all the commands in the <3rd argument> (.txt) 
- Save the running-config to startup-config.  
- Disconnect the SSH session.  

Errors:
- If the is an authentication error we will get an error message `R1.a-corp.com >> Authentication error`
- If the is an connectivity (TCP/22) error we will get an error message `R2.a-corp.com >> TCP/22 connectivity error`
- Errors are logged in the cmdrunner.log

Finally the script will:
- Repeat the process for all devices in <2nd_argument> (.json) 
- Timestamp the date & time the script ended in D/M/Y H:M:S format.
- Divide start timestamp with end timstamp to get the time (in H:M:S format) of how long the script took to run.
- Print SCRIPT STATISTICS


# Successful demo

```Cython

```

# Unsuccessful demo

- R1: I have misconfigured authentication.
- R2: I have no SSH (TCP/22) reachability.
- R3: This router is configured correctly.

```Cython

```

# cmdrunner.log

```

```
