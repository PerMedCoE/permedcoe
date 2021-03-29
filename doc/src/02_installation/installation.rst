Installation
============

This section shows how to install the PerMedCoE base package, but first,
describes the required dependencies.

Requirements
------------

- Python >= 3.6
- `Singularity <https://singularity.lbl.gov/docs-installation>`_


Installation from Pypi
----------------------

This package is publicly available in Pypi:

.. code-block:: console

    python3 -m pip install permedcoe


Installation from source code
-----------------------------

This package provides an automatic installation script:

.. code-block:: console

    git clone https://github.com/PerMedCoE/permedcoe.git
    cd permedcoe
    ./install.sh

.. ATTENTION::

    This script creates a file named ``installation_files.txt`` to keep track of the installed files.
    It is used with the ``uninstall.sh`` script to clean up the system.


Uninstall from Pypi
-------------------

Uninstall can be done as usual ``pip`` packages:

.. code-block:: console

    python3 -m pip uninstall permedcoe


Uninstall from source code
--------------------------

If installed using ``install.sh``, the uninstall can be performed by running:

.. code-block:: console

    ./uninstall.sh

And then the folder can be cleaned as well using the ``clean.sh`` script.

.. code-block:: console

    ./clean.sh
