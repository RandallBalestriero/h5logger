import os


def validate_log(filename):
    assert os.path.exists(filename)
