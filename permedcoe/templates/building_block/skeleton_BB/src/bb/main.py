#!/usr/bin/python3

from permedcoe import container        # To define container related needs
from permedcoe import binary           # To define binary to execute related needs
from permedcoe import task             # To define task related needs

from permedcoe import FILE_IN          # To define file type and direction
from permedcoe import FILE_OUT         # To define file type and direction
from permedcoe import DIRECTORY_IN     # To define directory type and direction
from permedcoe import DIRECTORY_OUT    # To define directory type and direction

from permedcoe import get_environment  # Get variables from invocation (tmpdir, processes, gpus, memory)


# Single and global container definition for this building block
SAMPLE_CONTAINER = "/path/to/image.sif"  # TODO: Define your container


def function_name(*args, **kwargs):
    """ Extended python interface:
    To be used only with PyCOMPSs - Enables to define a workflow within the building block.
    Tasks are not forced to be binaries: PyCOMPSs supports tasks that are pure python code.

    # PyCOMPSs help: https://pycompss.readthedocs.io/en/latest/Sections/02_App_Development/02_Python.html

    Requirement: all tasks should be executed in a container (with the same container definition)
                 to ensure that they all have the same requirements.
    """
    print("Building Block entry point to be used with PyCOMPSs")
    # TODO: (optional) Pure python code calling to PyCOMPSs tasks (that can be defined in this file or in another).


@container(engine="SINGULARITY", image=SAMPLE_CONTAINER)
@binary(binary="/path/to/my_binary")                      # TODO: Define the binary to be used.
@task(dataset=FILE_IN, output=FILE_OUT)                   # TODO: Define the inputs and output parameters.
def building_block_task(dataset_flag="-d", dataset=None,  # TODO: Define a representative task name
                        output_flag="-o", output=None,
                        operation="-x"):                  # TODO: Define the binary parameters
    # The Definition is equal to:
    #    /path/to/my_binary -d dataset -o output -x
    # Empty function since it represents a binary execution:
    pass


def invoke(input, output, config):
    """ Common interface.

    Args:
        input (str): Input file path.
        output (str): Output directory path.
        config (dict): Configuration dictionary.
    Returns:
        None
    """
    # TODO: Declare how to run the binary specification (convert config into building_block_task call)
    operation = config["operation"]
    # env_vars = get_environment()  # NOSONAR - Retrieves the extra flags.
    building_block_task(dataset=input,
                        output=output,
                        operation=operation)
