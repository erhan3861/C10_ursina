from ursina import held_keys

def editor_cam_handler(key, editor_camera):
    """
    editor camera keys
    x position change -> right arrow - left arrow
    y position change -> scroll up - scroll arrow
    z position change -> up arrow- down arrow
    print position and rotation -> p key
    """
    if not editor_camera.enabled: return
    if key == "scroll up" and editor_camera.enabled:
        editor_camera.y += .5
    elif key == "scroll down" and editor_camera.enabled:
        editor_camera.y -= .5
    elif held_keys["right arrow"] and editor_camera.enabled:
        editor_camera.x += .5
    elif held_keys["left arrow"] and editor_camera.enabled:
        editor_camera.x -= .5
    elif held_keys["up arrow"] and editor_camera.enabled:
        editor_camera.z += .5
    elif held_keys["down arrow"] and editor_camera.enabled:
        editor_camera.z -= .5
    elif held_keys["up arrow"] and editor_camera.enabled:
        editor_camera.z += .5
    elif held_keys["c"] and held_keys["x"] and editor_camera.enabled:
        editor_camera.rotation_x += 5
    elif held_keys["c"] and held_keys["y"] and editor_camera.enabled:
        editor_camera.rotation_y += 5
    elif held_keys["c"] and held_keys["z"] and editor_camera.enabled:
        editor_camera.rotation_z += 5
    elif key=="p": print("position: ", editor_camera.position, "rotation: ", editor_camera.rotation)
