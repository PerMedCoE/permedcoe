.. PerMedCoE Base Package documentation master file, created by
   sphinx-quickstart on Thu Mar 18 17:03:27 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PerMedCoE Base Package's documentation!
==================================================

.. image:: ../_static/logo_1.png
   :width: 500
   :align: center
   :target: https://permedcoe.eu

**PerMedCoE** is the **HPC/Exascale Centre of Excellence for Personalised Medicine in Europe**.

Personalised Medicine (PerMed) opens unexplored frontiers to treat diseases at the individual
level combining clinical and omics information.
However, the performances of the current simulation software are still insufficient to tackle
medical problems such as tumour evolution or patient-specific treatments.
The challenge is to develop a sustainable roadmap to scale-up the essential software for the
cell-level simulation to the new European HPC/Exascale systems.
Simulation of cellular mechanistic models are essential for the translation of omic data to
medical relevant actions and these should be accessible to the end-users in the appropriate
environment of the PerMed-specific big confidential data.
The goal of PerMedCoE is to provide an efficient and sustainable entry point to the
HPC/Exascale-upgraded methodology to translate omics analyses into actionable models of
cellular functions of medical relevance.

In this direction, the PerMedCoE project developments are based on containers enabling
reproducible operations in heterogeneous HPC infrastructures, and their inclusion into
efficient **building blocks (BBs)** and **workflows**.

The ``permedcoe`` package provides a Python API necessary for the development
of **Building Blocks (BBs)** in the **HPC/Exascale Centre of Excellence in
Personalised Medicine** (`PerMedCoE <https://permedcoe.eu/>`_) project.

In addition, it provides a command line tool that eases the application or
Building Block (BB) execution, as well as being able to create empty templates for them.


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   02_installation/installation
   03_components/components
   04_development/development
   05_samples/samples
   07_acks/acknowledgements



..
    01 is potentially a quickstart section
    06 is potentially a troubleshooting section

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
