from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'Basic Bayesian Network library'
LONG_DESCRIPTION = 'Basic Bayesian Network library'

# Setting up
setup(
    name="JBayesLibPy20009",
    version=VERSION,
    author="Jorge Caballeros",
    author_email="cab20009@uvg.edu.gt",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream',
              'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
