#!/usr/bin/env python

from distutils.core import setup

setup(name='afia',
      version='0.1',
      description='Another Foucault Image Anaylzer',
      author='Alexander Ulbrich',
      author_email='alex.ulbrich.ulm@gmail.com',
      install_requires=[
            'numpy',
            'opencv-python', 
            'tk', 
            'matplotlib'],
      scripts=['bin/afia'],
     )