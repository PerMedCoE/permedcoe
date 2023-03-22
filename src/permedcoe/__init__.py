# ########################## #
# ####### PUBLIC API ####### #
# ########################## #

# Decorator selector
try:
    # Running with PyCOMPSs will take these imports
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
    from pycompss.api.parameter import STDOUT
    from pycompss.api.parameter import STDERR
    TMPDIR = "pycompss_sandbox"
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
    from permedcoe.core.decorators import STDOUT
    from permedcoe.core.decorators import STDERR
    TMPDIR = "None"

# Public functions
from permedcoe.base import get_environment
from permedcoe.base import set_debug
from permedcoe.base import invoker

# Arguments definition - explicit arguments
from permedcoe.utils.user_arguments import Arguments
