import bpy
import json
import os

def mesh_to_dict(obj):
    """Converts a Blender mesh object to a dictionary with name, position, scale, and mesh type."""
    mesh_dict = {
        "name": obj.name,
        "position": {
            "x": obj.location.x,
            "y": obj.location.y,
            "z": obj.location.z
        },
        
        "rotation": {
            "x": obj.rotation_euler.x,
            "y": obj.rotation_euler.y,
            "z": obj.rotation_euler.z
        },
        
        "scale": {
            "x": obj.scale.x,
            "y": obj.scale.y,
            "z": obj.scale.z
        },
        "mesh_type": obj.type
    }
    return mesh_dict

def save_selected_meshes_to_json(filepath):
    """Saves the selected mesh objects in the current Blender scene to a JSON file."""
    selected_meshes = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    
    meshes_data = [mesh_to_dict(mesh) for mesh in selected_meshes]
    
    with open(filepath, 'w') as f:
        json.dump(meshes_data, f, indent=4)
    
    print(f"Saved {len(selected_meshes)} mesh objects to {filepath}")


output_path = r"D:\pythonDerslerim\C10_ursina\DERS13\assets\selected_meshes.json"

# Save the selected meshes to JSON
save_selected_meshes_to_json(output_path)
