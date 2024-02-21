# SIMPLE UNIT TESTER
Siple unit tester made in python for test driven developement

## Usage
```
python tester.py TESTED_SCRIPT FOLDER_WITH_TESTS [-h] [-i --interpret INTERPRET] [-f --format FORMAT] [-t --timeout TIMEOUT]
```

##### TESTED_SCRIPT
Script you wanted to be tested.

##### FOLDER_WITH_TESTS
Folder which contain tests for tester.
File in folder should be in this format:
```
1. .src - files containing input
2. .rc - files containing return code
3. .out - files containing output (optional)
```
