from ursina import *
import json

seciliBlok = 1 # tuğla 
kayitDosyasi = "kayitlar.json"

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

def kaydet():
    kayitlar = []
    # sahnedeki bütün varlıkları gez
    for e in scene.entities:
        if isinstance(e, Block):  # aradığımız varlık Block sınıfının bir örneği mi?
           kayitlar.append({'pos':tuple(e.position), "texture":str(e.texture)})
    with open("kayitlar/" + kayitDosyasi, "w") as file:
        json.dump(kayitlar, file)


def yukle(kayitDosyasi): 
    kayitlar = []
    # yeni bir sahne oluştur
    for e in scene.entities:
        if isinstance(e, Block):
            destroy(e, delay=0.1)

    with open("kayitlar/" + kayitDosyasi) as file:
        kayitlar = json.load(file)
        for kayit in kayitlar:
            if kayit["texture"] == "white_cube.png": continue
            Block(position = kayit["pos"], texture = kayit["texture"])




def buton_yukle():
    dosyaİsimleri = ["kayitSelman.json", "kayitHakan.json", "kayitCaglar.json", "kayitMustafa.json", "kayitAbdullah.json", "kayitİhsan.json"]

    for d in dosyaİsimleri:
        index = dosyaİsimleri.index(d)
        btn1 = Button(text=d[5:-5], position=(-.8 + index*0.3, .4), scale=.1, on_click = lambda x = d: yukle(x))
        btn1.fit_to_text()