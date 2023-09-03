#!python3
# Directory Maintainer
# Organizes the files within a directory
# Usage: python3 main.py [path/to/directory] [--log-window=N] [--size-threshold=M]
import argparse
import os
import shutil

import pprint
pp = pprint.PrettyPrinter(indent=4)

import re
from functools import reduce


def clean_directory(directory, log_window, size_threshold):
    # Implement the directory cleaning functionality here
    if pathExists(directory) and pathIsDirectory(directory):
        # Files in the directory
        base_directory = os.path.abspath(directory)

        files = [ os.path.join(base_directory, f) for f in os.listdir(directory) ]

        # Log file extensions
        extentions = ['.csv', '.log', '.txt']

        groups_files_dictionary = {
            "unrecognized_files": [],
            ".csv": [],
            ".log": [],
            ".txt": [],
        }

        for file_name in files:
            file_path = os.path.join(base_directory, file_name)
            if(os.path.exists(file_path)):
                pattern = r'\.([^\.]+)$'
                extension = re.search(pattern, file_name)
                ext = extension.group() if extension  else None
                if(not os.path.isdir(file_name) and ext in extentions):
                        if ext not in groups_files_dictionary:
                             groups_files_dictionary[ext] = []
                        groups_files_dictionary[ext].append(file_name)
                else:
                    if not file_name.split('/')[-1] in [fn[1:] for fn in extentions] :
                        groups_files_dictionary["unrecognized_files"].append(file_name)
        
        # Collect sorted files by creation time
        sortedLogFiles = sortFilesByTimeStamp(groups_files_dictionary[".log"])

        sortedCsvFiles = sortFilesByCreationDate(groups_files_dictionary[".csv"])

        # Retain N most recent log files
        retainOnlyRecentFiles(log_window, sortedLogFiles, os.path.join(base_directory, "log"))

        # Retain N most recent csv files
        retainOnlyRecentFiles(log_window, sortedCsvFiles, os.path.join(base_directory, "csv"))

        # Separate small txt files from large txt files
        smallTxtFiles, largeTxtFiles = separateLargeFiles(groups_files_dictionary[".txt"], size_threshold)

        # Sort small txt files by creation date
        sortedSmallTxtFiles = sortFilesByCreationDate(smallTxtFiles)
        # Sort large txt files by creation date
        sortedLargeTxtFiles = sortFilesByCreationDate(largeTxtFiles)

        # Retain N most recent small txt files
        retainOnlyRecentFiles(log_window, sortedSmallTxtFiles, os.path.join(base_directory, "txt"))

        # Retain N most recent large txt files
        retainOnlyRecentFiles(log_window, sortedLargeTxtFiles, os.path.join(base_directory, "txt", "large_txt_files"))

        # Unrecognized files
        unknownFiles(groups_files_dictionary["unrecognized_files"])

def unknownFiles(files):
    for f in files:
        print("Unknown extension: " + f.split('/')[-1])

def pathExists(path_to_file):
    if not os.path.exists(path_to_file):
        print(f"The Path '{directory}' does not exist.")
        return False
    return True

def pathIsDirectory(path_to_file):
    if not os.path.isdir(path_to_file):
        print(f"'{path_to_file}' is not a directory.")
        return False
    return True

def moveFile(destination, source):
    if not os.path.exists(destination):
        # If the directory does not exist create a new one
        os.makedirs(destination)

    # shutil.move(source, destination)
    dest = os.path.join(destination, source.split("/")[-1])
    if os.path.exists(dest):
        if os.path.isdir(dest):
           shutil.rmtree(dest)
        else:
            os.remove(dest)
        shutil.move(source, destination)
    else:
        shutil.move(source, destination)
    

def deleteFile(path_to_file):
    if os.path.exists(path_to_file):
        if os.path.isdir(path_to_file):
            shutil.rmtree(path_to_file)
            print(f"DELETED DIRECTORY :   {path_to_file}")
        else:
            os.remove(path_to_file)
            print(f"DELETED FILE      :   {path_to_file}")

def retainOnlyRecentFiles(N, files, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
        pass
    for f in files[0:-N]:
        deleteFile(f)
        pass
    for f in files[-N:]:
        moveFile(destination, f)
        pass

def separateLargeFiles(files, threshold):
    small_files = []
    large_files = []
    for f in files:
        file_size = os.path.getsize(f) / 1024
        if file_size > threshold:
            large_files.append(f)
        else:
            small_files.append(f)
    return [small_files, large_files]

def sortFilesByCreationDate(file_paths):
    new_file_paths = [*file_paths]
    new_file_paths.sort(key=lambda x: os.stat(x).st_mtime)
    return new_file_paths

def sortFilesByTimeStamp(log_files):
    pattern = r'^(\d{8})'
    yyyymmddSortable = [ file_name for file_name in log_files if re.search(pattern, file_name.split("/")[-1])]
    yyyymmddSortable.sort(key=lambda f: re.search(pattern, f.split("/")[-1]).group())
    return yyyymmddSortable
        

# This code reads the command line arguments and passes them into the
# clean_directory function.
# It sets the defaults for the log window and the size threshold
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean up a messy data directory')
    parser.add_argument('directory', help='the directory to clean')
    parser.add_argument('--log-window',
            dest='log_window',
            default=30, # retain 30 log files by default
            type=int, 
            help='log retention policy: how many most recent log files to keep')
    parser.add_argument('--size-threshold',
            dest='size_threshold',
            default=50, # 50KB default
            type=int, 
            help='file size threshold: how large is a large text file')
    directory = parser.parse_args().directory
    log_window = parser.parse_args().log_window
    size_threshold = parser.parse_args().size_threshold

    clean_directory(directory, log_window, size_threshold)
