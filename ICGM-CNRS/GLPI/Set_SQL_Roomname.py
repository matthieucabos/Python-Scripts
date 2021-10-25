import os
import pyexcel as p

__author__="CABOS Matthieu"
__date__=25/10/2021

def gen(size,maxi=100):
	# Generator for relative size array
	res=[]
	for i in range(size):
		ok=False
		while not ok:
			tmp=r.randint(65,122)
			if (tmp >= 65 and tmp <= 90) or (tmp >= 97 and tmp <=122):
				ok=True
				res.append(chr(tmp))
				tmp=0
	return res

def complete_permutation(permutation):
	# Completing secondaries permutations since 1.1
	rez=[]
	for item in permutation:  
		rez.append(item)
		k=item[1]
		l=item[1]+1
		while l<=item[0]:
			rez.append((k,l,0))
			k+=1
			l+=1
	return rez

def shellSort(liste):
	# Shell sort algorithm with permutation memory as list
	permutation=[]
	count=0
	for i in range(len(liste)):
		count=0
		for j in range(i,len(liste)):
			tmp=liste[j]
			k=j
			while(k>=i and liste[k-i]>tmp):
				liste[k]=liste[k-i]
				k-=i
				count+=1
			liste[k]=tmp
			if(j!=k):
				permutation.append((j,k,1))
	final_perm=[]
	# 1.1
	final_perm=complete_permutation(permutation)
	return (liste,final_perm)

def permutation(liste,permutation):
	# Realize the signed permutation iven as second return of shellSort function
	final_liste=liste[:]
	for i in permutation:
		if (i[2]==1):
			liste=final_liste[:]
		final_liste[i[1]]=liste[i[0]]
	return final_liste

def Del_duplicate(records):
	res=[]
	for i in range(len(records)):
		if not (records[i] in records[i+1:]):
			res.append(records[i])
	return res


file_name='../Switchs.ods'
dest_file_name="Switchs2.ods"
column_id=0

# Getting ods file as array
records = p.get_array(file_name=file_name)
id_list=[]

for record in records:
	id_list.append(record[column_id])       # Getting Plug numbers (as example)

sorting=shellSort(id_list)                  # Sorting Id List
out_array=permutation(records,sorting[1])   # Apply permutation to full array

file_name='Switchs2.ods'
etage=''
done=[]
values=[]

records=out_array
loc_id=0
for rec in records:
	if (not rec[0] in done) and (not rec[0] == '') and (not rec[0] == 'Bureau') and (not rec[0] == 'CINES'):
		# Sorting by Floor
		if ('N1' in rec[0]):
			etage='Étage 1'
			loc_id=2
		elif ('N2' in rec[0]):
			etage='Étage 2'
			loc_id=3
		elif ('N3' in rec[0]):
			etage='Étage 3'
			loc_id=4
		elif ('N4' in rec[0]):
			etage='Étage 4'
			loc_id=5
		elif ('RJPA' in rec[0]) or ('RJLG' in rec[0]):
			etage='PAC RDJ'
			loc_id=6
		elif ('SSPA' in rec[0]):
			etage='PAC SS'
			loc_id=7
		elif ('RJEP' in rec[0]):
			etage=' Exp Prot RDJ'
			loc_id=8
		elif ('SSEP' in rec[0]):
			etage='Exp Prot SS'
			loc_id=9
		# Updating values fields
		Room="\""
		Room=Room+str(rec[0])+"\""
		values.append('values('+str(Room)+','+str(loc_id)+', "Batiment Balard > '+str(etage)+' > '+str(rec[0])+'", 3,"{"1":1,"'+str(loc_id)+'":'+str(loc_id)+'}",Now(),Now());')
	done.append(rec[0])

# SQL Formatting
sql_pre='insert into glpi_locations (name,locations_id,completename , level,ancestors_cache,date_mod,date_creation) '
Content=''
for item in values:
	Content= Content + sql_pre + item + '\n'

# Writing SQL into file my_glpi.sql
f=open('my_glpi.sql','w')
f.write(Content)
f.close()
quit()