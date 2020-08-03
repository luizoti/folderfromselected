#!/usr/bin/python

import os
import os.path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QListWidgetItem 
  
  
class Ui_MainWindow(QWidget): 
    def __init__(self): 
        self.app = QApplication(sys.argv) 
        self.window = QWidget() 
        self.listWidget = QListWidget() 
        self.window.setWindowTitle("Select a name to folder!") 
        self.makelist()                


    def makelist(self):
        for filename in sys.argv:
            if not sys.argv[0] == filename:
                QListWidgetItem(os.path.basename(filename), self.listWidget)

        window_layout = QVBoxLayout(self.window)
        window_layout.addWidget(self.listWidget)
        self.window.setLayout(window_layout)
      
        self.window.show() 
        sys.exit(self.app.exec_()) 


    def editname(self):
        pass


    def makedir(self):
        pass


if __name__ == '__main__': 
    Ui_MainWindow()      
