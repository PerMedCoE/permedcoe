import os
import importlib
import logging
import pathlib
import shutil
import subprocess
import sys
import urllib.request
from urllib.error import HTTPError
import zipfile

from permedcoe.base import invoker
from permedcoe.bb import get_container_path
from permedcoe.utils.log import init_logging
from permedcoe.utils.executor import command_runner
from permedcoe.utils.artifact import adapt_name
from permedcoe.utils.artifact import rename_folder
from permedcoe.utils.artifact import show_todo


BUILDING_BLOCK_LABELS = ("building_block", "bb")
APPLICATION_LABELS = ("application", "app")


def execute_building_block(arguments):
    """Execute the requested building block.

    Args:
        arguments (Namespace): System arguments.
    """
    # Building block invocation
    building_block = arguments.name
    logging.info("Executing Building Block: %s" % str(building_block))
    bb_module = importlib.import_module(building_block)
    invoke_function = getattr(bb_module, "invoke")
    # Check if json with parameters is defined
    params_json_file = os.path.join(bb_module.__path__[0], "definition.json")
    if os.path.isfile(params_json_file):
        __set_bb_sysargv__(building_block)
        invoker(invoke_function, params_json_file)
    else:
        try:
            __set_bb_sysargv__(building_block)
            arguments_function = getattr(bb_module, "arguments_info")
            invoker(invoke_function, arguments_function)
        except AttributeError:
            # old school BB
            invoker(invoke_function)


def __set_bb_sysargv__(name):
    """Removes the unnecessary parameters from sys.argv so that
    the building block invocation does not fail.

    Args:
        name (str): Building block name.
    """
    reset_args_index = sys.argv.index(name) + 1
    new_args = [sys.argv[0]] + sys.argv[reset_args_index:]
    sys.argv = new_args


