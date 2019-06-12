#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='OTX_transform',
    author='Sebastien Larinier',
    version='1.0',
    author_email='sebdraven@protonmail.com',
    maintainer='Sebastien Larinier',
    url='',
    description='Maltego transform for interacting with a otx alienvault.',
    license='GPLv3',
    packages=find_packages('OTX_transform'),
    package_dir={'': 'OTX_transform'},
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3',
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: Internet',
    ],
    package_data={
        '': ['*.gif', '*.png', '*.conf', '*.mtz', '*.machine']  # list of resources
    },
    python_requires='>=3.5',
    install_requires=[
        'canari>=3.3.9,<4',
        'request'
    ],
    dependency_links=[
        # custom links for the install_requires
    ]
)
