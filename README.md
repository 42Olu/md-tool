# General Information
* if you have any questions or problems send me an e-mail
* this tools purpose is to manage metadata of all data files in a given working directory
* this includes managing a list of keywords and process descriptions
* the test_dir folder is a directory to test out the tool and see if it fits your needs
* if metadata already exists and you want to start using this tool i would suggest
  1. backup the existing metadata
  2. delete the metadata folders 
  3. copy the excisting metadata manually inside the tool
  * this insures that no metadata is lost and that the tool works properly
* it needs a python 3 installation to work

* for Linux use the following command to start it:
```
./md_tool.run
```

* for Windows use the following command or double click md_tool.bat
```
md_tool.bat
```
* it can also theoretically be run on all operating systems with:
```
python main.py
```
if python is the path to a python 3 exe.

* if you select a working directory without stored metadata it will initialize metadata files in seperate folders
```
test-dir/					test-dir/
├── t1						├── metadata
│   ├── t2					│   ├── test2 (copy)-txt-metadata.txt	
│   │   ├── t.csv				│   ├── test2-txt-metadata.txt
│   │   ├── test2.txt				│   ├── test (copy)-txt-metadata.txt
│   │   └── test.txt				│   └── test-txt-metadata.txt
│   ├── test2 (copy).txt			├── t1
│   └── test2.txt				│   ├── metadata
├── t2				  ⟶		│   │   ├── test2 (copy)-txt-metadata.txt
│   ├── t.csv					│   │   └── test2-txt-metadata.txt
│   ├── test2.txt				│   ├── t2
│   └── test.txt				│   │   ├── metadata
├── test2 (copy).txt				│   │   │   ├── t-csv-metadata.txt
├── test2.txt					│   │   │   ├── test2-txt-metadata.txt
├── test (copy).txt				│   │   │   └── test-txt-metadata.txt
└── test.txt					│   │   ├── t.csv
						│   │   ├── test2.txt
						│   │   └── test.txt
						│   ├── test2 (copy).txt
						│   └── test2.txt
						├── t2
						│   ├── metadata
						│   │   ├── t-csv-metadata.txt
						│   │   ├── test2-txt-metadata.txt
						│   │   └── test-txt-metadata.txt
						│   ├── t.csv
						│   ├── test2.txt
						│   └── test.txt
						├── test2 (copy).txt
						├── test2.txt
						├── test (copy).txt
						└── test.txt
```

* the metadata files follow a specific scheme:
```
path to data file: /path/to/the/data/file.ext

metadata keyword::  metadata information
...
```
* the separator between the keyword and the metadata is <pre>"::  "</pre> written out ColonColonSpaceSpace
  * this can be used to manually add metadata with a text editor

# Instructions
* after starting the tool it will warn you if no keywords.pkl or processes.pkl are found
  * the recovery will be started to create the missing files from existing metadata or create empty files

* If no warnung occured you will be able to select the working directory which includes your datafiles you want to add or edit the metadata of
  * it also works if you select a parent directory which holds your data directories

* The tool will warn you if unknown keywords or processes are found inside this directory
  * this can happen if other people with their own instances of the tool edited metadata for this directory and added processes or keywords
* you can import these unknown keywords or processes into your keywords.pkl or processes.pkl
  * **WARNING:** if you choose to not import these unknown keywords or processes they will be deleted from the metadata which could lead to the loss of wanted metadata

* You are now inside the main window of the tool
* on the left side you can see a file browser
* if you click on a file the metadata editor opens
* the editor consists of a list of keywords and entry boxes to fill in metadata information
  * if you press ctrl+l in one of these entries it will copy the information from the last file you opened
* the first keyword will always be some sort of process description
  * in this drop down list you can select the process which lead you to this data file
* right click on a keyword will let you change the name

* on the right side you can see function buttons:
  * [<] this will fill in all the metadata information from the last file you opened
  * [>] this will write the currently input metadata for all files in the directory of the current file
  * [>>] this will write the currently input metadata for all files in the directory of the current file and all its subdirectories
  * [>>>] this will write the currently input metadata for all files in your opened working directory
  * **WARNING:** these buttons can lead to already put in metadata being overwritten
* the next two buttons are there to let you add/remove keywords and to let you edit your list of processes
* the reset button empties the metadata of the currently opened file

# Warnings
* I tried my best to test this tool and eliminate bugs but my advice would be the following:
  * backup your metadata regularly in case something is lost or overwritten to eliminate the possibility to lose your metadata
* I tested the tool most extensively on ubuntu (the development platform)
* I also tested the tool on Windows
* in theory it should also run on mac os

# Known Issues
* on windows when scrolling over a scrollable canvas, for example the entry list, it sometimes throws an error but works flawless
  * this may be happening because the delta of the event is not exactly 120 or -120
  * because the main development platform was linux I am going to ignore this issue at the moment
* If you rename a data file you need to manually rename the metadata file accordingly if you want the metadata to load correctly
* imported process descriptions will be given place holder names with which they are displayed in your tool
  * you can rename them manually inside the process editing window
  * the metadata is the description and not the name -> not a problem
