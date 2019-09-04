# General Information
* this tools purpose is to manage metadata of all data files in a given working directory
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
* the separator between the keyword and the metadata is <pre>"::  "</pre> = ColonColonSpaceSpace

# Instructions

# Warnings
