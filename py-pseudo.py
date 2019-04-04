# Python-to-AQA-psudocode converter
# Concept by Andrew Mulholland aka gbaman
# Rewritten to fit new standards by David Wheatley (davwheat)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# import RegEx
import re
from time import sleep


def isInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def ReadFileAsList(filename):
    # Open given file name
    try:
        file = open(filename)
    except:
        # Exit on failed file load with explanation to user
        print()
        print("ERROR:")
        print(f"Couldn't load file '{filename}'")
        print("Exiting...")
        exit()

    lines = []

    for line in file.readlines():
        # Remove *nix or windows line endings depending on what the file uses
        if line[-2:] == "\r\n":
            line = line[:-2]
        elif line[-1:] == "\n":
            line = line[:-1]

        # Add line to array of lines
        lines += [line]

    return lines


def RemoveEmptyLines(listOfLines):
    # regex to match any full whitespace line
    whitespaceRegex = r"^\s*$"

    # counter
    i = 0

    # below uses a copy of the array to prevent odd line removal issues
    # for each line in the list...
    for line in listOfLines.copy():
        # if it matches the regex...
        if re.search(whitespaceRegex, line):
            # remove it from the list
            listOfLines.pop(i)
        else:
            # if not, move onto the next
            i += 1


def RemoveMultiLineComments(listOfLines):
    # search string
    linesToIgnore = []

    # counter
    i = 0

    # for each line in the list...
    for line in listOfLines:
        # if it contains a multiline string (""")
        if '"""' in line:
            # add its line number to the ignore list
            linesToIgnore += [i]

    RemoveLines(listOfLines, linesToIgnore)


def RemoveLines(listOfLines, linesToRemove):
    # for each item in linesToRemove...
    for i in linesToRemove:
        # remove it from the list
        listOfLines.pop(i)


def Replace(listOfLines, replaceSets):
    for replaceSet in replaceSets:
        i = 0
        for line in listOfLines:
            if replaceSet[0] in line:
                listOfLines[i].replace(replaceSet[0], replaceSet[1])
            i += 1


def ReplaceInputOutput(listOfLines):
    # Replace print statements
    i = 0
    for line in listOfLines.copy():
        if "print" in line:
            listOfLines[i] = re.sub(r"(print).*\(", line, "OUTPUT ")
            startStr = line.find('"')
            endStr = line.rfind('"')
            printStr = line[startStr:endStr+1]

            listOfLines[i] += printStr
        i += 1

    # Replace input statements
    i = 0
    for line in listOfLines.copy():
        if "input" in line:
            if '"' in line:
                startStr = line.find('"')
                endStr = line.rfind('"')
                printStr = line[startStr:endStr+1]
                listOfLines.insert(i, "OUTPUT " + printStr)

                listOfLines[i] = re.sub(r"\s*(\s*\".*\"\s*)\s*", line, "")
                i += 1

            listOfLines[i] = re.sub(r"(input)\s*\(\s*\)", line, "USERINPUT")
        i += 1


def SelectPythonFile():
    filepath = input("Enter Python file path: ")
    pyLines = ReadFileAsList(filepath)
    RemoveEmptyLines(pyLines)
    RemoveMultiLineComments(pyLines)
    ReplaceInputOutput(pyLines)
    Replace(pyLines, [["!=", "≠"], ["<=", "≤"], [">=", "≥"], ["=", "←"]])

    print(pyLines)


def main():
    option = ""

    while not isInt(option) or (int(option) not in [1, 2, 3]):
        print("           ============================          ")
        print("           | Python -> AQA Pseudocode |          ")
        print("           |        Converter         |          ")
        print("           ============================          ")
        print("                                                 ")
        print("           Concept by github.com/gbaman          ")
        print("  Rewritten & maintained by github.com/davwheat  ")
        sleep(1)
        print()
        print("1. Convert Python file to AQA Pseudocode")
        print("2. About")
        print()
        print("3. Exit")
        print()
        print()
        option = input("Choose an option: ")

        if isInt(option) and (int(option) in [1, 2, 3]):
            option = int(option)
            if option == 1:
                SelectPythonFile()


main()
