import os
from permedcoe.core.constants import SEPARATOR

DO_NOT_PARSE = (".pyc")


def adapt_name(name, path):
    """ Replace recursively into the given path they keyword with name.
    Like a set recursively.

    Args:
        name (str): Name to personalize the files.
        path (str): Path to find the files.
    """
    for directory_name, dirs, files in os.walk(path):
        for file_name in files:
            if not file_name.endswith(DO_NOT_PARSE):
                file_path = os.path.join(directory_name, file_name)
                with open(file_path) as f:
                    s = f.read()
                s = s.replace("NEW_NAME", name)
                with open(file_path, "w") as f:
                    f.write(s)


def rename_folder(name, path):
    """ Adapt the building block folder name.

    Args:
        name (str): Name to personalize the folder name.
        path (str): Path to find the files.
    """
    source = os.path.join(path, "src", "bb")
    destination = os.path.join(path, "src", name)
    os.rename(source, destination)


def show_todo(path):
    """ Show on the screen all to do messages.

    Args:
        path (str): Artifact path.
    """
    print(SEPARATOR)
    print("To be completed:")
    print()
    for directory_name, dirs, files in os.walk(path):
        for file_name in files:
            if not file_name.endswith(DO_NOT_PARSE):
                file_path = os.path.join(directory_name, file_name)
                __show_work__(file_path)
    print(SEPARATOR)


def __show_work__(file_path):
    """ Show the TODO messages of a given set of lines.

    Args:
        file_path (str): File to be analyzed.
    """
    with open(file_path) as f:
        lines = f.readlines()
    position = 0
    for line in lines:
        if "TODO" in line:
            _, message = line.split("#")
            print("- %s:(%s):\t%s" % (str(os.path.basename(file_path)),
                                      str(position),
                                      str(message).strip()))
        position += 1
