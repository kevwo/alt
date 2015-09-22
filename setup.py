try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(name='alt',
      version='0.0.1',
      url='https://github.com/kevwo/alt',
      zip_safe=False,
      py_modules=['alt'],
      description='Web API level tests and testrunner',
      author='Kevin Woodmansee',
      license='MIT',
      long_description=long_description,
      install_requires=['requests']
)
