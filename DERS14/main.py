from ursina import *
from ursina.shaders import basic_lighting_shader as bls
from ursina.prefabs.first_person_controller import FirstPersonController as FPS
from setup_scene import *
from car import *

Entity.default_shader = bls

def input(key):
    if held_keys["1"]: ground.x -= 0.1
    elif held_keys["2"]: ground.x += 0.1
    elif held_keys["3"]: camera.y -= 0.1
    elif held_keys["4"]: camera.y += 0.1
    elif held_keys["5"]: camera.z -= 0.1
    elif held_keys["6"]: camera.z += 0.1

    elif key == "c":
        for i in colliders :
            i.visible = not i.visible

    elif held_keys["tab"]:
        camera.rotation_y = 180
        camera.z = 5

    elif key == "tab up":
        camera.rotation_y = 0
        camera.z = -3

    elif key == "p":
        print(car.position)
        print([checkpoints[cp]["lap"] for cp in checkpoints])
        

def update():
    distance_xz(bot_car, checkpoints["cp6"]["pos"])
    if car.y <= -4.65 or held_keys["space"]:car.speed = 5 
    else: car.speed = 20
    check()

    txt_player.text = "PLAYER : " + str(car.lap)
    txt_computer.text = "COMPUTER : " + str(bot_car.lap)

def check():
    for cp in checkpoints:
        if distance_xz(car, checkpoints[cp]["pos"]) < 3 and car.speed > 5:
            checkpoints[cp]["lap"] = car.lap
    
    # botun puan alması
    if distance_xz(bot_car, checkpoints["cp6"]["pos"]) < 1:
        bot_car.lap += 1
        
    # tüm cp leri kontrol et ve lap sayısına eşit değilse geri dön
    for cp in checkpoints:
        if checkpoints[cp]["lap"] != car.lap: return
    else:
        # eğer lap sayısına eşitse lap sayısını artır ve lap değerlerini sıfırla
        car.lap += 1
        for cp in checkpoints: checkpoints[cp]["lap"] = 0 

checkpoints = {
    "cp1" : {"pos" : Vec3(21.7882, -4.30218, -137.483), "lap" : 0},
    "cp2" : {"pos" : Vec3(-29.489, 1.03619, -112.661), "lap" : 0},
    "cp3" : {"pos" : Vec3(-22.7099, 0.988298, -42.1838), "lap" : 0},
    "cp4" : {"pos" : Vec3(29.2164, 1.03619, -161.279), "lap" : 0},
    "cp5" : {"pos" : Vec3(21.2111, 0.988298, -232.15), "lap" : 0},
    "cp6" : {"pos" : Vec3(21.3983, -4.30218, -166.699), "lap" : 0},
}

app = Ursina(borderless=False)

# Sahneyi kur
setup_scene(json_file_path, custom_scale=200)

ground = Entity(model="plane", scale=500, x=-50, y=-5.2, z=-50, texture="grass", collider="box")

track = Entity(model="track", scale=200)

car = FPS(model="car", speed=20, origin_y=-.5, lap=0)
car.position = Vec3(21, -4.30, -200) # Vec3(21, -4.30, -147)

bot_car = Car(model="car")

Sky(texture="sky_sunset")

txt_player = Text("PLAYER : 0", position=(-0.8,0.45), scale=2)
txt_computer= Text("COMPUTER : 0", position=(0.4,0.45), scale=2)

camera.y = .5
camera.z = -4

# EditorCamera()

# Uygulamayı başlat
app.run()

