from base_opt import *
from cmatrix import *
from mouchar import *
class StrMatrix(object):
	def __init__(self,sr,sc,init_value='a'):		
		self.size_raw=sr
		self.size_column=sc
		self.data=[init_value]*sr*sc

	def ij_2_ind(self,i,j,size_raw):    
		return j*size_raw+i

	def ind_2_ij(self,ind,size_raw):
		return (int(ind/size_raw),ind%size_raw)

	def __setitem__(self,key,value):
		self.data[self.ij_2_ind(key[0],key[1],self.size_raw)]=value 

	def __getitem__(self,key):
		return self.data[self.ij_2_ind(key[0],key[1],self.size_raw)]

def inv_permut(permut):
	res=[]
	for i in range(len(permut)):
		res.append(permut[permut[i]])
	return res

def cyclic_permut(permut,size):
	res=permut[:]
	ind=0
	for i in range(size):
		if((i+1)>len(permut)):
			res.append(permut[i % len(permut)]+ind*len(permut))
			print(permut[i % len(permut)])
		if((i+1) % len(permut)==0 and i!=0):
			ind+=1
	return res

def convert_matrix(mat,base):
	res=StrMatrix(mat.size_r(),mat.size_c())
	for i in range(mat.size_r()):
		for j in range(mat.size_c()):
			res[i,j]=table[base][mat[i,j]]
	return res

def create_table():
	rec_level_h = [6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4]
	rec_level_m = [5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3]
	rec_level_l = [4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
	table = []
	bases = []
	tmp   = ()
	ok    = 0
	mini   =11
	mytime = 0
	fini = 0
	finalt = 0
	initt  =time.time()
	for i in range (mini,37):
		mytime=time.time()
		ind = 1
		ok  = 0
		bases.append(tablebase(i))
		table.append(recursive_build(bases[i-mini]))
		while(not ok):
			tmp=recursive_build_sup_lvl(bases[i-mini],table[i-mini],ind)
			table[i-mini]=tmp[0]
			ind+=1
			if(ind==rec_level_l[i-mini]):
				ok=1
	return table
