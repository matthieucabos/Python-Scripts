import re
import pyexcel as p
import datetime
import os
import uuid

__author__='CABOS Matthieu'
__date__=10/11/2021


def TreatReg():

	# Lecture et mise à jour du fichier des Invités Enregistrés (Les entrées ayant plus d'un an sont supprimées)

	ind=0
	f=open("registred_guests",'r+')
	Content=f.readlines()
	NewContent=[]
	today=datetime.date.today()
	regex=r'[0-9]+-[0-9]+-[0-9]+'
	for line in Content:
		matches = re.finditer(regex, line, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):
			if ind :
				realDelta=0
				Date=match.group()	
				ind=0
				RegDate=(datetime.date(int(Date[0:4]),int(Date[5:7]),int(Date[8:])))
				Delta=(str(RegDate-today))
				regex2=r'-[0-9]*'
				matches2=re.finditer(regex2,Delta,re.MULTILINE)
				for matchNum, match in enumerate(matches2, start=1):
					realDelta= (int(match.group()) <= -365)
				if not realDelta :
					NewContent.append(line)
				break
			ind+=1	
	f=open('registred_guests','w')
	f.write(''.join(NewContent))
	f.close()

try:
	TreatReg()
except:
	pass

def verify_duplicate(liste):

	# On vérifie la présence d'adresses dupliquées depuis le fichier de configuration DHCP

	error=[]
	duplicate=(False,0)
	tmp=""
	Ip=""
	# Coursing the @ list
	for i in range(len(liste)):
		tmp=liste[i]
		for j in range(i+1,len(liste)):
			if tmp==liste[j]:  # Checking errors
				regex=r"(\d+.){3}\d+"
				matches = re.finditer(regex, liste[j], re.MULTILINE)
				for matchNum, match in enumerate(matches, start=1):
					Ip=match.group()
				error.append(Ip)
	if not (error==[]):
		return error
	else:
		return None

def TreatConf():

	# On traite le fichier de configuration pour récupérer le nombre d'adresses IP dupliquées

	# capture ip flag
	ip_catch=False
	# @ IP & MAC list
	ip=[]
	mac=[]
	dpt='dhcpd-519.conf'
	# courding the department list
	content=os.popen("cat "+str(dpt)).readlines() # Getting raw content of dhcp conf files
	for item in content:
		try:
			# I verify correspondance betwween MAC@ and Fixed_IP@
			if (re.search(r'fixed-address',item)[0])!=None:        
				ip.append(item)
			if (re.search(r'hardware ethernet',item)[0])!=None:
				mac.append(item)
		except:
			pass
	return (verify_duplicate(ip))

