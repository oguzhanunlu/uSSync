# This file is part of uSSync. 
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Copyright 2013 Erdal Sivri, Oguzhan Unlu
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

def tray_icon(app):
    trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("images/uSSync.png"), app)
    menu = QtGui.QMenu('uSSync')
    openAction = menu.addAction('Open')
    exitAction = menu.addAction('Exit')
    trayIcon.setContextMenu(menu)
    trayIcon.showMessage('uSSync is running!', 'Click to open window
Right click for menu')
    trayIcon.show()

def main(args):
    app = QtGui.QApplication(args)
    w = QtGui.QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('uSSync Test App')
    w.show()
    tray_icon(app)
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
