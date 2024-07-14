
from gameStructures import *
import pygame
import random

aspectRatio = (16, 9)

class ImageData:
    def __init__(self, surface, position, scaleFactor):
        self.surface = surface
        self.initialPosition = position
        self.position = position
        self.scaleFactor = scaleFactor
        self.attachToCursor = False
        self.cursorAttachOffset = (0, 0)

    def isAttachedToCursor(self):
        return self.attachToCursor

    def setCursorAttachment(self, attached, offset=(0, 0)):
        self.attachToCursor = attached
        self.cursorAttachOffset = offset
        if not attached:
            self.position = self.initialPosition

    def positionAtCursor(self):
        self.position = (pygame.mouse.get_pos()[0] + self.cursorAttachOffset[0], pygame.mouse.get_pos()[1] + self.cursorAttachOffset[1])

    def getPositionedBounds(self):
        pos = (self.position[0] * self.scaleFactor, self.position[1] * self.scaleFactor)
        scaledSurface = pygame.transform.scale_by(self.surface, self.scaleFactor)
        return scaledSurface.get_rect(topleft=pos)


class SelectionZone:
    def __init__(self, left, top, width, height, scaleFactor):
        self.rect = pygame.Rect(left, top, width, height)
        self.scaleFactor = scaleFactor

    def getPositionedBounds(self):
        scaledRect = pygame.Rect.scale_by(self.rect, self.scaleFactor)
        scaledRect.left = self.rect.left * self.scaleFactor
        scaledRect.top = self.rect.top * self.scaleFactor
        return scaledRect


fontRef = "Kingthings_Trypewriter_2.ttf"
imageRefs = {
    "evilComputer": "Main_Screen_Final.png",   # 16:9
    "quill"       : "Quillnoink.png",
    "evilGoblin"  : "evilGoblin.png",
}
initImagePositions = {
    "evilComputer": (0, 0),
    "quill"       : (1272,805),
    "evilGoblin"  : (0,1050),
}
selectionZoneSetupData = {
    "inkwell" : (1262,950,62,53),
    "fishHead": (1695,300,55,50),
}
soundRefs = {
    "peter1" : "Petah/-101soundboards.mp3",
    "peter2" : "Petah/alright-then-lets-do-it-101soundboards.mp3",
    "peter3" : "Petah/boy-i-tell-you-that-really-grinds-my-gears-101soundboards.mp3",
    "peter4" : "Petah/holy-crap-i-am-freaking-out-101soundboards.mp3",
    "peter5" : "Petah/i-havent-felt-this-out-of-place-since-that-week-i-lived-with-superman-101soundboards.mp3",
    "peter6" : "Petah/jaja-101soundboards.mp3",
    "peter7" : "Petah/this-is-peter-griffin-101soundboards.mp3",
    "peter8" : "Petah/what-a-glorious-day-101soundboards.mp3",
    "peter9" : "Petah/when-im-when-im-in-a-restaurant-right.mp3",
}


def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()  # for sounds
    pygame.font.init()   # for font

    # Screen Size:
    infoObject = pygame.display.Info()
    screenWidth = infoObject.current_w
    screenHeight = infoObject.current_h

    # Prepare Assets
    scaleFactor, images = loadImages(imageRefs, initImagePositions, screenWidth)
    selectionZones = createSelectionZones(selectionZoneSetupData, scaleFactor)
    sounds = loadSounds(soundRefs, volume=0.5)
    #font = pygame.font.Font(fontRef)
    font = pygame.font.SysFont("Consolas", 18, bold=True)

    # Setup Cursor
    pygame.mouse.set_visible(True)

    # Pygame related
    window = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)  # pygame.SCALED
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Console Setup
    consoleLineCount = 23
    consolePrintedLines = []
    consoleActiveLine = None
    for i in range(consoleLineCount):
        consolePrintedLines.append(None)
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")
    addConsolePrintedLine(consolePrintedLines, font, "testessttestes")
    addConsolePrintedLine(consolePrintedLines, font, "asdfsdfesfasef")
    addConsolePrintedLine(consolePrintedLines, font, "testeasfaefsfeasf ssttestes")

    # Game State
    quillHeld = False

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT event means the user clicked X to close your window
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                quitRequest = checkImageClick(images["evilGoblin"], event.pos)
                zone = checkSelectionZones(selectionZones, event.pos)
                if quitRequest and not quillHeld:
                    running = False
                elif zone == "inkwell":
                    if quillHeld:
                        quillHeld = False
                        images["quill"].setCursorAttachment(False)
                    else:
                        quillHeld = True
                        images["quill"].setCursorAttachment(True, (-25, -145))
                elif zone == "fishHead" and quillHeld:
                    sounds[random.randrange(0, len(sounds) - 1)].play()

        # Display update
        frame = createFrame(images, consolePrintedLines, screenWidth, screenHeight)
        drawSelectionZones(False, frame, selectionZones)  # Needs to happen after scaling!
        window.blit(frame, frame.get_rect())  # apply frame to window
        pygame.display.flip()  # flip() the display to put your work on screen

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    # Exit game
    pygame.quit()


