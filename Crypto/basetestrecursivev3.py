import sys 
import math as m

# author  : CABOS Matthieu
# release : 09/02/2018

def reverse(s):
	str= ""
	for i in s:
		str=i+str
	return str

def splitTable(table):
	local_list=table.split('\n')
	res_list=[]
	for i in range (0,len(local_list)):
		res_list.append(local_list[i])
	return res_list

def table(base,debut,fin,inc):
	represent=''
	letter='a'
	powIndex=0
	count=0
	if(fin>10*base):
		fin=10*base
	for i in range(debut,fin):
		current=i
		if(i<base):
			if(i<10):
				represent+=str(i)
			else:				
				represent+=letter
				letter=chr(ord(letter)+1)
			if(i==base-1):
				letter='a'
		else:
			tmp=''
			while(current/base!=0):
				count=powIndex*10*base
				if(not current%(10*base)):
							powIndex+=1
				#print("i = " + str(i) + " | powIndex = "+ str(powIndex) + " | count = " + str(count) + " | mod = " + str(current%(10*base)))
				if(base<10):
					tmp+=str(current%base)
				else:					
					if(current%base<10):
						tmp+=str(current%base)
					else:
						tmp+=letter										
						if(count==0):
							letter=chr(ord(letter)+1)
						else:
							count-=1						
						if(current%base==base-1):
							letter='a'				
				current=int(current/base)
			represent+=reverse(tmp)
		represent+="\n"
	return represent


def rec_table_construct_lvl1(table,base,powindex,last):
	lettrebase=table[10:base]
	if(powindex == 1):
		del table[10*base]
	res=table[:]
	for i in range (len(table)-1,base**2-1):
		if(i%base==(base-1) and i!=len(table)-1):
			powindex+=1
		res.append(lettrebase[powindex-1]+str(table[(i-len(table)+1)%base]))
		# print("i = "+str(i)+" | i%base = "+str(i%base)+" | ib"+str(base)+" = "+str(res[i]))
	return res

def rec_table_construct_final(table,base,lvl):
	res=[]
	basetable=table[0:base]
	for i in range(0,len(basetable)):
		basetable[i]=basetable[i][lvl:]
	# print(basetable)	
	for eat in basetable:
		for this in table:
			res.append(eat+this)
	# print(res)
	# print(len(res))
	return res

def rec_manage(table):
	j=0
	for i in range(9,len(table)):
		# print("i = "+str(i))
		table2=table[i][:]
		table2=rec_table_construct_lvl1(table2,i+2,1,0)
		table2=rec_table_construct_final(table2,i+2,1)
		table2=rec_table_construct_final(table2,i+2,2)
		table[i]=table2[:]
	for i in range (9,18):
		j=3
		table2=table[i][:]
		while(len(table2)<1000000):
			table2=rec_table_construct_final(table2,i+2,j)
			j+=1
		table[i]=table2[:]
	# for i in range (19,28):
	# 	table2=table[i][:]
	# 	table2=rec_table_construct_final(table2,i+2,3)
	# 	table[i]=table2[:]
	return table

def ascii_to_int(chaine):
	res = []
	for letter in chaine:
		res.append(ord(letter))
	return res

def int_to_ascii(crypt):
	res = ''
	for i in range (0,len(crypt)):
		res+=chr(crypt[i])
	return res

def cryptChaine(to_crypt,table,base):
	res = []
	for i in range(0,len(to_crypt)):
		res.append(table[base][to_crypt[i]])
	return res

def local_table_dico(table2,base,rangeB):
	str_base={}
	res = {}
	if(rangeB>base**2):
		rangeB=base**2
	for i in range (0,rangeB):
		str_base[i]=table2[base][i]
	return str_base

def limit_range(Range,base):
	res=0
	if(Range>base**2):
		res=base**2
	else:
		res=Range 
	return res

def base_key(int_chaine):
	res=[]
	for i in range (0,len(int_chaine)):
		tmp=((int_chaine[i]*int_chaine[len(int_chaine)-i-1]+10)%36)
		if(tmp<10):
			tmp+=10
		res.append(tmp)
	return res 

def vec_poids(int_chaine):
	res = []
	res.append(int_chaine[0])
	for i in range(1,len(int_chaine)):
		res.append(res[i-1]+int_chaine[i])
	return res

