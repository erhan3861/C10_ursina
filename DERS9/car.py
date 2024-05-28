from ursina import *
from ursina.shaders import basic_lighting_shader as bls

class Car(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent = scene, **kwargs)
        self.collider = "box"
        self.speed = 0
        self.direction = 1 # 1 forward -1 back

        # ön tekerlek
        self.tyre1 = Entity(model="car_tyre", position=Vec3(91.2364, 33.597, -127.75), parent=self)
        self.tyre2 = Entity(model="car_tyre", position=Vec3(-79.542, 33.6717, -127.79), parent=self, rotation_y=180)

        # arka tekerlekler
        self.tyre3 = Entity(model="car_tyre", position=Vec3(91.6467, 35.4102, 147.16), parent=self)
        self.tyre4 = Entity(model="car_tyre", position=Vec3(-79.542, 35.4102, 147.164), parent=self, rotation_y=180)
        self.tyre_list = [self.tyre1, self.tyre2, self.tyre3, self.tyre4]

    def input(self, key):
        if held_keys["up arrow"]:
            self.speed += 1
            if not gas_sound.playing: gas_sound.play()
        elif held_keys["down arrow"]:
            self.speed -= 3

        if self.speed > 300: self.speed = 300
        elif self.speed < 0: self.speed = 0

        if key == "d": self.direction = 1
        elif key == "r": self.direction = -1

    def update(self):
        self.position -= self.forward * self.speed * self.direction  
        if self.speed > 0:
            # tekerleklerin dönmesi
            for t in self.tyre_list:
                t.rotation_x += self.direction * 50

            # arabanın tekerleğe göre dönmesi
            self.rotation_y += self.tyre1.rotation_y / 30
            # arabanın düz gitmesi
            if -10 < self.tyre1.rotation_y < 10:
                self.rotation_y -= self.tyre1.rotation_y / 30

        # arabanın ön tekerinin sağa sola dönmesi
        self.tyre1.rotation_y += (held_keys["right arrow"]-held_keys["left arrow"]) * 3

        if self.tyre1.rotation_y > 30: self.tyre1.rotation_y = 30
        elif self.tyre1.rotation_y < -30: self.tyre1.rotation_y = -30

        self.tyre2.rotation_y += (held_keys["right arrow"] - held_keys["left arrow"]) * 3
    
        if self.tyre2.rotation_y > 210: self.tyre2.rotation_y = 210
        elif self.tyre2.rotation_y < 150: self.tyre2.rotation_y = 150

        # arabanın kendi kendine yavaşlaması
        if not held_keys["up arrow"]: self.speed -= 0.5
        if self.speed < 0: 
            self.speed = 0
            gas_sound.stop()

# ana bölüm
def update():
    cam.position = car.position + Vec3(0, 10, 40) # Kamerayı arabayı takip etmesi için güncelle
 
app = Ursina(borderless=False)

ground = Entity(model="plane", texture="asphalt", scale=5000, texture_scale=(100,100))

Sky(texture="sky_sunset")

car = Car(model="car", scale=0.05, position=Vec3(0.010477, 0, 0.0529), shader=bls) 

cam = EditorCamera(y = 10, z=40, rotation_y=180)

# ses nesnesi app = Ursina() kodundan sonra olmamalı
gas_sound = Audio('gas.wav', loop=True, autoplay=False)   

app.run()









            
                








