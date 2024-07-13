
import pygame


def gameFunction():
    # Ship Integrity
    initShipIntegrity = 100

    # Game Clock
    gameStepLength = 100  # in ms

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update screen content
        updateDisplay(screen)
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()


def updateDisplay(screen):
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

