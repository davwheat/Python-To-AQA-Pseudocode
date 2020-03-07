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
import io


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
                listOfLines[i] = line.replace(replaceSet[0], replaceSet[1])
            i += 1


def ReplaceInputOutput(listOfLines):
    # Replace print statements
    i = 0
    for line in listOfLines.copy():
        if "print" in line:
            listOfLines[i] = re.sub(r"(print).*\(", line, "OUTPUT ")

            startStr = line.find('(')
            endStr = line.rfind(')')
            printStr = line[startStr+1:endStr]

            listOfLines[i] += printStr
        i += 1

    # Replace input statements
    i = 0
    for line in listOfLines.copy():
        if "input" in line:
            # if line doesn't match input() -- (no print)
            if not re.search(r"input\s*\(\s*\)", line):
                startStr = line.find('(')
                endStr = line.rfind(')')
                printStr = line[startStr+1:endStr]
                listOfLines.insert(i, "OUTPUT " + printStr)

                # listOfLines[i] = re.sub(r"\s*(\s*\".*\"\s*)\s*", line, "")
                i += 1

            startInput = line.find('input(')
            endInput = line.rfind(')')
            listOfLines[i] = line[:startInput] + \
                "USERINPUT" + line[endInput+1:]
        i += 1

# No real clue how this works
# I just stole it from the O.G. repo


def ReplaceCodeBlocks(listOfLines, linesToAvoid=[]):
    """
        This function traces through the entire file tracing indentation to find where structures start and end.
        The protocol for the lists is as follows
        [WordSearchingFor, WordReplaceWith, EmptyList, EmptyList, AddANewLineAfter?]
        The 2 empty lists are used to store the location and line number of where the items are found, which is passed onto the replacing function
        A basic description of what is going on
            We define the list of lists, searchFor which holds the stuff we are going to look for.
            We then, using a for loop iterate through every line.
            Inside that loop we have a second for loop which iterates through all the objects in searchFor.
            Basically we are checking to see if any of the words are on the current line, 1 word at a time from searchFor.
            If we find a word and it isn't a line we are meant to be avoiding (maybe it has a multiline comment?) we move down
                We assign distance to how many characters in from the left the found word was, this will be the level in we are tracing with.
                The program then searches each line that follows to see if it can find any character to the left (or equal) to distance on its current line.
                # or ~~~ it ignores those lines.
                If it finds and first character is else,
                If it isn't any of those special characters that has been found first, we can assume this structure has finished as it has unindentected.
                    We write the line number and how far in the structure started to the 2 empty lists inside the sublist.
            Finally we return the searchFor list, hopefully with lots of line numbers and indentation distances.
    """
    svgfile = listOfLines.copy()

    searchFor = [["if", "ENDIF", [], [], False], ["def", "ENDSUBROUTINE", [], [], True], [
        "class", "ENDCLASS", [], [], True], ["while", "ENDWHILE", [], [], False], ["for", "ENDFOR", [], [], False]]

    for count in range(len(svgfile)):  # Iterate through each line in the text file
        for i in range(len(searchFor)):  # For each line in text file, iterate through clues
            currentClue = searchFor[i][0]
            # Check if the current line in the file has the required string
            found = svgfile[count].find(searchFor[i][0])

            if (not (found == -1)) and not (count in linesToAvoid):
                distance = found  # Distance is basically how many characters it is indented in
                lineDone = False
                for a in range(count+1, len(svgfile)):  # Iterate through rest of the lines
                    f = False

                    for x in range(0, distance + 1):
                        if distance == 0:
                            pass
                        try:
                            if not (svgfile[a][x] == " "):
                                if svgfile[a][distance:(distance+4)] == "else":
                                    f = False
                                elif (svgfile[a][distance:(distance+1)] == "#"):
                                    f = False
                                elif (svgfile[a][distance:(distance+3)] == "~~~"):
                                    f = False
                                else:
                                    f = True

                        except:
                            print("Error:")
                            print(svgfile[a])

                    if f:
                        if lineDone == False:
                            searchFor[i][2].append(a)
                            searchFor[i][3].append(distance)
                            lineDone = True
                        break

    # rebuild code

    svgfile2 = listOfLines = []
    toRemove = []

    for i in range(0, len(svgfile)):  # iterate through the text file
        # Iterate through each of the words to be replaced
        for count in range(0, len(searchFor)):
            if i in searchFor[count][2]:  # Checks if this line is being requested
                # If it is, lets iterate through and find the exact reference
                for x in range(0, len(searchFor[count][2])):
                    if searchFor[count][2][x] == i:  # Checks if it is the exact reference
                        workingWith = x
                        indented = ""
                        for z in range(0, searchFor[count][3][x]):
                            indented = indented + " "

                        svgfile2.append(indented + searchFor[count][1])
                        if searchFor[count][4]:
                            svgfile2.append("")
        if not (i in toRemove):
            svgfile2.append(svgfile[i])

    listOfLines = svgfile2
    return svgfile2


