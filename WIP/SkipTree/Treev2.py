import time
import sys

#Skiplist/Tree Hybrid Module
# Should be used as a tree structure or skiplist structure
# Structures are packaged once populated to high-speed data-structure

#%%

# Constructors #

# double way switch (usefull isn't it ?)
def switch(x,*arg):
	dic ={}
	for i in range (0,int(len(arg)-1)):
		dic[arg[i]]=arg[i+1]
	return dic.get(x,'default')

# compute a cell structure from arg infos
def compute_cell(value,root,*son):
	cell=[0]*2
	cell[0]=value
	cell[1]=root
	for i in range(0,len(son)):
		cell.append(son[i])
	return cell 

# make the root of the tree (standard empty list)
def make_root(tree,*cell):
	return []

# make a leaf on the tree from pos at the rigth place
def make_leaf(pos,tree,value,lvl_bool,right):
	try:
		if(isinstance(tree[-1],list) and right):
			if(lvl_bool):
				tree[-1]=(make_leaf(pos,tree[-1],value,lvl_bool,right))
			else:
				tree[-1]=make_leaf(pos,tree[-1],value,0,right)
		else:
			if(lvl_bool):
				tree.append([value])
			else:
				tree.append(value)
	except:
		tree.append(value)
	return tree 

# make a node in the structure from pos at the rigth place
def make_node(pos,tree,value,lvl_bool,right):
	if(isinstance(tree[-1],list) and right):
		if(lvl_bool):
			tree[-1]=(make_node(pos,tree[-1],value,lvl_bool,right))
		else:
			tree[-1]=make_node(pos,tree[-1],value,0,right)
	else:
		if(lvl_bool):
			tree.append([value])
		else:
			tree.append(value)
	# tree.append(0)
	return tree

# Compute a pos from width and depth (not fixed, please wait a bit)
def compute_pos(width,depth):
	pos=[]
	pos.append(width)
	pos.append(depth)
	return pos

# # To fix course in width
# def course_in_width_next(tree,current_pos):
# 	int_pos=current_pos[0]+current_pos[1]+1
# 	if(is_node(tree[int_pos])):
# 		return tree[int_pos+1]
# 	else: 
# 		return tree[int_pos][0]

# # To fix course in depth
# def course_in_depth_next(tree,current_pos):
# 	int_pos=current_pos[0]+current_pos[1]+1
# 	if(is_node(tree[int_pos])):
# 		i=0
# 		while(not is_node(tree[int_pos][i])):
# 			i+=1
# 			if(is_leaf(tree[int_pos][i])):
# 				return tree[int_pos][i]
# 				break
# 		return tree[int_pos][i]
# 	else:
# 		return tree[int_pos+1]

#%%

# Utils #

# Map each element the given function
def map(tree,funct):
	ind=0
	length=len(tree)
	while(ind!=length):
		try:
			if(isinstance(tree[ind],list) and (len(tree[ind])>1)):
				tree[ind]=map(tree[ind],funct)			
			elif(isinstance(tree[ind],int)):
				tree[ind]=funct(tree[ind])
			else: 
				tree[ind][0]=funct(tree[ind][0])
			ind+=1	
		except:
			break
	return tree

# print a list
def to_string(item):
	return str(item)

# print a cell infos
def print_cell(cell,pos):
	print("cell at width "+str(pos[0])+" | depth "+str(pos[1])+" | data : "+str(cell[0])+" | root : "+str(cell[1])+" | sons "+to_string(cell[2:]))


# Find an index of the given item in the structure
def find_index(item,liste,r,find):
	res=r[:]
	if(not find):
			if(item in liste):
				res.append(liste.index(item))
				find+=1
			else:
				for elem in liste:
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
	if(not find):
		try:
			return res[-1]
		except:
			return res
	else:
		if(isinstance(res,int)):
			return res
		else:
			return res[0]

# Go to the given indice(s) in the structure and return item
def go_to(skiplist,*indice):
	local_list=skiplist[:]
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
		if(not isinstance(liste[res],int)):
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
	if(isinstance(skiplist,list)):
		for i in range(0,len(skiplist)):
			if(not isinstance(skiplist[i],list)):
				res.append(skiplist[len(skiplist)-i-1])
			else:
				res.append(reverse(skiplist[len(skiplist)-i-1]))
		if(len(res)!=1):
			return res
		else:
			return res[0]
	else:
		return skiplist

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

#%%

# Base table constructor

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
		res.append(str(indice)+str(i))
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

