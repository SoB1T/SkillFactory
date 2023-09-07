import random
from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int


class Ship:
    def __init__(self, size, x, y, rotation):
        self.cell = Cell(x, y)
        self.x = x
        self.y = y
        self.size = size
        self.hp = size
        self.rotation = rotation
        self.coords = self._get_coords()
        self.aura = self._get_coords_aura()

    def _get_coords_aura(self):
        aura = set()
        for i in self.coords:
            for d in range(-1, 2):
                x = i[0] + d
                aura.add((x, i[1]))
                for d in range(-1, 2):
                    aura.add((x, i[1] + d))
        return tuple(aura)

    def _get_coords(self):
        coords = set()
        if self.rotation == "up":
            for i in range(self.size):
                coords.add((self.x, self.y - i))
        if self.rotation == "dawn":
            for i in range(self.size):
                coords.add((self.x, self.y + i))
        if self.rotation == "right":
            for i in range(self.size):
                coords.add((self.x - i, self.y))
        if self.rotation == "left":
            for i in range(self.size):
                coords.add((self.x + i, self.y))

        return tuple(coords)

    def hit(self):
        self.hp -= 1

    def destrou(self):
        return self.hp == 0


class Board:
    def __init__(self, size, ship_vars=["1", "1", "1", "1", "2", "2", "3"]):
        self.size = size
        self.grid = [["~" for i in range(size)] for i in range(size)]
        self.radar = [["~" for i in range(size)] for i in range(size)]
        self.ships_cords = []
        self.list_ships_cords = self._get_coords_ships()
        self.ships = []
        self.board_coords = self._get_coords_board()
        self.ship_sizes = ship_vars
        self.free_ship_sizes = [int(i) for i in self.ship_sizes]

    def _get_coords_ships(self):
        list = []
        for m in self.ships_cords:
            list.append(m[0])
        return list

    def _get_coords_board(self):
        coords = set()
        for i in range(0, self.size):
            for d in range(0, self.size):
                coords.add((i, d))
        return tuple(coords)

    def ship_randomizer(self):
        counter = 0
        while True:

            size = self.ship_sizes
            size_ship = random.choice(size)
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            rotation = random.choice(["left", "right", "up", "dawn"])
            ship = Ship(int(size_ship), x, y, rotation)
            # надо спросить почему корды из экземпляра достать получилось а ауру нет
            if self.can_plays_ship(ship):
                if self.other_ship(ship):
                    self.add_ship(ship)
                    size.remove(size_ship)
                    return True
                else:
                    counter += 1
                    continue
            elif counter <= 100:
                counter += 1
                continue
            if counter > 100:
                return False

    def can_plays_ship(self, ship):
        for i in ship.coords:
            if i in self.board_coords:
                pass
                if i in self.ships_cords:
                    return False
                else:
                    pass
            else:
                return False
        return True

    def other_ship(self, ship):
        for i in ship.aura:
            if i in self.ships_cords:
                return False
            else:

                pass  # (2, 0), (2, 1), (2, 2) (0, 1), (4, 3), (4, 0), (5, 5), (2, 4), (2, 5), (0, 3), (0, 4)]
        return True

    def add_ship(self, ship):

        self.ships.append((ship.x, ship.y))
        for d in list(ship.coords):
            self.ships_cords.append(d)
            if ship.rotation == "left":
                for i in range(ship.size):
                    self.grid[ship.x + i][ship.y] = "■"


            elif ship.rotation == "right":
                for i in range(ship.size):
                    self.grid[ship.x - i][ship.y] = "■"


            elif ship.rotation == "up":
                for i in range(ship.size):
                    self.grid[ship.x][ship.y - i] = "■"


            elif ship.rotation == "dawn":
                for i in range(ship.size):
                    self.grid[ship.x][ship.y + i] = "■"

    def fill_the_field(self):
        counter = 0
        ships = self.free_ship_sizes

        for i in ships:
            print(ships)
            print(i, "fill")
            while True:
                counter += 1
                if counter >= 500:
                    print("а может ошибка и тут")
                    return False
                else:
                    if self.ship_randomizer():
                        ships.remove(i)
                        if len(ships) == 0:
                            print("ошибка тут")
                        return True
                    else:
                        continue


    def fild(self):
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.grid[i])
            print(f)

    def radars(self):
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.radar[i])
            print(f)


def main():
    player_board = Board(6)

    while True:
        player_board.fill_the_field()
        if player_board.fill_the_field:
            break
        else:
            player_board.__init__()
            continue
    player_board.fild()
    print(player_board.ships_cords)
    print(player_board.ships)