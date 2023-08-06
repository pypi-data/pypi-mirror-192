
from setuptools import setup, Extension

sqrt = Extension('quake_inverse_sq._sqrt', sources=['quake_inverse_sq/_sqrt.c'])

setup(
    name="quake-inverse-squareroot",
    version="0.0.3",
    description="A Python port from Quake 3's fast inverse square root algorithm",
    ext_modules=[sqrt],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/timelessnesses/quake-inverse-squareroot',
    packages=['quake_inverse_sq']
)