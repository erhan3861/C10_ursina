from ursina import *
import json

# JSON dosyasının yolunu belirtin
json_file_path = 'assets/colliders.json'

colliders = []

def load_meshes_from_json(json_file):
    with open(json_file, 'r') as f:
        meshes_data = json.load(f)
    return meshes_data

def create_entity_from_data(mesh_data):
    position = Vec3(mesh_data["position"]["x"], mesh_data["position"]["z"], mesh_data["position"]["y"])
    rotation = Vec3(mesh_data["rotation"]["x"]*-60, mesh_data["rotation"]["z"]*-60, mesh_data["rotation"]["y"]*60)
    scale = Vec3(mesh_data["scale"]["x"], mesh_data["scale"]["z"], mesh_data["scale"]["y"])
    
    entity = Entity(
        name=mesh_data["name"],
        position=position*200,
        rotation=rotation,
        scale=scale*200*2,
        model='plane',  # Placeholder model; you can customize this based on your needs
        collider='box',  # Adding a box collider; customize as needed
        double_sided = True, 
        color = color.red
    )
    colliders.append(entity)
    return entity

def setup_scene(json_file):
    meshes_data = load_meshes_from_json(json_file)
    for mesh_data in meshes_data:
        create_entity_from_data(mesh_data)