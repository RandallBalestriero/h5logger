import h5py
import numpy as np
import os
from contextlib import contextmanager
from . import _utils as utils


class h5logger:
    """h5 logger

    Args:
    -----

        filename: str
            the name of the h5 file to log the data into
    """

    def __init__(self, filename: str):
        self._filename = filename
        if os.path.exists(filename):
            assert filename[-2:] == "h5"

        else:
            file = h5py.File(filename, "w")
            file.close()

    def log(self, name: str, value: object) -> None:
        utils.validate_log(self.filename)
        if not hasattr(value, "shape"):
            value = np.array(value)
        if not hasattr(value, "dtype"):
            value = np.array(value)

        with h5py.File(self.filename, "a") as f:
            if name not in f:
                f.create_dataset(
                    name,
                    (1,) + value.shape,
                    maxshape=(None,) + value.shape,
                    dtype=value.dtype,
                )
            dset = f[name]
            dset.resize(dset.shape[0] + 1, axis=0)
            dset[-1] = value

    @property
    def filename(self):
        return self._filename

    def keys(self):
        with h5py.File(self.filename, "r") as f:
            for key in f.keys():
                yield key

    @contextmanager
    def open(self):
        f = h5py.File(self.filename, "r")
        try:
            yield f
        finally:
            f.close()