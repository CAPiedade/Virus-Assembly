from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'SymmetryClassGroups',
  ext_modules=[
    Extension('c_symmetry', ['c_symmetry.pyx'])
    ],
  cmdclass = {'build_ext': build_ext}
)
