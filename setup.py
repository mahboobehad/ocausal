# In the name of Allah
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocausal",
    version="0.0.1",
    author_email="mahboobe.haddadi@gmail.com",
    author="mahboobehad",
    description="time frame stream outlier detector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0 only (GPL-3.0-only)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

