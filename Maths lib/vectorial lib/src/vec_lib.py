import numpy as np
import time as t

def no_way():
	"""
		A function saying the divisions are the first ennemy of a CPU.
	"""
	print("no more division on computers !!! please take your pen.")
	print("This is a message from the CTSL (CPU Time Savers League) .")

class Point():
	"""
		The point object to compute 2 dimensions geometric interaction.

		=============== ==========
		**Attributes**   **Type**
		*x*               float
		*y*               float
		=============== ==========
	"""

	def __init__(self,x=0.0,y=0.0):
		self.x=x
		self.y=y

		# getters and setters
	def set_x(self,x):
		self.x=x
	def set_y(self,y):
		self.y=y
	def get_x(self):
		return self.x
	def get_y(self):
		return self.y

		# basic operators redefinition
	def op(self,B,op):
		if op=='+':
			return Point(self.get_x()+B.get_x(),self.get_y()+B.get_y())
		elif op=='-':
			return Point(self.get_x()-B.get_x(),self.get_y()-B.get_y())

	def __add__(self,p):
		return self.op(p,'+')

	def __sub__(self,p):
		return self.op(p,'-')

		# Utility

	def print_screen(self):
		print(" ( "+str(self.get_x())+" , "+str(self.get_y())+" ) ")

	def copy(self):
		return Point(self.get_x(),self.get_y())


class Vect():
	"""
		The vector object to compute 2 dimensions vectorial operations.
		=============== ==========
		**Attributes**   **Type**
		*x*               Point
		*y*               Point
		=============== ==========
	"""

	def __init__(self,x0,x1,y0,y1,dim=2):
		self.x=Point(x0,x1)
		self.y=Point(y0,y1)
		self.dim=dim

		# getters and setters
	def set_x(self,x):
		self.x=x
	def set_y(self,y):
		self.y=y
	def get_x(self):
		return self.x
	def get_y(self):
		return self.y
		

		# basic operators redefinition
	def op(self,B,op):
		if op=='+':
			return Vect(self.get_x().get_x()+B.get_x().get_x(),self.get_x().get_y()+B.get_x().get_y(),self.get_y().get_x()+B.get_y().get_x(),self.get_y().get_y()+B.get_y().get_y())
		elif op=='-':
			return Vect(self.get_x().get_x()-B.get_x().get_x(),self.get_x().get_y()-B.get_x().get_y(),self.get_y().get_x()-B.get_y().get_x(),self.get_y().get_y()-B.get_y().get_y())
		elif op=='*':
			return Vect(B*self.get_x().get_x(),B*self.get_x().get_y(),B*self.get_y().get_x(),B*self.get_y().get_y())

	def __add__(self,vec):
		return self.op(vec,'+')

	def __sub__(self,vec):
		return self.op(vec,'-')

	def __mul__(self,coef):
		return self.op(coef,'*')

		#Specific operators definition

	def vectorize(self):
		#vectorize self vector
		return Vect(0,0,self.get_y().get_x()-self.get_x().get_x(),self.get_y().get_y()-self.get_x().get_y())

	def cross(self,vec):
		#cross product self and vec
		v1=self.vectorize()
		v2=vec.vectorize()
		return v1.get_y().get_x()*v2.get_y().get_y()-v1.get_y().get_y()*v2.get_y().get_x()

	def dot(self,vec):
		#dot product self and vec
		v1=self.vectorize()
		v2=vec.vectorize()
		return v1.get_y().get_x()*v2.get_y().get_x()+v1.get_y().get_y()*v2.get_y().get_y()

	def norm(self):
		#get the norm of self vector
		return np.sqrt(self.dot(self))

	def normalize(self):
		#normalize self vector
		vec=self.vectorize()
		return Vect(0,0,-vec.get_y().get_y(),vec.get_y().get_x())

	def translate_to(self,point=Point(0,0)):
		#translate self vector to the given point
		return self+Vect(self.get_x().get_x(),self.get_x().get_y(),point.get_x(),point.get_y())

	def unit_vector(self):
		#get unit vector from self
		return self*(1/self.norm())

	def normalize_not_vectorized(self):
		#normalize self vector WITHOUT vectorizing (in fact vectorized and "unvectorized")
		vec=self.vectorize()
		return Vect(0,0,-vec.get_y().get_y(),vec.get_y().get_x()).translate_to(self.get_x())

		#Utility

	def print_screen(self):
		print(" ( "+str(self.get_y().get_x()-self.get_x().get_x())+" , "+str(self.get_y().get_y()-self.get_x().get_y())+" ) ")

	def copy(self):
		return Vect(self.get_x().get_x(),self.get_x().get_y(),self.get_y().get_x(),self.get_y().get_y())

