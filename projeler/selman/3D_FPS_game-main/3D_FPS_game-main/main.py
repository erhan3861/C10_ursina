from ursina import *
from direct.actor.Actor import Actor
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint
from mermi import *
from ursina.shaders import basic_lighting_shader as bls, colored_lights_shader as cls
from collider_setup import *
from bomba import *
from effects import Effects
from collect import *

Entity.default_shader = bls

class CustomSky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture="sunset.hdr",
            double_sided=True,
            scale=3000,
            shader=cls
        )


class Enemy(Entity):
    enemy_list = []
    def __init__(self,  move_speed=0.1, collider_speed=1, **kwargs):
        super().__init__(model=None, scale=0.7, y=0, collider="box", **kwargs)
        self.actor = Actor("assets/hero.glb")
        self.actor.reparentTo(self)
        # self.actor.loop('walk')
        # self.actor.setPlayRate(0.71, 'Walk')  # Set the animation speed
        self.collider = BoxCollider(self, size=(1, 3, 1))
        self.shader = cls
        self.collider_speed = collider_speed  # Collider speed
        print(self.actor.get_anim_names())
        # self.collider.visible = True
        self.speed = 0.1

        Enemy.enemy_list.append(self)

    def update(self):
        dist = distance_xz(self, player)

        if dist < 5:
            print_on_screen("BUSTED")
            if self.actor.getCurrentAnim() == None:
                self.actor.play("attack")
        else:
            if self.actor.getCurrentAnim() == None:
                self.actor.play("walk")

        self.look_at_2d(player, axis="y")
        self.position += self.forward * time.dt * self.speed  # Movement speed multiplier

        for enemy in Enemy.enemy_list:
            if enemy == self: continue
            if distance_xz(self, enemy) < 1:
                self.position -= self.forward * time.dt * self.collider_speed  # Collider speed multiplier

        for b in Ball.ball_list:
            if distance(b, self) < 1:
                self.hit_enemy()

        self.rotation_y += 180

    def hit_enemy(self):
        self.z -= 25

    def input(self, key):
        if key == "1":
            self.actor.play("attack_walk_walk1")
        elif key == "2":
            self.actor.play("attack")
        elif key == "3":
            self.actor.play("walk_normal")

def input(key):
    if key == 'left mouse down':
        dir = camera.forward + Vec3(0, 0.01, 0)
        pos = player.position + player.forward + Vec3(0, 1.6, 0)
        ball = Ball(pos=pos, speed=15, dir=dir, rot=player.rotation)
        ball.shader = bls
    elif key == 'b up':
            e = PhysicsEntity(model='bomba', velocity=Vec3(0), scale =1 ,position=player.position+Vec3(0,1.5,0)+player.forward, collider='box')
            e.velocity = (camera.forward + Vec3(0,.5,0)) * 15

            invoke(Particle.move, e, Enemy.enemy_list, delay=2.9)
            invoke(generate_particle, e,  delay=2.9)


def generate_particle(entity):
    p = Effects(parent=entity, position=entity.position, file=r'effects\dust.ptf')
    p.scale = 3
    a = Audio("sounds/cannon.wav", autoplay=False, auto_destroy=True)
    a.play()
    
app = Ursina(borderless=False)

sky = CustomSky()

arena = Entity(model="map6", scale=350, y=-34.5) #harita14

ground = Entity(model="plane", scale=300, y=0, texture="grass", color=color.lime)
ground_box = Entity(model="plane", scale=300, y=-1.5, collider="box")

player = FirstPersonController(x=-10, origin_y=-.5, speed=3)
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))
player_step_sound = Audio("sounds/footstep.wav", autoplay=False, auto_destroy=False)

# Gun setup with model 'gun3'
gun = Entity(model='gun3', parent=camera, position=(.5, -.25, .25), scale=(.3, .2, 1), origin_z=-.5, on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=8, y=1, x=5, world_scale=.5, model='quad', color=color.yellow, enabled=False)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

def update():
    if held_keys['left mouse']:
        shoot()

    # sound issue
    if held_keys["w"] or held_keys["a"] or held_keys["s"] or held_keys["d"]:
            if not player_step_sound.playing:
                player_step_sound.play()  
    
def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled = True
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise',
              pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0)
        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, gun, 'on_cooldown', False, delay=.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)


enemies = [Enemy(x=x * 20, anim_speed=0.5, move_speed=0.1, collider_speed=0.05) for x in range(5)]  # Düşmanların animasyon, hareket ve collider hızlarını azaltmak için değerler eklendi
collects = [Collect(player = player, y=0.5, scale=.5) for i in range(10)]
Collect.gui()

setup_scene("assets\colliders.json", 350)

#EditorCamera()

app.enableParticles()
app.run()
