from codecs import open
from os import path
from sys import version
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()

setup(name='RandomCorrMat',
      version='0.1',
      description='package containing multiple methods to simulate correlation matrices',
      long_description = long_description,
      url='https://github.com/tamaghnaroy/RandomCorrMat',
      author='Tamaghna Roy',
      author_email='tamaghna@gmail.com',
      license='MIT',
      packages=['RandomCorrMat'],
      install_requires=['numpy'],
      test_suite='nose.collector',
      tests_require=['nose'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Mathematics', ],
      keywords='applied-mathematics correlation-matrices simulation correlation-matrix-simulation',
      zip_safe=False)