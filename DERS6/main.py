from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint
# from ursina.shaders import basic_lighting_shader as bls

# Entity.default_shader = bls

class CustomSky(Entity): # Entity sınıfından miras alıyoruz
    def __init__(self): # setup, kendisi otomatik çalışıyor
        super().__init__(
            parent = scene, # ebevyn -> 3D sahne
            model = "sphere", # küre
            texture = "farm.hdr", # kaplama, doku
            double_sided = True, # çift taraflı yap
            scale = 300 # büyüklük
        )

    # def update(self):
    #     self.rotation_y += 10 * time.dt

class Platform(Button):
    def __init__(self, position=Vec3(0)):
        super().__init__(
            parent = scene, # scene -> 3 boyutlu camera.ui -> 2 boyutlu
            model = "rock_07_2k",
            collider = "box", # çarpışma olayını belirtiyoruz
            position = position,
            color = color.white, 
            scale = 10
        )
        # nesnenin kodları, hareket edebilir özelliği
        self.moveable = random.randint(0, 1) # 0 -> False 1 -> True

    # overwrite
    def update(self):
        if round(distance(player, self)) < 10:
            self.on_click = Func(player.animate_position, self.position, duration=3, curve=curve.out_circ)
        # buraya hareketli platform yazılacak
        if self.moveable == 1: # hareketli
            self.color = color.lime
            if self.y < -13:
                self.y += 1 * time.dt
            elif self.y >= -13:
                 self.y = -15

    def on_mouse_enter(self): # enter -> giriş
        print_on_screen(round(distance(player, self)), scale=3)

    # 1. ödevimiz hareketli platformla beraber hareket etmek


app = Ursina(borderless = False) # kenarsız False olsun

sky = CustomSky() 

ground = Entity(parent=scene, model="plane", scale=250, y=-20,  texture = "ground_txt", color = color.rgba(90,76,26,255), texture_scale=(50, 50), collider='box') # 

player = FirstPersonController()

rock = Draggable(parent=scene, model="rock_07_2k", x=10, y=-19, scale=10, plane_direction=(0,1,0), lock=(0,1,0), color=color.white)

# EditorCamera()

# ders6 kodları
p1 = Platform(position = (5, -18, 5)) # x,y,z
p2 = Platform(position=(10, -15,15)) 
p3 = Platform(position=(15, -15, -5)) 
p4 = Platform(position=(9, -15, 25)) 
p5 = Platform(position=(11, -15, 35)) 

bat = Entity(model="Bat", position=(5, -15, 35), scale=5) 


app.run()