import os
import re

def find_directory(liste):
	#Find directory list from the given string and the regular expression
	regex = re.compile("C.*$",re.MULTILINE)
	ret=[]
	ret=re.findall(regex,liste)
	return ret

def find_py_file(string):
	#Find .py file list from the given list and the regular expression
	regex=re.compile("([a-zA-Z_]*\.py)",re.MULTILINE)
	ret=[]
	ret=re.findall(regex,string)
	return ret

def find_path():
	#find full path list of .py file with their associated directory
	regex_dir = re.compile("C.*$",re.MULTILINE)
	py_files=[]
	liste=''
	liste=os.popen("dir \"*.py\" /s").read()
	dir_liste=find_directory(liste)
	splitted=re.split(regex_dir,liste)

	final_path=[]
	for i in range(2,len(splitted)-1):
		final_path.append(dir_liste[i])
		final_path.append(find_py_file(splitted[i+1]))
	return final_path

def rebuild_string(liste):
	#rebuild string_path from computed list
	path_list=[]
	tmp_name=''
	for i in range(0,len(liste)):
		if(i%2==0):
			tmp_name=liste[i]
		else:
			for j in range(0,len(liste[i])):
				path_list.append(tmp_name+"\\"+liste[i][j])
	return path_list



path=find_path()
path_list=[]
path_list=rebuild_string(path)
print(path_list)

# Used regular expressions
# directory
# \C\\*.*$

# py file :
# (\n*.*\s)([a-zA-Z_]*\.\p\y))
