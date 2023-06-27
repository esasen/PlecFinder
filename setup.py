from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

compile_args = ['-g', '-std=c++21', '-stdlib=libc++']
cmdclass = {}
ext_modules = []

cmdclass.update({'build_ext': build_ext})
ext_modules+=cythonize([Extension("plecfinder.PyLk.pylk._writhemap_cython", ["plecfinder/PyLk/pylk/_writhemap_cython.pyx"], include_dirs=[numpy.get_include()])])


# ~ ext_modules+=cythonize("pylk/cythonWM.pyx"),include_dirs=[numpy.get_include()]
# ~ compile_args = ['-g', '-std=c++17', '-stdlib=libc++']

setup(  name='PlecFinder',
        version='0.0.1',
        description='A package to calculate the topology of a given configuration.',
        url='https://github.com/esasen/PlecFinder',
        author='Enrico Skoruppa',
        author_email='enrico.skoruppa@gmail.com',
        license='MIT',
        package_dir =   {
                            'plecfinder':           'plecfinder',
                            'plecfinder.iopolymc':  'plecfinder/iopolymc',
                            'plecfinder.pylk':      'plecfinder/PyLk/pylk'
                        },
        packages=['plecfinder','plecfinder.pylk','plecfinder.iopolymc'],
        include_package_data=True,
        package_data={'': ['examples/*.state']},
        install_requires=[
            'numpy',
            'numba',
            'cython',
            'scipy'
            ],
        zip_safe=False,
        ext_modules=ext_modules,
        cmdclass=cmdclass,
        compile_args=compile_args
        )

