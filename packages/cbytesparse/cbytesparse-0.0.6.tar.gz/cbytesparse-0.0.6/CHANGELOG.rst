Changelog
=========

0.0.6 (2023-02-18)
------------------

* Following the ``bytesparse`` Python package, version ``0.0.6``.
* Added automatic wheel builder within GitHub Actions CI.
* Added *byte-like* methods and inplace editing.
* Added support to Python 3.11, removed 3.6.
* Added some minor features.
* Improved documentation.
* Improved testing.
* Improved repository layout (``pyproject.toml``).
* Minor fixes.


0.0.5 (2022-02-22)
------------------

* Following the ``bytesparse`` Python package, version ``0.0.5``.
* Added ``bytesparse`` class, closer to ``bytearray`` than ``Memory``.
* Added registration to the abstract base classes.
* Added missing abstract and ported methods.
* Added cut feature.
* Added more helper methods.
* Fixed values iteration.
* Improved extraction performance.
* Improved testing.


0.0.4 (2022-01-09)
------------------

* Following the ``bytesparse`` Python package, version ``0.0.4``.
* Refactored current implementation as the ``c`` sub-module.
* Removed experimental backup feature.
* Added dedicated methods to backup/restore mutated state.
* Fixed some write/insert bugs.
* Fixed some trim/bound bugs.
* Methods sorted by name.
* Removed useless functions.


0.0.2 (2022-01-03)
------------------

* Forced extension compilation.
* Using explicit factory methods instead of constructor arguments.
* Added block collapsing helper function.
* Minor fixes.
* Improved test suite.


0.0.1 (2021-12-27)
------------------

* First release on PyPI.
