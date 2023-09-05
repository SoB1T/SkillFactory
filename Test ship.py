class Ship:
    def __init__(self, size, x, y, rotation):
        self.x = x
        self.y = y
        self.size = size
        self.hp = size
        self.rotation = rotation
        self.coords = self._get_coords(x, y, size, rotation)
        self.aura = self._get_coords_aura(x, y, size, rotation, self.coords)

    def _get_coords_aura(self, x, y, size, rotation, coords):
        aura = set()
        if rotation == "left" or rotation == "right":
            for d in range(y - 1, y + 2):
                for i in range(x - 1, x + size + 1):
                    if (i, d) in coords:
                        continue
                    else:
                        aura.add((i, d))
            return tuple(aura)
        if rotation == "up" or rotation == "dawn":
            for d in range(y - 1, y + size + 1):
                for i in range(x - 1, x + 2):
                    if (i, d) in coords:
                        continue
                    else:
                        aura.add((i, d))
            return tuple(aura)

    def _get_coords(self, x, y, size, rotation):
        coords = set()
        if rotation == "up":
            for i in range(size):
                coords.add((x, y - i))
        if rotation == "dawn":
            for i in range(size):
                coords.add((x, y + i))
        if rotation == "right":
            for i in range(size):
                coords.add((x - i, y))
        if rotation == "left":
            for i in range(size):
                coords.add((x + i, y))

        return tuple(coords)

    def hit(self):
        self.hp -= 1

    def destrou(self):
        return self.hp == 0


ship=Ship(2, 2, 3,"right")
# print(ship.size)
print(ship.aura)
# print(ship.rotation)
print(ship.coords)
# print(ship.x)
# print(ship.y)
# print(ship.hp)


def _get_coords_board(size):
    coords = set()
    for i in range(0, size):
        for d in range(0, size):
            coords.add((i, d))
    return tuple(coords)

print(_get_coords_board(6))

def can_plays_ship(ship, board_coords):
    for i in ship:
        if i in board_coords:
            return True
        else:
            return False

def other_ship( aura, ships_cords):
    intersec=[]
    for i in aura:
        if i in ships_cords:

            intersec.append(1)
        else:
            pass
    if intersec:
        return False
    else:
        return True

ships_cord=((2,3),(1,3))
ships_cords=set(ships_cord)
print(ships_cords)
print(other_ship(ship.aura,ships_cords))