import random
from dataclasses import dataclass


@dataclass
class Cell:  # обьект с помощью которого мы можем красиво любоваться координатами
    x: int
    y: int


class Ship:  # сам корабль
    def __init__(self, size, x, y, rotation):
        self.cell = Cell(x, y)  # его красивые координаты носа
        self.size = size  # его менее красивый размер
        self.hp = size  # его здоровье
        self.rotation = rotation  # то куда смотрит нос корабля
        self.coords = self._get_coords()  # координаты коробля
        self.aura = self._get_coords_aura()  # аура вокруг корябля где не должны находится чужие корабли сейчас лишь
        # список

    def __repr__(self):  # красивые данные об объекте корабль для тестов убирать жалко
        return f'Ship {self.size} {self.cell} {self.hp} {self.rotation}'

    def _get_coords_aura(self):  # метод для получения координат ауры корабля
        aura = []
        for i in self.coords:  # берет координату из списка координат
            for d in range(-1, 2):  # выбирает один x
                x = i.x + d
                for j in range(-1, 2):  # выбирает и перебирает все y в линии x
                    y = i.y + j
                    aura.append(Cell(x, y))  # заносит одну координату в красивом виде и дает циклу y выполнить шаг
        return tuple(aura)  # возвращает все полученные коодинаты

    def _get_coords(self):  # метод для создания корабля и внесения его координат относительно данных из ship_randomizer
        coords = []
        if self.rotation == "up":  # если корабль смотрит вверх, то мы генерируем и добавляем координаты ниже
            # стартовой точки относительно оси y
            for i in range(self.size):
                x = self.cell.x
                y = self.cell.y - i
                coords.append(Cell(x, y))
        if self.rotation == "dawn":  # если корабль смотрит вниз, то мы генерируем и добавляем координаты выше
            # стартовой точки относительно оси y
            for i in range(self.size):
                x = self.cell.x
                y = self.cell.y + i
                coords.append(Cell(x, y))
        if self.rotation == "right":  # если корабль смотрит вправо, то мы генерируем и добавляем координаты левее
            # стартовой точки относительно оси x
            for i in range(self.size):
                x = self.cell.x - i
                y = self.cell.y
                coords.append(Cell(x, y))
        if self.rotation == "left":  # если корабль смотрит влево, то мы генерируем и добавляем координаты правее
            # стартовой точки относительно оси x
            for i in range(self.size):
                x = self.cell.x + i
                y = self.cell.y
                coords.append(Cell(x, y))
        return tuple(coords)  # возвращаем стартовые координаты

    def hit(self):  # если в корабль попадут
        self.hp -= 1
        if self.hp == 0:
            return True
        return False


class Board:  # великое и ужасное игровое поле
    def __init__(self, size):
        self.size = size  # его размер передается ему при вызове
        self.grid = [["~" for i in range(size)] for i in range(size)]  # генератор матрицы заполненной ~ по факту
        # будущее игровое поле с кораблями
        self.radar = [["~" for i in range(size)] for i in range(size)]  # а это без кораблей
        self.full_coords = []  # координаты всех аур кораблей
        self.ships = []  # список с созданными экземплярами кораблей
        self.ship_vars = [3, 2, 2, 1, 1, 1, 1]  # временный вариант версий кораблей

    def move_in_board(self, cell):  # проверка на то вход в границы поля
        return cell.x not in range(0, self.size) or cell.y not in range(0, self.size)

    def ship_randomizer(self, ship_var):  # бесконечный кошмар генератор кораблей и заполнения поля ими
        count = 0
        while count <= 500:  # не уверен, что этот счетчик на что-то влияет, но работает же
            size = ship_var
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            rotation = random.choice(["left", "right", "up", "dawn"])
            ship = Ship(size, x, y, rotation)
            count += 1
            if self.can_plays_ship(ship):  # проверяет можно ли поставить корабль с учетом аур и других кораблей
                self.add_ship(ship)  # добовляет корабль и ауру
                return True  # передает что установка прошла успешно
            else:
                continue
        return False  # передает что установка прошла провально

    def can_plays_ship(self, ship):
        for i in ship.coords:  # берет по одной координате и перебирает на соотвествие проверкам

            if not self.move_in_board(i):  # корабль влезает в поле?
                pass
                if i in self.full_coords:  # корабль не стоит в упор к другому корабли или на нем
                    return False  # корабль не соответствует требованиям
                else:
                    pass
            else:
                return False  # корабль не соответствует требованиям
        return True  # корабль соответствует требованиям

    def add_ship(self, ship):  # добавляет корабли
        self.ships.append(ship)  # добавляет экземпляр в список для экземпляров
        for i in ship.aura:  # добавляет в координату ауру поскольку на поле рисует другой цикл
            self.full_coords.append(i)
        for i in ship.coords:  # рисует на поле
            self.grid[i.x][i.y] = "■"

    def fill_the_field(self):  # заполнитель поля одна из причин медлительности программы
        counter = 0
        for i in self.ship_vars:  # берет один из вариантов корабля
            while True:
                counter += 1
                if counter >= 500:  # если не ошибаюсь, то если было сделано 250000 попыток без результата начнет
                    # генерацию поля заново очистив поле
                    self.__init__(self.size)
                    return False
                else:
                    if self.ship_randomizer(i):
                        break
                    else:
                        continue
        return True

    def fild(
            self):  # добавляет в матрицу fild разделители ввиде | и список координат сверху A|B и тд и с левого края
        # 1 и тд
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.grid[i])
            print(f)

    def empty_fild(self):  # то же самое, но без кораблей нужен для поля врага
        head = "    " + " | ".join(str(i + 1) for i in range(self.size))
        print(head)
        for i in range(self.size):
            f = f"{chr(65 + i)} | " + " | ".join(self.radar[i])
            print(f)


