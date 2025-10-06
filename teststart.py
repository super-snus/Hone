import hone
import pygame
import sys
import math

hone.init()
hone.window.mode((0, 0), True)

screen = hone.get_screen()

ObjRotate = 0

hone.obj.create("obj/startlogo.obj", "logo")
hone.obj.position.z(4, "logo")
#hone.obj.rotate.y(0, "logo")
while True:
    ObjRotate +=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pass
    

    rotatelol = 50
    ampletude = 2
    hone.obj.position.z((math.sin(ObjRotate/(rotatelol)) * ampletude)+4, "logo")

    #hone.obj.scale.y((math.sin(ObjRotate/(rotatelol)) * ampletude)+4, "logo")
    
    hone.Render()