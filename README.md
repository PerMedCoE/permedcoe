# HPC/Exascale Centre of Excellence in Personalised Medicine

## Base Building Block

This package provides the base for all **Building Blocks (BBs)** developed in the **HPC/Exascale Centre of Excellence in Personalised Medicine** ([PerMedCoE](https://permedcoe.eu/)) project.

## Table of Contents

- [HPC/Exascale Centre of Excellence in Personalised Medicine](#hpcexascale-centre-of-excellence-in-personalised-medicine)
  - [Base Building Block](#base-building-block)
  - [Table of Contents](#table-of-contents)
  - [User instructions](#user-instructions)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Command line](#command-line)
    - [Public API](#public-api)
    - [Uninstall](#uninstall)
  - [Developer instructions](#developer-instructions)
    - [Building block](#building-block)
  - [License](#license)
  - [Contact](#contact)

## User instructions

### Requirements

- Python >= 3.6
- [Singularity](https://singularity.lbl.gov/docs-installation)

### Installation

There are two ways to install this package (from Pypi and manually):

- From Pypi:

  This package is **NOT YET** publicly available in Pypi:

  ```shell
  pip install permedcoe
  ```

  or more specifically:

  ```shell
  python3 -m pip install permedcoe
  ```

- From source code:

  This package provides an automatic installation script:

  ```shell
  ./install.sh
  ```

  This script creates a file `installation_files.txt` to keep track of the installed files. It is used with the `uninstall.sh` script to clean up the system.


### Command line

  This package provides the `permedcoe` command:

  ```shell
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

  ```

- It enables to execute single building blocks or applications:

  ```shell
  $ permedcoe execute -h
  usage: permedcoe execute [-h] {building_block,bb,application,app} ...

  positional arguments:
    {building_block,bb,application,app}
      building_block (bb)
                          Execute a building block.
      application (app)   Execute an application.

  optional arguments:
    -h, --help            show this help message and exit
  ```

  - In particular for building blocks:

    ```shell
    $ permedcoe execute building_block -h
    usage: permedcoe execute building_block [-h] [-i INPUT [INPUT ...]] [-o OUTPUT [OUTPUT ...]]
                                        [-c CONFIG] [-d] [-l {debug,info,warning,error,critical}]
                                        [--tmpdir TMPDIR] [--processes PROCESSES] [--gpus GPUS]
                                        [--memory MEMORY] [--mount_points MOUNT_POINTS]

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

    ```

  - In particular for building blocks:

    ```shell
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
    ```

- And it is also available to create a skeleton of a building block or an application:

  ```shell
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
  ```

### Public API

The `permedcoe` package provides a set of public decorators, parameter type definition and functions to be used in the Building Block implementation.

- Public decorators:

    ```python
    from permedcoe import container
    from permedcoe import constraint
    from permedcoe import binary
    from permedcoe import mpi
    from permedcoe import task
    ```

- Parameter type definition:

    ```python
    from permedcoe import FILE_IN
    from permedcoe import FILE_OUT
    from permedcoe import FILE_INOUT
    from permedcoe import DIRECTORY_IN
    from permedcoe import DIRECTORY_OUT
    from permedcoe import DIRECTORY_INOUT
    ```

- Functions:

    ```python
    from permedcoe import invoke
    from permedcoe import get_environment
    ```

### Uninstall

Uninstall can be done as usual `pip` packages:

There are two ways to uninstall this package, that depends on the way that it was installed (from Pypi or using `install.sh`):

- From Pypi:

  ```shell
  pip uninstall permedcoe
  ```

  or more specifically:

  ```shell
  python3 -m pip uninstall permedcoe
  ```

- From manual installation (using `install.sh`):

  ```shell
  ./uninstall.sh
  ```

  And then the folder can be cleaned as well using the `clean.sh` script.

  ```shell
  ./clean.sh
  ```

## Developer instructions

### Building block

If you are willing to implement your Building Block (BB), check:

- [Documentation](https://permedcoe.readthedocs.io/en/latest/)
- [Tutorial](https://permedcoe.readthedocs.io/en/latest/04_tutorial/tutorial.html)
- [basic_application](https://github.com/PerMedCoE/basic_application)
- [Lysozyme_in_water](https://github.com/PerMedCoE/Lysozyme_in_water) repositories, where you will find BB and application samples.

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Contact

<https://permedcoe.eu/contact/>
