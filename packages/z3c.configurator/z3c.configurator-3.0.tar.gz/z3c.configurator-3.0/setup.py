##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='z3c.configurator',
    version='3.0',
    author="Zope Community",
    author_email="zope-dev@zope.dev",
    description="Dynamic configuration",
    long_description=(
        read('README.txt')
        + '\n\n.. contents::\n\n' +
        read('src', 'z3c', 'configurator', 'README.txt')
        + '\n\n' +
        read('src', 'z3c', 'configurator', 'browser', 'README.txt')
        + '\n\n' +
        read('CHANGES.txt')
    ),
    license='ZPL 2.1',
    keywords='zope3 z3c configurator configuration',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/z3c.configurator',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    python_requires='>=3.7',
    extras_require=dict(
        test=[
            'zope.testing',
            'zope.testrunner',
        ],
        ftest=[
            'zope.annotation',
            'zope.dublincore',
            'zope.formlib',
            'zope.securitypolicy',
            'zope.testbrowser',
            'zope.app.authentication',
            'zope.app.pagetemplate',
            'zope.app.testing',
            'zope.app.zcmlfiles',
        ],
        zmi=[
            'zope.browserpage',
            'zope.formlib',
        ],
    ),
    install_requires=[
        'setuptools',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    zip_safe=False,
)
