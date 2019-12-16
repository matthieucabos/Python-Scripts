import numpy as np


__author__="CABOS Matthieu"
__date__=31_05_2018

cdef class Point():
    cdef double X 
    cdef double Y
    """
        The point object to compute 2 dimensions geometric interaction.

        =============== ==========
        **Attributes**   **Type**
        *x*               float
        *y*               float
        =============== ==========
    """

    def __init__(self,x=0.0,y=0.0):
        self.X=x
        self.Y=y

        # getters and setters
    cpdef set_x(self,x):
        self.X=x
    cpdef set_y(self,y):
        self.Y=y
    cpdef x(self):
        return self.X
    cpdef y(self):
        return self.Y

        # basic operators redefinition
    cpdef op(self,B,op):
        if op=='+':
            return Point(self.x()+B.x(),self.y()+B.y())
        elif op=='-':
            return Point(self.x()-B.x(),self.y()-B.y())

    def __add__(self,p):
        return self.op(p,'+')

    def __sub__(self,p):
        return self.op(p,'-')

        # Utility

    cpdef print_screen(self):
        print(" ( "+str(self.x())+" , "+str(self.y())+" ) ")

    cpdef copy(self):
        return Point(self.x(),self.y())


cdef class Vector():
    """
        The vector object to compute 2 dimensions vectorial operations.
        =============== ==========
        **Attributes**   **Type**
        *x*               Point
        *y*               Point
        =============== ==========
    """

    cdef Point x
    cdef Point y
    cdef double angle

    # def __init__(self,x0,x1,y0,y1):
    def __init__(self,*arg):
        if(len(arg)==4):
            # self.x=Point(x0,x1)
            # self.y=Point(y0,y1)
            self.x=Point(arg[0],arg[1])
            self.y=Point(arg[2],arg[3])
        else:
            self.x=arg[0]
            self.y=arg[1]

    # getters and setters
    cpdef setPoints(self,x,y):
        self.setP1(x)
        self.setP2(y)
    cpdef setP1(self,x):
        self.x=x
    cpdef setP2(self,y):
        self.y=y
    cpdef p1(self):
        return self.x
    cpdef p2(self):
        return self.y
    cpdef x1(self):
        return self.x.x()
    cpdef x2(self):
        return self.y.x()
    cpdef y1(self):
        return self.x.y()
    cpdef y2(self):
        return self.y.y()
    cpdef angle(self):
        return self.angle
    cpdef vect(self):
        res=(self.x1(),self.y1(),self.x2(),self.y2())
        return res


        # basic operators redefinition
    cpdef op(self,B,op):
        if op=='+':
            return Vector(self.p1().x()+B.p1().x(),self.p1().y()+B.p1().y(),self.p2().x()+B.p2().x(),self.p2().y()+B.p2().y())
        elif op=='-':
            return Vector(self.p1().x()-B.p1().x(),self.p1().y()-B.p1().y(),self.p2().x()-B.p2().x(),self.p2().y()-B.p2().y())
        elif op=='*':
            return Vector(B*self.p1().x(),B*self.p1().y(),B*self.p2().x(),B*self.p2().y())

    def __add__(self,vec):
        return self.op(vec,'+')

    def __sub__(self,vec):
        return self.op(vec,'-')

    def __mul__(self,coef):
        return self.op(coef,'*')

        #Specific operators definition

    cpdef vectorize(self):
        #vectorize self vector
        return Vector(0,0,self.p2().x()-self.p1().x(),self.p2().y()-self.p1().y())

    cpdef prod(self,vec):
        #cross product self and vec

        cdef Vector v1=self.vectorize()
        cdef Vector v2=vec.vectorize()
        return v1.p2().x()*v2.p2().y()-v1.p2().y()*v2.p2().x()

    cpdef dot(self,vec):
        #dot product self and vec
        cdef Vector v1=self.vectorize()
        cdef Vector v2=vec.vectorize()
        return v1.p2().x()*v2.p2().x()+v1.p2().y()*v2.p2().y()

    cpdef length(self):
        #get the norm of self vector
        cdef double res
        res=np.sqrt((self.dot(self)))
        return res

    cpdef normalVector(self):
        #normalize self vector
        cdef Vector vec=self.vectorize()
        return Vector(0,0,-vec.p2().y(),vec.p2().x())

    cpdef translate(self,point=Point(0,0)):
        #translate self vector to the given Point
        self=self+Vector(point.x(),point.y(),self.x2()+point.x(),self.y2()+point.y())

    cpdef unitVector(self):
        #get unit vector from self
        return self*(1/self.length())

    cpdef normalVector_not_vectorized(self):
        #normalize self vector WITHOUT vectorizing (in fact vectorized and "unvectorized")
        cdef Vector vec=self.vectorize()
        return Vector(0,0,-vec.p2().y(),vec.p2().x()).translate(self.p1())

        #Utility

    cpdef print_screen(self):
        print(" ( "+str(self.p2().x()-self.p1().x())+" , "+str(self.p2().y()-self.p1().y())+" ) ")

    cpdef copy(self):
        return Vector(self.p1().x(),self.p1().y(),self.p2().x(),self.p2().y())

    cpdef pointAt(self,t):
        interval_x=self.p2().x()-self.p1().x()
        interval_y=self.p2().y()-self.p1().y()
        x=self.p1().x()+t*interval_x
        y=self.p1().y()+t*interval_y
        return Point(x,y)

    cpdef setLength(self,length):
        if (self.length()>length):
            while (self.length()>length):
                self.setP2(Point(self.x2()-0.000001,self.y2()-0.000001))
        else:
            while (self.length()<length):
                self.setP2(Point(self.x2()+0.000001,self.y2()+0.000001))

    @staticmethod
    def fromPolar(length,angle):
        return Vector(0,0,length+np.cos(angle),length+np.sin(angle))
