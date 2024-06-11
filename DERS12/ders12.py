from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from ursina.prefabs.first_person_controller import FirstPersonController as FPS

Entity.default_shader = bls


def input(key):
    if key == "z":
        car.position = collisions.duz1.world_position
    if held_keys["tab"]:
        camera.rotation_y = 180
        camera.z = 5
    if key == "tab up":
        camera.rotation_y = 0
        camera.z = -3
    if key == "y":
        print_on_screen(car.world_y)
        print(car.position)
    
def update():

    if car.world_y < 0.7 or held_keys["space"]:car.speed = 5 
    else: car.speed = 20
    
app = Ursina(borderless=False)

car = FPS(model="car", speed=20, origin_y = -.5)
car.position = Vec3(33, 0.7, 0)

ground = Entity(model="plane", scale=600, texture="grass", collider="box")

track = Entity(model = "track", scale=300, y=8, z=200)

collisions = load_blender_scene(name="track_collision", reload=True)
collisions.parent = track

for e in collisions.children:
    if "duz" in e.name:
        e.color = color.red
    else:
        e.color = color.lime
    e.color = color.clear
    e.collider = "box"
    e.double_sided = True
    # e.y -= .005

collisions.zemin1.world_y = 0.7
    
Sky(texture="sky_sunset")

camera.z = -3


app.run()