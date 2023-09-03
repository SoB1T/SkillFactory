import random


class Ship:
    def __init__(self, size):
        self.size = size
        self.hp = size
        self.coords = set()

    def hit(self):
        self.hp -= 1

    def destrou(self):
        return self.hp == 0

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
                    continue
            else:
                continue

    def can_plays_ship(self, ship, rotation, x, y):
        if rotation == "left":
            if x == 5 and ship.size > 1:
                return False
            else:
                return True
        elif rotation == "right":
            if x == 0 and ship.size > 1:
                return False
            else:
                return True
        elif rotation == "up":
            if y == 5 and ship.size > 1:
                return False
            else:
                return True
        elif rotation == "dawn":
            if y == 0 and ship.size > 1:
                return False
            else:
                return True

    def other_ship(self, ship, rotation, x, y):
        if rotation == "left" or rotation == "right":
            for d in range(y - 1, y + 2):
                for i in range(x - 1, x + ship.size + 1):
                    if d == y and i == x:
                        continue
                    elif d == y and i == x + ship.size:
                        continue
                    else:
                        if [i, d] in self.ships_cords:
                            return False
                        else:
                            return True
        if rotation == "up" or rotation == "dawn":
            for d in range(y - 1, y + ship.size + 1):
                for i in range(x - 1, x + 2):
                    if d == y and i == x:
                        continue
                    elif d == y + ship.size and i == x:
                        continue
                    else:
                        if [i, d] in self.ships_cords:
                            return False
                        else:
                            return True

    def add_ship(self, ship, rotation, x, y):

        self.ships.append([x, y])
        if rotation == "left":
            for i in range(ship.size):
                self.grid[x + i][y] = "■"
                self.ships_cords.append([x + i, y])
                ship.coords.add((x + i, y))
        elif rotation == "right":
            for i in range(ship.size):
                self.grid[x - i][y] = "■"
                self.ships_cords.append([x - i, y])
                ship.coords.add((x - i, y))
        elif rotation == "up":
            for i in range(ship.size):
                self.grid[x][y + i] = "■"
                self.ships_cords.append([x, y + i])
                ship.coords.add((x, y + i))
        elif rotation == "dawn":
            for i in range(ship.size):
                self.grid[x][y - i] = "■"
                self.ships_cords.append([x, y - i])
                ship.coords.add((x, y - i))

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


def main():
    player_board = Board(6)
    computer_board = Board(6)

    player_ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]
    computer_ships = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]

    for ship in player_ships:
        player_board.ship_randomizer(ship)

    for ship in computer_ships:
        computer_board.ship_randomizer(ship)

    player_moves = set()
    computer_moves = set()

    while True:
        print("Поле игрока!:")
        player_board.fild()
        print("\nПоле компьютера!:")
        computer_board.fild()

        try:
            player_move = input("Сделайте ход (например, A1): ").upper()
            if player_move in player_moves:
                raise Exception("Вы уже стреляли по этой ячейке.")

            player_moves.add(player_move)
            x = int(player_move[1]) - 1
            y = ord(player_move[0]) - ord('A')

            if computer_board.grid[y][x] == '■':
                print("Вы подбили вражеский корабль!")
                for ship in computer_ships:
                    if (y, x) in ship.coords:
                        ship.hit()
                        if ship.destrou():
                            print("Вражеский корабль потоплен!")
                            for coord in ship.coords:
                                computer_board.grid[coord[0]][coord[1]] = 'X'
                            computer_ships.remove(ship)
                        else:
                            computer_board.grid[y][x] = 'X'
            else:
                print("Мимо!")
                computer_board.grid[y][x] = 'T'

            for ship in player_ships:
                print(f"Игрок: Корабль размером {ship.size}, попаданий: {ship.hit}, координаты: {ship.coords}")

            while True:
                computer_move = (random.randint(0, 5), random.randint(0, 5))
                if computer_move not in computer_moves:
                    computer_moves.add(computer_move)
                    break

            if player_board.grid[computer_move[0]][computer_move[1]] == '■':
                print("Компьютер попал по вашему кораблю!")
                for ship in player_ships:
                    if computer_move in ship.coords:
                        ship.hit()
                        if ship.destrou():
                            print("Ваш корабль потоплен!")
                        player_board.grid[computer_move[0]][computer_move[1]] = 'X'
                        ship.coords.remove(computer_move)
            else:
                print("Компьютер промахнулся!")
                player_board.grid[computer_move[0]][computer_move[1]] = 'T'

            for ship in computer_ships:
                print(f"Компьютер: Корабль размером {ship.size}, попаданий: {ship.hit}, координаты: {ship.coords}")

            if all(ship.destrou() for ship in computer_ships):
                print("Поздравляю! Вы выиграли!")
                break

            if all(ship.destrou() for ship in player_ships):
                print("Компьютер выиграл!")
                break

            print("Состояние игры:")
            print("Корабли противника:")
            for ship in computer_ships:
                print(f"Корабль размером {ship.size}, потоплен: {ship.destrou()}")
            print("Ваши корабли:")
            for ship in player_ships:
                print(f"Корабль размером {ship.size}, потоплен: {ship.destrou()}")

        except Exception as e:
            print("Ошибка:", e)


main()