def vec_1_poids(vec_poids):
	res=[]
	for i in range (0,len(vec_poids)):
		res.append(1/vec_poids[i])
	return res

def equa_2_nd(a,b,c):
	res = 0
	racine1 = 0.0
	racine2 = 0.0
	delta = b**2-4*a*c 
	if(delta>0):
		racine1 = (-b+m.sqrt(delta))/2*a
		racine2 = (-b-m.sqrt(delta))/2*a
	if(racine1>0):
		res = int(racine1)
	else:
		res = int(racine2)
	return res

def multlist(a,b):
	res = []
	if(len(a)!=len(b)):
		return []
	else:
		for i in range(0,len(a)):
			res.append(a[i]*b[i])
	return res

def transpose_base(liste,key,table):
	res = []
	if(len(liste)!=len(key)):
		return []
	else :
		for i in range (0,len(liste)):
			if(key[i]==10):
				res.append(liste[i])
			else:
				res.append(table[key[i]-2][liste[i]])
	return res

def inv_transpose_base(liste,key,table):
	res = []
	if(len(liste)!=len(key)):
		return []
	else:
		for i in range(0,len(liste)):
			if(key[i]==10):
				res.append(int(liste[i]))
			else:
				res.append(int(table[key[i]-2].index(liste[i])))
	return res

def crypt_procedure(chaine,table):
	int_chaine = ascii_to_int(chaine)
	base_keyy  = base_key(int_chaine)
	if(len(base_keyy)%2==0):
		key=base_keyy[0:int(len(base_keyy)/2)]
	else:
		key=base_keyy[0:int((len(base_keyy)/2)+1)]
	vec_poid   = vec_poids(int_chaine)
	crypt_lst  = multlist(int_chaine,vec_poid)
	crypt_lst  = transpose_base(crypt_lst,base_keyy,table)
	# print(crypt_lst)
	return(crypt_lst,key)

def cyclik_ascii(current):
	sep=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
	tmp=((sep.index(current)+1)%13)
	res =sep[tmp]
	return res

def crypt_final(tuple,int_chaine):
	sept=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
	res = ''
	sep =sept[int(int_chaine[1]*m.cos(int_chaine[0]))%13] 
	crypt=tuple[0]
	key=tuple[1]
	for i in range (0,len(crypt)):
		res+=sep+str(crypt[i])
		sep=cyclik_ascii(sep)
	return res

def slurp(chaine):
	tmp=''
	res = []
	sep=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
	for elem in chaine:
		if(not elem in sep):
			tmp+=str(elem)
			# print("tmp = "+tmp)
		else :
			res.append(tmp)
			# print("res = ")
			# print(res)
			tmp=''
		if(elem==''):
			break
	res=res[1:]
	res.append(tmp)
	return res

def resolve(liste):
	res = []
	x = 0
	tmp2 = 0
	res.append(int(m.sqrt(liste[0])))
	tmp=res[0]
	for i in range (1,len(liste)):
		# print("y = "+str(tmp))
		# print("x = "+str(x))
		tmp2 = equa_2_nd(1,-tmp,-liste[i])
		x=tmp2-tmp
		res.append(int(x))
		tmp=tmp2
	# print(res)
	return res

def decrypt_procedure(chaine,key,table):
	res = ''
	base=key[:]
	tmp = []
	key.reverse()
	tmp = key[:]
	to_find = []
	to_find=slurp(chaine)
	if(len(to_find)%2==0):
		base+=tmp[0:len(key)]
	else:
		base+=tmp[1:len(key)]
	tmp_liste=inv_transpose_base(to_find,base,table)
	int_liste=resolve(tmp_liste)
	res = int_to_ascii(int_liste)
	return res

def split(chaine,seuil):
	res = []
	tmp = ''
	index = 0
	div=int(len(chaine)/seuil)
	for i in range(0,div):
		tmp=''
		print("index = "+str(index)+" | seuil = "+str(seuil)+" | i = "+str(i))
		for j in range(index,(index+seuil)):
			tmp+=chaine[j]
			print("j = "+str(j)+" | tmp = "+str(tmp))
			if(j==(index+seuil-1)):
				index=j+1
		res.append(tmp)
	if((index-1)<len(chaine)):
		tmp=chaine[index:]
		res.append(tmp)
	return res

