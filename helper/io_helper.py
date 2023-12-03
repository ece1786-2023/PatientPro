import os
import sys
import re

def extract_num(fn):
    match = re.search(r'(\d+)', fn)
    return int(match.group()) if match else 0

def get_dir_files(dir_path):
    file_names = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_names.append(os.path.join(root, file))

    file_names.sort(key=extract_num)
    return file_names

def read_file_list(file_paths):
    records = []
    for path in file_paths:
        if os.path.exists(path):
            with open(path, 'r') as file:
                records.append(file.read())
        else:
            print(f"[ERROR] File not found: {path}")
    if records == []:
        print("[ERROR] empty directory")
        sys.exit()
    return records