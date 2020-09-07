import sys
import time
from mouchar import *
#Author : CABOS Matthieu
#Date : 06/2018

def tablebase(base):
	res = []
	letter = 'a'
	# //
	for i in range(0,base):
		if(i<10 or (i<=10 and base <=10)):
			res.append(str(i))
		if(i>=10 and base >10):
			res.append(letter)
			letter=chr(ord(letter)+1)
	return res

def recursive_build(table_base):
	res = []
	# //*2
	for i in table_base:
		for j in table_base:
			res.append(i+j)

	return res

def recursive_build_sup_lvl_safe_mode(current,indice):
	res = []
	#//
	for i in current:
		# try:
		res.append(str(indice)+str(i))
		# except:
			# print("break in method : recursive_build_sup_lvl_safe_mode")
			# break
	return res

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

# base  = int(sys.argv[1])
# test1 = []
# test2 = []
# tmp = ()
# print("test tablebase : ")
# test1=tablebase(base)
# print(test1)
# print("test : done\n")
# print("test recursive_buid : ")
# test2=recursive_build(test1)
# print(test2)
# print("test : done\n")
# print("test recursive_build_sup_lvl_safe_mode : ")
# test2=recursive_build_sup_lvl_safe_mode(test1,'e')
# print(test2)
# print("test : done\n")
# print("test recursive_build_sup_lvl 1 : ")
# test1=tablebase(base)
# tmp=recursive_build_sup_lvl(test1,test1,1)
# test2=tmp[0]
# print(len(test2))
# print("test recursive_build_sup_lvl full range : ")
# ind = 2
# while(1):
# 	tmp=recursive_build_sup_lvl(test1,test2,ind)
# 	test2=tmp[0]
# 	ind+=1
# 	print("recursive level "+str(ind))
# 	if(tmp[1]==1):
# 		break
# print("test : done \n")
# print(len(test2))
# print(test2[0])
# print(test2[-1])


print("test full tables recursive_build_sup_lvl full range : ")
print("test full computer numeric remap : ")
rec_level_h = [6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4]
rec_level_m = [5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3]
rec_level_l = [4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
table = []
bases = []
tmp   = ()
ok    = 0
mini   =11
# stop   = int(sys.argv[2])
mytime = 0
fini = 0
finalt = 0
initt  =time.time()
for i in range (mini,36):
	mytime=time.time()
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
		# ok=tmp[1]
		ind+=1
		print("recursive level "+str(ind))
		if(ind==rec_level_l[i-mini]):
			ok=1
		# time.sleep(7)
		# if(ind==stop):
		# 	ok=1
	fini=time.time()-mytime
	print("i-mini = "+str(i-mini)+" | Constructor base "+str(i)+" done in "+str(fini)+"s. length = "+str(len(table[i-mini]))+" | last value = "+str(table[i-mini][-1]))
finalt=time.time()-initt
print("Calulation time : "+str(finalt))
