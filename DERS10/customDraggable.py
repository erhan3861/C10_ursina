from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from random import randint

class CustomDraggable(Draggable):
    instances =  []
    def __init__(self, model="cube", position=Vec3(0,0,0)):
        super().__init__(parent=scene)
        self.model = model
        self.position = position
        self.plane_direction = (0, 1, 0) # x ve z de sürüklenebilir
        self.lock = (0, 1, 0) # y eksenini kilitle
        self.color = color.white
        self.highlight_color = color.lime # üzerine geldiğimizdeki rengi
        self.scale = 20 # 20 kat büyüttük
        self.clicked = False
        self.selected = []
        CustomDraggable.instances.append(self)
        self.shader = bls

    def input(self, key):
        # sürüklemeyi sağ-sol yukarı-aşağıda yap
        if key == "y up":
            self.plane_direction = (0, 0, 1) # x ve y de sürüklenebilir
            self.lock = (1, 0, 1) # y eksenini kilitle
        elif key == "t up":
            self.plane_direction = (0, 1, 0) # x ve z de sürüklenebilir
            self.lock = (0, 1, 0) # y eksenini kilitle
        elif key == "e up" and self.clicked:
            self.rotation_y += 10
        
        super().input(key) # miras aldığım sınıfında inputu kullan

    def on_click(self):
        # tüm nesnelerin clicked özelliğini False yap
        for e in CustomDraggable.instances:
            e.clicked = False
        # sonra kendimizin clicked öz True yap
        self.clicked = True