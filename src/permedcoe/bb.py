"""Private functions used by the building blocks."""

import os


def get_container_path():
    """Retrieve the PerMedCoE container images path.

    :return: The value of the PERMEDCOE_IMAGES environment variable.
    :raises Exception: If the "PERMEDCOE_IMAGES" is not defined.
    """
    # Container definition environment variable
    CONTAINER_PATH_VN = "PERMEDCOE_IMAGES"
    if CONTAINER_PATH_VN in os.environ:
        return os.environ[CONTAINER_PATH_VN]
    else:
        raise Exception("Please define %s environment variable with the path." % CONTAINER_PATH_VN)


CONTAINER_PATH = get_container_path()


def get_computing_units():
    """Retrieve the computing units required for the tasks.

    :return: The value of the COMPUTING_UNITS environment variable as integer.
    """
    # Computing units for the tasks
    COMPUTING_UNITS_VN = "COMPUTING_UNITS"
    if COMPUTING_UNITS_VN in os.environ:
        return int(os.environ[COMPUTING_UNITS_VN])
    else:
        return 1


COMPUTING_UNITS = get_computing_units()
