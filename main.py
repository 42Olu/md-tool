import os
from md_file import MD_file
from utils import *
import tkinter as tk
import tkinter.ttk as ttk
from GUI import GUI
from process_description import PD_handler
from tkinter import messagebox
from recovery import *


def main():
    """
    Function which starts the main program loop
    """
    root = tk.Tk()
    root.withdraw()
    # load the list filled with keywords
    keywords = load_keywords()

    if keywords == []:
        if messagebox.askyesno("keywords.pkl not found", "keywords.pkl not found.\nDo you want to try to recover the keywords?"):
            if recover_keywords():
                messagebox.showinfo("keywords.pkl", "Successfully saved keywords.pkl\nRestart the tool now.")
            else:
                messagebox.showinfo("keywords.pkl not found", "You did not recover the keywords.")
        else:
            messagebox.showinfo("keywords.pkl not found", "You did not recover the keywords.")
        exit()

    # load the process descriptions
    processes = load_processes()
    
    if processes is None:
        if messagebox.askyesno("processes.pkl not found", "processes.pkl not found.\nDo you want to try to recover process descriptions?"):
            if recover_processes():
                messagebox.showinfo("processes.pkl", "Successfully recovered processes.pkl\nRestart the tool now.")
            else:
                messagebox.showinfo("processes.pkl not found", "You did not recover the process descriptions.")
        else:
            messagebox.showinfo("processes.pkl not found", "You did not recover the process descriptions.")
        exit()

    # choose a working directory
    working_dir = get_working_dir()

    if not type(working_dir) is str:
        exit()

    # search for unkown keywords or processes in the working directory
    reload_keywords, reload_processes = recover_from_other_users(working_dir, keywords, processes)

    if reload_keywords:
        keywords = load_keywords()

    if reload_processes:
        processes = load_processes()

    # create the list with all file paths
    data_file_list = create_data_file_list(working_dir)

    # create the MD_file_dict
    MD_files = create_MD_file_dict(data_file_list, keywords)
    
    # create the gui object
    gui_handler = GUI(working_dir, MD_files, keywords, processes)
    # start the mainloop
    gui_handler.start_mainloop()
    

    



# execute main if main.py is run
if __name__ == "__main__":
    main()