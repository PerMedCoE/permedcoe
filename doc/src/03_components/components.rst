Components
==========

The ``permedcoe`` package provides a Python API necessary for the development
of **Building Blocks (BBs)** in the **HPC/Exascale Centre of Excellence in
Personalised Medicine** (`PerMedCoE <https://permedcoe.eu/>`_) project.

In addition, it provides a command line tool that eases the application or
building block execution, as well as being able to create empty templates for them.


Python API
----------

The ``permedcoe`` package provides a set of public decorators, parameter type
definition and functions to be used in the Building Block implementation.

- Public decorators:

    .. code-block:: python

        from permedcoe import Container
        from permedcoe import Constraint
        from permedcoe import Binary
        from permedcoe import Mpi
        from permedcoe import Task

- Parameter type definition:

    .. code-block:: python

        from permedcoe import FILE_IN
        from permedcoe import FILE_OUT
        from permedcoe import DIRECTORY_IN
        from permedcoe import DIRECTORY_OUT

- Functions:

    .. code-block:: python

        from permedcoe import set_debug
        from permedcoe import invoke
        from permedcoe import get_environment

The usage of these decorators, type definitions and functions is described in
:ref:`04_development/development:Development` Section.

Command line
------------

This package provides the ``permedcoe`` command, which enables to execute
single building blocks or applications, as well as to create skeletons for
building blocks and applications.

.. code-block:: console

  $ permedcoe -h
  usage: permedcoe [-h] [-d] [-l {debug,info,warning,error,critical}] {execute,x,template,t} ...

  positional arguments:
    {execute,x,template,t}
      execute (x)         Execute a building block.
      template (t)        Shows an example of the requested template.

  optional arguments:
    -h, --help            show this help message and exit
    -d, --debug           Enable debug mode. Overrides log_level (default: False)
    -l {debug,info,warning,error,critical}, --log_level {debug,info,warning,error,critical}
                          Set logging level. (default: error)



Execution
~~~~~~~~~

The execution of building blocks or applications with the ``permedcoe`` command
is performed by indicating ``execute`` (or ``x``) after ``permedcoe``.
The following snippet shows it followed the ``-h`` flag to provide the help.

.. code-block:: console

  $ permedcoe execute -h
  usage: permedcoe execute [-h] {building_block,bb,application,app} ...

  positional arguments:
    {building_block,bb,application,app}
      building_block (bb)
                          Execute a building block.
      application (app)   Execute an application.

  optional arguments:
    -h, --help            show this help message and exit


Building Block execution
^^^^^^^^^^^^^^^^^^^^^^^^

In particular, if ``permedcoe execute`` is followed by ``building_block`` (or
``bb``), indicates that the user wants to execute an available building block.

.. WARNING::

    The building block to execute must be previously installed, and its name
    (as imported in python) has to be provided.

.. code-block:: console

    $ permedcoe execute building_block -h
    usage: permedcoe execute building_block [-h] [-i INPUT [INPUT ...]] [-o OUTPUT [OUTPUT ...]]
                                        [-c CONFIG] [-d] [-l {debug,info,warning,error,critical}]
                                        [--tmpdir TMPDIR] [--processes PROCESSES] [--gpus GPUS]
                                        [--memory MEMORY] [--mount_points MOUNT_POINTS]
                                        name

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                            Input file/s or directory path/s (default: None)
      -o OUTPUT [OUTPUT ...], --output OUTPUT [OUTPUT ...]
                            Output file/s or directory path/s (default: None)
      -c CONFIG, --config CONFIG
                            Configuration file path (default: None)
      -d, --debug           Enable Building Block debug mode. Overrides log_level (default: False)
      -l {debug,info,warning,error,critical}, --log_level {debug,info,warning,error,critical}
                            Set logging level (default: None)
      --tmpdir TMPDIR       Temp directory to be mounted in the container (default: None)
      --processes PROCESSES
                            Number of processes for MPI executions (default: None)
      --gpus GPUS           Requirements for GPU jobs (default: None)
      --memory MEMORY       Memory requirement (default: None)
      --mount_points MOUNT_POINTS
                            Comma separated alias:folder to be mounted in the container (default: None)



Application execution
^^^^^^^^^^^^^^^^^^^^^

Alternatively, if ``permedcoe execute`` is followed by ``application`` (or
``app``), indicates that the user wants to execute the given application.

.. WARNING::

    The workflow manager selected must be available in the system.

.. code-block:: console

    permedcoe execute application -h None)
    usage: permedcoe execute application [-h] [-w {none,pycompss,nextflow,snakemake}]
                                        [-f FLAGS [FLAGS ...]]
                                        name [parameters [parameters ...]]

    positional arguments:
      name                  Application to execute
      parameters            Application parameters (default: None)

    optional arguments:
      -h, --help            show this help message and exit
      -w {none,pycompss,nextflow,snakemake}, --workflow_manager {none,pycompss,nextflow,snakemake}
                            Workflow manager to use (default: none)
      -f FLAGS [FLAGS ...], --flags FLAGS [FLAGS ...]
                            Workflow manager flags (default: None)



Template creation
~~~~~~~~~~~~~~~~~

The ``permedcoe`` command is also able to create a skeleton of a building block
or an application:

.. code-block:: console

  $ permedcoe template -h
  usage: permedcoe template [-h] [-t {all,pycompss,nextflow,snakemake}]
                            {bb,building_block,app,application} name

  positional arguments:
    {bb,building_block,app,application}
                          Creates a Building Block or Application template.
    name                  Building Block or Application name.

  optional arguments:
    -h, --help            show this help message and exit
    -t {all,pycompss,nextflow,snakemake}, --type {all,pycompss,nextflow,snakemake}
                          Application type. (default: all)

.. HINT::

     Once the artifact is created, it describes the minimal expected implementation
     actions to be done in order to complete a Building Block or an application.
