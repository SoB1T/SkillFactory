import random


class Ship:
    def __init__(self, w, nose):
        self.w = w
        self.hp = w
        self.nose = nose  # nose[[x],[y],"left"]

    def hit(self):
        self.hp -= 1

    def destrou(self):
        return self.hp == 0


# class Dots():
#     def __init__(self):
#         self.
#         self.type1="~"
#         self.type2="X"
#         self.type3="■"
#         self.type4="O"
class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [["~" for i in range(size)] for i in range(size)]
        self.radar = [["~" for i in range(size)] for i in range(size)]
        self.ships_cords = []
        self.ships = []

    def ship_randomizer(self, ship):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            rotation = random.choice(["left", "right", "up", "dawn"])
            if self.can_plays_ship(ship, rotation, x, y):
                if self.other_ship(ship, rotation, x, y):
                    self.add_ship(ship, rotation, x, y)
                    break
            else:
                pass

    def can_plays_ship(self, ship, rotation, x, y):
        if rotation == "left":
            if x == 5 and ship > 1:
                return False
            else:
                return True
        elif rotation == "right":
            if x == 0 and ship > 1:
                return False
            else:
                return True
        elif rotation == "up":
            if y == 5 and ship > 1:
                return False
            else:
                return True
        elif rotation == "dawn":
            if y == 0 and ship > 1:
                return False
            else:
                return True

    def other_ship(self, ship, rotation, x, y):
        if rotation == "left" or rotation == "right":
            for d in range(y - 1, y + 2):
                for i in range(x - 1, x + ship + 1):
                    if d == y and i == x:
                        continue
                    elif d == y and i == x + ship:
                        continue
                    else:
                        if [i, d] in self.ships:
                            return False
                        else:
                            return True
        if rotation == "up" or rotation == "dawn":
            for d in range(y - 1, y + ship + 1):
                for i in range(x - 1, x + 2):
                    if d == y and i == x:
                        continue
                    elif d == y + ship and i == x:
                        continue
                    else:
                        if [i, d] in self.ships:
                            return False
                        else:
                            return True

    def add_ship(self, ship, rotation, x, y):

        if rotation == "left":
            for i in range(ship):
                self.grid[x + i][y] = "■"
                self.ships.append([x, y])
                self.ships_cords.append([x + i, y])
                self.Ship.w([x + i, y])
        if rotation == "right":
            for i in range(ship):
                self.grid[x - i][y] = "■"
                self.ships.append([x, y])
                self.ships_cords.append([x - i, y])
                self.Ship.w([x - i, y])
        if rotation == "up":
            for i in range(ship):
                self.grid[x][y + i] = "■"
                self.ships.append([x, y])
                self.ships_cords.append([x, y + i])
                self.Ship.w([x, y + i])
        if rotation == "dawn":
            for i in range(ship):
                self.grid[x][y - i] = "■"
                self.ships.append([x, y])
                self.ships_cords.append([x, y - i])
                self.Ship.w([x, y - i])
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
