from distutils.core import setup
from Cython.Build import cythonize

setup(
	name="vec_lib_3d",
	ext_modules=cythonize("algebra_3D.pyx"),
	)