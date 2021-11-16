#!/usr/bin/python3
import os

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
from permedcoe import get_environment  # Get variables from invocation (tmpdir, processes, gpus, memory)


# Single and global container definition for this building block
SAMPLE_CONTAINER = "/PATH/TO/container/sample.sif"  # TODO: Define your container


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
@binary(binary="cp")                                        # TODO: Define the binary to be used.
@task(dataset=FILE_IN, output_dir=DIRECTORY_OUT)            # TODO: Define the inputs and output parameters.
def building_block_task(dataset=None,                       # TODO: Define a representative task name
                        target_flag="-t", output_dir=None,
                        verbose="-v"):                      # TODO: Define the binary parameters
    # The Definition is equal to:
    #    cp <dataset> -t <output_dir> -v
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
    # Sample config parameter get:
    #     operation = config["operation"]
    # Then operation can be used to tune the building_block_task parameters or even be a parameter.
    # Sample permedcoe environment get:
    #     env_vars = get_environment()
    # Retrieves the extra flags from permedcoe.
    dataset = input[0]
    output_dir = output[0]
    os.mkdir(output_dir)
    building_block_task(dataset=dataset,
                        output_dir=output_dir)
