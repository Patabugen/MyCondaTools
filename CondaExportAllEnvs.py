# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 18:48:30 2019

@author: Mithras44
@docstrings: Google

Exports all conda environments to a folder in user directory. Can be used either as a script or from the command line.
To use as a script change the export_folder variable to desired export folder and run.
To use it from command line you can change the default export folder by changing export_folder but also override it 
with the --export_folder argument.
Define folder path with python CondaExportAllEnvs.py --export_folder=/folder/subfolder
"""

import subprocess
import json
import os
import argparse

export_folder = "/ACproject/My_Conda_Backup_Envs"  # Change to desired export
#  folder in user directory my_conda_backup_envs


def cmd_export_folder(export_folder=export_folder):
    """Takes script default export folder but can be overwritten by argument from command line.

    Args:
        export_folder (str, optional): Folder within user directory. Defaults for export_folder variable if arg isn't provided via command line.
    Returns:
        export_folder (str): String of folder (non full path) to export conda env yml files.
    """

    parser = argparse.ArgumentParser(description="""Export all conda
                                      environments into .yml files to
                                      export_folder """)
    parser.add_argument('--export_folder', type=str, default=export_folder,
                        help=f"""folder to export to within user directory
                         (default: {export_folder})""")
    args = parser.parse_args()
    export_folder = args.export_folder
    return export_folder


def create_export_folder_path(export_folder=export_folder):
    """Takes export folder argument and creates folder if it doesn't exist and returns full path.

    Args:
        export_folder (str, optional): Defaults to export_folder.

    Returns:
        export_folder_path (str): Returns full folder path
    """

    home = os.path.expanduser('~')
    if str(export_folder[0]) != "/":
        export_folder = "/" + export_folder
    else:
        export_folder_path = home + export_folder
    if not os.path.exists(export_folder_path):
        os.makedirs(export_folder_path, mode=0o777)
    return export_folder_path


def conda_env_list():
    """Creates a list of all the conda environments.

    Returns:
        env_names_list (list): A list of al the conda environments.
    """

    command_output = subprocess.run(["conda", "env", "list", "--json"],
                                    universal_newlines=True,
                                    stdout=subprocess.PIPE)
    output = json.loads(command_output.stdout)
    output_envs = output['envs'][1:]
    env_names_list = []
    for env in output_envs:
        env = env.replace("\\", "/")
        env_name = env.split("/")[-1:]
        env_names_list += env_name
    env_names_list.append("base")
    return env_names_list


def export_envs(env_names_list, export_folder_path):
    """Creates yaml files of conda enviroments in export folder.

    Args:
        env_names_list (list): List of all the conda to export.
        export_folder_path (str): Full path of where the yaml files should be created.
    """

    print(export_folder_path)
    for env_name in env_names_list:
        command_run = subprocess.run(
            f"conda env export --name {env_name} > {env_name}_conda_env.yml",
            shell=True, universal_newlines=True, stderr=subprocess.PIPE,
            cwd=export_folder_path)
        if command_run.returncode != 0:
            print(env_name + " : " + command_run.stderr)
        else:
            print(env_name + " : done")
    print("Complete")


def main(export_folder=export_folder):
    """Main.

    Args:
        export_folder (str, optional): Defaults to export_folder variable.
    """

    export_folder = cmd_export_folder(export_folder)
    export_folder_path = create_export_folder_path(export_folder)
    env_names_list = conda_env_list()
    export_envs(env_names_list, export_folder_path)


if __name__ == "__main__":
    main(export_folder)
