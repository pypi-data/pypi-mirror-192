from setuptools import setup

setup(name='magic_key',
      version='0.1',
      description='This module provides iPython integration and magics that allow exact, inexact and intellegent code execution.',
      url='https://gitlab.com/mcaledonensis/magic-key',
      author='Merlinus Caledonensis',
      author_email='merlin@roundtable.game',
      license='Apache 2.0',
      packages=['magic_key'],
      package_data={'': ['prompt.txt']},
      include_package_data=True,
      zip_safe=False)
