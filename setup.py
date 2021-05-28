from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

# This call to setup() does all the work
setup(
    name="xdrone",
    version="0.1.11",
    description="xDrone Language Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xDrone-DSL/xDroneLanguageServer",
    author="Kai Zhu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    scripts=['./cmdline.py'],
    install_requires=["click", "antlr4-python3-runtime", "netifaces", "netaddr"],
    entry_points={
        "console_scripts": [
            "xdrone=cmdline:main",
        ]
    },
)
