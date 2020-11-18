
__author__="CABOS Matthieu"
__date__=18_11_2020

'''
	Here you will find a tester as decorator. The tester take as the only parameter the name of the function to test.
'''

def switch(x,*arg):
	dic ={}
	for i in range(int(len(arg)-1)):
		dic[arg[i]]=arg[i+1]
	return dic.get(x,'default')

def arg_build(args):
	# Arguments builder
	res=[]
	if(args[0]=='i'):
		tmp=0
		for item in args[1:]:
			if item != " ":  #Integer reconstruction since Horner Scheme
				tmp*=10
				tmp+=int(item)
			else:
				res.append(tmp)
				tmp=0
		res.append(tmp)
	elif (args[0]=='s'):
		tmp=""
		for item in args[1:]:
			if item!=" ":
				tmp+=item
			else:
				tmp+=" "
				res.append(tmp)
				tmp=""
		res.append(tmp)
	elif (args[0]=='f'):
		tmp=0.0
		decimal=False
		index=1
		for item in args[1:]:
			if item!=" " and item!=".":
				tmp*=10
				tmp+=float(item)
			elif item=="." :
				decimale=True
			elif item == " ":
				res.append(tmp)
				tmp=0.0
				decimal=False
			elif decimale:
				item=float(item)/10**index
				tmp+=item
				index*=10
		res.append(tmp)
	return res

def test(func):
	class Decorator(object):
		def __init__(self,func):
			self.func=func
		def __call__(self,*args,**kwargs):
			real_arg=switch(self.func.__name__,
				'summ','i10 5',
				'divv','f20 2',
				'concat','sCeci est un test')
			real_res=switch(self.func.__name__,
				'summ',15,
				'divv',10,
				'concat','Ceci est un test')

			#Asserting return values from parameters values (testing procedure)

			if(self.func(arg_build(real_arg),**kwargs)==real_res): #self.func implicitely convert args to tuple :(
				print ("Test passed, congratulations !")
				return self.func(arg_build(real_arg),**kwargs)
			else:
				print ("Error occured, go back to work lazy dev !")
	return Decorator

@test('func')
def summ(args):
	summ=0
	for item in args:
		summ+=item
	return summ

@test('divv')
def divv(args):
	return args[0]/args[1]

@test('concat')
def concat(args):
	res=""
	for item in args:
		res+=item
	return res
