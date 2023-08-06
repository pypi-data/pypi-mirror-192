from setuptools import find_packages, setup
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="example_andy_project",
    version="0.0.1",
    author="Andy",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)