from evilComputer import *

PRINT_DEBUG = False
PRINT_DEBUG_TO_COMPUTER = False

def print_debug(text):
    if PRINT_DEBUG:
        print(text)
        if PRINT_DEBUG_TO_COMPUTER:
            printToConsole(text)

def print_all(text):
    print(text)
    printToConsole(text)