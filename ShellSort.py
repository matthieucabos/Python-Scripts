import random as r

__author__="CABOS Matthieu"
__date__=30_06_2020

# A script for sorting list using the BEST ALGORITHM EVER FOUND

def gen(size,maxi=100):
	res=[]
	for i in range(size):
		res.append(r.randint(-maxi,maxi))
	return res

def shellSort(liste):
	for i in range(len(liste)):
		for j in range(i,len(liste)):
			tmp=liste[j]
			k=j
			while(k>=i and liste[k-i]>tmp):
				liste[k]=liste[k-i]
				k-=i
			liste[k]=tmp
	return liste
