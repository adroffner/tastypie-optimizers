#! /usr/bin/env python
#
# Tastypie Optimizers
# ======================================================================
try:
    # Allow Python eggs bdist_egg
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from tastypie_optimizers import __version__

readme = open('README.md', 'r')
README_TEXT = readme.read()
readme.close()

setup(name='django-tastypie-optimizers',
      version=__version__,
      license='MIT Licensed',
      description='Tastypie Optimizer for ModelResource requests',
      long_description=README_TEXT,
      author='Andrew Droffner',
      author_email='adroffner@gmail.com',
      url='https://github.com/adroffner/tastypie-optimizers',
      download_url='',
      packages=['tastypie_optimizers', ],
      ## scripts=[''],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          ],
     )


