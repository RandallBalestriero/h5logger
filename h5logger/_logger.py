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
        
        replace_if_exists: bool
            if True, then any file with same name will be deleted, if False
            then any new logged data will be appended onto anything that already exists
    """

    def __init__(self, filename: str, replace_if_exists: bool = False):

        # be sure to use self.filename anywhere down this line as it
        # took care of extension formatting automatically
        self._filename = utils.produce_filename(filename)

        if os.path.exists(self.filename) and not replace_if_exists:
            # we have to make sure that it is a proper .h5 file
            # and we can append data to it if needed
            utils.check_file_validity(self.filename)
        elif os.path.exists(self.filename) and replace_if_exists
            os.remove(self.filename)
        else:
            # we simply write and close to create the file
            file = h5py.File(self.filename, "w")
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
            assert dset.shape[1:] == value.shape
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
