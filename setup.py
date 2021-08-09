import io
from os import path

from setuptools import find_packages, setup

version = {}
with open('fcxref/_version.py') as fp:
    exec(fp.read(), version)

current_dir = path.abspath(path.dirname(__file__))
with io.open(path.join(current_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fcxref',
    description='Manages FreeCAD external references.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/gbroques/fcxref',
    author='G Roques',
    version=version['__version__'],
    packages=find_packages(exclude=['tests']),
    # Incude data files specified in MANIFEST.in file.
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fcxref=fcxref.cli:main'
        ]
    },
    install_requires=[],
    classifiers=[
        # Full List: https://pypi.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
