import random as r
import matplotlib.pyplot as mpl

# A module of analysis of pseudo-random distribution 
# https://ram-0000.developpez.com/tutoriels/cryptographie/images/GenerateurAleatoirePhysique.jpg
# ;-/ 

def rand_list(mode):
	#Generate a pseudo-random distribution
	res=[]
	for i in range(0,100):
		if(mode):
			try:
				res.append((r.randint(0,100)*r.randint(0,100)+r.randint(0,100)) % r.randint(0,100))
			except:
				pass
		else:
			res.append(r.randint(0,100))
	return res

def hist_cumu(hist):
	#Compute the cumulated histogram from the given histogram
	for i in range(1,100):
		hist[i]+=hist[i-1]
	return hist

def analysis(liste):
	#Compute the histogram of the given list values
	hist=[0]*100
	hist_cumul=[0]*100
	for item in liste:
		hist[item]+=1
	hist_cumul=hist_cumu(hist)
	return(hist,hist_cumul)

def suppr_double(liste):
	#Suppr duplicated values from the list
	for i in range(0,len(liste)-1):
		if(liste[i] in liste[i:]):
			del liste[i]
	return liste

def ratio_analysis(liste):
	#Analysis of the ratio between two near generated values
	res=[]
	res2=[]
	for i in range(1,len(liste)):
		try:
			res.append(liste[i]/liste[i-1])
			res2.append(liste[i]%liste[i-1])
		except:
			pass
	return(res,res2)

def substract_analysis(liste):
	#Anlysis of the difference of two near generated values
	res=[]
	for i in range(1,len(liste)):
		res.append(liste[i]-liste[i-1])
	return res

def xtract_sub_sequence(liste,a,b):
	#xtract the subsequence [a,b] in the given list
	tmp=liste[:-b]
	return liste[:a]

def compare(seq1,seq2):
	#Compare two given sub-sequences
	nb_item=len(seq1)
	prob=0
	if(len(seq1)==len(seq2)):
		for i in range(0,len(seq1)):
			if(seq1[i]==seq2[i]):
				prob+=1
	return (prob/nb_item)

def find_prob_sequence(seq):
	#find probability of similitude sequence in the given sequences
	prob=[]
	for i in range(0,len(seq)-1):
		prob.append(compare(seq[i],seq[i+1]))
	return prob

def evaluate_results(prob_list,threshold):
	#Evaluate the probabilities values fixed by the "interesting" threshold value
	index_list=[]
	if not(threshold>1 or threshold<0):
		for i in range(0,len(prob_list)):
			if prob_list[i]>threshold:
				index_list.append(i)
	return index_list

def print_analysis(liste,label,mode):
	#Print beautiful curves to illustrate differents kind of analysis (and profitable my work time of course)
	x_axis=range(0,len(liste))
	mpl.figure()
	if(mode):
		mpl.plot(x_axis,liste,label=label)
	else:
		mpl.hist(liste,x_axis,label=label)
	mpl.show()

def conclude():
	print("Pseudo random generator algorithms are not so random. Maybe a fantastic hardware random number generator could help you (at least 250e for a great and solid module)")

def random_with_view_list(a,b):
	#Vlc dedicace (random music playlist for example)
	res=[]
	length=b-a
	while(len(res)!=length)
		do:
			tmp=randint(a,b)
		while(tmp in res)
		res.append(tmp)
	return res

hist=0
curve=1

print("Rand generator test")
liste=[]
liste=rand_list(1)
print(liste)
print("analysis_test")
test=analysis(liste)
# test_without_duplic=suppr_double(liste)
# test2=analysis(test_without_duplic)
print_analysis(test,"analysis simple rand generated",hist)
print_analysis(test,"analysis simple rand generated without duplicated values",hist)
print("ratio analysis test")
test=[]
test=ratio_analysis(liste)
print_analysis(test)
print("substract test")
test=[]
test=substract_analysis(liste)
print_analysis(test,curve)
print("xtract sub sequence test")
xtracts=[]
for i in [0,10,20,30,40,50,60,70,80,90]:
	xtracts.append(xtract_sub_sequence(liste,i,i+10))
prob=[]
prob=find_prob_sequence(xtracts)
print_analysis(prob,curve)