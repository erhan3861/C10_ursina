from ursina import *
from ursina.shaders import basic_lighting_shader as bls

Entity.default_shader = bls

class Nesne(Draggable):
    instances = []
    def __init__(self, model="cube", position=Vec3(0)):
        super().__init__(parent=scene)
        self.model = model
        self.position = position
        self.plane_direction = (0, 1, 0) # 0 hareket edebildiği düzlem, 1 yani y ekseni kilitli 
        self.lock = (0, 1, 0) 
        self.color = color.white
        self.highlight_color = color.lime
        Nesne.instances.append(self)

def control():
    sayac = 0
    for e in scene.entities:
        if isinstance(e, Nesne):
            sayac += 1
            if sayac > 10:
                return True
    return False

# ana program
def input(key):
    if key == "c up":
        if control() : return
        cannon = Nesne(model="cannon", position = mouse.world_point)

# Oyun
app = Ursina(borderless=False)
       
ground = Entity(model="plane", scale=100, collider="box", texture="grass")

Sky()

EditorCamera()

app.run()



