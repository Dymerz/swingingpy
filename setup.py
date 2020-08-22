import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swingingpy",
    version="0.0.1",
    author="Urbain Corentin",
    author_email="corentin.urbain.pro@gmail.com",
    description="Perform SwinigDoor algorithm for real-time data.",
    long_description=long_description,
    url="https://github.com/Dymerz/swingingpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
