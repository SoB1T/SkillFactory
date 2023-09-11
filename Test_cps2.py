import random
from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int


class Ship:
    def __init__(self, size, x, y, rotation):
        self.cell = Cell(x, y)
        self.size = size
        self.hp = size
        self.rotation = rotation
        self.coords = self._get_coords()
        self.aura = self._get_coords_aura()

    def __repr__(self):
        return f'Ship {self.size} {self.cell} {self.hp} {self.rotation}'

    def _get_coords_aura(self):
        aura = []
        for i in self.coords:
            for d in range(-1, 2):
                x = i.x + d
                for j in range(-1, 2):
                    y = i.y + j
                    aura.append(Cell(x, y))
        return tuple(aura)

    def _get_coords(self):
        coords = []
        if self.rotation == "up":
            for i in range(self.size):
                x = self.cell.x
                y = self.cell.y - i
                coords.append(Cell(x, y))
        if self.rotation == "dawn":
            for i in range(self.size):
                x = self.cell.x
                y = self.cell.y + i
                coords.append(Cell(x, y))
        if self.rotation == "right":
            for i in range(self.size):
                x = self.cell.x - i
                y = self.cell.y
                coords.append(Cell(x, y))
        if self.rotation == "left":
            for i in range(self.size):
                x = self.cell.x + i
                y = self.cell.y
                coords.append(Cell(x, y))

        return tuple(coords)

    def hit(self):
        self.hp -= 1
        if self.hp == 0:
            return True
        return False



class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [["~" for i in range(size)] for i in range(size)]
        self.radar = [["~" for i in range(size)] for i in range(size)]
        self.full_coords = []
        self.ships = []
        self.ship_vars = [3, 2, 2, 1, 1, 1, 1]  # временный вариант

    def ship_randomizer(self, ship_var):
        count = 0
        while count <= 500:
            size = ship_var
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            rotation = random.choice(["left", "right", "up", "dawn"])
            ship = Ship(size, x, y, rotation)
            count += 1
            # надо спросить почему корды из экземпляра достать получилось а ауру нет
            if self.can_plays_ship(ship):
                if self.other_ship(ship):
                    self.add_ship(ship)
                    return True
                else:
                    continue
            else:

                continue
        return False

    def can_plays_ship(self, ship):
        for i in ship.coords:
            x = i.x
            y = i.y
            if x in range(0, 6) and y in range(0, 6):
                pass
                if i in self.full_coords:
                    return False
                else:
                    pass
            else:
                return False
        return True

    def other_ship(self, ship):
        for i in ship.coords:
            if i in self.full_coords:
                return False
            else:

                pass  # (2, 0), (2, 1), (2, 2) (0, 1), (4, 3), (4, 0), (5, 5), (2, 4), (2, 5), (0, 3), (0, 4)]
        return True

    def add_ship(self, ship):
        x = ship.cell.x
        y = ship.cell.y
        self.ships.append(ship)
        # self.ships.append(Cell(x, y))
        for i in ship.aura:
            self.full_coords.append(i)
        for d in list(ship.coords):
            self.full_coords.append(d)
            if ship.rotation == "left":
                for i in range(ship.size):
                    self.grid[ship.cell.x + i][ship.cell.y] = "■"
            elif ship.rotation == "right":
                for i in range(ship.size):
                    self.grid[ship.cell.x - i][ship.cell.y] = "■"
            elif ship.rotation == "up":
                for i in range(ship.size):
                    self.grid[ship.cell.x][ship.cell.y - i] = "■"
            elif ship.rotation == "dawn":
                for i in range(ship.size):
                    self.grid[ship.cell.x][ship.cell.y + i] = "■"

    def fill_the_field(self):
        counter = 0

        for i in self.ship_vars:
            while True:

                counter += 1
                if counter >= 500:

                    self.__init__(self.size)
                    return False

                else:
                    if self.ship_randomizer(i):
                        break
                    else:
                        continue

        return True

    # self.Ship.n

    def fild(self):
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.grid[i])
            print(f)

    def empty_fild(self):
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.radar[i])
            print(f)


class Player:
    def __init__(self, size):
        self.player_move = []
        self.board = Board(size)
        self.gen_fild()
        self.ships = self.board.ships
        self.ships_destrou = []
        self.life_ships = len(self.ships) - len(self.ships_destrou)

    def gen_fild(self):
        success = False
        while success is False:
            success = self.board.fill_the_field()


class Ai(Player):

    def make_move(self):
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            shot = Cell(x, y)
            if shot in self.player_move:
                continue
            else:
                self.player_move.append(shot)

                return True



class User(Player):
    def move_in_board(self, shot):
        if shot.x not in range(0, 6) and shot.y not in range(0, 6):
            return False
        else:
            return True

    def make_move(self):
        while True:
            try:
                x, y = input("Сделайте свой ход, например A 1").split()
                x, y = ord(x) - ord('A'),int(y)- 1
                shot = Cell(x, y)
                if not self.move_in_board(shot):
                    raise CellOutException("Вне границы доски")
                elif shot in self.player_move:
                    print("Сюда вы уже стреляли")
                    continue
                else:
                    self.player_move.append(shot)
                    return True
            except ValueError:
                print("Неправильный ввод")
            except CellOutException as e:
                print(e)


class CellOutException(Exception):
    pass


class Game_controler:
    def __init__(self):
        self.player_1 = User(6)
        self.player_2 = Ai(6)
        self.players = [self.player_2, self.player_1]
        self.conts = []
        self.move_count = len(self.conts)

    def hit_check(self,moving_player, other_player):
        if moving_player.make_move():
            for ship in other_player.ships:
                for i in moving_player.player_move:
                    if i in ship.coords:
                        if ship.hit():
                            other_player.ships_destrou.append(1)
                            if moving_player == self.player_1:
                                print(f"Игрок уничтожил корабль компьютера")
                            else:
                                print(f"Компьютер уничтожил корабль игрока")
                        else:
                            if moving_player == self.player_2:
                                self.player_1.board.grid[i.x][i.y] = "X"
                                print(f"Компьютер поразил корабль игрока")
                                pass
                            else:
                                print(f"Игрок поразил корабль компьютера")
                                self.player_1.board.radar[i.x][i.y] = "X"
                                pass
                        return True
                    else:
                        if moving_player == self.player_2:
                            print("Компьютер промазал")
                            self.player_1.board.grid[i.x][i.y] = "O"
                            pass
                        else:
                            print("Вы промазали")
                            self.player_1.board.radar[i.x][i.y] = "O"
                            pass
                        return False
    def move(self):
        random.shuffle(self.players)
        moving_player, other_player = self.players[0], self.players[1]
        while True:
            print("-"* 100)
            print("Поле противника(компьютер)")
            self.player_1.board.empty_fild()
            print("Ваше поле")
            self.player_1.board.fild()
            if self.player_1.life_ships == 0:
                print("Поле противника(компьютер)")
                self.player_2.board.fild()
                print("Ваше поле")
                self.player_1.board.fild()
                print("Компьютер победил")
                return True
            elif self.player_2.life_ships == 0:
                print("Поле противника(компьютер)")
                self.player_2.board.fild()
                print("Ваше поле")
                self.player_1.board.fild()
                print("Игрок победил")
                return True
            else:
                if self.hit_check(moving_player, other_player):
                    continue
                else:
                    if moving_player == self.player_1:
                        moving_player, other_player = self.player_2, self.player_1
                    else:
                        moving_player, other_player = self.player_1, self.player_2


def main():
    game = Game_controler()
    game.move()
main()