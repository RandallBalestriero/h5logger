# Powerful Minimalist h5 Python logger

h5logger is a minimalist logger that allows to save arbitrary quantities/arrays into h5 files in a continuous/streaming manner. The logger automatically create/open/close h5 files and append data as a stream whenever the user calls the ``log`` method of the ``h5logger`` class. Only dependancy requirement is [h5py](https://docs.h5py.org/en/stable/build.html) and [NumPy](https://github.com/RandallBalestriero/h5logger).


## Walkthrough example

 Here is a simple example to store different
 realisation of random binary variables:
```
import numpy as np
from h5logger import h5logger


# set seed for reproducibility

np.random.seed(0)

# create the logger that will save the continuous
# stream of data into the logging_data.h5 file
# we set replace_if_exists=True to remove any
# previously saved h5 file with same name 
# and not append data to an existing h5 file

logger = h5logger("logging_data.h5", replace_if_exists=True)

for i in range(10):
    number = np.random.randint(2)
    logger.log("number", number)

# all the data is now into the h5 file which can be
# accessed as desired by the user, h5logger provides
# some built-in reading utilities that only load
# in memory the accessed slices of data

with logger.open() as data:
    print(data["number"])
    # >>> <HDF5 dataset "number": shape (10,), type "<i8">
    print(data["number"][:])
    # >>> [0 1 1 0 1 1 1 1 1 1]
```

## h5logger or TensorBoard/Comet.ml/MLflow/...?

*Short answer: h5logger is the simplest, easiest, cheapest (free) solution to quickly set-up saving/logging pipelines regardless of the use-cases.*

Depending on everyone's needs and purposes, different loggers will shine. We thus only highlight here some key benefits/differences of h5logger against the alternatives:

- **Minimalist:** the entire logger relies on only two dependencies (h5py,numpy), nothing else is needed, no required registration
- **Versatile:** the entire goal of h5logger is to do one thing and do it as best as possible. That thing is allow saving of arbitrary streaming data/arrays. Anything else, e.g. plotting, is left to the user. This makes h5logger easy to insert in many existing softwares due to its little overlap with existing softwares
- **Powerful:** as detailed below, h5logger leverages the powerful HDF5 file formatting enabling out-of-the-box performances on very big data
- **Platform independant:** the logger can be used the same across platform/hardware


## Why the h5 format?

h5 files have many advantages:
 - **big-data friendly:** h5py does not return an in-memory numpy array. Instead it returns something that behaves like it, hence accessing different chunks of data from any saved quantity can be done near instantly even though the entire dataset might be humongously large. Have a look at the [h5py introduction](https://docs.h5py.org/en/latest/high/dataset.html#dataset) for more information.

- **streaming data friendly:** because h5 supports saving data per chunk, it is extremely well suited to dynamically expand dataset and insert new observations, i.e., it efficiently deals with saving streams of data

- **command-line monitoring:** another great advantage of h5 files is their ability to be monitored from a terminal with simple command-line e.g. `h5ls logging_data.h5`. This is a crucial feature to easily monitor (locally and remotely) the logging status. For a list of commands see [this guide](https://support.hdfgroup.org/products/hdf5_tools/#h5dist) (requires hdf5 package which can be installed with [anaconda](https://anaconda.org/anaconda/hdf5)/[brew](https://formulae.brew.sh/formula/hdf5)/[apt]())