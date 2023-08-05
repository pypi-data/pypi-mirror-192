from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='matematykab',
  version='1.0.2',
  description='This is simple library for informatik lessons.',
  long_description=open('README.rst').read(),
  url='',  
  author='Mocusiek',
  author_email='testomail123321@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='matematykab',
  packages=find_packages(),
  install_requires=[] 
)