import os
import importlib
import logging
import pathlib
import shutil

from permedcoe.utils.preproc import preprocessing
from permedcoe.utils.log import init_logging
from permedcoe.utils.executor import command_runner
from permedcoe.utils.artifact import adapt_name
from permedcoe.utils.artifact import rename_folder
from permedcoe.utils.artifact import show_todo


BUILDING_BLOCK_LABELS = ("building_block", "bb")
APPLICATION_LABELS = ("application", "app")


def execute_building_block(arguments):
    """ Execute the requested building block.

    Args:
        arguments (Namespace): System arguments.
    """
    # Grab input and output
    in_path = arguments.input
    out_path = arguments.output
    # Preprocess
    cfg = preprocessing(arguments)
    # Building block invocation
    building_block = arguments.name
    logging.info("Executing Building Block: %s" % str(building_block))
    bb_module = importlib.import_module(building_block)
    invoke = getattr(bb_module, "invoke")
    invoke(in_path, out_path, cfg)


def execute_application(arguments):
    """ Execute the requested building block.

    Args:
        arguments (Namespace): System arguments.
    """
    app_name = arguments.name
    app_parameters = arguments.parameters
    workflow_manager = arguments.workflow_manager
    workflow_flags = arguments.flags
    # Init logging
    init_logging(arguments.debug, arguments.log_level)
    logging.info("Executing Application: %s" % str(app_name))
    logging.info("Parameters: %s" % str(app_parameters))
    logging.info("Workflow manager: %s" % str(workflow_manager))
    logging.info("Workflow flags: %s" % str(workflow_flags))
    # Workflow manager selector
    command = []
    if workflow_manager == "pycompss":
        command.append("runcompss")
    elif workflow_manager == "nextflow":
        command.append("nextflow")
    elif workflow_manager == "snakemake":
        command.append("snakemake")
    else:
        command.append("python3")
    if workflow_flags:
        for flag in workflow_flags:
            command += flag.split()
    if workflow_manager == "snakemake":
        command.append("--snakefile")
    command.append(app_name)
    if app_parameters:
        for parameter in app_parameters:
            command += parameter.split()
    command_runner(command)


def create_template(debug, log_level, artifact, name, app_type=None):
    """ Creates a building block or application template.

    Args:
        artifact (str): Artifact (building block or application)
        name (str): Artifact name
        type (str): Specific type of application (ignored for building blocks)

    Raises:
        Exception: Unsupported artifact
    """
    # Init logging
    init_logging(debug, log_level)
    # Prepare destination
    current_path = pathlib.Path().absolute()
    if os.path.exists(os.path.join(current_path, name)):
        print("Can not create template. A folder with name %s already exists." % str(name))  # noqa: E501
        exit(1)
    # Prepare source
    egg_path = pathlib.Path(__file__).parent.parent.absolute()
    source_path = os.path.join(egg_path, "templates")
    # Choose what to extract to this folder
    if artifact in BUILDING_BLOCK_LABELS:
        print("Creating Building Block template")
        skeleton_path = os.path.join(source_path,
                                     "building_block",
                                     "skeleton_BB")
    elif artifact in APPLICATION_LABELS:
        print("Creating Application template")
        app_path = os.path.join(source_path, "application")
        if app_type == "pycompss":
            skeleton_path = os.path.join(app_path, "PyCOMPSs")
        elif app_type == "nextflow":
            skeleton_path = os.path.join(app_path, "NextFlow")
        elif app_type == "snakemake":
            skeleton_path = os.path.join(app_path, "SnakeMake")
        else:
            skeleton_path = app_path
    else:
        raise Exception("Unrecognized template type: %s" % str(artifact))
    # Copy from sources to destination
    destination_path = os.path.join(current_path, name)
    logging.debug("Copying artifact to: %s" % str(destination_path))
    shutil.copytree(skeleton_path, destination_path)
    # Adapt name into the files
    logging.debug("Adapting name: %s to the artifact" % str(name))
    adapt_name(name, destination_path)
    # Adapt folder name if needed
    if artifact in BUILDING_BLOCK_LABELS:
        # Rename folder
        logging.debug("Adapting building block source folder name")
        rename_folder(name, destination_path)
        logging.debug("Artifact created")
    # Show TODO messages
    show_todo(destination_path)
