from connector import *
from gameStructures import *
from client import *
import pygame
import random

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


fontRef = "Beyond_Wonderland.ttf"
imageRefs = {
    "evilComputer": "Main_Screen_Final.png",   # 16:9
    "quill"       : "Quillnoink.png",
    "evilGoblin"  : "evilGoblin.png",
    "pencilCup"   : "pencilCup.png",
    "dragon"      : "dragon.png",
    "crystalBall" : "Crystal_Ball.png",
    "candle"      : "Candle.png",
}
initImagePositions = {
    "evilComputer": (0, 0),
    "quill"       : (1272,805),
    "evilGoblin"  : (0,1050),
    "pencilCup"   : (550, 650),
    "dragon"      : (0, 160),
    "crystalBall" : (180, 775),
    "candle"      : (1550, 725),
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
    "dragon1": "Dragonrar.mp3",
    "dragon2": "Dragonrarr2.mp3",
}


def main():
    # Start Backend
    client_thread = threading.Thread(target=start_client, args=())
    client_thread.start()

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
    peterSoundNames = ["peter1", "peter2", "peter3", "peter4", "peter5", "peter6", "peter7", "peter8", "peter9"]
    dragonSoundNames = ["dragon1", "dragon2"]
    sounds = loadSounds(soundRefs, volume=1.0)
    scrollFont = pygame.font.Font(fontRef, 27)
    consoleFont = pygame.font.SysFont("Consolas", 18, bold=True)

    # Setup Cursor
    pygame.mouse.set_visible(True)

    # Pygame related
    window = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)  # pygame.SCALED
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Console Setup
    consoleLineCount = 23
    consoleLineLength = 45
    scrollEditString = ""
    scrollEditSurface = None
    consolePrintedLines = []
    for i in range(consoleLineCount):
        consolePrintedLines.append(None)

    # Typing Setup - values will be in milliseconds
    backspaceKeyHeld = False
    continuousBackspace = False
    backspaceKeyHeldStartTime = 0
    continuousBackspaceStartDelay = 100
    continuousBackspaceCooldown = 10
    continuousBackspaceLatestTime = 0

    # Game State
    quillHeld = False

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT event means the user clicked X to close your window
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                quitRequest = checkImageClick(images["evilGoblin"], event.pos)
                dragonClick = checkImageClick(images["dragon"], event.pos)
                zone = checkSelectionZones(selectionZones, event.pos)
                if quitRequest and not quillHeld:
                    running = False
                elif dragonClick:
                    sounds[dragonSoundNames[random.randrange(0, len(dragonSoundNames) - 1)]].play()
                elif zone == "inkwell":
                    if quillHeld:
                        quillHeld = False
                        images["quill"].setCursorAttachment(False)
                    else:
                        quillHeld = True
                        images["quill"].setCursorAttachment(True, (-25, -145))
                elif zone == "fishHead" and quillHeld:
                    sounds[peterSoundNames[random.randrange(0, len(peterSoundNames) - 1)]].play()
            elif event.type == pygame.KEYDOWN and quillHeld:
                if event.key == pygame.K_BACKSPACE:
                    backspaceKeyHeld = True
                    backspaceKeyHeldStartTime = pygame.time.get_ticks()
                    scrollEditString = scrollEditString[:-1]  # Remove last character on backspace
                elif event.key == pygame.K_RETURN:
                    appendScrollCommand(scrollEditString)
                    # printToConsole(scrollEditString)
                    scrollEditString = ""
                elif len(scrollEditString) <= consoleLineLength:
                    scrollEditString += event.unicode  # Add the pressed key to the string
                scrollEditSurface = scrollFont.render(scrollEditString, True, "black")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    backspaceKeyHeld = False
                    continuousBackspace = False

        # backspace goodener
        if backspaceKeyHeld:
            if not continuousBackspace and pygame.time.get_ticks() - backspaceKeyHeldStartTime > continuousBackspaceStartDelay:
                continuousBackspace = True
                continuousBackspaceLastTimestamp = pygame.time.get_ticks()
                scrollEditString = scrollEditString[:-1]  # Remove last character on backspace
                scrollEditSurface = scrollFont.render(scrollEditString, True, "black")
            elif continuousBackspace and pygame.time.get_ticks() - continuousBackspaceLatestTime > continuousBackspaceCooldown:
                continuousBackspaceLatestTime = pygame.time.get_ticks()
                scrollEditString = scrollEditString[:-1]  # Remove last character on backspace
                scrollEditSurface = scrollFont.render(scrollEditString, True, "black")

        # Look for new console outputs
        while len(linesToPrint) != 0:
            addConsolePrintedLine(consolePrintedLines, consoleFont, linesToPrint.pop(0))

        # Display update
        frame = createFrame(images, consolePrintedLines, scrollEditSurface, screenWidth, screenHeight)
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


def createFrame(images, consolePrintedLines, scrollTextSurface, screenWidth, screenHeight):
    # Evil computer image dictates frame size
    frame = pygame.Surface((images["evilComputer"].surface.get_width(), images["evilComputer"].surface.get_height()))
    frame.fill("black")
    # Blit non-cursor images
    for img in images:
        if not images[img].isAttachedToCursor() and images[img].position is not None:
            frame.blit(images[img].surface, images[img].position)
    # Blit console printed lines surface
    for i in range(len(consolePrintedLines)):
        if consolePrintedLines[i] is not None:
            frame.blit(consolePrintedLines[i], (670, 135 + i * 20))
    # Blit editable scroll string
    if scrollTextSurface is not None:
        frame.blit(scrollTextSurface, (725, 870))
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
    sounds = {}
    for sound in soundData:
        sounds[sound] = pygame.mixer.Sound(soundData[sound])
        sounds[sound].set_volume(volume)
    return sounds


def addConsolePrintedLine(consolePrintedLines, font, text):
    # Render new line
    line = font.render(text, True, "black")
    # Drop the oldest line
    consolePrintedLines.pop(0)
    # Append new line to list
    consolePrintedLines.append(line)