class Player:  # класс игроков
    def __init__(self, size):
        self.player_move = []  # список ходов
        self.board = Board(size)  # поле игрока
        self.gen_fild()  # генерирует корабли на поле игрока
        self.ships = self.board.ships  # корабли на поле игрока
        self.ships_destrou = []  # уничтожаные корабли
        self.life_ships = len(self.ships) - len(self.ships_destrou)  # остаток живых

    def gen_fild(self):
        success = False
        while success is False:
            success = self.board.fill_the_field()


class Ai(Player):  # класс компьютера
    def make_move(self):  # генератор ходов компа
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            shot = Cell(x, y)
            if shot in self.player_move:
                continue
            else:
                self.player_move.append(shot)
                return shot


class User(Player):  # класс пользователя
    def make_move(self):  # принимает ход игрока и проверяет его на ошибки
        while True:
            try:
                x, y = input("Сделайте свой ход, например A 1").split()
                x, y = ord(x) - ord('A'), int(y) - 1
                shot = Cell(x, y)
                if self.board.move_in_board(shot):
                    raise CellOutException("Вне границы доски")
                elif shot in self.player_move:
                    print("Сюда вы уже стреляли")
                    continue
                else:
                    self.player_move.append(shot)
                    return shot
            except ValueError:
                print("Неправильный ввод")
            except CellOutException as e:
                print(e)


class CellOutException(Exception):
    pass


class Game_Сontroler:  # класс игрового контролера
    def __init__(self):
        self.player_1 = User(6)  # игрок
        self.player_2 = Ai(6)  # компьютер
        self.players = [self.player_2, self.player_1]  # очередность игроков

    def hit_check(self, shot, other_player,moving_player):
        for ship in other_player.ships:
            if shot in ship.coords:
                if ship.hit():
                    other_player.ships_destrou.append(1)
                    for i in ship.aura:
                        if other_player.board.move_in_board(i) or i in ship.coords:
                            continue
                        else:
                            moving_player.board.radar[shot.x][shot.y] = "X"
                            other_player.board.grid[shot.x][shot.y] = "X"
                            moving_player.board.radar[i.x][i.y] = "0"
                            other_player.board.grid[i.x][i.y] = "0"
                    if other_player == self.player_2:
                        print(f"Игрок уничтожил корабль компьютера")
                    else:
                        print(f"Компьютер уничтожил корабль игрока")
                    return True

                else:
                    moving_player.board.radar[shot.x][shot.y] = "X"
                    other_player.board.grid[shot.x][shot.y] = "X"
                    if other_player == self.player_2:
                        print(f"Игрок поразил корабль компьютера")
                    else:
                        print(f"Компьютер поразил корабль игрока")
                return True

        if other_player == self.player_1:  # в случае промаха
            moving_player.board.radar[shot.x][shot.y] = "O"
            other_player.board.grid[shot.x][shot.y] = "O"
            if other_player == self.player_2:
                print(f"Вы промазали{shot}")
            else:
                print(f"Компьютер промазал{shot}")
        return False

    def move(self):  # основной цикл ходов
        random.shuffle(self.players)  # перед началом игры перемешивает список с игроками для выбора первого кто ходит
        moving_player, other_player = self.players[0], self.players[1]
        while True:
            print("-" * 100)
            print("Поле противника(компьютер)")
            self.player_1.board.empty_fild()
            print("Ваше поле")
            self.player_1.board.fild()
            if len(self.player_1.ships_destrou) == 7:
                print("Поле противника(компьютер)")
                self.player_2.board.fild()
                print("Ваше поле")
                self.player_1.board.fild()
                print("Компьютер победил")
                return True
            elif len(self.player_2.ships_destrou) == 7:
                print("Поле противника(компьютер)")
                self.player_2.board.fild()
                print("Ваше поле")
                self.player_1.board.fild()
                print("Игрок победил")
                return True
            else:
                shot = moving_player.make_move()
                if self.hit_check(shot, other_player, moving_player):
                    continue
                else:
                    if moving_player == self.player_1:
                        moving_player, other_player = self.player_2, self.player_1
                    else:
                        moving_player, other_player = self.player_1, self.player_2


def start_game():  # я не знаю зачем это существует, но пусть будет
    game = Game_Сontroler()
    game.move()


start_game()