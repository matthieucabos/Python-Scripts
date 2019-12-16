def isalpha(char):
	return (char in ['1','2','3','4','5','6','7','8','9'])

def switch(x,*arg):
	dic ={}
	for i in range (0,int(len(arg)-1)):
		dic[arg[i]]=arg[i+1]
	return dic.get(x,'default')

def reverse(liste):
	res=[]
	for i in range(0,len(liste)):
		res.append(liste[len(liste)-i-1])
	return res

def abs(x):
	if(x<0):
		return -x 
	else:
		return x

def swap(a,b):
	# no ram swap
	b+=a
	a=b-a 
	b=b-a 
	return(a,b)

def string2int(str):
	tmp=0
	for i in range(0,len(str)):
		tmp+=int(str[i])
		tmp*=10
	return tmp

def convert(val,base):
	res=''
	sgn= 1 if val<0 else 0
	if(sgn):
		val=abs(val)
		res='-'
	while(val>0):
		res=res+str(val%base)
		val/=base
	return res

def int2list(val):
	res=[]
	sgn= 1 if val<0 else 0
	if(sgn):
		val=abs(val)
		res.append('-')
	while(val>0):
		res.append(str(val%base))
		val/=base
	return res

def complement_at(x,base=2):
	return (base-1-x)

def complement(x,base=2):
	splitted=int2list(x,10)
	final_res=0
	for i in range(0,len(splitted)):
		splitted[i]=complement_at(splitted[i],base)
		final_res*=10
		final_res+=splitted[i]
	return final_res

def sort(List,threshold=10000):
	if(len(List)<threshold):
		# tri1
	else:
		# tri2

def list2int(list):

def read_file_in_list(path):

def write_list_in_file(path):
