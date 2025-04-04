import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    prev1X = 0
    prev1Y = 0
    prev2X = 0
    prev2Y = 0

    screen.fill((0, 0, 0))

    isMouseDown1 = False
    isMouseDown2 = False
    line_thickness = 1 

    while True:
        pressed = pygame.key.get_pressed()

        current1X = prev1X
        current1Y = prev1Y
        current2X = prev2X
        current2Y = prev2Y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    isMouseDown1 = True
                if event.button == 3: 
                    isMouseDown2 = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    isMouseDown1 = False
                if event.button == 3:
                    isMouseDown2 = False

            if event.type == pygame.MOUSEMOTION:
        
                current1X = event.pos[0]
                current1Y = event.pos[1]
                current2X = event.pos[0]
                current2Y = event.pos[1]

            if event.type == pygame.MOUSEWHEEL:
                
                if event.y > 0: 
                    line_thickness += 1
                if event.y < 0:  
                    line_thickness = max(1, line_thickness - 1) 

        if isMouseDown1:
            pygame.draw.line(screen, (255, 255, 255), (prev1X, prev1Y), (current1X, current1Y), line_thickness)

        if isMouseDown2:
            pygame.draw.line(screen, (0, 0, 0), (prev2X, prev2Y), (current2X, current2Y), line_thickness)

        prev1X = current1X
        prev1Y = current1Y
        prev2X = current2X
        prev2Y = current2Y

        pygame.display.flip()
        clock.tick(60)

main()
