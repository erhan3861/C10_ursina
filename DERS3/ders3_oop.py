from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from ursina.prefabs.first_person_controller import FirstPersonController
from editor_cam_handler import editor_cam_handler
from block import *

Entity.default_shader = bls

class Cannon(Draggable):
    instances = []
    def __init__(self, model="cannon", position =  Vec3(0)):
        super().__init__(parent = scene)
        self.model = model
        self.position = position
        self.y = .5
        self.plane_direction = (0, 1, 0)
        self.lock = (0, 1, 0) 
        self.color = color.white
        self.highlight_color = color.lime
        self.scale = 3
        self.clicked = False
        Cannon.instances.append(self)

    def input(self, key):
        if key == "y up" and held_keys["control"]:
            self.plane_direction = (0,0,1)
            self.lock = (0,0,1)
        elif key == "x up" and held_keys["control"]:
            self.plane_direction = (0,1,0)
            self.lock = (0,1,0)
        elif key == "r up" and self.clicked:
            self.rotation_y += 10
        elif key == "e up" and self.clicked:
            self.rotation_y -= 10
        super().input(key)
    
    def on_click(self):
        for e in Cannon.instances:
            e.clicked = False
        self.clicked = True



# Oyun Başlangıcı
game_start = False

# Zemin Küpleri
grounds = []

def input(key):
    if key == "c up":
        cannon = Cannon(position=Vec3(10,0.5,15)) # kale
    elif key == "g up" and held_keys["control"]: 
        cannon = Cannon(position=Vec3(10,0.5,15)) # gate
        cannon.model = "gate"
        cannon.scale = 5
    elif key == "s up" and held_keys["control"]: 
        cannon = Cannon(position=Vec3(20,10,15)) # gate
        cannon.model = "wallNarrowStairs"
        cannon.scale = 20
        cannon.y = 5
    elif key == "t up" and held_keys["control"]: 
        cannon = Cannon(position=mouse.world_point) # gate
        cannon.model = "siegeCatapult"
        cannon.scale = 5
        cannon.y = 2.5
        
    elif key == "tab":
        editor_camera.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = Vec3(18, 19.5, -12.5) #Vec3(15.5, 19, -23) # Vec3(18, 19.5, -12.5) -> Selman kale pos
        editor_camera.rotation = Vec3(33.0953, 0, 0)
    
    
    
    editor_cam_handler(key, editor_camera)
    
# Oyun
app = Ursina(borderless=False)

ground = Entity(model="plane", scale=80, collider="box", texture="grass")

player = FirstPersonController(z=-5)
# for i in range(15):
#     for j in range(15):
#         ground = Entity(model='cube', position=(i+5, 0, -j-5), texture='white_cube', collider="box")
#         grounds.append(ground.position)

cannon = Cannon(model="korsan")

Sky()

editor_camera = EditorCamera(enabled=False)

buton_yukle()

app.run()