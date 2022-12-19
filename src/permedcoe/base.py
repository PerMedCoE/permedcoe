from permedcoe.utils.arguments import single_bb_sysarg_parser as __bb_parser__
from permedcoe.utils.arguments import load_parameters_from_json as __bb_param_loader__
from permedcoe.utils.preproc import preprocessing as __preprocessing__
from permedcoe.utils.log import init_logging as __init_logging__
from permedcoe.utils.environ import get_environment as __get_environment__
import permedcoe.core.environment as __cmd_flags__


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


def invoker(function, arguments_info=None) -> None:
    """ Parse the input parameters (from sys.argv) and then invoke the
    given BB function.

    Args:
        function (function): Building block function to invoke.
        arguments_info (function): Building block arguments information.
    Returns:
        None
    """
    if arguments_info:
        # Grab the BB arguments info to tune the argument parser
        if isinstance(arguments_info, str):
            # Use the parameters defined in the given file
            bb_arguments = __bb_param_loader__(arguments_info)
        else:
            # Use the given arguments
            bb_arguments = arguments_info()
        old_school_args = False
    else:
        # If set to none, use old-school inputs and outputs parameters
        bb_arguments = None
        old_school_args = True
    arguments = __bb_parser__(bb_arguments)
    if arguments.debug:
        print("Building Block arguments:\n%s" % str(bb_arguments))
    # Set execution related conditions
    __cmd_flags__.DEBUG = arguments.debug
    __cmd_flags__.DISABLE_CONTAINER = arguments.disable_container
    set_debug(arguments.debug)
    # Preprocess
    cfg = __preprocessing__(arguments)
    if old_school_args:
        # Grab input and output
        in_path = arguments.input
        out_path = arguments.output
        # Building block invocation
        function(in_path, out_path, cfg)
    else:
        # Building block invocation
        function(arguments, cfg)
