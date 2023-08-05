import sys
import os
from setuptools import setup, find_packages
PACKAGES = find_packages()

# Get version and release info, which is all stored in lineNdots/version.py
ver_file = os.path.join('lineNdots', 'version.py')
with open(ver_file) as f:
    exec(f.read())

# Give setuptools a hint to complain if it's too old a version
# 24.2.0 added the python_requires option
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 24.2.0']
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ['wheel'] if 'bdist_wheel' in sys.argv else []

REQUIRES = [
        'python>=3.9'
        'seaborn>=0.12',
        'matplotlib',
        'numpy>=1.13',
        'pandas>=1.2'
        ]

opts = dict(name='lineNdots',
            version='0.0.1',
            description='A Seaborn-Pyplot package to plot group-level reuslts, as an alternative to box plots.',
            long_description=open('README.md').read(),
            url='https://github.com/neuromechanist/lineNdots',
            maintainer='Seyed (Yahya) Shirazi',
            maintainer_email='shirazi@ieee.org',
            author='Seyed (Yahya) Shirazi',
            author_email='shirazi@ieee.org',
            license='MIT',
            classifiers=[
                'Intended Audience :: Science/Research',
                'Intended Audience :: Developers',
                'License :: OSI Approved',
                'Programming Language :: Python',
                'Topic :: Software Development',
                'Topic :: Scientific/Engineering',
                'Operating System :: Microsoft :: Windows',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Operating System :: MacOS',
            ],
            platforms='any',
            packages=PACKAGES,
            install_requires=REQUIRES,
            setup_requires=SETUP_REQUIRES,
            requires=REQUIRES)


if __name__ == '__main__':
    setup(**opts)
