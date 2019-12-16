from distutils.core import setup
from Cython.Build import cythonize

setup(
	name="algebra",
	ext_modules=cythonize("algebra.pyx"),
	)