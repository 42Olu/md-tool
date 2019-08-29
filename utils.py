import os
import tkinter as tk
from tkinter import filedialog
from md_file import MD_file
import pickle


"""
This file contains useful utility functions:

    load_keywords()
    save_keywords(keyword_list)
    get_working_dir()
    create_data_file_list(dir)
    create_MD_file_dict(data_files, keywords)
"""

def load_keywords():
    """
    Function which loads the metadata tags from keywords.pkl

    returns:
        keywords - list     ... list containing the keywords as strings
    """
    keywords = []

    # check if keywords.txt is a file
    if os.path.isfile("keywords.pkl"):
        # open the file and read the lines
        with open("keywords.pkl", "rb") as f:
            # depickle the saved list
            keywords = pickle.load(f)
    return keywords


def save_keywords(keywords):
    """
    Function to save the keywords to keyword.pkl

        keywords - list     ... list containing all keywords as strings
    """

    # open the file 
    with open("keywords.pkl", "wb") as f: 
        # serialize and dump the list
        pickle.dump(keywords, f)


def get_working_dir():
    """
    Function which executes the open file dialog and gets the working directory
    """
    # select the working_dir
    root = tk.Tk()
    # withdraw the standard window which is created
    root.withdraw()
    working_dir = filedialog.askdirectory()
    return working_dir


def create_data_file_list(dir):
    """
    Function to create a list of all files in a given directory
    
        dir - string/path   ... path to the working directory
    returns:
        file_list - list    ... containg paths to all files in the working directory
    """
    # initialize data file list
    data_file_list = []

    # create directory walk
    w = os.walk(dir)
    # filling the list with all file paths
    for root, _, files in w:
        # iterate over all files
        for f in files:
            # create the path
            path = os.path.join(root, f)

            # check if metadata is in the filename or directory above
            if not "metadata" in f and not "metadata" in os.path.split(root)[1]:
                data_file_list.append(os.path.join(root, f))

    return data_file_list

    
def create_MD_file_dict(data_files, keywords):
    """
    Function that creates a dict of MD_file objects
    as pseudo dict wrapper around the metadata files.

    This also creates empty metadata files if no files are present.

        data_files   - list   ... containing all paths to data files
        keywords     - list   ... list with all keywords as strings
    returns:
        MD_file_dict - dict   ... containing one MD_file for each data file, the key is the path to the datafile
    """
    # initialize empty dict
    MD_file_dict = {}
    # iterate over the data files
    for data_file in data_files:
        # fill the dict
        MD_file_dict[data_file] = MD_file(data_file, keywords)
    return MD_file_dict