from ursina import *


def input(key):
    if held_keys["y"] and key == "+":
        e1.size_y += 0.1
        e1.collider = BoxCollider(e1, size=(e1.size_x, e1.size_y, e1.size_z))
        e1.collider.visible = True

    elif held_keys["y"] and key == "-":
        e1.size_y -= 0.1
        e1.collider = BoxCollider(e1, size=(e1.size_x, e1.size_y, e1.size_z))
        e1.collider.visible = True

    elif held_keys["x"] and key == "+":
        e1.size_x += 0.1
        e1.collider = BoxCollider(e1, size=(e1.size_x, e1.size_y, e1.size_z))
        e1.collider.visible = True

    elif held_keys["x"] and key == "-":
        e1.size_x -= 0.1
        e1.collider = BoxCollider(e1, size=(e1.size_x, e1.size_y, e1.size_z))
        e1.collider.visible = True

    elif held_keys["z"] and key == "+":
        e1.size_z += 0.1
        e1.collider = BoxCollider(e1, size=(e1.size_x, e1.size_y, e1.size_z))
        e1.collider.visible = True

    elif held_keys["z"] and key == "-":
        e1.size_z -= 0.1
        e1.collider = BoxCollider(e1, size=(e1.size_x, e1.size_y, e1.size_z))
        e1.collider.visible = True

    if key == "h":
        e1.collider.visible = not e1.collider.visible

    if key == "p":
        print("size = ",e1.collider.size)

    if key == "left mouse down":
        if mouse.world_point:   
            print(mouse.world_point)
                 

app = Ursina(borderless=False)

e1 = Entity(model="scarecrow1", size_x=1, size_y=1, size_z=1)
size = (0.5, 1.9, 1)
e1.collider = BoxCollider(e1,size = size)
e1.collider.visible = True

Sky(color=color.black)

EditorCamera()

app.run()