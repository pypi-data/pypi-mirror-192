#!/usr/bin/env python3

from setuptools import setup
from hermit import Meta

# Get metada
version = Meta.version()

setup(
	name='memhermit',
	author='Albert Saez',
	author_email='albertsaeznunez@gmail.com',
	license='MIT',
	version=version,
	description='Phy memory explorer',
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3"
	],
	packages=['hermit']
)
