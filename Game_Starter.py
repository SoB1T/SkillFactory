Xzero = {
    11: "-", 21: "-", 31: "-",
    12: "-", 22: "-", 32: "-",
    13: "-", 23: "-", 33: "-"
}  # обьявляю словарь игровое поле для использования его как глобальной переменной
Player_move = set()  # множество с ходами игроков
Rules = f"Первый, выстроивший в ряд 3 своих фигуры по вертикали, горизонтали или большой диагонали, выигрывает. Если " \
        f"\nигроки заполнили все 9 ячеек и оказалось, что ни в одной вертикали, " \
        f"\nгоризонтали или большой диагонали нет " \
        f"\nтрёх одинаковых знаков, партия считается закончившейся в ничью." \
        f"\nПоле координат выглядит следующим образом:" \
        f"\n11 21 31 " \
        f"\n12 22 32" \
        f"\n13 23 33"

Reference = f"\nИгра крестики нолики" \
            f"\nНаписана: SoB вкачестве практической работы для курса Python разработчик" \
            f"\n на оброзовательной платформе SkillFactory"


def XO():  # обьявление игры
    print("Игра крестики нолики")
    global Xzero

    def game_start():
        keyw = input("Введите S для начала игры, R для получения правил или Ref для получения справки")
        if keyw == "S":
            pass
        elif keyw == "R":
            print(Rules)
            game_start()
        elif keyw == "Ref":
            print(Reference)
            game_start()
        else:
            game_start()

    game_start()
    count = 1  # счетчик ходов
    while count < 10:  # цыкл для обьявления ничьей и счета ходов

        def player_changer():  # на основе хода определяет какой игрок ходит, а также его символ.
            nonlocal count
            if count % 2 == 0:  # нолик ходит на четных ходах
                player = {'name': 'Нолик', 'symbol': 'O'}
            else:
                player = {'name': 'Крест', 'symbol': 'X'}  # крестик на нечетных
            return player

        player = (player_changer())  # для удобства присваиваем переменной player результат работы player_changer

        def symbol_changer():  # функция изменяющая символ на игровом поле
            def field():  # функция для вывода игрового поля
                global Xzero
                nonlocal count
                print(f"Ход {count} "
                      f"\n{Xzero[11], Xzero[21], Xzero[31]}"
                      f"\n{Xzero[12], Xzero[22], Xzero[32]}"
                      f"\n{Xzero[13], Xzero[23], Xzero[33]}")

            field()
            global Player_move
            global Xzero
            x = int(input(f"Ход игрока {player['name']}"))
            if x not in Xzero:  # защита от некоректной позиций
                print("Вы выбрали некоректную позицию")
                symbol_changer()
            elif x in Player_move:
                print("Вы выбрали занятую позицию")
                x = None  # костыль для того чтобы при вводе верной позиций игрок не изменил несколько символов
                symbol_changer()
            else:
                pass
            Player_move.add(x)  # добавляем одобренный ход в список ходов
            Xzero.update({x: player['symbol']})  # обновляем символ на поле

        def winner_chekcer():  # проверка на победу
            global Xzero
            win_count = 20  # число для прибавления к счетчику ходов в случае победы
            if "X" in Xzero[11] and "X" in Xzero[22] and "X" in Xzero[33] or "O" in Xzero[11] and "O" in Xzero[
                22] and "O" in Xzero[33]:
                print("У нас победитель!")  # искос верх вправо низ лево
                return win_count
            elif "X" in Xzero[11] and "X" in Xzero[12] and "X" in Xzero[13] or "O" in Xzero[11] and "O" in Xzero[
                12] and "O" in Xzero[13]:
                print("У нас победитель!")  # колона1
                return win_count
            elif "X" in Xzero[21] and "X" in Xzero[22] and "X" in Xzero[23] or "O" in Xzero[21] and "O" in Xzero[
                22] and "O" in Xzero[23]:
                print("У нас победитель!")  # колона2
                return win_count
            elif "X" in Xzero[31] and "X" in Xzero[32] and "X" in Xzero[33] or "O" in Xzero[31] and "O" in Xzero[
                32] and "O" in Xzero[33]:
                print("У нас победитель!")  # колона3
                return win_count
            elif "X" in Xzero[11] and "X" in Xzero[21] and "X" in Xzero[31] or "O" in Xzero[11] and "O" in Xzero[
                21] and "O" in Xzero[31]:
                print("У нас победитель!")  # ряд1
                return win_count
            elif "X" in Xzero[12] and "X" in Xzero[22] and "X" in Xzero[32] or "O" in Xzero[12] and "O" in Xzero[
                22] and "O" in Xzero[32]:
                print("У нас победитель!")  # ряд2
                return win_count
            elif "X" in Xzero[13] and "X" in Xzero[23] and "X" in Xzero[33] or "O" in Xzero[13] and "O" in Xzero[
                23] and "O" in Xzero[33]:
                print("У нас победитель!")  # ряд3
                return win_count
            elif "X" in Xzero[31] and "X" in Xzero[22] and "X" in Xzero[13] or "O" in Xzero[31] and "O" in Xzero[
                22] and "O" in Xzero[13]:
                print("У нас победитель!")  # искос верх лево низ право
                return win_count
            else:
                win_count = 0  # обнуление счетчика костыль чтобы функция возвращала не None
                return win_count

        winner_chekcer()  # в первую очередь проверяю на наличие победы и только потом позволяю сделать ход
        symbol_changer()
        count += winner_chekcer()  # причина существования костыля на 84 строке
        if count > 19:  # проверяем победу и определяем победителя
            if count % 2 == 0:  # поскольку проверка победы идет до обновления счетчика проверяем четность
                print("Победил НОЛИК")
                print(f"\n{Xzero[11], Xzero[21], Xzero[31]}"
                      f"\n{Xzero[12], Xzero[22], Xzero[32]}"
                      f"\n{Xzero[13], Xzero[23], Xzero[33]}")
            else:
                print("Победил КРЕСТИК")
                print(f"\n{Xzero[11], Xzero[21], Xzero[31]}"
                      f"\n{Xzero[12], Xzero[22], Xzero[32]}"
                      f"\n{Xzero[13], Xzero[23], Xzero[33]}")
            break
        else:
            None
        count += 1
    if count == 10:  # проверка на ничью
        print("Ничья")
        print(f"\n{Xzero[11], Xzero[21], Xzero[31]}"
              f"\n{Xzero[12], Xzero[22], Xzero[32]}"
              f"\n{Xzero[13], Xzero[23], Xzero[33]}")
    else:
        None
    Player_move = set()  # обнуляем ходы игрока
    Xzero = {
        11: "-", 21: "-", 31: "-",
        12: "-", 22: "-", 32: "-",
        13: "-", 23: "-", 33: "-"
    }  # отчищаем поле
    print("Для начала новой игры вновь используйте команду XO()")
