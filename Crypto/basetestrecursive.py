import sys 
#Author : CABOS Matthieu
#Date : 02/2018
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
		del table[powindex*10*base]
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

represent=''
table2 = []
dic = {}
main_dic={}
choice = ' '

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


# for i in range (0,len(table2)):
# 	dic=local_table_dico(table2,i+2,len(table2[i]))
# 	main_dic["Base" + str(i+2)]=dic

while(choice!='q'):
	localbase=int(input("Please enter base indice : "))
	if(localbase>=37):
		print("Work in progress, thanks 4 ur patience")
		exit(0)
	localbase-=2
	local_range=limit_range(Range,localbase+2)
	print(local_range)
	for i in range(0,local_range):
		print(str(i) + " | "+str(table2[localbase][i]))
	print("3 x 8 = " + str(table2[localbase][3*8]))
	print("test recursive build : done")
	table3=table2[localbase][:]
	table3=rec_table_construct_lvl1(table3,localbase+2,1,0)
	# print("-----------------------------------------------")
	# print(table3)
	table3=rec_table_construct_final(table3,localbase+2,1)
	table3=rec_table_construct_final(table3,localbase+2,2)
	# print("-----------------------------------------------")
	# print(table3)
	# for i in range(0,len(table3)):
	# 	print(str(i) + " | "+str(table3[i]))
	try:
		print(table3[1679614])
		choice='q'
	except: choice=input("c)ontinue or q)uit") 
	

# print("test dico : ")
#Chrono on
# testbase=int(input("Please enter base : "))
# testvalue=int(input("Please enter number"))
# tmpvalue=main_dic["Base"+str(testbase)][testvalue]
# print(str(testvalue) + "b" + str(testbase) + " = " + str(tmpvalue))
#Chrono off

# while range>=10*base => split/concat/range:10

