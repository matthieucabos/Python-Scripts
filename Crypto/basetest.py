import sys 
from mouchar import *
#Author : CABOS Matthieu
#Date : 01/2018
def reverse(s):
	str= ""
	for i in s:
		str=i+str
	return str

def table(base,debut,fin,inc):
	represent=''
	letter='a'
	powIndex=0
	count=0
	print("Base"+str(base))
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
	print(represent)

represent=''
if(len(sys.argv)!=4):
	print("Usage : Basemin Basemax Range")
	exit(0)
Basemin = int(sys.argv[1])
Basemax = int(sys.argv[2])
Range   = int(sys.argv[3])
if(Basemin<2 or Basemax>36):
	print("Affichage impossible veuillez selectionner une plage de valeure contenue dans [2,36]")
	exit(0)


for i in range(Basemin,Basemax):
	print("\n")
	table(i,0,Range,1)
		#represent.split(" \n ")


