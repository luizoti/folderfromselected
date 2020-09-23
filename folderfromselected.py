#!/usr/bin/python3

import os
import sys
import argparse

from os import mkdir, rmdir, listdir, rename
from os.path import basename, isfile, isdir, join, dirname
from shutil import copytree, move, Error as sterr

from PyQt5.QtGui import QKeyEvent, QIcon, QKeySequence
from PyQt5.Qt import QDir
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QTreeView, QFileDialog, QShortcut

realpath = join(os.path.dirname(os.path.realpath(__file__)), 'icos')
parse = argparse.ArgumentParser(description='Create folder from selected files:')

parse.add_argument('-c', '--cmd', nargs='+', metavar='filelist', help='CMD create folder')
parse.add_argument('-g', '--gui', nargs='+', metavar='filelist', help='GUI create folder')
parse.add_argument('-d', '--dir', metavar='dirname', help='Name of dir for CMD')
parse.add_argument('-m', '--move', metavar='movepath', help='Path to move created dir')
args = parse.parse_args()

# 
# 
class NewPathLine(QLineEdit):
    def __init__(self, parent):
        super(NewPathLine, self).__init__(parent)
        self.parentWindow = parent
        self.label = 'Digite o caminho para mover a pasta'
        self.setPlaceholderText(self.label)
        self.setStyleSheet("color: #7d7d7d")
        self.setEnabled(False)


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


    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [16777234, 16777236] and self.label in self.text():
            self.setCursorPosition(0)
        else:
            super().keyPressEvent(event)
            pass
        self.parentWindow.keyPressEvent(event)
# 
# 
# 
class FileTextbox(QLineEdit):
    def __init__(self, parent):
        super(FileTextbox, self).__init__(parent)
        self.parentWindow = parent
        self.label = 'Digite o nome da pasta'
        self.setPlaceholderText(self.label)


    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in [16777234, 16777236] and self.label in self.text():
            self.setCursorPosition(0)
        else:
            super().keyPressEvent(event)
            pass
        self.parentWindow.keyPressEvent(event)


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.mk = ManageFiles()
        self.title = 'Criar Pasta!'
        self.setWindowIcon(QIcon(join(realpath, 'folder.svg')))

        self.EnterKey = QShortcut(QKeySequence("Enter"), self)
        self.ExitKey = QShortcut(QKeySequence("Esc"), self)

        self.ExitKey.activated.connect(self.close)
        self.EnterKey.activated.connect(lambda: print("Hey Hey"))

        self.width, self.height = 500, 400
        self.left = round(int((size.width() - self.width)/ 2))
        self.top = round(int((size.height() - self.height + 40) / 2))
        self.setFixedSize(self.width, self.height)
        #  
        self.vbox_primary = QVBoxLayout()
        # 
        self.textbox_layout_hoziontal = QHBoxLayout()
        self.textpath_layout_hoziontal = QHBoxLayout()
        self.buttons_hoziontal = QHBoxLayout()

        self.list = QListWidget()
        # 
        self.checkmove = QCheckBox()
        self.checkmove.setIcon(QIcon(join(realpath, 'lock.svg')))
        self.search = QPushButton()
        self.search.setIcon(QIcon(join(realpath, 'find.svg')))
        self.search.setFixedSize(30, 30)
        self.search.setEnabled(False)
        self.clear = QPushButton('Limpar')
        self.create = QPushButton('Criar')

        self.filetextbox = FileTextbox(self)
        self.pathtextbox = NewPathLine(self)
        
        self.filetextbox.setFixedWidth(480)
        self.initUI()
        

    def initUI(self):
        count = 0
        for filename in reversed(listfiles):
            self.list.insertItem(count, basename(filename).split('.')[0])
            count + 1
            pass
        # 
        self.list.clicked.connect(self.current_selected and self.filetextbox_change)
        self.list.itemSelectionChanged.connect(self.current_selected and self.filetextbox_change)
        self.search.clicked.connect(lambda: self.pathtextbox.folderdiag())
        self.checkmove.stateChanged.connect(lambda: self.enable_pathtextbox(self.pathtextbox.isEnabled()))
        self.create.clicked.connect(self.folder_action)

        self.clear.clicked.connect(self.clearact)
        self.vbox_primary.addWidget(self.list)
        self.textbox_layout_hoziontal.addWidget(self.filetextbox)
        self.textpath_layout_hoziontal.addWidget(self.pathtextbox)
        self.textbox_layout_hoziontal.addSpacing(200)
        self.textpath_layout_hoziontal.addWidget(self.search)
        self.textpath_layout_hoziontal.addWidget(self.checkmove)
        self.buttons_hoziontal.addWidget(self.clear)
        self.buttons_hoziontal.addWidget(self.create)
        self.vbox_primary.addLayout(self.textpath_layout_hoziontal)
        self.vbox_primary.addLayout(self.textbox_layout_hoziontal)
        self.vbox_primary.addLayout(self.buttons_hoziontal)
        self.setLayout(self.vbox_primary)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


    def enable_pathtextbox(self, state):
        if state is False:
            self.checkmove.setIcon(QIcon(join(realpath, 'unlock.svg')))
            self.pathtextbox.setEnabled(True)
            self.search.setEnabled(True)
            self.pathtextbox.setStyleSheet("color: white")
        elif state is True:
            self.checkmove.setIcon(QIcon(join(realpath, 'lock.svg')))
            self.pathtextbox.setEnabled(False)
            self.search.setEnabled(False)
            self.pathtextbox.setStyleSheet("color: #7d7d7d")
            pass
        pass
        self.pathtextbox.setPlaceholderText(self.pathtextbox.label)


    def folder_action(self):
        if self.pathtextbox.isEnabled() is True:
            self.pathtextbox.clear()
            self.pathtextbox.setPlaceholderText(self.pathtextbox.label)
            pass

        if len(self.filetextbox.text()) == 0:
            self._dir = listfiles[0].split('.')[0]            
        else:
            self._dir = join(dirname(listfiles[0].split('.')[0]), self.filetextbox.text())
            pass
        
        try:
            self.mk.makedir(self._dir)
        except Exception as e:
            raise e

        self.close()

    def current_selected(self):
        item = self.list.currentItem()
        return str(item.text())


    def filetextbox_change(self):
        self.filetextbox.setStyleSheet("color: white")
        self.filetextbox.setText(self.current_selected())


    def clearact(self):
        self.filetextbox.clear()
        self.filetextbox.setPlaceholderText(self.filetextbox.label)
        # 


