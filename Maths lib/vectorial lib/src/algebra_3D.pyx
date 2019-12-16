import numpy as np
import Complex as c


__author__="CABOS Matthieu"
__date__=31_05_2018

cdef class Point():
    cdef double X 
    cdef double Y
    cdef double Z
    """
        The point object to compute 2 dimensions geometric interaction.

        =============== ==========
        **Attributes**   **Type**
        *x*               float
        *y*               float
        =============== ==========
    """

    cpdef void init(self,double x=0.0,double y=0.0,double z=0.0):
        self.X=x
        self.Y=y
        self.Z=z

        # getters and setters
    cpdef set_x(self,double x):
        self.X=x
    cpdef set_y(self,double y):
        self.Y=y
    cpdef set_z(self,double z):
        self.Z=z
    cpdef double x(self):
        return self.X
    cpdef double y(self):
        return self.Y
    cpdef double z(self):
        return self.Z

        # basic operators redefinition
    cpdef Point op(self,Point B,str op):
        """
            Operator redefinition for the class Point.

            =============== ========== ===============================
            **Parameters**   **Type**   **Description**
            *B*              Point     The second member as a Point
            *op*             string      the operator to execute
            =============== ========== ===============================

            Returns
            -------
            Point
                The computed point operation
        """
        if op=='+':
            return Point(self.x()+B.x(),self.y()+B.y(),self.z()+B.z())
        elif op=='-':
            return Point(self.x()-B.x(),self.y()-B.y(),self.z()-B.z())

    def __add__(self,p):
        return self.op(p,'+')

    def __sub__(self,p):
        return self.op(p,'-')

        # Utility

    cpdef void print_screen(self):
        print(" ( "+str(self.x())+" , "+str(self.y())+" , "+str(self.z())+" ) ")

    cpdef Point copy(self):
        return Point(self.x(),self.y(),self.z())