def ReadAndWrite(Times):

	# Lecture et Mise à jour du fichier de configuration DHCP pour préserver la cohérence de la structure du sous réseau

	NewContent='#vlan: 519 (ICGM-GUEST)\nsubnet 10.14.12.0  netmask 255.255.255.0 {\n'
	f=open('dhcpd-519.conf','r')
	Content=f.read()
	regex=r'host(.*\n){10}'
	matches=re.finditer(regex, Content, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
		if Times<0 :
			NewContent+=match.group()
		Times-=1
	NewContent+='}'
	f.close()
	f=open('dhcpd-519.conf','w')
	f.write(NewContent)

# Initialisation du vlan Guest

vlans={
	'ICGM-GUEST':
	{
        "id":519,
        "gateway":"10.14.21.1",
        "nat":"193.50.7.131",
        "subnet":"10.14.12.0",
        "netmask":"255.255.255.0",
        "subdomain":"guest.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    }
}

#On commence par relire les anciennes associations

macRegex=r"([0-9a-z]+:){5}[0-9a-z]+"
ipRegex=r"fixed-address (10.14.[0-9.]+)"
registred={}
lastIP={}

os.system('rm dhcpd-519.conf')

# On parcourt le fichier conf du vlan 519

info=vlans['ICGM-GUEST'];
id=info['id'];
registred={}
lastIP[id]=info['init']
if os.path.isfile("dhcpd-%d.conf"%(id)):
	with open("dhcpd-%d.conf"%(id), "r") as openfileobject:
		ip="";mac="";
		for line in openfileobject:
			matches = re.finditer(macRegex, line, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				mac=(match.group())
			matches = re.finditer(ipRegex, line, re.MULTILINE)
			for matchNum, match in enumerate(matches, start=1):
				ip=(match.group()[14:])
			if (mac != '') and (ip != ''):
				registred[mac]=ip
				numbers=ip.split('.')
				if(int(numbers[3])>=lastIP[id]):
					lastIP[id]=int(numbers[3])+1


# On lit le fichier Invites

records = p.iget_records(file_name="./Invites.ods")
f1 = open("dhcpd.conf", "w")
f1.write("""
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
ignore client-updates;
default-lease-time 86400;
max-lease-time 86400;

option domain-name              "icgm.fr";
option domain-name-servers      193.49.132.10;
#option time-offset              +7200; # Europe/Paris
#one-lease-per-client            off;
default-lease-time              86400;
max-lease-time                  90480;
option                          ip-forwarding off;
deny unknown-clients;

subnet 10.14.12.0 netmask 255.255.255.0 {
# note that no range is given so dhcpd will not try to
# assign IP addresses
}
""");
if not os.path.isfile("dhcpd-519.conf"):
	counter=0
else:
	counter = int(sum(1 for line in open('dhcpd-519.conf')) / 10)

if os.path.isfile("registred_guests"):
	f=open("registred_guests",'r')
	RegContent=f.read()
else:
	RegContent=''

# On parcours le contenu du fichier lu

BreakFlag=0
for record in records:
	if (not record['Adresse Mac']==''):
		dateA=record['Date d’arrivée']
		dateD=record['Date de départ']
		today=datetime.date.today()

		# Si la date courrante est comprise entre la date d'arrivée et la date de départ

		f=open("registred_guests",'a')
		if dateA <= today and today <= dateD :
			counter+=1
			nom=uuid.uuid4()

			# On met à jour l'historique des visites

			if (not record['Nom de l’invité'] in RegContent):
				content=(str(nom)+' Nom :  '+str(record['Nom de l’invité'])+' '+str(record['Adresse Mac'])+' Arrivée : '+str(record['Date d’arrivée'])+' Départ : '+str(record['Date de départ'])+"\n")
				f.write(content)
			if(record['Adresse Mac']=='')or(nom == ''):
				print("Ligne ignorée");
			else:

				# On rajoute l'invité au reseau invité

				dns="193.49.132.10";
				vlan='ICGM-GUEST'
				if(vlan in vlans):

					# On met à jour les champs d'informations DHCP

					info=vlans[vlan]
					id=info['id']
					mac=record['Adresse Mac'].strip();
					ip=re.sub(r'(\.1$)', "."+str(info["init"]), info["gateway"])

		            #Soit l'ordinateur est déjà connu et on conserve son IP

					if(mac in registred.keys()):
						ip=registred[mac]

					#Soit on lui en rajoute une

					else:
						print ("Ajout de %s (mac %s) non trouvé dans le vlan %d"%(nom, mac, id))
						ip=re.sub(r'(\.1$)', "."+str(lastIP[id]), info["gateway"])
						# print(ip)
						if lastIP[id] < 255 :
							lastIP[id]=lastIP[id]+1
							if BreakFlag:
								BreakFlag+=1
						else:
							lastIP[id]=2
							BreakFlag+=1

					info["content"]=info["content"]+"""
		host %s {
		    hardware ethernet %s;
		    fixed-address %s;
		    option routers %s;
		    option ntp-servers %s;
		    option domain-name-servers %s;
		    option domain-name "%s";          
		    option subnet-mask %s;
		    option host-name "%s";
		} """ % (nom, mac,ip, info['gateway'], info['gateway'], dns, info['subdomain'],info['netmask'],nom)
					info["dns"]=info["dns"]+"%s\t\tIN\tA\t%s\n"%(nom, ip)
					numbers=ip.split('.')
					info["rev"]=info["rev"]+"%d\tIN\tPTR\t%s.%s.\n"%(int(numbers[3]),nom,info["subdomain"])
				else:
					print("Vlan %s non trouvé" % (vlan))
			f.close()

# On écrit les informations dans le fichier dhcpd-519.conf (le serveur DHCP Guest)

info=vlans['ICGM-GUEST'];
if info['content']!="":
    fvlan= open("dhcpd-%d.conf"%(info["id"]), "w")
    fvlan.write("#vlan: %d (%s)\n" %(info["id"],vlan));
    fvlan.write("subnet %s  netmask %s {" % (info['subnet'],info['netmask']))
    fvlan.write(info["content"]);
    f1.write("include \"/etc/dhcp/dhcpd-%d.conf\"; #vlan %s\n" % (info["id"], vlan));
    fvlan.write("\n}\n");
    fvlan.close();
    arpa=re.sub(r'([0-9]+)[.]([0-9]+)[.]([0-9]+)[.]0',r'\3.\2.\1', info["subnet"])
    now = datetime.datetime.now() # current date and time
    serial = now.strftime("%Y%m%d00")

# On vérifie la duplication d'IP et on met a jour le fichier de configuration DHCP associé

FalseIP=TreatConf()
print(FalseIP)
ReadAndWrite(len(FalseIP)-1)

f1.close()