# Global interfaces
linesToPrint = []
commandQueue = []

# From gregtech backend
def printToConsole(text):
    linesToPrint.append(text)


# To gregtech backend
def appendScrollCommand(text):
    commandQueue.append(text)