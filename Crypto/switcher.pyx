from ...  import v1
from ...  import v2
.
.
.



cpdef class crypt_mode():
	string list v_name
	string v_current
	int size
	int ind

	def __cinit__(self,name):
		for n in name:
			self.v_name.append(n)
		self.size=len(name)
		self.v_current=self.v_name[0]

	cdef void inc(self):
		#increment the cyclic crypting mode
		self.ind=(self.ind+1)%(self.size)
		self.v_current=v_name[self.ind]

	cdef string name(self):
		#get the name of the current crypting algorithm version
		return self.v_name

cpdef class clock():
	cdef:
		int list seq
		int size
		float frequency
		int current

	cdef __cinit__(self,seq,freq):
		self.seq=seq
		self.size=len(seq)
		self.frequency=freq

	cdef void on(self):
		#start the clock
		ind=0

		while(1):
			ind+=1
			if ind % self.size == 0 :
				self.current=(self.current+1)%self.size

	cdef int rise(self):
		#get rising state (int=1)
		return (self.seq[self.current])

cpdef class crypter():
	cdef:
		string to_crypt
		string cryptd 
		string key
		int list clock_seq
		crypt_mode code_cr

	def __cinit__(self,to_crypt,clock_seq=clock([1,0,0,1,0,0,0,1,0,0,0,1])):
		# clock_seq code the sequence of switchin algorithm (used to decrypt similary)
		self.to_crypt=to_crypt
		self.code_cr=crypt_mode(["v1","v2","v3","v4","v4.2"])
		self.key=code_cr.name().get_key(to_crypt)
		self.cryptd=code_cr.name().get_string(to_crypt) #35sec to write
		self.clock_seq=clock_seq

	cdef void switch_crypt(self):
		#switch the crypting algorithm from the rising state clock
		if(self.clock_seq.rise()):
			self.code_cr.inc()

	cdef void on(self):
		#start the cyclic crypting switch clock-sync
		self.clock_seq.on()
		while(1):
			self.switch_crypt()

def example():
	code_cr=crypt_mode(["v1","v2","v3","v4","v4.2"])
	clock_seq=clock([1,0,0,1,0,0,0,1,0,0,0,1])

	while(1):
		switch_crypt(clock_seq,code_cr)