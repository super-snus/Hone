# -*- coding: utf-8 -*-
import pygame
import numpy as np
import pygame.surfarray as surfarray

width, height = 1280, 720
pygame.init()
screen = pygame.display.set_mode((width, height))

# ������ ����� �����������
buffer = np.zeros((width, height, 3), dtype=np.uint8)

# ������ ������� ������������ ������
buffer[100:120, :] = [255, 0, 0]  # X �� 100 �� 120, ��� ������

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    surfarray.blit_array(screen, buffer)
    pygame.display.flip()

pygame.quit()
