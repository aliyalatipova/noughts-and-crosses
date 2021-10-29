import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from typing import Callable


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.boats = list()
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Азбука морзе 2')

        abc = list('abcdefghij')
        # создание своего поля
        self.buttons = list()
        size_btn = 25
        for stolb in range(len(abc)):
            n_st = abc[stolb]
            group = list()
            for i in range(10):
                # n_st + str(i)
                self.btn = QPushButton('', self)
                self.btn.resize(size_btn, size_btn)
                self.btn.move((i + 1) * size_btn, (stolb + 1) * size_btn)
                group.append(self.btn)
            self.buttons.append(group)
        #
        self.btn_make_boat = QPushButton('создать', self)
        self.btn_make_boat.clicked.connect(self.make_boat)
        self.btn_make_boat.move(195, 280)

        self.edit_xy = QLineEdit(self)
        self.edit_xy.move(260, 0)

        for st in range(len(abc)):
            self.lbl = QLabel(self)
            self.lbl.setText(abc[st])
            self.lbl.move(18, (st + 1) * 25 + 5)

        for i in range(10):
            self.lbl = QLabel(self)
            self.lbl.setText(str(i))
            self.lbl.move((i + 1) * size_btn + 7, 14)

        # создание поля противника
        self.buttons_pr = list()
        for st in range(len(abc)):
            group = list()
            for i in range(10):
                self.btn = QPushButton('', self)
                self.btn.resize(size_btn, size_btn)
                self.btn.move((i + 1) * size_btn + 350, (st + 1) * size_btn)
                group.append(self.btn)
            self.buttons_pr.append(group)

        for st in range(len(abc)):
            self.lbl = QLabel(self)
            self.lbl.setText(abc[st])
            self.lbl.move(365, (st + 1) * 25)

        for i in range(10):
            self.lbl = QLabel(self)
            self.lbl.setText(str(i))
            self.lbl.move((i + 1) * size_btn + 360, 13)

        for j in range(10):
            for i in range(10):
                self.buttons[j][i].clicked.connect(self.some_gen(j, i))

        # 100500 переменных
        self.some = ['0000000000' for i in range(10)]
        self.count = 0
        self.four = list()
        self.three = list()
        self.two = list()
        self.one = list()
        self.but_of_boat = list()


    def some_gen(self, j: int, i: int) -> Callable:
        def some():
            print(j, i)
            color = '#ff007f'
            self.boats.append([j, i])
            self.but_of_boat.append([j, i])
            self.buttons[j][i].setStyleSheet("background-color: {}".format(color))
        return some


    def make_boat(self):
        # проверка на подряд и в одном ряду
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())