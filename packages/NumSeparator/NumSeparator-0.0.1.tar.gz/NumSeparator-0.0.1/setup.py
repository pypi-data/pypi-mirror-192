from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='NumSeparator',
  version='0.0.1',
  description='100000 ----> 100,000',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Irene Nsengumukiza',
  author_email='irene.study.2023@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='numbers', 
  packages=find_packages(),
  install_requires=[''] 
)
