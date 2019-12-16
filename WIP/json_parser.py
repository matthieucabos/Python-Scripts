import re
import enum

def supQuote(string):
	res=""
	for s in string:
		if(s!="\"" and s!="\n" and s!="\t"):
			res+=s
	return res

def getkey(string):
	res=""
	found=False
	for s in string:
		if(s!=":" and not found):
			res+=s 
		else:
			found=True
	return res

def getvalue(string):
	res=""
	found=False
	for s in string:
		if(found):
			res+=s
		if(s==":"):
			found=True
	return res


class json_parser:

	def __init__(self):
		self.dic={}
		self.data=""
		self.enum=self.create_enum()

	def type_identifier(self,local_data):
		# Get the type from the given local_data argument
		return switch(True,
			'str',isintance(data,str),
			'int',isintance(data,int),
			'float',isintance(data,float),
			'list',isinstance(data,list))

	def get_data(self,path):
		# Get full data from the file specified by given path argument
		if(re.finditer(r".*\.json",path)):
			# Assert the parameter file is a json file
			file = open(path,"r")
			data=file.read()
			# for elem in raw:
			# 	data.append(elem)
			file.close()
			return data
		else:
			return none

	def split(self,local_data):
		# Split data 
		res=[]
		tmp=""
		for elem in local_data:
			if(elem!="\n" and elem!="\t" and elem!=","):
				tmp+=elem
			elif(elem=="\n"):
				res.append(tmp)
				tmp=""
			else:
				pass
		return res

	def create_enum(self,names=[],enum_name="enum"):
		# Create a enum object from the given names array and enum_name defining the class name.
		values={}
		for i in range(0,len(names)):
			values.update({names[i]:i+1})  # updating the class content dictionnary
		meta=type(enum.Enum)
		bases=(enum.Enum,)
		dict=meta.__prepare__(names,bases)
		for key,value in values.items():
			dict[key]=value
		return meta(enum_name,bases,dict)  # get Enum object as a return using metaclass function

	def find_obj(self,data):
		# Find an object in raw local_data (json syntax)
		res={}
		i=0
		matches=re.finditer(r"\".*\[([^\]]|\n)*\]",data,re.MULTILINE)
		if(matches):
			for m in matches:
				key=re.finditer(r"\"[^:]*\"",m.group(0))
				value=re.finditer(r"\[(.|\n)*\]",m.group(0))
				for k in key:
					if(not i):
						truekey=k.group(0)
					i+=1
				i=0
				for v in value:
					if(not i):
						# print(v.group(0))
						# print(self.is_obj(v.group(0)))
						# if(not self.is_obj(v.group(0))):
						res[supQuote(truekey)]=self.get_entry(supQuote(v.group(0)),1)
						# else:
						# 	res[supQuote(truekey)]=self.find_obj(v.group(0))

		return res

	def get_entry(self,data,rec=0):
		# Get the key of a json entry
		res={}
		i=0
		if(not rec):
			regex=r"\"[^:]*\""
		else:
			regex=r"[^[{]*[^[{}\],]"
		matches=re.finditer(regex,data,re.MULTILINE)
		if(matches):
			for m in matches:
				if(not self.is_obj(data) or rec):
					if(not rec):
						if(i%2==0):
							tmp=m.group(0)
						else:
							res[supQuote(tmp)]=supQuote(m.group(0))
						i+=1
					else:
						if(i%2==0):
							tmp=m.group(0)	
							key=getkey(tmp)
							value=getvalue(tmp)	
							res[key]=value
							key=""
							value=""		
			return res
		else:
			return {}

	def is_obj(self,line):
		for l in line:
			if(l=="[" or l=="]"):
				return True
		return False

	def _2xml(self):
		res="<?xml version="1.0" ?>"
		pass

	def _2Json(self):
		pass

# Parser algorithm

J=json_parser()
test=J.get_data("test2.json") # Get raw data as string
test2=J.find_obj(test)       # Collecting Json objects
test=J.split(test)           # Split the raw sequence
for i in range(0,len(test)):  
	test2.update(J.get_entry(test[i])) # Updating dictionnary with alone key/values

print(test2)
# print("------------------")
# print(test2["encore"])