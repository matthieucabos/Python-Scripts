# GLPI

**Author** : *CABOS Matthieu*

**Release** : *25/10/2021*

**Organisation** : *ICGM-CNRS*


____________________________________________________________________________

# Usage

To use, please to create a *'GLPI'* Folder into your server root Repertory.

This Root repertory must contain the 'Switchs.ods' file containing the Routing Table of the Cisco Network.

The Switchs.ods file must use the form :

**Room id | Staff | Socket id | VDI | Cisco name | n° Switch | n° on the banner | row of headband | Switch Socket n° | vLan Id**

It must be present at top level of **Set_SQL_Roomname.py** :

Folder Structure::

************************************
```bash
.
├── GLPI
│   └── Set_SQL_Roomname.py
└── Switchs.ods
```
************************************

To generate the associated SQL File, please to use the command :

```bash
python3 Set_SQL_Roomname.py
```

It will produce the file my_glpi.sql wich allow to update a GLPI server.

# Support

For any support request, please mail @ matthieu.cabos@umontpellier.fr