def build_table():
	rec_level_h = [6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3]
	rec_level_m = [5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,1,1,1,1,1,1]
	rec_level_l = [4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,1,1,1,1,1,1,1,1]
	table = []
	bases = []
	tmp   = ()
	ok    = 0
	mini   =2
	mytime = 0
	fini = 0
	finalt = 0
	initt  =time.time()
	for i in range (mini,30):
		mytime=time.time()
		ind = 1
		ok  = 0
		bases.append(tablebase(i))
		table.append(recursive_build(bases[i-mini]))
		while(not ok):
			tmp=recursive_build_sup_lvl(bases[i-mini],table[i-mini],ind)
			table[i-mini]=tmp[0]
			ind+=1
			if(ind==rec_level_h[i-mini]):
				ok=1
	return table

#%%

# Hashmap computation #

# Compute the complement value in given context, ruled by maxi
def complement(value,maxi):
	return maxi-value

# Compute hashcode for 1 cell, determined by his index
def hashcode(Table,index,heigth):
	ind=0
	print(str(index))
	while (int(Table[heigth-2][ind])!=index):
		ind+=1
	return ind

# Get max 
def get_max(heigth):
	return (heigth*heigth)-1

# Align the given value with zero according with heigth
def zero_align(value,heigth):
	loc_len=heigth-1
	tmp=value
	if(tmp>1):
		loc_len=0
		while(tmp>1):
			loc_len+=1
			tmp/=10
	for i in range(0,loc_len):
		value*=10
	print("zero align " +str(value))
	return value

# Flat the given skiptree
def flat_tree(skiptree):
	res=[]
	for i in range(0,len(skiptree)):
		if(not isinstance(skiptree[i],list)):
			res.append((skiptree[i],0))
		else:
			res.extend(flat_tree(skiptree[i]))
	return res

# Compute hashcode for the given skiptree
def compute_hash(skiptree):
	res=[]
	skiptree=map(skiptree,to_string)
	heigth=get_heigth(skiptree)
	flatten=flat_tree(skiptree)
	maxi=get_max(heigth)

	for i in range(0,len(flatten)):
		local=[]
		local=find_index_recursivity_manage(flatten[i],skiptree,local,0)
		print("flatten [ "+str(i)+" ] = "+flatten[i])
		print("local = "+str(local))
		res.append(complement(hashcode(Table,zero_align(get_raw_value(local),heigth),heigth)),maxi)
	print(res)
	return res

# Package the "flex" skiptree to high-speed data-structure
def pack(flat_tree,hashc):
	if(len(flat_tree)==len(hashc)):
		for i in range(0,len(flat_tree)):
			flat_tree[i][1]=hashc[i]
	return flat_tree

#%%

# Tree manipulator #

# Get brothers as a list from the given element and packed tree
def bro(elem,packed_tree):
	res=[]
	for i in range(0,len(packed_tree)):
		if(elem==packed_tree[i][0]):
			hashc=packed_tree[i][1]
			break 
	for i in range(0,len(packed_tree)):
		if(abs(hashc-packed_tree[i][1])==1):
			res.append(packed_tree[i][0])
	return res

# Get the root (is exists) from the given element and packed tree
def root(elem,packed_tree):
	for i in range(0,len(packed_tree)):
		if(elem==packed_tree[i][0]):
			hashc=packed_tree[i][1]
			break 
	for i in range(0,len(packed_tree)):
		if(hashc==packed_tree[i][1]):
			return packed_tree[i][0]
	return 0

# TODO
def childs(elem,packed_tree):
	pass

# Get elements from the given packed_tree
def get_elem(packed_tree):
	res=[]
	for i in range(0,len(packed_tree)):
		res.append(packed_tree[i][0])
	return res

# Test the bro appartenance of a and b
def is_bro(a,b,packed_tree):
	brothers=bro(a,packed_tree)
	return (b in brothers)

# Test if b is the root of a
def is_root(a,b,packed_tree):
	return (root(a,packed_tree)==b)

# TODO
def draw(skiptree):
	pass

#%%

# Initialisation routine #

Table=build_table()
# print(Table[2])
# val=3112
# print(hashcode(Table,3112,4))
# print(zero_align(31,4))

# zero_align(elem,heigth)
# hashcode(Table,elem,heigth)
# maxi=get_max(heigth)
# complement(elem,maxi)

# print(complement(Table,3112,4))

