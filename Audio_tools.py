import math as m
import numpy as np
import sys
from scipy.io.wavfile import write
from scipy.special import erf

__author__="CABOS Matthieu"
__date__="09/10/2018"
error_inc=0

"""
	This is the main code skeleton for modular synthesizer using emulation of local electric systems.
"""

#################################
########### from net ############
#################################

def fusion(gauche,droite):
    resultat = []
    index_gauche, index_droite = 0, 0
    while index_gauche < len(gauche) and index_droite < len(droite):        
        if gauche[index_gauche] <= droite[index_droite]:
            resultat.append(gauche[index_gauche])
            index_gauche += 1
        else:
            resultat.append(droite[index_droite])
            index_droite += 1
    if gauche:
        resultat.extend(gauche[index_gauche:])
    if droite:
        resultat.extend(droite[index_droite:])
    return resultat
 
def tri(m):
    if len(m) <= 1:
        return m
    milieu = len(m) // 2
    gauche = m[:milieu]
    droite = m[milieu:]
    gauche = tri(gauche)
    droite = tri(droite)
    return list(fusion(gauche, droite))



#%%
#################################
############# utils #############
#################################


#double way switch
def switch(x,*arg):
	"""
		Redefined C-like switch.
		Could also be used as an inverse switch where x is a value and arg the differents variables to test.

		==============   ============== ==================================================
		**Parameters**   **Type**        **Description**
		*x*              string          the variable name to switch
		*arg*            string/generic  the differents states to switch, defined mod 2 :
										 "string",function,"string",function,...
		==============   ============== ==================================================

		Returns
		-------
			The function or action corresponding to the switch entry.

		Example
		-------
		As normal mode
		switch(variable,
			"case a",action_a
			"case b",action_b)

		As inverse mode
		switch(True,
			"variable_a",action_a,
			"variable_b",action_b)
	"""
	dic ={}
	for i in range (0,int(len(arg)-1)):
		dic[arg[i]]=arg[i+1]
	return dic.get(x,'default')


def midi_to_freq(midi):
	"""
		Get note frequency from midi logic note number.

		=============== ========== =======================
		**Parameters**   **Type**   **Description**
		*midi*           int        the logical midi note
		=============== ========== =======================

		Returns
		-------
			float
			the frequency value in Hz.
	"""
	if (midi < 0 or midi > 127):
		error("midi",1)
	else:
		return 440*np.exp(np.log(2)*((midi-69)/12));

def lin(value,inter1=0,inter2=10):
	# Linear transfer function (in base 10 as default)
	return value*((inter2-inter1)/10)+inter1


def ERF(x):
	# Error function utils for logarithmic distribution
	sig=False
	if(x<0):
		x=-x
		sig=True
	local_erf=[erf(i/50) for i in range(0,100)]
	try :
		if(not sig):
				# local_erf=local_erf[-1::-1]
				return local_erf[int(x*50)]
		else:
				return -local_erf[int(x*50)]
	except:
		return 0
# ICI!!!
def log(value,inter1,inter2,sig=1,mu=2):
	# log distribution function
	x=value/inter1
	return inter2*(1/2 + ERF((np.log(x)-mu)/sig*np.sqrt(2))/2)
	# return 1/2+1/2*ERF((np.log(value)-mu)/sig*np.sqrt(2))

def log_distr(inter1,inter2=127,sig=1,mu=2):
	# Create a local log distribution from inter1 (should be voltage value) to inter2 (127 as default)
	local_distr=[log(i/inter1,inter1,inter2,sig,mu) for i in range(0,inter1*10)]
	print(local_distr)
	return(tri(local_distr))

def exp(value,inter1,inter2,lmbd=1.0):
	# exp distribution function
	x=value/inter1
	return inter2*(1-np.exp(-lmbd*x))

