import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyDiscoDmx",
    version = "0.0.1",
    author = "Tobias Tschech",
    author_email = "tobias@tschech-online.de",
    description = ("A simple DMX Light Controller which only uses Audio as trigger input for starting some effects"),
    license = "GNU",
    keywords = "dmx sound_to_light controller",
    url = "http://packages.python.org/pydiscodmx",
    packages=['pydiscodmx'],
    #data_files={
    #    "pydiscodmx": [ "pyDiscoDmx.dist.ini", "fixtures.dist.json" ]
    #},
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    entry_points={
        'console_scripts': ['pydiscodmx=pydiscodmx.pyDiscoDmx:main']
    }
)
