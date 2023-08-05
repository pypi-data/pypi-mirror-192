import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MMA_test",
    version="1.2.1",
    author="ZHIHE ZHAO",
    author_email="zhaozhihe98@163.com",
    description="A test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'MMA_test': ['*.nii.gz', '*.yaml']}
)