def loadImages(imgRefs, imgPositions, screenWidth):
    imageSurfaces = {}
    for ref in imgRefs:
        imageSurfaces[ref] = pygame.image.load(imgRefs[ref])
    # Determine scale factor
    scaleFactor = (screenWidth * 1.0) / imageSurfaces["evilComputer"].get_width()
    # Place into class
    images = {}
    for img in imageSurfaces:
        images[img] = ImageData(imageSurfaces[img], imgPositions[img], scaleFactor)
    return scaleFactor, images


def createFrame(images, consolePrintedLines, screenWidth, screenHeight):
    # Evil computer image dictates frame size
    frame = pygame.Surface((images["evilComputer"].surface.get_width(), images["evilComputer"].surface.get_height()))
    frame.fill("black")
    # Blit non-cursor images
    for img in images:
        if not images[img].isAttachedToCursor() and images[img].position is not None:
            frame.blit(images[img].surface, images[img].position)
    # Blit text surface
    for i in range(len(consolePrintedLines)):
        if consolePrintedLines[i] is not None:
            frame.blit(consolePrintedLines[i], (670, 135 + i * 20))
    # Scale frame
    scaledFrame = pygame.transform.scale(frame, (screenWidth, screenHeight))
    # Blit image(s) attached to cursor (need to be post scaling)
    for img in images:
        if images[img].isAttachedToCursor():
            images[img].positionAtCursor()
            scaledFrame.blit(images[img].surface, images[img].position)
    return scaledFrame


def createSelectionZones(selectZonesConfig, scaleFactor):
    selectionZones = {}
    for zone in selectZonesConfig:
        selectionZones[zone] = SelectionZone(selectZonesConfig[zone][0], selectZonesConfig[zone][1],
                                             selectZonesConfig[zone][2], selectZonesConfig[zone][3], scaleFactor)
    return selectionZones


# Will return first zone that click lands in bounds of, so be careful with overlaps!
def checkSelectionZones(selectionZones, mouseClickPos):
    for zone in selectionZones:
        if selectionZones[zone].getPositionedBounds().collidepoint(mouseClickPos):
            return zone
    return None


def checkImageClick(image, mouseClickPos):
    return image.getPositionedBounds().collidepoint(mouseClickPos)


def drawSelectionZones(debug, frame, selectionZones):
    if debug:
        for zone in selectionZones:
            pygame.draw.rect(frame, "purple", selectionZones[zone].getPositionedBounds())


def loadSounds(soundData, volume=1.0):
    sounds = []
    for sound in soundData:
        newSound = pygame.mixer.Sound(soundData[sound])
        newSound.set_volume(volume)
        sounds.append(newSound)
    return sounds


# Treat
def addConsolePrintedLine(consolePrintedLines, font, text):
    # Render new line
    line = font.render(text, True, "black")
    # Drop the oldest line
    consolePrintedLines.pop(0)
    # Append new line to list
    consolePrintedLines.append(line)


# Call to main
main()
