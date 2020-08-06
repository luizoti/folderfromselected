#!/usr/bin/python3

import sys
from os.path import basename, splitext
from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QLineEdit
 
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Criar Pasta'

        self.width = 800
        self.height = 400

        self.left = round(int((size.width() - self.width)/ 2))
        self.top = round(int((size.height() - self.height + 40) / 2))
        # 
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.list = QListWidget()
        self.initUI()


    def initUI(self):
        count = 0
        for filename in sys.argv:
            if not sys.argv[0] == filename:
                self.list.insertItem(count, basename(filename).split('.')[0])
                count + 1
                pass
            pass

        self.list.clicked.connect(self.listview_clicked)
        self.vbox.addWidget(self.list)

        self.button = QPushButton('Criar Pasta!')
        self.textbox = QLineEdit()
        self.pasta = QLabel('Pasta:')
        self.hbox.addWidget(self.textbox)
        self.hbox.addSpacing(10)
        self.hbox.addWidget(self.button)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.pasta)
        self.setLayout(self.vbox)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


    def listview_clicked(self):
        item = self.list.currentItem()
        textboxValue = str(item.text())
        self.textbox.setText(textboxValue)


# def makelist(self):


# # def editname(self):

# #     pass


# # def makedir(self):
# #     pass
  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()

    ex = App()
    sys.exit(app.exec_())
    