from ._logger import h5logger

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
