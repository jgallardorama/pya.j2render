import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def get_version():
    version = {}
    with open('j2tool/version.py') as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version['__version__']


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="j2tool",
    version=get_version(),
    url="xyz_url",
    license="JGR License",
    author="JGR",
    author_email="jgr@jgr.es",
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    long_description=read("README.rst"),
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "Click>=7.0",
        "pyyaml>=5.0",
        "colorama==0.4.4",
        "jinja2==3.0.1",
        "markupsafe==2.0.1",
        "watchdog==2.1.5"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points="""
        [console_scripts]
        j2tool=j2tool.cli:start
    """,
)
