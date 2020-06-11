from setuptools import setup, find_packages


setup(
    name="pyndex",  # Replace with your own username
    version="0.1",
    author="Alessandro Micheli",
    author_email="am1118@imperial.ac.uk",
    description="Pyndex: A python package for Russell index reconstruction.",
    url="https://github.com/alemicheli/pyndex",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
