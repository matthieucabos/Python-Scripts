import sys 
import math as m
import random as r
# codes from math:
# sqrt
# cos
# randint (moindre carré)

# high resolution cryptographic protocol
# author  : CABOS Matthieu
# release : 12/02/2018
# only for security tools as :
#   * autentification security
#   * cryptographic procedure
#   * software protection
# WARNING : i don't support any other use, use with extreme precaution

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

def cyclik_ascii_lvl2(current):
	sep=[":",";","<","=",">","?","@"]
	tmp=((sep.index(current)+1)%6)
	res =sep[tmp]
	return res

def cyclik_ascii_lvl3(current):
	sep=['A','B','C','D','E','F','G','H','I','J','K','L'] 		
	tmp=r.randint(0,11)
	res = sep[tmp]
	return res

def cyclik_ascii_mesquin(current,int_chaine):
	mesquin=['M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] 
	tmp=r.randint(0,11)
	res=mesquin[tmp]
	return res

def reverse(liste):
	res=[]
	for i in range(0,len(liste)):
		res.append(liste[len(liste)-i-1])
	return res

def split_number(num):
	res=[]
	while(num>0):
		res.append(num % 10)
		num=int(num/10)
	return reverse(res)

def complement_at(x,base=2):
	return (base-1-x)

def get_value(x,table,base):
	ind=0
	while(table[base][ind]!=x):
		ind+=1
	return ind

def complement_at_sup11(x,table,base=11):
	nb_char=len(x)
	local_max=0
	for i in range(0,nb_char):
		local_max+=(base-1)*base**i
	num_value=local_max-get_value(x,table,base)
	return table[base][num_value]

def complement(x,table,base=2):
	final_res=0
	if(base<=10):
		splitted=split_number(int(x))
		for i in range(0,len(splitted)):
			splitted[i]=complement_at(splitted[i],base)
			final_res*=10
			final_res+=splitted[i]
		return final_res
	else:
		final_res=complement_at_sup11(x,table,base)
		return final_res

def crypt_final(tuple,int_chaine,table):
	sept=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
	res = ''
	sep =sept[int(int_chaine[1]*m.cos(int_chaine[0]))%13] 
	crypt=tuple[0]
	key=tuple[1]
	tmp_len=len(key)
	if(len(key)%2==0):
		for i in range(1,tmp_len):
			key.append(key[tmp_len-i-1])
	else:
		for i in range(0,tmp_len):
			key.append(key[tmp_len-i-1])
	for i in range (0,len(crypt)):
		# injective crypt[i]
		res+=sep+str(complement(crypt[i],table,key[i])) 
		sep=cyclik_ascii(sep)
	return res

def crypt_final_long(liste,int_chaine,table):
	sept=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
	res = ''
	sep =sept[int(int_chaine[1]*m.cos(int_chaine[0]))%13] 
	for i in range (0,len(liste)):
		res+=sep+str(liste[i])
		sep=cyclik_ascii(sep)
	# print(res)
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

def slurp2(chaine):
	tmp=''
	res = []
	sep=[":",";","<","=",">","?","@"]
	for elem in chaine:
		if(not elem in sep):
			tmp+=str(elem)
		else:
			res.append(tmp)
			tmp=''
		if(elem==''):
			break
	res.append(tmp)
	return res

def slurp3(chaine):
	tmp=''
	mesquin=['M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	for elem in chaine:
		if(not elem in mesquin):
			tmp+=str(elem)		
	return tmp

def slurp4(chaine):
	tmp=''
	res = []
	sep=['A','B','C','D','E','F','G','H','I','J','K','L'] 	
	for elem in chaine:
		if(not elem in sep):
			tmp+=str(elem)
		else:
			res.append(tmp)
			tmp=''
		if(elem==''):
			break
	res.append(tmp)
	return res

def miam(key):
	tmp=''
	count=1
	res=[]
	for this in key:
		# print("this = "+str(this))
		# print("tmp = "+str(tmp))
		if(count%2==0):
			tmp+=str(this)
			count=1
			# print("tmp = "+str(tmp))
			res.append(tmp)
			tmp=''
		else:
			tmp=str(this)
			count+=1
	for i in range(0,len(res)):
		res[i]=int(res[i])
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
	print(len(to_find))
	print(len(key))
	for i in range(0,len(to_find)):
		#injective inverse to_find[i]
		to_find[i]=complement(to_find[i],table,base[i])
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
		# print("index = "+str(index)+" | seuil = "+str(seuil)+" | i = "+str(i))
		for j in range(index,(index+seuil)):
			tmp+=chaine[j]
			# print("j = "+str(j)+" | tmp = "+str(tmp))
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

def mesqui(txt,seuil):
	mesquin=['M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	res=''
	sep='M'
	for i in range(0,len(txt)):
		res+=txt[i]
		if(i%int((seuil))==0):
			res+=sep 
			sep=cyclik_ascii_mesquin(sep,int_chaine)
	return res


# firs step numeric base construction
def tablebase(base):
	res = []
	letter = 'a'
	letterbis = 'A'
	# //
	for i in range(0,base):
		if(i<10 or (i<=10 and base <=10)):
			res.append(str(i))
		if(i>=10 and base >10 and base<37):
			res.append(letter)
			letter=chr(ord(letter)+1)
	return res

# first level recursive build
def recursive_build(table_base):
	res = []
	# //*2
	for i in table_base:
		for j in table_base:
			res.append(i+j)
	return res

# first level recursive build in safe mode
def recursive_build_sup_lvl_safe_mode(current,indice):
	res = []
	#//
	for i in current:
		res.append(str(indice)+str(i))
	return res

# final level recursive build (the best one) 
def recursive_build_sup_lvl(table_base,current,lvl):
	res   = []
	break_ind = 0
	#//
	for i in table_base:	
		try :
			res.extend(recursive_build_sup_lvl_safe_mode(current,i))
		except:
			print("break in method : recursive_build_sup_lvl")
			break_ind=1
			break
	return (res,break_ind)

def table():
	rec_level_h = [6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4]
	rec_level_m = [5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3]
	rec_level_l = [4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
	table       = []
	bases       = []
	tmp         = ()
	ok          = 0
	mini        = 11
	mytime      = 0
	fini        = 0
	finalt      = 0

	for i in range (mini,37):
		ind = 1
		ok  = 0
		bases.append(tablebase(i))
		table.append(recursive_build(bases[i-mini]))
		# print(table[i-mini])
		# print(bases[i-mini])
		while(not ok):
			# print("i-mini = "+str(i-mini)+" | len table = "+str(len(table[i-mini]))+" | ok = "+str(ok))
			tmp=recursive_build_sup_lvl(bases[i-mini],table[i-mini],ind)
			table[i-mini]=tmp[0]
			ind+=1
			# print("recursive level "+str(ind))
			if(ind==rec_level_l[i-mini]):
				ok=1
	return table

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
table2=table()
long_chaine = []
long_crypt  = []
longi=0
seuil = 20
seuil_lvl2=70
choice = ''
userchoice=0
sep=['!','"','#','$','%','&','(',')','*','+',',','-','.','/']
sep_lvl2=[":",";","<","=",">","?","@"]
sep_lvl3=['A','B','C','D','E','F','G','H','I','J','K','L'] 
mesquin=['M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

long_long_chaine = []
tmp_long_chaine  = []
long_chaine      = []
long_crypt       = []
testc            = []
testk            = []
int_chaine       = []
lvl2_key_miam    = []
tmp_crypt        = []


while(choice!='q'):
	# init_all()
	current_sep_lvl3    =  "A"
	current_sep_lvl2    =  ":"
	long_chaine[:]      = []
	long_crypt[:]       = []
	long_long_crypt     = []
	testc[:]            = []
	testk[:]            = []
	int_chaine[:]       = []
	lvl2_key_miam[:]    = []
	long_long_chaine[:] = []
	tmp_long_chaine[:]  = []
	tmp_crypt           = ()
	testkey             = ''
	raw_txt             = ''
	clean_txt           = ''
	longi               = 0
	longii              = 0
	res                 = ()

	if(userchoice):
		chaine = ''
		chaine=input("Veuillez entrer la chaine à crypter : ")
	if(len(chaine)>=seuil and len(chaine)<seuil_lvl2):
		long_chaine = split(chaine,seuil)
		longi+=1
	else: 
		if(len(chaine)>=seuil_lvl2):
			tmp_long_chaine = split(chaine,seuil_lvl2)
			for i in range(0,len(tmp_long_chaine)):
				long_long_chaine.append(split(tmp_long_chaine[i],seuil))
			longii+=1
	if(not longi and not longii):
		res=crypt_procedure(chaine,table2)
	else :
		if(longi):
			for i in range(0,len(long_chaine)):
				long_crypt.append(crypt_procedure(long_chaine[i],table2))
		if(longii):
			for i in range (0,len(long_long_chaine)):
				for j in range(0,len(long_long_chaine[i])):
					tmp_crypt = crypt_procedure(long_long_chaine[i][j],table2)
					long_long_crypt.append(tmp_crypt)
			# print(long_crypt[-1][0])
	if(not longi and not longii):
		testc = res[0]
		testk = res[1]
	else :
		if (longi):
			for i in range (0,len(long_crypt)):
				for j in range(0,len(long_crypt[i][0])):
					testc.append(str(long_crypt[i][0][j]))				
				for k in range(0,len(long_crypt[i][1])):
					testk.append(str(long_crypt[i][1][k]))				
				current_sep_lvl2=cyclik_ascii_lvl2(current_sep_lvl2)
				testc[-1]+=current_sep_lvl2
				testk[-1]+=current_sep_lvl2
		if(longii):
			for l in range (0,len(long_long_crypt)):
				# print(long_long_crypt[l])
				for j in range(0,len(long_long_crypt[l][0])):
					testc.append(str(long_long_crypt[l][0][j]))	
				for k in range(0,len(long_long_crypt[l][1])):		
					testk.append(str(long_long_crypt[l][1][k]))
				current_sep_lvl2=cyclik_ascii_lvl2(current_sep_lvl2)
				testc[-1]+=current_sep_lvl2
				testk[-1]+=current_sep_lvl2		
				# print("l = "+str(l)+" | len long[l] = "+str(len(long_long_crypt[l][0])))			
				if(len(long_long_crypt[l][0])<seuil):	
					current_sep_lvl3=cyclik_ascii_lvl3(current_sep_lvl3)
					testc[-1]+=current_sep_lvl3
					testk[-1]+=current_sep_lvl3	
		# print(testc)
		# print(testk)
	int_chaine=(ascii_to_int(chaine))
	for i in range(0,len(testk)):
		testkey+=str(testk[i])
	if(not longi and not longii):
		raw_txt = crypt_final(res,int_chaine,table2)
	else:
		raw_txt += crypt_final_long(testc,int_chaine,table2)
	raw_txt=mesqui(raw_txt,seuil)
	testkey=mesqui(testkey,seuil)
	print("---------------------------------")
	print("Chaine cryptée : \n")
	print(raw_txt)
	print("---------------------------------")
	print("Clé unique : \n")
	print(testkey)
	print("---------------------------------")
	raw_txt = slurp3(raw_txt)
	testkey = slurp3(testkey)
	if(not longi and not longii):
		clean_txt = decrypt_procedure(raw_txt,testk,table2)
	else:
		if(longi):
			lvl2_liste = []
			lvl2_key   = []
			lvl2_liste = slurp2(raw_txt)		
			lvl2_key   = slurp2(testkey)
			lvl2_key_miam = []
			# print(lvl2_liste)
			# print(lvl2_key)
			for i in range (0,len(lvl2_key)):
				lvl2_key_miam.append(miam(lvl2_key[i]))
			# print(lvl2_key_miam)
			for i in range (0,len(lvl2_liste)-1):
				clean_txt+= decrypt_procedure(lvl2_liste[i],lvl2_key_miam[i],table2)
		if(longii):
			lvl3_liste = []
			lvl3_key   = []
			lvl3_liste = slurp4(raw_txt)
			lvl3_key   = slurp4(testkey)
			lvl2_liste = []
			lvl2_key   = []
			lvl2_key_miam = []
			final_key  = []
			for i in range (0,len(lvl3_key)):
				lvl2_key.append(slurp2(lvl3_key[i]))
			for i in range (0,len(lvl3_liste)-1):
				lvl2_liste.append(slurp2(lvl3_liste[i]))
			for i in range(0,len(lvl2_key)-1):
				lvl2_key_miam[:] = []
				for j in range (0,len(lvl2_key[i])):
					lvl2_key_miam.append(miam(lvl2_key[i][j]))
					# print("miam")
					# print(lvl2_key_miam)
				del lvl2_key_miam[-1]
				final_key.append(lvl2_key_miam)
				# print("final")
				# print(final_key)
				# print("liste : "+str(len(lvl2_liste))+" | key "+str(len(final_key)))
				for k in range (0,len(lvl2_liste[i])-1):
					# print("lvl2[i][k] : ")
					# print(lvl2_liste[i][k])
					# print(final_key[0][k])
					clean_txt+=decrypt_procedure(lvl2_liste[i][k],final_key[0][k],table2)
					# print(str(k) + "/" + str(len(lvl2_liste[i])-2))
				# print(str(i)+" / "+str(len(lvl2_key)-1))

	print("Chaine décryptée : \n")
	print(clean_txt)
	choice=input("c)ontinuer ou q)uitter")
	if(choice!='q'):
		userchoice+=1
