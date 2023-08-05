#!/usr/bin/env python

"""The setup script."""
import time
from setuptools import setup, find_packages
# from aigc import __version__

version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().split('\n')

setup(
    author="aigc",
    author_email='313303303@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="AI生成",
    entry_points={
        'console_scripts': [
            'aigc=aigc.clis.cli:cli'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='aigc',
    name='aigc',
    packages=find_packages(include=['aigc', 'aigc.*']),

    test_suite='tests',
    url='https://github.com/yuanjie-ai/aigc',
    version=version, # '0.0.0',
    zip_safe=False,
)

