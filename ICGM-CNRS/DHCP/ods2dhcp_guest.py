import re
import pyexcel as p
import datetime
import os

__author__='CABOS Matthieu'
__date__=10/11/2021

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

# On parcourt le fichier conf du vlan 519

info=vlans['ICGM-GUEST'];
id=info['id'];
registred={}
lastIP[id]=info['init']
if os.path.isfile("dhcpd-%d.conf"%(id)):
	with open("dhcpd-%d.conf"%(id), "r") as openfileobject:
		ip="";mac="";
		for line in openfileobject:
			# print(line)
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
	counter=int(os.popen('cat dhcpd-519.conf | tail -11 | head -1 | grep -Po "\K[0-9]*"').read())

def get_date(string):
	y=int(string[:4])
	m=int(string[5:7])
	d=int(string[8:])
	return datetime.date(y,m,d)

# On parcours le contenu du fichier lu

for record in records:
	if (not record['Adresse Mac']==''):
		str_date=str(record['Date d’arrivée'])
		dateA=get_date(str_date)
		str_date2=str(record['Date de départ'])
		dateD=get_date(str_date2)
		today=datetime.date.today()

		# Si la date courrante est comprise entre la date d'arrivée et la date de départ

		if dateA <= today and today <= dateD :
			counter+=1
			nom='Guest'+str(counter)
			# On met à jour l'historique des visites
			os.system('echo '+str(nom)+' Nom :  '+str(record['Nom de l’invité'])+' '+str(record['Adresse Mac'])+' Arrivée : '+str(record['Date d’arrivée'])+' Départ : '+str(record['Date de départ'])+' >> registred_guests')
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
						lastIP[id]=lastIP[id]+1
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
					if (len(nom)>7):
						info["dns"]=info["dns"]+"%s\tIN\tA\t%s\n"%(nom, ip)
					else:
						info["dns"]=info["dns"]+"%s\t\tIN\tA\t%s\n"%(nom, ip)
					numbers=ip.split('.')
					info["rev"]=info["rev"]+"%d\tIN\tPTR\t%s.%s.\n"%(int(numbers[3]),nom,info["subdomain"])
				else:
					print("Vlan %s non trouvé" % (vlan))

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
    fhost=open("%d.host"%(info["id"]),"w")
    now = datetime.datetime.now() # current date and time
    serial = now.strftime("%Y%m%d00")

    # On écrit le fichier host

    fhost.write("""$TTL 43200
@               IN      SOA     dhcpd.srv-prive.icgm.fr.  Fabrice\.Boyrie.icgm.fr. (
                    %s ; serial
                    43200 ; refresh
                    3600 ; retry
                    3600000 ; expire
                    604800 ; default_ttl
                    )
;
;
@               IN      NS    dhcpd.srv-prive.icgm.fr.
_vlmcs._tcp     IN      SRV   0 0 1688  snkms.unistra.fr. 
"""%(serial))
    fhost.write(info["dns"])
    fhost.close()

    # On écrit le fichier rev

    frev=open("%d.rev"%(info["id"]),"w")
    frev.write("""$TTL 43200
@               IN      SOA     dhcpd.srv-prive.icgm.fr.  Fabrice\.Boyrie.icgm.fr. (
                    %s ; serial
                    43200 ; refresh
                    3600 ; retry
                    3600000 ; expire
                    604800 ; default_ttl
                    )
;
;
@               IN      NS    dhcpd.srv-prive.icgm.fr.
"""%(serial))
    frev.write(info["rev"])
    frev.close()
f1.close()