import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Nim",
    version="0.1.0",
    author="Christopher Holder",
    author_email="holder@cs.fsu.edu",
    description="Ethereum State Channels for Python and Web3py Wrapper library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="www.projectnim.org",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux Distro",
    ],
)