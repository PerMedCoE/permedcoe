# ########################## #
# ####### PUBLIC API ####### #
# ########################## #

# Decorator selector
try:
    # Running with PyCOMPSs with take these imports
    from pycompss.api.container import container
    from pycompss.api.constraint import constraint
    from pycompss.api.binary import binary
    from pycompss.api.task import task
    from pycompss.api.mpi import mpi
    from pycompss.api.parameter import FILE_IN
    from pycompss.api.parameter import FILE_OUT
    from pycompss.api.parameter import FILE_INOUT
    from pycompss.api.parameter import DIRECTORY_IN
    from pycompss.api.parameter import DIRECTORY_OUT
    from pycompss.api.parameter import DIRECTORY_INOUT
    from pycompss.api.parameter import Type
    from pycompss.api.parameter import StdIOStream
    from pycompss.api.parameter import STDIN
    # raise ImportError  # NOSONAR
except ImportError:
    # Without PyCOMPSs it will take the core
    from permedcoe.core.decorators import container
    from permedcoe.core.decorators import constraint
    from permedcoe.core.decorators import binary
    from permedcoe.core.decorators import task
    from permedcoe.core.decorators import mpi
    from permedcoe.core.decorators import FILE_IN
    from permedcoe.core.decorators import FILE_OUT
    from permedcoe.core.decorators import FILE_INOUT
    from permedcoe.core.decorators import DIRECTORY_IN
    from permedcoe.core.decorators import DIRECTORY_OUT
    from permedcoe.core.decorators import DIRECTORY_INOUT
    from permedcoe.core.decorators import Type
    from permedcoe.core.decorators import StdIOStream
    from permedcoe.core.decorators import STDIN

# Public functions
from permedcoe.base import get_environment
from permedcoe.base import set_debug
from permedcoe.base import invoker

# Arguments definition
from permedcoe.utils.user_arguments import ArgumentDirections as __ArgumentDirections__
from permedcoe.utils.user_arguments import Argument as __Argument__
class Arguments:

    def __init__(self):
        self.arguments = {}
        self.arguments["default"] = __ArgumentDirections__()

    def add_input(self, name, type, description, check=None, mode="default"):
        if not mode in self.arguments:
            self.arguments[mode] = __ArgumentDirections__()
        self.arguments[mode].add_input(name, __Argument__(type, description, check))

    def add_output(self, name, type, description, mode="default"):
        if not mode in self.arguments:
            self.arguments[mode] = __ArgumentDirections__()
        self.arguments[mode].add_output(name, __Argument__(type, description))

    def get_arguments(self) -> dict:
        return self.arguments

    def __str__(self) -> str:
        args_str = ""
        for k, v in self.arguments.items():
            args_str += "Mode: %s\n" % k
            args_str += "Arguments: %s\n" % v
        return args_str