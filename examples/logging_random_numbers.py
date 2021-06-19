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
