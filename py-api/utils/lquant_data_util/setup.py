from setuptools import setup

setup(name = 'lquant_data_util',
      version = '0.1',
      description = 'Utilities functions for factors and gics',
      author = 'Kartik Arora',
      author_email = 'karora@wolferesearch.com',
      license = 'Proprietary',
      packages = ['lquant_data_util'],
      zip_safe = False, requires=['pandas','lquantPy'])
