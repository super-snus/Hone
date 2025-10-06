import hone
import time
import sys
import pygame
import random

hone.window.mode((0, 0), True)

hone.init()

point_id = 0
drag = 0.03
live_time = 0.1
Points = []

def create_point(position, velocity, massa):
    global point_id
    new_point = {
        "position": list(position),  # делаем список, чтобы можно было менять
        "massa": massa,
        "velocity": list(velocity),
        "live_time": live_time,
        "ID": point_id
    }
    Points.append(new_point)
    hone.obj.create("obj/Cube.obj", point_id)
    point_id += 1

create_point((0, 0, 2), (0, 0.02, 0), 0.5)
#hone.obj.create("obj/test.obj", "Voxel")
#hone.obj.position.z(10, "Voxel")


timelol = 0

while True:

    timelol += 1
    if timelol == 15:
        timelol = 0
        create_point((0, 0, 2), (random.uniform(-0.03, 0.03), random.uniform(-0.03, 0.03), random.uniform(-0.03, 0.03)), 0.1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pass

    for point in Points:
        #получаем и задаём новый live_time
        point["live_time"] = point["live_time"] - 0.001
        if point["live_time"] < 0:
            hone.obj.remove(point["ID"])
        
        #меняем размер в зависимости от live_time
        hone.obj.scale.x(point["live_time"], point["ID"])
        hone.obj.scale.y(point["live_time"], point["ID"])
        hone.obj.scale.z(point["live_time"], point["ID"])

        # Получаем текущие значения
        vx, vy, vz = point["velocity"]
        px, py, pz = point["position"]

        # Обновляем позицию
        new_px = px + vx
        new_py = py + vy
        new_pz = pz + vz

        new_vx = vx * (1 - drag)
        new_vy = vy * (1 - drag)
        new_vz = vz * (1 - drag)
        point["position"] = [new_px, new_py, new_pz]
        point["velocity"] = [new_vx, new_vy, new_vz]


        # Обновляем позицию объекта в сцене
        hone.obj.position.x(new_px, point["ID"])
        hone.obj.position.y(new_py, point["ID"])
        hone.obj.position.z(new_pz, point["ID"])

    hone.Render()
    #time.sleep(0.016)  # ~60 FPS
