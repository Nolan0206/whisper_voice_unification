import os
from pathlib import Path

import pandas as pd
from colorama import Fore

'''
def multiple_file_types(*patterns):
    return it.chain.from_iterable(glob.iglob(pattern) for pattern in patterns)
'''


def show_argparse(args):
    args_dict = vars(args)
    df = pd.DataFrame({'argument': args_dict.keys(), 'value': args_dict.values()})
    print('*' * 15)
    print(df)
    print('*' * 15)


def read_txt(txt_name: str):
    try:
        txt = []
        print(txt_name)
        with open(txt_name, "r") as f:
            line = f.readline()
            while line:
                txt.append(line.strip())
                line = f.readline()
    except FileNotFoundError:
        print("read_txt filename error")
        return None
    else:
        return txt


def input_content():
    content = input("the json folder")
    if not os.path.exists(content):
        print(Fore.RED + "Directory file is not exist")
        return None
    else:
        if os.path.isfile(content):
            print(Fore.RED + "file is not a dir")
            return None
        else:
            return content


def read_dir(dir_name):
    if dir_name is None:
        print(Fore.RED + "Directory file is None")
        print(Fore.BLUE + "Please enter the json folder")
        json_directory = input_content()
    else:
        path_str = Path(dir_name)
        if path_str.exists() and path_str.is_dir():
            json_directory = dir_name
        else:
            json_directory = input_content()
    if isinstance(json_directory, str):
        path_str = Path(json_directory)
    else:
        return None
    file_example = [str(p) for p in path_str.glob('*') if p.suffix in [".json", ".csv"]]
    if not file_example:
        print(Fore.RED + f"The json file list is empty, because the json or csv file is not found in {dir_name}")
        print(Fore.BLUE + "Please check if the file directory is correct")
        return None
    else:
        return file_example


def read_config(catalog: str):
    try:
        method, catalog = catalog.split('<')
    except ValueError:
        print(f"{catalog} is an error format")
        return None
    if method == "txt":
        file_name = read_txt(catalog)
        if not file_name:
            print(Fore.RED + f"The json file list is empty, because the json file is not found in {catalog}")
            return None
        return file_name
    elif method == "dir":
        file_name = read_dir(catalog)
        if not file_name:
            print(Fore.RED + f"The json file list is empty, because the json file is not found in {catalog}")
            return None
        else:
            return file_name
    else:
        print(Fore.RED + "error")
        return None
