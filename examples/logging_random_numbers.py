import numpy as np
from h5logger import h5logger


# set seed for reproducibility
np.random.seed(0)

# create the logger that will save the continuous
# stream of data into the logging_data.h5 file
logger = h5logger("logging_data.h5")

for i in range(10):
    number = np.random.randint()

    # save the number realisation into the `number`
    # variable, any string can be used for name
    logger.log("number", number)

# all the data is now into the h5 file which can be
# access as desired by the user
# h5logger has some built-in reading functions
with logger.open() as data:
    print(data["accu"])
    #
