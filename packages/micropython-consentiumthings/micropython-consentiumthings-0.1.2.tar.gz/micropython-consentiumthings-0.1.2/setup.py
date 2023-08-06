import sys
sys.path.pop(0)
from setuptools import setup

from codecs import open
from os import path

cwd = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(cwd, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="micropython-consentiumthings",
    py_modules=["ConsentiumThings"],
    version="0.1.2",
    description="MicroPython IoT lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="IoT, micropython",
    url="https://github.com/ConsentiumInc/micropython-consentiumthings",
    author="Debjyoti Chowdhury",
    author_email="consentium.inc@gmail.com",
    maintainer="Debjyoti Chowdhury",
    maintainer_email="consentium.inc@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
    ],
)
