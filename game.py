# -*- coding: utf-8 -*-

import hone
import time
import sys
import pygame
import math

ObjRotate = 0


hone.window.mode((1024, 768), False)

hone.init()

#hone.win.create("test game", 800, 600)
#hone.obj.create("obj/test2.obj", "Text")
hone.obj.create("obj/logolol.obj", "GordonFreeman")
hone.obj.position.z(1.5, "Text")
hone.obj.rotate.y(180, "GordonFreeman")

hone.obj.position.z(4, "GordonFreeman")
hone.obj.position.y(0, "GordonFreeman")
hone.obj.rotate.y(0, "GordonFreeman")


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
screen = hone.get_screen()

while True:

	clock.tick(999)
	fps = clock.get_fps()

	ObjRotate +=1
	#if ObjRotate > 360:
	#	ObjRotate = 0

	#hone.obj.rotate.y(ObjRotate, "Text")
	#hone.obj.rotate.x(45, "Text")
	#hone.obj.rotate.z(ObjRotate, "Text")

	#hone.obj.rotate.x(ObjRotate, "GordonFreeman")
	hone.obj.rotate.y(ObjRotate, "GordonFreeman")
	#hone.obj.rotate.z(ObjRotate, "GordonFreeman")
	#hone.obj.rotate.x(0, "GordonFreeman")

	rotatelol = 50
	ampletude = 4
	#hone.obj.position.x(math.sin(ObjRotate/(rotatelol)) * ampletude, "GordonFreeman")
	#hone.obj.position.y(math.sin(ObjRotate/(rotatelol- 25)), "GordonFreeman")
	#hone.obj.position.z(math.sin(ObjRotate/(rotatelol- 50)), "GordonFreeman")
	

	hone.Render()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				pass

	# ������ ������
	fps_text = font.render(f'FPS: {fps:.1f}', True, (255, 255, 255))
	text_rect = fps_text.get_rect(topleft=(10, 10))
	screen.blit(fps_text, text_rect)

	# �����: flip ��� ���
	pygame.display.update(text_rect)