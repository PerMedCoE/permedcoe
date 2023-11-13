import os
from permedcoe.core.constants import SEPARATOR

DO_NOT_PARSE = (".pyc", ".def", ".sif")
PARSING_KEY = "NEW_NAME"
PARSING_PATH = "/PATH/TO/"


def adapt_name(name, path):
    """Replace recursively into the given path they keyword with name.
    Like a set recursively.

    Args:
        name (str): Name to personalize the files.
        path (str): Path to find the files.
    """
    template_path = path + "/"
    for directory_name, _, files in os.walk(path):
        for file_name in files:
            if not file_name.endswith(DO_NOT_PARSE):
                file_path = os.path.join(directory_name, file_name)
                with open(file_path) as file_descriptor:
                    content = file_descriptor.read()
                content = content.replace(PARSING_KEY, name)
                content = content.replace(PARSING_PATH, template_path)
                with open(file_path, "w") as file_descriptor:
                    file_descriptor.write(content)


def rename_folder(name, path):
    """Adapt the building block folder name.

    Args:
        name (str): Name to personalize the folder name.
        path (str): Path to find the files.
    """
    source = os.path.join(path, "src", "bb")
    destination = os.path.join(path, "src", name)
    os.rename(source, destination)


def show_todo(path):
    """Show on the screen all to do messages.

    Args:
        path (str): Artifact path.
    """
    print(SEPARATOR)
    print("To be completed:")
    print()
    for directory_name, _, files in os.walk(path):
        for file_name in files:
            if not file_name.endswith(DO_NOT_PARSE):
                file_path = os.path.join(directory_name, file_name)
                __show_work__(file_path)
    print(SEPARATOR)


def __show_work__(file_path):
    """Show the TODO messages of a given set of lines.

    Args:
        file_path (str): File to be analyzed.
    """
    with open(file_path) as file_descriptor:
        lines = file_descriptor.readlines()
    position = 0
    for line in lines:
        if "TODO" in line:
            _, message = line.split("#")
            file_name = str(os.path.basename(file_path))
            stripped_message = str(message).strip()
            print(f"- {file_name}:({position}):\t{stripped_message}")
        position += 1
