import os
import sys
import argparse


def parse_sys_argv():
    """ Parses the sys.argv.

    Args:
        None
    Returns:
        All arguments as namespace.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)         # noqa: E501
    parser.add_argument("-d", "--debug",
                        help="Enable debug mode. Overrides log_level",
                        action="store_true")
    parser.add_argument("-l", "--log_level",
                        help="Set logging level.",
                        choices=["debug", "info", "warning", "error", "critical"],                   # noqa: E501
                        default="error",
                        type=str)

    # Parent parser - includes all arguments which are common to all actions
    parent_parser = argparse.ArgumentParser(add_help=False,
                                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # noqa: E501
    # Currently empty

    # Execute sub-parser
    subparsers = parser.add_subparsers(dest='action')
    parser_execute = subparsers.add_parser('execute',
                                           aliases=['x'],
                                           help='Execute a building block.',
                                           parents=[parent_parser],
                                           formatter_class=argparse.ArgumentDefaultsHelpFormatter)   # noqa: E501
    subparsers_execute = parser_execute.add_subparsers(dest='execute')
    parser_execute_bb = subparsers_execute.add_parser('building_block',
                                                      aliases=['bb'],
                                                      help='Execute a building block.',                        # noqa: E501
                                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # noqa: E501
    parser_execute_bb.add_argument(dest='name',
                                   type=str,
                                   help='Building Block to execute')
    __bb_execute_arguments__(parser_execute_bb)
    parser_execute_app = subparsers_execute.add_parser('application',
                                                       aliases=['app'],
                                                       help='Execute an application.',                          # noqa: E501
                                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # noqa: E501
    parser_execute_app.add_argument(dest='name',
                                    type=str,
                                    help='Application to execute')
    parser_execute_app.add_argument(dest='parameters',
                                    type=str,
                                    nargs='*',
                                    help='Application parameters')
    parser_execute_app.add_argument('-w', '--workflow_manager',
                                    type=str,
                                    choices=["none", "pycompss", "nextflow", "snakemake"],           # noqa: E501
                                    default="none",
                                    help='Workflow manager to use')
    parser_execute_app.add_argument('-f', '--flags',
                                    type=str,
                                    nargs='+',
                                    help='Workflow manager flags')
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
    parser_template = subparsers.add_parser('template',
                                            aliases=['t'],
                                            help='Shows an example of the requested template.',      # noqa: E501
                                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # noqa: E501
    subparser_template = parser_template.add_subparsers(dest='template')
    parser_template_bb = subparser_template.add_parser('building_block',
                                                       aliases=['bb'],
                                                       help='Create a building block template.',                # noqa: E501
                                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # noqa: E501
    parser_template_bb.add_argument(dest='name',
                                    type=str,
                                    help='Building Block to create')
    parser_template_app = subparser_template.add_parser('application',
                                                        aliases=['app'],
                                                        help='Create an application template.',                  # noqa: E501
                                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # noqa: E501
    parser_template_app.add_argument(dest='name',
                                     type=str,
                                     help='Application to create')
    parser_template_app.add_argument('-t', '--type',
                                     choices=["all", "pycompss", "nextflow", "snakemake"],  # noqa: E501
                                     default="all",
                                     type=str,
                                     help='Application type.')

    # Check if the user does not include any argument
    if len(sys.argv) < 2:
        #  Show the usage
        print(parser.print_usage())
        sys.exit(1)

    arguments = parser.parse_args()

    # Check if the user does not include any argument after the action
    if sys.argv[-1] in ["execute", "x", "template", "t"]:
        #  Show the usage
        action = sys.argv[-1]
        try:
            print(subparsers.choices[action].print_usage())
        except KeyError:
            print(parser.print_usage())
        sys.exit(1)

    return arguments


def single_bb_sysarg_parser(bb_arguments):
    """ Parses the sys.argv.

    Args:
        bb_arguments: Building block arguments.
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser()
    if bb_arguments:
        # Building block detailed parser
        __bb_specific_arguments__(parser, bb_arguments)
    else:
        # Old-school argument parser
        __bb_execute_arguments__(parser)
    __bb_common_arguments__(parser)
    args = parser.parse_args()

    # Check if input file and directory arguments exist
    __bb_arguments_checks__(args, bb_arguments)

    if bb_arguments is None:
        # Check if the user does not include input and output
        if not args.input or not args.output:
            #  Show the usage
            print(parser.print_usage())
            print("Please, specify input and output")
            sys.exit(1)

    return args


