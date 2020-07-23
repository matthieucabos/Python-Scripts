from cmatrix import *
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

__author__="CABOS Matthieu"
__date__=21_07_2020

# Algorithm Initialization
imgPIL=Image.open("zolie.png")
img=np.array(imgPIL)
test=[]
size_r=img.shape[0]
size_c=img.shape[1]

# Getting the max of size to draw square matrix (factorisables)
if(size_r>size_c): 
	init_r=size_r
	init_c=size_r
else:
	init_r=size_c
	init_c=size_c

img2=np.zeros((init_r,init_c,4), dtype=np.uint8)

# Initializing Matrix
mRed=Matrix(init_r,init_c)
mBlue=Matrix(init_r,init_c)
mGreen=Matrix(init_r,init_c)
mAlpha=Matrix(init_r,init_c)

# Getting RGBA Pix values Matrix
for i in range(size_r):
	for j in range(size_c):
		try:
			mRed[i,j]=float(img[i,j][0])
			mBlue[i,j]=float(img[i,j][1])
			mGreen[i,j]=float(img[i,j][2])
			mAlpha[i,j]=float(img[i,j][3])
		except:
			mRed[i,j]=float(0)
			mBlue[i,j]=float(0)
			mGreen[i,j]=float(0)
			mAlpha[i,j]=float(0)

# Crypting matrix using LU factorization
LR,UR=mRed.LU()
LB,UB=mBlue.LU()
LG,UG=mGreen.LU()
LA,UA=mAlpha.LU()

# Crypting Result as the sum of L,U matrix
CR_R=LR+UR   # Crypted image data as RGB+Alpha Matrix
CR_B=LB+UB
CR_G=LG+UG
CR_A=LA+UA

# Decrytping matrix multiplying Upper and Lower restored
DeCrR=CR_R.triangle(1)*CR_R.triangle(0)
DeCrB=CR_B.triangle(1)*CR_B.triangle(0)
DeCrG=CR_G.triangle(1)*CR_G.triangle(0)
DeCrA=CR_A.triangle(1)*CR_A.triangle(0)

# Drawing the .png results 
for i in range(init_r):
	for j in range(init_c):
		img2[i,j]=np.array(int(DeCrR[i,j]),int(DeCrB[i,j]),int(DeCrG[i,j]),int(DeCr[i,j]))
		crypted[i,j]=np.array(int(CR_R[i,j]),int(CR_B[i,j]),int(CR_G[i,j]),int(CR_A[i,j]))

# Show results (img is the original content, crypted is the crypted content and img2 is the restored content)
plt.imshow(img)
plt.show()

plt.imshow(crypted)
plt.show()

plt.imshow(img2)
plt.show()