cell_test = compute_cell(5,0,1,2,3)
pos_test  = compute_pos(0,0)
print_cell(cell_test,pos_test)
tree_test=[]
tree_test = make_root(tree_test,cell_test)
print(tree_test)
tree_test = make_leaf(compute_pos(0,1),tree_test,1,0,1)
print(tree_test)
tree_test = make_node(compute_pos(1,1),tree_test,2,0,1)
print(tree_test)
tree_test = make_leaf(compute_pos(0,2),tree_test,3,1,1) # left branch
print(tree_test)
tree_test = make_leaf(compute_pos(2,1),tree_test,4,0,0)
print(tree_test)
tree_test = make_node(compute_pos(3,1),tree_test,5,0,1)
print(tree_test)

tree_test = make_leaf(compute_pos(1,2),tree_test,6,1,1)
print(tree_test)
tree_test = make_leaf(compute_pos(2,2),tree_test,7,0,1)
print(tree_test)
tree_test = make_node(compute_pos(3,2),tree_test,8,0,1)
print(tree_test)

tree_test = make_leaf(compute_pos(0,3),tree_test,9,1,1)
print(tree_test)
tree_test = make_node(compute_pos(1,3),tree_test,10,0,1)
print(tree_test)
tree_test = make_leaf(compute_pos(2,3),tree_test,11,0,1)
print(tree_test)


# heigth=get_heigth(tree_test)
# print(heigth)

# test=flat_tree(tree_test)
# print(test)

test2=compute_hash(tree_test)
print(test2)



# Advanced Tree Representation
# ============================

# tree       list index      rel pos   index     proprieties

# r:::::::::list[0]          pos 0 0 = [0]       //init exception
# |                        
# +-n:::::::list[1]          pos 1 0 = [1]    
# | |
# | +-l:::::list[1][0]       pos 2 0 = [1,0]     z(n-1)+=y  or [f(x-1,y),0]
# |
# +-n:::::::list[2]          pos 1 1 = [2]       z(n-1)+=y
# | |
# | +-l:::::list[2][0]       pos 2 1 = [2,0]     [f(x-1,y),0]
# | 
# +-n:::::::list[3]          pos 1 2 = [3]       if y>x [z(n)++] (z0=zn)        
#   |
#   +-n:::::list[3][0]       pos 2 2 = [3,0]     [f(x-1,y),0]
#   | |
#   | +-l:::list[3][0][0]    pos 3 0 = [3,0,0]   z(n)+=y-(z(n-1)) / assert(x>2) and (y<x)
#   | |
#   | +-l:::list[3][0][1]    pos 3 1 = [3,0,1]   z(n)+=y-(z(n-1)) / assert(x>2) and (y<x)
#   | |
#   | +-l:::list[3][0][2]    pos 3 2 = [3,0,2]   z(n)+=y-(z(n-1)) / assert(x>2) and (y<x)
#   |
#   +-n:::::list[3][1]       pos 2 3 = [3,1]     if y>x [z(0),...,z(n)++] 
#     |
#     +-n:::list[3][1][0]    pos 3 3 = [3,1,0]   [f(x-1,y),0]
#     | |
#     | +-l:list[3][1][0][0] pos 4 0 = [3,1,0,0]  y<x && x>x-1
#     | |
#     | +-l:list[3][1][0][1] pos 4 1 = [3,1,0,1]  z(n)+=y-(z(n-1)) / assert(x>2) and (y<x)
#     |
#     +-n:::list[3][1][1]    pos 3 4 = [3,1,1]    if y>x [z(0),...,z(n)++] 
#       |
#       +-l:list[3][1][1][0] pos 4 2 = [3,1,1,0]  z(n)+=y-(z(n-1)) / assert(x>2) and (y<x)
#       | 
#       +-l:list[3][1][1][1] pos 4 3 = [3,1,1,1]  z(n)+=y-(z(n-1)) / assert(x>2) and (y<x)
#       |
#       +-l:list[3][1][1][2] pos 4 4 = [3,1,1,2]  z(n)+=y-(z(n-1)) / assert(x>2)

#                             f(x,y) = [z(1),...,z(n)]
#                                  x = nb_item_z_array

# Hashtables calculation
# ======================

#  b(prof+1)    b(prof)            
# conv b5       conv b4           conv b(prof_max)(0-cp)  complement 255=max(b(prof_max))
# 10=5  => [1]    = 1     n  +1   64                      191      même_root => +prof_max^(prof_max-prof)
# 11=6  => [2]    = 2     n  +1   128                     127      
# 12=7  => [3]    = 3     n  +1   192                     63    +-64

# 20=10 => [10]   = 4     l  +1   64                      191   +-16     
# 21=11 => [20]   = 8     l  +4   128                     127
# 22=12 => [30]   = 12    n  +4   192                     63
# 23=13 => [31]   = 13    n  +1   208                     47

