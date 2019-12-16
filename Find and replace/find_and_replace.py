import os
import re
import sys

__author__="CABOS Matthieu"
__date__="09/10/2018"

#===========================================================#
# WARNING !!! NO WAY BACK !!! , please be extremely careful #
#===========================================================#
# The algorithm replace parts of codes into a source code.  #
# The replaced code could be single word or a sequence.     #
# In case of sequence please replace the full line to       #
# keep file structure                                       #
# To treat big packages including differents levels of tree,#
# the algorithm is recursive and will act on each .ext file.#
# extension is given as the first argument                  #
# original code to replace is given as the second one       #
# the replaced code is given as the third.                  #
# Three arguments are given as string.                      #
#===========================================================#
# Explanations:                                             #
# =============                                             #
# -Create directory list and .py file list from current     #
#        directory                                          #
# -Rebuild original string path for each source file        #
# -Open and replace the original code samples givenby       #
#        the replace part of code                           #
# -Write modified contents in source file                   #
#===========================================================#

def find_directory(liste):
	"""
		Find directory list from the given string and the regular expression

		=============== ========== ========================
		**Parameters**   **Type**   **Description**
		*liste*          String     The name list to treat
		=============== ========== ========================

		Returns
		-------
			String list
			The list containing all directories path
	"""
	regex = re.compile("[C-G]:.*$",re.MULTILINE)
	ret=[]
	ret=re.findall(regex,liste)
	return ret

def find_file(string,extension):
	"""
		Find .extension file list from the given list and the regular expression

		=============== ========== =============================================
		**Parameters**   **Type**   **Description**
		*liste*          String     The name list to treat
		*extension*      String     File ext to search (like py for python file)
		=============== ========== =============================================

		Returns
		-------
			String list
			The list containing all .ext files name
	"""
	string_reg="([a-zA-Z0-9-_.!;,=+()#°@^*"+"\."+extension+")"
	regex=re.compile(string_reg,re.MULTILINE)
	ret=[]
	ret=re.findall(regex,string)
	return ret

def find_path(extension):
	"""
		Find full path list of .extension file with their associated directory

		=============== ========== =============================================
		**Parameters**   **Type**   **Description**
		*extension*      String     File ext to search (like py for python file)
		=============== ========== =============================================

		Returns
		-------
			String list
			The list containing all .ext files path and their associated directory
	"""
	#
	regex_dir = re.compile("[C-G]:.*$",re.MULTILINE)
	py_files=[]
	liste=''
	if (os.name=='nt'):    # windows users command
		cmd="dir \"*."+extension+"\" /s"
	else:                  # posix users command
		cmd="ls -R"
	liste=os.popen(cmd).read()
	dir_liste=find_directory(liste)
	splitted=re.split(regex_dir,liste)
	final_path=[]
	for i in range(0,len(splitted)-1):
		final_path.append(dir_liste[i])
		final_path.append(find_file(splitted[i+1],extension))
	return final_path

def rebuild_string(liste):
	"""
		Rebuild string_path from the computed list

		=============== ============= ==========================================
		**Parameters**   **Type**     **Description**
		*liste*          String list  The list computed from find_path function
		=============== ============= ==========================================

		Returns
		-------
			String list
			The list containing all the .ext files path
	"""
	path_list=[]
	tmp_name=''
	for i in range(0,len(liste)):
		if(i%2==0):
			tmp_name=liste[i]
		else:
			for j in range(0,len(liste[i])):
				path_list.append(tmp_name+"\\"+liste[i][j])
	return path_list

def concat(liste):
	"""
		Concatenate lines_list to rebuild the treated file content

		=============== ============ ==================================
		**Parameters**   **Type**     **Description**
		*liste*          String list  The file contents as a line list
		=============== ============ ==================================

		Returns
		-------
			String
			The rebuilt file contents.
	"""
	res=""
	for line in liste:
		res+=line
	return res

def find_word_in_string(string):
	"""
		Create the words list from the given string
	"""
	regex=re.compile("\s",re.MULTILINE)
	words=re.split(regex,string)
	return words

def replace_word_in_string(string,word_or,word_re):
	"""
		replace any occurence of word_or by word_re in the given string

		=============== ========== =======================================
		**Parameters**   **Type**   **Description**
		*string*         String     The string to treat
		*word_or*        String     The or)iginal sub-sequence to replace
		*word_re*        String     The re)placement sub-sequence
		=============== ========== =======================================

		Returns
		-------
			String
			The rebuilt string with replacement.
	"""
	ret=""
	words=find_word_in_string(string)
	for i in range(0,len(words)):
		print(words[i])
		if(word_or in words[i]):
			words[i]=word_re
		ret+=words[i]+(" ")
	return ret

def get_nb_words(string):
	#admire
	return len(find_word_in_string(string))


def replace_code(path_list,original_code,replaced_code,mode):
	"""
	The main algorithm of source code replacement, all the original_code found in source file will be replaced by replaced code argument.

	================ =========== =======================================
	**Parameters**   **Type**     **Description**
	*path_list*      String list  The path list to browse
	*original_code*  String       The original sub-sequence to replace
	*replaced_code*  String       The re)placement sub-sequence
	*mode*           Int          Replacement mode
									0 => single word
									1 => instruction's sequence
	================ =========== =======================================

	Returns
	-------
		None
		WARNING ! The algorithm write replacement code directly in files.
		No way back
		Please be careful !!!
	"""
	for i in range(0,len(path_list)):
		filename=path_list[i]
		try:
			file=open(filename,"r+")
			print(filename + " \n| opened and treated")
		except:
			pass
		lines=file.readlines()
		file.seek(0,0)
		file.truncate()
		for i in range(0,len(lines)):
			if(original_code in lines[i]):
				if(not mode):
					lines[i]=replace_word_in_string(lines[i],original_code,replaced_code)
				else:
					lines[i]=replaced_code
		file_content=''
		file_content=concat(lines)
		file.write(file_content)
	print("Done, thanks.")

# Main script body

if(len(sys.argv)!=4):
	print("usage : find_and_replace.py <file extension> <code part to replace> <desired replace code>")
	exit(0)

ext=sys.argv[1]
print(ext)
original_code=sys.argv[2]
mode=(0 if (get_nb_words(original_code)==1) else 1)
replaced_code=sys.argv[3]
mode=(0 if (get_nb_words(replaced_code)==1) else 1)
print("mode = "+str(mode))

path=find_path(ext)
path_list=[]
path_list=rebuild_string(path)
for i in range(0,len(path_list)):
	print(path_list[i])
for i in range(0,len(path_list)):
	print(path_list[i])
replace_code(path_list,original_code,replaced_code,mode)

# Used regular expressions
#Tested on https://regex101.com/
# directory
# \C\\*.*$

# py file :
# (\n*.*\s)([a-zA-Z_]*\.\p\y))

# :-) 
