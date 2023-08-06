from setuptools import setup

setup(
   name='tymer',
   version='1.0',
   description='A simple timer',
   author='Morris El Helou',
   author_email='morrishelou@gmail.com',
   include_package_data=True,
   packages=['pythontimer'], 
   package_data={"pythontimer": ["*.ico"]},
   install_requires=[], #external packages as dependencies
)