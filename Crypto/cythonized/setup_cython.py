from distutils.core import setup
from Cython.Build import cythonize

setup(
	name="basetestrecursive",
	ext_modules=cythonize("basetestrecursive.pyx"),
	)