# 30=15 => [300]  = 48    l  +35  192                     63    +-4
# 31=16 => [301]  = 49    l  +1   196                     59 
# 32=17 => [302]  = 50    l  +1   200                     55
# 33=18 => [310]  = 52    n  +2   208                     47
# 34=19 => [311]  = 53    n  +1   212                     43

# 40=20 => [3100] = 208   l  +155 208                     47     +-1  
# 41=21 => [3101] = 209   l  +1   209                     46     
# 42=22 => [3110] = 212   l  +3   212                     43       
# 43=23 => [3111] = 213   l  +1   213                     42
# 44=24 => [3112] = 214   l  +1   214                     41
#                                                         fils_g = même valeur
#                                                         frere  = prof_max^(prof_max-prof)

#            /\
#            ||
#            list_index_rec


# TODO list
# =========

# # test the child appartenance between two cell into the skiplist/tree structure
# def is_child(cell1,cell2,skiptree):

# Execution time compare
# ======================

# TpsRech(liste)=O(len(liste)log(len(liste)))
# TpsRech(SkipTree)=O(x.len(liste)log(x.len(liste)))   TpsRech(SkipTree)<<TpsRech(Tree)

# Blabla
# ======

# rafler toutes les cell à une profondeur donné i : Tree[_,...,_,xi] i in [0,nb_cell]  => xi (on "coupe" les cellules de profondeur i)
# 	                                                   \_____/
# 	                                                   	  i-1
# rafler les sous-arbres à une profondeur j | j<i, i : prof_max : Tree[_,...,xj,...xi] => xj (on "coupe" les branches à partir de j )                                                 	  

# substituer des sous-arbres à des feuilles (et inversement)
# + implementation des operateurs standards d arborescence avec tps d execution diminué

# Il s'agit d'un hybride skiplist/tree implementant une arborescence dans un ensemble de listes imbriquées.
# L interet principal de la structure tient dans le calcul des tables de hashage via la conversion de bases numeriques des indexs de liste mis bout à bout 
# (je sais, ca peut sembler un peut tordu mais ca marche), conversion particulierement rapide en raison de l absence de calculs complexes.

# Les valeurs de la tables de hashage sont obtenues par :
# 	° 1ere conversion dans la base (profondeur maximum + 1) il s agit des indices de listes mis bout a bout (aucun calculs, concatenation très rapide)
# 	° 2eme conversion inverse des valeurs obtenues 0-alignées à droite dans la base 10 (substitution de valeurs dans la base pré calculée, rapide)
# 	° complement à la valeur maximum de la base (profondeur maximum) au nombre maximum d indices (additions/ soustractions, rapide)

# Une fois calculées la comparaison des valeurs de la table de hachage revelent les liens root et les liens children.
# Bref tout ce dont on a besoin en un temps d execution record (j espere).

# Le but du "jeu" etant de prevoir une structure rapide (skiplist) qui a la forme d un arbre et utilisable en tant qu arbre capable
# d "encaisser" les grande arborescence (à la manière des calculs de base)
# Donc, il faut miser sur une recursivité EXEMPLAIRE de construction, le minimum de duplicata memoire temporaire pour les traitements.
# J espere pouvoir arriver à encaisser des arborescences de millions/milliards d elements (autant voir gros directement quitte à tailler dans le lard
# pour les plus petites structures)
# Tout simplement parce qu adapter une structure de petite taille a des grandes quantite de donnees c est un milliard de fois plus dur que l inverse

# J ai deja bien avancé, la recuperation des indexs et conversion numerique presque-OK
# Les tables de bases sont deja codées, reste à implementer les complements/Hashage par base, et les fonctions utilitaires pour recuperer les
# fils,les freres, les chaines/chemins, etc, etc

# La fonction hashbase calculera la valeur numerique du complemet de l index converti dans la base de profondeur de l arbre, ces valeurs
# revelent par la suite toute la structure de l arobrescence, on en deduira les informations de noeuds automatiquement.
# Resultat, on peut remplir l arbre "a la sauvage" (par lecture de fichier par exemple) sur une grande profondeur et le remanier
# (taille des branches, des feuilles, algorithmes de parcours divers et variés, calculs des + court chemin, minimax, etc, etc)

# Bref un outil qui pourrait s averer plus que pratique par la suite, une petite interface graphique elementaire pour manier plus rapidement
# l arborescence, implementation du plus court chemin de Dijkstra, facilitée de parallelisation sur les listes 

# Pour ce qui est des quelques "miss" du langage python (switch, ...), ca reste tres rapidement codé.
# J imagine par la suite generer les code C/C++ a partir des algos python, histoire d etre tranquille pour de bon