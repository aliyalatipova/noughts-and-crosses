import sys

from random import choice, randrange
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QInputDialog
from typing import Callable
import work_bd

ABC = list('abcdefghij')
SIZE_BTN = 25
BLACK = "#000000"
FIELD_COLOR = '#e3ff89'


class Sea_fight(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 700, 500)
        self.setWindowTitle('one')

        self.start()

        self.name = QLineEdit(self)
        self.name.move(260, 300)

        self.edit_xy = QLineEdit(self)
        self.edit_xy.move(260, 0)

        self.make_variables()
        self.my_field()
        self.enemy_field()
        self.select_ships()

    def start(self):
        self.btn_make_boat = QPushButton('создать', self)
        self.btn_make_boat.clicked.connect(self.make_twelve)
        self.btn_make_boat.move(195, 280)

    def make_variables(self):
        self.all_flags = list()
        # координты клеток в которых находятся корабли пользователя
        self.boats = list()
        self.four = list()
        self.three = list()
        self.two = list()
        self.one = list()
        self.ships = list()

    def restart(self):
        pass

    def enemy_field(self):
        # создание поля противника
        self.buttons_pr = list()
        for st in range(len(ABC)):
            group = list()
            for i in range(10):
                self.btn = QPushButton('', self)
                self.btn.resize(SIZE_BTN, SIZE_BTN)
                self.btn.move((i + 1) * SIZE_BTN + 350, (st + 1) * SIZE_BTN)
                group.append(self.btn)
            self.buttons_pr.append(group)

        for st in range(len(ABC)):
            self.lbl = QLabel(self)
            self.lbl.setText(ABC[st])
            self.lbl.move(365, (st + 1) * 25)

        for i in range(10):
            self.lbl = QLabel(self)
            self.lbl.setText(str(i))
            self.lbl.move((i + 1) * SIZE_BTN + 360, 13)


    def my_field(self):
        # создание своего поля
        self.buttons = list()
        for stolb in range(len(ABC)):
            # ln_st = ABC[stolb]
            group = list()
            for i in range(10):
                self.btn = QPushButton('', self)
                self.btn.resize(SIZE_BTN, SIZE_BTN)
                self.btn.move((i + 1) * SIZE_BTN, (stolb + 1) * SIZE_BTN)
                group.append(self.btn)
                self.btn.setStyleSheet(
                        "background-color: {}".format(FIELD_COLOR))
            self.buttons.append(group)
        for st in range(len(ABC)):
            self.lbl = QLabel(self)
            self.lbl.setText(ABC[st])
            self.lbl.move(18, (st + 1) * 25 + 5)

        for i in range(10):
            self.lbl = QLabel(self)
            self.lbl.setText(str(i))
            self.lbl.move((i + 1) * SIZE_BTN + 7, 14)


    def select_ships(self):
        print('select ships')
        for j in range(10):
            for i in range(10):
                self.buttons[j][i].clicked.connect(self.some_gen(j, i))


    def some_gen(self, j: int, i: int) -> Callable:
        def some():
            PINK = '#ff007f'
            if [j, i] in self.boats:
                self.boats.remove([j, i])
                self.buttons[j][i].setStyleSheet("background-color: {}".format(FIELD_COLOR))
            else:
                self.buttons[j][i].setStyleSheet("background-color: {}".format(PINK))
                self.boats.append([j, i])

        return some



    def make_twelve(self):
        # создается список с 12 строками, в каждой строке 12 нулей
        # в тех координатах где есть корабль ставится вместо нуля 1
        if len(self.boats) != 20:
            self.flag = False
        self.boats.sort()
        self.twelve = list()
        self.twelve.append('000000000000')
        for j in range(10):
            line = list()
            line.append('0')
            for i in range(10):
                if [j, i] in self.boats:
                    line.append('1')
                else:
                    line.append('0')
            line.append('0')
            line = ''.join(line)
            self.twelve.append(line)
        self.step_two()

    def step_two(self):
        self.search4()
        self.search3()
        self.search2()
        self.search1()
        self.check_field()

    def who_starts(self):
        begin, ok_pressed = QInputDialog.getItem(
            self, "Кто начинает игру", "Кто начинает игру?",
            ("Я", "Мой противник", "Выбрать автоматически"), 1, False)
        if begin == "Выбрать автоматически":
            begin = choice(['Я', 'Мой противник'])
        if begin == 'Я':
            self.my_move()
        elif begin == 'Мой противник':
            self.opponent_move()

    def my_move(self):
        self.edit_xy.setText('my move')

        for j in range(10):
            for i in range(10):
                self.buttons_pr[j][i].clicked.connect(self.my_choice(j, i))


    def my_choice(self, j: int, i: int) -> Callable:
        def some():
            move = [j + 1, i + 1]

            if move in self.my_moves:
                self.my_move()
            else:
                print('self.donald')
                print(self.donald)
                print('self.enemy_ships')
                print(self.enemy_ships)
                self.my_moves.append(move)
                print('мой ход')
                print([[j + 1, i + 1]])
                if [j + 1, i + 1] in self.enemy_buttons:
                    self.buttons_pr[j][i].setStyleSheet("background-color: {}".format(BLACK))

                    if [[j + 1, i + 1]] in self.donald:
                        self.i_killed += 1
                        print('я убил')
                        print(self.enemy_ships)
                        for ship in self.enemy_ships:
                            if [j + 1, i + 1] in ship:
                                print(ship)
                                for btn in self.around_one_ship(ship):
                                    try:
                                        self.buttons_pr[btn[0] - 1][btn[1] - 1].setText('*')
                                    except IndexError:
                                        print('IndexError')
                                        print(btn[0] - 1, btn[1] - 1)
                                        print(move)
                    else:
                        list1 = list()
                        # list2 = list()
                        for x in self.donald:
                            if [j + 1, i + 1] in x:
                                x.remove([j + 1, i + 1])
                                list1.append(x)
                            else:
                                list1.append(x)
                        self.donald = list1
                        print(' ранил')

                else:
                    print('я промахнулся')
                    self.buttons_pr[j][i].setText('-')

                if self.check_game():
                    self.opponent_move()
        return some

    def opponent_move(self):
        self.edit_xy.setText("opponent's move")
        # НАДО ВЕРНУТЬ ЭТУ СТРОКУ
        move = choice(self.list_to_go)
        self.list_to_go.remove(move)
        if [move[0] - 1, move[1] - 1] in self.boats:
            self.buttons[move[0] - 1][move[1] - 1].setStyleSheet("background-color: {}".format(BLACK))
            # print(self.kesha)
            if [move] in self.kesha:
                print('комп убил')
                self.comp_killed += 1
                for ship in self.ships:
                    if move in ship:
                        around_ship = self.around_one_ship(ship)
                        print(around_ship)
                        for btn in around_ship:
                            if btn[0] != 0 and btn[1] != 0:
                                if btn in self.list_to_go:
                                     self.list_to_go.remove(btn)
                            self.buttons[btn[0] - 1][btn[1] - 1].setText('*')
            else:
                # удаляем из списка с кораблями координату той, на которую сделали ход
                list1 = list()
                for x in self.kesha:
                    if move in x:
                        x.remove(move)
                    else:
                        list1.append(x)
                self.kesha = list1
                print('комп ранил(')
        else:
            print('жаль комп')
            self.buttons[move[0] - 1][move[1] - 1].setText('-')
        if self.check_game():
            self.my_move()

    def check_game(self):
        if self.i_killed >= 10:
            return False
        elif self.comp_killed >= 10:
            return False
        else:
            return True

    def end_of_game(self):
        if self.i_killed >= 10:
            self.edit_xy.setText('ВЫ победили')
        else:
            self.edit_xy.setText('Компьютер победил')

    def search1(self):
        for b in range(4):
            a = self.twelve
            n = 1
            some = list()
            # по горизонтали
            for j in range(len(a)):
                for i in range(12 - n):
                    if a[j][i] == '1':
                        some = [[j, i]]
                        print(j, i)
            # по вертикали
            if len(some) == 0:
                for j in range(11 - n):
                    for i in range(len(a)):
                        if a[j][i] == '1':
                            some = [[j, i]]
            if len(some) > 0:
                self.one.append(some)
            self.ships.append(some)
            #
            self.n_around(some)
            self.change(some)

    def search2(self):
        for ship in range(3):
            a = self.twelve
            n = 2
            some = list()
            # по горизонтали
            for j in range(len(a)):
                for i in range(12 - n):
                    if a[j][i] == a[j][i + 1] and a[j][i] == '1':
                        some = [[j, i], [j, i + 1]]
                        print(j, i)
            # по вертикали
            if len(some) == 0:
                for j in range(12 - n):
                    for i in range(len(a)):
                        if a[j][i] == a[j + 1][i] and a[j][i] == '1':
                            some = [[j, i], [j + 1, i]]
            if len(some) > 0:
                self.two.append(some)
            self.ships.append(some)
            #
            self.n_around(some)
            self.change(some)


    def search3(self):
        for ship in range(2):
            a = self.twelve
            n = 3
            some = list()
            # по горизонтали
            for j in range(len(a)):
                for i in range(12 - n):
                    if a[j][i] == a[j][i + 1] and a[j][i + 2] == '1':
                        if a[j][i] == '1':
                            some = [[j, i], [j, i + 1], [j, i + 2]]
                            print(j, i)
            # по вертикали
            if len(some) == 0:
                for j in range(11 - n):
                    for i in range(len(a)):
                        if a[j][i] == a[j + 1][i] and a[j + 2][i] == '1':
                            if a[j][i] == '1':
                                some = [[j, i], [j + 1, i], [j + 2, i]]
            if len(some) > 0:
                self.three.append(some)
            self.ships.append(some)
            #
            self.n_around(some)
            self.change(some)

    def search4(self):
        # в результате выполнения этой функции мы получаем координаты корабля на 4 клетки
        a = self.twelve
        n = 4
        some = list()
        # по горизонтали
        for j in range(len(a)):
            for i in range(12 - n):
                if a[j][i] == a[j][i + 1] and a[j][i + 2] == a[j][i + 3]:
                    if a[j][i] == '1' and a[j][i + 3] == '1':
                        some = [[j, i], [j, i + 1], [j, i + 2], [j, i + 3]]
        # по вертикали
        if len(some) == 0:
            for j in range(11 - n):
                for i in range(len(a)):
                    if a[j][i] == a[j + 1][i] and a[j + 2][i] == a[j + 3][i]:
                        if a[j][i] == '1' and a[j + 3][i] == '1':
                            some = [[j, i], [j + 1, i], [j + 2, i], [j + 3, i]]
        if len(some) > 0:
            self.four.append(some)
        self.ships.append(some)
        #
        self.n_around(some)
        self.change(some)


    def change(self, list1):
        # функция должна будет сделать замену елементам списка в в списке на 2
        for x in list1:
            for j in range(12):
                if j == x[0]:
                    some = self.twelve[j][:x[1]] + '2' + self.twelve[j][x[1] + 1:]
                    twelve1 = list()
                    twelve1.extend(self.twelve[:j])
                    twelve1.append(some)
                    twelve1.extend(self.twelve[j + 1:])
                    self.twelve = twelve1


    def n_around(self, ship_xy):
        # эта фуенция создает список с координатами вокруг ОДНОГО корабля
        list1 = list()
        for x in ship_xy:
            list1.append([x[0] - 1, x[1] - 1])
            list1.append([x[0], x[1] - 1])
            list1.append([x[0] - 1, x[1]])
            list1.append([x[0] - 1, x[1] + 1])
            list1.append([x[0] + 1, x[1] - 1])
            list1.append([x[0] + 1, x[1]])
            list1.append([x[0], x[1] + 1])
            list1.append([x[0] + 1, x[1] + 1])
        list2 = [x for x in list1 if x not in ship_xy]
        list2.sort()

        self.check_0(list2)


    def check_0(self, xy_around):
        # функция проверят
        fl = True
        xy_around1 = [x for x in xy_around if (x[0] != 0) and (x[1] != 0)]
        for x in xy_around1:
            try:
                if self.twelve[x[0]][x[1]] != '0':
                    fl = False
                    break
            except IndexError:
                pass

        self.all_flags.append(fl)

    def check_field(self):
        flag1 = True
        for flag in self.all_flags:
            if not flag:
                flag1 = False
                break
        flag2 = (len(self.one) == 4 and len(self.two) == 3 and len(self.three) == 2 and len(self.four) == 1)
        if flag2 and flag1:
            self.btn_make_boat.setText('true')
            for x in self.ships:
                print(x)
            self.make_enemy_boats()
            self.who_starts()
        else:
            self.btn_make_boat.setText('false')

    def make_variables_pr(self):
        self.enemy_ships = list()
        self.enemy_buttons = list()
        self.enemy_around = list()
        self.list_to_go = self.make_list_to_go()
        # из кеши я буду удалять корабли
        self.kesha = self.ships
        self.i_killed = 0
        self.comp_killed = 0
        self.my_moves = list()

    def make_list_to_go(self):
        to_go = list()
        for j in range(1, 11):
            for i in range(1, 11):
                to_go.append([j, i])
        return to_go

    def make_enemy_boats(self):
        self.make_variables_pr()
        self.make_boat4()
        self.make_boat3()
        self.make_boat2()
        self.make_boat1()
        # self.enemy_ships_not_changed = self.enemy_ships
        self.donald = self.enemy_ships

    def make_boat4(self):
        a = choice(['вертикально', 'горизонтально'])
        if a == 'вертикально':
            j = n_row = randrange(1, 8)
            i = n_column = randrange(1, 11)
            boat = [[j, i], [j + 1, i], [j + 2, i], [j + 3, i]]
        else:
            j = n_row = randrange(1, 11)
            i = n_column = randrange(1, 8)
            boat = [[j, i], [j, i + 1], [j, i + 2], [j, i + 3]]
        around_b4 = self.around_one_ship(boat)
        self.enemy_buttons.extend(boat)
        self.enemy_around.extend(around_b4)
        self.enemy_ships.append(boat)

    def around_one_ship(self, ship_xy):
        # возвращает клетки вокруг корабля
        list1 = list()
        for x in ship_xy:
            # в одном выаолнении списка в list1 добавляются координаты клеток вокруг одной из клеток корабля
            list1.append([x[0] - 1, x[1] - 1])
            list1.append([x[0], x[1] - 1])
            list1.append([x[0] - 1, x[1]])
            list1.append([x[0] - 1, x[1] + 1])
            list1.append([x[0] + 1, x[1] - 1])
            list1.append([x[0] + 1, x[1]])
            list1.append([x[0], x[1] + 1])
            list1.append([x[0] + 1, x[1] + 1])
        list2 = [x for x in list1 if x not in ship_xy]
        list2.sort()
        return list2

    def make_boat3(self):
        # количество кораблей с длиной три
        for ship in range(2):
            while True:
                a = choice(['вертикально', 'горизонтально'])
                if a == 'вертикально':
                    j = n_row = randrange(1, 9)
                    i = n_colum = randrange(1, 11)
                    boat = [[j, i], [j + 1, i], [j + 2, i]]
                else:
                    j = n_row = randrange(1, 11)
                    i = n_column = randrange(1, 9)
                    boat = [[j, i], [j, i + 1], [j, i + 2]]
                around3 = self.around_one_ship(boat)
                # с помощью этого флага будет сделана проверка наличия вокруг корабля других кораблей
                flag = self.examination(boat, around3)
                if flag:
                    self.enemy_buttons.extend(boat)
                    self.enemy_ships.append(boat)
                    self.enemy_around.extend(around3)
                    break

    def make_boat2(self):
        for ship in range(3):
            while True:
                a = choice(['вертикально', 'горизонтально'])
                if a == 'вертикально':
                    j = n_row = randrange(1, 10)
                    i = n_colum = randrange(1, 11)
                    boat = [[j, i], [j + 1, i]]
                else:
                    j = n_row = randrange(1, 11)
                    i = n_column = randrange(1, 10)
                    boat = [[j, i], [j, i + 1]]
                around2 = self.around_one_ship(boat)
                # с помощью этого флага будет сделана проверка наличия вокруг корабля других кораблей
                flag = self.examination(boat, around2)
                if flag:
                    self.enemy_buttons.extend(boat)
                    self.enemy_around.extend(around2)
                    self.enemy_ships.append(boat)
                    break

    def make_boat1(self):
        for ship in range(4):
            while True:
                a = choice(['вертикально', 'горизонтально'])
                if a == 'вертикально':
                    j = n_row = randrange(1, 11)
                    i = n_colum = randrange(1, 11)
                    boat = [[j, i]]
                else:
                    j = n_row = randrange(1, 11)
                    i = n_column = randrange(1, 11)
                    boat = [[j, i]]
                around1 = self.around_one_ship(boat)
                # с помощью этого флага будет сделана проверка наличия вокруг корабля других кораблей
                flag = self.examination(boat, around1)
                if flag:
                    self.enemy_buttons.extend(boat)
                    self.enemy_around.extend(around1)
                    self.enemy_ships.append(boat)
                    break

    def examination(self, boat, around):
        flag = True
        for btn in around:
            if btn in self.enemy_buttons:
                flag = False
                break
        for btn in boat:
            if (btn in self.enemy_buttons) or (btn in self.enemy_around):
                flag = False
                break
        return flag


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Sea_fight()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())