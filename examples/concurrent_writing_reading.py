import numpy as np
from h5logger import h5logger
from multiprocessing import Process
import time
import os


def background_writer_option1(steps):
    """dummy background saver"""
    logger = h5logger("logging_data_concurrent.h5", replace_if_exists=True)
    np.random.seed(1)
    for i in range(steps):
        time.sleep(1)
        number = np.random.randn()
        logger.log("number", number)
        if i % 2 == 0:
            logger.log("even_number", 20 * number)
            # the first time we hit this line, all datasets have been created
            # we can thus enable concurrent reading, we can repeatedly call
            # if as only the first call has any effect
            logger.enable_concurrent_readers()
    logger.close()


def background_writer_option2(steps):
    """dummy background saver"""
    np.random.seed(2)
    logger = h5logger(
        "logging_data_concurrent.h5",
        replace_if_exists=True,
        concurrent_readers=True,
        datasets={"number": (1, "float"), "even_number": (1, "float")},
    )

    for i in range(steps):
        time.sleep(1)
        number = np.random.randn()
        logger.log("number", number)
        if i % 2 == 0:
            logger.log("even_number", 20 * number)
    logger.close()


def reader_option1():
    with h5logger.open("logging_data_concurrent.h5") as data:
        dset = data["even_number"]
        while True:
            dset.refresh()
            print(dset[:])
            if dset.size == 5:
                break
            time.sleep(1)


def reader_option2():
    while True:
        with h5logger.open("logging_data_concurrent.h5") as data:
            print(data["even_number"][:])
            if data["even_number"].size == 5:
                break
        time.sleep(1)


p = Process(target=background_writer_option1, args=(10,))
p.start()
time.sleep(0.2)
reader_option1()
p.join()

# Unable to open file (unable to lock file, errno = 35, error message = 'Resource temporarily unavailable')
# Retrying in 2 secondes...
# [32.48690727]
# [ 32.48690727 -10.56343505]
# [ 32.48690727 -10.56343505]
# [ 32.48690727 -10.56343505  17.30815259]
# [ 32.48690727 -10.56343505  17.30815259]
# [ 32.48690727 -10.56343505  17.30815259  34.89623528]
# [ 32.48690727 -10.56343505  17.30815259  34.89623528]
# [ 32.48690727 -10.56343505  17.30815259  34.89623528   6.38078192]

p = Process(target=background_writer_option2, args=(10,))
p.start()
time.sleep(0.2)
reader_option2()
p.join()

# [-8.33515695]
# [-8.33515695]
# [ -8.33515695 -42.72392191]
# [ -8.33515695 -42.72392191]
# [ -8.33515695 -42.72392191 -35.8687117 ]
# [ -8.33515695 -42.72392191 -35.8687117 ]
# [ -8.33515695 -42.72392191 -35.8687117   10.05762834]
# [ -8.33515695 -42.72392191 -35.8687117   10.05762834]
# [ -8.33515695 -42.72392191 -35.8687117   10.05762834 -21.15904438]

os.remove("logging_data_concurrent.h5")
