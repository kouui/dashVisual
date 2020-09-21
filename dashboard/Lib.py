#!/Users/liu/kouui/anaconda3/envs/dash_py38/bin/python
# -*- coding: utf-8 -*-


import sys, os



def get_import_info_from_file_path(s):
    r"""
    """
    path = os.path.abspath(s)
    index = -1*path[::-1].find('/')
    directory = path[:index]
    module = path[index:]
    if module.endswith(".py"):
        module = module[:-3]

    return directory, module

def import_train_func_from_file_path(directory, module):
    r"""
    """
    sys.path.append(directory)

    #exec(f"from {module} import train", globals())
    D = {}
    exec(f"from {module} import train", {}, D)
    return D["train"]

if __name__ == "__main__":
    pass
