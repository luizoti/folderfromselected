#!/usr/bin/python3

import sys
import argparse
from os.path import basename
from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QLineEdit
 
parser = argparse.ArgumentParser(description='Create folder from selected files!')

parser.add_argument('-g', '--gui', action='store_true', help='gui create folder')
parser.add_argument('-f', '--fast', action='store_true', help='fast create folder')
parser.add_argument('list', nargs='+', help='Set flag')
args = parser.parse_args()


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Criar Pasta'

        self.width = 800
        self.height = 400

        self.left = round(int((size.width() - self.width)/ 2))
        self.top = round(int((size.height() - self.height + 40) / 2))
        # 
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.list = QListWidget()
        self.parseArgs()


    def parseArgs(self):
        self.filelist = args.list
        try:
            if args.gui is True and len(self.filelist) > 0:
                print('gui: ', self.filelist)
                self.initUI()
            elif args.fast is True and len(self.filelist) > 0:
                print('fast: ', self.filelist)
                pass
        except Exception:
            pass


    def initUI(self):
        count = 0
        for filename in reversed(self.filelist):
            self.list.insertItem(count, basename(filename).split('.')[0])
            count + 1
            pass

        self.list.clicked.connect(self.listview_clicked)
        self.list.itemSelectionChanged.connect(self.listview_clicked)
        self.vbox.addWidget(self.list)

        self.button = QPushButton('Criar Pasta!')
        self.textbox = QLineEdit()
        self.button.clicked.connect(self.makelist)
        self.pasta = QLabel('Pasta: ')
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


    def makelist(self):
        item = self.list.currentItem()
        textboxValue = str(item.text())
        print(textboxValue)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()

    ex = App()
    sys.exit(app.exec_())
    