"""
NOTE: Do not modify this file unless you want to change the name
      of the main.py file or use tmpdir is required.
      Then it is necessary to adapt the import.
"""

import os
from permedcoe import invoker
from NEW_NAME.main import invoke
from NEW_NAME.definitions import BB_SOURCE_PATH


def main():
    invoker(invoke, os.path.join(BB_SOURCE_PATH, "definition.json"))  # TODO: Add require_tmpdir=True if the asset requires to write within the tmpdir.


if __name__ == "__main__":
    main()
