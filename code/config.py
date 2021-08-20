"""
Program: config.py
Project: Sets working directory for testing and debugging
Author: Nicolas Lopez
"""

# ==================================================
# Basic Libraries
# ==================================================

import sys
import os
import yaml


# ==================================================
# Add WD to sys.path
# ==================================================

def sys_add_path(path='/Diffractogram Metrics/code/',
                 wd_path=None, subf = False):
    """ Adds folder and subfolders to sys path to correctly read functions
        The folder is added from the current working directory if no adress is passed"""

    wd_path = os.getcwd().replace('\\', '/') if wd_path is None else wd_path

    if subf:
        # TODO
        1 +1

    # If (path != working directory) then update wd.
    if path.split('/')[-1] != wd_path.split('/')[-1]:
        wd_path += path
        os.chdir(wd_path)

    if wd_path not in sys.path: sys.path.append(wd_path)


# ======================================
# Read configuration files
# ======================================
def read_yml(config_path, file):
    try:
        with open(f"{config_path}/{file}.yml") as f:
            print(f"File {file}.yml loaded")
            return yaml.load(f, Loader=yaml.FullLoader)
    except Exception:
        print(f"File {file}.yml could not be read at {config_path}")




sys_add_path()