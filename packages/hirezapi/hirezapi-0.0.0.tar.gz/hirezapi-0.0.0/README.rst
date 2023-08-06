========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/hirezapi/badge/?style=flat
    :target: https://hirezapi.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/AidanJohnston/hirezapi/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/AidanJohnston/hirezapi/actions

.. |codecov| image:: https://codecov.io/gh/AidanJohnston/hirezapi/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/AidanJohnston/hirezapi

.. |version| image:: https://img.shields.io/pypi/v/hirezapi.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/hirezapi

.. |wheel| image:: https://img.shields.io/pypi/wheel/hirezapi.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/hirezapi

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/hirezapi.svg
    :alt: Supported versions
    :target: https://pypi.org/project/hirezapi

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/hirezapi.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/hirezapi

.. |commits-since| image:: https://img.shields.io/github/commits-since/AidanJohnston/hirezapi/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/AidanJohnston/hirezapi/compare/v0.0.0...main



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: MIT license

Installation
============

::

    pip install hirezapi

You can also install the in-development version with::

    pip install https://github.com/AidanJohnston/hirezapi/archive/main.zip


Documentation
=============


https://hirezapi.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
