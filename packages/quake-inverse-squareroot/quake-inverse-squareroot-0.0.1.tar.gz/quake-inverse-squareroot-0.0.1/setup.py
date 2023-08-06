import shutil

shutil.copyfile('src/_sqrt.c', 'sqrt.c')
shutil.copyfile('src/_quake_inverse_sq.pyi', 'quake_inverse_sq.pyi')

from setuptools import setup, Extension

sqrt = Extension('quake_inverse_sq', sources=['sqrt.c'])

setup(
    name="quake-inverse-squareroot",
    version="0.0.1",
    description="A Python port from Quake 3's fast inverse square root algorithm",
    ext_modules=[sqrt],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)