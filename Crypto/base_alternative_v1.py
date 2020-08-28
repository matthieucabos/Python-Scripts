from base_opt import *
import random as r

#Author : CABOS Matthieu
#Date : 02/2020

sep=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
vir=[]

# Construction de la table des bases

table=table()

# Algorithme de cryptage

# txt=input("Entrez un texte")
txt="salut bande de nazes"
# txt="salut bande de nazes, on va tester une chaine de grande longueur pour verifier si l'algorithme fonctionne toujours"
l=[]
res=[]
for i in range(len(txt)):
	l.append(ord(txt[i]))

print(l)
print("#################################")

first=int(l[0])
for i in range(0,len(l)-1):
	res.append(float(l[i+1]/l[i]))
key=[]
for i in range(0,len(l)-2):               # Finir la chaine de texte par trois caractères "usuels", par exemple "..."
	key.append(int((l[i]*l[i+1])%l[i+2])) # Eventuellement ameliorer la clé en la complementant a 36 sur [10,36] 
	key[i]=(key[i])%26

print(res)
print("#################################")

for i in range(len(res)):
	res[i]=int(res[i]*10000)
res.append(first)
key.append(key[0])	#key padding
key.append(key[1])

print(len(res))
print(len(key))
print(key)
print("################################")
print(res)
print("################################")

crypt=[]
for i in range(len(res)):
	crypt.append(table[key[i]][res[i]])

# rajouter des operations de listes reversibles 

string=""
for i in range(len(crypt)):
	string+=crypt[i]
	string+=sep[r.randint(0,13)]

print(string)
print("################################")

#######################################################################################################

rez=[]
tmp=''
ind=0
for item in string:
	if not item in sep:
		tmp+=item
		# print(tmp)
	else:
		rez.append(table[key[ind]].index(tmp))
		tmp=''
		ind+=1
firstt=rez[-1]
rez=rez[:-1]

print(rez)
print("################################")

# Algorithme de décryptage

for i in range(0,len(rez)):
	rez[i]=rez[i]/10000

print(rez)
print("################################")

rezz=[]
rezz.append(first*rez[0])

print(rez)
print("################################")

for i in range(1,len(rez)):
	rezz.append(rez[i]*rezz[i-1])

print(rezz)

final=[]

for i in range(len(rezz)):
	final.append(chr(round(rezz[i])))
txt=[]
txt.append(chr(first))
for i in range(len(final)):
	txt+=final[i]
	
print(txt)