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
                      ./cmdrunner.py switch/2960/24_port.json switch/2960/24_cmd.txt

Script input:         SSH Username/Password
                      Specify devices as a .json file
                      Note: See "switch/2960/24_port.json" as an example
                      Specify show/config commands as a .txt file
                      Note: Show commands need "do" in the front
                            See "switch/2960/24_cmd.txt" as an example

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
        - If password don't match each other you will get an error message `>> Passwords do not match. Try again. ` and you will prompted for password again
            - The script though will continue to run, but you should use Ctrl + C to cancel the script and try again.
