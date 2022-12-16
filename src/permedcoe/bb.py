"""Private functions used by the building blocks."""

import os


def get_container_path():
    """Retrieve the PerMedCoE container images path.

    :raises Exception: If the "PERMEDCOE_IMAGES" is not defined.
    """
    # Container definition environment variable
    if "PERMEDCOE_IMAGES" in os.environ:
        return os.environ["PERMEDCOE_IMAGES"]
    else:
        raise Exception("Please define PERMEDCOE_IMAGES environment variable with the path.")


CONTAINER_PATH = get_container_path()
