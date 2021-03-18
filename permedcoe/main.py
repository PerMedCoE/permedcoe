#!/usr/bin/python3

from permedcoe.utils.arguments import parse_sys_argv \
    as __parse_sys_argv__
from permedcoe.core.functions import execute_building_block \
    as __execute_building_block__
from permedcoe.core.functions import execute_application \
    as __execute_application__
from permedcoe.core.functions import create_template \
    as __create_template__


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
        if debug:
            print("Creating template")
        __create_template__(arguments.debug,
                            arguments.log_level,
                            arguments.template,
                            arguments.name,
                            arguments.type)


if __name__ == "__main__":
    main()
