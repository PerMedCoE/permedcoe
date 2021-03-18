from permedcoe.utils.arguments import single_bb_sysarg_parser as __bb_parser__
from permedcoe.utils.preproc import preprocessing as __preprocessing__
from permedcoe.utils.log import init_logging as __init_logging__
from permedcoe.utils.environ import get_environment as __get_environment__


def get_environment():
    """ Retrieve the environment variables set on call as dictionary.

    Returns:
        dict: Dictionary containing the environment set on call.
    """
    return __get_environment__()


def set_debug(level=False):
    """ Sets the global debug variable

    Args:
        debug: True to enable debug. False otherwise.
    Returns:
        None
    """
    __init_logging__(level)


def invoker(function) -> None:
    """ Parse the input parameters (from sys.argv) and then invoke the
    given BB function.

    Args:
        function (function): Building block function to invoke.
    Returns:
        None
    """
    arguments = __bb_parser__()
    # Grab input and output
    in_path = arguments.input
    out_path = arguments.output
    # Preprocess
    cfg = __preprocessing__(arguments)
    # Building block invocation
    function(in_path, out_path, cfg)
