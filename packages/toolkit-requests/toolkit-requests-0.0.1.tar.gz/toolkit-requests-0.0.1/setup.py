import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='toolkit-requests',
    version='0.0.1',
    description='Typosquatting talk example, do not use.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/requests/toolbelt',
    author='N. Body',
    author_email='nepijav923@otanhome.com',
    license='Apache',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)                                                  