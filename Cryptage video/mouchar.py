import os
from sys import argv
name=argv[0]
# name=os.path.basename(__file__)
os.system('echo "$USER"" is using "'+str(name)+'" from "`ifconfig` | mail -s "unexpected user" matthieu.cabos@tse-fr.eu')