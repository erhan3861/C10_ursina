from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader,basic_lighting_shader as bls
from ders17_model import *

Entity.default_shader = lit_with_shadows_shader

# ders17 değişkenleri
mode = "USER"
click_position = Vec3(0)
reaction_time = 0 # kalecinin hamle zamanı



# Sky isimli bir sınıf oluşturuyorz
class Sky(Entity):
    def __init__(self): # sınıfımızın kurulumu yapılıyor
        super().__init__( # bir üst sınıfımızın değişkenleri atanıyor
            parent = scene,
            model = "sphere", # küre
            texture = "sunflower.hdr",
            double_sided = True, # iki yönlü
            scale = 1200,
            y = -50,
            rotation_y = 90,
            unlit = True
        )
# MARK:input
def input(key):
    global mode, reaction_time

    if key == "right arrow":
        reaction_time = time.time() - start_time
        actor.play("right")
    
    elif key == "left arrow":
        reaction_time = time.time() - start_time
        actor.play("left")
    
    elif key == "up arrow":
        reaction_time = time.time() - start_time
        actor.play("idle")
    
    elif key == "v up":
        body_collider.visible = not body_collider.visible
    
    elif key == "right mouse down":
        ball.rotation = Vec3(0)
        ball.position = Vec3(0, 2, -250) # topun başlangıç konumu
        # if mouse.world_point:
        #     ball.position = mouse.world_point
    elif key == "b up": # b is BOT
        print_on_screen("AI", scale=5, duration=5) 
        mode = "AI"
        # model.train()
        # model.save_model()
        model.load_model()

    elif key == "u up":
        print_on_screen("USER", scale=5, duration=5) 
        mode = "USER"

    # elif key == "1":
    #     model.load_model(model_name = "caglar.pkl")
    # elif key == "2":
    #     model.load_model(model_name = "hakan.pkl")
    # elif key == "3":
    #     model.load_model(model_name = "ihsan.pkl")
    # elif key == "4":
    #     model.load_model(model_name = "mustafa.pkl")
    # elif key == "5":
    #     model.load_model(model_name = "selman.pkl")


def shoot(): #MARK:shoot
    global start_time, click_position
    # Top fırlatıldığında başlangıç zamanını kaydedin
    start_time = time.time()
    
    ball.start = 1 # topun çıkışını haber veriyoruz

    if mouse.world_point:
        empty = Entity(position = mouse.world_point)
    else:
        empty = Entity()
    empty.look_at(ball)

    ball.rotation = empty.rotation
    
    click_position = empty.position

    destroy(empty)

    ball.rotation_x -= 30
    ball.anim = ball.animate_position(ball.forward*10, duration=2, curve=curve.linear)

    # topun animasyonu bitince zemine düşmesi / çıkması
    invoke(ball.animate_y, 2, 1, delay=2) # belirli bir süre sonra tetikle 2 y=2 demek, 1 sn de demek

    # MARK:predict    
    if mode == "AI":
        reaction_time, direction = model.predict([click_position])

        # hamleyi uygula
        invoke(goalkeeper_move, direction, delay=reaction_time)

def goalkeeper_move(direction): # left, idle, right  -> 0,1,2
    if direction == 2: 
        actor.play("right") # 2
    elif direction == 0:
        actor.play("left") # 0
    else:
        actor.play("idle") # 1

# MARK:update
def update():
    if actor.getCurrentAnim() == None:
        actor.loop("idle")

    # kalecinin topu yakalaması
    if ball.intersects(body_collider).hit and ball.start:
        ball.start = 0

        # direction : kalecinin hamle yönü
        if body_collider.world_x < -3.5:
            direction = 0 # left
        elif body_collider.world_x > 3.5:
            direction = 2 # right
        else:
            direction = 1 # idle
        model.save_data(click_position, reaction_time, direction) #MARK:save_data

        # print_on_screen("KALECİ TUTTU", scale=3)
        angle = ball.intersects(body_collider).world_normal
        ball.look_at_2d(ball.position + angle, "y")
        ball.anim = ball.animate_position(ball.forward*30, duration=3, curve=curve.out_circ)
        ball.direction = 3
        return

    # topun kalenin sağ,sol,yukarına çarpması
    hit_info = ball.intersects(ignore = [ground, front_wall, body_collider])
    if hit_info.hit:
        print("hit")
        for seq in ball.anim: # animasyonun tüm çerçevelerini bitir
            seq.kill()
        ball.position = hit_info.world_point
        # invoke çalıştığı için y konumu 2 sn sonra tekrar 2 oluyor

    # GOL olayı
    if ball.intersects(front_wall).hit:
        print_on_screen("GOOOOL", scale=5, position=(-.3, -.3))
        for seq in ball.anim: # animasyonun tüm çerçevelerini bitir
            seq.kill()

    # zemine çarpma 
    if ball.y <= 1.5:
        for seq in ball.anim: # animasyonun tüm çerçevelerini bitir
            seq.kill()

    # topun çarpma sonrası yuvarlanması
    elif ball.direction > 0:
        ball.rotation_x += 100 * ball.direction * time.dt
        ball.direction -= time.dt
        if ball.direction < 0: ball.direction = 0


app = Ursina(borderless = False)

player = Entity(scale=20, shader=bls)

actor = Actor("assets/goalkeeper.glb") # assets mutlaka yazılmalı
actor.reparentTo(player) # animasyonları playere yükledik
print(actor.getAnimNames()) # animasyonların isimlerini getir 
print(actor.getJoints()) # animasyon eklemlerini getir

actor.loop('idle')

body = actor.exposeJoint(None, 'modelRoot', 'mixamorig5:Spine') # mixamorig5 isminde 5 sayısı animasyona göre değişir
body_collider = Entity(model="cube", scale=(50,100,30),  collider="box", visible=False)
body_collider.reparent_to(body)

# zemin
ground = Entity(model="plane", scale=1000, scale_x = 2500, texture="field", z = -1066, rotation_y=90, collider="box")

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

front_wall = Entity(model="cube", scale=(120,45,5), origin_y=-.5, world_position=Vec3(-5.6, 1.45, 5), collider="box", double_sided=True, color=clr) 
back_wall = Entity(model="quad", scale=(125,50), origin_y=-.5, world_position=Vec3(-5.6, 1.45, 35), collider="box", double_sided=True, color=clr) 
front_wall.collider.visible = False

camera.y = 20
camera.z = -370

Sky() 

# EditorCamera()

sun = DirectionalLight()
sun.look_at((1, -1, -3))

# modeli yükle
model = GoalkeeperModel()
try:
    model.load_model()
except:
    pass
app.run()

