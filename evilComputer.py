
from gameStructures import *
import pygame

aspectRatio = (16, 9)
# scaleFactor = (images["evilComputer"].surface.get_width(), images["evilComputer"].surface.get_height())

class ImageData:
    def __init__(self, surface, position):
        self.surface = surface
        self.position = position

    def getPositionedRect(self):
        return self.surface.get_rect(topleft=self.position)


imageRefs = {
    "evilComputer": "Main_Screen_Final.png",   # 16:9
    "quitButton"  : "quitButton.png",
    "cursor"      : "Quillnoink.png"
}


def main():
    # Initialize Pygame
    pygame.init()

    # Prepare Assets
    images = loadImages()
    #images["evilComputer"] = pygame.transform.scale(images["evilComputer"], (840, 1008))
    #images["evilComputer"] = pygame.transform.scale(images["evilComputer"], (2560, 1440))
    #font = pygame.font.Font(None, 24)

    # Screen Size:
    infoObject = pygame.display.Info()
    screenWidth = infoObject.current_w
    screenHeight = infoObject.current_h

    # Pygame related
    window = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)  # pygame.SCALED
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        # poll for events
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT or \
                (event.type == pygame.MOUSEBUTTONDOWN and images["quitButton"].getPositionedRect().collidepoint(event.pos)):
                running = False

        # Update screenSurface content and scale screenSufrace to resolution
        frame = pygame.transform.scale(createFrame(images), (screenWidth, screenHeight))
        # apply frame to window
        window.blit(frame, frame.get_rect())
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


def loadImages():
    imageSurfaces = {}
    imagePositions = {}
    for ref in imageRefs:
        imageSurfaces[ref] = pygame.image.load(imageRefs[ref])
        imagePositions[ref] = None
    # Specific image positions here
    imagePositions["evilComputer"] = (0, 0)
    imagePositions["quitButton"] = (imageSurfaces["evilComputer"].get_width() - imageSurfaces["quitButton"].get_width(), 0)
    imagePositions["cursor"] = None
    # Place into class
    images = {}
    for img in imageSurfaces:
        images[img] = ImageData(imageSurfaces[img], imagePositions[img])
    return images


def createFrame(images):
    # Evil computer image dictates frame size
    frame = pygame.Surface((images["evilComputer"].surface.get_width(), images["evilComputer"].surface.get_height()))
    frame.fill("black")
    # Blit fixed position images
    for img in images:
        if images[img].position is not None:
            frame.blit(images[img].surface, images[img].position)
    # Blit cursor
    return frame


# Call to main
main()
