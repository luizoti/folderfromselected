#!/usr/bin/python3

import os
from os.path import join, basename

import argparse

from PyQt5.Qt import QDir
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeyEvent, QIcon, QKeySequence

from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QCheckBox, QLineEdit, QTreeView, QFileDialog, QShortcut
from PyQt5.QtWidgets import QLabel

from filemanager import FilesManager

parse = argparse.ArgumentParser(description='Create folder from selected files:')
parse.add_argument('-f', '--filelist', nargs='+', metavar='filelist', help='CMD create folder', required=True)
args = parse.parse_args()

current_dir = os.path.dirname(os.path.realpath(__file__))
# # # 
# # # 
def GetIcon(iconame):
    return QIcon(join(current_dir, 'icos', iconame))

class CurrentResolution(QDesktopWidget):
    def __init__(self):
        QDesktopWidget.__init__(self)
        self.screenGeometry(-1)
        self.height()
        self.width()

class ButtonsLayout(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)
        self.clear = QPushButton('Limpar')
        self.create = QPushButton('Criar')

        self.addWidget(self.clear)
        self.addWidget(self.create)

class NewPathBox(QLineEdit):
    def __init__(self, parent):
        super(NewPathBox, self).__init__(parent)
        self.parentWindow = parent
        self.label = 'Digite o caminho para mover a pasta'
        self.setPlaceholderText(self.label)
        self.setStyleSheet("color: #7d7d7d")
        self.setEnabled(False)

        self.SearchBtnInside = QPushButton()
        self.SearchBtnInside.setIcon(GetIcon('find.svg'))
        # self.SearchBtnInside.setFixedSize(30, 30)
        self.SearchBtnInside.setStyleSheet('');
        self.SearchBtnInside.setCursor(Qt.ArrowCursor)
        self.SearchBtnInside.setEnabled(True)
        self.SearchBtnInside.clicked.connect(self.folderdiag)

        self.lay = QHBoxLayout()
        self.lay.addStretch(1)
        self.lay.addWidget(self.SearchBtnInside)
        self.setLayout(self.lay)

    def folderdiag(self):
        diag = QFileDialog()
        diag.setDirectory(QDir.home())
        diag.setFileMode(QFileDialog.Directory)

        if diag.exec_():
            folder = diag.selectedFiles()[0]
            if folder != self.label:
                self.setText(folder)
                pass
            pass

    def EnablePathTextBox(self, state):
        if state is True:
            self.setEnabled(state)
            self.SearchBtnInside.setEnabled(state)
            self.setStyleSheet("color: white")
        elif state is False:
            self.setEnabled(state)
            self.SearchBtnInside.setEnabled(state)
            self.setStyleSheet("color: #7d7d7d")
            pass
        pass
        self.setPlaceholderText(self.label)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [16777234, 16777236] and self.label in self.text():
            self.setCursorPosition(0)
        else:
            super().keyPressEvent(event)
            pass
        self.parentWindow.keyPressEvent(event)


class FileTextbox(QLineEdit):
    def __init__(self, parent):
        super(FileTextbox, self).__init__(parent)
        self.parentWindow = parent
        self.label = 'Digite o nome da pasta'
        self.setPlaceholderText(self.label)
        self.setFixedWidth(480)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [16777234, 16777236] and self.label in self.text():
            self.setCursorPosition(0)
        else:
            super().keyPressEvent(event)
            pass
        self.parentWindow.keyPressEvent(event)


class ListWidget(QListWidget):
    def __init__(self):
        QHBoxLayout.__init__(self)
        self.injectItemToList()


    def injectItemToList(self):
        count = 0
        
        for filename in reversed(args.filelist):
            self.insertItem(count, basename(filename).split('.')[0])
            count + 1
            pass

    def current_selected(self):
        item = self.currentItem()
        return str(item.text())

