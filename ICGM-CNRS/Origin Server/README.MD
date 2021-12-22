# Origin Server


**Author** *CABOS Matthieu*

**Date**  *2020/2021*

**Organization** *ICGM-CNRS*

______________________________________________________________________________________________________

These Scripts have been written to manage properly an Origin Server (See [*Origin*](https://ritme.com/software/origin/) )

It is adapted to the Origin ssh platform (reading and treating **opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses** and **/usr/local/flexlm/orglabdebug.log**
wich are the Licence File and the Tokens Log file.

Two main scripts have been written to automate the DHCP Informations retrievmen : 

[1/ Get_User_Info_From_IP_v3.py](https://github.com/matthieucabos/Python-Scripts/tree/master/ICGM-CNRS/DHCP#get_user_info_from_ip_v2py)

[2/ Origin_Users.py](https://github.com/matthieucabos/Python-Scripts/tree/master/ICGM-CNRS/DHCP#origin_userspy)

___________________________________________________________________________________________________

## Get_User_Info_From_IP_v3.py

This script is the optimised version of the Origin_Users.py script.

Since the two first versions, the optimised version is ruled differently from the first one :
* **Cut logfile** since the date (today as default)
* **Read and extract informations** from the logwatch file with the associated *Treat_log_v2.sh* Scripot
* **Open, read & Treat the logwatch** file :
  * **Getting IP list** associated to a timed & named token. The resultys are stored by time order, arbitrary indexed from 1 -> n
  * **Getting host ID** from the full Origin user name (with form name@host) => Allow multiple users sessions on the same host
  * **Compute the Cantor difference** between two adjacents set (indexed +- 1) to get the User's associated IP
* **Building DHCP dictionnary** and get infos since the given IP adresses list as parameter :
  * **Building DHCP Dictionnary**
  * **Updating Users Dictionnary** since the DHCP dictionnary from the ip correspondance (as key entry of the Users dictionnary)
  * **Updating the Users Dictionnary** since the Cisco output command : ssh <Cisco_name> 'show mac address' to get the associated cisco switch ID and the gigabit ethernet ID
* **Finaly write the RAM stored informations dictionnary** into the Origin_history file

Please to use with the correct syntax :

```bash
python3 Get_User_Info_From_IP_v3.py
```

The script must be used into an equivalent environment structure :

```bash
.
├── DHCP
│   └── Get_User_Info_From_IP_v3.py
└── dhcpd-vlan_i.conf
└── dhcpd-vlan_i+1.conf
.
.
.
└── dhcpd-vlan_n.conf
```


These actions need an efficient log file since the Origin server orglabdebug.log file.
I use a logwatch intermediate file with allocated token inserted into the token log file.
It is ruled by automatic script : 

```bash
date >> ./logwatch
ss -n -t | grep 60213 >> ./logwatch
tail -n 1 /usr/local/flexlm/orglabdebug.log >> ./logwatch
```
This script is lauched periodically with commands :

```bash
inotifywait -q -m -e modify /usr/local/flexlm/orglabdebug.log|
while read -r filename event; do
 ./Script.sh       
done
```

The result is shown with the following syntax :

```bash
{'mac': '90b1.1ca3.3575', 'ip': '10.14.18.145', 'hostname': '"BBBAACCC"', 'departement': 'DPT4', 'vlan': 513, 'cisco': 'Balard-PAC-2', 'socket': '1/0/36', 'Description': 'RJLG07-01', 'origin_name': 'c2mstud@c2mstud3-pc', 'connexion time': '198.3088238040606 min'}
```

With :


| **Field Identifier** | **Data Type**      | **Description**                                                                           |
|----------------------|--------------------|-------------------------------------------------------------------------------------------|
| **mac**              | Hexadecimal string | *The full mac address of the current User*                                                |
| **ip**               | Decimal string     | *The full fixed IP from the origin server*                                                | 
| **hostname**         | String             | *The Hostname from the DHCP server (could be different from the Origin server Hostname)*  |
| **departement**      | String             | *The departement description section*                                                     |
| **vlan**             | Integer            | *The sub-network lan Identifier*                                                          |
| **cisco**            | String             | *The Cisco Switch Identifier Name*                                                        |
| **socket**           | Decimal String     | *The associated Gigabit Ethernet socket (with form **x/y/z**)*                            |
| **Description**      | String             | *The associated outlet exact name (as it is written in a Cisco Switch)*                   |
| **origin_name**      | String             | *The Origin User's avatar name*                                                           |
| **connexion time**   | Float              | *If still connected, the connection time of the User, else the starting connection time*  |

Finally written into the Origin_history file into the **origin.srv-prive.icgm.fr** server.
 
## Origin_Users.py

### From Version 1

This script is used to get a full repertory of connected Users on the [*Origin*](https://fr.wikipedia.org/wiki/Origin_(logiciel)) server of the ICGM laboratory.
It use the Licence informations to write the proper Connection history file.

To make it, the algorithm follow these steps below :
* **Initialisation** : *Variables definition to store the temporary infos*
* **Getting Users acount informations since the top level** : *Using the os.getenv function, I get the ssh needed informations to connect*
* **Connecting an ssh session to the origin.srv-prive.icgm.fr server** : *Starting an ssh session with netmiko*
* **Getting users list Informations** : *Getting the connected users informations since Origin's jetons*
* **Getting the Port Informations** : *Getting the port numbers informations since the* ```bash netstat -anp ```
* **Getting the raw IP list informations** : *Getting and treating the IP list informations since the* ```bash ss -n -t``` *command*
* **Getting the raw hostname list Informations** : *Getting and treating Port numbers informations since the* ```bash ss -n -t -r``` *command*
* **Exit the ssh session and read the Ordinateurs.ods file** : *Close the current session with netmiko*
* **Updating the Origin_history file since the newest Informations** : *Updating history with the command*
```bash 
scp ./Origin_history <user>@origin.srv-prive.icgm.fr
```

### From Version 2 :

These actions need an efficient log file since the Origin server orglabdebug.log file.
I use a logwatch intermediate file with allocated token inserted into the token log file.
It is ruled by automatic script : 

```bash
date >> /tmp/logwatch
ss -n -t | grep 60213 >> /tmp/logwatch
tail -n 1 /usr/local/flexlm/orglabdebug.log >> /tmp/logwatch
```
This script is lauched periodically with commands :

```bash
inotifywait -q -m -e modify /usr/local/flexlm/orglabdebug.log|
while read -r filename event; do
 bin/script.sh       
done
```
Once the logwatch file properly instanced, I read it and treat informations since the token allocations.
The intermediate algorithm is ruled by following steps :

* **Cut logfile** since the date (today as default)
* **Read** the log file
* **Treat Log file content** since regular expression to get 
  * *IP_@ list*
  * *New user information*
* **Associate a new user** to the difference between 2 log slice
* **Compute the Set Cantor difference** by User ID
* **Get the real (most susceptible one) IP_@** from user name

Once these informations found, there are linked to the already existing database since the IP adress to obtain the exact Elapsed connection time and the exact login name foreach user.

The result is shown with the following syntax :

```bash
<Switch Cisco Name> | <Vlan Number> <MAC_@> <Cisco Socket> | <Hostname> | <Departement> | <Ip_@> | <Socket Description> | <User login> | <Time Elapsed>
```
Finally written into the Origin_history file into the **origin.srv-prive.icgm.fr** server.

Please to use this script with the correct syntax (and the latest version):

```bash
python3 Origin_Users_parallelisation_v2.py
```

The script must be used into an equivalent environment structure :

```bash
.
├── DHCP
│   └── Origin_Users.py
└── Ordinateurs.ods
```

Where Ordinateurs.ods is the DHCP authorisation list table with form :

```bash
<Hostname> | <MAC_@> | <Vlan> | <Relative Informations>
```

## Support

For any Support request, please to mail @ **matthieu.cabos@umontpellier.fr**
