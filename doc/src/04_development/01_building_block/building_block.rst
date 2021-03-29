Building Block
==============

First step
----------

The first suggested step is to start with a template created with the
``permedcoe`` command:

.. code-block:: console

  permedcoe template building_block my_building_block

The result of this command is a folder containing a python package
with all scripts and base code to start developing your Building Block.

.. TIP::

    More than one Building Block can be included within the created package.

.. HINT::

    The Building Block template creation provides the main actions to be
    performed in order to complete your building block:

    .. code-block:: console

        ------------------------------------------
        To be completed:

        - main.py:(15):	TODO: Define your container
        - main.py:(29):	TODO: (optional) Pure python code calling to PyCOMPSs tasks (that can be defined in this file or in another).
        - main.py:(33):	TODO: Define the binary to be used.
        - main.py:(34):	TODO: Define the inputs and output parameters.
        - main.py:(35):	TODO: Define a representative task name
        - main.py:(37):	TODO: Define the binary parameters
        - main.py:(54):	TODO: Declare how to run the binary specification (convert config into building_block_task call)
        ------------------------------------------


Package structure
-----------------

The package contains the following scripts:

.. code-block:: console

    .
    ├── build.sh
    ├── clean.sh
    ├── install_editable.sh
    ├── install.sh
    ├── LICENSE
    ├── pyproject.toml
    ├── README.md
    ├── setup.cfg
    ├── setup.py
    ├── src
    │   └── my_building_block
    │       ├── __init__.py
    │       ├── __main__.py
    │       ├── main.py
    └── uninstall.sh

+------------------------------------+--------------------------------------------+
| **File name**                      | **Description**                            |
+------------------------------------+--------------------------------------------+
| setup.cfg                          | Package configuration (Pypi metadata)      |
+------------------------------------+--------------------------------------------+
| pyproject.toml                     | Building requirements                      |
+------------------------------------+--------------------------------------------+
| install.sh                         | Manual installation script                 |
+------------------------------------+--------------------------------------------+
| build.sh                           | Script that builds the package             |
+------------------------------------+--------------------------------------------+
| setup.py                           | Package setup                              |
+------------------------------------+--------------------------------------------+
| clean.sh                           | Script that cleans build files             |
+------------------------------------+--------------------------------------------+
| README.md                          | Package description                        |
+------------------------------------+--------------------------------------------+
| LICENSE                            | Package license                            |
+------------------------------------+--------------------------------------------+
| install_editable.sh                | Installation within the same folder script |
+------------------------------------+--------------------------------------------+
| src/my_building_block/             | Folder that contains the building block    |
+------------------------------------+--------------------------------------------+
| src/my_building_block/__init__.py  | Package import resolver                    |
+------------------------------------+--------------------------------------------+
| src/my_building_block/main.py      | **Building block main file**               |
+------------------------------------+--------------------------------------------+
| src/my_building_block/__main__.py  | Building block invocation file             |
+------------------------------------+--------------------------------------------+
| uninstall.sh                       | Uninstall script                           |
+------------------------------------+--------------------------------------------+


Building block structure
------------------------

There are a set of rules to implement a PerMedCoE compliant Building Block:

- Provide a executable Python script with the following structure:

  .. code-block:: python

    from permedcoe import Container        # To define container related needs
    from permedcoe import Binary           # To define binary to execute related needs
    from permedcoe import Task             # To define task related needs

    from permedcoe import FILE_IN          # To define file type and direction
    from permedcoe import FILE_OUT         # To define file type and direction
    from permedcoe import DIRECTORY_IN     # To define directory type and direction
    from permedcoe import DIRECTORY_OUT    # To define directory type and direction

    from permedcoe import get_environment  # Get variables from invocation (tmpdir, processes, gpus, memory)


    # Single and global container definition for this building block
    SAMPLE_CONTAINER = "/path/to/image.sif"  # TODO: Define your container


    def function_name(*args, **kwargs):
        """ Extended python interface:
        To be used only with PyCOMPSs - Enables to define a workflow within the building block.
        Tasks are not forced to be binaries: PyCOMPSs supports tasks that are pure python code.

        # PyCOMPSs help: https://pycompss.readthedocs.io/en/latest/Sections/02_App_Development/02_Python.html

        Requirement: all tasks should be executed in a container (with the same container definition)
                    to ensure that they all have the same requirements.
        """
        print("Building Block entry point to be used with PyCOMPSs")
        # TODO: (optional) Pure python code calling to PyCOMPSs tasks (that can be defined in this file or in another).


    @Container(engine="SINGULARITY", image=SAMPLE_CONTAINER)
    @Binary(binary="/path/to/my_binary")                      # TODO: Define the binary to be used.
    @Task(dataset=FILE_IN, output=FILE_OUT)                   # TODO: Define the inputs and output parameters.
    def building_block_task(dataset_flag="-d", dataset=None,  # TODO: Define a representative task name
                            output_flag="-o", output=None,
                            operation="-x"):                  # TODO: Define the binary parameters
        # The Definition is equal to:
        #    /path/to/my_binary -d dataset -o output -x
        # Empty function since it represents a binary execution:
        pass


    def invoke(input, output, config):
        """ Common interface.

        Args:
            input (str): Input file path.
            output (str): Output directory path.
            config (dict): Configuration dictionary.
        Returns:
            None
        """
        # TODO: Declare how to run the binary specification (convert config into building_block_task call)
        operation = config["operation"]
        # env_vars = get_environment()  # NOSONAR - Retrieves the extra flags.
        building_block_task(dataset=input,
                            output=output,
                            operation=operation)


