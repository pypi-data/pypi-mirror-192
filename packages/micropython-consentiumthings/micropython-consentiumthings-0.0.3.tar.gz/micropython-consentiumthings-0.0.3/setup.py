__version__ = "0.0.3"

from setuptools import setup, find_packages


def long_description():
    with open("README.md", "r") as fo:
        return fo.read()


setup(
    name="micropython-consentiumthings",
    version=__version__,
    url="https://github.com/ConsentiumInc/micropython-consentiumthings",
    description="A MicroPython library for send sensor data to ConsentiumThings IoT server",
    keywords=["micropython", "IoT"],
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=['ConsentiumThings'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
    ],
)