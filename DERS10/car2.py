from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from customDraggable import CustomDraggable

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
    # cam.world_position = car.world_position + Vec3(0, 10, 0) # Kamerayı arabayı takip etmesi için güncelle
    # cam.world_rotation = car.world_rotation
    pass

def input(key):
    if held_keys["1"]:cam.y += 1
    elif held_keys["2"]:cam.y -= 1
    elif held_keys["4"]:cam.x += 1
    elif held_keys["5"]:cam.x -= 1
    elif held_keys["7"]:cam.z += 1
    elif held_keys["8"]:cam.z -= 1
    elif key == "p": print(cam.position)
    elif key == "z" : cam.position = Vec3(39, 88, -29) # direksiyon modu
    elif key == "x" : cam.position = Vec3(-10, 67, -217) # sürüş modu
    elif key == "c" : cam.position = Vec3(2, 174, 574) # arkadan görünüş
    elif held_keys["v"]: # önden görünüş
        cam.rotation_y = 0  
        cam.position = Vec3(2, 174, -900)
    elif key == "v up" : cam.rotation_y = 180 
    elif key == "m": # yandan görünüş
        cam.rotation_y = 90  
        cam.position = Vec3(-890, 133, 29)
    elif key == "m up" : cam.rotation_y = 180 
    elif key == "b": 
        cam.world_position =  Vec3(0, 10, 0)

app = Ursina(borderless=False)

ground = Entity(model="plane", texture="asphalt", scale=5000, texture_scale=(100,100), collider="box")

Sky(texture="sky_sunset")

car = Car(model="car", scale=0.05, position=Vec3(0.010477, 0, 0.0529), shader=bls) 

cam = EditorCamera(parent=car, y = 150, z=100, rotation_y = 180)

# ses nesnesi app = Ursina() kodundan sonra olmamalı
gas_sound = Audio('gas.wav', loop=True, autoplay=False) 

cBarrier1 = CustomDraggable(model="barrierYellow", position=Vec3(20,5,0))

barrier = Entity(model="barrieryellow1", x=-20, y=5, scale=20)

app.run()

# https://kenney.nl/assets/racing-kit
# https://sketchfab.com/3d-models/traffic-cones-e03b1d2dfdc0416bb8324d15573ea60c









            
                








