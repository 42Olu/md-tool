import tkinter as tk 
import os
from utils import *
from tkinter import messagebox
from tkinter import filedialog
from process_description import PD_handler

def recover_keywords():
    """
    The purpose of this Function is to recover keywords from a given metadata file
    or initialize new empty keywords
    """
    root = tk.Tk()
    root.withdraw()

    if os.path.isfile("keywords.pkl"):
        print("You do not want to go there yet!")
        exit()

    if messagebox.askyesno("Recovering Keywords", "Yes: to try and recover from Metadata from metadata file\nNo:  to create a new empty keyword file"):
        md = filedialog.askopenfilename()
        with open(md, "r") as f:
            lines = f.readlines()

        lines = lines[2:]
        keys = [line.split(":")[0] for line in lines]
        if messagebox.askyesno("Found Keys", "Found the following keys:\n"+str(keys)+"\nDo you want to save them?"):
            save_keywords(keys)
            return True
    else:
        if messagebox.askyesno("Recovering Keywords", "Warning: this could overwrite existing Metadata\n\nYes: to initialize new empty keywords.pkl\nNo:  to cancel"):
            save_keywords(["process description"])
            return True
    return False


def recover_processes():
    """
    The purpose of this Function is to recover processes from a given working directory
    or initialize new empty processes
    """
    root = tk.Tk()
    root.withdraw()

    if os.path.isfile("processes.pkl"):
        print("You do not want to go there yet!")
        exit()

    if messagebox.askyesno("Recovering Process Description", "Yes: to try and recover them from a data directory\nNo:  to create an empty processes.pkl"):
        dir = filedialog.askdirectory()
        # initialize metadata file list
        metadata_file_list = []

        # create directory walk
        w = os.walk(dir)
        # filling the list with all file paths
        for root, _, files in w:
            # iterate over all files
            for f in files:
                # create the path
                path = os.path.join(root, f)

                # check if metadata is in the filename or directory above
                if  "metadata" in f or "metadata" in os.path.split(root)[1]:
                    metadata_file_list.append(path)

        descriptions = []

        # loop over the metadata files and search non empty descriptions
        for md in metadata_file_list:
            with open(md, "r") as f:
                lines = f.readlines()
            lines = [line.replace("\n", "") for line in lines]

            pd = lines[2].split("::  ")[1]

            if pd != "":
                descriptions.append(pd)

        # create empty process handler
        processes = PD_handler()

        if len(descriptions) == 0:
            if messagebox.askyesno("Recovering Process Descriptions", "Could not find existing descriptions\n\nDo you want to initalize an empty processes.pkl?"):
                save_processes(processes)
                return True
            else:
                return False

        if messagebox.askyesno("Recovering Process Descriptions", "Found the following descriptions:\n" + str(descriptions) + "\nDo you want to save them?"):
            for i,descr in enumerate(descriptions):
                processes["descr_"+str(i+1)] = descr

            save_processes(processes)
            messagebox.showinfo("Attention", "The descriptions where saved with placeholder names!\nTo change the names use the edit description button in the tool.")
            return True       
    else:
        if messagebox.askyesno("Recovering Process Descriptions", "Warning: this could overwrite existing Process Descriptions\n\nYes: to initialize an empty processes.pkl\nNo:  to cancel"):
            save_processes(PD_handler())
            return True
    return False