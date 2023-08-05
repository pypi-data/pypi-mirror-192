import site
import sys

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]
if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyBIS",
    version="1.35.2",
    author="ID SIS • ETH Zürich",
    author_email="openbis-support@id.ethz.ch",
    description="openBIS connection and interaction, optimized for using with Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sissource.ethz.ch/sispub/openbis/tree/master/pybis",
    packages=find_packages(),
    license="Apache Software License Version 2.0",
    install_requires=[
        "pytest",
        "requests",
        "urllib3",
        "pandas",
        "texttable",
        "tabulate",
        "python-dateutil",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
