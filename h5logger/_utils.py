import os


def produce_filename(filename):
    pre, ext = os.path.splitext(filename)
    if ext == "":
        return filename + ".h5"
    elif exp == ".h5":
        return filename
    raise RuntimeError(
        "provided filename has file extension {ext} that is not compatible with h5"
    )


def check_file_validity(filename):
    pre, ext = os.path.splitext(filename)
    assert ext == "h5"


def validate_log(filename):
    assert os.path.exists(filename)
