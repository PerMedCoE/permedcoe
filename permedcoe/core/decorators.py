"""
This file implements the decorators to be used in the building blocks,
which wrap the container, binary and execution actions.
"""

import os
import sys
import inspect
import subprocess
import logging
from collections import OrderedDict

from permedcoe.core.building_block import PerMedBB

# Environment variable names
from permedcoe.core.constants import PERMEDCOE_TMPDIR
from permedcoe.core.constants import PERMEDCOE_PROCESSES
from permedcoe.core.constants import PERMEDCOE_GPUS
from permedcoe.core.constants import PERMEDCOE_MEMORY
from permedcoe.core.constants import PERMEDCOE_MOUNT_POINTS
from permedcoe.core.constants import SEPARATOR


# ################################################################# #
# ########################## DECORATORS ########################### #
# ################################################################# #

class Container(object):
    """
    Container class (decorator style)

    Gets the container related information.
    """

    def __init__(self, *args, **kwargs):
        # Decorator parameters
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            # args and kwargs are the function invocation parameters
            # Delegate the needed info to the task through the **kwargs.
            kwargs["engine"] = self.kwargs["engine"]
            kwargs["image"] = self.kwargs["image"]
            return f(*args, **kwargs)
        return wrapped_f


class Constraint(object):
    """
    Dummy Constraint class (decorator style)
    """

    def __init__(self, *args, **kwargs):
        # Decorator parameters
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            # args and kwargs are the function invocation parameters
            # Delegate the needed info to the task through the **kwargs.
            kwargs["computing_units"] = self.kwargs["computing_units"]
            return f(*args, **kwargs)
        return wrapped_f


class Mpi(object):
    """
    Mpi class (decorator style)

    Gets the MPI related information.
    """

    def __init__(self, *args, **kwargs):
        # Decorator parameters
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            # args and kwargs are the function invocation parameters
            # Delegate the needed info to the task through the **kwargs.
            kwargs["runner"] = self.kwargs["runner"]
            kwargs["binary"] = self.kwargs["binary"]
            kwargs["computing_nodes"] = self.kwargs["computing_nodes"]  # noqa TODO: ignored since it requires node names
            if "environment" in self.kwargs:
                kwargs["environment"] = self.kwargs["environment"]
            else:
                kwargs["environment"] = []
            return f(*args, **kwargs)
        return wrapped_f


class Binary(object):
    """
    Binary class (decorator style)

    Gets the binary related information.
    """

    def __init__(self, *args, **kwargs):
        # Decorator parameters
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            # args and kwargs are the function invocation parameters
            # Delegate the needed info to the task through the **kwargs.
            kwargs["binary"] = self.kwargs["binary"]
            if "environment" in self.kwargs:
                kwargs["environment"] = self.kwargs["environment"]
            else:
                kwargs["environment"] = []
            return f(*args, **kwargs)
        return wrapped_f


