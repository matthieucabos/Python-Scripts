import numpy as np 

__author__="CABOS Matthieu"
# __date__=02_07_2018

####################################
# Complex arithmetic implementation#
####################################

# TO TEST
cdef class Complex():
	cdef:
		double a 
		double b 
#%%

###################
###### Utils ######
###################

	def __init__(self,double a,double b):
		self.a=a 
		self.b=b 

	cpdef double a(self):
		return self.a 

	cpdef double b(self):
		return self.b

	cpdef void set_a(self,double a):
		self.a=a 

	cpdef void set_b(self,double b):
		self.b=b

	cpdef Complex op(self,Complex z,str op):
		if(op=='+'):
			return Complex(self.a()+z.a(),self.b()+z.b())
		elif(op=='-'):
			return Complex(self.a()-z.a(),self.b()-z.b())
		elif(op=='*'):
			return Complex(self.a()*z.a()-self.b()*z.b(),self.b()+z.a()+self.a()*z.b())
		elif(op=='/'):
			return Complex(z*self.conjug()/self.module()**2)

	cpdef void print_screen(self):
		print("z = "+str(self.a())+" + "+str(self.b())+" i")
#%%

####################
#### Arithmetic ####
####################

	cpdef void conjug(self):
		self.b=-self.b

	cpdef double module(self):
		return (self.a()*self.a()+self.b()*self.b())**1/2

	cpdef double arg(self):
		return np.arctan(self.b()/self.a())

	def __add__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float)) or (isinstance(z,double))):
			return self.op(Complex(z,0),'+')
		elif(isinstance(z,Complex)):
			return self.op(z,'+')

	def __sub__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float)) or (isinstance(z,double))):
			return self.op(Complex(z,0),'-')
		elif(isinstance(z,Complex)):
			return self.op(z,'-')

	def __mul__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float)) or (isinstance(z,double))):
			return self.op(Complex(z,0),'*')
		elif(isinstance(z,Complex)):
			return self.op(z,'*')

	def __div__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float)) or (isinstance(z,double))):
			return self.op(Complex(z,0),'/')
		elif(isinstance(z,Complex)):
			return self.op(z,'/')

	cpdef Complex sqrt(self):
		cdef:
			double X
			double Y
		X=self.a()**2-self.b()**2
		Y=2*self.a()*self.b()
		return Complex((X+(X**2+Y**2)**1/2)**1/2,Y/2*x)

	cpdef Complex mul_inv(self):
		return Complex(Complex(1,0)/self)

	cpdef Complex polar(self):
		return self.module()*Complex(np.cos(self.arg(),npsin(self.arg())))

	cpdef Complex pow(self,n):
		return self.module()**n*Complex(np.cos(self.arg()*n),np.sin(self.arg()*n))

	cpdef Complex exp(Complex z):
		return np.exp(z.a())*Complex(np.cos(z.b()),np.sin(z.b()))
    	
#%%

###################
# transformations #
###################

	cpdef void translate(self,Complex x):
		self+=x 

	cpdef rotate(self,Complex x,Complex y):
		cdef:
			Complex center
			double angle
		center = y/1-x
		angle  = x.arg()
		self=self*x
		self+=y
		return (center,angle)

#%%

#######################
# Standards generator #
#######################

	@staticmethod
	def unit_root_n(n):
		return Complex(np.cos(2*np.pi/n),np.sin(2*np.pi/n))

	@staticmethod
	def mandelbrot(self,z,c):
		return z**2+c