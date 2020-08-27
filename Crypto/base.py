import sys 

def reverse(s):
	str= ""
	for i in s:
		str=i+str
	return str

def table(base,debut,fin,inc):
	represent=""
	letter='a'
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
			while(current/base!=0):
				if(base<10):
					represent+=str(current%base)
				else:
					if(current%base<10):
						represent+=str(current%base)
					else:
						represent+=letter
						letter=chr(ord(letter)+1)
						if(current%base==base-1):
							letter='a'
				current=int(current/base)
		represent+="\n"
	represent=reverse(represent)
	print(represent[::-1])

# if(len(sys.argv)!=3):
# 	print("Usage : Basemin Basemax")
Basemin = 2
Basemax = 36
if(Basemin<2 or Basemax>36):
	print("Affichage impossible veuillez selectionner une plage de valeure contenue dans [2,36]")



for i in range(Basemin,Basemax):
	print("\n")
	table(i,0,200,1)
