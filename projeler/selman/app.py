from ursina import *
from ursina.shaders import basic_lighting_shader as bls, colored_lights_shader as cls
from ursina.prefabs.first_person_controller import FirstPersonController as FPS 

Entity.default_shader = bls

app = Ursina(borderless=False)

ground = Entity(model="plane", scale = 250, texture="grass", color=color.lime, collider="box")

arena = Entity(model="medieval_fps", scale=4)

player = FPS()

# EditorCamera()

Sky()

app.run()