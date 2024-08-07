from ursina import *
from ursina.shaders import basic_lighting_shader as bls, colored_lights_shader as cls

Entity.default_shader = bls

app = Ursina(borderless=False)

player = Entity(model="player_model")

EditorCamera()

Sky()

app.run()