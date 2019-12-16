def sgn(x):
	return x/np.abs(x)

# TO TEST
class Equation:
	coef=[]
	solution=[]

	def __init__(self,*coeff):
		for c in coef:
			self.coef.append(c)
			self.order+=1

	def get_delta(self):
		if self.order==2:
			self.delta=self.coef[1]**2-4*coef[0]*coef[2]
		elif self.order==3:
			self.a0=coef[3]/coef[0]
			self.a1=coef[2]/coef[0]
			self.a2=coef[1]/coef[0]
			self.a3=a2/coef[0]
			self.p=a1-a2*a3
			self.q=a0-a1*a3+2*(a3**3)
			self.delta=(q/2)**2+(p/3)**3
		elif self.order==4:
			self.z=self.coef[1]/2*self.coef[0]
			self.A=(self.coef[2]/self.coef[0])-(3*self.z**2)/2
			self.B=self.coef[3]/self.coef[0]+self.z**3-(self.coef[2]*self.z/self.coef[0])
			self.C=(self.coef[4]/self.coef[0])-3*(self.z/2)**4+(self.coef[2]/self.coef[0])*(self.z/2)**2-(self.coef[3]/self.coef[0])*(z/2)
			self.D=-2*(self.A/3)**3-self.B**2+8/3*self.A*self.C
			self.E=(-(self.A**2)/3)-4*self.C
			self.delta=(self.E/3)**3+(self.D/2)**2
		else: pass

	def solve(self):
		self.get_delta()
		if self.order==2 :
			if self.delta>0:
				self.solution.append((-self.coef[1]+np.sqrt(self.delta))/2*coef[0])
				self.solution.append((-self.coef[1]-np.sqrt(self.delta))/2*coef[0])
				self.solution.append("real")
			elif self.delta==0:
				self.solution.append(-self.coef[1]/2*coef[0])
				self.solution.append("real")
			elif self.delat<0:
				self.solution.append(-self.coef[1]/2*self.coef[0],np.sqrt(self.delta)/2*coef[0])
				self.solution.append(-self.coef[1]/2*self.coef[0],-np.sqrt(self.delta)/2*coef[0])
				self.solution.append("complex")
		elif self.order==3:
			if self.delta>0:
				w=((-self.q/2)+np.sqrt(self.delta))**(1/3)
				self.solution.append(w-(self.p/3*w)-a3)
				self.solution.append(((-a2+self.solution[0])/2),(np.sqrt(3)/2)*(w+(self.p/3*w)))
				self.solution.append(((-a2+self.solution[0])/2),(-np.sqrt(3)/2)*(w+(self.p/3*w)))
				self.solution.append("complex")
			elif self.delta==0:
				self.solution.append((3*self.q/self.p)-self.a3)
				self.solution.append((-3*self.q/self.p)-self.a3)
				self.solution.append(self.x2)
				self.solution.append("real")
			elif self.delat<0:
				u=2*np.sqrt(-self.p/3)
				v=-self.q/(2*(-self.p/3)**3/2)
				t=np.arccos(v)/3
				self.solution.append(u*np.cos(t)-self.a3)
				self.solution.append(u*np.cos(t+(2*np.pi/3))-a3)
				self.solution.append(u*np.cos(t+4*np.pi/3)-a3)
				self.solution.append("real")
		elif self.order==4:
			if self.delta>0:
				self.W=((-self.D/2)+np.sqrt(self.delta))**1/3
				self.U=self.W-self.E/3*self.W
			elif self.delta==0:
				self.U=3*(self.D/self.E)
			elif self.delta<0:
				self.U=(2*np.sqrt(-self.E/3))*np.cos(1/3*np.arccos(-self.D/(2*(-self.E/3)**3/2)))
			self.T=(self.A/3)+self.U
			self.R=np.sqrt(self.T-self.A)
			self.S=np.sqrt((self.T/2)-self.C)
			self.deltb=-self.coef[1]/4*self.coef[0]
			self.delta2=(self.R**2)-2*self.T-4*self.S
			if(self.B==0):
				self.p1=-self.R/2
			else:
				self.p1=sgn(self.B)*self.R/2
			self.p2=np.sqrt(np.abs(self.delta2))/2
			if self.delta2>=0:
				self.solution.append(self.p1+self.deltb+self.p2)
				self.solution.append(self.p1+self.deltb-self.p2)
			else:
				self.solution.append(self.p1+self.deltb,self.p2)
				self.solution.append(self.p1+self.deltb,-self.p2)
			self.delta3=self.R**2-2*self.T+4*self.S 
			if self.B==0:
				self.p3=self.R/2
			else:
				self.p3=-sgn(self.B)*self.R/2
			self.p4=np.sqrt(np.abs(self.delta3))/2
			if(self.delta3>=0):
				self.solution.append(self.p3+self.deltb+self.p4)
				self.solution.append(self.p3+self.deltb-self.p4)
				self.solution.append("real")
			else:
				self.solution.append(self.p3+self.deltb,self.p4)
				self.solution.append(self.p3+self.deltb,-self.p4)
				self.solution.append("complex")
		else:

class system:
	cdef list equation

	def __init_(self,equation):
		for eq in equation:
			self.equation.append(eq)

	

