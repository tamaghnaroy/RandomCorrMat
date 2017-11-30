from codecs import open
from os import path
import os
from sys import version
from setuptools import setup

def convert_md_to_rst(source, destination=None):
    """
    Try to convert the source, an .md (markdown) file, to an .rst (reStructuredText) file at the destination.
    If the destination isn't provided, it defaults to be the same as the source path except for the
    filename extension. If the destination file already exists, it will be overwritten.
    In the event of an error, the destination file will be left untouched.
    """

    # Doing this in the function instead of the module level ensures the
    # error occurs when the function is called, rather than when the module
    # is evaluated.
    try:
        import pypandoc
    except ImportError:
        # Don't give up right away; first try to install the python module.
        os.system("pip install pypandoc")
        import pypandoc

    # Set our destination path to a default, if necessary
    destination = destination or (os.path.splitext(source)[0] + '.rst')

    try:
        # Try to convert the file.
        pypandoc.convert(
            source,
            'rst',
            format='md',
            outputfile=destination
        )
    except:
        # If for any reason the conversion fails, try to put things back
        # like we found them.
        if os.path.isfile(destination):
            os.remove(destination)
        raise

# I use separate conversion from md file to a rst file for pypi to have a more control on what
# I put on the pypi page vs. what is displayed on the Github page. So, I use this is create the initial .rst from the .md
# file and then tweak the rst file manually before uploading to PyPi
here = path.abspath(path.dirname(__file__))
readme_md = path.join(here, 'README.md')
description_rst = path.join(here, 'description.rst')

description = 'Package containing multiple methods to simulate random correlation matrices'
long_description = description

if path.isfile(readme_md) :
    if not path.isfile(description_rst):
        convert_md_to_rst(readme_md, description_rst)

    with open(path.join(here, 'description.rst'), encoding='utf-8') as f:
        long_description = f.read()


setup(name='RandomCorrMat',
      version='0.1.4',
      description=description,
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
                   'Topic :: Scientific/Engineering :: Mathematics'],
      keywords='applied-mathematics correlation-matrices simulation correlation-matrix-simulation',
      zip_safe=False)