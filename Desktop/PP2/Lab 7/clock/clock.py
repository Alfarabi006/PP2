import pygame
import os

pygame.init()
mickey = pygame.image.load(r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 7\clock\main-clock.png")
right_hand = pygame.image.load(r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 7\clock\righthand.PNG") 
left_hand = pygame.image.load(r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 7\clock\lefthand.PNG")  
screen = pygame.display.set_mode((840, 847))
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    current_time = pygame.time.get_ticks()
    seconds = (current_time // 1000) % 60
    minutes = (current_time // 60000) % 60

    right_hand_rect = right_hand.get_rect()
    right_hand_rect.center = (420, 423.5)
    right_hand_rect_angle = minutes * 6  
    rotated_right_hand = pygame.transform.rotate(right_hand, -right_hand_rect_angle)
    rotated_right_hand_rect = rotated_right_hand.get_rect(center = right_hand_rect.center)

    left_hand_rect = left_hand.get_rect()
    left_hand_rect.center = (420, 423.5)
    left_hand_rect_angle = seconds * 6
    true_left_hand = pygame.transform.rotate(left_hand, 58)
    rotated_left_hand = pygame.transform.rotate(true_left_hand, -left_hand_rect_angle)
    rotated_left_hand_rect = rotated_left_hand.get_rect(center = left_hand_rect.center)

    screen.fill((255, 255, 255))
    screen.blit(mickey, (5, 5))
    screen.blit(rotated_right_hand, rotated_right_hand_rect)
    screen.blit(rotated_left_hand, rotated_left_hand_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()