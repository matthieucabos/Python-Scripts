# DHCP


**Author** *CABOS Matthieu*

**Date**  *2020/2021*

**Organization** *ICGM-CNRS*

______________________________________________________________________________________________________

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