def __bb_arguments_checks__(args, bb_arguments):
    """ Check if input file and directory arguments exist.

    Args:
        args (argparsed): Parsed arguments.
        bb_arguments (dict): BB arguments information.
    """
    mode = args.mode
    arguments = bb_arguments.get_arguments()[mode]
    print(arguments)
    input_arguments = arguments.get_inputs()
    issues = []
    for k, v in input_arguments.items():
        check = v.get_check()
        to_check = vars(args)[k]
        if check == "file":
            if not os.path.isfile(to_check):
                issues.append("ERROR: Argument %s for file %s does not exist." % (k, to_check))
        if check == "folder":
            if not os.path.isdir(to_check):
                issues.append("ERROR: Argument %s for directory %s does not exist." % (k, to_check))
    output_arguments = arguments.get_outputs()
    if issues:
        for message in issues:
            print(message)
        raise Exception("ERROR: Wrong or missing argument/s.")


def __bb_specific_arguments__(parser, bb_arguments):
    """ BB specific arguments for Building block execute.

    Args:
        parser (parser): Parser to append arguments.
        bb_arguments (dict): BB arguments information.
    """
    arguments = bb_arguments.get_arguments()
    if len(arguments) == 1:
        # Only default mode
        inputs = arguments["default"].get_inputs()
        for param_name, param in inputs.items():
            parser_inner = parser.add_argument("--%s" % param_name,
                                               help="(INPUT) %s" % param.get_description(),
                                               type=param.get_type(),
                                               required=True)
        outputs = arguments["default"].get_outputs()
        for param_name, param in outputs.items():
            parser_inner = parser.add_argument("--%s" % param_name,
                                               help="(OUTPUT) %s" % param.get_description(),
                                               type=param.get_type(),
                                               required=True)
    else:
        # More than one mode
        subparser = parser.add_subparsers(dest="mode")
        for k, v in arguments.items():
            parser_mode = subparser.add_parser(k)
            inputs = v.get_inputs()
            for param_name, param in inputs.items():
                parser_inner_mode = parser_mode.add_argument("--%s" % param_name,
                                                             help="(INPUT) %s" % param.get_description(),
                                                             type=param.get_type(),
                                                             required=True)
            outputs = v.get_outputs()
            for param_name, param in outputs.items():
                parser_inner_mode = parser_mode.add_argument("--%s" % param_name,
                                                             help="(OUTPUT) %s" % param.get_description(),
                                                             type=param.get_type(),
                                                             required=True)


def __bb_execute_arguments__(parser):
    """ Add old-school arguments for Building block execute.

    Args:
        parser (parser): Parser to append arguments
    """
    parser.add_argument("-i", "--input",
                        help="Input file/s or directory path/s",
                        nargs="+",
                        type=str)
    parser.add_argument("-o", "--output",
                        help="Output file/s or directory path/s",
                        nargs="+",
                        type=str)


def __bb_common_arguments__(parser):
    """ Add common arguments for Building block execute.

    Args:
        parser (parser): Parser to append arguments
    """
    parser.add_argument("-c", "--config",
                    help="(CONFIG) Configuration file path",
                    type=str)
    parser.add_argument("-d", "--debug",
                        help="Enable Building Block debug mode. Overrides log_level",        # noqa: E501
                        action="store_true")
    parser.add_argument("-l", "--log_level",
                        help="Set logging level",
                        choices=["debug", "info", "warning", "error", "critical"],           # noqa: E501
                        type=str)
    parser.add_argument("--tmpdir",
                        help="Temp directory to be mounted in the container",
                        type=str)
    parser.add_argument("--processes",
                        help="Number of processes for MPI executions",
                        type=int)
    parser.add_argument("--gpus",
                        help="Requirements for GPU jobs",
                        type=int)
    parser.add_argument("--memory",
                        help="Memory requirement",
                        type=int)
    parser.add_argument("--mount_points",
                        help="Comma separated alias:folder to be mounted in the container",  # noqa: E501
                        type=str)
    # Hidden flag for advanced users
    parser.add_argument("--disable_container",
                        help=argparse.SUPPRESS,
                        action="store_true")
