import random


class Ship:
    def __init__(self, size, x, y, rotation):
        self.x = x
        self.y = y
        self.size = size
        self.hp = size
        self.rotation = rotation
        self.coords = self._get_coords()
        self.aura = self._get_coords_aura()

    def _get_coords_aura(self):
        aura = set()
        if self.rotation == "left" or self.rotation == "right":
            for d in range(self.y - 1, self.y + 2):
                for i in range(self.x - 1, self.x + self.size + 1):
                    if (i, d) in self.coords:
                        continue
                    else:
                        aura.add((i, d))
            return tuple(aura)
        if self.rotation == "up" or self.rotation == "dawn":
            for d in range(self.y - 1, self.y + self.size + 1):
                for i in range(self.x - 1, self.x + 2):
                    if (i, d) in self.coords:
                        continue
                    else:
                        aura.add((i, d))
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
    def __init__(self, size):
        self.size = size
        self.grid = [["~" for i in range(size)] for i in range(size)]
        self.radar = [["~" for i in range(size)] for i in range(size)]
        self.ships_cords = set()
        self.ships = []
        self.board_coords = self._get_coords_board()

    def _get_coords_board(self):
        coords = set()
        for i in range(0, self.size):
            for d in range(0, self.size):
                coords.add((i, d))
        return tuple(coords)

    def ship_randomizer(self, ship_vars):
        while True:
            size = ship_vars
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            rotation = random.choice(["left", "right", "up", "dawn"])
            ship = Ship(int(size), x, y, rotation)
            # надо спросить почему корды из экземпляра достать получилось а ауру нет
            if self.can_plays_ship(ship):
                if self.other_ship(ship):
                    self.add_ship(ship)
                    break
                else:
                    continue
            else:
                continue

    def can_plays_ship(self, ship):
        for i in ship.coords:
            if i in self.board_coords:
                pass
            else:
                return False
        return True

    def other_ship(self, ship):
        intersec = []
        for i in ship.aura:
            if i in self.ships_cords:
                print(i)
                intersec.append(1)
                for i in ship.coords:
                    if i in self.ships_cords:
                        intersec.append(1)
                    else:
                        pass
            else:
                pass
        if intersec:
            return False
        else:
            return True

    def add_ship(self, ship):

        self.ships.append((ship.x, ship.y))
        if ship.rotation == "left":
            for i in range(ship.size):
                self.grid[ship.x + i][ship.y] = "■"
                self.ships_cords.add((ship.x + i, ship.y))

        elif ship.rotation == "right":
            for i in range(ship.size):
                self.grid[ship.x - i][ship.y] = "■"
                self.ships_cords.add((ship.x - i, ship.y))

        elif ship.rotation == "up":
            for i in range(ship.size):
                self.grid[ship.x][ship.y - i] = "■"
                self.ships_cords.add((ship.x, ship.y + i))

        elif ship.rotation == "dawn":
            for i in range(ship.size):
                self.grid[ship.x][ship.y + i] = "■"
                self.ships_cords.add((ship.x, ship.y - i))

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


# функиця мейн для тестов не забудь написать свою логику
def main():
    player_board = Board(6)
    computer_board = Board(6)

    size_ship_vars = ["1", "1", "1", "1", "2", "2", "3"]
    player_ships = size_ship_vars
    comp_ships = size_ship_vars
    for ship_vars in player_ships:
        player_board.ship_randomizer(ship_vars)

    for ship_vars in comp_ships:
        computer_board.ship_randomizer(ship_vars)

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
                for ship in comp_ships:
                    if (y, x) in ship.coords:
                        ship.hit()
                        if ship.destrou():
                            print("Вражеский корабль потоплен!")
                            for coord in ship.coords:
                                computer_board.grid[coord[0]][coord[1]] = 'X'
                            comp_ships.remove(ship)
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

            for ship in comp_ships:
                print(f"Компьютер: Корабль размером {ship.size}, попаданий: {ship.hit}, координаты: {ship.coords}")

            if all(ship.destrou() for ship in comp_ships):
                print("Поздравляю! Вы выиграли!")
                break

            if all(ship.destrou() for ship in player_ships):
                print("Компьютер выиграл!")
                break

            print("Состояние игры:")
            print("Корабли противника:")
            for ship in comp_ships:
                print(f"Корабль размером {ship.size}, потоплен: {ship.destrou()}")
            print("Ваши корабли:")
            for ship in player_ships:
                print(f"Корабль размером {ship.size}, потоплен: {ship.destrou()}")

        except Exception as e:
            print("Ошибка:", e)


main()
