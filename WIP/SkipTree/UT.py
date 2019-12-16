def zero_align(value,heigth):
	loc_len=0
	tmp=value
	while(tmp>1):
		loc_len+=1
		tmp/=10
		print(tmp)
	for i in range(0,loc_len):
		value*=10
	return value

print(zero_align(31,4))