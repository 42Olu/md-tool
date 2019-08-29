import os
from md_file import MD_file
from utils import *
import tkinter as tk
import tkinter.ttk as ttk


class GUI:
    """
    Class to handle the GUI elements.
    this includes:
        - a treeview as a file browser
        - a list of editable metadata entries
        - buttons to edit the processing steps
        - buttons for fast process options
        - buttons to add and remove keywords
    """
    def __init__(self, working_dir, MD_files, keywords):
        """
        Initializes the GUI handler

            working_dir     - string    ... path to the working directory
            MD_files        - dict      ... dict containing MD_file dict wrapper for the metadata files
            keywords        - list      ... list containing all metadata keywords 
        """
        # saving important parameters
        self.working_dir = working_dir
        self.MD_files = MD_files
        self.keywords = keywords

        # creating the tk master window
        self.master = tk.Tk()
        self.master.title("Metadata Tool")

        # creating a frame for the treeview
        self.tree_frame = tk.Frame(self.master)

        # fixing the geometry so that the window is resizable
        self.tree_frame.grid(column=0, row=0, sticky="nsew", padx = 10, pady = 10)
        self.master.rowconfigure(0, weight=1)

        # creating the treeview object which is used to display the files in working_dir
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.heading("#0" ,text="File List")
        self.tree.pack(expand=True, fill='y')

        # filling the treeview object
        self.root = self.tree.insert('', 'end', text=self.working_dir, open=True)
        self.create_treeview(self.working_dir, self.root)

        # binding the double click event to the treeview object to open the clicked file
        self.tree.bind("<Double-1>", self.on_double_click)

        # topframe is needed to create the list of entries later on
        self.topframe = None


    def create_treeview(self, path, parent):   
        """
        Recursive function which adds an tree element for each data file in the given path

            path    - string        ... path to the directory which should be processed
            parent  - tree element  ... the parent element of this directory
        """ 
        # iterate over all elements in path
        for p in os.listdir(path):
            # concatenate the path and p
            abspath = os.path.join(path, p)
            # checking if its not a metadata directory
            if not "metadata" == p:
                #insert the element into the treeview
                parent_element = self.tree.insert(parent, 'end', text=p, open=True)

                # if the added element is a directory 
                if os.path.isdir(abspath):
                    # execute this function with the directory and the directory element as parent
                    self.create_treeview(abspath, parent_element)

    def get_tree_path(self, item):
        """
        Recursive Function to calculate the filepath to a given tree element.

            item    - tree element  ... the element of the tree view for which the path should be created
        returns
            path    - string        ... file path to the tree element
        """
        if self.tree.parent(item) == "":
            return self.tree.item(item)["text"]
        else:
            return os.path.join(self.get_tree_path(self.tree.parent(item)), self.tree.item(item)["text"])

    def frame_focus(self, event):
        """
        Reset the scroll region to encompass the inner frame
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_resize(self, event):
        """
        Function to resize the entry list if the canvas is resized
        """
        padding = 10
        width = self.canvas.winfo_width() - padding
        self.canvas.itemconfigure("entries", width=width)

    def create_entry_list(self):
        """
        Function to create a scrollable resizable list of tkinter widgets
        """
        # to get a scrollable list of tkinter widgets which are resizable the following steps are needed:
        # 1. create a top frame
        #       this frame will hold the canvas and scrollbar so that they are the same size and can be displayed on the grid
        self.topframe = tk.Frame(self.master)
        # 2. set sticky to all 4 directions and the weight to >0 that the frame can be resized if the window dimensions change  
        self.topframe.grid(column=1, row=0, sticky="nsew", padx = 10, pady = 10)
        self.master.columnconfigure(1, weight=4)

        # 3. create the canvas and the scrollbar in the top frame 
        self.canvas = tk.Canvas(self.topframe)
        self.scrollbar = tk.Scrollbar(self.topframe, orient="vertical", command=self.canvas.yview)
        # 4. add the scrollbar to the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 5. create the frame for the widgets on the canvas
        self.entry_frame = tk.Frame(self.canvas)
        
        # 6. grid the scrollbar and the canvas
        self.scrollbar.grid(row=0,column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        # 7. set the weights for the canvas and scrollbar so that they are resizable
        self.topframe.rowconfigure(0, weight=4)
        self.topframe.columnconfigure(0, weight=4)

        # 8. blit the widget frame onto the canvas
        self.canvas.create_window((0,0),window=self.entry_frame,anchor='nw', tags=["entries"])
        
        # 9. bind a function to the widget frame that it stays in focus and cant be scrolled away
        self.entry_frame.bind("<Configure>", self.frame_focus)
        # 10. bind a function to the canvas which updates the width of the widget frame if the window is resized 
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # setting the weigth of the entries to 1 so that they stretch if the window is resized
        self.entry_frame.columnconfigure(1, weight=1)

        self.label_list = []
        self.entry_list = []
        self.stringvar_list = []

        # 11. finally add the planned widgets on the widget frame
        self.file_name = tk.StringVar(self.master)
        self.entry_list_title = tk.Label(self.entry_frame, font = "Courier 16", textvariable=self.file_name)
        self.entry_list_title.grid(row=0, columnspan=2, sticky="ew", pady=3, padx=15)
        for i,keyword in enumerate(self.keywords):
            self.label_list.append(tk.Label(self.entry_frame, font = "Courier 11", text=keyword).grid(row=i+1,column=0, sticky="w", pady=1, padx=4))

            self.stringvar_list.append(tk.StringVar(self.master))
            self.entry_list.append(tk.Entry(self.entry_frame, font = "Courier 11", textvariable=self.stringvar_list[-1]))
            self.entry_list[-1].grid(row=i+1, column=1, sticky="ew", pady=1)

    def on_double_click(self, event):
        """
        Function which handles the double click event on a tree element
        inspired by:
            https://stackoverflow.com/questions/3794268/command-for-clicking-on-the-items-of-a-tkinter-treeview-widget
        """
        # first identify the tree element
        element = self.tree.identify('item',event.x,event.y)
        # second get the path of this tree element
        path = self.get_tree_path(element)

        # check if the path is a directory (only files should be opened)
        if os.path.isdir(path):
            return

        # control output
        print("changed to file: ", path)
        # this bool determines if the metadata should be saved if the file is changed
        save_md = True

        # check if the entry list was already created
        # this is needed to set the focus on the first double clicked file
        if self.topframe is None:
            self.create_entry_list()
            # do not save empty strings if this is the first opened file
            save_md = False

        if save_md:
            old_path = os.path.join(self.working_dir, self.file_name.get())
        self.file_name.set(os.path.relpath(path, self.working_dir))
        for i,keyword in enumerate(self.keywords):
            if save_md:
                self.MD_files[old_path][keyword] = self.stringvar_list[i].get()
            self.stringvar_list[i].set(self.MD_files[path][keyword])


    def start_mainloop(self):
        """
        Function which starts the tkinter main loop
        """
        self.master.mainloop()