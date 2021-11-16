#!/usr/bin/python3

import sys

# To set building block debug mode
from permedcoe import set_debug
# TODO: Import the desired building blocks entry points and use invoke or any other function.
from my_building_block import invoke
from my_building_block import building_block_task


def main():
    # Enable set_debug to have a more verbose output
    set_debug(False)
    # Sample application:
    print("Sample python application using my_building_block BB")
    # Get parameters
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    conf = {}  # conf is empty since it is not used by my_building_block
    # Building Block invocation
    building_block_task(input_file=input_file,
                        output_file=output_file)
    # Alternative Building Block invocation (uning invoke method)
    # invoke(input_file,
    #        output_file)


if __name__ == "__main__":
    main()
