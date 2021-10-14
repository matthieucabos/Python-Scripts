#!/usr/bin/python3
#pip3 install pyexcel
#pip3 install pyexcel.ods --user
import re
import sys
import pyexcel as p
from datetime import datetime
if (len(sys.argv)==2):
    LimitSwitch=sys.argv[1]
else:
    LimitSwitch=""
    
switchs={}
records = p.iget_records(file_name="Switchs.ods")
for record in records:
    vlan=record['vlan']
    if(vlan != ""):
        switch=record['Switch']
        numSwitch=record['N° du switch dans la pile']
        numPriseSwitch=record['Numéro sur le switch']
        commande="interface GigabitEthernet%d/0/%d\n"%(numSwitch, numPriseSwitch)
        PriseBureau=record['Prises'];
        colonne=record['N° sur bandeau']
        commande=commande+"description %s, vlan %d, col%d\n"%(PriseBureau, vlan, colonne)
        commande=commande+"switchport access vlan %d\n"%(vlan)
        commande=commande+"ip dhcp snooping limit rate  50\n"
        commande=commande+"switchport port-security maximum 1\n"
        commande=commande+"switchport port-security violation restrict\n"

        if(switch in switchs):
            switchs[switch]=switchs[switch]+commande;
        else:
            switchs[switch]=commande;

for switch in switchs:
    if(switch==LimitSwitch) or (LimitSwitch==""):
        print("ssh -tt %s  <<EOF"%(switch))
        print("enable")
        print("configure terminal")
        print(switchs[switch])
        print("exit")
        print("exit")
        print("wr")
        print("exit");
        print("EOF")
    else:
        print("#Switch %s omis" % (switch))
        
