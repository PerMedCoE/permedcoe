# HPC/Exascale Centre of Excellence in Personalised Medicine

## Building Block Skeleton

This package provides a **Building Block (BB)** skeleton using the **HPC/Exascale Centre of Excellence in Personalised Medicine** (
[PerMedCoE](https://permedcoe.eu/)) base Building Block.

## Table of Contents

- [HPC/Exascale Centre of Excellence in Personalised Medicine](#hpcexascale-centre-of-excellence-in-personalised-medicine)
  - [Building Block Skeleton](#building-block-skeleton)
  - [Table of Contents](#table-of-contents)
    - [User instructions](#user-instructions)
      - [Requirements](#requirements)
      - [Installation](#installation)
      - [Usage](#usage)
      - [Uninstall](#uninstall)
    - [Developer instructions](#developer-instructions)
      - [Building block](#building-block)
      - [Best practices](#best-practices)
    - [License](#license)
    - [Contact](#contact)

### User instructions

#### Requirements

- Python >= 3.6
- Singularity

#### Installation

This package is publicly available in Pypi:

```bash
pip install package_name
```

or more specifically:

```bash
./install.sh
```

#### Usage

The `skeleton_BB` package provides a clear interface that allows it to be used with multiple workflow managers (e.g. PyCOMPSs, NextFlow and Snakemake).

- Command line interface:

    Once installed the `skeleton_BB` package, it provides the `skeleton`
    command, that can be used from the command line. For example:

    ```text
    $ skeleton -h
    usage: skeleton [-h] [-d] [--tmpdir TMPDIR] [--processes PROCESSES] [--gpus GPUS] [--memory MEMORY] input output config

    positional arguments:
    input                 Input file or directory path
    output                Output file or directory path
    config                Configuration file path

    optional arguments:
    -h, --help            show this help message and exit
    -d, --debug           Enable Building Block debug mode
    --tmpdir TMPDIR       Temp directory to be mounted in the container
    --processes PROCESSES
                            Number of processes for MPI executions
    --gpus GPUS           Requirements for GPU jobs
    --memory MEMORY       Memory requirement
    ```

    This interface can be used within any workflow manager that requires binaries (e.g. NextFlow and Snakemake).

    In addition, any building block requires to have a function being called from the `__main__`, so that it can also be invoked from Python scripts. This allows to use the BB from PyCOMPSs seamlessly.

    ```python
    from skeleton_BB.sample import skeleton_BB

    skeleton_BB(input, output, config)
    ```

- Extension for PyCOMPSs:

    Moreover, a BB can also implement a Python function not limited to the input (file or directory), output (file or directory) and config (yaml file) signature. This enables application developers to use the BB with PyCOMPSs using Python objects instead of files among BBs.

    ```python
    from skeleton_BB.sample import skeleton_BB_extended

    skeleton_BB_extended(*args, **kwargs)  # specific interface
    ```

#### Uninstall

Uninstall can be done as usual `pip` packages:

```bash
pip uninstall skeleton_BB
```

or more specifically:

```bash
./uninstall.sh
./clean.sh
```

### Developer instructions

#### Building block

There are a set of rules to implement a PerMedCoE compliant Building Block:

- Provide a executable Python script with the following structure:

    ```Python
    from PerMedCoE_BB import invoke
    from PerMedCoE_BB import container
    from PerMedCoE_BB import binary
    from PerMedCoE_BB import task
    from PerMedCoE_BB import FILE_IN
    from PerMedCoE_BB import FILE_OUT
    from PerMedCoE_BB import DIRECTORY_IN
    from PerMedCoE_BB import DIRECTORY_OUT

    CONTAINER = "/path/to/container.sif"

    def skeleton_BB_extended(...):
        # Python code calling to tasks (see PyCOMPSs)
        ...

    @container(engine="SINGULARITY", image=CONTAINER)
    @binary(binary="/path/to/binary")
    @task(dataset=FILE_IN, output=FILE_OUT)
    def skeleton_BB_task(dataset_flag="-d", dataset=None,
                       output_flag="-o", output, ...):
        # Equivalent to:
        # /path/to/binary -d dataset -o output
        ...

    def skeleton_BB(input, output, config):
        # Process config parameters dictionary to
        # prepare the call to 'skeleton_BB_task'
        dataset = config["dataset"]
        output = config["output"]
        skeleton_BB_task(dataset=dataset,
                       output=output)
        ...

    if __name__ == "__main__":
        invoke(skeleton_BB)
        # 'invoke' provides the command line interface and
        # parses the input arguments.
    ```

- Use a single container per Building Block (`CONTAINER`).

- Use the decorators provided by `PerMedCoE_BB` package. They provide the capability to use the BB in various workflow managers transparently. In other words, the BB developer does not have to deal with the peculiarities of the workflow managers.

- A BB can be a single executable, but it can be a more complex code if the `skeleton_BB_extended` function is implemented and used with PyCOMPSs.

- It is necessary to have function (`skeleton_BB`) with a specific signature: `(input, output, config)`. It must be called from the  `if __name__=="__main__"` using the `invoke` function with the function name as parameter (`invoke(skeleton_BB)`).

- The `invoke` function provides the command line interface for
the BB as shown in the [usage](#usage) section. In addition, it
parses the Yaml config file and invokes the `skeleton_BB` function
with the appropriate parameters.

- The BB `binary` must be defined with the `@task`, `@binary` and `@container` decorators (`skeleton_BB_task`). This function needs to declare the binary flags, and it is invoked from the `skeleton_BB` function.

- The `@task` decorator must declare the type of the file or directories for the binary invocation. In particular, using the parameter name and `FILE_IN`/`FILE_OUT`/`DIRECTORY_IN`/`DIRECTORY_OUT` to define if the parameter is a file or a directory and if the binary is consuming the file/directory or it is producing it.

#### Best practices

There are a set of best practices suggested to BB developers:

- Use a code style:
  - [pep8](https://www.python.org/dev/peps/pep-0008/)
  - [black](https://github.com/psf/black)

- container best practices:
  - one
  - two

- Document your BB.

### License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

### Contact

<https://permedcoe.eu/contact/>
