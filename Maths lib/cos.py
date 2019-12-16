def floor(x):
	return int(x)

def abs(x):
	return x if x>0 else -x

def cos(x):
	const=1/3.141592653589793
	x*=const
	x-=0.25+floor(x+0.25)
	x*=16*(abs(x)-1)
	return x