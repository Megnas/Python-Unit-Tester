# SIMPLE UNIT TESTER
Simple unit tester made in python for test driven developement

## Usage
```
python tester.py TESTED_SCRIPT FOLDER_WITH_TESTS [-h] [-i --interpret INTERPRET] [-f --format FORMAT] [-t --timeout TIMEOUT]
```

##### TESTED_SCRIPT
Script you wanted to be tested.

##### FOLDER_WITH_TESTS
Folder which contain tests for tester.
File in folder should be in this format:
- .src - files containing input
- .rc - files containing return code
- .out - files containing output (optional)

##### INTERPRET
If you are using an interpret to run you code you need to specify it here. For example if you are using pythonuse **-i python** or if you need specific verison of python, for example python3.10, use **-i python3.10**

##### FORMAT
If you use specific format of type of format, you need to specify it with **-f** flag.
Formats availible:
- plaintext - compares two strings (default)
- xml - Standard XML
- xml-utf8 - XML with UTF-8 encoding

##### TIMEOUT
Maximum amouth of time reserved for program to finish its task. It it can not complete its task in given, it is killed and marked as failure. Default time is 10s.
