from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader,basic_lighting_shader as bls

Entity.default_shader = lit_with_shadows_shader

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

def input(key):
    if key == "right arrow":
        actor.play("right")
    elif key == "left arrow":
        actor.play("left")
    elif key == "up arrow":
        actor.play("idle")
    elif key == "v up":
        body_collider.visible = not body_collider.visible
    elif key == "right mouse down":
        ball.rotation = Vec3(0)
        ball.position = Vec3(0, 2, -250) # topun başlangıç konumu


def shoot():
    ball.start = 1
    
    if mouse.world_point:
        empty = Entity(position=mouse.world_point)
    else:
        empty = Entity()
    empty.look_at(ball)
    
    ball.rotation = empty.rotation
    destroy(empty)

    ball.rotation_x -= 30
    ball.anim = ball.animate_position(ball.forward * 10, duration=2,curve=curve.linear)
    
    # topu zemin üzerine getiriyoruz
    invoke(ball.animate_y, 2, 1, delay=2)

def update():
    if actor.getCurrentAnim() == None:
        actor.loop("idle")
    # ders16
    # kalecinin topu yakalaması olayı
    if ball.intersects(body_collider).hit and ball.start:
        angle = ball.intersects(body_collider).world_normal
        ball.look_at_2d(ball.position + angle, "y")
        ball.anim = ball.animate_position(ball.forward * 30, duration=3, curve=curve.out_circ)
        ball.start = 0
        ball.direction = 3
        return
    
    # topun kalenin sağ, sol ve yukarı kısmına çarpması olayı
    hit_info = ball.intersects(ignore=[ground, front_wall, body_collider])
    if hit_info.hit:
        print("hit")
        for seq in ball.anim:
            seq.kill()
        ball.position = hit_info.world_point # topun geriye gitmesi

    # gol olayı
    if ball.intersects(front_wall).hit:
        print_on_screen("GOOOOL", scale=5, position=(-.3,-.3))
        for seq in ball.anim:
            seq.kill()

    # top zemine çarparsa şut animasyonunu durdur
    if ball.y < 1.5: 
        for seq in ball.anim:
            seq.pause()
    # çarpma hareketi sonrası topun x ekseninde yuvarlanması
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

camera.y = 20
camera.z = -370

# kale colliders
clr = color.clear
right_wall = Entity(model="right_wall", world_parent=soccer_goal, world_x=57, world_z=15, collider="box", double_sided=True, color=clr)
left_wall = Entity(model="left_wall", world_parent=soccer_goal, world_x=57, world_z=15, collider="box", double_sided=True, color=clr)
up_wall = Entity(model="up_wall", world_parent=soccer_goal, world_x=57, world_z=15, collider="box", double_sided=True, color=clr)

front_wall = Entity(model="cube", scale=(120,45,5), origin_y=-.5, world_position=Vec3(-5.6, 1.45, 5), collider="box", double_sided=True, color=clr) 
back_wall = Entity(model="quad", scale=(125,50), origin_y=-.5, world_position=Vec3(-5.6, 1.45, 35), collider="box", double_sided=True, color=clr) 
front_wall.collider.visible = False

Sky() 

# EditorCamera()

app.run()

