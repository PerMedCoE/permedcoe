# ########################## #
# ####### PUBLIC API ####### #
# ########################## #

# Decorator selector
try:
    # Running with PyCOMPSs with take these imports
    from pycompss.api.container import Container
    from pycompss.api.constraint import Constraint
    from pycompss.api.binary import Binary
    from pycompss.api.task import Task
    from pycompss.api.parameter import FILE_IN
    from pycompss.api.parameter import FILE_OUT
    from pycompss.api.parameter import DIRECTORY_IN
    from pycompss.api.parameter import DIRECTORY_OUT
    from pycompss.api.parameter import Type
    from pycompss.api.parameter import StdIOStream
    from pycompss.api.parameter import STDIN
    # raise ImportError  # NOSONAR
except ImportError:
    # Without PyCOMPSs it will take the core
    from permedcoe.core.decorators import Container
    from permedcoe.core.decorators import Constraint
    from permedcoe.core.decorators import Binary
    from permedcoe.core.decorators import Task
    from permedcoe.core.decorators import FILE_IN
    from permedcoe.core.decorators import FILE_OUT
    from permedcoe.core.decorators import DIRECTORY_IN
    from permedcoe.core.decorators import DIRECTORY_OUT
    from permedcoe.core.decorators import Type
    from permedcoe.core.decorators import StdIOStream
    from permedcoe.core.decorators import STDIN

# Public functions
from permedcoe.base import get_environment
from permedcoe.base import set_debug
from permedcoe.base import invoker
