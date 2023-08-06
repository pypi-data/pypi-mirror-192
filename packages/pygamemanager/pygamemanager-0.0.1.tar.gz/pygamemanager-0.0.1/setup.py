from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'A package that makes pygame easy'
LONG_DESCRIPTION = 'A package that makes pygame really easy so that it is split up into a easier way to manage'


# Setting up
setup(
    name="pygamemanager",
    version=VERSION,
    author="Jack",
    author_email="<notsharing@currently.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'pygame', 'simple', 'easy', 'manageable'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)