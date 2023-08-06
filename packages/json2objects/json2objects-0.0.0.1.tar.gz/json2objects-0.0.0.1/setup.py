from pathlib import Path
from configparser import ConfigParser
from setuptools import setup, find_packages

config = ConfigParser()
config.read('setup.cfg')

setup(
    name="json2objects",
    license="MIT",
    author="forevercynical",
    author_email="me@cynical.gg",
    description="Easily convert JSON files to Python objects.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/forevercynical/json2objects",
    version = config.get('metadata', 'version'),
    packages=find_packages(),
    install_requires=[],
    keywords=[
        "json2objects",
        "convert-json-to-objects",
        "generate-classes-from-json",
        "json-to-objects",
        "json-to-python-objects",
        "json-to-python-classes",
        "json-to-classes",
        "class-generator",
        "class-generator-from-json"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7"
)
