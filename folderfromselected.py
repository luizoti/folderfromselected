#!/usr/bin/python3

import os
import sys
import os.path
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
 
class FileList(QWidget):
    def __init__(self):
        self.App = QApplication(sys.argv)
        self.App.size(200, 200)
        self.label = QLabel("Hello Word")
        self.label.show()
        self.App.exec_()

# def makelist(self):
#     for filename in sys.argv:
#         if not sys.argv[0] == filename:
#             pass
#         pass

# # def editname(self):

# #     pass


# # def makedir(self):
# #     pass
  

if __name__ == '__main__':
    FileList()
    