def tilps(chaine):
	res = ''
	for i in range (0,len(chaine)):
		res+=chaine[i]
	return res

represent=''
table2 = []
dic = {}
main_dic={}
choice = ' '
chaine=''
chaine=sys.argv[1]

if(len(sys.argv)!=4):
	Basemin = 2
	Basemax = 37
	Range   = 36**2
else : 	
	Basemin = int(sys.argv[1])
	Basemax = int(sys.argv[2])
	Range   = int(sys.argv[3])

if(Basemin<2 or Basemax>37):
	print("Affichage impossible veuillez selectionner une plage de valeure contenue dans [2,36]")
	exit(0)

maxi=Basemax-Basemin

for i in range(Basemin,Basemax):
	table2.append(table(i,0,Range,1))

for i in range (0,len(table2)):
	table2[i]=splitTable(table2[i])

for j in range (0,len(table2)):
	table2[j]=rec_table_construct_lvl1(table2[j],j+2,1,0)
	for k in range(0,j+2):
		table2[j][k]=(str(0)+table2[j][k])
table2=rec_manage(table2)


# print("Max int = "+str(sys.maxsize))
# for i in range(9,len(table2)):
# 	print("Length Base "+str(i+2)+" = "+str(len(table2[i])))
choice = ''
userchoice=0
while(choice!='q'):
	if(userchoice):
		chaine=input("Veuillez entrer la chaine à crypter : ")
	res = ()
	res=crypt_procedure(chaine,table2)
	testc = res[0]
	testk = res[1]
	testkey=''
	int_chaine=(ascii_to_int(chaine))
	sep=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
	sep_lvl2=[":",";","<","=",">","?","@"]
	# sepk=sep[int(int_chaine[1]*m.cos(int_chaine[0]))%13] 
	for i in range(0,len(testk)):
		testkey+=str(testk[i])
		# testkey+=sepk
		# sepk=cyclik_ascii(sepk)
	raw_txt = crypt_final(res,int_chaine)
	print("---------------------------------")
	print("Chaine cryptée : \n")
	print(raw_txt)
	print("---------------------------------")
	print("Clé unique : \n")
	print(testkey)
	print("---------------------------------")
	clean_txt = decrypt_procedure(raw_txt,testk,table2)
	print("Chaine décryptée : \n")
	print(clean_txt)
	choice=input("c)ontinuer ou q)uitter")
	if(choice!='q'):
		userchoice+=1

# for i in range (0,len(table2)):
# 	dic=local_table_dico(table2,i+2,len(table2[i]))
# 	main_dic["Base" + str(i+2)]=dic

# while(choice!='q'):
	# localbase=int(input("Please enter base indice : "))
	# if(localbase>=37):
		# print("Work in progress, thanks 4 ur patience")
		# exit(0)
	# localbase-=2
	# local_range=limit_range(Range,localbase+2)
	# print(local_range)
	# for i in range(0,local_range):
		# print(str(i) + " | "+str(table2[localbase][i]))
	# print("3 x 8 = " + str(table2[localbase][3*8]))
	# table2=rec_manage(table2)
	# print("test recursive build : done")
	# table3=table2[localbase][:]
	# table3=rec_table_construct_lvl1(table3,localbase+2,1,0)
	# print("-----------------------------------------------")
	# print(table3)
	# table3=rec_table_construct_final(table3,localbase+2,1)
	# table3=rec_table_construct_final(table3,localbase+2,2)
	# print("-----------------------------------------------")
	# print(table3)
	# for i in range(0,len(table3)):
	# 	print(str(i) + " | "+str(table3[i]))
	# try:
		# print(table3[1679614])
		# choice='q'
	# except: choice=input("c)ontinue or q)uit") 
	

# print("test dico : ")
#Chrono on
# testbase=int(input("Please enter base : "))
# testvalue=int(input("Please enter number"))
# tmpvalue=main_dic["Base"+str(testbase)][testvalue]
# print(str(testvalue) + "b" + str(testbase) + " = " + str(tmpvalue))
#Chrono off

# while range>=10*base => split/concat/range:10

