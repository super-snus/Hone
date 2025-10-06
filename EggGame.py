# -*- coding: utf-8 -*-

import hone
import time
import sys
import pygame

ObjRotate = 0
camera_rotate = (0, 0, 0)
camera_position = (0, 0, 0)

#pygame.event.set_grab(True)

hone.window.mode((0, 0), True)

hone.init()

#hone.win.create("test game", 800, 600)
hone.obj.create("obj/Monkey.obj", "Egg")
hone.obj.create("obj/Egg2.obj", "Egg2")
hone.obj.create("obj/Egg2.obj", "Egg3")
hone.obj.position.z(2, "Egg")
hone.obj.position.y(-2, "Egg2")
hone.obj.position.z(-2, "Egg3")


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
screen = hone.get_screen()
while True:
	clock.tick(600)
	fps = clock.get_fps()

	keys = pygame.key.get_pressed()
	dx, dy = pygame.mouse.get_rel()

	camera_rotate = (camera_rotate[0] - dy, camera_rotate[1] - dx, camera_rotate[2])

	if keys[pygame.K_u]:
		camera_rotate = (camera_rotate[0] + 1, camera_rotate[1], camera_rotate[2])
	if keys[pygame.K_j]:
		camera_rotate = (camera_rotate[0] - 1, camera_rotate[1], camera_rotate[2])
	if keys[pygame.K_h]:
		camera_rotate = (camera_rotate[0], camera_rotate[1] + 1, camera_rotate[2])
	if keys[pygame.K_k]:
		camera_rotate = (camera_rotate[0], camera_rotate[1] - 1, camera_rotate[2])


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		#if event.type == pygame.KEYDOWN:
		#	if event.key == pygame.K_w:
		#		camera_rotate = (camera_rotate[0], camera_rotate[1] + 1, camera_rotate[2])

	hone.camera.rotate.x(camera_rotate[0])
	hone.camera.rotate.y(camera_rotate[1])
	hone.camera.rotate.z(camera_rotate[2])
	print(camera_rotate)

	hone.Render()

	fps_text = font.render(f'FPS: {fps:.1f}', True, (255, 255, 255))
	text_rect = fps_text.get_rect(topleft=(10, 10))
	screen.blit(fps_text, text_rect)

	# ÂÀÆÍÎ: flip åù¸ ðàç
	pygame.display.update(text_rect)
	
	#print(screen == pygame.display.get_surface())
				