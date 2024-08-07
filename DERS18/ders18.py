from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader, basic_lighting_shader as bls, colored_lights_shader as cls
import time
from ders17_model import GoalkeeperModel  # Modeli içe aktar
import numpy as np
from ursina.networking import *

Entity.default_shader = lit_with_shadows_shader

mode = "USER"
click_position = Vec3(0)
reaction_time = 0
user = "g"
start_time = 0
score_f = 0
score_g = 0

messages = [] # diğer oyuncudan gelen mesajlar
peer = Peer() # multiplayer mod için diğer oyuncu değişkenini ekledik

def on_connect(connection, time_connected):
    print("Connected to", connection.address)

def on_disconnect(connection, time_disconnected):
    print("Disconnected from", connection.address)

def on_data(connection, data, time_received): #MARK:on_data
    global click_position, reaction_time

    # print(data.decode("utf-8"))

    if user == "g": # g -> goalkeeper
        try:
            pos_list = data.decode("utf-8").split(",")
            ball.position = Vec3(float(pos_list[0]), float(pos_list[1]), float(pos_list[2]))
        except: pass
    
    elif "right" in data.decode("utf-8"):
        reaction_time = time.time() - start_time
        actor.play("right")
    
    elif "left" in data.decode("utf-8"):
        reaction_time = time.time() - start_time
        actor.play("left")
    
    elif "idle" in data.decode("utf-8"):
        reaction_time = time.time() - start_time
        actor.play("idle")
    else:
        message = Text(text="Received: {}".format(data.decode("utf-8")), origin=(0, 0), y=-0.05-len(messages)*0.05)
        messages.append(message)
        s = Sequence(1, Func(message.fade_out, duration=0.5), 0.5, Func(destroy, message), Func(messages.pop, 0))
        s.start()

    # gol haberi alınırsa
    if user == "g" and "gol" in data.decode("utf-8"):
        print_on_screen("GOOOOL", scale=5, position=(-.3, -.3))
        score_f = data.decode("utf-8").split(",")[1]
        text_f.text = str(score_f) 
        score_g = data.decode("utf-8").split(",")[2]
        text_g.text = str(score_g)

    # kaleciye kurtarış skoru eklemek
    if "score_g" in data.decode("utf-8"):
        score_g = data.decode("utf-8").split(",")[1]
        text_g.text = str(score_g)
 

peer.on_connect = on_connect
peer.on_disconnect = on_disconnect
peer.on_data = on_data


# Sky isimli bir sınıf oluşturuyoruz
class Sky(Entity):
    def __init__(self):  # sınıfımızın kurulumu yapılıyor
        super().__init__(  # bir üst sınıfımızın değişkenleri atanıyor
            parent=scene,
            model="sphere",  # küre
            texture="sunflower.hdr",
            double_sided=True,  # iki yönlü
            scale=1200,
            y=-50,
            rotation_y=90,
            unlit=True
        )