class Vector_field():
	"""
		=============== ============
		**Attributes**   **type**
		*vec*            Vect list
		*pts*            Point list
		*size*           int
		=============== ============
	"""
	vec=[]
	pts=[]
	size=0

	def __init__(self,vec,pts):
		if(len(vec)==len(pts)):
			for item in vec:
				self.vec.append(item)
			for item in pts:
				self.pts.append(item)
				self.size+=1

	def get_vec(self):
		return self.vec
	def get_pts(self):
		return self.pts
	def get_size(self):
		return self.size

	def op(self,field,op):
		if op=='+':
			if(self.get_size()==field.get_size()):
				vec=[]
				for item,item2 in self.get_vec(),field.get_vec():
					vec.append(item+item2)
				return Vector_field(vec,self.pts)
		elif op=='-':
			if(self.get_size()==field.get_size()):
				vec=[]
				for item,item2 in self.get_vec(),field.get_vec():
					vec.append(item-item2)
				return Vector_field(vec,self.pts)
		elif op=='*':
			if(isinstance(field,int) or isinstance(field,float)):
				vec=[]
				for item in self.get_vec():
					vec.append(field*item)
				return Vector_field(vec,self.pts)
		elif op=='/':
			no_way()

	def __add__(self,vec_f):
		return self.op(vec_f,'+')
	def __sub__(self,vec_f):
		return self.op(vec_f,'-')
	def __mul__(self,coef):
		return self.op(coef,'*')

	# def mean(self):

	# def interpolation(self):

	# def extend_field(self):

	def print_screen(self):
		ind=0
		for item in self.get_vec():
			print("element ["+str(ind)+"] : ")
			item.print_screen()
			self.pts[ind].print_screen()
			ind+=1

start=t.time()
list_vec=[]
list_dot=[]
for i in range(0,99999):
	list_vec.append(Vect(i,2*i,3*i,4*i))
	if(len(list_vec)>0):
		list_dot.append(list_vec[i-1].dot(list_vec[i]))
stop=t.time()
print("99999 dot product computed in "+str(float(stop-start))+"s.")


# test=Point(0,2)
# test2=Point(2,4)
# vect=Vect(0,2,2,4)
# vect2=Vect(1,3,6,7)
# vect.print_screen()
# vect2.print_screen()
# print("add test : ")
# add=vect+vect2
# add.print_screen()
# print("sub test:")
# sub=vect2-vect
# sub.print_screen()
# print("mul test:")
# mul=vect*10
# mul.print_screen()
# print("vectorize test:")
# vect2.vectorize()
# vect2.print_screen()
# print("cross test:")
# cross=vect.cross(vect2)
# print(cross)
# print("dot test:")
# dot=vect.dot(vect2)
# print(dot)
# print("norm test:")
# norm=vect.norm()
# print(norm)
# print("normalize test:")
# norma=vect.normalize()
# norma.print_screen()
# print("translate test:")
# tran=vect2.translate_to(Point(8,10))
# tran.print_screen()
# print("unit_vector test:")
# uv=vect.unit_vector()
# uv.print_screen()
# print("norm not vect test:")
# nvt=vect.normalize_not_vectorized()
# nvt.print_screen()
# print("print_screen test!")
# print("no comment")
# print("Vecor field init test:")
# vec=[]
# pts=[]
# for i in range(0,10):
# 	vec.append(Vect(i,i*2,i+4,i*3))
# 	pts.append(Point(i*5,2*i-3))
# field=Vector_field(vec,pts)
# field.print_screen()