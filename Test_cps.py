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

    def destrou(self):
        if self.hp==0:
            return self.hp == 0


class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [["~" for i in range(size)] for i in range(size)]
        self.radar = [["~" for i in range(size)] for i in range(size)]
        self.full_coords = []
        self.ships = []
        self.ship_vars = [3,2,2,1,1,1,1]  # временный вариант


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
            if x in range(0,6) and y in range(0,6):
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
    def __init__(self,size):
        self.player_move= []
        self.filde=[]
        self.ships=[]
        self.size=size
    def gen_fild(self):
        board=Board(self.size)
        success = False
        while success is False:
            success = board.fill_the_field()
        self.filde.append(board.fild())
        self.ships.append(board.ships)
class Ai(Player):
    def make_move(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if x in self.player_move and y in self.player_move:
                continue
            else:
                self.player_move.append(Cell(x,y))
                break
class User(Player):
    def move_in_board(self,shot):
        if shot.x not in range(0,6) and shot.y not in range(0,6):
            return False
        else:
            return True
    def make_move(self):
        try:
            x,y =input("Сделайте свой ход, например A1")
            x,y = int(x), int(y)
            shot= Cell(x,y)
            if not self.move_in_board(shot):
                raise CellOutException("Вне границы доски")
            else:
                self.player_move.append(shot)
                return True
        except ValueError:
            print("Неправильный ввод")
        except CellOutException as e:
            print(e)
# функиця мейн для тестов не забудь написать свою логику
class CellOutException(Exception):
    pass

def main():
    player_board = Board(6)
    computer_board = Board(6)
    success = False
    while success is False:
        success = player_board.fill_the_field()
    success = False
    while success is False:
        success = computer_board.fill_the_field()
    player_board.fild()
    print(f"Корабли{player_board.ships} координаты{player_board.full_coords}")
    computer_board.fild()

    # size_ship_vars = ["1", "1", "1", "1", "2", "2", "3"]
    # player_ships = size_ship_vars
    # comp_ships = size_ship_vars
    # for ship_vars in player_ships:
    #     player_board.ship_randomizer(ship_vars)
    #
    # for ship_vars in comp_ships:
    #     computer_board.ship_randomizer(ship_vars)
    #
    # player_moves = set()
    # computer_moves = set()
    #
    # while True:
    #     print("Поле игрока!:")
    #     player_board.fild()
    #     print("\nПоле компьютера!:")
    #     computer_board.fild()
    #
    #     try:
    #         player_move = input("Сделайте ход (например, A1): ").upper()
    #         if player_move in player_moves:
    #             raise Exception("Вы уже стреляли по этой ячейке.")
    #
    #         player_moves.add(player_move)
    #         x = int(player_move[1]) - 1
    #         y = ord(player_move[0]) - ord('A')
    #
    #         if computer_board.grid[y][x] == '■':
    #             print("Вы подбили вражеский корабль!")
    #             for ship in comp_ships:
    #                 if (y, x) in ship.coords:
    #                     ship.hit()
    #                     if ship.destrou():
    #                         print("Вражеский корабль потоплен!")
    #                         for coord in ship.coords:
    #                             computer_board.grid[coord[0]][coord[1]] = 'X'
    #                         comp_ships.remove(ship)
    #                     else:
    #                         computer_board.grid[y][x] = 'X'
    #         else:
    #             print("Мимо!")
    #             computer_board.grid[y][x] = 'T'
    #
    #         for ship in player_ships:
    #             print(f"Игрок: Корабль размером {ship.size}, попаданий: {ship.hit}, координаты: {ship.coords}")
    #
    #         while True:
    #             computer_move = (random.randint(0, 5), random.randint(0, 5))
    #             if computer_move not in computer_moves:
    #                 computer_moves.add(computer_move)
    #                 break
    #
    #         if player_board.grid[computer_move[0]][computer_move[1]] == '■':
    #             print("Компьютер попал по вашему кораблю!")
    #             for ship in player_ships:
    #                 if computer_move in ship.coords:
    #                     ship.hit()
    #                     if ship.destrou():
    #                         print("Ваш корабль потоплен!")
    #                     player_board.grid[computer_move[0]][computer_move[1]] = 'X'
    #                     ship.coords.remove(computer_move)
    #         else:
    #             print("Компьютер промахнулся!")
    #             player_board.grid[computer_move[0]][computer_move[1]] = 'T'
    #
    #         for ship in comp_ships:
    #             print(f"Компьютер: Корабль размером {ship.size}, попаданий: {ship.hit}, координаты: {ship.coords}")
    #
    #         if all(ship.destrou() for ship in comp_ships):
    #             print("Поздравляю! Вы выиграли!")
    #             break
    #
    #         if all(ship.destrou() for ship in player_ships):
    #             print("Компьютер выиграл!")
    #             break
    #
    #         print("Состояние игры:")
    #         print("Корабли противника:")
    #         for ship in comp_ships:
    #             print(f"Корабль размером {ship.size}, потоплен: {ship.destrou()}")
    #         print("Ваши корабли:")
    #         for ship in player_ships:
    #             print(f"Корабль размером {ship.size}, потоплен: {ship.destrou()}")
    #
    #     except Exception as e:
    #         print("Ошибка:", e)
    #


main()
