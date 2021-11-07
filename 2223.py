import sys

from random import choice
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QInputDialog
from typing import Callable

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

        self.btn_make_boat = QPushButton('создать', self)
        self.btn_make_boat.clicked.connect(self.make_twelve)
        self.btn_make_boat.move(195, 280)

        self.btn_restart = QPushButton('начать сначала', self)
        self.btn_restart.clicked.connect(self.restart)
        self.btn_restart.move(195, 300)


        self.edit_xy = QLineEdit(self)
        self.edit_xy.move(260, 0)

        self.make_variables()
        self.my_field()
        self.enemy_field()
        self.select_ships()


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
        for j in range(10):
            for i in range(10):
                self.buttons[j][i].setStyleSheet("background-color: {}".format(FIELD_COLOR))
        self.make_variables()
        self.select_ships()

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
        # self.btn_make_boat.clicked.connect(self.who_starts)


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
                self.buttons_pr[j][i].clicked.connect(self.some_gen1(j, i))


    def some_gen1(self, j: int, i: int) -> Callable:
        def some1():
            self.buttons_pr[j][i].setText('.')
            self.asking_answer(j, i)
        return some1

    def asking_answer(self, j, i):
        answer, ok_pressed = QInputDialog.getItem(
            self, "Ответ противника", "Ответ вашего противника",
            ("Убил", "Мимо", "Ранил"), 1, False)
        if answer != 'Мимо':
            self.buttons_pr[j][i].setStyleSheet("background-color: {}".format(BLACK))
            if answer == 'Ранил':
                self.opponent_move()
            if answer == 'Убил':
                self.i_killed(j, i)
                list3 = [[j - 1, i - 1], [j - 1, i], [j - 1, i + 1], [j, i - 1], [j, i + 1],
                            [j + 1, i - 1], [j + 1, i], [j + 1, i + 1]]
                list4 = [x for x in list3 if (x[0] != 0 and x[1] != 0)]
                # в list4 координаты клеток вокруг убитой
                for x in list4:
                    self.buttons_pr[x[0]][x[1]].setText('.')
        self.opponent_move()

    def i_killed(self, j, i):
        pass

    def i_hurt(self):
        pass

    def opponent_move(self):
        self.edit_xy.setText("opponent's move")
        print(self.boats)
        print(self.ships)
        for j in range(10):
            for i in range(10):
                self.buttons[j][i].clicked.connect(self.some_gen2(j, i))

    def some_gen2(self, j: int, i: int) -> Callable:
        def some2():
            if [j, i] in self.boats:
                self.buttons[j][i].setStyleSheet("background-color: {}".format(BLACK))
                list5 = list()
                # изменяется self.boats
                for x in self.ships:
                    if [j, i] in x:
                        x1 = [a for a in x if a != [j, i]]
                        list5.append(x1)
                    else:
                        list5.append(x)
                self.boats = list5
                if [[j + 1, i + 1]] in self.ships:
                    print([[j + 1, i + 1]])
                    self.btn_make_boat.setText('убил')
            else:
                self.buttons_pr[j][i].setText('.')
            self.my_move()
        return some2


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
                for j in range(11 - n):
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
        print(fl)

    def check_field(self):

        flag1 = True
        for flag in self.all_flags:
            if not flag:
                flag1 = False
                break
        print(len(self.one), len(self.two), len(self.three), len(self.four))
        flag2 = (len(self.one) == 4 and len(self.two) == 3 and len(self.three) == 2 and len(self.four) == 1)
        print(flag1, flag2)
        if flag2 and flag1:
            self.btn_make_boat.setText('true')
            self.who_starts()
        else:
            self.btn_make_boat.setText('false')
            self.idk()

    def idk(self):
        for j in range(10):
            for i in range(10):
                self.buttons[j][i].clicked.connect(self.make_pink(j, i))

    def make_pink(self, j: int, i: int) -> Callable:
        def pink():
            PINK = '#ff007f'
            if [j, i] in self.boats:
                pass
                #self.boats.remove([j, i])
                # self.buttons[j][i].setStyleSheet("background-color: {}".format(FIELD_COLOR))
            else:
                self.buttons[j][i].setStyleSheet("background-color: {}".format(PINK))
                self.boats.append([j, i])

        return pink



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Sea_fight()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())