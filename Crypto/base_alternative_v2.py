from base_opt import *
import random as r
#Author : CABOS Matthieu
#Date : 02/2020

sep=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
vir=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# Construction de la table des bases

table=table()

def mirror(liste):
	res=liste[:]
	for i in range(1,len(liste)):
		res.append(liste[-i])
	res.append(liste[0])
	return res

# Algorithme de cryptage

# txt=input("Entrez un texte")
txt="salut bande de nazes"
# txt="une autre chaine pour"
# txt="salut bande de nazes, on va tester une chaine de grande longueur pour verifier si l'algorithme fonctionne toujours"
l=[]
res=[]
for i in range(len(txt)):
	l.append(ord(txt[i]))

print("l = ")
print(l)
print("#################################")

first=int(l[0])
for i in range(0,len(l)-1):
	res.append(float(l[i+1]/l[i]))
key=[]
for i in range(0,len(l)-2):               # Finir la chaine de texte par trois caractères "usuels", par exemple "..."
	key.append(int((l[i]*l[i+1])%l[i+2])) # Eventuellement ameliorer la clé en la complementant a 36 sur [10,36] 
	key[i]=(key[i])%26

print("res =")
print(res)
print("#################################")

for i in range(len(res)):
	res[i]=int(res[i]*10000)
res.append(first)
key.append(key[0])	#key padding
key.append(key[1])

print(len(res))
print(len(key))
print("key = ")
print(key)
print("################################")
print("res =")
print(res)
print("################################")

tmp=0
Float_res=[]
Mirror_key=[]
Mirror_key=mirror(key)

for i in range(len(res)):
	tmp = res[i]/(key[i]+1)
	Float_res.append(int(tmp))
	Float_res.append(int((tmp-int(tmp))*1000))
	tmp=0.0

print("Float_res = ")
print(Float_res)
print("################################")
print(len(Float_res))
print(len(Mirror_key))
#ICI
for i in range(len(Float_res)):
	Float_res[i]*=10

crypt=[]
for i in range(len(Float_res)):
	crypt.append(table[Mirror_key[i]][Float_res[i]])
print(crypt)
print("################################")
# rajouter des operations de listes reversibles 

string=""
ind=0
for i in range(len(crypt)):
	string+=crypt[i]
	if(ind%2==0):
		string+=vir[r.randint(0,25)]
	else:
		string+=sep[r.randint(0,13)]
	ind+=1

print("string = ")
print(string)
print("################################")

#######################################################################################################

rez=[]
tmp=''
ind=0
for item in string:
	if not item in sep and not item in vir:
		tmp+=item
		# print(tmp)
	else:
		rez.append(table[Mirror_key[ind]].index(tmp))
		tmp=''
		ind+=1
firstt=rez[-1]
rez=rez[:-1]

print("rez =")
print(rez)
print("################################")

for i in range(len(rez)):
	rez[i]/=10
Float_rez=[]
for i in range(0,len(rez)):
	if(i%2==0):
		tmp=rez[i]
	else:
		Float_rez.append(tmp+rez[i]/1000)
		tmp=0.0
		
print("Float_rez = ")
print(Float_rez)
print("################################")

# Algorithme de décryptage

rez=[]
for i in range(len(Float_rez)):
	rez.append(round(Float_rez[i]*(Mirror_key[i]+1)))

print("rez =")
print(rez)
print("################################")

rezz=[]
rezz.append((first*rez[0])/10000)

print("rez =")
print(rez)
print("################################")

for i in range(1,len(rez)):
	rezz.append((rez[i]*rezz[i-1])/10000)

print(rezz)

final=[]

for i in range(len(rezz)):
	final.append(chr(round(rezz[i])))
txt=[]
txt.append(chr(first))
for i in range(len(final)):
	txt+=final[i]
	
print(txt)