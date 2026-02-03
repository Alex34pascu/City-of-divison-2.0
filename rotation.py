import math
directions = {
        0: "north",
        45: "northeast",
        90: "east",
        135: "southeast",
        180: "south",
        225: "southwest",
        270: "west",
        315: "northwest",
        360: "north",
    }

# Rotation matrix function
def rotate_matrix(x, y, angle, x_shift=0, y_shift=0, units="DEGREES"):
    """
    Rotates a point in the xy-plane counterclockwise through an angle about the origin
    https://en.wikipedia.org/wiki/Rotation_matrix
    :param x: x coordinate
    :param y: y coordinate
    :param x_shift: x-axis shift from origin (0, 0)
    :param y_shift: y-axis shift from origin (0, 0)
    :param angle: The rotation angle in degrees
    :param units: DEGREES (default) or RADIANS
    :return: Tuple of rotated x and y
    """

    # Shift to origin (0,0)
    x -= x_shift
    y -= y_shift

    # Convert degrees to radians
    if units == "DEGREES":
        angle = math.radians(angle)

    # Handle special case for 180-degree rotation
    if angle == math.pi:
        xr = -x
        yr = -y
    else:
        # Rotation matrix multiplication to get rotated x & y
        xr = x * math.cos(angle) - y * math.sin(angle)
        yr = x * math.sin(angle) + y * math.cos(angle)

    # Shift back to the original position
    xr += x_shift
    yr += y_shift

    return xr, yr

def get_dir(facing):

    # Normaliseer facing tussen 0 en 360
    facing = facing % 360

    # Zoek de dichtsbijzijnde hoek
    closest_angle = min(directions.keys(), key=lambda angle: abs(angle - facing))

    return directions[closest_angle]

def snap_to_closest_angle(facing, direction):
    angles = sorted(directions.keys())  # [0, 45, ..., 315]
    facing = facing % 360

    if direction == "right":
        # Zoek eerst de eerstvolgende grotere hoek
        for angle in angles:
            if angle > facing and angle<360:
                return angle
        return 0  # wrap around naar 'north'
    elif direction == "left":
        # Zoek de laatste kleinere hoek
        for angle in reversed(angles):
            if angle < facing:
                return angle
        return 315  # wrap around naar laatste richting
    else:
        # standaard: snap naar dichtstbijzijnde
        closest_angle = min(angles, key=lambda angle: abs(angle - facing))
        return closest_angle
 
def move(x, y, facing, times=1):
    # Zet facing om naar radialen (0° = vooruit op de y-as)
    angle_rad = math.radians(facing)

    # Bereken eenheidsvector in die richting
    dx = math.sin(angle_rad)
    dy = math.cos(angle_rad)

    # Verplaats speler
    x += dx * times
    y += dy * times

    return x, y
def calculate_rotation(x1, y1, x2, y2, facing):
    # Bereken het verschil tussen de twee x-coördinaten
    delta_x = x2 - x1

    # Bereken het verschil tussen de twee y-coördinaten
    delta_y = y2 - y1

    # Bereken de rotatie op de x-as (horizontal rotation)
    rotation_x = math.degrees(math.atan2(delta_y, delta_x))

    # Bereken de rotatie op de y-as (vertical rotation)
    distance = math.sqrt(delta_x**2 + delta_y**2)
    rotation_y = math.degrees(math.atan2(facing, distance))

    return rotation_x, rotation_y