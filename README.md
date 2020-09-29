# KDE Context Menu to Create folder from selected files - folderfromselected.

This project creates two entries in the context menu, the goal is to create folders for selected files.

There are two modes of operation, cmd and gui, and with them it is possible to perform exactly the same operations, create a directory for the files and move the directory to another location.

The cmd mode should work correctly in any distribution with python, the gui mode will only work if the distribution supports Qt, pyQt.

I tested only on KDE.

# Install

Clone the repo and run (whith no sudo) ```./install.sh``` or ```sudo -E ./install.sh```.

# Easy Install

sudo wget -P '/tmp/' "https://raw.githubusercontent.com/luizoti/folderfromselected/master/install.sh" && sudo chmod +x /tmp/install.sh && sudo -E /tmp/install.sh -i
