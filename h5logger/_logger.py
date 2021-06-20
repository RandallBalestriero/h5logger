import h5py
import numpy as np
import os
from contextlib import contextmanager
from . import _utils as utils
import time


class _safe_open:
    """Custom context manager for opening files."""

    def __init__(self, filename, *args, **kwargs):
        self.f = False
        while not self.f:
            self.open(filename, *args, **kwargs)
            if self.f:
                break
            time.sleep(2)

    def open(self, filename, *args, **kwargs):
        try:
            self.f = h5py.File(filename, *args, **kwargs)
        except Exception as e:
            error_message = str(e)
            if "Resource temporarily unavailable" in error_message:
                print(error_message)
                print("Retrying in 2 secondes...")
            else:
                raise (e)

    def __enter__(self):
        return self.f

    def __exit__(self, *args):
        self.f.close()


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

    def __init__(
        self,
        filename: str,
        replace_if_exists: bool = False,
        concurrent_readers: bool = False,
        datasets: dict or None = None,
    ):

        # be sure to use self.filename anywhere down this line as it
        # took care of extension formatting automatically
        self._filename = utils.produce_filename(filename)
        self._concurrent_readers = concurrent_readers

        if os.path.exists(self.filename) and not replace_if_exists:
            # we have to make sure that it is a proper .h5 file
            # and we can append data to it if needed
            utils.check_file_validity(self.filename)
            tag = "a"
        elif os.path.exists(self.filename) and replace_if_exists:
            os.remove(self.filename)
            tag = "w"
        else:
            tag = "w"

        self._file = h5py.File(self.filename, tag, libver="latest")
        self._need_full_resize = []
        if tag == "w" and self.concurrent_readers:

            assert datasets is not None
            for name, (dim, dtype) in datasets.items():
                assert type(name) == str
                assert type(dim) == int
                self._file.create_dataset(
                    name,
                    (0,) * dim,
                    maxshape=(None,) * dim,
                    dtype=dtype,
                )
                self._need_full_resize.append(name)

            self._file.swmr_mode = self.concurrent_readers

    def enable_concurrent_readers(self):
        if self._file.swmr_mode == False:
            self._file.swmr_mode = True

    def close(self):
        self._file.close()

    def log(self, name: str, value: object) -> None:
        utils.validate_log(self.filename)
        if not hasattr(value, "shape"):
            value = np.array(value)
        if not hasattr(value, "dtype"):
            value = np.array(value)

        if name not in self._file:
            if self._file.swmr_mode:
                raise RuntimeError(
                    "trying to log a non-initialized dataset with concurrent readers on"
                )
            self._file.create_dataset(
                name,
                (0,) + value.shape,
                maxshape=(None,) + value.shape,
                dtype=value.dtype,
            )

        dset = self._file[name]
        if name in self._need_full_resize:
            dset.resize((1,) + value.shape)
            self._need_full_resize.remove(name)
        else:
            assert dset.shape[1:] == value.shape
            dset.resize(dset.shape[0] + 1, axis=0)
        dset[-1] = value

        # Notify the reader process that new data has been written
        dset.flush()

    @property
    def filename(self):
        return self._filename

    @property
    def concurrent_readers(self):
        return self._concurrent_readers

    def keys(self):
        with h5py.File(self.filename, "r") as f:
            for key in f.keys():
                yield key

    @staticmethod
    def open(filename):
        return _safe_open(
            utils.produce_filename(filename), "r", libver="latest", swmr=True
        )