def AtoBinCtoD(AtoB,CtoD,value,mode,**arg):
	"""
		Transfer/conversion function from [A,B] to [C,D]

		=============== ============ =====================================================================
		**Parameters**   **Type**    **Description**
		*AtoB*            int tuple  starting interval as (A,B)
		*CtoD*            int tuple  ending interval as (C,D)
		*value*           float      the raw value to treat
		*mode*            string     the transfer distribution mode between:
										* 'linear' : a*x+b
										* 'log' : log distr with mu=0 and sig as optionnal last argument
											sig in ]0,10]
										* 'exp' : exp distr with lambda as optionnal last argument
											lambda in [0,1.5]
		=============== ============ =====================================================================

		Returns
		-------
			float
			The converted value
	"""
	inter1=AtoB[1]-AtoB[0]
	inter2=CtoD[1]-CtoD[0]
	log=log_distr(inter1,inter2,**arg)
	return switch(mode,
		'linear',lin(value,inter1,inter2),
		'log',log[int(value*10)],
		'exp',exp(value,inter1,inter2,**arg))


#%%
#################################
####### sound_oscillators #######
#################################

def play_sin(freq,amp,t):
	"""
		sin VCO emulation : give the sin osc value at time t (t in z, where z represent the full length of the loop to treat)

		============== ==========  ==============================
		**Parameters**   **Type**   **Description**
		*freq*          float      The frequency of the VCO
		*amp*           float      Amplitude of the oscillator
		*t*             int        the t time
		============== ==========  ==============================

		Returns
		-------
			float
			The emulated voltage of the VCO from parameters.
	"""
	return amp*m.sin(2*m.pi*freq*t)

# tri oscillator emulation
def play_tri(freq,amp,t):
	"""
		tri VCO emulation : give the tri osc value at time t (t in z, where z represent the full length of the loop to treat)

		============== ==========  ==============================
		**Parameters**   **Type**   **Description**
		*freq*          float      The frequency of the VCO
		*amp*           float      Amplitude of the oscillator
		*t*             int        the t time
		============== ==========  ==============================

		Returns
		-------
			float
			The emulated voltage of the VCO from parameters.
	"""
	return amp*np.arcsin(np.sin(2*m.pi*freq*t)) 

def cot(x):
	"""
		Local cotangent computing
	"""
	if(x==0):
		error("Zero divide",2)
	else:
		# cos_x=np.cos(x)
		return 1/np.tan(x)   # (cos_x/np.sqrt(1-cos_x*cos_x))  

# sawtooth oscillator emulation
def play_saw(freq,amp,t):
	"""
		saw VCO emulation : give the saw osc value at time t (t in z, where z represent the full length of the loop to treat)

		============== ==========  ==============================
		**Parameters**   **Type**   **Description**
		*freq*          float      The frequency of the VCO
		*amp*           float      Amplitude of the oscillator
		*t*             int        the t time
		============== ==========  ==============================

		Returns
		-------
			float
			The emulated voltage of the VCO from parameters.
	"""
	if(freq==0):
		error("Zero divide",3)
	else:
		return np.arctan(cot(np.pi*t/freq))*(2*amp/np.pi)

# squ oscillatior emulation (to fix) 
def play_squ(freq,amp,t):
	"""
		squ VCO emulation : give the squ osc value at time t (t in z, where z represent the full length of the loop to treat)

		============== ==========  ==============================
		**Parameters**   **Type**   **Description**
		*freq*          float      The frequency of the VCO
		*amp*           float      Amplitude of the oscillator
		*t*             int        the t time
		============== ==========  ==============================

		Returns
		-------
			float
			The emulated voltage of the VCO from parameters.
	"""
	if(t*freq<int(t*freq)):
		return amp
	else:
		return-amp

#%%
#################################
##### sound playing routine #####
#################################

def play_midi(freq,amp,t,wav_form):
	"""
		Play a single midi note from frequency.

		=============== ========== ==========================================================
		**Parameters**   **Type**   **Description**
		*freq*           float     The note frquency to play
		*amp*            float     The amplitude value of the played note
		*t*              int       The t time in z (where z represent the full signal loop)
		*wav_form*       string    The wavform name between sin, tri, squ or saw
		=============== ========== ==========================================================

		Returns
		-------
			float
			A single audio signal point as a float.
	"""
	assertt=["sin","tri","squ","saw"]
	if not wav_form in assertt:
		error("Wav form name",4)
	else:
		signal=switch(wav_form,
			"sin",play_sin(freq,amp,t),
			"tri",play_tri(freq,amp,t),
			"squ",play_squ(freq,amp,t),
			"saw",play_saw(freq,amp,t))
		return signal

