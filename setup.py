# Setup file for creating whl file
# Will upload whl file to DataBricks and we'll use it as library
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyot",
    version="0.0.1",
    author="Masayuki Ota",
    author_email="masota@microsoft.com",
    description="A small example package for DataBricks dataops",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NT-D/streaming-dataops",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)