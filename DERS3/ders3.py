from ursina import *
from ursina.shaders import basic_lighting_shader as bls

Entity.default_shader = bls

app = Ursina(borderless=False)

grounds = [] # zemindeki küpleri saklar / tutar
for i in range(20): # dış döngü
    for j in range(20): # iç
        ground = Entity(model='cube', position=(-10 + i, 0, 10 - j), texture='white_cube')
        grounds.append(ground)

nesne1 = Draggable(parent=scene, model='cannon', y=.67, plane_direction=(0, 1, 0), lock=(0, 1, 0),color=color.white)

nesne2 = Draggable(parent=scene, model='siegeCatapult', scale=2, y=1, plane_direction=(0, 1, 0), lock=(0, 1, 0),color=color.white)

nesne3 = Draggable(parent=scene, model='wallPillar', scale=2, y=1.5, plane_direction=(0, 1, 0), lock=(0, 1, 0),color=color.white)

Sky()

EditorCamera()

app.run()
