from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from ursina.prefabs.first_person_controller import FirstPersonController

Entity.default_shader = bls

seciliBlok = 1 # tuğla 

def update():
    global seciliBlok
    if held_keys["1"]: # 1 tuşuna basılırsa
        seciliBlok = 1 # tuğla bloğu olsun 
    elif held_keys["2"]: # 2 tuşuna basılırsa
        seciliBlok = 2 # tahta bloğu olsun 
    elif held_keys["3"]: seciliBlok = 3 # çimen bloğu olsun 


# blok sınıfı nesne yönelimli programlama
class Block(Button):
    def __init__(self, position=(0,0,0), texture="white_cube"):
        super().__init__(
            parent = scene, # 3 boyutlu uzayı 
            position = position,
            model = "cube",
            texture = texture,
            color = color.white,
            origin_y = .5,
            highlight_color = color.lime # hover
        )

    def input(self, key):
        if self.hovered: # üzerinde gezinmek
            if key == "left mouse down": # sol tıklama
                if seciliBlok == 1:
                    block = Block(position=self.position + mouse.normal, texture="brick")
                elif seciliBlok == 2:
                    block = Block(position=self.position + mouse.normal, texture="burnt_sand")
                elif seciliBlok == 3: block = Block(position=self.position + mouse.normal, texture="gras364")
                
                
                # 2.blok alıştırma -> ödev

            elif key == "right mouse down":
                destroy(self) # yok etmek

# ana program
app = Ursina(borderless = False)                

player = FirstPersonController()

for x in range(20):
    for z in range(20):
        block = Block(position = (x, 0, z))

Sky()

app.run()