cdef class Vector():
    """
        The vector object to compute 2 dimensions vectorial operations.
        =============== ==========
        **Attributes**   **Type**
        *x*               Point
        *y*               Point
        =============== ==========
    """
    cdef:
        Point x
        Point y
        double angle

    def __init__(self,arg):
        if(len(arg)==6):
            self.x=Point(arg[0],arg[1],arg[2])
            self.y=Point(arg[3],arg[4],arg[5])
        else:
            self.x=arg[0]
            self.y=arg[1]

    # getters and setters
    cpdef void setPoints(self,x,y):
        self.setP1(x)
        self.setP2(y)
    cpdef void setP1(self,x):
        self.x=x
    cpdef void setP2(self,y):
        self.y=y
    cpdef Point p1(self):
        return self.x
    cpdef Point p2(self):
        return self.y
    cpdef double x1(self):
        return self.x.x()
    cpdef double x2(self):
        return self.y.x()
    cpdef double y1(self):
        return self.x.y()
    cpdef double y2(self):
        return self.y.y()
    cpdef double z1(self):
        return self.x.z()
    cpdef double z2(self):
        return self.y.z()
    cpdef double angle(self):
        return self.angle
    cpdef double vect(self):
        res=(self.x2()-self.x1(),self.y2()-self.x1(),self.z2()-self.x1())
        return res


        # basic operators redefinition
    cpdef Vector op(self,Vector B,str op):
        """
            Operator redefinition for the class Point.

            =============== ========== ================================
            **Parameters**   **Type**   **Description**
            *B*              Vector     The second member as a Vector
            *op*             string      the operator to execute
            =============== ========== ================================

            Returns
            -------
            Vector
                The computed vector operation
        """
        if op=='+':
            return Vector(self.p1().x()+B.p1().x(),self.p1().y()+B.p1().y(),self.p1().z()+B.p1().z(),
                           self.p2().x()+B.p2().x(),self.p2().y()+B.p2().y(),self.p2().z()+B.p2().z())
        elif op=='-':
            return Vector(self.p1().x()-B.p1().x(),self.p1().y()-B.p1().y(),self.p1().z()-B.p1().z(),
                           self.p2().x()-B.p2().x(),self.p2().y()-B.p2().y(),self.p2().z()-B.p2().z())
        elif op=='*':
            if(isinstance(B,Point)):
                return Vector(self.p1().x()*B.p1().x(),self.p1().y()*B.p1().y(),self.p1().z()*B.p1().z(),
                               self.p2().x()*B.p2().x(),self.p2().y()*B.p2().y(),self.p2().z()*B.p2().z())
            else:
                return Vector(self.p1().x()*B,self.p1().y()*B,self.p1().z()*B,
                               self.p2().x()*B,self.p2().y()*B,self.p2().z()*B)

    def __add__(self,vec):
        return self.op(vec,'+')

    def __sub__(self,vec):
        return self.op(vec,'-')

    def __mul__(self,coef):
        return self.op(coef,'*')

        #Specific operators definition

    cpdef Vector vectorize(self):
        """
            Vectorize self vector by setting first point at origin.

            Returns
            -------
            Vector
                The vectorized vector
        """
        return Vector(0,0,0,self.p2().x()-self.p1().x(),self.p2().y()-self.p1().y(),self.p2().z()-self.p1().z())

    cpdef double prod(self,vec):
        """
            Cross product self and vec.

            Returns
            -------
            double
                The prod result         
        """
        cdef Vector v1=self.vectorize()
        cdef Vector v2=vec.vectorize()
        return (v1.p2().y()*v2.p2().z()-v1.p2().z()*v2.p2().y()) + (v1.p2().z()*v2.p2().x()-v1.p2().x()*v2.p2().z()) + (v1.p2().x()*v2.p2().y()-v1.p2().y()*v2.p2().x())

    cpdef double dot(self,vec):
        """
            Dot product self and vec.

            Returns
            -------
            double
                The dot result  
        """
        cdef:
            Vector v1=self.vectorize()
            Vector v2=vec.vectorize()
        return v1.p2().x()*v2.p2().x()+v1.p2().y()*v2.p2().y()+v1.p2().z()*v2.p2().z()

    cpdef double length(self):
        """ 
            Get the norm of self vector.

            Returns
            -------
            float
                The euclidian length of the vector
        """
        cdef double res
        res=((self.dot(self)))**(1/2)
        return res

    # cpdef normalVector(self):
    #     #normalize self vector
    #     cdef Vector vec=self.vectorize()
    #     return Vector(0,0,-vec.p2().y(),vec.p2().x())

    cpdef void translate(self,point=Point(0,0)):
        """
            Translate self vector to the given Point.

            =============== ========== ===================================
            **Parameters**   **Type**   **Description**
            *point*          Point    The translation destination point
            =============== ========== ===================================
        """
        vect=self.vectorize()
        self=self+Vector(point.x(),point.y(),point.z(),vect.x2()+point.x(),vect.y2()+point.y(),vect.z2()+point.z())

    cpdef double unitVector(self):
        """
            Get unit vector from self.
        """
        return self*(1/self.length())

    # cpdef normalVector_not_vectorized(self):
    #     #normalize self vector WITHOUT vectorizing (in fact vectorized and "unvectorized")
    #     cdef Vector vec=self.vectorize()
    #     return Vector(0,0,-vec.p2().y(),vec.p2().x()).translate(self.p1())

        #Utility

    cpdef void print_screen(self):
        print(" ( "+str(self.p2().x()-self.p1().x())+" , "+str(self.p2().y()-self.p1().y())+" , "+str(self.p2().z()-self.p1().z())+" ) ")

    cpdef Vector copy(self):
        return Vector(self.p1().x(),self.p1().y(),self.p1().z(),self.p2().x(),self.p2().y(),self.p2().z())

    cpdef Point pointAt(self,t):
        """
            Get the point result after a translation by self vector, scaling by t.

            =============== ========== ====================================
            **Parameters**   **Type**   **Description**
            *t*              double     The scale range of the translation
            =============== ========== ====================================

            Returns
            -------
            Point
                The translated point.
        """
        cdef:
            double interval_x
            double interval_y
            double interval_z

        interval_x=self.p2().x()-self.p1().x()
        interval_y=self.p2().y()-self.p1().y()
        interval_z=self.p2().z()-self.p1().z()
        x=self.p1().x()+t*interval_x
        y=self.p1().y()+t*interval_y
        z=self.p1().z()+t*interval_z
        return Point(x,y,z)

    cpdef void setLength(self,length,precision=6):
        """
            Change the length of the vector without lambda-multiplication.
            (you can define a precise length).

            =============== ========== =====================================
            **Parameters**   **Type**   **Description**
            *length*         double     The new length of the selff vector
            =============== ========== =====================================
        """
        cdef double interp

        interp=1/10**precision
        if (self.length()>length):
            while (self.length()>length):
                if(self.length()-length>0.01): 
                    self.setP2(Point(self.x2()-interp*1000,self.y2()-interp*1000,self.z2()-interp*1000))
                elif(self.length()-length>0.0001):
                    self.setP2(Point(self.x2()-interp*10,self.y2()-interp*10,self.z2()-interp*10))
                else:
                    self.setP2(Point(self.x2()-interp,self.y2()-interp,self.z2()-interp))
        else:
            while (self.length()<length):
                if(length-self.length()>0.01):
                    self.setP2(Point(self.x2()+interp*1000,self.y2()+interp*1000,self.z2()+interp*1000))
                elif(length-self.length()>0.0001):
                    self.setP2(Point(self.x2()+interp*10,self.y2()+interp*10,self.z2()+interp*10))
                else:
                    self.setP2(Point(self.x2()+interp,self.y2()+interp,self.z2()+interp))

    cpdef int hortogo(self,vec):
        """
            Test the hortogonal proprieties of self vector and given vec.

            =============== ========== ==============================
            **Parameters**   **Type**   **Description**
            *vec*             Vector   The vector to test with self
            =============== ========== ==============================

            Returns
            -------
            int
                * 0 : Vectors are not hortgonal
                * 1 : Vectors are hortogonal
        """
        return(self.dot(vec)==0)

    cpdef double cos(self,vec):
        """
            Get a fast computed cos from self vector and vec vector.
            The operation is realized if and only if the two vectors have the same origin.

            =============== ========== ===========================================
            **Parameters**   **Type**   **Description**
            *vec*            Vector    The vector angle-oriented with self vector
            =============== ========== ===========================================

            Returns
            -------
            double
                The computed cosine.
        """
        if not ((self.p1().x()==vec.p1().x()) and (self.p1().y()==vec.p1().y()) and (self.p1().z()==vec.p1().z())):
            v1=self.vectorize()
            v2=vec.vectorize()
        return(self.dot(vec)/self.prod(vec))

    cpdef double angle_vec(self,vec):
        """
            Get the angle between two vectors.
            The operation is realized if and only if the two vectors have the same origin.

            =============== ========== ===========================================
            **Parameters**   **Type**   **Description**
            *vec*            Vector    The vector angle-oriented with self vector
            =============== ========== ===========================================

            Returns
            -------
            double
                The angle between the two vectors.
        """
        return np.arccos(self.cos(vec))

    @staticmethod
    def fromPolar(angle,length=1):
        # Return the vector from angle, unit vector as default
        return Vector(0,0,length+np.cos(angle),length+np.sin(angle))

