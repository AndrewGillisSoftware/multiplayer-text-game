# randomNameGenerator.py
# Isaac Schroeder
# 11/29/22
# NOTE: This isn't just any random name generator, this is a name generator I created to name characters for games.
#   As a result, the name structures and name piece bank may have some wackiness to them.
# NOTE 2: My goal is to make the generation very generalized and modular, but as a result there is a possibility of
#   generating profane sounding names. This is not intentional, and some sort of filtering system is a future goal.


import csv
import random


def loadSymbolTableData(fileName):
    symbolTableData = {}
    try:
        symbolTableFile = open(fileName, "r")
        reader = csv.reader(symbolTableFile, delimiter=",")
        for row in reader:
            # symbol is a key to access its replacement options
            symbolTableData[row[1]] = parseSymbolRow(row[2:])
    except Exception as error:
        print("Error reading in the name symbol table: {}".format(error))
        symbolTableData = None
    finally:
        symbolTableFile.close()
        return symbolTableData


# Parses a row of symbol replacement options based on my defined format:
#   a = any letter.
#   any characters other than "()[]" outside parenthesis are fixed.
#   any letters or letter sequences inside brackets that are inside parenthesis can be selected to fill upon
#       replacement, and at least one letter or letter sequence must be chosen.
#   example: bla(bc[ch]dtz)ou(c[ck]s[st]t[th])
def parseSymbolRow(row):
    result = []
    for cell in range(len(row)):
        parsed_cell = []
        sequence = ""
        sublist = None
        depth = 0
        row[cell] = row[cell].lower()  # Send all letters in cell to lowercase!
        if len(row[cell]) != 0:  # Only process cell if not empty
            for char in range(len(row[cell])):
                if depth == 1:
                    if row[cell][char] == ")":
                        parsed_cell.append(sublist)
                        depth = 0
                        continue
                    elif row[cell][char] == "[":
                        depth = 2
                        continue
                    else:
                        sublist.append(row[cell][char])
                elif depth == 2:
                    if row[cell][char] == "]":
                        sublist.append(sequence)
                        sequence = ""
                        depth = 1
                        continue
                    else:
                        sequence += row[cell][char]
                elif row[cell][char] == "(":
                    if len(sequence) != 0:
                        parsed_cell.append(sequence)
                        sequence = ""
                    sublist = []
                    depth = 1
                    continue
                else:
                    sequence += row[cell][char]
            if len(sequence) != 0:
                parsed_cell.append(sequence)
            # print(parsed_cell)
            result.append(parsed_cell)
    # print(result)
    return result


def printSymbolTableData(symbolTableData):
    for symbol, replacements in symbolTableData.items():
        print("Symbol: {}".format(symbol))
        print("Replacement Options: {}".format(replacements))


# Returns a name based on the given string.
# If no string given, defaults to "@" which is replaced by pre-made builder templates.
def generateName(symbolTable, genString="@"):
    reference = genString
    while True:
        result = ""
        replacementOccurred = False  # for keeping track if a replacement has occured (stop looping if no replacement this loop)
        for char in reference:
            if char in symbolTable:  # if char is a key for the symbol table, then perform a replacement
                replacementOccurred = True
                cell = symbolTable[char][random.randrange(0, len(symbolTable[char]))]  # Select a random cell in the symbolTable row
                for item in cell:
                    if type(item) is str:
                        result += item
                    else:  # Otherwise it's a list of options to make a choice from
                        if random.random() < 0.5:  # There is a 50% chance of empty replacement for this level of choice
                            result += item[random.randrange(0, len(item))]
            else:
                result += char
        reference = result
        if not replacementOccurred:
            break
    return result


def obtainIntInput():
    while True:
        try:
            inp = int(input("How many names to generate? "))
        except ValueError:
            print("Invalid input, please enter a positive integer!")
        else:
            if inp > 0:
                return inp
            else:
                print("Invalid input, ensure your provided integer is greater than zero!")