# -*- coding: utf-8 -*-

from math import tan, cos, sin, radians
import math
#import cupy as cp
import os
import sys
import time
import random

sys.stdout = open(os.devnull, 'w')
import pygame
sys.stdout = sys.__stdout__

#import taichi as ti

#ti.init(arch=ti.gpu)  # Использовать GPU, если есть (иначе CPU)

pygame.init()

objects = []
#vertex = []
FOV = 90
H = 480
W = 640
init = False


#H = 780
#W = 1080

CharH = 1
CharW = 1
A = H / W
ZNEAR = 0.5
#ZFAR = 100
display = [[" " for _ in range(W)] for _ in range(H)]
z_buffer = [[float('inf') for _ in range(W)] for _ in range(H)]

cameraRotate_X, cameraRotate_Y, cameraRotate_Z = 0, 0, 0
cameraPos_X, cameraPos_Y, cameraPos_Z = 0, 0, 0

screen_info = pygame.display.Info()

screen = pygame.display.set_mode((W, H))

#лого
def init():
    global init

    image = pygame.image.load('logo.png')


    #image = pygame.transform.scale(image, (W // 4, H // 4))
    image_rect = image.get_rect(center=(W // 2, H // 2))

    # Центрирование по экрану
    image_rect.center = screen.get_rect().center

    init = True
    screen.fill((0, 0, 0))  # Очистка экрана
    screen.blit(image, image_rect)  # Рисуем изображение
    pygame.display.flip()  # Обновляем экран
    time.sleep(3)



# матрицы
def RotateXmatrix(point, angle):
    x, y, z = point
    angle = radians(angle)

    matrix = [
        [1, 0, 0, 0],
        [0, cos(angle), -sin(angle), 0],
        [0, sin(angle), cos(angle), 0],
        [0, 0, 0, 1]
    ]

    return MatrixMultiply(matrix, (x, y, z))

def RotateYmatrix(point, angle):
    x, y, z = point
    angle = radians(angle)

    matrix = [
        [cos(angle), 0, sin(angle), 0],
        [0, 1, 0, 0],
        [-sin(angle), 0, cos(angle), 0],
        [0, 0, 0, 1]
    ]

    return MatrixMultiply(matrix, (x, y, z))

def RotateZmatrix(point, angle):
    x, y, z = point
    angle = radians(angle)

    matrix = [
        [cos(angle), -sin(angle), 0, 0],
        [sin(angle), cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    return MatrixMultiply(matrix, (x, y, z))

def MatrixMultiply(matrix, vector):
    x, y, z = vector
    x_new = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + matrix[0][3]
    y_new = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + matrix[1][3]
    z_new = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + matrix[2][3]
    w = matrix[3][0] * x + matrix[3][1] * y + matrix[3][2] * z + matrix[3][3]

    # Однородные координаты: делим на w (чтобы перспектива работала)
    if w != 0:
        x_new /= w
        y_new /= w
        z_new /= w

    return x_new, y_new, z_new



class window:
    @staticmethod
    def name(name):
        pygame.display.set_caption(name)
    
    @staticmethod
    def mode(size, fullscreen):
        global H, W
        H, W = size
        if fullscreen:
            #H, W = size
            
            if H == 0 and W == 0:
                W = screen_info.current_w
                H = screen_info.current_h
            A = H / W
            display = [[" " for _ in range(W)] for _ in range(H)]
            z_buffer = [[float('inf') for _ in range(W)] for _ in range(H)]



            screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(size)



# класс для управления камерой
class camera:
    # класс вращения
    class rotate:
        @staticmethod
        def x(x_rotate):
            global cameraRotate_X
            cameraRotate_X = x_rotate

        @staticmethod
        def y(y_rotate):
            global cameraRotate_Y
            cameraRotate_Y = y_rotate

        @staticmethod
        def z(z_rotate):
            global cameraRotate_Z
            cameraRotate_Z = z_rotate
    class position:
        def x(x_pos):
            global cameraPos_X
            cameraPos_X = x_pos
        def y(y_pos):
            global cameraPos_Y
            cameraPos_Y = y_pos
        def z(z_pos):
            global cameraPos_Z
            cameraPos_Z = z_pos


# класс для работы с объектами
class obj:
    # класс вращения
    class rotate:
        @staticmethod
        def x(X_rotate, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Rotate"]
                    obj["Rotate"] = [X_rotate, Y, Z]

        @staticmethod
        def y(Y_rotate, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Rotate"]
                    obj["Rotate"] = [X, Y_rotate, Z]

        @staticmethod
        def z(Z_rotate, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Rotate"]
                    obj["Rotate"] = [X, Y, Z_rotate]

    # класс позиции
    class position:
        @staticmethod
        def x(X_pos, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Position"]
                    obj["Position"] = [X_pos, Y, Z]

        @staticmethod
        def y(Y_pos, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Position"]
                    obj["Position"] = [X, Y_pos, Z]

        @staticmethod
        def z(Z_pos, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Position"]
                    obj["Position"] = [X, Y, Z_pos]
    
    class scale:
        @staticmethod
        def x(X_scale, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Scale"]
                    obj["Scale"] = [X_scale, Y, Z]

        @staticmethod
        def y(Y_scale, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Scale"]
                    obj["Scale"] = [X, Y_scale, Z]

        @staticmethod
        def z(Z_scale, object_id):
            global objects
            for obj in objects:
                if obj["ID"] == object_id:
                    X, Y, Z = obj["Scale"]
                    obj["Scale"] = [X, Y, Z_scale]

    # функция создания объекта
    @staticmethod
    def create(patch, ID):
        mtl_flag = False
        current_mtl = ""
        current_mtl_file = ""
        with open(patch, 'r') as file:
            lines = file.readlines()

        new_object = {
            "ID": ID,
            "Vertices": [],
            "Faces": [],
            "Colors": [],
            "Rotate": [0, 0, 0],
            "Position": [0, 0, 0],
            "Scale": [1, 1, 1]
        }
        objects.append(new_object)

        for line in lines:
            tokens = line.strip().split()
            if tokens[0] == "v":
                AddVertexOnObj(float(tokens[1]), float(tokens[2]), float(tokens[3]), ID)
            elif tokens[0] == "mtllib":
                current_mtl_file = tokens[1]
                mtl_flag = True
            elif tokens[0] == "usemtl":
                current_mtl = tokens[1]
            elif tokens[0] == "f":
                if mtl_flag:
                    color = parse_mtl(os.path.join(os.path.dirname(patch), current_mtl_file), current_mtl) # (?, ?, ?)
                else:
                    color = (1, 1, 1)
                print(color)
                AddFaceOnObj(int(tokens[1]), int(tokens[2]), int(tokens[3]), ID, lines, color)
            else: 
                pass
        #print('lol end')

    def remove(ID):
        for index, item in enumerate(objects):
            if item["ID"] == ID:
                del objects[index]
                break  # Удаляем только первый найденный

def parse_mtl(current_mtl_file, current_mtl):
    Kd_flag = False
    with open(current_mtl_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
        #print(lines)
    for line in lines:
        tokens = line.strip().split()
        if tokens[0] == "newmtl":
            if tokens[1] == current_mtl:
                Kd_flag = True
        elif tokens[0] == "Kd" and Kd_flag:
            color = tokens[1], tokens[2], tokens[3]
            return color
        else:
            pass

def AddVertexOnObj(X, Y, Z, object_id):
    for obj in objects:
        if obj["ID"] == object_id:
            obj["Vertices"].append([X, Y, Z])

def AddFaceOnObj(v1, v2, v3, object_id, lines, color = (255, 255, 255)):
    for obj in objects:
        if obj["ID"] == object_id:
            obj["Faces"].append([int(v1) - 1, int(v2) - 1, int(v3) - 1])
            obj["Colors"].append(color)
            #print(f"Faces count: {len(obj["Faces"])} | Colors count: {len(obj["Colors"])}")

# алгоритм художника
def DrawTriangle(v1, v2, v3, v3d1, v3d2, v3d3, color = (1, 1, 1)):
    global cameraPos_X, cameraPos_Y, cameraPos_Z
    d1 = v3d1
    d2 = v3d2
    d3 = v3d3

    cam_position = [cameraPos_X, cameraPos_Y, cameraPos_Z]
    U = [d3[i] - d1[i] for i in range(3)] 
    V = [d2[i] - d1[i] for i in range(3)]
    N = [
        U[1] * V[2] - U[2] * V[1],
        U[2] * V[0] - U[0] * V[2],
        U[0] * V[1] - U[1] * V[0]
    ]

    C = [(d1[i] + d2[i] + d3[i]) / 3 for i in range(3)]
    B = [C[i] - cam_position[i] for i in range(3)]

    def normalize(v):
        length = sum(i**2 for i in v) ** 0.35
        return [i / length for i in v] if length != 0 else [0, 0, 0]

    N = normalize(N)
    B = normalize(B)

    result = sum(N[i] * B[i] for i in range(3))

    z1, z2, z3 = v3d1[2], v3d2[2], v3d3[2]

    if result > 0:   
        normalized = min(1, result / 0.5)
        #Red, Blue, Green = color

        Red = int(float(color[0]) * 255)
        Green = int(float(color[1]) * 255)
        Blue = int(float(color[2]) * 255)

        Red = int(normalized * Red)
        Blue = int(normalized * Blue)
        Green = int(normalized * Green)

        pygame.draw.polygon(screen, (Red, Green, Blue), [v1, v2, v3])

# функция отображения треугольника 2d с Z буфером
def DrawTriangleZ(v1, v2, v3, v3d1, v3d2, v3d3):
    global z_buffer, H, W
    if v1[1] > v2[1]: v1, v2 = v2, v1; v3d1, v3d2 = v3d2, v3d1
    if v1[1] > v3[1]: v1, v3 = v3, v1; v3d1, v3d3 = v3d3, v3d1
    if v2[1] > v3[1]: v2, v3 = v3, v2; v3d2, v3d3 = v3d3, v3d2

    def Interpolate(y, v_start, v_end, d_start, d_end):
        if v_start[1] == v_end[1]:
            return v_start[0], d_start[2]
        t = (y - v_start[1]) / (v_end[1] - v_start[1])
        x = v_start[0] + t * (v_end[0] - v_start[0])
        z = d_start[2] + t * (d_end[2] - d_start[2])
        return int(x), z

    for y in range(v1[1], v3[1] + 1):
        if y < v2[1]:
            x1, z1 = Interpolate(y, v1, v2, v3d1, v3d2)
            x2, z2 = Interpolate(y, v1, v3, v3d1, v3d3)
        else:
            x1, z1 = Interpolate(y, v2, v3, v3d2, v3d3)
            x2, z2 = Interpolate(y, v1, v3, v3d1, v3d3)

        if x1 > x2:
            x1, x2 = x2, x1
            z1, z2 = z2, z1

        for x in range(x1, x2 + 1):
            t = (x - x1) / (x2 - x1) if x1 != x2 else 0
            z = z1 + t * (z2 - z1)
            DrawPoint(x, y, z, " ")

    DrawLine2D(v1, v2, v3d1[2], v3d2[2])
    DrawLine2D(v2, v3, v3d2[2], v3d3[2])
    DrawLine2D(v1, v3, v3d1[2], v3d3[2])

# функция вывода линии на экран
def DrawLine2D(start, end, z1, z2):
    x1, y1 = start
    x2, y2 = end
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    points = []
    z = z1
    dz = (z2 - z1) / max(dx, dy, 1)

    while True:
        points.append((x1, y1, z))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
        z += dz

    for X, Y, Z in points:
        DrawPoint(X, Y, Z)

# Функция вывода 2D точки на экран
def DrawPoint(X, Y, Z, sympol="#"):
    global W, H, display, z_buffer
    if 0 <= int(X) < W and 0 <= int(Y) < H:
        if Z < z_buffer[int(Y)][int(X)]:
            z_buffer[int(Y)][int(X)] = Z + 0.001
            display[int(Y)][int(X)] = sympol

# Функция рендера
def Render():
    global W, H, A, FOV, ZFAR, ZNEAR, vertex, display, z_buffer, cameraPos_X, cameraPos_Y, cameraPos_Z, cameraRotate_X, cameraRotate_Y, cameraRotate_Z, init

    #screen.fill((0, 0, 0))

    for obj in objects:
        vertices_2d = []

        for vertex in obj["Vertices"]:
            X, Y, Z = vertex

            #лол кек просто ps1 эфектик для дёргающихся моделек
            #X += random.uniform(-0.01, 0.01)
            #Y += random.uniform(-0.01, 0.01)
            #Z += random.uniform(-0.01, 0.01)

            # тут scale
            X *= obj["Scale"][0]
            Y *= obj["Scale"][1]
            Z *= obj["Scale"][2]

            # применяем параметр вращения
            X, Y, Z = RotateXmatrix((X, Y, Z), obj["Rotate"][0])
            X, Y, Z = RotateYmatrix((X, Y, Z), obj["Rotate"][1])
            X, Y, Z = RotateZmatrix((X, Y, Z), obj["Rotate"][2])

            # применяем параметр позиции
            X += obj["Position"][0]
            Y += obj["Position"][1]
            Z += obj["Position"][2]

            # ===== ЧЕРНАЯ ДЫРА (МИНИМАЛИСТИЧНАЯ ВЕРСИЯ) =====
            # black_hole_pos = [0, 0, 4]  # Позиция дыры (X, Y, Z)
            # effect_radius = 2.5         # Радиус влияния
            # event_horizon = 0.5  # Радиус, после которого вершина "исчезает"
            # max_pull = 0.75    # Макс. сила притяжения
            
            # # Вектор к центру дыры
            # dx = black_hole_pos[0] - X
            # dy = black_hole_pos[1] - Y
            # dz = black_hole_pos[2] - Z
            # dist_sq = dx*dx + dy*dy + dz*dz
            # dist = max(dist_sq**0.5, 0.0001)  # Защита от деления на 0
            
            # if dist < effect_radius:
            #     if dist <= event_horizon:
            #         # Вершина пересекла горизонт - фиксируем её у центра
            #         X = black_hole_pos[0]
            #         Y = black_hole_pos[1]
            #         Z = black_hole_pos[2] - 0.01
            #     else:
            #         # Нормализованный вектор (направление к дыре)
            #         nx = dx / dist
            #         ny = dy / dist
            #         nz = dz / dist
                  
            #         # Сила эффекта (0 на границе, 1 у горизонта)
            #         force = 1.0 - (dist - event_horizon) / (effect_radius - event_horizon)
            #         force = max(0.0, min(force, 1.0))  # Ограничиваем 0..1
                  
            #         # Притяжение (с ограничением)
            #         pull_force = force * max_pull
            #         X += nx * pull_force
            #         Y += ny * pull_force
            #         Z += nz * pull_force
                  
            #         # Дополнительно: лёгкое закручивание
            #         if force > 0.5:
            #             spin = (force - 0.5) * 2.0  # 0..1
            #             angle = spin * 3.14  # Пол-оборота при макс. силе
            #             # Вращаем X и Y вокруг дыры
            #             cos_a = math.cos(angle)
            #             sin_a = math.sin(angle)
            #             rel_x = X - black_hole_pos[0]
            #             rel_y = Y - black_hole_pos[1]
            #             X = black_hole_pos[0] + rel_x * cos_a - rel_y * sin_a
            #             Y = black_hole_pos[1] + rel_x * sin_a + rel_y * cos_a
            # =============================================

            #тут вращение камеры
            X, Y, Z = RotateXmatrix((X, Y, Z), cameraRotate_X)
            X, Y, Z = RotateYmatrix((X, Y, Z), cameraRotate_Y)
            X, Y, Z = RotateZmatrix((X, Y, Z), cameraRotate_Z)

            #тут позиция камеры

            Z = max(Z, 0.1)

            if Z == Z:
                display_X = round((X / Z) * (H / W) * (1 / tan(radians(FOV) / 2)) * W / 2 + W / 2)
                display_Y = round((-Y / Z) * (CharW / CharH) * (1 / tan(radians(FOV) / 2)) * H / 2 + H / 2)
                vertices_2d.append([display_X, display_Y, X, Y, Z])

        paired = list(zip(obj["Faces"], obj["Colors"]))
        paired.sort(
            key=lambda pair: sum(vertices_2d[pair[0][i]][4] for i in range(3)) / 3,
            reverse=True
        )
        obj["Faces"], obj["Colors"] = zip(*paired)

        #for face in obj["Faces"]:
        for face, color in zip(obj["Faces"], obj["Colors"]):
            v1 = vertices_2d[face[0]][:2]
            v2 = vertices_2d[face[1]][:2]
            v3 = vertices_2d[face[2]][:2]

            v3d1 = vertices_2d[face[0]][2:5]
            v3d2 = vertices_2d[face[1]][2:5]
            v3d3 = vertices_2d[face[2]][2:5]


            if v3d1[2] < ZNEAR and v3d2[2] < ZNEAR and v3d3[2] < ZNEAR:
                continue
            DrawTriangle(v1, v2, v3, v3d1, v3d2, v3d3, color)
    if init == True:
        Draw()
    else:
        print("hone is not initialized")
        sys.exit(0)

def Draw():
    global display
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
        #    os.exit()
        #pass

    pygame.display.update()
    screen.fill((150, 150, 150))

def get_screen():
    return screen