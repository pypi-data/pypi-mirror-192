import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cwb", # Replace with your own username
    version="0.0.2",
    author="caeruleum",
    author_email="ceruleanxyz@gmail.com",
    description="mediawiki bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/caeruleum/ceruleanwikibot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)