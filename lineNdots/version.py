from os.path import join as pjoin

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'  # use '' for full releases, 'a' for alpha releases,
                          # 'b' for beta releases, 'rc' for release candidates, 'dev' for development releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "lineNdots: simple line and dot plots for data visualization."
# Long description will go up on the pypi page
long_description = """
LineNdots
=========
LineNdots is a straightforward implementation of plots with lines as range and dots as data points.
It is heavliy inspired from the `ggrain` and `raincloud` packages in R. However, it does not include the singautre
KDE plot of the `raincloud` package.

Also, LineNdots adds the signature single line plots for the individual data points,
which was missing in the ported `ggrain` package to python (PtitPrince).

(c) 2024, Seyed Yahya Shirazi, Swartz Center for Computational Neuroscience, University of California, San Diego
"""

NAME = "lineNdots"
MAINTAINER = "Seyed Yahya Shirazi"
MAINTAINER_EMAIL = "shirazi@ieee.org"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "http://github.com/neuromechanist/lineNdots"
DOWNLOAD_URL = ""
LICENSE = "MIT"
AUTHOR = "Seyed Yahya Shirazi"
AUTHOR_EMAIL = "shirazi@ieee.org"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGE_DATA = {'fetch_citations': [pjoin('data', '*')]}
REQUIRES = ['seaborn', 'matplotlib', 'numpy', 'pandas']
PYTHON_REQUIRES = ">= 3.9"
