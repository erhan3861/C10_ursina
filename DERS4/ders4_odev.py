from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from random import randint
import os

Entity.default_shader = bls

class Nesne(Draggable):
    instances =  []
    selected = []
    def __init__(self, model="cube", position=Vec3(0,0,0)):
        super().__init__(parent=scene)
        self.model = model
        self.position = position
        self.plane_direction = (0, 1, 0) # x ve z de sürüklenebilir
        self.lock = (0, 1, 0) # y eksenini kilitle
        self.color = color.white
        self.highlight_color = color.lime # üzerine geldiğimizdeki rengi
        self.scale = 2 # 2 kat büyüttük
        self.clicked = False
        self.selected = []
        Nesne.instances.append(self)

    def input(self, key):
        # sürüklemeyi sağ-sol yukarı-aşağıda yap
        if key == "y up":
            self.plane_direction = (0, 0, 1) # x ve y de sürüklenebilir
            self.lock = (1, 0, 1) # y eksenini kilitle
        elif key == "x up":
            self.plane_direction = (0, 1, 0) # x ve z de sürüklenebilir
            self.lock = (0, 1, 0) # y eksenini kilitle
        elif key == "r up" and self.clicked:
            self.rotation_y += 10
            for e in Nesne.selected:
                e.rotation_y += 10
        
        super().input(key) # miras aldığım sınıfında inputu kullan

    def on_click(self):
        # tüm nesnelerin clicked özelliğini False yap
        for e in Nesne.instances:
            e.clicked = False
        # sonra kendimizin clicked özelliğini True yap
        self.clicked = True
        # çoklu seçim için left shfift kullan
        if held_keys["left shift"]:
            self.color = color.blue
            Nesne.selected.append(self)
        else:
            for e in Nesne.selected:
                e.color = color.white
            Nesne.selected.clear()


    # ödev : shift tuşuna basılınca birden çok nesne seçilsin ve bunlar döndürülsün
    # held_keys["left shift"] 
        
# ana bölüm
app = Ursina(borderless = False) 

ground = Entity(model = "plane", scale=100, collider="box", texture="grass")

# nesne1 = Nesne(model="GLB format\siege-catapult.glb")
# nesne2 = Nesne(model="GLB format\siege-ballista.glb", position = Vec3(20,0,0))

model_yolu = "GLB format"
for i in os.listdir(model_yolu):
    pos = randint(-20,20), 0, randint(-20,20) # x ,y, z
    Nesne(model=f"{model_yolu}/{i}", position=pos)

    
Sky()
EditorCamera()
app.run()

