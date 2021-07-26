import io
from os import path

from setuptools import setup

version = {}
with open('freecad_external_links/_version.py') as fp:
    exec(fp.read(), version)

current_dir = path.abspath(path.dirname(__file__))
with io.open(path.join(current_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='freecad-external-links',
    description='Utility for cross-document links or references in FreeCAD.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/gbroques/freecad-external-links',
    author='G Roques',
    version=version['__version__'],
    packages=['freecad_external_links'],
    entry_points={
        'console_scripts': [
            'fcxlink=freecad_external_links.cli:main'
        ]
    },
    install_requires=[],
    classifiers=[
        # Full List: https://pypi.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