class CheckBox(QCheckBox):
    def __init__(self):
        super(CheckBox, self).__init__()
        self.ChangeIco()
        self.stateChanged.connect(self.ChangeIco)
        

    def ChangeIco(self):
        if self.isChecked() is False:
            self.setIcon(GetIcon('lock.svg'))
        else:
            self.setIcon(GetIcon('unlock.svg'))
            pass
        pass

class AppGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.fm = FilesManager
        self.appSize() # App Dimensions and position 
        # self.setStyleSheet(open(join(current_dir, 'stylesheet.css'),"r").read())
        self.setWindowTitle('Create folder')
        self.setWindowIcon(GetIcon('folder.svg'))
        # Global Keys
        self.EnterKey = QShortcut(QKeySequence("Enter"), self)
        self.ExitKey = QShortcut(QKeySequence("Esc"), self)
        self.ExitKey.activated.connect(self.close)
        self.EnterKey.activated.connect(lambda: print("Hey Hey"))
        # Widgets
        self.checkMove = CheckBox()
        self.buttonlaybar = ButtonsLayout()
        self.listwidget  = ListWidget()
        self.filetextbox = FileTextbox(self)
        self.pathtextbox = NewPathBox(self)
        # Base Layouts
        self.primaryLayout = QVBoxLayout()
        self.subLayTextBoxHorizontal = QHBoxLayout()
        self.subLayTextPathHorizontal = QHBoxLayout()
        self.baseCMD()
        self.UIOrdererInit()
        self.show()
        

    def appSize(self):
        self.resolution = CurrentResolution()
        self.width, self.height = 500, 400
        self.left = round(int((self.resolution.width() - self.width)/ 2))
        self.top = round(int((self.resolution.height() - self.height + 40) / 2))
        self.setFixedSize(QSize(self.width, self.height))
        self.setGeometry(self.left, self.top, self.width, self.height)


    def baseCMD(self):
        self.checkMove.stateChanged.connect(lambda: self.pathtextbox.EnablePathTextBox(self.checkMove.isChecked()))
 
        self.buttonlaybar.clear.clicked.connect(self.clearFileTextBox)
        self.buttonlaybar.create.clicked.connect(self.createDirAction)

        self.listwidget.clicked.connect(self.changeFileTextBox)
        self.listwidget.itemSelectionChanged.connect(self.changeFileTextBox)
        pass


    def UIOrdererInit(self):
        self.primaryLayout.addWidget(self.listwidget)

        self.subLayTextBoxHorizontal.addWidget(self.filetextbox)
        self.subLayTextPathHorizontal.addWidget(self.pathtextbox)
        self.subLayTextBoxHorizontal.addSpacing(200)
        self.subLayTextPathHorizontal.addWidget(self.checkMove)

        self.primaryLayout.addLayout(self.subLayTextPathHorizontal)
        self.primaryLayout.addLayout(self.subLayTextBoxHorizontal)
        self.primaryLayout.addLayout(self.buttonlaybar)
        self.setLayout(self.primaryLayout)


    def createDirAction(self):
        if self.pathtextbox.isEnabled() is True:
            self.pathtextbox.clear()
            self.pathtextbox.setPlaceholderText(self.pathtextbox.label)

        if len(self.filenameetextbox.text()) == 0:
            self._dir = listfiles[0].split('.')[0]            
        else:
            self._dir = join(dirname(listfiles[0].split('.')[0]), self.filetextbox.text())
        
        try:
            self.mk.makedir(self._dir)
        except Exception as e:
            raise e

        self.close()


    def changeFileTextBox(self):
        self.filetextbox.setStyleSheet("color: white")
        self.filetextbox.setText(self.listwidget.current_selected())


    def clearFileTextBox(self):
        self.filetextbox.clear()
        self.filetextbox.setPlaceholderText(self.filetextbox.label)
        # 
    pass


if __name__ == '__main__':
    MainEventThread = QApplication(['AppGui'])
    MainApp = AppGui()
    MainApp.show()
    MainEventThread.exec()