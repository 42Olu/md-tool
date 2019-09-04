# General Information
* this tools purpose is to manage metadata of all data files in a given working directory
* if metadata already exists and you want to start using this tool i would suggest
  1. backup the existing metadata
  2. delete the metadata folders 
  3. copy the excisting metadata manually into the tool
  * this insures that no metadata is lost and the tool works properly
* this includes managing a list of keywords and process descriptions
* it needs a python 3 installation to work

* for Linux use the following command to start it:
```
./md_tool.run
```

* for Windows use the following command or double click md_tool.bat
```
md_tool.bat
```
* it can also be run on all operating systems with:
```
python3 main.py
```

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

metadata keyword::  
...
```
* the separator between the keyword and the metadata is <pre>"::  "</pre> written out ColonColonSpaceSpace
  * this can be used to manually add metadata with a text editor

# Instructions
* after starting the tool it will warn you if no keywords.pkl or processes.pkl is found
  * the recovery will be started to create the missing files from existing metadata or create empty files

* If no warnung occured you will be able to select the working directory which includes your datafiles you want to add or edit the metadata of
  * it also works if you select a parent directory which holds your data directories

* The tool will warn you if unknown keywords or processes are found inside this directory
  * this can happen if other people with their own instances of the tool edited metadata for this directory and added processes or keywords
* you can import these unknown keywords or processes into your keywords.pkl or processes.pkl
  ```diff
- WARNING:``` if you choose to not import these unknown keywords or processes they will be deleted from the metadata which could lead to the loss of wanted metadata



# Warnings
