import os


def produce_filename(filename: str) -> str:
    pre, ext = os.path.splitext(filename)
    if ext == "":
        return filename + ".h5"
    elif ext == ".h5":
        return filename
    raise RuntimeError(
        "provided filename has file extension {ext} that is not compatible with h5"
    )


def check_file_validity(filename: str) -> bool:
    pre, ext = os.path.splitext(filename)
    if ext == "h5":
        return True
    else:
        return False


def validate_log(filename: str) -> bool:
    if os.path.exists(filename):
        return True
    else:
        return False