def execute_application(arguments):
    """Execute the requested building block.

    Args:
        arguments (Namespace): System arguments.
    """
    # Application related arguments
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
    """Creates a building block or application template.

    Args:
        debug (bool): Force debug mode.
        log_level (str): Log level.
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
        print(
            "Can not create template. A folder with name %s already exists." % str(name)
        )  # noqa: E501
        exit(1)
    # Prepare source
    egg_path = pathlib.Path(__file__).parent.parent.absolute()
    source_path = os.path.join(egg_path, "templates")
    # Choose what to extract to this folder
    if artifact in BUILDING_BLOCK_LABELS:
        print("Creating Building Block template")
        skeleton_path = os.path.join(source_path, "building_block", "skeleton_BB")
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


def deploy_bb(debug, log_level, name):
    """Deploys the requested building block.

    Args:
        debug (bool): Force debug mode.
        log_level (str): Log level.
        name (str): Building block name.

    Raises:
        Exception: Not found building block.
    """
    # Init logging
    init_logging(debug, log_level)
    logging.debug("Checking Building Block: %s" % str(name))
    __deploy_bb__(name)


def __deploy_bb__(name):
    """Deploys the requested building block.

    Args:
        name (str): Building block name.

    Raises:
        Exception: Not found building block.
    """
    url = "https://github.com/PerMedCoE/BuildingBlocks/tree/main/%s" % str(name)
    bb_exists = __check_url__(url)
    container_folder = get_container_path()
    if bb_exists:
        __install_bb__(name)
        __deploy_container__(name, container_folder)
    else:
        print("ERROR: Building Block %s not found." % str(name))


def __install_bb__(name):
    """Install the required building block.

    Args:
        name (str): Building block name.
    """
    cmd = ["python3",
           "-m",
           "pip",
           "install",
           "git+https://github.com/PerMedCoE/BuildingBlocks.git@main#subdirectory=%s" % str(name)
    ]
    logging.debug("Installing Building Block %s" % str(name))
    command_runner(cmd)


def __deploy_container__(name, container_folder):
    """Donwload and deploy the building block associated container.

    Args:
        name (str): Building block name.
        container_folder (str): Container destination folder.
    """
    bb_module = importlib.import_module(name + "_BB")
    container_name = bb_module.definitions.CONTAINER
    if isinstance(container_name, list):
        # More than one container required
        logging.debug("More than one container required for this Building Block: %s" % container_name)
        for container in container_name:
            __download_container__(name, container_folder)
    elif isinstance(container_name, str):
        # Single container required
        logging.debug("One container required for this Building Block: %s" % container_name)
        __download_container__(name, container_folder)
    else:
        raise Exception("ERROR: Container name must be string or list of strings. Not: %s" % container_name)


def __download_container__(name, container_folder):
    """Donwload the building block associated container.

    Args:
        name (str): Building block name.
        container_folder (str): Container destination folder.
    """
    container_file = os.path.join(container_folder, name + ".sif")
    if os.path.exists(container_file) and os.path.isfile(container_file):
        logging.debug("Container %s already exists" % name)
    else:
        logging.debug("Downloading %s container" % name)
        cmd = [
            "apptainer",
            "pull",
            container_file,
            "docker://ghcr.io/jaantollander/%s:latest" % name
        ]
        command_runner(cmd)


def deploy_workflow(debug, log_level, name):
    """Deploys the requested workflow.

    Args:
        debug (bool): Force debug mode.
        log_level (str): Log level.
        name (str): Workflow name.

    Raises:
        Exception: Not found workflow.
    """
    # Init logging
    init_logging(debug, log_level)
    logging.debug("Checking Workflow: %s" % str(name))
    url = "https://github.com/PerMedCoE/%s/" % str(name)
    workflow_exists = __check_url__(url)
    if workflow_exists:
        logging.debug("Found Workflow: %s" % str(url))
        zip_file = "https://github.com/PerMedCoE/%s/archive/refs/heads/main.zip" % str(
            name
        )
        # Check if exists a file called main.zip in this folder before continuing
        logging.debug("Checking if associated zip file exists: %s" % str(zip_file))
        zip_exists = __check_url__(zip_file)
        if zip_exists:
            logging.debug("Found zip file: %s" % str(zip_file))
            # Download zip file in the current folder
            current_folder = os.getcwd()
            target_file = os.path.join(current_folder, "main.zip")
            if os.path.exists(target_file):
                print("ERROR: A file named %s already exists." % str(target_file))
                print(
                    "       Please, try again in another folder or remove the existing 'main.zip' file."
                )
            else:
                # file with the same name does not exist in the current folder
                logging.debug("Downloading zip file: %s" % str(zip_file))
                con = urllib.request.urlopen(zip_file)
                with con as dl_zip_file:
                    with open(target_file, "wb") as out_file:
                        out_file.write(dl_zip_file.read())
                logging.debug("Downloaded into: %s" % str(target_file))
                # Unzip the downloaded file
                logging.debug("Unzipping file: %s" % str(target_file))
                with zipfile.ZipFile(target_file, "r") as zip_ref:
                    zip_ref.extractall(current_folder)
                extracted_folder = os.path.join(current_folder, "%s-main" % str(name))
                logging.debug(
                    "Unzipped file into the folder: %s" % str(extracted_folder)
                )
                # Rename folder
                target_folder = os.path.join(current_folder, str(name))
                logging.debug(
                    "Renaming folder: %s to %s"
                    % (str(extracted_folder), str(target_folder))
                )
                if os.path.exists(target_folder):
                    print(
                        "ERROR: A folder named %s already exists." % str(target_folder)
                    )
                    print(
                        "       Please, try again in another folder or remove the existing folder."
                    )
                else:
                    shutil.move(extracted_folder, target_folder)
                    logging.debug("Final folder: %s" % str(target_folder))
                # Clean main.zip (downloaded file)
                logging.debug("Cleaning downloaded file: %s" % str(target_file))
                os.remove(target_file)
                print("SUCCESS: Workflow deployed.")
                # Now install the workflow associated building blocks
                logging.debug("Installing workflow building blocks.")
                bb_installed = __install_workflow_building_blocks__(target_folder)
                if bb_installed:
                    print(
                        "SUCCESS: Building Blocks for %s successfully installed."
                        % str(name)
                    )
                    # Finally, give next steps information
                    __show_instructions__(target_folder, str(name))
                else:
                    print("ERROR: Could not install the necessary Building Blocks")
        else:
            print("ERROR: Could not found workflow %s zip file." % str(name))
    else:
        print("ERROR: Workflow %s not found." % str(name))


def __check_url__(url):
    """Checks if the given url exists.

    Args:
        url (str): Url to check.

    Return:
        Boolean: If the url exists.
    """
    try:
        status_code = urllib.request.urlopen(url).getcode()
    except HTTPError:
        return False
    return status_code == 200


def __install_workflow_building_blocks__(workflow_path):
    """Runs the install script within the workflow path that downloads and installs
    its necessary building blocks.

    Args:
        workflow_path (str): Directory that contains a workflow.

    Return:
        Boolean: True if success. False otherwise
    """
    wf_required_bbs = os.path.join(workflow_path, "BuildingBlocks", "required_BBs.txt")
    if os.path.exists(wf_required_bbs) and os.path.isfile(wf_required_bbs):
        required_bbs = []
        with open(wf_required_bbs) as fd:
            for line in fd:
                l = line.strip()
                if not l.startswith("#"):
                    required_bbs.append(l)
        for bb in required_bbs:
            __deploy_bb__(bb)
        return True
    else:
        print("ERROR: Could not install the workflow building blocks.")
        print("REASON: Does not contain the required Building Blocks file: %s" % str(wf_required_bbs))
        print("        Please, contact PerMedCoE team in order to fix it (https://permedcoe.eu/contact/).")
        return False


def __show_instructions__(target_folder, name):
    """Shows instruction about the recently deployed workflow.

    Args:
        target_folder (str): Directory that contains a workflow.
        name (str): workflow name.
    """
    print("\nINFORMATION:\n")
    print("\t- The workflow has been deployed in: %s" % target_folder)
    print("\t- Its associated building blocks have been installed.")
    print("\nNEXT STEPS:\n")
    print("\t- 1st: Make sure that you have installed the desired workflow manager:")
    print("\t       Currently supported: PyCOMPSs, Snakemake and NextFlow.")
    print("\t- 2nd: Go to the workflow folder: For example:")
    sample_path = os.path.join(target_folder, "Workflow", "PyCOMPSs")
    print("\t       cd %s" % sample_path)
    print(
        "\t- 3rd: Check if the workflow requires to prepare the sample dataset. For example:"
    )
    print("\t       ./0_preparse_datset.sh")
    print("\t       If it does not exist, then you can skip this step.")
    print("\t- 4th: Locate and run the execution script. For example:")
    print("\t       ./run.sh")
    print(
        "\t       CAUTION 1: Some workflows may have more than one run scripts with different parameters (e.g. a_run.sh)."
    )
    print(
        "\t       CAUTION 2: launch.sh scripts are aimed to be used in supercomputers."
    )
    print(
        "\nFor more information, please check the workflow documentation: https://github.com/PerMedCoE/%s"
        % name
    )
