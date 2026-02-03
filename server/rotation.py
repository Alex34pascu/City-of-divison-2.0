import math
def get_dir(facing):
 final=""
 if facing==0:
  final="north"
 if facing==45:
  final="north east"
 if facing==90:
  final="east"
 if facing==135:
  final="south east"
 if facing==180:
  final="south"
 if facing==225:
  final="south west"
 if facing==270:
   final="west"
 if facing==315:
  final="north west"
 return final


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