#MARK:input
def input(key):
    global mode, reaction_time, user, click_position

    if key in "bmu": gui_func(key[0])
    
    if key == "right arrow" and user != "f":
        reaction_time = time.time() - start_time
        actor.play("right")

        try:
            if mode == "MP": peer.send(peer.get_connections()[0], "right".encode("utf-8"))
        except: pass


    elif key == "left arrow" and user != "f":
        reaction_time = time.time() - start_time
        actor.play("left")

        try:
            if mode == "MP": peer.send(peer.get_connections()[0], "left".encode("utf-8"))
        except: pass

        
    elif key == "up arrow" and user != "f" :
        reaction_time = time.time() - start_time
        actor.play("idle")

        try:
            if mode == "MP": peer.send(peer.get_connections()[0], "idle".encode("utf-8"))
        except: pass

        
    elif key == "v up":
        body_collider.visible = not body_collider.visible
    
    elif key == "right mouse down":
        ball.rotation = Vec3(0)
        ball.position = Vec3(0, 2, -250)  # topun başlangıç konumu
    
    elif key == "p":
        print("pos=" , body_collider.world_position) #  sol -3, orta, 3 sağ
    
    elif key == "b up": # BOT
        mode = "AI"
        user = "ai"
        status_text.text = f"MODE = {mode}"
        model.train() # train the model with the current dataset
        model.save_model()
        model.load_model()
        ball.on_click = shoot
        bg.enabled = False

    elif key == "u up":
        mode = "USER"
        user = "user"
        status_text.text = f"MODE = {mode}"
        ball.on_click = shoot
        bg.enabled = False
        

    elif key == "m up": # multiplayer
        mode = "MP"
        status_text.text = f"MODE = {mode} HOST : H\n CLIENT : C"
        bg.enabled = False

    elif key == "space" and mode == "MP":
        if peer.is_running():
            x,y,z = mouse.world_point
            peer.send(peer.get_connections()[0], f"pos:{x},{y},{z}".encode("utf-8"))
    
    elif key == "h" and mode == "MP":
        status_text.text = "HOST"
        peer.start("25.43.224.124", 8080, is_host=True)
        user = "f" # footballer
        ball.on_click = shoot
        gui_func("m")
    
    elif key == "c" and mode == "MP":
        status_text.text = "CLIENT"
        peer.start("25.43.224.124", 8080, is_host=False)
        user = "g" # goalkeeper
        ball.on_click = ball_click_none_func
        gui_func("m")
    
def ball_click_none_func():
    "this function called when ball clicked in MP mode and goalkeeper user"
    return

#MARK:shoot
def shoot():
    global start_time, click_position
    start_time = time.time()  # Top fırlatıldığında başlangıç zamanını kaydedin
    ball.start = 1  # topun çıkışını haber veriyoruz

    if mouse.world_point:
        empty = Entity(position=mouse.world_point)
    else:
        empty = Entity()
    
    # MP mode futbolcu click_position bilgisini gönderir
    if mode == "MP" and user == "f":
        try:
            x,y,z = empty.position
            peer.send(peer.get_connections()[0], f"pos:{x},{y},{z}".encode("utf-8"))
        except:
            pass
    elif mode == "MP" and user == "g": # kaleci click_position bilgisini alır ve kullanır
        empty.position = click_position

    empty.look_at(ball)

    ball.rotation = empty.rotation

    click_position = empty.position

    ball.rotation_x -= 30

    if mode == "MP" and user == "f":
        try:
            x,y,z = empty.position
            peer.send(peer.get_connections()[0], f"pos:{x},{y},{z}".encode("utf-8"))
        except:
            pass


    ball.anim = ball.animate_position(ball.forward * 10, duration=2, curve=curve.linear)

    # topun animasyonu bitince zemine düşmesi / çıkması
    invoke(ball.animate_y, 2, 1, delay=2)  # belirli bir süre sonra tetikle 2 y=2 demek, 1 sn de demek

    # ball reposition after shooting Vec3(0, 2, -250) -> first position
    invoke(ball.animate_position, Vec3(0, 2, -250), 0, delay=5)
    invoke(ball.animate_rotation, Vec3(0), 0, delay=5)

    destroy(empty)

    # Modeli kullanarak tahmin yap MARK:predict
    if mode == "AI":
        reaction_time, direction = model.predict([click_position])
        print(reaction_time, direction)

        # Reaksiyon süresini ayarla, tahmin edilen yöne hamle yap
        invoke(goalkeeper_move, direction, delay=reaction_time)


def goalkeeper_move(direction):
    if direction == 2: 
        actor.play("right") # 2
    elif direction == 0:
        actor.play("left") # 0
    else:
        actor.play("idle") # 1