def play_sound(midi_note,amp,t,wav_form):
	"""
		Convert and play a midi logic note number.

		==============   ========  ==========================================================
		**Parameters**   **Type**   **Description**
		*midi_note*      int        The midi logical note number to play
		*amp*            float      The amplitude value of the played note
		*t*              int        The t time in z (where z represent the full signal loop)
		*wav_form*       string     The wavform name between sin, tri, squ or saw
		==============   ========  ==========================================================

		Returns
		-------
			float
			A single audio signal point as a float.
	"""
	if (midi_note < 0 or midi_note > 127):
		error("midi",5)
	else:
		freq=midi_to_freq(midi_note)
		if(amp>0):
			signal=play_midi(freq,amp,t,wav_form)
		return signal

def signal_mix(signal1,signal2):
	"""
		Mix two signal preserving meaned amplitude value of the two given signals.

		===============  ==========  =======================
		**Parameters**   **Type**    **Description**
		*signal1*        float list  Signal as a float list
		*signal2*        float list  Signal as a float list
		===============  ==========  =======================

		Returns
		-------
			Float list
			The mixed signal as a float list.
	"""
	if(len(signal1)!=len(signal2)):
		return []
	for i in range (0,len(signal1)):
		signal1[i]=int((signal1[i]+signal2[i])/2)
	return signal1

#%%
#################################
####### Sequencer features ######
#################################

	#Sequencer read mode

def play_midi_sequence(midi_seq,wav_form,raw_bpm):
	"""
		Read and play a midi sequence.

		=============== ========== ====================================================
		**Parameters**   **Type**   **Description**
		*midi_seq*       int list   A midi sequence as a list of midi logic note (int)
		*wav_form*       string     The wavform name between sin, tri, squ or saw   
		*raw_bpm*        int        Standard bpm value
		=============== ========== ====================================================

		Returns
		-------
			Float list
			The played midi sequence signal as a Float list
	"""
	signal = [0]*raw_bpm*len(midi_seq)
	for t in range(0,len(midi_seq)):
		if (midi_seq[t] != 0):
			for i in range(0,raw_bpm-1):
				signal[raw_bpm*t+i]=int(play_sound(midi_seq[t],10,(t+i)/raw_bpm,wav_form))
		else:
			for i in range(0,raw_bpm-1):
				signal[raw_bpm*t+i]=0
	return signal

def octave_transpose(midi_seq,octave):
	"""
		Transpose a sequence from the given octave.

		=============== ========== ====================================================
		**Parameters**   **Type**   **Description**
		*midi_seq*       int list   A midi sequence as a list of midi logic note (int)
		*octave*         int        the number of octave to transpose
		=============== ========== ====================================================

		Returns
		-------
			int list
			The transposed sequence as an int list.
	"""
	for i in range(0,len(midi_seq)):
		if(midi_seq[i]!=0):
			midi_seq[i]+=12*octave
	return midi_seq

def tone_transpose(midi_seq,tune):
	"""
		Transpose a sequence from the given tune

		=============== ========== ====================================================
		**Parameters**   **Type**   **Description**
		*midi_seq*       int list   A midi sequence as a list of midi logic note (int)
		*tune*           int        The number of tune to transpose
		=============== ========== ====================================================

		Returns
		-------
			int List
			The transposed sequence as an int list.
	"""
	for i in range(0,len(midi_seq)):
		if(midi_seq[i]!=0):
			midi_seq[i]+=tune
	return midi_seq

def harmonic(freq_seq,tune=0):
	"""
		Add the n-th harmonic (between 3,4,5 and 6) to the current frequency signal.
	"""
	res=[0]*len(freq_seq)
	for i in range(0,len(freq_seq)):
		if(tune==3):   # Tierce majeure
			res[i]=(freq_seq[i]+(5/4)*freq_seq[i])/2
		elif(tune==4): # Quarte
			res[i]=(freq_seq[i]+(4/3)*freq_seq[i])/2
		elif(tune==5): # Quinte
			res[i]=(freq_seq[i]+(3/2)*freq_seq[i])/2
		elif(tune==6): # Sixte
			res[i]=(freq_seq[i]+(5/3)*freq_seq[i])/2
	return res

#%%
#################################
###### Sounds optimisation ######
#################################

