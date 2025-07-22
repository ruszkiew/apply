
Usage:
  ./apply.py <device_name>|<device_ip>|<file_of_devices> <command>|<file_of_commands>

Description:
   The apply utility lets you easily SSH to any number of devices and execute a
   single or list of commands.

Usage Notes:
   This script creates an SSH channel and prompts the user for username and password.
   Environmental variables ROUTER_USERNAME and ROUTER_PASSWORD could also be used
     but not recommended.

Examples:
    apply.py my_router 'show ip int brief'
    apply.py 10.1.1.1 'show version'
    apply.py router.lst 'show run | inc ntp'
    apply.py router.lst command.lst

     * router.lst and command.lst are files in the example
     ** 'wait=<seconds>' command can pause in command list

