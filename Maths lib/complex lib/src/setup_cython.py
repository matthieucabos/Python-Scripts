from distutils.core import setup
from Cython.Build import cythonize

setup(
	name="Complex",
	ext_modules=cythonize("Complex.pyx"),
	)