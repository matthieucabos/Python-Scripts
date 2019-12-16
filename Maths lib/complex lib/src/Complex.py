import numpy as np 

# __author__="CABOS Matthieu"
# __date__=02_07_2018

####################################
# Complex arithmetic implementation#
####################################

def sqrt(X):
	x=0.01
	for i in range(0,100):
		x=(x+X/x)/2
	return x

class Complex:
#%%

###################
###### Utils ######
###################

	def __init__(self,a,b):
		self.a=a 
		self.b=b

	def set_a(self,a):
		self.a=a 

	def set_b(self,b):
		self.b=b

	def op(self,z,op):
		if(op=='+'):
			return Complex(self.a+z.a,self.b+z.b)
		elif(op=='-'):
			return Complex(self.a-z.a,self.b-z.b)
		elif(op=='*'):
			return Complex(self.a*z.a-self.b*z.b,self.b*z.a+self.a*z.b)
		elif(op=='/'):
			# return Complex(z*self.conjug()/self.module()**2)
			den=(z.a**2+z.b**2)
			return Complex((z.a*self.a+z.b*self.b)/den,(self.b*z.a-self.a*z.b)/den)

	def print(self):
		print("z = "+str(self.a)+" + "+str(self.b)+" i")
#%%

####################
#### Arithmetic ####
####################

	def conjug(self):
		return Complex(self.a,-self.b)


	def module(self):
		return sqrt(self.a*self.a+self.b*self.b)

	def arg(self):
		return np.arctan(self.b/self.a)

	def __add__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float))):
			return self.op(Complex(z,0),'+')
		elif(isinstance(z,Complex)):
			return self.op(z,'+')

	def __iadd__(self,z):
		self=self+z 
		return self

	def __sub__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float))):
			return self.op(Complex(z,0),'-')
		elif(isinstance(z,Complex)):
			return self.op(z,'-')

	def __isub__(self,z):
		self=self-z
		return self

	def __mul__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float))):
			return self.op(Complex(z,0),'*')
		elif(isinstance(z,Complex)):
			return self.op(z,'*')

	def __imul__(self,z):
		self=self*z 
		return self

	def __truediv__(self,z):
		if((isinstance(z,int)) or (isinstance(z,float))):
			return self.op(Complex(z,0),'/')
		elif(isinstance(z,Complex)):
			return self.op(z,'/')

	def __idiv__(self,z):
		self=self/z 
		return self 

	def __pow__(self,n):
		for i in range(0,n-1):
			self=self*self 
		return self

	def __ipow__(self,n):
		self=self**n 
		return self

	def __neg__(self):
		return Complex(-self.a,-self.b)

	def __str__(self):
		self.print()
		return 'printed'

	def __eq__(self,z):
		if(isinstance(z,Complex)):
			return (self.a==z.a and self.b==z.b)
		else:
			return false

	def __ne__(self,z):
		return not(self==z)

	def __gt__(self,z):
		return(self.a>=z.a and self.b>z.b)

	def __ge__(self,z):
		return(self.a>=z.a and self.b>=z.b)

	def __lt__(self,z):
		return(self.a<=z.a and self.b<z.b)

	def __le__(self,z):
		return(self.a<=z.a and self.b<=z.b)

	def sqrt(self):	
		# X=self.a**2-self.b**2
		# Y=2*self.a*self.b
		# return Complex((X+(X**2+Y**2)**1/2)**1/2,Y/2*X)
		r=self.module()
		return ((self+r)/((self+r).module()))*sqrt(r)

	def mul_inv(self):
		return Complex(1,0)/self

	def polar(self):
		return Complex(np.cos(self.arg(),np.sin(self.arg())))*self.module()

	def pow(self,n):
		return Complex(np.cos(self.arg()*n),np.sin(self.arg()*n))*self.module()**n


    	
#%%

###################
# transformations #
###################

	def translate(self,x):
		self+=x 

	def rotate(self,x,y):
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

	def exp(z):
		return Complex(np.cos(z.b()),np.sin(z.b()))*np.exp(z.a())