import hone

#hone.obj.create("obj/egg.obj", "Player")

hone.init()

hone.window.mode((400, 400), False)

hone.obj.create("obj/Untitled.obj", "Ground")
hone.obj.position.x(-1, "Ground")
hone.obj.scale.x(40, "Ground")

while True:

    hone.Render()