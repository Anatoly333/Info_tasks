"""Replace all occurrences of strings 'replace_from' on 'replace_from' in folder with .c extension, with timing."""
import os
import time

start_time = time.time()


def replace_text_in_folder(path, replace_from, replace_to):
    """Replace all occurrences of strings 'replace_from' on 'replace_from' in folder."""
    files = []
    all_paths = []
    files = list(os.walk(path))
    for names in files:
        for file_names in names[2]:  # names[2] = array of all_paths
            all_paths.append(os.path.join(names[0], file_names))

    for file_path in all_paths:
        if file_path.split('.')[-1] == 'c':  # file extension
            with open(file_path, 'r') as file:
                filedata = file.read()
            filedata = filedata.replace(replace_from, replace_to)

            with open(file_path, 'w') as file:
                file.write(filedata)


if __name__ == '__main__':
    print(replace_text_in_folder('/content/cpython', 'Saturn', 'Return'))
    print(f"--- {time.time() - start_time}s seconds ---")
