import random



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


class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [["~" for i in range(size)] for i in range(size)]
        self.radar = [["~" for i in range(size)] for i in range(size)]
        self.ships_cords = set()
        self.ships = []
        self.board_coords = self._get_coords_board(size)

    def _get_coords_board(self, size):
        coords = set()
        for i in range(0, size ):
            for d in range(0, size ):
                coords.add((i, d))
        return tuple(coords)

    def ship_randomizer(self, ship_vars):
        while True:
            size = ship_vars
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            rotation = random.choice(["left", "right", "up", "dawn"])
            ship = Ship(int(size), x, y, rotation)
            ship = ship.coords
            aura = ship.aura#надо спросить почему корды из экземпляра достать получилось а ауру нет
            if self.can_plays_ship(ship,self.board_coords):
                if self.other_ship(aura, self.ships_cords):
                    self.add_ship(ship, rotation, x, y)
                    break
                else:
                    continue
            else:
                continue

    def can_plays_ship(self,ship, board_coords):
        for i in ship:
            if i in board_coords:
                return True
            else:
                return False

    def other_ship(self,aura, ships_cords):
        intersec = []
        for i in aura:
            if i in ships_cords:

                intersec.append(1)
            else:
                pass
        if intersec:
            return False
        else:
            return True

    def add_ship(self, ship, rotation, x, y):

        self.ships.append((x, y))
        if rotation == "left":
            for i in range(ship.size):
                self.grid[x + i][y] = "■"
                self.ships_cords.add((x + i, y))

        elif rotation == "right":
            for i in range(ship.size):
                self.grid[x - i][y] = "■"
                self.ships_cords.add((x - i, y))

        elif rotation == "up":
            for i in range(ship.size):
                self.grid[x][y + i] = "■"
                self.ships_cords.add((x, y + i))

        elif rotation == "dawn":
            for i in range(ship.size):
                self.grid[x][y - i] = "■"
                self.ships_cords.add((x, y - i))

    # self.Ship.nose

    def fild(self):
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.grid[i])
            print(f)

    def radar(self):
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.radar[i])
            print(f)