"""Private functions used by the building blocks."""

import os

from permedcoe.utils.exceptions import PerMedCoEException


def get_container_path():
    """Retrieve the PerMedCoE container images path.

    :return: The value of the PERMEDCOE_IMAGES environment variable.
    :raises Exception: If the "PERMEDCOE_IMAGES" is not defined.
    """
    # Container definition environment variable
    container_path_vn = "PERMEDCOE_IMAGES"
    if container_path_vn in os.environ:
        container_path_vn_value = os.environ[container_path_vn]
        if os.path.isdir(container_path_vn_value):
            return container_path_vn_value
        raise PerMedCoEException(
            f"Container path does not exit: {container_path_vn_value}"
        )
    raise PerMedCoEException(
        f"Please define {container_path_vn} environment variable with the path."
    )


CONTAINER_PATH = get_container_path()


def get_computing_units():
    """Retrieve the computing units required for the tasks.

    :return: The value of the COMPUTING_UNITS environment variable as integer.
    """
    # Computing units for the tasks
    computing_units_vn = "COMPUTING_UNITS"
    if computing_units_vn in os.environ:
        return int(os.environ[computing_units_vn])
    return 1


COMPUTING_UNITS = get_computing_units()
