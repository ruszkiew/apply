# 'apply.py' Cisco IOS CLI Automation

## Support Modules
Paramiko - http://www.paramiko.org/installing.html
'pip install paramiko'

## Usage

python apply.py -h

Usage:
  ./apply.py <device_name>|<device_ip>|<file_of_devices> <command>|<file_of_commands>

Description:
   The apply utility lets you easily touch any number of devices and execute a
   single or list of commands.

Usage Notes:
   This script creates an SSH channel and prompts the user for username and password.
   It is not advised by the username and password can be hardcoded in the script.

## Examples

    apply.py my_router 'show ip int brief'
    apply.py 10.1.1.1 'show version'
    apply.py router.lst 'show run | inc ntp'
    apply.py router.lst command.lst

     * router.lst and command.lst are files in the example
     ** 'wait=<seconds>' command can pause in command list

## Todo
See [TODO](TODO.md) for a list of planned features/fixes.

## Changelog
See [CHANGELOG](CHANGELOG.md) for a list of changes.
