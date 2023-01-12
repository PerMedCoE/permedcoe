#!/usr/bin/python3

from permedcoe.utils.arguments import parse_sys_argv as __parse_sys_argv__
from permedcoe.core.functions import (
    execute_building_block as __execute_building_block__,
)
from permedcoe.core.functions import execute_application as __execute_application__
from permedcoe.core.functions import create_template as __create_template__
from permedcoe.core.functions import deploy_bb as __deploy_bb__
from permedcoe.core.functions import deploy_workflow as __deploy_workflow__


def main():
    """
    Main entry point for the "permedcoe" executable.
    """
    # Parse sys.argv
    arguments = __parse_sys_argv__()
    debug = True if arguments.debug else False
    # Action selector
    if arguments.action in ["execute", "x"]:
        if arguments.execute in ["building_block", "bb"]:
            if debug:
                print("Executing Building Block")
            __execute_building_block__(arguments)
        if arguments.execute in ["application", "app"]:
            if debug:
                print("Executing Application")
            __execute_application__(arguments)
    if arguments.action in ["submit", "s"]:
        if debug:
            print("Submit Application")
        raise NotImplementedError
    if arguments.action in ["template", "t"]:
        if arguments.template in ["building_block", "bb"]:
            app_type = None
            if debug:
                print("Creating building block template")
        else:
            app_type = arguments.type
            if debug:
                print("Creating application template")
        __create_template__(
            arguments.debug,
            arguments.log_level,
            arguments.template,
            arguments.name,
            app_type,
        )
    if arguments.action in ["deploy", "d"]:
        if arguments.deploy in ["building_block", "bb"]:
            if debug:
                print("Deploying Building Block")
            __deploy_bb__(arguments.debug, arguments.log_level, arguments.name)
        else:
            if debug:
                print("Deploying Workflow")
            __deploy_workflow__(arguments.debug, arguments.log_level, arguments.name)


if __name__ == "__main__":
    main()
