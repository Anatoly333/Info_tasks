import os
import subprocess
import platform


def get_file_paths_by_os(root: str):
    """Return file paths for every file in root and its subdirectories, using os."""
    files = []
    all_paths = []
    files = list(os.walk(root))
    for names in files:
        for file_names in names[2]:  # names[2] = array of all_paths
            all_paths.append(os.path.join(names[0], file_names))
    return all_paths


print(get_file_paths_by_os("C:\\Users\\Анатолий\\Desktop\\Info_Anatoly"))