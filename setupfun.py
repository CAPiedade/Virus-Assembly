from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'SymmetryClassGroupsFunction',
  ext_modules=[
    Extension('c_symmetryfun', ['c_symmetryfun.pyx'])
    ],
  cmdclass = {'build_ext': build_ext}
)