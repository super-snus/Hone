# -*- coding: utf-8 -*-
import pygame
import numpy as np
import pygame.surfarray as surfarray

width, height = 1280, 720
pygame.init()
screen = pygame.display.set_mode((width, height))

# создаём буфер изображения
buffer = np.zeros((width, height, 3), dtype=np.uint8)

# рисуем красную вертикальную полосу
buffer[100:120, :] = [255, 0, 0]  # X от 100 до 120, вся высота

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    surfarray.blit_array(screen, buffer)
    pygame.display.flip()

pygame.quit()