def factorial(n):
	"""
		Local factorial computing.
		float to float
	"""
	if(n==0):
		return 1
	else:
		return n*factorial(n-1)

def bessel_polynomial(order,x):
	"""
		Loacl Bessel polynomial implementation.

		=============== ========== ======================================
		**Parameters**   **Type**   **Description**
		*order*          int        The order of the polynom to compute.
		*x*              float      The x value of the polynom
		=============== ========== ======================================

		Returns
		-------
			Float
			The compute bessel polynom from given args.
	"""
	for i in range(0,order):
		res+=(factorial(n+i)/(factorial(n-i)*factorial(i)))*(x**(n-i)/2**i)
	return res

def butterworth_polynomial(order,x):
	"""
		Loacl Butterworth polynomial implementation.

		=============== ========== ======================================
		**Parameters**   **Type**   **Description**
		*order*          int        The order of the polynom to compute.
		*x*              float      The x value of the polynom
		=============== ========== ======================================

		Returns
		-------
			Float
			The compute Butterworth polynom from given args.
	"""
	res=x+1
	for i in range(1,int((order-1)/2)):
		res*=(x*x-2*x*np.cos(((2*i+order-1)/2*order)*np.pi)+1)
	return res

def make_harmonics(signal,wav_form,sequence,raw_bpm):
	"""
	 	Make pseudo-harmonics on the frequency band (obsolete, should be implemented directly on oscillators maths generated Fourier series).

		=============== ============ ===============================================
	 	**Parameters**   **Type**     **Description**
	 	*signal*         float array  The signal to feed in harmonics
	 	*wav_form*       string       The wavform name between sin, tri, squ or saw
	 	*sequence*       int list     The midi sequence as an int list
	 	*raw_bpm*        int          Standard bpm value
	 	=============== ============ ===============================================

	 	Returns
	 	-------
	 		Float list
	 		The feeded signal.
	"""

	sequence=octave_transpose(sequence,1)
	signal=signal_mix(signal,play_midi_sequence(sequence,wav_form,raw_bpm))
	for j in [5,17]:
		sequence=tone_transpose(sequence,j)
		signal=signal_mix(signal,play_midi_sequence(sequence,wav_form,raw_bpm))
	return signal

# signal filtering procedure
def filter(signal,cutoff,reso,mode,order=8):
	"""
		Analogic filter emulation using Butterworth polynom.

		=============== =========== =====================================
		**Parameters**   **Type**    **Description**
		*signal*         Float list  The signal to filter
		*cutoff*         Float       The cutoff point as a float
		*reso*           Float       The filter resonnacne as a float
		*mode*           int  		 Filter type is given by mode :
										1 => low pass profile
										2 => bandpass profile
										3 => notch profile
										4 => highpass profile
										5 => feedback comb profile       
		*order*          int         The order of the polynom to compute.
		=============== =========== =====================================

		Returns
		-------
			Float list
			The filtered signal.

	"""
		# FFT filtering init if needed

		# list signal, int mode
		# fft_sif=[]
		# fft_sig=np.fft.fft(signal)
		# filter_=[0]*len(fft_sig)
		# fft_sig*=filter_
		# return np.ifft(fft_sig)

	omega=2*np.pi*cutoff # Filter pulsation
	epsilon=75 			 # arbitrary in Hz (should be replaced by a slope function)

	if mode==2 :   # band pass 
		fa_m=cutoff-2*epsilon
		fa_p=cutoff+2*epsilon
		fp_m=cutoff-epsilon
		fp_p=cutoff+epsilon
	elif mode==3 : # notch
		fa_m=cutoff-epsilon
		fa_p=cutoff+epsilon
		fp_m=cutoff-2*epsilon
		fp_p=cutoff+2*epsilon

	B=(fp_p-fp_m)/cutoff

	if mode==1:
		# low pass profile

			# bessel filtering as an example
			# bess_0=bessel_polynomial(0)
			# for i in range(0,len(signal)):
			# 	res.append(bess_0/bessel_polynomial(signal[i]/cutoff))

		G_0=1
		for i in range(0,len(signal)):
			res.append(G_0/butterworth_polynomial(order,signal[i]/cutoff))
	elif mode==2:
		# bandpass profile
		tmp_sig=[]
		for i in range(0,len(signal)):
			tmp_sig.append(1/B*(signal[i]+(1/signal[i])))
		res=filter(tmp_sig,cutoff,reso,1)		
	elif mode==3:
		# notch profile
		tmp_sig=[]
		for i in range(0,len(signal)):
			tmp_sig.append(B*(1/(signal[i]+(1/signal[i]))))
		res=filter(tmp_sig,cutoff,reso,1)
	elif mode==4:
		# highpass profile
		tmp_sig=[]
		for i in range(0,len(signal)):
			tmp_sig.append(1/signal[i])
		res=filter(tmp_sig,cutoff,reso,1)
	elif mode==5:
		# comb profile
		for i in range(0,len(signal)):
			# res.append(signal[i]+reso*signal[i-cutoff])
			res.append(1/np.sqrt((1+reso*reso)-2*reso*np.cos(2*np.pi*t*cutoff)))
	return res

