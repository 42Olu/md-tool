import os
from md_file import MD_file
from utils import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


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
    def __init__(self, working_dir, MD_files, keywords, processes):
        """
        Initializes the GUI handler

            working_dir     - string    ... path to the working directory
            MD_files        - dict      ... dict containing MD_file dict wrapper for the metadata files
            keywords        - list      ... list containing all metadata keywords 
            processes       - PD_handler... object which handels the process descriptions
        """
        # saving important parameters
        self.working_dir = working_dir
        self.MD_files = MD_files
        self.keywords = keywords
        self.processes = processes

        # creating the tk master window
        self.master = tk.Tk()
        self.master.title("Metadata Tool")

        # creating a frame for the treeview
        self.tree_frame = tk.Frame(self.master)

        # fixing the geometry so that the window is resizable
        self.tree_frame.grid(column=0, row=0, sticky="nsew", padx = 10, pady = 10)
        self.master.rowconfigure(0, weight=1)

        # creating the treeview object which is used to display the files in working_dir
        # using selectmode browse disables multiple selections in the treeview
        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse")
        self.tree.heading("#0" ,text="File List")
        self.tree.grid(column=0, row=1, sticky="ns")
        self.tree_frame.rowconfigure(1, weight=1)

        # loading the logo (as a gif because tkinter)
        # and displaying the logo abouth the tree view
        self.logo_canvas = tk.Canvas(self.tree_frame, width=200, height=64)
        self.logo = tk.PhotoImage(master=self.logo_canvas, file="saldilogo.gif")
        self.logo_canvas.create_image((0,0), image=self.logo, anchor="nw")
        self.logo_canvas.grid(column=0, row=0, sticky="nw", pady=5)

        # filling the treeview object
        self.root = self.tree.insert("", "end", text=os.path.relpath(self.working_dir, os.getcwd()), open=True)
        self.create_treeview(self.working_dir, self.root)

        # binding the tree select event to the treeview object to open the selected metadata file
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_selection)

        # topframe is needed to create the list of entries later on
        self.topframe = None

        # file_name=None is needed to counter a bug when adding or removing keywords
        # but no tree item is selected
        self.file_name = None

        # the last opened metadata file to copy from it
        self.last_opened_file = None


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
                parent_element = self.tree.insert(parent, "end", text=p, open=True)

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
            return os.path.abspath(os.path.join(self.get_tree_path(self.tree.parent(item)), self.tree.item(item)["text"]))

    def edit_scroll_frame_focus(self, event, edit_canvas):
        """
        Function so that the edit window scroll region stays in focus
        """
        edit_canvas.configure(scrollregion=edit_canvas.bbox("all"))

    def frame_focus(self, event):
        """
        Reset the scroll region to encompass the inner frame
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_edit_canvas_resize(self, event, edit_canvas):
        """
        Function to resize the entry list if the canvas is resized
        """
        padding = 10
        width = edit_canvas.winfo_width() - padding
        edit_canvas.itemconfigure("edit", width=width)

    def on_canvas_resize(self, event):
        """
        Function to resize the entry list if the canvas is resized
        """
        padding = 10
        width = self.canvas.winfo_width() - padding
        self.canvas.itemconfigure("entries", width=width)

    def on_return_button(self, event, i):
        """
        function to jump to the next entry box and save the metadata if return is pressed

            i   - index     ... index of the entry in the entry list
        """
        if i < len(self.entry_list)-1: # exclude the last entry
            self.entry_list[i+1].focus_set()

        # get the path to the data file
        path = os.path.abspath(self.file_name.get())
        # save the metadata of the entry box
        self.MD_files[path][self.keywords[i]] = self.stringvar_list[i].get()

    def on_up_button(self, event, i):
        """
        function to jump to the previous entry box and save the metadata if the up arrow is pressed

            i   - index     ... index of the entry in the entry list
        """
        if i > 1: # exclude the first entry
            self.entry_list[i-1].focus_set()

        # get the path to the data file
        path = os.path.abspath(self.file_name.get())
        # save the metadata of the entry box
        self.MD_files[path][self.keywords[i]] = self.stringvar_list[i].get()

    def on_entry_focus_loss(self, event, i):
        """
        function to save the metadata if an entry looses focus

            i   - index     ... index of the entry in the entry list
        """
        # get the path to the data file
        path = os.path.abspath(self.file_name.get())
        # save the metadata of the entry box
        self.MD_files[path][self.keywords[i]] = self.stringvar_list[i].get()

    def on_ctrl_s(self, event):
        """
        Function to save the current metadata if ctrl + s are pressed
        """
        # save the metadata
        self.save_current_metadata()
        # set focus to the master window
        # this indicates to the user that something happened
        self.master.focus_set()

    def bind_mousewheel(self, event):
        """
        Function to bind mouse wheel to scrolling when the mouse enters the entry frame
        """
        # windows
        self.master.bind('<MouseWheel>', self.on_mousewheel) 
        # linux
        self.master.bind('<Button-4>', self.on_mousewheel)
        self.master.bind('<Button-5>', self.on_mousewheel)

    def unbind_mousewheel(self, event):
        """
        Function to unbind the mouse wheel if the mouse leaves the entry frame
        """
        # windows
        self.master.unbind('<MouseWheel>') 
        # linux
        self.master.unbind('<Button-4>')
        self.master.unbind('<Button-5>')

    def on_mousewheel(self, event):
        """
        Function which binds mouse wheel to scrolling the canvas
        """
        if event.num == 5 or event.delta < 0:
            v = 1
        if event.num == 4 or event.delta > 0:
            v = -1
        self.canvas.yview_scroll(v, "units")

    def on_tree_selection(self, event, from_window=False):
        """
        Function which handles the tree selection element
        inspired by:
            https://stackoverflow.com/questions/34849035/how-to-get-the-value-of-a-selected-treeview-item
        """
        
        if not len(self.tree.selection()) == 0:
            # first identify the selected tree element
            element = self.tree.selection()[0]
            # second get the path of this tree element
            path = self.get_tree_path(element)
        else:
            path = os.path.abspath(self.last_selection)

        # check if the path is a directory (only files should be opened)
        if os.path.isdir(path):
            self.tree.selection_remove(element)
            return
        else:
            self.last_selection = path

        # abort if the file is already opened
        if not self.topframe is None and os.path.abspath(self.file_name.get()) == path:
            return
        # control output
        print("changed to file: ", path)
        # this bool determines if the metadata should be saved if the file is changed
        save_md = True

        # if coming from the add/remove window do not save
        if from_window:
            save_md = False

        # check if the entry list was already created
        # this is needed to set the focus on the first double clicked file
        if self.topframe is None:
            self.create_entry_list()
            # do not save empty strings if this is the first opened file
            save_md = False

        # if we want to save the metadata 
        # (everytime except the first time we click on a data file because then the entry variables are empty)
        if save_md:
            # save the path of the closed data file in a temp variable to save the meta data
            old_path = os.path.abspath(self.file_name.get())
        
        # set the filename label to the newly opened file
        self.file_name.set(os.path.relpath(path, os.getcwd()))

        if save_md:
            self.last_opened_file = []
        # iterate over the keywords and load the metadata from the corresponding file
        # save the metadata of the closed file to the disc
        # (everytime except the first time we click on a data file because then the entry variables are empty)
        for i,keyword in enumerate(self.keywords):
            if save_md:
                # save the last opened information
                self.last_opened_file.append(self.stringvar_list[i].get())
            # process description
            if i == 0:
                # make sure the process description is valid and use No Description if not
                if not self.stringvar_list[i].get() in self.processes.get_process_names():
                    self.stringvar_list[i].set(self.processes[[""]])

                if save_md:
                    self.MD_files[old_path][keyword] = self.processes[self.stringvar_list[i].get()]

                # make sure, that an up to date description is saved
                if not self.MD_files[path][keyword] in self.processes.get_process_descriptions():
                    self.MD_files[path][keyword] = self.processes[self.stringvar_list[i].get()]
                self.stringvar_list[i].set(self.processes[[self.MD_files[path][keyword]]])
            # every other entry
            else:
                if save_md:
                    self.MD_files[old_path][keyword] = self.stringvar_list[i].get()
                self.stringvar_list[i].set(self.MD_files[path][keyword])

    def save_current_metadata(self, path=None):
        """
        Function which saves the metadata for the currently opened file
        """
        # if a file was opened
        if not self.topframe is None:
            # if no path is given
            if path is None:
                # create the path
                path = os.path.abspath(self.file_name.get())

            # save each entry
            for i,keyword in enumerate(self.keywords):
                if i == 0:
                    self.MD_files[path][keyword] = self.processes[self.stringvar_list[i].get()]
                else:
                    self.MD_files[path][keyword] = self.stringvar_list[i].get()

    def update_keywords(self, keyword_string, window):
        """
        Function to update the keywords after the add/remove window

            keyword_string  - string        ... input string from the add/remove text
            window          - tk.Toplevel   ... the opened window to close it correctly
        """

        # parse the keyword string
        keyword_list = keyword_string.split("\n")

        # remove duplicates but keep order
        seen = set()
        unique_data = []
        for key in keyword_list:
            if key not in seen:
                unique_data.append(key)
                seen.add(key)

        # iterate over the string and trim whitespace
        keyword_list = [key.replace("\n", "").strip() for key in keyword_list]

        # remove empty strings
        while "" in keyword_list:
            keyword_list.remove("")

        # check if the list is empty
        if len(keyword_list) == 0:
            # no keywords should not be possible
            return

        keyword_list.insert(0, self.keywords[0])

        if messagebox.askokcancel("Save Keywords", "Do you want to update the Keywords?"):
            # close the window and free self.master
            window.destroy()

            # save current metadata
            self.save_current_metadata()

            # iterate over the md files and update the keywords
            for md in self.MD_files:
                # update keywords
                self.MD_files[md].set_keywords(keyword_list)
                # save md to disc
                self.MD_files[md].write()
            
            # update keywords of gui
            self.keywords = keyword_list

            # update the gui
            self.create_entry_list()
            # get the last selection and make sure no data is lost
            self.on_tree_selection(None, from_window=True)

            # save the new keyword list
            save_keywords(self.keywords)

    def create_add_remove_window(self):
        """
        Function which opens the add and remove keyword window.
        """
        def reset_text():
            """
            function needed to reset the text widget
            """
            # 1. clear the text widget
            keyword_text.delete('1.0', "end")
            # 2. insert the keywords
            for i, key in enumerate(self.keywords):
                if i != 0:
                    keyword_text.insert("end", key + '\n')

        # create a second window and force it to the top
        add_remove = tk.Toplevel(self.master)
        add_remove.grab_set()
        add_remove.title("add/remove keywords")

        # create a label with instructions
        tk.Label(add_remove, text="Instructions", font = "Courier 18").grid(column=0, row=0, padx=10, pady=10, sticky="w")
        tk.Label(add_remove, text="\t- one keyword per line", font = "Courier 12").grid(column=0, row=1, padx=10, pady=2, sticky="w")
        tk.Label(add_remove, text="\t- order of lines is the order of keywords", font = "Courier 12").grid(column=0, row=2, padx=10, pady=2, sticky="w")
        tk.Label(add_remove, text="\t- whitespace at the beginning and end of the line will be trimmed", font = "Courier 12").grid(column=0, row=3, padx=10, pady=2, sticky="w")
        tk.Label(add_remove, text="\t- do not use \\n in a keyword", font = "Courier 12").grid(column=0, row=4, padx=10, pady=2, sticky="w")
        tk.Label(add_remove, text="\nAttention:", font = "Courier 16").grid(column=0, row=5, padx=10, pady=10, sticky="w")
        tk.Label(add_remove, text="\t- changing an existing keyword is the same as removing it and adding a new one", font = "Courier 12").grid(column=0, row=6, padx=10, pady=2, sticky="w")                        
        tk.Label(add_remove, text="\t  -> metadata could be lost!", font = "Courier 12").grid(column=0, row=7, padx=10, pady=2, sticky="w")
        tk.Label(add_remove, text="\t- use right click on a keyword in the main window to edit it", font = "Courier 12").grid(column=0, row=8, padx=10, pady=2, sticky="w")

        # create the editor widget
        keyword_text = tk.Text(add_remove, font = "Courier 12")
        keyword_text.grid(columnspan=2, row=9, sticky="nsew", padx=10, pady=10)
        add_remove.rowconfigure(9, weight=1)

        # load the keywords
        reset_text()

        # add control buttons
        reset_button = tk.Button(add_remove, text="reset", 
                                 font = "Courier 12", bg="gray", 
                                 command=reset_text)
        reset_button.grid(column = 1, row = 10, sticky="ew", pady=10, padx=10)

        save_button = tk.Button(add_remove, text="save", 
                                 font = "Courier 12", bg="gray", 
                                 command=lambda : self.update_keywords(keyword_text.get("1.0","end"), add_remove))
        save_button.grid(column = 0, row = 10, sticky="ew", pady=10, padx=10)

        # clicking the x should mirror the effect of clicking the save button
        add_remove.protocol("WM_DELETE_WINDOW", add_remove.destroy)


    def update_processes(self, descr, old_name, name, edit_window, edit_processes_window):
        """
        Function to update the process description after closing the description editor

            descr       - string        ... description of the process
            name        - name          ... name of the process
            edit_window - tk.Toplevel() ... the editor window
        """
        descr = descr.replace("\n", " ")

        if name == "":
            return

        if name in self.processes.get_process_names() and name != old_name:
            return

        if descr in self.processes.get_process_descriptions() and (old_name == "+" or descr != self.processes[old_name]):
            return

        # close the window and free self.master
        edit_window.destroy()

        # check if the old name is currently selected in the open file
        if old_name == self.stringvar_list[0].get():
            self.stringvar_list[0].set(name)

        # if the name needs to be updated
        if old_name in self.processes.get_process_names() and name != old_name:
            # if the description needs to be updated
            if self.processes[old_name] != descr:
                # update the saved descriptions for old name
                for md in self.MD_files:
                    # if one md file uses the old description
                    if self.MD_files[md][self.keywords[0]] == self.processes[old_name]:
                        # set the new description
                        self.MD_files[md][self.keywords[0]] = descr
                # update the internal description
                self.processes[old_name] = descr
            # update the name of the edited process
            self.processes[[descr]] = name
        else:
            self.processes[name] = descr

        save_processes(self.processes)
        edit_processes_window.destroy()
        self.create_edit_process_window()


    def edit_process(self, name, edit_processes_window):
        """
        Function which opens an editor window to edit a process description

            name    - string    ... name of the process description
        """
        def reset_text():
            """
            function needed to reset the text widget
            """
            # 1. clear the text widget
            editor.delete('1.0', "end")
            if name in self.processes.get_process_names():
                # 2. insert the description
                editor.insert("end", self.processes[name])

        # create a window and force it to the top
        edit_process = tk.Toplevel(self.master)
        edit_process.grab_set()
        if name == "+":
            edit_process.title("add process description")
        else:
            edit_process.title(name)

        # create the entry for the name
        name_entry_stringvar = tk.StringVar(edit_process, value="")
        if name != "+":
            name_entry_stringvar.set(name)
        name_entry = tk.Entry(edit_process, textvariable=name_entry_stringvar, font="Courier 12")
        name_entry.grid(columnspan=2, row=1, sticky="we", padx=10, pady=10)
        edit_process.rowconfigure(1)

        tk.Label(edit_process, font="Courier 12", text="Name:").grid(column=0, row=0, sticky="w", padx=5, pady=5)
        tk.Label(edit_process, font="Courier 12", text="Process Description:").grid(column=0, row=2, sticky="w", padx=5, pady=5)

        # create the textbox for the description
        editor = tk.Text(edit_process, font = "Courier 12")
        editor.grid(columnspan=2, row=3, sticky="nsew", padx=10, pady=10)
        edit_process.rowconfigure(3, weight=1)

        reset_text()

        # bind ctrl + s to exit window + save
        edit_process.bind('<Control-s>', lambda x: self.update_processes(editor.get("1.0","end"), name, name_entry.get(), edit_process, edit_processes_window))

        edit_process.protocol("WM_DELETE_WINDOW", lambda : self.update_processes(editor.get("1.0","end"), name, name_entry.get(), edit_process, edit_processes_window))

        # adding save button
        tk.Button(edit_process, text="save", 
                  font = "Courier 12", bg="gray", 
                  command=lambda : self.update_processes(editor.get("1.0","end"), name, name_entry.get(), edit_process, edit_processes_window)).grid(column=0, row=4, sticky="w", padx=5, pady=10)

        # adding cancel button
        tk.Button(edit_process, text="cancel", 
                  font = "Courier 12", bg="gray", 
                  command=edit_process.destroy).grid(column=1, row=4, sticky="e", padx=5, pady=10)

    def delete_process_description(self, name, window):
        """
        Function to delete a process description

            name    - string        ... name of the process description
            window  - tk.Toplevel() ... handler to the process editing window
        """
        if messagebox.askokcancel("Are you sure?", "Do you really want to delete\n\"" + name + "\"?\nFiles with this process description\nwill be set to \"No Description\"."):
            # loop over md files and delete these process description
            for md in self.MD_files:
                if self.MD_files[md][self.keywords[0]] == self.processes[name]:
                    self.MD_files[md][self.keywords[0]] = ""
            # delete the process description
            self.processes.remove(name, self.processes[name])

            # save the process description dict
            save_processes(self.processes)

            # resume process editing
            window.destroy()
            self.create_edit_process_window()

    def create_edit_process_window(self):
        """
        Function that creates the editing window for process descriptions
        """
        def bind_edit_mousewheel(event):
            """
            Function to bind mouse wheel to scrolling when the mouse enters the process frame
            """
            # windows
            edit_processes.bind('<MouseWheel>', on_edit_mousewheel) 
            # linux
            edit_processes.bind('<Button-4>', on_edit_mousewheel)
            edit_processes.bind('<Button-5>', on_edit_mousewheel)


        def unbind_edit_mousewheel(event):
            """
            Function to unbind the mouse wheel if the mouse leaves the process frame
            """
            # windows
            edit_processes.unbind('<MouseWheel>') 
            # linux
            edit_processes.unbind('<Button-4>')
            edit_processes.unbind('<Button-5>')

        def on_edit_mousewheel(event):
            """
            Function which binds mouse wheel to scrolling the canvas
            """
            if event.num == 5 or event.delta < 0:
                v = 1
            if event.num == 4 or event.delta > 0:
                v = -1
            edit_canvas.yview_scroll(v, "units")

        
        # create a second window and force it to the top
        edit_processes = tk.Toplevel(self.master)
        edit_processes.grab_set()
        edit_processes.title("edit processes")

        tk.Label(edit_processes, text="<Right Click> delete, <Left Click> edit, [+] new", font="Courier 12").grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        # creating a scrollabel list of buttons
        # 1. the topframe
        edit_topframe = tk.Frame(edit_processes)

        # 2. set sticky to all 4 directions and the weight to >0 that the frame can be resized if the window dimensions change  
        edit_topframe.grid(column=0, row=1, sticky="nsew", padx = 10, pady = 10)
        edit_processes.rowconfigure(1, weight=1)

        # 3. create the canvas and the scrollbar in the top frame 
        edit_canvas = tk.Canvas(edit_topframe)
        edit_scrollbar = tk.Scrollbar(edit_topframe, orient="vertical", command=edit_canvas.yview)
        # 4. add the scrollbar to the canvas
        edit_canvas.configure(yscrollcommand=edit_scrollbar.set)

        # 5. create the frame for the widgets on the canvas
        edit_frame = tk.Frame(edit_canvas)
        
        # 6. grid the scrollbar and the canvas
        edit_scrollbar.grid(row=0,column=1, sticky="ns", pady=10)
        edit_canvas.grid(row=0, column=0, sticky="nsew", pady=10)
        # 7. set the weights for the canvas and scrollbar so that they are resizable
        edit_topframe.columnconfigure(0, weight=1)
        edit_topframe.rowconfigure(0, weight=1)

        # because of reasons we need to do this or else is the scrollbar not resizable
        # (maybe because its a toplevel window and not a master? i dont know...)
        edit_scrollbar.columnconfigure(0, weight=1)

        # 8. blit the widget frame onto the canvas
        edit_canvas.create_window((0,0),window=edit_frame, anchor="nw", tags=["edit"])
        
        # 9. bind a function to the widget frame that it stays in focus and cant be scrolled away
        edit_frame.bind("<Configure>", lambda x: self.edit_scroll_frame_focus(x, edit_canvas))
        # 10. bind a function to the canvas which updates the width of the widget frame if the window is resized 
        edit_canvas.bind("<Configure>", lambda x: self.on_edit_canvas_resize(x, edit_canvas))

        # bind the mousewheel to the scrolling when mouse is on top of the frame
        # https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
        edit_frame.bind('<Enter>', bind_edit_mousewheel)
        edit_frame.bind('<Leave>', unbind_edit_mousewheel)

        # setting the weigth of the entries to 1 so that they stretch if the window is resized
        edit_frame.columnconfigure(0, weight=1)

        process_buttons = []
        end = 0
        for i, name in enumerate(self.processes.get_process_names()):
            # create a lambda to get a new scope where our i is not overwritten
            #    see also https://stackoverflow.com/questions/14259072/tkinter-bind-function-with-variable-in-a-loop
            def create_edit_lambda(x, edit_processes):
                return lambda : self.edit_process(x, edit_processes)
            
            if name != "No Description":
                process_buttons.append(tk.Button(edit_frame, font = "Courier 11", text=name,
                                             bg = "gray", command=create_edit_lambda(name, edit_processes)))
                process_buttons[-1].grid(column=0, row=i, sticky="ew", padx=10, pady=2)

                def create_delete_lambda(x, edit_processes):
                    return lambda ev: self.delete_process_description(x, edit_processes)
                process_buttons[-1].bind('<Button-3>', create_delete_lambda(name, edit_processes))

            end = i 

        # + button
        process_buttons.append(tk.Button(edit_frame, font = "Courier 11", text="+",
                                         bg = "gray", command=lambda : self.edit_process("+", edit_processes)))
        process_buttons[-1].grid(column=0, row=end+1, sticky="ew", padx=10, pady=7)

        # exit behaviour
        edit_processes.protocol("WM_DELETE_WINDOW", lambda : self.exit_process_editing(edit_processes))

    def exit_process_editing(self, processes_window):
        """
        Function to handle the exit behaviour of the edit process window

            process_window  - tk.Toplevel() ... a handle to the editing window
        """
        processes_window.destroy()
        # backup opened description
        tmp = self.stringvar_list[0].get()
        # update the entry list
        self.create_entry_list()
        # overwrite new process description
        # this leads to an updated standard selection in the option menu
        self.stringvar_list[0].set(tmp)
        # get last selected
        self.on_tree_selection(None, from_window=True)


    def update_keyword(self, event, i, window):
        """
        function update the keyword

            i   - index     ... index of the keyword
        """
        # temp list to check if the keyword is a duplicate
        tmp = list(self.keywords)
        tmp.remove(tmp[i])
        if not self.stringvar_label_list[i].get() == "" and not self.stringvar_label_list[i].get() in tmp:
            window.destroy()

            # new keyword
            n_keyword = self.stringvar_label_list[i].get()

            # iterate over the md files and update the ith keyword
            for md in self.MD_files:
                # update keywords
                self.MD_files[md].update_keyword(i, n_keyword)
                # save md to disc
                self.MD_files[md].write()

            # update self.keywords
            self.keywords[i] = n_keyword
            save_keywords(self.keywords)
        

    def edit_keyword(self, event, i):
        """
        Function which opens a small window containing an entry to edit one keyword

            i   - index ... index of the keyword/label
        """
        # create a second window and force it to the top
        edit = tk.Toplevel(self.master)
        edit.attributes("-topmost", True)
        edit.wait_visibility()
        edit.grab_set()
        edit.resizable(0, 0)
        edit.title("edit keyword")

        # create the edit entry
        edit_entry = tk.Entry(edit, textvariable=self.stringvar_label_list[i], font = "Courier 12")
        edit_entry.grid(column=0, row=0, sticky="we", padx=10, pady=10)
        edit.rowconfigure(0, weight=1)

        # set the focus to the entry
        edit_entry.focus_set()
        edit_entry.icursor("end")

        # bind the return key to update
        edit_entry.bind('<Return>', lambda x: self.update_keyword(x, i, edit))

        # clicking the x should mirror the effect of hitting the return key
        edit.protocol("WM_DELETE_WINDOW", lambda : self.update_keyword(None, i, edit))              

    def reset_current_metadata(self):
        """
        Function to reset the currently opened file
        """
        # check if you really want to do this
        if messagebox.askyesno("Reset current file", "Do you really want to reset the currently opened metadata file?"):
            # loop over the stringvars and reset them
            for i,stringvar in enumerate(self.stringvar_list):
                if i == 0:
                    stringvar.set(self.processes[[""]])
                else:
                    stringvar.set("")
            # save the empty metadata
            self.save_current_metadata()

    def copy_last_opened(self, index=None):
        """
        copy metadata from last opened file

            index   - index     ... if given copys only keyword with index
        """
        # check if a last opened file exists
        if self.last_opened_file is None:
            return
        
        # check if an index is given
        if index is None:
            if messagebox.askyesno("Copy from last opened File", "Do you really want to copy all metadata from the last opened file?\n\nWarning:\nThis overwrites all currently input metadata!"):
                for i in range(len(self.last_opened_file)):
                    self.stringvar_list[i].set(self.last_opened_file[i])
        else:
            self.stringvar_list[index].set(self.last_opened_file[index])

        # save the copied metadata
        self.save_current_metadata()

    def copy_to_directory(self, subdirectories=False, workingdir=False):
        """
        Function to copy the current metadata to the whole directory

            subdirectories      - bool      ... should subdirectories be also overwritten
            workingdir          - bool      ... should all files in the working dir be overwritten
        """
        if workingdir:
            # ask if they really want to do this
            if messagebox.askyesno("Copy metadata to all other files", "Do you really want to copy the currently input metadata to all files?\n\nWarning:\nThis will overwrite metadata of the other files!"):
                for md_path in self.MD_files:
                    self.save_current_metadata(path=md_path)

        elif subdirectories:
            # ask if they really want to do this
            if messagebox.askyesno("Copy metadata to the directory and subdirectories", "Do you really want to copy the currently input metadata to all files in this directory and all its subdirectories?\n\nWarning:\nThis will overwrite metadata of the other files!"):
                # get all datafiles in this directory and its subdirectory
                # initialize data file list
                files_in_dir_and_subs = []

                # create directory walk
                w = os.walk(os.path.dirname(os.path.abspath(self.file_name.get())))
                # filling the list with all file paths
                for root, _, files in w:
                    # iterate over all files
                    for f in files:
                        # create the path
                        path = os.path.join(root, f)

                        # check if metadata is in the filename or directory above
                        if not "metadata" in f and not "metadata" in os.path.split(root)[1]:
                            files_in_dir_and_subs.append(os.path.normpath(path))

                # loop over the files and set the metadata
                for file_path in files_in_dir_and_subs:
                    self.save_current_metadata(path=file_path)

        else:
            # ask if they really want to do this
            if messagebox.askyesno("Copy metadata to directory", "Do you really want to copy the currently input metadata to the whole directory?\n\nWarning:\nThis will overwrite metadata of the other files in this directory!"):
                # create a list with all paths to files in the directory
                files_in_dir = [os.path.join(os.path.dirname(os.path.abspath(self.file_name.get())), f) \
                                for f in os.listdir(os.path.dirname(os.path.abspath(self.file_name.get()))) \
                                if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(self.file_name.get())), f))]

                # loop over the files and set the metadata
                for file_path in files_in_dir:
                    self.save_current_metadata(path=file_path)

    def create_entry_list(self):
        """
        Function to create a scrollable resizable list of tkinter widgets
        """
        # check if the list is already created
        if not self.topframe is None:
            # this means that we come from a window which updates the entry list
            # we therefore need to destroy the old list
            #self.topframe.grid_forget()
            self.topframe.destroy()

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
        self.scrollbar.grid(row=1,column=1, sticky="ns", pady=10)
        self.canvas.grid(row=1, column=0, sticky="nsew", pady=10)
        # 7. set the weights for the canvas and scrollbar so that they are resizable
        self.topframe.rowconfigure(1, weight=1)
        self.topframe.columnconfigure(0, weight=1)

        # 8. blit the widget frame onto the canvas
        self.canvas.create_window((0,0),window=self.entry_frame,anchor="nw", tags=["entries"])
        
        # 9. bind a function to the widget frame that it stays in focus and cant be scrolled away
        self.entry_frame.bind("<Configure>", self.frame_focus)
        # 10. bind a function to the canvas which updates the width of the widget frame if the window is resized 
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # bind the mousewheel to the scrolling when mouse is on top of the frame
        # https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar
        self.entry_frame.bind('<Enter>', self.bind_mousewheel)
        self.entry_frame.bind('<Leave>', self.unbind_mousewheel)


        # setting the weigth of the entries to 1 so that they stretch if the window is resized
        self.entry_frame.columnconfigure(1, weight=1)

        self.label_list = []
        self.stringvar_label_list = []
        self.entry_list = []
        self.stringvar_list = []

        # 11. finally add the planned widgets on the widget frame
        if not self.file_name is None:
            self.last_selection = self.file_name.get()
        self.file_name = tk.StringVar(self.master)
        self.entry_list_title = tk.Label(self.topframe, font = "Courier 18", textvariable=self.file_name)
        self.entry_list_title.grid(row=0, columnspan=2, sticky="nwe", pady=10, padx=10)

        for i,keyword in enumerate(self.keywords):
            self.stringvar_label_list.append(tk.StringVar(self.master, value=keyword))
            self.label_list.append(tk.Label(self.entry_frame, font = "Courier 12", textvariable=self.stringvar_label_list[-1]))
            self.label_list[-1].grid(row=i+1,column=0, sticky="w", pady=1, padx=4)

            #  create a lambda to get a new scope where our i is not overwritten
            def create_edit_keyword_lambda(j):
                return lambda event: self.edit_keyword(event, j)

            self.label_list[-1].bind('<Button-3>', create_edit_keyword_lambda(i))

            # the first element is the process description
            if i == 0:
                self.stringvar_list.append(tk.StringVar(self.master))
                self.entry_list.append(tk.OptionMenu(self.entry_frame, self.stringvar_list[0], command=lambda x: self.save_current_metadata(), *self.processes.get_process_names()))
                self.entry_list[-1].grid(row=i+1, column = 1, sticky="ew", pady=3)
            else:
                self.stringvar_list.append(tk.StringVar(self.master))
                self.entry_list.append(tk.Entry(self.entry_frame, font = "Courier 12", textvariable=self.stringvar_list[-1]))
                self.entry_list[-1].grid(row=i+1, column=1, sticky="ew", pady=1)
                
                # bind the on return function
                # 1. create a lambda to get a new scope where our i is not overwritten
                #    see also https://stackoverflow.com/questions/14259072/tkinter-bind-function-with-variable-in-a-loop
                def create_return_lambda(j):
                    return lambda event: self.on_return_button(event, j)
                
                # 2. bind the created lambda
                self.entry_list[-1].bind('<Return>', create_return_lambda(i))

                # doing the same for up and down arrow keys
                # down arrow key gets the same functionality as return
                # we can therefore reuse our functions
                self.entry_list[-1].bind('<Down>', create_return_lambda(i))

                # up arrow needs a similar functionality
                def create_up_lambda(j):
                    return lambda event: self.on_up_button(event, j)

                self.entry_list[-1].bind('<Up>', create_up_lambda(i))

                # bind focus out event to save the metadata 
                # this double saves in case of enter, up or down but is mainly if the mouse clicks on something different
                # this is mainly a safety measure to minimize data loss
                def create_focus_loss_lambda(j):
                    return lambda event: self.on_entry_focus_loss(event, j)

                self.entry_list[-1].bind('<FocusOut>', create_focus_loss_lambda(i))

                # bind ctrl + L to copy information from the last opened file
                def create_last_opened_lambda(j):
                    return lambda event: self.copy_last_opened(index=j)

                self.entry_list[-1].bind('<Control-l>', create_last_opened_lambda(i))

        # bind ctrl + s to the master window to save the metadata and loose focus of the current entry
        # this is only done now to make sure the entries already excist
        self.master.bind('<Control-s>', self.on_ctrl_s)


        ### Functionality buttons:
        self.button_frame = tk.Frame(self.topframe)
        self.button_frame.grid(column=2, row=1, padx=10, pady=10)

        self.edit_processes_button = tk.Button(self.button_frame, font = "Courier 11", text="<",
                                             bg = "gray70", command=self.copy_last_opened)
        self.edit_processes_button.grid(column=0, row=0, pady=5, sticky="new")


        self.edit_processes_button = tk.Button(self.button_frame, font = "Courier 11", text=">",
                                             bg = "gray70", command=self.copy_to_directory)
        self.edit_processes_button.grid(column=0, row=1, pady=5, sticky="new")


        self.edit_processes_button = tk.Button(self.button_frame, font = "Courier 11", text=">>",
                                             bg = "gray70", command=lambda : self.copy_to_directory(subdirectories=True))
        self.edit_processes_button.grid(column=0, row=2, pady=5, sticky="new")


        self.edit_processes_button = tk.Button(self.button_frame, font = "Courier 11", text=">>>",
                                             bg = "gray70", command=lambda : self.copy_to_directory(workingdir=True))
        self.edit_processes_button.grid(column=0, row=3, pady=(5,20), sticky="new")


        self.add_remove_keywords = tk.Button(self.button_frame, font = "Courier 11", text="add/remove\nKeywords",
                                             bg = "gray60", command=self.create_add_remove_window)
        self.add_remove_keywords.grid(column=0, row=4, pady=5, sticky="new")


        self.edit_processes_button = tk.Button(self.button_frame, font = "Courier 11", text="edit\nprocesses",
                                             bg = "gray60", command=self.create_edit_process_window)
        self.edit_processes_button.grid(column=0, row=5, pady=5, sticky="new")


        self.edit_processes_button = tk.Button(self.button_frame, font = "Courier 11", text="reset",
                                             bg = "gray40", command=self.reset_current_metadata)
        self.edit_processes_button.grid(column=0, row=6, pady=20, sticky="new")

    def on_closing(self):
        """
        Function which saves the open metadata and destroys the master window
        """
        # save the currently opened file
        self.save_current_metadata()

        if messagebox.askokcancel("Quit", "Do you want to quit?\nProgress will be saved."):
            # these both calls fix the issue with linux and not closing properly
            self.master.quit()
            self.master.destroy()
            save_keywords(self.keywords)

    def start_mainloop(self):
        """
        Function which starts the tkinter main loop
        and handles exit behaviour of the main loop
        """
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.mainloop()