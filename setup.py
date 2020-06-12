from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="pyndex",  
    version="0.1",
    author="Alessandro Micheli",
    author_email="am1118@imperial.ac.uk",
    description="Pyndex: A python package for Russell index reconstruction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alemicheli/pyndex",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