- Use a single container per Building Block (``SAMPLE_CONTAINER``).

- Use the decorators provided by ``permedcoe`` package.
  They provide the capability to use the BB in various workflow managers transparently.
  In other words, the BB developer does not have to deal with the peculiarities of the workflow managers.

- A BB can be a single executable, but it can be a more complex code if the ``my_building_block_extended`` function is implemented and used with PyCOMPSs.

- It is necessary to have an ``invoke`` function with a specific signature: ``def invoke(input, output, config)``-

- The BB ``binary`` must be defined with the ``@task``, ``@binary`` and ``@container`` decorators (``my_building_block_task``).
  This function needs to declare the binary flags, and it is invoked from the ``invoke`` function.

- The ``@task`` decorator must declare the type of the file or directories for the binary invocation.
  In particular, using the parameter name and ``FILE_IN``/``FILE_OUT``/``DIRECTORY_IN``/``DIRECTORY_OUT``
  to define if the parameter is a file or a directory and if the binary is consuming the file/directory or it is producing it.


Deployment
----------

Installation
~~~~~~~~~~~~

The package provides two ways to install this package (from Pypi and manually):

- From Pypi:

  After uploading the package to Pypi it can be installed as usual Python packages:

  .. code-block:: console

    pip install my_building_block

  or more specifically:

  .. code-block:: console

    python3 -m pip install my_building_block

- From source code:

  This package provides an automatic installation script, but it is necessary to install the ``permedcoe``
  package before the ``my_building_block`` package since it is required by ``my_building_block``.

  .. code-block:: console

    # Install permedcoe package
    git clone https://github.com/PerMedCoE/permedcoe.git
    cd permedcoe
    ./install.sh
    # Install my_building_block
    cd ../my_building_block
    ./install.sh


  .. TIP::

    This script creates a file ``installation_files.txt`` to keep track of the installed files.
    It is used with the ``uninstall.sh`` script to clean up the system.

Usage
~~~~~

The ``my_building_block`` package provides a clear interface that allows it to be used with multiple workflow managers
(e.g. PyCOMPSs, NextFlow and Snakemake).

- Command line interface:

  Once installed the ``my_building_block`` package, it provides the ``my_building_block``
  command, that can be used from the command line. For example:

  .. code-block:: console

    $ my_building_block -h
    usage: my_building_block [-h] [-i INPUT [INPUT ...]] [-o OUTPUT [OUTPUT ...]] [-c CONFIG] [-d]
                    [-l {debug,info,warning,error,critical}] [--tmpdir TMPDIR] [--processes PROCESSES]
                    [--gpus GPUS] [--memory MEMORY] [--mount_points MOUNT_POINTS]

    optional arguments:
        -h, --help            show this help message and exit
        -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                            Input file/s or directory path/s
        -o OUTPUT [OUTPUT ...], --output OUTPUT [OUTPUT ...]
                            Output file/s or directory path/s
        -c CONFIG, --config CONFIG
                            Configuration file path
        -d, --debug           Enable Building Block debug mode. Overrides log_level
        -l {debug,info,warning,error,critical}, --log_level {debug,info,warning,error,critical}
                            Set logging level
        --tmpdir TMPDIR       Temp directory to be mounted in the container
        --processes PROCESSES
                            Number of processes for MPI executions
        --gpus GPUS           Requirements for GPU jobs
        --memory MEMORY       Memory requirement
        --mount_points MOUNT_POINTS
                            Comma separated alias:folder to be mounted in the container

  This interface can be used within any workflow manager that requires binaries (e.g. NextFlow and Snakemake).

  In addition, it can be used with PyCOMPSs by importing the decorated function or any other specific for PyCOMPSs.

  .. code-block:: python

    from my_building_block import building_block_task

    building_block_task(dataset_flag="-d", dataset=None,
                        output_flag="-o", output=None,
                        operation="-x")

- Extension for PyCOMPSs:

  Moreover, a BB can also implement a Python function not limited to the input (file/s or directory/ies),
  output (file/s or directory/ies) and config (yaml file) signature.
  This enables application developers to use the BB with PyCOMPSs using Python objects instead of files among BBs.

  .. code-block:: python

    from my_building_block import function_name

    function_name(*args, **kwargs)  # specific interface

Uninstall
~~~~~~~~~

Uninstall can be done as usual ``pip`` packages:

There are two ways to uninstall this package, that depends on the way that it was installed (from Pypi or using ``install.sh``):

- From Pypi:

  .. code-block:: console

    pip uninstall my_building_block

  or more specifically:

  .. code-block:: console

    python3 -m pip uninstall my_building_block


- From manual installation (using ``install.sh``):

  .. code-block:: console

    ./uninstall.sh


  And then the folder can be cleaned as well using the ``clean.sh`` script.

  .. code-block:: console

    ./clean.sh


Best practices
--------------

There are a set of best practices suggested to BB developers:

- Use a code style:
    - `pep8 <https://www.python.org/dev/peps/pep-0008/>`_
    - `black <https://github.com/psf/black>`_

- Document your BB.
