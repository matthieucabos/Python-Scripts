import os
import sys
import re
import netmiko

__author__="CABOS Matthieu"
__date__=18/10/2021

IPSwitchs={
    'Balard-1C-1': '10.14.0.47',
    'Balard-1D-1': '10.14.0.49',
    'Balard-1G-1': '10.14.0.51',
    'Balard-1H-1': '10.14.0.54',
    'Balard-2C-1': '10.14.0.56',
    'Balard-2D-1': '10.14.0.58',
    'Balard-2G-1': '10.14.0.60',
    'Balard-2H-1': '10.14.0.62',
    'Balard-2H-2': '10.14.0.63',
    'Balard-3C-1': '10.14.0.65',
    'Balard-3D-1': '10.14.0.67',
    'Balard-3G-1': '10.14.0.69',
    'Balard-3G-2': '10.14.0.70',
    'Balard-3H-1': '10.14.0.72',
    'Balard-4C-1': '10.14.0.74',
    'Balard-4D-1': '10.14.0.76',
    'Balard-4G-1': '10.14.0.78',
    'Balard-4H-1': '10.14.0.80',
    'Balard-EP-1': '10.14.0.40',
    'Balard-PAC-1': '10.14.0.42',
    'Balard-PAC-2': '10.14.0.43'
    }

#Buildig Error dictionnary
Error_dict={}
for Cisco in IPSwitchs.keys():
	home= os.getenv('HOME')
	user=os.getenv('USER')
	keyfile=home+'/.ssh/cisco'
	ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[Cisco],
                                         username=user, use_keys=True, key_file=keyfile)
	if (ssh_session.send_command("show interface | i err-disable") != '' ):
		Error_dict[Cisco]=ssh_session.send_command("show interface | i err-disable")

	
# Getting exact Gigait Ethernet Socket from Error dictionnary and store them into Gb_dict Dictionnary
regex=r'([0-9]/){2}[0-9]+'
Gb_dict={}
for k,v in Error_dict.items():
	Gb=[]
	matches = re.finditer(regex, v, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		Gb.append(match.group())
	Gb_dict[k]=Gb

f=open('Error_liste.txt','a')
for k,v in Gb_dict.items():
	f.write(str(k)+" "+''.join(v))
f.close()

# Brownsing Cisco list and write & apply associated shell script
for Cisco in Gb_dict.keys():
	if not Gb_dict[Cisco]==[]:
		home= os.getenv('HOME')
		user=os.getenv('USER')
		keyfile=home+'/.ssh/cisco'
		ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[Cisco],
	                                         username=user, use_keys=True, key_file=keyfile)
		for item in Gb_dict[Cisco]:
			if item != None:
				command=['interface GigabitEthernet'+str(item),'shutdown','no shutdown']
				ssh_session.send_config_set(command)
		ssh_session.send_command("exit\n")
		ssh_session.disconnect()

#Reomving temporary files
quit()
