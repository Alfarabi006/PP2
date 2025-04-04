import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    baseLayer = pygame.Surface((640, 480))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))

    isMouseDown = False
    prevX = -1
    prevY = -1
    currentX = -1
    currentY = -1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    isMouseDown = True
                    currentX =  event.pos[0]
                    currentY =  event.pos[1]    
                    prevX =  event.pos[0]
                    prevY =  event.pos[1]

            if event.type == pygame.MOUSEBUTTONUP:
                if isMouseDown:
                    isMouseDown = False
                    baseLayer.blit(screen, (0, 0))

            if event.type == pygame.MOUSEMOTION:
                if isMouseDown:
                    currentX =  event.pos[0]
                    currentY =  event.pos[1]

        if isMouseDown and prevX != -1 and prevY != -1 and currentX != -1 and currentY != -1:
            screen.blit(baseLayer, (0, 0))
            center_x, center_y = calculateCenter(prevX, prevY, currentX, currentY)
            radius = math.sqrt((currentX-prevX)**2 + (currentY-prevY)**2)
            pygame.draw.polygon(screen, (255, 255, 255), [(center_x, center_y - radius), (center_x - math.sqrt(3)/2 * radius, center_y + radius/2), (center_x + math.sqrt(3)/2 * radius, center_y + radius/2)], 1)

        pygame.display.flip()
        clock.tick(60)

def calculateCenter(x1, y1, x2, y2):
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y

main()
