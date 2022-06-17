""" return file paths"""
import os
import subprocess
import platform


def get_file_paths_by_os(root: str):
    """Return file paths for every file in root and its subdirectories, using os."""
    all_paths = []
    for root_path, files_paths in os.walk(root):
        for file_names in files_paths:
            all_paths.append(os.path.join(root_path, file_names))
    return all_paths


print(get_file_paths_by_os('/content/gdrive/MyDrive/Jet_ML'))


def get_file_paths_by_subprocess(root: str):
    """Return file paths for every file in root and its subdirectories, using subprocess."""
    plt = platform.system()
    if plt == 'Windows':
        cmd = f'dir {root} /s /b /o:gn'
    if plt == 'Linux':
        cmd = f'ls {root}'
    if plt == 'darwin':
        cmd = f'ls {root}'
    all_paths = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return all_paths.decode("utf-8").split("\n")


if __name__ == '__main__':
    answer = get_file_paths_by_subprocess('/content/gdrive/MyDrive/Jet_ML')

    print(os.name)
    print(platform.system())
    print(get_file_paths_by_subprocess('/content/gdrive/MyDrive/Jet_ML'))

    print("after __name__ guard")
