# This file is only used by tox right now. So the values might not all be
# correct.

from distutils.core import setup

setup(
    name='vimswitch',
    version='0.1-beta',
    description='A utility for switching between vim profiles',
    author='Shafqat Bhuiyan',
    author_email='priomsrb@gmail.com',
    url='https://github.com/priomsrb/vimswitch',
    packages=['vimswitch', 'vimswitch.test'],
    package_data={'vimswitch': ['vimswitch/*'], 'vimswitch.test': ['vimswitch/test/*']}
    #long_description='''Really long text here.'''
    #
    #This next part it for the Cheese Shop
    #classifiers=[]
)
