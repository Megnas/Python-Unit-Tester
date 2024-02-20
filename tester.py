from subprocess import Popen, PIPE, TimeoutExpired
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

def runTest(testDir,interpret, script, testName, timeOut):
    print("Running test name: \033[35m{0}\033[0m".format(testName))
    
    inStr = readFile(testDir + testName + ".src")
    inData = inStr.encode()
    
    toRun = []
    if interpret == "":
        toRun = ["./{0}".format(script)]
    else:
        roRun = [interpret, script]

    proc = Popen(toRun, stdin=PIPE, stderr=PIPE, stdout=PIPE)
    
    outData : bytes
    errData : bytes

    try:
        outData, errData = proc.communicate(input=(inData), timeout=timeOut)
    except TimeoutExpired:
        print("Time out error")
        return

    outStr = outData.decode("ascii")
    errStr = errData.decode("ascii")

    retCode = int(readFile(testDir + testName + ".rc"))
    if not retCode == proc.returncode:
        print("Program ended with different exit code than excepted \033[36m{0}\033[0m (Ecpected: \033[36m{1}\033[0m)".format(proc.returncode, retCode))
        print("Source:\n\033[94m{0}\033[0m".format(inStr))
        print("Errors:\n\033[31m{0}\033[0m".format(errStr))
        print("\033[41mTEST FAILED\033[0m\n")
        return
    
    correctOut = readFile(testDir + testName + ".out")
    if not correctOut == outStr:
        print("Output of code differs:\n\033[94m{0}\033[0m\nCorrect code:\n\033[94m{1}\033[0m".format(outStr, correctOut))
        print("\033[41mTEST FAILED\033[0m\n")
        return

    print("\033[42mTEST PASSED\033[0m\n")


parser = argparse.ArgumentParser(description="Simple tester for Test Driven Developement (TDD)")
parser.add_argument("program", type=str, help="Tested program that will be runned")
parser.add_argument("path", type=str, help="Path to folder with test files.")
parser.add_argument("--timeout", type=int, default=10, help="Maximum amouth of time for program to run. Default=10")
parser.add_argument("--interpret", type=str, default="", help="Interpreter that runs program. Deafult=Binary file")

args = parser.parse_args()

program = args.program
testsDir = args.path
timeOut = args.timeout
interpret = args.interpret

tests = getTests(testsDir)

for test in tests:
    runTest(testsDir,interpret, program, test, timeOut)
