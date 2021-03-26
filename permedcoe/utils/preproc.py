import yaml
import logging

from permedcoe.utils.log import init_logging
from permedcoe.utils.environ import set_environment
import permedcoe.core.environment as cmd_flags



def preprocessing(arguments):
    # Parse configuration file
    if arguments.config:
        with open(arguments.config, "r") as config_fd:
            cfg = yaml.safe_load(config_fd)
    else:
        cfg = None
    # Initialize logging
    init_logging(arguments.debug, arguments.log_level)
    # Global environment flags from command line
    cmd_flags.DEBUG = arguments.debug
    cmd_flags.DISABLE_CONTAINER = arguments.disable_container
    # Export variables
    set_environment(arguments.tmpdir,
                    arguments.processes,
                    arguments.gpus,
                    arguments.memory,
                    arguments.mount_points)
    # Show arguments
    logging.debug("Arguments:")
    for param, value in arguments.__dict__.items():
        logging.debug("\t - " + str(param) + " : " + str(value))
    return cfg
