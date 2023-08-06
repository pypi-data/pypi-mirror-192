import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meny",
    version="1.1.1",
    author="Naphat Amundsen",
    author_email="naphat@live.com",
    description="Simple and sexy console interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Napam/meny",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "meny=meny.cli:cli"
        ]
    },
    python_requires=">=3.7",
)