#MARK:update
def update(): 
    global score_f, score_g
    if mode == "MP":   
        peer.update()

        if not peer.is_running():
            status_text.text = f"MODE = {mode} \nfor HOST : PRESS H\n for CLIENT : PRESS C"
            return
        
        if peer.is_hosting():
            status_text.text = "MODE : MULTIPLAYER\nHosting on localhost, port 8080."
        else:
            status_text.text = "MODE : MULTIPLAYER\nConnected to host with address localhost, port 8080."

        # top konumu karşı bilgisayara gönderiliyor
        if peer.is_running() and user == "f":
            try:
                x,y,z = ball.world_position # tuple unpack
                peer.send(peer.get_connections()[0], f"{x},{y},{z}".encode("utf-8"))
            except: pass


    if actor.getCurrentAnim() == None:
        actor.loop("idle")

    if user == "g": return # MP modda kaleci topa müdahele etmemesi için geri dönüldü

    # kalecinin topu yakalaması
    if ball.intersects(body_collider).hit and ball.start:
        ball.start = 0
        
        # Başarılı hamle verilerini kaydet 0:left  1:idle 2:right
        if body_collider.world_x < -3.5: 
            direction = 0 # left
        elif body_collider.world_x > 3.5:
            direction = 2 # right
        else:
            direction = 1 # idle
        model.save_data(click_position, reaction_time, direction) # MARK:save_data

        angle = ball.intersects(body_collider).world_normal
        ball.look_at_2d(ball.position + angle, "y")
        ball.anim = ball.animate_position(ball.forward * 30, duration=3, curve=curve.out_circ)
        ball.direction = 3

        # kaleciye puan verilmesi
        score_g += 1
        text_g.text = str(score_g)
        try:
            peer.send(peer.get_connections()[0], f"score_g,{score_g}".encode("utf-8"))
        except:
            pass
        return

    # topun kalenin sağ,sol,yukarına çarpması
    hit_info = ball.intersects(ignore=[ground, front_wall, body_collider])
    if hit_info.hit:
        # print("hit")
        for seq in ball.anim:  # animasyonun tüm çerçevelerini bitir
            seq.kill()
        ball.position = hit_info.world_point

    # GOL olayı
    
    if ball.intersects(front_wall).hit:
        print_on_screen("GOOOOL", scale=5, position=(-.3, -.3))

        if ball.anim == None: return
        for seq in ball.anim:  # animasyonun tüm çerçevelerini bitir
            seq.kill()
        
        # kaleciye çarparsa veya topa dokunma olmadan gol olursa
        if ball.start in (0,1) :
            score_f += 1
            text_f.text = str(score_f)
        # kaleciye çarpıp gol olursa
        if ball.start == 0:
            score_g -= 1
            text_g.text = str(score_g)
        ball.start = -1

        try:
            peer.send(peer.get_connections()[0], f"gol,{score_f},{score_g}".encode("utf-8"))
        except:
            pass

    # zemine çarpma 
    if ball.y <= 1.5:
        for seq in ball.anim:  # animasyonun tüm çerçevelerini bitir
            seq.kill()

    # topun çarpma sonrası yuvarlanması
    elif ball.direction > 0:
        ball.rotation_x += 100 * ball.direction * time.dt
        ball.direction -= time.dt
        if ball.direction < 0: ball.direction = 0

def gui_func(key): #MARK:gui_func
    key_b_seq.kill()
    key_m_seq.kill()
    key_u_seq.kill()
    
    key_b.color,  key_m.color,  key_u.color = color.white, color.white, color.white
    key_m.x, key_u.x =  -0.65, -0.53

    if key == "b":
        key_b.color = color.lime
        ball_gui.enabled = True
        glove.enabled = False
        ball_gui.x = -0.77

    elif key == "m":
        key_m.color = color.lime
        if user == "f":
            ball_gui.enabled, glove.enabled = True, False
        elif user == "g":
            ball_gui.enabled, glove.enabled = False, True
       
        ball_gui.x = -0.65

    elif key == "u":
        key_u.color = color.lime
        ball_gui.enabled = glove.enabled = False

    text_f.enabled, text_g.enabled, shooter_gui.enabled, keeper_gui.enabled = True, True, True, True

app = Ursina(borderless=False)

# MARK:GUI entities ------------------------------------------------------------------------------
bg = Entity(model="quad", parent=camera.ui, texture="bg", scale=(1.8,1))

