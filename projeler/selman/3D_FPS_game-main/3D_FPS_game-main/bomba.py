from ursina import *
from particle import *

physics_entities = []
class PhysicsEntity(Entity):
    def __init__(self, model='bomba', collider='box', **kwargs):
        super().__init__(model=model, collider=collider, **kwargs)
        physics_entities.append(self)
        self.bomb = True
        self.lifetime = 100

    def update(self):
        if self.intersects():
            self.stop()
            return
        if self.y <= .15:
            self.stop()
            return

        self.velocity = lerp(self.velocity, Vec3(0), time.dt)
        self.velocity += Vec3(0,-1,0) * time.dt * 5
        self.position += (self.velocity + Vec3(0,-4,0)) * time.dt


    def stop(self):
        self.y = 0
        self.velocity = Vec3(0,0,0)
        if self in physics_entities:
            physics_entities.remove(self)
        self.bomb_func()

    def on_destroy(self):
        self.stop()


    def throw(self, direction, force):
        pass

    def bomb_func(self):
        if self.bomb:
            a = Audio("sounds/clock.mp3", autoplay=False, auto_destroy=False, loop=True)
            a.play()
            invoke(self.animate_scale(1.3, duration=1, curve=curve.out_expo_boomerang, loop=True))
            destroy(a, delay=2.7)
            destroy(self, delay=3)

        self.bomb = False

   
if __name__ == "__main__":
    from ursina.shaders import lit_with_shadows_shader
    
    Entity.default_shader = lit_with_shadows_shader
    

    from ursina.prefabs.first_person_controller import FirstPersonController
    app = Ursina()
    
    player = FirstPersonController()

    ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=Vec2(32), collider='box')

    def input(key):
        if key == 'left mouse down':
            e = PhysicsEntity(model='bomba', velocity=Vec3(0), scale =1 ,position=player.position+Vec3(0,1.5,0)+player.forward, collider='box')
            e.velocity = (camera.forward + Vec3(0,.5,0)) * 15
            invoke(Particle.move, e, delay=2.9)

    Entity(model="bomba")

    DirectionalLight().look_at(Vec3(1,-1,-1))

    Sky()

    app.run()