cdef class Vector_field():
    """
        =============== ============
        **Attributes**   **type**
        *vec*            Vect list
        *pts*            Point list
        *size*           int
        =============== ============
    """
    cdef:
        list vec
        list pts
        int size

    vec=[]
    pts=[]
    size=0

    def __init__(self,vec,pts):
        if(len(vec)==len(pts)):
            for item in vec:
                self.vec.append(item)
                self.size+=1
            for item in pts:
                self.pts.append(item)

    cpdef list get_vec(self):
        return self.vec
    cpdef list get_pts(self):
        return self.pts
    cpdef int get_size(self):
        return self.size

    cpdef Vector_field op(self,Vector_field field,str op):
        if op=='+':
            if(self.get_size()==field.get_size()):
                vec=[]
                for item,item2 in self.get_vec(),field.get_vec():
                    vec.append(item+item2)
                return Vector_field(vec,self.pts)
        elif op=='-':
            if(self.get_size()==field.get_size()):
                vec=[]
                for item,item2 in self.get_vec(),field.get_vec():
                    vec.append(item-item2)
                return Vector_field(vec,self.pts)
        elif op=='*':
            if(isinstance(field,int) or isinstance(field,float)):
                vec=[]
                for item in self.get_vec():
                    vec.append(field*item)
                return Vector_field(vec,self.pts)
        elif op=='/':
            pass
            # no_way()

    def __add__(self,vec_f):
        return self.op(vec_f,'+')
    def __sub__(self,vec_f):
        return self.op(vec_f,'-')
    def __mul__(self,coef):
        return self.op(coef,'*')

    # def mean(self,):

    # def interpolation(self,Vector_field to_interpolate):

    cpdef void extend_field(self,list to_add):
        for item in to_add:
            self.vec.append(item)
            self.size+=1

    cpdef void print_screen(self):
        cdef int ind
        ind=0
        for item in self.get_vec():
            print("element ["+str(ind)+"] : ")
            item.print_screen()
            self.pts[ind].print_screen()
            ind+=1

    @staticmethod
    def radial_field(order,origine=Point(0,0,0)):
        # Generate the radial vector field from given order as an integer and the origine point O as default.
        res=[]
        angle=0
        alpha=(2*np.pi/order)
        for i in range(0,order):
            # res.append(fromPolar(np.arccos(c.unit_root_n(i).a())))
            angle+=alpha
            res.append(Vector.fromPolar(angle))
        return Vector_field(res,origine)
