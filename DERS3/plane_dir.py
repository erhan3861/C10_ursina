def input(key):
    if key == "y up" and held_keys["control"]:
        cannon2.plane_direction = (0,0,1)
        cannon2.lock = (0,0,1)
    if key == "x up" and held_keys["control"]:
        cannon2.plane_direction = (0,1,0)
        cannon2.lock = (0,1,0)
