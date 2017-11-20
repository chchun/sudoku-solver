#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2016 David Shi (dcmshi)

from setuptools import setup

if __name__ == '__main__':
    setup(
        name='sudoku-solver',
        version='1.0',
        url='https://github.com/dcmshi/sudoku-solver',
        license='New BSD License',
        author='David Shi',
        author_email='shibisoma@hotmail.com',
        description='sudoku solver using back-tracking, forward-checking, and heuristics',
        py_modules=('sudoku',),
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Topic :: Education',
            'Topic :: Games/Entertainment :: Puzzle Games',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)