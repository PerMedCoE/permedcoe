import argparse
import os
import json
import sys

from permedcoe.utils.user_arguments import Arguments


def parse_sys_argv():
    """Parses the sys.argv.

    Args:
        None
    Returns:
        All arguments as namespace.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )  # noqa: E501
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug mode. Overrides log_level",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        help="Set logging level.",
        choices=["debug", "info", "warning", "error", "critical"],  # noqa: E501
        default="error",
        type=str,
    )

    # Parent parser - includes all arguments which are common to all actions
    parent_parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )  # noqa: E501
    # Currently empty

    # Execute sub-parser
    subparsers = parser.add_subparsers(dest="action")
    parser_execute = subparsers.add_parser(
        "execute",
        aliases=["x"],
        help="Execute a building block.",
        parents=[parent_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    subparsers_execute = parser_execute.add_subparsers(dest="execute")
    parser_execute_bb = subparsers_execute.add_parser(
        "building_block",
        aliases=["bb"],
        help="Execute a building block.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    parser_execute_bb.add_argument(
        dest="name", type=str, help="Building Block to execute"
    )
    __bb_execute_arguments__(parser_execute_bb)
    parser_execute_app = subparsers_execute.add_parser(
        "application",
        aliases=["app"],
        help="Execute an application.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    parser_execute_app.add_argument(
        dest="name", type=str, help="Application to execute"
    )
    parser_execute_app.add_argument(
        dest="parameters", type=str, nargs="*", help="Application parameters"
    )
    parser_execute_app.add_argument(
        "-w",
        "--workflow_manager",
        type=str,
        choices=["none", "pycompss", "nextflow", "snakemake"],  # noqa: E501
        default="none",
        help="Workflow manager to use",
    )
    parser_execute_app.add_argument(
        "-f", "--flags", type=str, nargs="+", help="Workflow manager flags"
    )
    # TODO: If provide support for application submission to Croupier
    # Submit sub-parser
    # parser_submit = subparsers.add_parser('submit',
    #                                       aliases=['s'],
    #                                       help='Submit an application.',
    #                                       parents=[parent_parser],
    #                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)    # noqa: E501
    # parser_submit.add_argument('-s', '--system',
    #                            dest='system',
    #                            type=str,
    #                            help='System where to submit')
    # parser_submit.add_argument(dest='name',
    #                            type=str,
    #                            help='Application name')
    # parser_submit.add_argument(dest='parameter',
    #                            type=str,
    #                            nargs='+',
    #                            help='Application parameter')

    # Templates
    parser_template = subparsers.add_parser(
        "template",
        aliases=["t"],
        help="Shows an example of the requested template.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    subparser_template = parser_template.add_subparsers(dest="template")
    parser_template_bb = subparser_template.add_parser(
        "building_block",
        aliases=["bb"],
        help="Create a building block template.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    parser_template_bb.add_argument(
        dest="name", type=str, help="Building Block to create"
    )
    parser_template_app = subparser_template.add_parser(
        "application",
        aliases=["app"],
        help="Create an application template.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    parser_template_app.add_argument(
        dest="name", type=str, help="Application to create"
    )
    parser_template_app.add_argument(
        "-t",
        "--type",
        choices=["all", "pycompss", "nextflow", "snakemake"],  # noqa: E501
        default="all",
        type=str,
        help="Application type.",
    )

    # Deploy
    parser_deploy = subparsers.add_parser(
        "deploy",
        aliases=["d"],
        help="Download and deploy the requested workflow or building block.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    subparser_deploy = parser_deploy.add_subparsers(dest="deploy")
    parser_deploy_bb = subparser_deploy.add_parser(
        "building_block",
        aliases=["bb"],
        help="A specific building block.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    parser_deploy_bb.add_argument(
        dest="name", type=str, help="Building Block to deploy."
    )
    parser_deploy_workflow = subparser_deploy.add_parser(
        "workflow",
        aliases=["app"],
        help="A specific workflow.",  # noqa: E501
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )  # noqa: E501
    parser_deploy_workflow.add_argument(
        dest="name", type=str, help="Workflow to deploy."
    )

    # Check if the user does not include any argument
    if len(sys.argv) < 2:
        #  Show the usage
        print(parser.print_usage())
        sys.exit(1)

    arguments = parser.parse_args()

    # Check if the user does not include any argument after the action
    if sys.argv[-1] in ["execute", "x", "template", "t", "deploy", "d"]:
        #  Show the usage
        action = sys.argv[-1]
        try:
            print(subparsers.choices[action].print_usage())
        except KeyError:
            print(parser.print_usage())
        sys.exit(1)

    return arguments


def single_bb_sysarg_parser(bb_arguments):
    """Parses the sys.argv.

    Args:
        bb_arguments: Building block arguments.
    Returns:
        Parsed arguments
    """
    if bb_arguments:
        # Building block detailed parser
        parser = argparse.ArgumentParser(description=bb_arguments.get_description())
        __bb_specific_arguments__(parser, bb_arguments)
    else:
        # Old-school argument parser
        parser = argparse.ArgumentParser()
        __bb_execute_arguments__(parser)
    __bb_common_arguments__(parser)
    args = parser.parse_args()

    if hasattr(args, "mode") and args.mode == None:
        #  Show the usage
        print(parser.print_help())
        print("Please, specify the appropriate parameters")
        sys.exit(1)
    elif bb_arguments:
        # Check if input file and directory arguments exist
        __bb_arguments_checks__(args, bb_arguments)
    else:
        # Check if the user does not include input and output
        if not args.input or not args.output:
            #  Show the usage
            print(parser.print_help())
            print("Please, specify input and output")
            sys.exit(1)

    return args


def __bb_arguments_checks__(args, bb_arguments):
    """Check if input file and directory arguments exist.

    Args:
        args (argparsed): Parsed arguments.
        bb_arguments (dict): BB arguments information.
    """
    if hasattr(args, "mode"):
        mode = args.mode
    else:
        mode = "default"
    arguments = bb_arguments.get_arguments()[mode]
    print(arguments)
    input_arguments = arguments.get_inputs()
    issues = []
    for k, v in input_arguments.items():
        check = v.get_check()
        to_check = vars(args)[k]
        if check == "file":
            if not os.path.isfile(to_check):
                issues.append(
                    "ERROR: Argument %s for file %s does not exist." % (k, to_check)
                )
        if check == "folder":
            if not os.path.isdir(to_check):
                issues.append(
                    "ERROR: Argument %s for directory %s does not exist."
                    % (k, to_check)
                )
    output_arguments = arguments.get_outputs()
    if issues:
        for message in issues:
            print(message)
        raise Exception("ERROR: Wrong or missing argument/s.")


def __bb_specific_arguments__(parser, bb_arguments):
    """BB specific arguments for Building block execute.

    Args:
        parser (parser): Parser to append arguments.
        bb_arguments (dict): BB arguments information.
    """
    arguments = bb_arguments.get_arguments()
    if len(arguments) == 1:
        # Only default mode
        inputs = arguments["default"].get_inputs()
        for param_name, param in inputs.items():
            help_msg = __get_help_message__("INPUT", param)
            parser_inner = parser.add_argument(
                "--%s" % param_name, help=help_msg, type=param.get_type(), required=True
            )
        outputs = arguments["default"].get_outputs()
        for param_name, param in outputs.items():
            help_msg = __get_help_message__("OUTPUT", param)
            parser_inner = parser.add_argument(
                "--%s" % param_name, help=help_msg, type=param.get_type(), required=True
            )
    else:
        # More than one mode
        subparser = parser.add_subparsers(dest="mode")
        for k, v in arguments.items():
            parser_mode = subparser.add_parser(k)
            inputs = v.get_inputs()
            for param_name, param in inputs.items():
                help_msg = __get_help_message__("INPUT", param)
                parser_inner_mode = parser_mode.add_argument(
                    "--%s" % param_name,
                    help=help_msg,
                    type=param.get_type(),
                    required=True,
                )
            outputs = v.get_outputs()
            for param_name, param in outputs.items():
                help_msg = __get_help_message__("OUTPUT", param)
                parser_inner_mode = parser_mode.add_argument(
                    "--%s" % param_name,
                    help=help_msg,
                    type=param.get_type(),
                    required=True,
                )


def __get_help_message__(param_direction, param):
    """Generate help message.

    Args:
        param_type (str): If the parameter is INPUT or OUTPUT.
        param (Argument): Parameter argument object.
    Returns:
        The message associated for the given parameter.
    """
    if param.get_check() in ["file", "folder"]:
        param_type = "%s (%s)" % (param.get_type().__name__, param.get_check())
    else:
        param_type = param.get_type().__name__
    help_msg = "(%s - %s) %s" % (param_direction, param_type, param.get_description())
    return help_msg


def __bb_execute_arguments__(parser):
    """Add old-school arguments for Building block execute.

    Args:
        parser (parser): Parser to append arguments
    """
    parser.add_argument(
        "-i", "--input", help="Input file/s or directory path/s", nargs="+", type=str
    )
    parser.add_argument(
        "-o", "--output", help="Output file/s or directory path/s", nargs="+", type=str
    )


def __bb_common_arguments__(parser):
    """Add common arguments for Building block execute.

    Args:
        parser (parser): Parser to append arguments
    """
    parser.add_argument(
        "-c", "--config", help="(CONFIG) Configuration file path", type=str
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable Building Block debug mode. Overrides log_level",  # noqa: E501
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        help="Set logging level",
        choices=["debug", "info", "warning", "error", "critical"],  # noqa: E501
        type=str,
    )
    parser.add_argument(
        "--tmpdir", help="Temp directory to be mounted in the container", type=str
    )
    parser.add_argument(
        "--processes", help="Number of processes for MPI executions", type=int
    )
    parser.add_argument("--gpus", help="Requirements for GPU jobs", type=int)
    parser.add_argument("--memory", help="Memory requirement", type=int)
    parser.add_argument(
        "--mount_points",
        help="Comma separated alias:folder to be mounted in the container",  # noqa: E501
        type=str,
    )
    # Hidden flag for advanced users
    parser.add_argument(
        "--disable_container", help=argparse.SUPPRESS, action="store_true"
    )


def load_parameters_from_json(parameters_file):
    """Load the parameters defined in the given json file.

    Args:
        parameters_file (str): File containing the parameters (json format).
    Returns:
        Loaded arguments.
    """
    with open(parameters_file, "r") as params_fd:
        raw_params = json.load(params_fd)
    # Now build the args object from raw_params
    short_description = raw_params["short_description"]
    long_description = raw_params["long_description"]
    use_description = raw_params["use_description"]
    parameters = raw_params["parameters"]

    arguments = Arguments()
    if use_description == "short":
        arguments.set_description(short_description)
    else:
        arguments.set_description(long_description)
    # just_one_mode avoids to use default as keyword
    just_one_mode = len(parameters) == 1
    for mode, params in parameters.items():
        for param in params:
            p_type = param["type"]
            p_name = param["name"]
            p_format, p_check = __convert_format__(param["format"])
            p_description = param["description"]

            if p_type == "input":
                if just_one_mode:
                    arguments.add_input(
                        name=p_name,
                        type=p_format,
                        description=p_description,
                        check=p_check,
                    )
                else:
                    arguments.add_input(
                        name=p_name,
                        type=p_format,
                        description=p_description,
                        check=p_check,
                        mode=mode,
                    )
            elif p_type == "output":
                if just_one_mode:
                    arguments.add_output(
                        name=p_name, type=p_format, description=p_description
                    )
                else:
                    arguments.add_output(
                        name=p_name, type=p_format, description=p_description, mode=mode
                    )
            else:
                raise Exception(
                    "Unexpected parameter type %s (supported input | output)"
                    % str(p_type)
                )
    return arguments


def __convert_format__(format):
    """Convert format to the actual type.

    Args:
        format (str): Input format.
    Returns:
        The supported format type and format to be checked.
    """
    if format == "str":
        return str, str
    elif format == "int":
        return int, int
    elif format == "float":
        return float, float
    elif format == "bool":
        return bool, bool
    elif format in ["file", "folder"]:
        return str, format
    else:
        raise Exception("Unsupported parameter type")
