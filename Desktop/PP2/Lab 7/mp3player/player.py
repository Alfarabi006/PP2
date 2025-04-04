import pygame
import os

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False

path = 'C:/Users/Sauka/OneDrive/Рабочий стол/Lab 7/mp3player/musics'
musiclist = os.listdir(path)
order = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pygame.mixer.music.load(os.path.join(path, musiclist[order]))
                pygame.mixer.music.play()
            elif event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_RIGHT:
                order = (order + 1) % len(musiclist)
                pygame.mixer.music.load(os.path.join(path, musiclist[order]))
                pygame.mixer.music.play(1)
            elif event.key == pygame.K_LEFT:
                order = (order - 1) % len(musiclist)
                pygame.mixer.music.load(os.path.join(path, musiclist[order]))
                pygame.mixer.music.play(1)

    screen.fill((255, 255, 255))
    pygame.display.flip()

pygame.quit()