def AddThenToIfBlocks(listOfLines):
    i = 0
    for line in listOfLines.copy():
        if "IF" in line and " THEN" not in line and "ENDIF" not in line:
            colonIndex = line.rfind(":")
            listOfLines[i] = line[:colonIndex] + " THEN"
        i += 1


def SelectPythonFile():
    return input("Enter Python file path: ")


def SaveListToFile(listOfLines):
    print()
    print("Conversion complete!")
    print()
    savePath = input("Please enter a path and filename to save to: ")
    print()

    # lineEndings = "\r\n" if input(
    #     "Please choose line endings (Windows - 1/Linux - 2)") == "1" else "\n"

    # print("Chosen " + ("Windows" if lineEndings ==
    #                    "\r\n" else "Linux") + " line endings")
    # print()

    print("Saving...")
    print()

    with io.open(savePath, 'w', encoding='utf8') as saveFile:
        saveFile.write("\n".join(listOfLines))

    print("Done!")
    print()
    input("Press ENTER to return to menu")


def Start():
    # get path to python file
    filepath = SelectPythonFile()
    # read each line of file into list
    pyLines = ReadFileAsList(filepath)
    # remove lines only containing whitespace
    RemoveEmptyLines(pyLines)
    # remove lines with multi-line comments
    RemoveMultiLineComments(pyLines)
    # replace print/input with OUTPUT and USERINPUT
    ReplaceInputOutput(pyLines)

    # replace common operators
    Replace(pyLines, [["!=", "≠"], ["<=", "≤"], [
            ">=", "≥"], ["=", "←"], ["==", "="]])

    # these are not guaranteed to be accurate - the most common uses of each of these is assumed
    Replace(pyLines, [["int(", "STRING_TO_INT("], ["str(", "INT_TO_STRING("], [
            "random.randint(", "RANDOM_INT("], ["randint(", "RANDOM_INT("], ["len(", "LEN("]])

    # replace elif with ~~~ so that it isn't recognised as an if
    Replace(pyLines, [["elif", "~~~"]])

    pyLines = ReplaceCodeBlocks(pyLines)

    Replace(pyLines, [["def ", "SUBROUTINE "], ["self.", " "], ["return", "RETURN"], [
            "else:", "ELSE"], ["if ", "IF "], [" or ", " OR "], [" and ", " AND "], ["class ", "CLASS "]])

    Replace(pyLines, [["~~~", "ELSE IF"]])  # replaces replaced thingies

    # Replace : in if blocks with THEN
    AddThenToIfBlocks(pyLines)

    SaveListToFile(pyLines)


def main():
    while True:
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
                    Start()
                    input()
                elif option == 2:
                    print("This project was originally created by gbaman. Rewritten and refactored to fit new AQA Pseudocode standards.\n\nThe version of pseudocode supported is available in the repository's root folder: https://github.com/davwheat/Python-To-AQA-Pseudocode\n\nPlease note that not all actions are supported yet -- only the basics. Feel free to open an issue if a technique you use isn't supported yet!")
                elif option == 3:
                    exit()


main()