def lfo_generator(rate,amp,offset,t):
	"""
		Low Frequency Oscillator Emulation.
		Return a low frequency sine ruled by rate period, amp)litude and offset .

		=============== ========== ====================================================================
		**Parameters**   **Type**   **Description**
		*rate*           Float      The rate of the generted sine in Hz.
		*amp*            Float      The amplitude of the generated sine
		*offset*         Float      The offset point value
		*t*              Int        The t time, t in z (where z represent the full length of the loop)
		=============== ========== ====================================================================

		Returns
		-------
			Float
			The t'computed value.

	"""
	if(rate<=50):
		return amp*np.cos(2*np.pi*rate*t)+offset

#################################
####### Testing procedure #######
#################################
		
# signal init
signal=[0]*66150*16

# raw midi sequences
frere_jaques=[24,26,28,24,
				24,26,28,24,
					28,29,31,0,
						28,29,31,0]
frere_jaques2=[31,33,31,29,
				28,0,24,0,
					31,33,31,29,
						28,0,24,0]
frere_jaques3=[24,19,24,0,
				24,19,24,0,
					0,0,0,0,
						0,0,0,0]
frere_jaques_final = [24,26,28,24,
				24,26,28,24,
					28,29,31,0,
						28,29,31,0,
							31,33,31,29,	
								28,0,24,0,
									31,33,31,29,
										28,0,24,0,
											24,19,24,0,
												24,19,24,0,
													0,0,0,0,
														0,0,0,0]

test_bass = [24,23,24,0,
				19,0,0,21,
					24,33,0,31,
						24,19,0,0,
							24,23,24,0,
								19,0,0,23,
									28,33,0,31,
										24,28,0,0]

# bpm=int(sys.argv[1])         #clock period in bpm
# raw_bpm=int(44100/(bpm/60))  #same clock converted in Hz

# wav_form=input("sin, tri ou squ ? <string>")
# octave=int(input("hauteur octave ? <int>"))
# if(octave>=-2 and octave <=8):
# 	octave_transpose(frere_jaques,octave)
# 	octave_transpose(frere_jaques2,octave)
# 	octave_transpose(frere_jaques3,octave)
# signal=play_midi_sequence(frere_jaques,wav_form,raw_bpm)
# signal+=play_midi_sequence(frere_jaques2,wav_form,raw_bpm)
# signal+=play_midi_sequence(frere_jaques3,wav_form,raw_bpm)
# scaled=np.int16(signal/np.max(np.abs(signal))*32767)
# write('test.wav',44100,scaled)
# signal = make_harmonics(signal,wav_form,frere_jaques_final,raw_bpm)
# # write signal into wav file (real sound here :) )
# scaled=np.int16(signal/np.max(np.abs(signal))*32767)
# write('test_harmonics.wav',44100,scaled)
# signal=play_midi_sequence(test_bass,wav_form,raw_bpm)
# signal=make_harmonics(signal,wav_form,test_bass,raw_bpm)
# scaled=np.int16(signal/np.max(np.abs(signal))*32767)
# write('test_bass.wav',44100,scaled)

# # Trace utils
# for i in range(0,127):
# 	print(" midi : " + str(i) + " | freq : " + str(midi_to_freq(i)))


# 44100/s
# 2/s 
# raw_bpm <=> 1bpm /120bpmn
#       <=> x bpm/60*44100
