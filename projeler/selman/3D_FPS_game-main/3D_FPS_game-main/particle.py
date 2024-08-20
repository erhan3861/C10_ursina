from ursina import *
from random import uniform
from ursina.shaders import basic_lighting_shader as bls

class Particle(Entity):
    def __init__(self, position, velocity, color, texture, enemies):
        super().__init__(
            model = "cube",
            color = color,
            texture = texture,
            position = position,
            scale = uniform(0.05, 0.2),
            rotation = Vec3(uniform(0,360),uniform(0,360),uniform(0,360))
        )
        self.velocity = velocity
        self.lifetime = uniform(1, 7)
        self.shader=bls
        self.enemies = enemies
        
    
    def update(self):
        self.position += self.velocity * time.dt
        self.lifetime -= time.dt

        self.hit_enemy()

        if self.lifetime <= 0:
            destroy(self)

    def hit_enemy(self):
        for e in self.enemies:
            if distance(e, self) < 0.5:
                print("hit")
                e.hit_enemy()

    @staticmethod
    def move(entity, enemies=[], clr=color.gray): 
        # entity.animate_scale(Vec3(0,0,0), duration=.1)
        entity.visible = False

        for i in range(50):
            pos = entity.position
            vel = Vec3(random.uniform(-2,2), random.uniform(-2,2), random.uniform(-2,2))
            clr = clr
            txr = "white_cube"

            Particle(pos,vel,clr,txr, enemies)

if __name__ == "__main__":
        
    from ursina.prefabs.first_person_controller import FirstPersonController

    app = Ursina(borderless=False)

    player = FirstPersonController()

    ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=Vec2(32), collider='box')

    def input(key):
        if key == 'left mouse down':
            e = Entity(model='cube', scale =1 ,position=player.position + Vec3(0,1.5,0) + player.camera_pivot.forward*10, collider='box')
            Particle.move(e)

    Sky()

    app.run()
    