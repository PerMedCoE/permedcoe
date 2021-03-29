Application
===========

First step
----------

The first suggested step is to start with a template created with the
``permedcoe`` command:

.. code-block:: console

  permedcoe template application my_application

The result of this command is a folder containing a three folders, one
for the three supported workflows managers (PyCOMPSs, Nextflow and Snakemake),
where a template for each of them is provided.

.. HINT::

    The application template creation provides the main actions to be
    performed in order to complete your building block:

    .. code-block:: console

        ------------------------------------------
        To be completed:

        - app.py:(9):	    TODO: Import the desired building blocks and use invoke or any other function.
        - Snakefile:(0):	TODO: Declare the building blocks to be used as rules.
        - Snakefile:(9):	TODO: Change bb to the building block name.
        - NextFlow.nf:(7):	TODO: Declare the building blocks to be used as process.
        - NextFlow.nf:(18):	TODO: Change bb to the building block name.
        ------------------------------------------

.. NOTE::

    The template provides support for PyCOMPSs, Nextflow and Snakemake, but it is not
    mandatory to implement the application for all of them. However, this decision
    will tight your application to a single workflow manager that needs to be available
    where the execution is going to take place.


Folder structure
----------------

The application contains the following scripts:

.. code-block:: console

    .
    ├── NextFlow
    │   ├── launch.sh
    │   └── NextFlow.nf
    ├── PyCOMPSs
    │   ├── app.py
    │   ├── launch.sh
    │   ├── launch_without_pycompss.sh
    └── SnakeMake
        ├── launch.sh
        └── Snakefile

+-------------------------------------+------------------------------------------------------+
| **File name**                       | **Description**                                      |
+-------------------------------------+------------------------------------------------------+
| PyCOMPSs                            | Folder containing the PyCOMPSs application template  |
+-------------------------------------+------------------------------------------------------+
| PyCOMPSs/app.py                     | Application template for PyCOMPSs                    |
+-------------------------------------+------------------------------------------------------+
| PyCOMPSs/launch.sh                  | Launch with PyCOMPSs script                          |
+-------------------------------------+------------------------------------------------------+
| PyCOMPSs/launch_without_pycompss.sh | Launch without PyCOMPSs script                       |
+-------------------------------------+------------------------------------------------------+
| SnakeMake                           | Folder containing the Snakemake application template |
+-------------------------------------+------------------------------------------------------+
| SnakeMake/launch.sh                 | Launch with Snakemake script                         |
+-------------------------------------+------------------------------------------------------+
| SnakeMake/Snakefile                 | Application template for Snakemake                   |
+-------------------------------------+------------------------------------------------------+
| NextFlow                            | Folder containing the Nextflow application template  |
+-------------------------------------+------------------------------------------------------+
| NextFlow/launch.sh                  | Launch with Nextflow script                          |
+-------------------------------------+------------------------------------------------------+
| NextFlow/NextFlow.nf                | Application template for Nextflow                    |
+-------------------------------------+------------------------------------------------------+

The developer responsibility is to complete at least one of the following files:

- ``NextFlow.nf``
- ``app.py``
- ``Snakefile``

And the mainly expected content of the application is the usage of building blocks.

.. TIP::

  Due to the Python nature of PyCOMPSs applications, it can also support python code and objects
  among building blocks, enabling the implementation of complex workflows with inner parallelism.

Best practices
--------------

There are a set of best practices suggested to application developers:

- Use a code style if using PyCOMPSs:
    - `pep8 <https://www.python.org/dev/peps/pep-0008/>`_
    - `black <https://github.com/psf/black>`_

- Document your Application.