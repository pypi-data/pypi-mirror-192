import setuptools
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='tool_for_vcs',
	version='0.0.1',
    description='A demo package.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'parse_work=package.vcs_p:parse_work'
        ]
    },
)