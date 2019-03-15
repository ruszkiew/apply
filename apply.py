#!/usr/bin/env python

############################################################
#                                                          #
# apply.py    - v2.7    - 12/18/18                         #
#                                                          #
# v2.7 - updated socket connection exception               #
# v2.6 - fixed input for python v2.7 + v3.0                #
# v2.5 - added to github                                   #
# v2.4 - added more debug - added /n to command array      #
# v2.3 - added script entry point                          #
# v2.2 - moved all prints to () for v3 support             #
# v2.1 - command output was fixed - put direct into list   #
# v2.0 - added absolute timeout for channel receiving      #
# v1.9 - added debug boolean for function printouts        #
# v1.8 - updated SSH without threads  - Tim Way help       #
# v1.7 - using ios_cli_parse to glean variablas to device  #
# v1.6 - added 'usage' output and checked for argv exist   #
# v1.5 - created more functions to prep for unit testing   #
# v1.4 - moved ssh class to module ssh.py                  #
# v1.3 - added mutli commands per session                  #
# v1.2 - added name resolution                             #
# v1.1 - added username and password prompt                #
# v1.0 - initial code based on Cisco PRNE class lab        #
#      - named it 'apply' from Craig Weinhold perl script  #
#                                                          # 
#                                                          # 
# *************** TODO *******************                 #  
# - allow to pass in variables to glean                    # 
# - add error correction - component testing               # 
# - add error correction - debug switch                    # 
#                                                          # 
#                                                          # 
############################################################

# libraries

# standard modules
import os
import socket
import getpass
import re
import sys
from time import sleep

# external modules
import paramiko
from paramiko import SSHClient,AutoAddPolicy

# my modules

###########################################################

# functions

def cliUsage():
   print(
         "\n"
         "Usage:\n"
         "  ./apply.py <device_name>|<device_ip>|<file_of_devices> <command>|<file_of_commands>\n"
         "\n"
         "Description:\n"
         "   The apply utility lets youu easily touch any number of devices and execute a\n"
         "   single or list of commands.\n"  
         "\n"
         "Usage Notes:\n"
         "   This script creates an SSH channel and prompts the user for username and password.\n"
         "   It is not advised by the username and password can be hardcoded in the script.\n"
         "\n"
         "Examples:\n"
         "    apply.py my_router 'show ip int brief'\n"
         "    apply.py 10.1.1.1 'show version'\n"
         "    apply.py router.lst 'show run | inc ntp'\n"
         "    apply.py router.lst command.lst\n"
         "\n"
         "     * router.lst and command.lst are files in the example\n"
         "     ** 'wait=<seconds>' command can pause in command list\n"
        )


def enterPassword():
  while True:
    _password = getpass.getpass('Enter Password:')
    _password_again = getpass.getpass('Confirm Password:')
    if _password != _password_again:
      print('Passwords do not match.  Please try again!')
    else:
      return _password


def getDevices():
   # ensure 2 cli parameters passed in 
   if len(sys.argv) != 3:
      cliUsage()
      exit()
   # determine if parameter is single device|command or a file
   if os.path.exists(sys.argv[1]):
      _device_list = [line.strip() for line in open(sys.argv[1], 'r')]
   else:
      _device_list = [sys.argv[1]]
   return _device_list


def getCommands():
   # ensure 2 cli parameters passed in 
   if len(sys.argv) != 3:
      cliUsage()
      exit()
   # determine if parameter is single device|command or a file
   if os.path.exists(sys.argv[2]):
      _command_list = [line.strip() for line in open(sys.argv[2], 'r')]
   else:
      _command_list = [sys.argv[2]]
   _command_list.append("\n")
   return _command_list


def resolveDevice(_device):
   if DEBUG: print("RESOLVEDEVICE")
   ip_regex = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
   ip_boolean = ip_regex.match(_device)
   if ip_boolean:
       ip_address = _device
   else:
       try:
           ip_address = socket.gethostbyname(_device)
       except socket.gaierror:
           ip_address = '0.0.0.0'
           print("## ",_device, "cannot be DNS resolved ##")
   if DEBUG: print("RESOLVEDEVICE-RETURN")
   return ip_address


def readChannelRecv(_channel):
   if DEBUG: print("READCHANNELRECV")
   buf = ''
   i = 0;
   while not _channel.recv_ready() and i < 20:
       sleep(.5)
       i = i + 1
   while _channel.recv_ready():
       buf += _channel.recv(1024).decode('utf-8')
       sleep(.5)
   if DEBUG: print("READCHANNELRECV-RETURN")
   return buf

def sshDevice(_ip_address,_username,_password, _command_list):

   if DEBUG: print("***************")
   if DEBUG: print(_ip_address)
   if DEBUG: print("***************")
   if DEBUG: print("SSHDEVICE")

   ssh = SSHClient()
   ssh.set_missing_host_key_policy(AutoAddPolicy())

   outputs = []

   try:
       ssh.connect(_ip_address, username=_username,port=22,password=_password, look_for_keys=False, timeout=4)
       channel = ssh.get_transport().open_channel( kind = 'session' )
       channel.invoke_shell()
       channel.send('term len 0\n')
       if DEBUG: print("SSHDEVICE-SEND-term len 0")
       readChannelRecv(channel)

       for command in _command_list:
           command.rstrip()
           wait_regex = re.search("^wait=(\d+)$",command)
           if wait_regex:
               if DEBUG: print("SSHDEVICE-WAIT-COMMAND")
               sleep(float(wait_regex.group(1)))
           else:
               if DEBUG: print("SSHDEVICE-SEND-COMMMAND-" + command)
               channel.send(command + '\n')
               output_arr = readChannelRecv(channel).splitlines()
               for output_str in output_arr:
                   if DEBUG: print('SSHDEVICE-OUTPUT <-- ' + output_str)
                   outputs.append(output_str)

       channel.send('term len 24\n')
       if DEBUG: print("SSHDEVICE-SEND-term len 24")
       readChannelRecv(channel)

       ssh.close()

   except  paramiko.AuthenticationException:
       print(' ## Authentication Failed ##')
   except  paramiko.SSHException:
       print(' ## Issues with SSH Service ##')
   except  Exception:
       print ('  ## Generic Connection Error ##')

   if DEBUG: print("SSHDEVICE-RETURN")

   return outputs

###########################################################

if __name__ == "__main__":

    DEBUG = False

    # fix python 3.x raw_input
    try: input = raw_input
    except NameError: pass

    # username = 'uid'
    username = input('Enter username for device login:')

    # password = 'pwd'
    password = enterPassword()

    device_list = getDevices();
    command_list = getCommands();

    # read device data
    for device in device_list:
        if DEBUG: print("MAIN-FOR")
        ip_address = resolveDevice(device)

        data = sshDevice(ip_address,username,password,command_list)
        for line in data:
            print(line)

###########################################################

   