class ManageFiles():
    def __init__(self):
        print(' Gerenciador de Arquivos')


    def makedir(self, dirpath):
        self.dir = dirpath

        if isdir(self.dir):
            print(f' Pasta já existe: {self.dir}')
            # 
            try:
                self.movefiles()
            except Exception as e:
                raise e
        elif isfile(self.dir) or not isdir(self.dir):
            print(f'  É um arquivo ou não existe: {self.dir}')
            olddir = self.dir
            self.dir = self.dir + '1'

            try:
                mkdir(self.dir)
                self.movefiles()
                rename(self.dir, olddir)
            except Exception as MkdirE:
                raise MkdirE
                pass
            pass


    def movefiles(self):
        print()
        print('Movendo arquivos:')
        for file in listfiles:
            try:
                move(file, self.dir)
                print(f' Arquivo movido, {file}')
            except sterr as Fexist:
                print(f' {Fexist.args[0]}, ignorado.')
            except FileNotFoundError as NotF:
                print(f' Arquivo não existe: {file}')
            pass


    def newpath(self, newpath):
        src_dir = dirname(_dir)
        dest_dir = join(newpath, basename(_dir))
        # 
        print()
        print(f'Movendo {_dir} para {newpath}.')

        def move_act():
            for file in listdir(_dir):
                file = join(_dir, file)
                if isfile(file):
                    if isdir(dest_dir):
                        print(f'  Arquivo {file}, copiado para {dest_dir}.')
                        move(file, dest_dir)

        try:
            if isdir(newpath):
                if newpath == src_dir:
                    print(f' Diretorio {src_dir} é igual a {dest_dir}.')
                else:
                    print(f' Movendo arquivos para {dest_dir}.')
                    if not isdir(dest_dir):
                        print(f' Diretorio {dest_dir}, criado!')
                        mkdir(dest_dir)
                    pass
                    # 
                    move_act()
                    # 
                    if len(listdir(_dir)) == 0:
                        rmdir(_dir)
                        print()
                        print(f' Diretorio {_dir}, apagado.')
                        pass
                        # 
            else:
                print(f'Diretorio {newpath} não existe!')
                pass
        except Exception as e:
            raise e
        pass


if __name__ == '__main__':
    if args.gui is not None:
        print('Graphical Interface Mode')
        listfiles = args.gui
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        size = screen.size()
        App()
        sys.exit(app.exec_())
    elif args.cmd is not None:
        print('Command Line Interface')
        listfiles = args.cmd
        # 
        if args.dir:
            _dir = join(dirname(listfiles[0].split('.')[0]), args.dir)
        else:
            _dir = listfiles[0].split('.')[0]
            pass

        mk = ManageFiles()
        mk.makedir(_dir)
        if args.move is not None:
            mk.newpath(args.move)
            pass
        pass