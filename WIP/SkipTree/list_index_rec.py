import time
import sys

# Find an index of the given item in the structure
def find_index(item,liste,r,find):
	res=r[:]
	if(not find):
			if(item in liste):
				res.append(liste.index(item))
				find+=1
			else:
				for elem in liste:
					# print("current elem = "+ str(elem))
					# print(res)
					if(isinstance(elem,list) and not find):
						if(item in elem):
							res.append(liste.index(elem))
							res.append(find_index(item,elem,res,find))
							break
						else:
							res.append(liste.index(elem))
							res.append(find_index(item,elem,res,find))
							break
					if(elem==liste[-1] and not find):
						res.pop()
					# print("########################################")							
	if(not find):
		return res[-1]
	else:
		return res

# Go to the given indice(s) in the structure and return item
def go_to(skiplist,*indice):
	local_list=skiplist[:]
	# print(indice)
	if(isinstance(indice,tuple) and isinstance(indice[0],list)):
		indice=indice[0]
	for i in indice :
		local_list=local_list[i]
	return local_list

# Recursivity management to treat big structures (to fix : the "switch" between the first step and the recursive call)
def find_index_recursivity_manage(item,liste,r,find):
	res=[]

	# Step 0
	res=find_index(item,liste,r,find)
	verif=go_to(liste,res)
	try:
		tmp=res+1
	except:
		pass

	# Recursive automat
	while(verif!=item):
		try: 
			verif=go_to(liste,res)
		except:
			break
		res=find_index(item,liste[res+1:],[],find)
	try:
		res[0]=res[0]+tmp
	except:
		pass
	return res

# Get the raw value of index(es) to compute the hashmap
def get_raw_value(index_list):
	res=index_list[0]*10**len(index_list)
	for i in range(1,len(index_list)):
		res+=index_list[i]*10**(len(index_list)-i)
	return int(res/10)

def reverse(skiplist):
	res=[]
	for i in range(0,len(skiplist)):
		if(not isinstance(skiplist[i],list)):
			res.append(skiplist[len(skiplist)-i-1])
		else:
			res.append(reverse(skiplist[len(skiplist)-i-1]))
	if(len(res)!=1):
		return res
	else:
		return res[0]

def get_heigth(skiplist):
	heigth=1
	heigth2=1
	tmp=skiplist[:]
	tmp2=reverse(skiplist)
	ind=0
	ind2=0

	# from start
	while(not isinstance(tmp,int)):
		try:
			if(isinstance(tmp[ind],list)):
				tmp=tmp[ind]
				heigth+=1
				ind=0
			else:
				ind+=1
		except:
			break

	#from end
	while(not isinstance(tmp2,int)):
		try:
			if(isinstance(tmp2[ind2],list)):
				tmp2=tmp2[ind2]
				heigth2+=1
				ind2=0
			else:
				ind2+=1
		except:
			break

	# Get max heigth
	return (heigth if (heigth>heigth2) else heigth2)


test=["a","b","c",["d","e",["f",["g","h","i"]]],"c2",[["d2","d21"],"e2","f2"]]
res=[]

res=find_index_recursivity_manage("a",test,res,0)
print("recursive find_index test : ")
print(res)
value=get_raw_value(res)
print("raw int conversion : ")
print(value)

# test_goto=0
# test_goto=go_to(test,3,2,1,0)
# print(test_goto)
# print("heigth = ")
# print(get_heigth(test))