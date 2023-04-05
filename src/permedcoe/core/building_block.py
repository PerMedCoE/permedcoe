"""
This file provides the PerMedBB class which implements the functionalities
to interact with the container infrastructure (Singularity).
"""

import os
import logging
import re
from permedcoe.utils.executor import command_runner


class PerMedBB(object):

    def __init__(self, img_path, mpi_runner, exe_path,
                 computing_nodes, computing_units,
                 mount_paths, user_mount_paths,
                 env_vars, flags):
        """ Constructor

        Args:
            img_path (str): Container path.
            mpi_runner (str): MPI runner. (default=None)
            exe_path (str): Executable path.
            computing_nodes (int): Number of compute nodes needed.
            computing_units (int): Number of compute units needed (cores).
            mount_paths (list[str]): List of folders to be mounted.
            user_mount_paths (list[str]): User defined mount paths.
            env_vars (dict{name: value}): Environment variables to delegate.
            flags (dict{name: value}): Flags for the container engine.
        """
        self.img_path = img_path
        self.exe_path = exe_path
        self.flags = flags

        self.sing_command_comp = {}
        self.sing_command_comp["base"] = "singularity --silent"
        self.sing_command_comp["action"] = "exec"
        self.sing_command_comp["action_flags"] = "--contain --cleanenv --pwd " + os.getcwd()  # noqa: E503
        self.sing_command_comp["sif"] = img_path
        if mpi_runner:
            # MPI execution within the container
            self.sing_command_comp["exe"] = [mpi_runner,
                                             "-np",
                                             self.computing_units,
                                             exe_path]
        else:
            # Single binary execution
            self.sing_command_comp["exe"] = exe_path
        self.sing_command_comp["mounts"] = ""
        mount_paths = sorted(mount_paths, key=len)
        for path in mount_paths:
            self.add_bind(path, path)
        if user_mount_paths:
            user_mounts = user_mount_paths.split(",")
            for mount in user_mounts:
                s, t = mount.split(":")
                self.add_bind(s, t)
        self.sing_command_comp["envs"] = ""
        for var in env_vars:
            self.add_env(var)
        self.sing_command_comp["flags"] = flags

    def add_env(self, env_var):
        """ Small helper function to add an environment variable to
        singularity command line.

        Args:
            env_var (str): Environment variable.
        """
        if self.sing_command_comp["envs"] == "":
            self.sing_command_comp["envs"] = "--env {}".format(env_var)
        else:
            self.sing_command_comp["envs"] = \
                self.sing_command_comp["envs"] + ",{}".format(env_var)

    def add_bind(self, s, t):
        """ Small helper function to add a bind point to singularity command line.

        Args:
            s (str): Source folder
            t (str): Destination folder
        """
        if self.sing_command_comp["mounts"] == "":
            self.sing_command_comp["mounts"] = "-B {}:{}".format(s, t)
        else:
            self.sing_command_comp["mounts"] = \
                self.sing_command_comp["mounts"] + ",{}:{}".format(s, t)

    def launch(self, shell=False, run_in_container=True):
        """ Executes the binary into the singularity container.

        Args:
            shell (bool, optional): Action shell. Defaults to False.
            run_in_container (bool, optional): Launch execution in container.
        """
        command = ""
        if run_in_container:
            order = ["base",
                     "action",
                     "action_flags",
                     "mounts",
                     "envs",
                     "sif",
                     "exe",
                     "flags"]
            if shell:
                self.sing_command_comp["action"] = "shell"
        else:
            order = ["exe",
                     "flags"]
        scc = self.sing_command_comp
        for c in order:
            if isinstance(scc[c], list):
                for elem_scc in scc[c]:
                    if isinstance(elem_scc, list):
                        command = command + " " + " ".join(elem_scc)
                    else:
                        command = command + " " + str(elem_scc)
            else:
                command = command + " " + scc[c]
        logging.info("Launching the command: %s" % command)
        cmd = re.sub(" +", " ", command.strip()).split(" ")
        command_runner(cmd)
