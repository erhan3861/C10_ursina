from ursina import *
from ursina.shaders import basic_lighting_shader as bls
import json


class Car(Entity):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.position =  Vec3(25, -4.30, -200)
        self.collider = "box"
        self.lap = 1
        self.clicked = False
        self.stop = False
        self.sequence = Sequence(loop=True, auto_destroy=False)
        self.route = self.load_route()

        self.on_click = self.select_obj # seçim

    def input(self, key):
        if key == "g up":
            self.sequence.finish()
            self.car_sequence()

        elif key == "e":  
            self.stop = not self.stop
            if self.stop :
                self.sequence.pause() # duraklatmak
            else:
                self.sequence.resume() # devam ettir


    def select_obj(self):
        self.clicked = True 

    def load_route(self):
        with open("assets/path.json", 'r') as f:
            route_data = json.load(f)
            locations = list(route_data.values())
            locations.reverse()
            
        return locations


    def goTo(self, pos): 
        self.look_at_2d(Vec3(pos), axis="y")

        # İki nokta arasındaki uzaklık hesaplanır
        distance_to_target = distance(self, Vec3(pos))

        # Arabanın rotation_x değeri hesaplanır
        self.rotation_x = math.degrees(math.atan2(self.y-pos[1], distance_to_target))

        self.animate_position(pos, duration=1, curve=curve.linear)
        

    def car_sequence(self):
        for pos in self.route:
            # self.sequence.append(Func(setattr, self, 'position', tuple(pos)))
            self.sequence.append(Func(self.goTo, tuple(pos)))
            self.sequence.append(Wait(1))
        self.sequence.start()

if __name__ == "__main__":
    app = Ursina()

    car = Car(model="car")
    print(car.route)

    ground = Entity(model="plane", texture="grass", scale=500, collider="box", y=-5)
    EditorCamera()

    app.run()
