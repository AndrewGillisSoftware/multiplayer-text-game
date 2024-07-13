
from gameStructures import *
import pygame

aspectRatio = (16, 9)

imageRefs = {
    "evilComputer": "Main_Screen_with_Mirror_Test3.png"   # 16:9
}


def main():
    # Prepare Assets
    images = loadImages()
    #images["evilComputer"] = pygame.transform.scale(images["evilComputer"], (840, 1008))
    #images["evilComputer"] = pygame.transform.scale(images["evilComputer"], (2560, 1440))
    #font = pygame.font.Font(None, 24)

    # Initialize Pygame
    pygame.init()

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
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
    images = {}
    for ref in imageRefs:
        images[ref] = pygame.image.load(imageRefs[ref])
    return images

def createFrame(images):
    # Fill the screen with a color to wipe away anything from last frame
    frame = pygame.Surface((images["evilComputer"].get_width(), images["evilComputer"].get_height()))
    frame.fill("black")
    frame.blit(images["evilComputer"], (0, 0))

    # Quit button
    # quitButtonRect = pygame.Rect()
    return frame

# Call to main
main()
