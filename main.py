import pygame

(width, height) = (800, 600)
BLUE = (0, 0, 255)


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    running = True
    while running:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(screen, BLUE, pos, 10)
                pygame.display.update()

            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
