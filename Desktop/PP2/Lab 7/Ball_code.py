import pygame

pygame.init()
screen = pygame.display.set_mode((1010, 510))
done = False
x = 25
y = 25

clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        if y > 25:
            y -= 10

    if pressed[pygame.K_s]:
        if y < 470:
            y += 10

    if pressed[pygame.K_a]:
        if x > 25:
            x -= 10

    if pressed[pygame.K_d]:
        if x < 970:
            x += 10

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
