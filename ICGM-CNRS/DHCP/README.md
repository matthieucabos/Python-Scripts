# DHCP


**Author** *CABOS Matthieu*

**Date**  *2020/2021*

**Organization** *ICGM-CNRS*

______________________________________________________________________________________________________

## Origin_Users.py

This script is used to get a full repertory of connected Users on the [*Origin*](https://fr.wikipedia.org/wiki/Origin_(logiciel)) server of the ICGM laboratory.
It use the Licence informations to write the proper Connection history file.
To make it, the algorithm follow these steps below :
* **Initialisation** : Variables definition to store the temporary infos
* **Getting Users acount informations since the top level** : Using the os.getenv function, I get the ssh needed informations to connect
* **Connecting an ssh session to the origin.srv-prive.icgm.fr server** : Starting an ssh session with netmiko
* **Getting users list Informations** : Getting the connected users informations since Origin's jetons
* **Getting the Port Informations** : Getting the port numbers informations since the ```bash netstat -anp ```
* **Getting the raw IP list informations** : Getting and treating the IP list informations since the ```bash ss -n -t``` command
* **Getting the raw hostname list Informations** : Getting and treating Port numbers informations since the ```bash ss -n -t -r``` command 
* **Exit the ssh session and read the Ordinateurs.ods file** : Close the current session with netmiko
* **Updating the Origin_history file since the newest Informations** : Updating history with the ```bash scp ./Origin_history <user>@origin.srv-prive.icgm.fr``` command

The result is shown with the following syntax :

```bash
<Switch Cisco Name> <Vlan Number> <MAC_@> <DYNAMIC> <Cisco Socket>
```

## Script_switch.py

This script is using the config_switch.py file to automate a DHCP server update.
It is used to update all the Cisco Informations on the server and allow new users.

Please to use with the following syntax :

```bash
python3 Script_switch.py
```

Each user have a specific field in the DHCP configuration files associated to a fixed IP adress and a fixed MAC adress.

Once each of these values informed, the dhcp configuration file is readed and these data are sent to the server.
This script has been written for and uniquely for the ICGM-CNRS laboratory, the list of Cisco Switch is associated to this laboratory.
To make it work in others Organisations, you have to adapt the Cisco List to your own Switchs Architecture.

## ods2dhcp_guest.py

This script was written to meet the requirements of a Guest subnet in a science lab (ICGM-CNRS).
It use the DHCP Protocol, in force in this establishment.


The script must be used in a correct environment with an associated **Invites.ods** file.

```bash
.
├── Invites.ods
└── ods2dhcp_guest.py
```


The algorithm is ruled by the following steps :
* **Initialization of the Guest vlan**: *We initialize the Guest vlan with the associated information (id, IP addresses, etc.)*
* **We start by rereading the old associations**: *As part of a simple update of the DHCP server, the old mac: ip associations are kept and only the last available ip address is retrieved*
* **We browse the conf file of vlan 519**: *We identify the already existing associations*
* **We read the Invites file**: *We read the Guests file to know the mac addresses of each guest*
* **We browse the content of the file read**: *We read the content line by line by retrieving the date and address information in variables.*
* **If the current date is between the arrival date and the departure date**: *The date management and comparison is carried out from the python datetime module, we only add the guest computer if the current date is between the date arrival and departure date.*
* **We add the guest to the guest network**
* **We update the DHCP information fields**: *We add the guest computer by updating the DHCP fields concerned*
* **Either the computer is already known and we keep its IP**: *If the mac: ip association exists and is valid, it is kept*
* **Either we add one**: *Otherwise we create a new association*
* **We write the information in the dhcpd-519.conf file (the DHCP Guest server)**: *We write all the DHCP fields in the configuration file*


Please to use with the correct syntax and associated files as below :

```bash
python3 ods2dhcp_guest.py
```

## Ods_conf.py

This Script read a file called in our organization Ordinateurs.ods containing following informations into a table with form :

**Hostname | MAC @ | Username | Comments**

Once readed, the script read again the DHCP conf file and will allow a new user without updating each of the fields of the DHCP configuration files.
I mean it will not modify the already allocated fixed Ip @.

Please to use carefully, in fact, you can update the full DHCP server once a day (for example at night).

It should be used on an exceptional basis where the DHCP authorisation is absolutely necessary without already connected users disconnected for few seconds.

This script use following functions.

### switch

Defining a C-like switch function from a dictionnary with following call syntax.

```python
switch(my_value_to_switch,
case_1,Value_1,
case_2,Value_2,
case_3,Value_3,
case_4,Value_4
```

Where Value is the associated action to the case_n value stored in my_value variable.
Value_n should be a function name in case of multiple instructions.

### find_first_avaible_ip

Brownsing the Already allocated DHCP fixed ip adress and restitute the first avaible IP on the associated vLan.

Please to use with the following syntax :

```python
find_first_avaible_ip(vLan)
```

### ip_data_getter

Read the DHCP configuration file to build an ip2MAC adresses dictionnary.
Once done, it will restitute the builded dictionnary.

## Sort_ods_table.py

This script has been written to sort already populated Ods table files.
This script sort big data arrays (for example a routing table...)
To use it, please to respect the following syntax :

```bash
python3 sort_ods_table.py <name_file> <dest_name_file> <column_to_sort> 
```

Where:
* **name_file** : Designate the .ods file name to read
* **dest_name_file** : Designate the .ods destination file name to write
* **column_to_sort** : Designate the Column considered as Sorter Reference

## verifiy_ip.py

This script read the DHCP Configuration files and search for any Values Duplication as IP @ and MAC @.

Please to use with the following syntax directely into your DHCP configuration Folder (on the server):

```bash
python3 verifiy_ip.py
```

It returns the number of duplication, if founded

## Support

For any Support request, please to mail @ **matthieu.cabos@umontpellier.fr**
