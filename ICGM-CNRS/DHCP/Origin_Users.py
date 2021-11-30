import os
import sys
import re
import netmiko
import pyexcel as p

__author__="CABOS Matthieu"
__date__=29/11/2021

def get_Port(output):

	# Getting port number since the regular expressions using the output stdout from the ssh

	port=0
	regex=r'[0-9]*'
	maxi=0
	matches = re.finditer(regex, output, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		try:
			port=int(match.group())
		except:
			pass
		if port > maxi:
			maxi=port 
	return maxi

def get_IP_list(IP):

	# Getting IP list since the regular expressions using the output stdout from the ssh

	banned=['127.0.0.1','10.14.14.20']
	res=[]
	tmp=[]
	regex=r"([0-9]*\.){3}[0-9]+"
	matches = re.finditer(regex, IP, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		tmp.append(match.group())
	for item in tmp:
		if not item in banned:
			res.append(item)
	return list(dict.fromkeys(res))

def get_Host_list(Host):

	# Getting Host list since the regular expressions using the output stdout from the ssh

	res=[]
	regex=r'^[a-zA-Z0-9_-]*'
	matches = re.finditer(regex, Host, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		res.append(match.group())
	return list(dict.fromkeys(res))

def Read_ods(path,Host_list,IP_list):

	# Reading the Ordintaeurs.ods file to get associated MAC_@ & Departement ID

	records = p.get_array(file_name=path)
	ind=0
	res=[]
	mac=''
	for record in records:
		if record[0] in Host_list:
			ind=Host_list.index(record[0])
			mac=record[1][:2]+record[1][3:5]+'.'+record[1][6:8]+record[1][9:11]+'.'+record[1][12:14]+record[1][15:17]
			res.append([record[0],mac,record[2],IP_list[ind]])
			mac=''
			ind=0
	return res

def Treat_Info(Infos):

	# Treat Infos getted since the ods file and the ssh output both. Etablishing a link between the MAC_@ and the Cisco Socket Number
	
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

	res=[]
	for cisco in IPSwitchs.keys():
		out=[]
		home= os.getenv('HOME')
		user=os.getenv('USER')
		keyfile=home+'/.ssh/cisco'
		ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=IPSwitchs[cisco],username=user, use_keys=True, key_file=keyfile)
		output=ssh_session.send_command('sh mac address-table')
		ssh_session.disconnect()
		out=output.split('\n')
		regex=r'Gi([0-9]\/){2}[0-9]+'
		for info in Infos:
			for line in out:
				if info[1] in line:
					matches=re.finditer(regex, line , re.MULTILINE)
					for matchNum, match in enumerate(matches, start=1):
						if match.group() != None :
							res.append('Cisco : '+str(cisco)+' | Vlan / Mac_@ / Cisco Socket : '+str(line)+' | Hostname : '+str(info[0])+' | Department :  '+str(info[2])+' | Ip_@ : '+str(info[3]))		
					if(len(res)==len(Infos)):
						return res			
	return(res)

def Write_in_file(to_write,path):

	# Write Infos in file

	f=open(path,'a')
	for item in to_write:
		f.write(item)
		f.write('\n')
	f.close()

# Initialisation

User_list=""
IP=""
Nb_Port=""
Host=""
IP_list=[]
Host_list=[]
Infos=[]
to_write=[]

# Getting Users acount informations since the top level

home= os.getenv('HOME')
user=os.getenv('USER')
keyfile=home+'/.ssh/known_hosts'

# Connecting an ssh session to the origin.srv-prive.icgm.fr server

ssh_session = netmiko.ConnectHandler(device_type='linux', ip='10.14.14.20', username=user, use_keys=True, key_file=keyfile)

# Getting raw users list Informations

User_list=ssh_session.send_command('/opt/Linux_FLEXnet_Server_ver_11.16.5.1/lmutil  lmstat -a -c /opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses/Origin_20jetons.lic | grep "^.*origin\.srv-prive\.icgm\.fr/27000.*"')

# Getting the Port Informations

Nb_Port = ssh_session.send_command('netstat -anp | grep ":::*" | grep LISTEN')
Real_port=get_Port(Nb_Port)

if (Real_port > 27000):

	# Getting the raw IP list informations

	IP=ssh_session.send_command('ss -n -t | grep '+str(Real_port)) # | grep -Po "\K([0-9]*\.){3}[0-9]+" 
	IP_list=get_IP_list(IP)

	# Getting the raw hostname list Informations

	Host=ssh_session.send_command('ss -n -t -r | grep '+str(Real_port)+' | cut -d " " -f16 ')
	Host_list=get_Host_list(Host)

	# Exit the ssh session and read the Ordinateurs.ods file

	ssh_session.disconnect()
	Infos=Read_ods('../Ordinateurs.ods',Host_list,IP_list)

	# Updating the Origin_history file since the newest Informations

	to_write=Treat_Info(Infos)
	try:
		os.system('scp '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/Origin_history .')
	except:
		pass
	Write_in_file(to_write,'./Origin_history')
	os.system('scp ./Origin_history '+str(user)+'@origin.srv-prive.icgm.fr:/home/mcabos/')
	quit()

else:
	print("No users connected")
	quit()