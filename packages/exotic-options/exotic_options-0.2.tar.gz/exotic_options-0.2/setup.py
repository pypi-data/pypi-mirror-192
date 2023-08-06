from setuptools import setup, find_packages


setup(name='exotic_options',
      version='0.2',
      description='The Formula to calculate some exotic options.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/Tavaresiqueira/exotic_options/',
      download_url = 'https://github.com/Tavaresiqueira/exotic_options/archive/v0.2.tar.gz',
      author='Joao Pedro Tavares',
      author_email='siqueiratav@gmail.com',
      packages=find_packages(),
      install_requires=['numpy', 'scipy'],
      )