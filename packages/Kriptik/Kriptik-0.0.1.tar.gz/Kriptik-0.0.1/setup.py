from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.1"
DESCRIPTION = "A 2D Python game engine"
LONG_DESCRIPTION = "A 2D Python game engine with a reasonably wide range of functionality given it's size."

# Setting up
setup(
    name="Kriptik",
    version=VERSION,
    author="wzack850",
    author_email="<wzack850@yahoo.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pillow", "pygame", "keyboard"],
    keywords=["python", "game engine", "2D", "python 3.x", "kriptik"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)