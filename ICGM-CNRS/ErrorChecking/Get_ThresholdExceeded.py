import os
import sys
import re
import netmiko

__author__="CABOS Matthieu"
__date__=22/10/2021

home= os.getenv('HOME')
user=os.getenv('USER')
keyfile=home+'/.ssh/id_rsa'
ssh_session = netmiko.ConnectHandler(device_type='linux', ip='10.14.23.23', use_keys=True,key_file=keyfile)
# ssh_session.send_command('psql -h localhost -U postgres opennms')
# Content=ssh_session.send_command("select * from alarms where lasteventtime > (now() AT TIME ZONE 'Europe/Paris')::date - interval '6 hours';")
# print(Content)