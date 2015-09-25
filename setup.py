try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README') as file:
    long_description = file.read()

packages = [
    'alt'
]

setup(name='alt',
      version='0.0.3',
      url='https://github.com/kevwo/alt',
      zip_safe=False,
      packages=packages,
      package_data={'alt': ['skeleton/*.*']},
      package_dir={'alt': 'alt'},
      description='Web API level tests and test runner',
      author='Kevin Woodmansee',
      author_email='kevinwoodmansee@gmail.com',
      license='MIT',
      long_description=long_description,
      install_requires=['requests>=2.7.0', 'pyyaml>=3.11', 'ddt>=1.0.0']
)
