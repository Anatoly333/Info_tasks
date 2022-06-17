"""Replace all occurrences of strings 'replace_from' on 'replace_from' in folder with .c extension, with timing and multiprocessing."""
from multiprocessing import Process
import os
import time

start_time = time.time()


def get_file_paths_by_os(root: str):
    """Return file paths for every file in root and its subdirectories, using os."""
    files = []
    all_paths = []
    files = list(os.walk(root))
    for names in files:
        for file_names in names[2]:  # names[2] = array of all_paths
            all_paths.append(os.path.join(names[0], file_names))
    return all_paths


def create_process(all_paths, replace_from, replace_to):
    """Creating multiprocessing processes."""
    amount_data_in_process = len(all_paths) // 2
    first_paths = all_paths[:amount_data_in_process]
    second_paths = all_paths[amount_data_in_process:]
    process_1 = Process(target=replace_text, args=(first_paths, replace_from, replace_to))
    process_2 = Process(target=replace_text, args=(second_paths, replace_from, replace_to))
    process_1.start()
    process_2.start()
    process_1.join()


def replace_text(all_paths, replace_from, replace_to):
    """Replacing text in folder."""
    for file_path in all_paths:
        if file_path.split('.')[-1] == 'c':  # file extension
            with open(file_path, 'r') as file:
                filedata = file.read()
            filedata = filedata.replace(replace_from, replace_to)

            with open(file_path, 'w') as file:
                file.write(filedata)


def replace_text_in_folder_multiprocess(path, replace_from, replace_to):
    """Replace all occurrences of strings 'replace_from' on 'replace_from' in folder using multiprocessing"""
    all_paths = get_file_paths_by_os(path)
    create_process(all_paths, replace_from, replace_to)


if __name__ == '__main__':
    print(replace_text_in_folder_multiprocess('/content/gdrive/MyDrive/project_folder/cpython', 'Return', 'Saturn'))
    print(f"--- {time.time() - start_time}s seconds ---")