key_b = Entity(model="quad", parent=camera.ui, texture="key_b", scale=(0.1,0.1), position=(-.77,-.35))
key_b_seq = Sequence(Func(key_b.animate_scale, 0.11, .3), 1, Func(key_b.animate_scale, 0.1, .3),1, loop=True)
key_b_seq.start()

key_m = Entity(model="quad", parent=camera.ui, texture="key_m", scale=(0.1,0.1), position=(-.50,-.35))
key_m_seq = Sequence(Func(key_m.animate_scale, 0.11, .3), 1, Func(key_m.animate_scale, 0.1, .3),1, loop=True)
key_m_seq.start()

key_u = Entity(model="quad", parent=camera.ui, texture="key_u", scale=(0.1,0.1), position=(-.25,-.35))
key_u_seq = Sequence(Func(key_u.animate_scale, 0.11, .3), 1, Func(key_u.animate_scale, 0.1, .3),1, loop=True)
key_u_seq.start()

glove = Entity(model="quad", parent=camera.ui, texture="glove", scale=(0.07,0.07), position=(-.65,-.45), enabled=False)
ball_gui = Entity(model="quad", parent=camera.ui, texture="ball", scale=(0.07,0.07), position=(-.65,-.45), enabled=False)

start_text = "MODE : USER \nPRESS : B for BOT / M for Multiplayer / U for USER"
status_text = Text(text=start_text, origin=(0, 0), position=(0, .35))

shooter_gui = Entity(model="quad", parent=camera.ui, texture="f", scale=0.06, position=(-.85, .45), enabled=False)
keeper_gui = Entity(model="quad", parent=camera.ui, texture="g", scale=(0.06, 0.05), position=(-.87, .38), enabled=False)
text_f = Text("0", position=(-.81, .47), scale=2,  enabled=False)
text_g = Text("0", position=(-.81, .40), scale=2,  enabled=False)
# GUI end --------------------------------------------------------------------------------------

player = Entity(scale=20, shader=cls)

actor = Actor("assets/goalkeeper.glb")  # assets mutlaka yazılmalı
actor.reparentTo(player)  # animasyonları playere yükledik
# print(actor.getAnimNames())  # animasyonların isimlerini getir 
# print(actor.getJoints())  # animasyon eklemlerini getir

actor.loop('idle')

body = actor.exposeJoint(None, 'modelRoot', 'mixamorig5:Spine')  # mixamorig5 isminde 5 sayısı animasyona göre değişir
body_collider = Entity(model="cube", scale=(50, 100, 30), collider="box", visible=False)
body_collider.reparent_to(body)

# zemin
ground = Entity(model="plane", scale=1000, scale_x=2500, texture="field", z=-1066, rotation_y=90, collider="box")

# kale
soccer_goal = Entity(model="scene.gltf", x=57, z=15, scale=0.25, rotation_y=180, shader=bls, color=color.white)

# top
ball = Entity(model="ball", scale=4, y=2, z=-250, collider="sphere", shader=bls, start=0, anim=None, direction=0, hit=0)

# ödev
ball.on_click = shoot

# kale colliders
clr = color.clear
right_wall = Entity(model="right_wall", world_parent=soccer_goal, world_x=57, world_z=15, collider="box", double_sided=True, color=clr)
left_wall = Entity(model="left_wall", world_parent=soccer_goal, world_x=57, world_z=15, collider="box", double_sided=True, color=clr)
up_wall = Entity(model="up_wall", world_parent=soccer_goal, world_x=57, world_z=15, collider="box", double_sided=True, color=clr)

front_wall = Entity(model="cube", scale=(120, 45, 5), origin_y=-.5, world_position=Vec3(-5.6, 1.45, 5), collider="box", double_sided=True, color=clr)
back_wall = Entity(model="quad", scale=(125, 50), origin_y=-.5, world_position=Vec3(-5.6, 1.45, 35), collider="box", double_sided=True, color=clr)
front_wall.collider.visible = False

camera.y = 20
camera.z = -370

Sky()

# EditorCamera()

sun = DirectionalLight()
sun.look_at((1, -1, -3))

# Modeli yükle
model = GoalkeeperModel()

app.run()
