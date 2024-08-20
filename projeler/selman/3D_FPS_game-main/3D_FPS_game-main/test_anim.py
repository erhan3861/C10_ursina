from ursina import *
from direct.actor.Actor import Actor

app = Ursina(borderless=False)

class Enemy(Entity):
    def __init__(self):
        super().__init__()
        self.actor = Actor("assets/sword_man.glb")
        self.actor.reparentTo(self)
        self.actor.loop('walk')

    def input(self, key):
        if key == "1":
            self.actor.play("walk")
        elif key == "2":
            self.actor.play("attack")
        elif key == "3":
            self.actor.play("attack_walk")

enemy = Enemy()

Sky()

EditorCamera()

app.run()
