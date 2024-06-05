from ursina import *
from ursina.shaders import basic_lighting_shader as bls

app = Ursina(borderless=False)

track = Entity(model = "track_c10")

Sky(texture="sky_sunset")

EditorCamera()

app.run()