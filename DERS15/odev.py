from ursina import *
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader,basic_lighting_shader as bls

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


# ödev
# topa sol tıklama yapınca çalışacak bir fonksiyon tanımlayınız
# Bu fonksiyonun görevi topu tıklamanın tersi istikametine göndermek
# örnek1 topun sol altına tıklayınca top sağ yukarı gitmeli
# örnek2 topun sağ altına tıklayınca top sol yukarı gitmeli
# örnek3 topun orta altına tıklayınca top orta yukarı gitmeli
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
soccer_goal = Entity(model="scene.gltf", x=57, z=11, scale=0.25, rotation_y=180, shader=bls, color=color.white)

# top
ball = Entity(model="ball", scale=4, y=2, z=-250, collider="sphere", shader=bls, start=0, anim=None, direction=0, hit=0)

# ödev
ball.on_click = shoot

# EditorCamera()

camera.y = 20
camera.z = -370

Sky(texture="sky_default", color=color.cyan, alpha=.7) 

app.run()

