from setuptools import setup

setup(
    name='binstruct',
    version='1.0.1',
    description='Library for read/write access of binary data via structures',
    long_description=open("README.rst", "r").read(),
    py_modules=['binstruct'],
    author='Silvan Wegmann',
    author_email='binstruct@narf.ch',
    url='https://github.com/Jokymon/binstruct',
    license='GNU GPL v3',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
