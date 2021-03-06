# -*- encoding: utf-8 -*-

import sys
import io
import os
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from pathlib import Path
import pprint

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()



setup(
    name='image_pipeline',
    version='0.0.1',
    license='Proprietary',
    description='Prototype image data flow',
    author='Bill McAbee',
    author_email='wmcabee@cognitivescale.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    #include_package_data=True,
    zip_safe=False,
    setup_requires=["pytest-runner", ],
    tests_require=["pytest", ],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Environment :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=['pandas', 'numpy', 'jsonlines','cortex-client'],
    extras_require={
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        # 'console_scripts': [
        #    'nameless = nameless.cli:main',
        # ]
    },
)
