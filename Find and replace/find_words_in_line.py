import re

def find_word_in_string(string):
	#Create the words list from the given string
	regex=re.compile("\s",re.MULTILINE)
	words=re.split(regex,string)
	return words

def replace_word_in_string(string,word_or,word_re):
	ret=""
	words=find_word_in_string(string)
	for i in range(0,len(words)):
		print(words[i])
		if(word_or in words[i]):
			words[i]=word_re
		ret+=words[i]+(" ")
	return ret

test="salut, comment ça va aujourd'hui ?\n salut Albert je vais tres bien et toi ?\n a+++"
words=find_word_in_string(test)
print(words)
test=replace_word_in_string(test,"salut","bon")
print(test)
	