import numpy as np

def get():
	return input("text (<60):\n")

def num(chaine):
	res=[ord(chaine[0])]
	chaine=chaine[1:]
	i=0
	for c in chaine:
		res.append(res[i]+ord(c))
		i+=1
	return res

def fibo(n,mode):
	# Mode define the numeric suit to use as a "big integer reducter" via dividing each term of the polynôme with a term of the suit.
	res=[1,1]
	for i in range(0,n-2):
		if mode == 0:
			res.append(res[i]+res[i+1])
		elif mode == 1 :
			res.append(res[i]+2*res[i+1]/3)
	return res

def crypt(chaine):
	res=num(chaine)
	tmp=fibo(len(res))
	for i in range(0,len(res)):
		res[i]=res[i]/tmp[i]
	return res

def decrypt(chaine,mode):
	# Mode should be implement here to respond to the different possible ways from used numeric suit...
	res=chaine
	tmp=fibo(len(chaine))
	for i in range(len(chaine)):
		res[i]=int(res[i]*tmp[i])
	z=[int(res[0])]
	for i in range(1,len(res)):
		z.append(res[i]-res[i-1])
	for i in range(len(z)):
		z[i]=chr(z[i])
	Str=""
	for y in z:
		Str+=y
	return Str

def chiffrer(liste):
	l=[]
	for item in liste:
		l.append(str(item).encode('utf32'))
	return l 

def dechiffrer(liste):
	l=[]
	for item in liste:
		l.append(float(item.decode('utf32')))
	return l