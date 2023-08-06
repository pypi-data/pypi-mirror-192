from setuptools import setup, find_packages


setup(name='quantitative_vale_model',
      version='0.1',
      description='Simple and profitable quantitative model to user in Brazilian VALE3 (VALE S.A.) Stocks',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/Tavaresiqueira/quantitative_vale_model/',
      download_url = 'https://github.com/Tavaresiqueira/quantitative_vale_model/archive/v0.1.tar.gz',
      author='Joao Pedro Tavares',
      author_email='siqueiratav@gmail.com',
      packages=find_packages(),
      install_requires=['backtrader', 'yfinance', 'pandas', 'datetime'],
      )
