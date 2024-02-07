from setuptools import setup

setup(name = 'pyqes',
      version = '0.1',
      description = 'Wrapper for QLaaS RESTful API',
      author = 'Kartik Arora',
      author_email = 'karora@wolferesearch.com',
      license = 'Proprietary',
      packages = ['pyqes'],
      zip_safe = False, 
      install_requires=['requests','datetime','pandas'])
