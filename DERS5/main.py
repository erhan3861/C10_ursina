from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController

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

app = Ursina(borderless = False) # kenarsız False olsun

sky = CustomSky() 

ground = Entity(parent=scene, model="plane", scale=250, y=-20,  texture = "ground_txt", color = color.rgba(90,76,26,255), texture_scale=(50, 50), collider='box') # 

player = FirstPersonController()

rock = Draggable(parent=scene, model="rock_07_2k", x=10, y=-19, scale=10, plane_direction=(0,1,0), lock=(0,1,0), color=color.white)

# EditorCamera()

app.run()