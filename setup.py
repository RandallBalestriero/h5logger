__author__ = "Randall Balestriero"


import setuptools
import versioneer
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h5logger",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Randall Balestriero",
    author_email="randallbalestriero@gmail.com",
    description="h5 logger in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["examples"]),
    url="https://github.com/RandallBalestriero/h5logger",
    project_urls={
        "Bug Tracker": "https://github.com/RandallBalestriero/h5logger/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "h5logger"},
    python_requires=">=3.6",
    install_requires=["h5py", "numpy"],
)
