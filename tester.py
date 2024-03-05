#!/usr/bin/python

from subprocess import Popen, PIPE, TimeoutExpired
from xml.dom import minidom
import argparse
import sys
import os

def readFile(filepath) -> str:
    #print("Opening file: {0}".format(filepath))
    if not os.path.isfile(filepath):
        return ""
    f = open(filepath, 'r')
    text = f.read()
    f.close()
    return text

def getTests(testsDirectory) -> list:
    testNames = []
    for fileName in os.listdir(testsDirectory):
        if fileName.endswith('.src'):
            file = os.path.splitext(fileName)[0]
            testNames.append(file)
    return testNames

def standartizeXML(xml : str) -> str:
    if xml == "":
        return ""
    xml = xml.replace('\r', '').replace('\n', '').replace('\t', '').replace("    ", '')
    parsedXML = minidom.parseString(xml)
    return parsedXML.toprettyxml()

def standartizeXML_UTF8(xml : str) -> str:
    if xml == "":
        return ""
    xml = xml.replace('\r', '').replace('\n', '').replace('\t', '').replace("    ", '')
    parsedXML = minidom.parseString(xml)
    return parsedXML.toprettyxml(encoding="UTF-8").decode("utf8")


def runTest(testDir, interpret, script, testName, timeOut, format) -> bool:
    print("Running test name: \033[35m{0}\033[0m".format(testName))
    
    inStr = readFile(testDir + testName + ".src")
    inData = inStr.encode()
    
    toRun = []
    if interpret == "":
        toRun = ["./{0}".format(script)]
    else:
        toRun = [interpret, script]

    proc = Popen(toRun, stdin=PIPE, stderr=PIPE, stdout=PIPE)
    
    outData : bytes
    errData : bytes

    try:
        outData, errData = proc.communicate(input=(inData), timeout=timeOut)
    except TimeoutExpired:
        print("Time out error")
        return False

    outStr = outData.decode("utf8")
    errStr = errData.decode("utf8")

    retCode = int(readFile(testDir + testName + ".rc"))
    if not retCode == proc.returncode:
        print("Program ended with different exit code than expected \033[36m{0}\033[0m (Expected: \033[36m{1}\033[0m)".format(proc.returncode, retCode))
        print("Source:\n\033[94m{0}\033[0m".format(inStr))
        print("Errors:\n\033[31m{0}\033[0m".format(errStr))
        print("\033[41mTEST FAILED\033[0m\n")
        return False
    
    correctOut = readFile(testDir + testName + ".out")
    
    if format == "xml":
        try:
            correctOut = standartizeXML(correctOut)
            outStr = standartizeXML(outStr)
        except Exception:
            print("Tester failed to parse XML")
            print("\033[41mTEST FAILED\033[0m\n")
            return False
    elif format == "xml-utf8":
        try:
            correctOut = standartizeXML_UTF8(correctOut)
            outStr = standartizeXML_UTF8(outStr)
        except Exception:
            print("Tester failed to parse XML")
            print("\033[41mTEST FAILED\033[0m\n")
            return False
    
    if not correctOut == outStr:
        print("Output of code differs:\n\033[94m{0}\033[0m\nCorrect code:\n\033[94m{1}\033[0m".format(outStr, correctOut))
        print("\033[41mTEST FAILED\033[0m\n")
        return False

    print("\033[42mTEST PASSED\033[0m\n")
    return True


parser = argparse.ArgumentParser(description="Simple tester for Test Driven Developement (TDD)")
parser.add_argument("program", type=str, help="Tested program that will be runned")
parser.add_argument("path", type=str, help="Path to folder with test files.")
parser.add_argument("-t", "--timeout", type=int, default=10, help="Maximum amouth of time for program to run. Default=10")
parser.add_argument("-i", "--interpret", type=str, default="", help="Interpreter that runs program. Deafult=Binary file")
parser.add_argument("-f", "--format", type=str, default="plaintext", help="Chose format of output: plaintext xml xml-utf8 (Default: plaintext)")

args = parser.parse_args()

program = args.program
testsDir = args.path
timeOut = args.timeout
interpret = args.interpret
format = args.format

if not (format == "plaintext" or format == "xml" or format == "xml-utf8"):
    sys.stderr.write("Invalid format type\n")
    exit(1)

tests = getTests(testsDir)

passed = 0
failed = 0

for test in tests:
    if runTest(testsDir, interpret, program, test, timeOut, format):
        passed += 1
    else:
        failed += 1

if failed == 0:
    print("All tests passed \033[42mSUCCESSFULLY\033[0m\n")
else:
    print("{0}/{1} tests passed".format(passed, passed + failed))