class Task(object):
    """
    Task class (decorator style) that defines the behaviour of a
    building block execution.
    Takes information from the higher level decorators (@container
    and @binary), does the necessary path transformations from
    relative to absolute, then instantiates a PerMed_BB instance
    with all this information and launches its execution.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            # To dummy task:
            # return f(*args, **kwargs)
            # Instead, takes all learnt from previous decorators, and acts:
            # Deploys the container and executes the binary

            # Pop the info from upper decorators:
            self.engine = kwargs.pop("engine")
            self.image = kwargs.pop("image")
            self.runner = kwargs.pop("runner", None)
            self.binary = kwargs.pop("binary")
            self.computing_nodes = kwargs.pop("computing_nodes", 1)
            self.computing_units = kwargs.pop("computing_units", 1)
            self.env_vars = kwargs.pop("environment")
            logging.debug(SEPARATOR)
            logging.debug("Container engine          : %s" % self.engine)
            logging.debug("Container image           : %s" % self.image)
            logging.debug("Container runner          : %s" % self.runner)
            logging.debug("Container binary          : %s" % self.binary)
            logging.debug("Container computing_nodes : %s" % self.computing_nodes)
            logging.debug("Container computing_units : %s" % self.computing_units)
            logging.debug("Container env vars        : %s" % self.env_vars)
            logging.debug(SEPARATOR)

            # Parameters provided by the user:
            defaults = self.__get_defaults__(f)
            flags = OrderedDict(defaults, **kwargs)
            flags_list = list(flags.values())
            logging.debug("Provided flags: %s" % str(kwargs))
            logging.debug("Default flags: %s" % str(defaults))
            logging.debug("User flags: %s" % str(flags_list))
            logging.debug(SEPARATOR)

            # Look for mount paths:
            mount_paths, update_paths, user_mount_paths = \
                self.__find_mount_paths__(kwargs)

            if update_paths:
                # There are paths that need to be fixed in flags list
                for k, v in update_paths.items():
                    flags[k] = v
                flags_list = list(flags.values())

            logging.debug("User flags: %s" % str(flags_list))
            logging.debug("Mount paths:")
            for path in mount_paths:
                logging.debug("- %s" % path)
            logging.debug(SEPARATOR)

            # Act:
            BB = PerMedBB(self.image,
                          self.runner,
                          self.binary,
                          self.computing_nodes,
                          self.computing_units,
                          mount_paths,
                          user_mount_paths,
                          self.env_vars,
                          flags_list)
            debug = True if logging.getLevelName == "DEBUG" else False
            BB.launch(debug=debug)
        return wrapped_f

    def __find_mount_paths__(self, kwargs):
        """ Looks for mount paths into the give input/output files/directories.

        Args:
            kwargs (dict): Keyword dictionary (invocation parameters)

        Returns:
            list: List with the paths to be mounted.
            dict: Dictionary with the flags to be updated
                  (from relative to absolute).
        """
        mount_paths = []
        update_paths = {}
        # Look into the invocation parameters
        for k, v in self.kwargs.items():
            path = ""
            if v == FILE_IN or v == FILE_OUT:
                # Remove file name and keep only the folder
                if isinstance(kwargs[k], list):
                    for element in kwargs[k]:
                        path, name = os.path.split(os.path.realpath(element))
                        update_paths[k] = os.path.join(path, name)
                else:
                    path, name = os.path.split(os.path.realpath(kwargs[k]))
                    update_paths[k] = os.path.join(path, name)
            elif v == DIRECTORY_IN or v == DIRECTORY_OUT:
                if isinstance(kwargs[k], list):
                    for element in kwargs[k]:
                        if os.path.exists(element):
                            path = os.path.realpath(element)
                        elif v == DIRECTORY_OUT:
                            os.mkdir(element)
                            path = os.path.realpath(element)
                        else:
                            raise Exception("Input directory does not exist: %s" % str(element))  # noqa: E503
                else:
                    if os.path.exists(kwargs[k]):
                        path = os.path.realpath(kwargs[k])
                    elif v == DIRECTORY_OUT:
                        os.mkdir(kwargs[k])
                        path = os.path.realpath(kwargs[k])
                    else:
                        raise Exception("Input directory does not exist: %s" % str(element))  # noqa: E503
            else:
                raise Exception("Unexpected task tag found.")
            # Relative path to absolute
            mount_paths.append(path)
        # Look into the environment
        if PERMEDCOE_TMPDIR in os.environ:
            mount_paths.append(os.environ(PERMEDCOE_TMPDIR))
        user_mount_paths = None
        if PERMEDCOE_MOUNT_POINTS in os.environ:
            user_mount_paths = os.environ[PERMEDCOE_MOUNT_POINTS]
        return mount_paths, update_paths, user_mount_paths

    @staticmethod
    def __get_defaults__(func):
        """ Retrieve the default parameters of the given function

        Args:
            func (function): Function to be inspected.

        Returns:
            OrderedDict: Contains the parameter name as key and its
                         default value as its value.
        """
        signature = inspect.signature(func)
        return OrderedDict({
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        })


FILE_IN = "FILE_IN"
FILE_OUT = "FILE_OUT"
DIRECTORY_IN = "DIRECTORY_IN"
DIRECTORY_OUT = "DIRECTORY_OUT"
Type = "type"
StdIOStream = "StdIOStream"
STDIN = None
STDOUT = None
STDERR = None