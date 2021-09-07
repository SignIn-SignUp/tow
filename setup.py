import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="tow",
    version=read('VERSION').strip(),
    author="Chacha Mwita",
    description=("A package manager for the generic package registry in GitLab."
                 "Packages can be pushed and pulled with authentication through a personal acess token."),
    keywords="tow gitlab package-manager generic-package-registry generic-packages",
    long_description=read('README.md'),
    packages=['pkg_manager'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'tow=pkg_manager.tow:run',
        ],
    },
)
