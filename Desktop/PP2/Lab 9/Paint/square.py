import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    baseLayer = pygame.Surface((640, 480))

    clock = pygame.time.Clock()

    start = None
    end = None

    screen.fill((0, 0, 0))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start = event.pos
                    end = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    end = event.pos
                    if start is not None and end is not None:
                        square_rect = calculateSquare(start, end)
                        pygame.draw.rect(screen, (255, 255, 255), square_rect, 1)
                        start = None
                        end = None

        pygame.display.flip()
        clock.tick(60)

def calculateSquare(start, end):
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    square_size = min(width, height)
    if x2 > x1:
        if y2 > y1:
            return pygame.Rect(x1, y1, square_size, square_size)
        else:
            return pygame.Rect(x1, y2, square_size, square_size)
    else:
        if y2 > y1:
            return pygame.Rect(x2, y1, square_size, square_size)
        else:
            return pygame.Rect(x2, y2, square_size, square_size)

main()
