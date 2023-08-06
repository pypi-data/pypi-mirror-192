import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nse-data-reader',
    packages=['nsepy', 'nsepy.derivatives', 'nsepy.debt'],
    version='1.0',
    description='Library to download financial data in pandas dataframe',
    author='Akash',
    author_email='akashmitra@gmail.com',
    url='https://github.com/akash-mitra/nsepy',
    entry_points='''
    [console_scripts]
    nsecli=nsepy.cli:cli
  ''',
    install_requires=['beautifulsoup4', 'requests', 'numpy', 'pandas', 'six', 'click', 'lxml', 'simpledbf'],
    keywords=['NIFTY', 'NSE', 'Stock Price'],
    classifiers=[],
)

# python setup.py sdist bdist_wheel
# pip install -e .
# twine upload --repository testpypi dist/*
# twine upload dist/*
