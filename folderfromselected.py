#!/usr/bin/python3

import sys
from os.path import basename
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QListWidget, QVBoxLayout
 
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Criar Pasta'

        self.width = 480
        self.height = 680 - 40

        self.left = round(int((size.width() - self.width) / 2))
        self.top = round(int((size.height() - self.height) / 2))
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,
                         self.top, 
                         self.width, 
                         self.height)

        vbox= QVBoxLayout()
        self.list = QListWidget()

        count = 0

        for filename in categorize(sys.argv):
            if not sys.argv[0] == filename:
                self.list.insertItem(count, basename(filename))
                count + 1
                pass
            pass

        self.list.clicked.connect(self.listview_clicked)
        vbox.addWidget(self.list)
        self.label = QLabel()
        self.label.setFont(QtGui.QFont("Sanserif", 15))
        vbox.addWidget(self.label)
        self.setLayout(vbox)
        self.show()


    def listview_clicked(self):
        item = self.list.currentItem()
        self.label.setText(str(item.text()))


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
    