import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MMA_SUBREGION_TOOL_pkg1",
    version="1.0.0",
    author="ZHIHE ZHAO",
    author_email="zhaozhihe98@163.com",
    description="A test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_data={'': ['*.ipynb', '*.yaml']}
)