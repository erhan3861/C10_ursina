from ursina import *

app = Ursina(borderless=False)

cube_ursina = Entity(model = "cube", color=color.red, scale=2, x = 2)

cube_blender = Entity(model = "cube_blender")

Sky()

EditorCamera()

app.run()
