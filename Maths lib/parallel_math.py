from mpi4py import MPI
import sys
from complex_lib.src import *
from matrix_lib.src import *
from vectorial_lib.src import *

#####################################################
# Parallel computing  sequencer  with shared memory #
#####################################################
#Here is my fast computing engine project including #
#	* linear 2D and 3D vectorial algebra operators  #
#	* ND matrix algebra operators                   #
#	* complex algebra operators                     #
#Should be used as a ND graphical engine, physical  #
#modelisation, mathematical use, low-level integrated#
#computing system                                   #
#####################################################
#Libraries are encoded with cython as .pyd extension#
#for faster computing.                              #
#Here is a parallel sequencer for multi-core CPU    #
#support.                                           #
#####################################################

# Conversion tools

class sequence:
	def __init__(self,**args):
		self.seq=[]
		for i in range(0,len(args)):
			self.seq.append(args[i])

	#TODO
	def execute(self,core_number=8):
		while(self.seq!=none):
			pass
	#TODO
	def edit(self)



def sqrt(X):
	# this one is easy
	x=0.01
	for i in range(0,100):
		x=(x+X/x)/2
	return x

def cos(X):
	# Still breaking my head against the wall
	pass

def rank(**cmd):
	# Local interpreter
	for i in range(0,len(cmd)):
		exec(cmd[i])



# if(len(argv)!=8):
# 	print("Use : input = 8 thd cmd as string")
for i in range(0,len(argv)):
	codetthd.append(argv[i])
rank=MPI.COMM_WORLD.Get_rank()
switch(rank,
	1,rank(codethd[1]),
	2,rank(codethd[2]),
	3,rank(codethd[3]),
	4,rank(codethd[4]),
	5,rank(codethd[5]),
	6,rank(codethd[6]),
	7,rank(codethd[7]),
	8,rank(codethd[8]))

