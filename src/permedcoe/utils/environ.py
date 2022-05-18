import os

from permedcoe.core.constants import PERMEDCOE_TMPDIR
from permedcoe.core.constants import PERMEDCOE_PROCESSES
from permedcoe.core.constants import PERMEDCOE_GPUS
from permedcoe.core.constants import PERMEDCOE_MEMORY
from permedcoe.core.constants import PERMEDCOE_MOUNT_POINTS


def set_environment(tmpdir=None,
                    processes=None,
                    gpus=None,
                    memory=None,
                    mount_points=None):
    """ Sets the necessary environment variables from the given arguments.

    Args:
        tmpdir (str, optional): Temporary directory to be mounted.
                                Defaults to None.
        processes (int, optional): Number of processes.
                                   Defaults to None.
        gpus (int, optional): Number of gpus.
                              Defaults to None.
        memory (int, optional): Amount of memory.
                                Defaults to None.
        mount_points (str, optional): User defined mount points.
                                      Defaults to None.
    """
    if tmpdir:
        if os.path.exists(tmpdir):
            os.environ[PERMEDCOE_TMPDIR] = tmpdir
        else:
            raise Exception("TMPDIR: %s does not exist." % tmpdir)
    if processes:
        os.environ[PERMEDCOE_PROCESSES] = processes
    if gpus:
        os.environ[PERMEDCOE_GPUS] = gpus
    if memory:
        os.environ[PERMEDCOE_MEMORY] = memory
    if mount_points:
        os.environ[PERMEDCOE_MOUNT_POINTS] = mount_points


def get_environment():
    """ Retrieve the environment variables set on call as dictionary.

    Returns:
        dict: Dictionary containing the environment set on call.
    """
    env_vars = {}
    if PERMEDCOE_TMPDIR in os.environ:
        env_vars["tmpdir"] = os.environ[PERMEDCOE_TMPDIR]
    if PERMEDCOE_PROCESSES in os.environ:
        env_vars["processes"] = os.environ[PERMEDCOE_PROCESSES]
    if PERMEDCOE_GPUS in os.environ:
        env_vars["gpus"] = os.environ[PERMEDCOE_GPUS]
    if PERMEDCOE_MEMORY in os.environ:
        env_vars["memory"] = os.environ[PERMEDCOE_MEMORY]
    if PERMEDCOE_MOUNT_POINT in os.environ:
        env_vars["mount_points"] = os.environ[PERMEDCOE_MOUNT_POINT]
    return env_vars
