import pygame
import math

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

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    end = event.pos
                    if start is not None and end is not None:
                        triangle_points = calculateTrianglePoints(start, end)
                        pygame.draw.polygon(screen, (255, 255, 255), triangle_points, 1)
                        baseLayer.blit(screen, (0, 0))
                        start = None
                        end = None

        pygame.display.flip()
        clock.tick(60)

def calculateTrianglePoints(start, end):
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    hypotenuse = math.sqrt(width**2 + height**2)
    if x2 > x1:
        if y2 > y1:
            return [(x1, y1), (x1, y2), (x2, y2)]
        else:
            return [(x1, y1), (x2, y1), (x2, y2)]
    else:
        if y2 > y1:
            return [(x1, y1), (x2, y1), (x2, y2)]
        else:
            return [(x1, y1), (x1, y2), (x2, y2)]

main()
