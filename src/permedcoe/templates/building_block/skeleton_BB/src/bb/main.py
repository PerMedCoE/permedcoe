# Decorator imports
from permedcoe import constraint       # To define constraints needs (e.g. number of cores)
from permedcoe import container        # To define container related needs
from permedcoe import binary           # To define binary to execute related needs
from permedcoe import mpi              # To define an mpi binary to execute related needs (can not be used with @binary)
from permedcoe import task             # To define task related needs
# @task supported types
from permedcoe import FILE_IN          # To define file type and direction
from permedcoe import FILE_OUT         # To define file type and direction
from permedcoe import FILE_INOUT       # To define file type and direction
from permedcoe import DIRECTORY_IN     # To define directory type and direction
from permedcoe import DIRECTORY_OUT    # To define directory type and direction
from permedcoe import DIRECTORY_INOUT  # To define directory type and direction
# Other permedcoe available functionalities
from permedcoe import Arguments        # Arguments definition
from permedcoe import get_environment  # Get variables from invocation (tmpdir, processes, gpus, memory)
from permedcoe import TMPDIR           # Default tmpdir key

# Import single container and assets definitions
from NEW_NAME.definitions import ASSETS_PATH  # binary could be in this folder
from NEW_NAME.definitions import CONTAINER
from NEW_NAME.definitions import COMPUTING_UNITS


def function_name(*args, **kwargs):
    """Extended python interface:
    To be used only with PyCOMPSs - Enables to define a workflow within the building block.
    Tasks are not forced to be binaries: PyCOMPSs supports tasks that are pure python code.

    # PyCOMPSs help: https://pycompss.readthedocs.io/en/latest/Sections/02_App_Development/02_Python.html

    Requirement: all tasks should be executed in a container (with the same container definition)
                 to ensure that they all have the same requirements.
    """
    print("Building Block entry point to be used with PyCOMPSs")
    # TODO: (optional) Pure python code calling to PyCOMPSs tasks (that can be defined in this file or in another).


@container(engine="SINGULARITY", image=CONTAINER)
@binary(binary="cp")                                        # TODO: Define the binary to be used (can be within ASSETS_PATH (e.g. my_binary.sh)).
@task(input_file=FILE_IN, output_file=FILE_OUT)             # TODO: Define the inputs and output parameters.
def building_block_task(                                    # TODO: Define a representative task name.
    input_file=None,                                        # TODO: Define the binary parameters.
    output_file=None,                                       # TODO: Define the binary parameters.
    verbose="-v"):                                          # TODO: Define the binary parameters.
    # TODO: Add tmpdir=TMPDIR if the tmpdir will be used by the asset script.
    """Summary.

    The Definition is equal to:
       cp <input_file> <output_file> -v
    Empty function since it represents a binary execution:

    :param input_file: Input file description, defaults to None
    :type input_file: str, optional
    :param verbose: Verbose description, defaults to "-v"
    :type verbose: str, optional
    # :param tmpdir: Temporary directory, defaults to TMPDIR
    # :type tmpdir: str, optional
    """
    pass


def invoke(arguments, config):
    """Common interface.

    Args:
        arguments (args): Building Block parsed arguments.
        config (dict): Configuration dictionary.
    Returns:
        None
    """
    # TODO: Define the arguments required by the Building Block in definition.json file.

    # TODO: Declare how to run the binary specification (convert config into building_block_task call).
    # Sample config parameter get:
    #     operation = config["operation"]
    # Then operation can be used to tune the building_block_task parameters or even be a parameter.
    # Sample permedcoe environment get:
    #     env_vars = get_environment()
    # Retrieves the extra flags from permedcoe.
    input_file = arguments.model
    output_file = arguments.result
    # tmpdir = arguments.tmpdir
    building_block_task(input_file=input_file,
                        output_file=output_file)
                        # tmpdir=tmpdir)
