from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("cythonWM.pyx"),include_dirs=[numpy.get_include()]
)
compile_args = ['-g', '-std=c++17', '-stdlib=libc++']
