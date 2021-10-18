import os
import sys
import re

__author__="CABOS Matthieu"
__date__=18/10/2021

Cisco_list=[
'Balard-EP-1',
'Balard-PAC-1',
'Balard-PAC-2',
'Balard-RDC-1',
'Balard-1C-1',
'Balard-1D-1',
'Balard-1G-1',
'Balard-1G-2',
'Balard-1H-1',
'Balard-2C-1',
'Balard-2D-1',
'Balard-2G-1',
'Balard-2H-1',
'Balard-2H-2',
'Balard-3C-1',
'Balard-3D-1',
'Balard-3G-1',
'Balard-3G-2',
'Balard-3H-1',
'Balard-4C-1',
'Balard-4D-1',
'Balard-4G-1',
'Balard-4H-1',
'Balard-SRV',
'Balard-SRV-SUP',
'Balard-SRV-CINES',
'Balard-SUP-CINES']

#Buildig Error dictionnary
Error_dict={}
for Cisco in Cisco_list:
	print(Cisco)
	Error_dict[Cisco]=os.popen('ssh -t '+str(Cisco)+' "show interface | i err-disable"').read()

# Getting exact Gigait Ethernet Socket from Error dictionnary and store them into Gb_dict Dictionnary
regex=r'([0-9]/){2}[0-9]+'
Gb_dict={}
for k,v in Error_dict.items():
	Gb=[]
	matches = re.finditer(regex, v, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		Gb.append(match.group())
	Gb_dict[k]=Gb

# Brownsing Cisco list and write & apply associated shell script
for Cisco in Cisco_list:
	if not Gb_dict[Cisco]==[]:
		f=open('Instructions_ssh'+Cisco+'.sh','a')
		os.system('chmod 777 Instructions_ssh'+Cisco+'.sh')
		f.write('#!/bin/bash\n# Author : CABOS Matthieu\n# Date : 18/10/2021\n')
		f.write("conf term\n")
		for item in Gb_dict[Cisco]:
			if item != None:
				f.write("interface GigabitEthernet"+str(item)+"\n")
				f.write("shutdown\n")
				f.write("no shutdown\n")
				f.write("exit\n")
				f.write("conf term\n")
		f.write("exit\n")
		os.system('ssh '+Cisco+' < Instructions_ssh'+Cisco+'.sh')
#Reomving temporary files
try:
	os.system('rm Instructions*')
except:
	pass
quit()