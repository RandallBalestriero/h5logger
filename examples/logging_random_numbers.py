import numpy as np
from h5logger import h5logger
import os

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

# we close the file since we do not need anymore writting operatior

logger.close()

# all the data is now into the h5 file which can be
# accessed as desired by the user, h5logger provides
# some built-in reading utilities that only load
# in memory the accessed slices of data

with h5logger.open("logging_data.h5") as data:
    print(data["number"])
    # >>> <HDF5 dataset "number": shape (10,), type "<i8">
    print(data["number"][:])
    # >>> [0 1 1 0 1 1 1 1 1 1]

os.remove("logging_data.h5")
