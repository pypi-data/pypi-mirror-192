# encoding: utf-8
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    desc = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='drunner',
    version='1.1.1',
    author='TimeAshore',
    author_email='timeashore@163.com',
    description='Drunner for everyone',
    long_description=desc,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",

        "License :: OSI Approved :: MIT License",
    ],
    py_modules=['drunner'],
    entry_points={
        'console_scripts': [
            'drunner = drunner:cli',
        ],
    },
    python_requires='>=3.8',
    install_requires=['Click>=8.1.3', 'requests>=2.27.1']
)
