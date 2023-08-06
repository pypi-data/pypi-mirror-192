from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'sh_bh'
LONG_DESCRIPTION = 'A package to create and delete S3,EC2 and IAM user in AWS'

# Setting up
setup(
    name="sh_bh",
    version=VERSION,
    author="Shubham",
    author_email="shubhambhosale1920@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['AWS', 'S3', 'EC2', 'IAMuser', 'Shubham-bh'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)