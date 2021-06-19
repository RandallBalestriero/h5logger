# Minimalist h5 Python logger

h5logger is a minimalist logger that allows to continuously save arbitrary quantities into h5 files. The logger automatically create/open/close h5 files and append data as a stream whenever the user calls the ``log`` method of the ``logger`` class. Only dependancy requirement is [h5py](https://docs.h5py.org/en/stable/build.html).


## Walkthrough example

 Here is a simple example to store different
 realisation of random variables:
```
import numpy as np
from h5logger import h5logger


# set seed for reproducibility
np.random.seed(0)

# create the logger that will save the continuous
# stream of data into the logging_data.h5 file, we also replace any
# file that already was saved from before, otherwise data is appended into it
logger = h5logger("logging_data.h5", replace_if_exists=True)

for i in range(10):
    number = np.random.randint(2)

    # save the number realisation into the `number`
    # variable, any string can be used for name
    logger.log("number", number)

# all the data is now into the h5 file which can be
# access as desired by the user
# h5logger has some built-in reading functions
with logger.open() as data:
    print(data["number"])
    # >>> <HDF5 dataset "number": shape (21,), type "<i8">
    # nothing is loaded in-memory yet, loading is only done
    # when accessing slices of data as in
    print(data["number"][:])
    # >>> [0 1 1 0 1 1 1 1 1 1]
```

Minimalist Python logger/saver storing continuous stream of data into h5 files


## Why the h5 format?

h5 files have many advantages:
 - **big data friendely:** h5py does not return an in-memory numpy array. Instead it returns something that behaves like it, hence accessing different chunks of data from any saved quantity can be done near instantly even though the entire dataset might be humongously large. Have a look at the [h5py introduction](https://docs.h5py.org/en/latest/high/dataset.html#dataset) for more information.

- **suited for saving streaming data:** because h5 supports saving data per chunk, it is extremely well suited to dynamically expand dataset and insert new observations, i.e., it efficiently deals with saving streams of data

- **command-line monitoring:** another great advantage of h5 files is their ability to be monitored from a terminal with simple command-line e.g. `h5ls logging_data.h5`. This is a crucial feature to easily monitor (locally and remotely) the logging status. For a list of commands see [this guide](https://support.hdfgroup.org/products/hdf5_tools/#h5dist) (requires hdf5 package which can be installed with [anaconda](https://anaconda.org/anaconda/hdf5)/[brew](https://formulae.brew.sh/formula/hdf5)/[apt]())