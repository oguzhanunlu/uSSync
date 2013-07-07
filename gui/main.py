#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

def tray_icon(app):
    trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("uSSync.png"), app)
    menu = QtGui.QMenu('uSSync')
    exitAction = menu.addAction("Exit")
    trayIcon.setContextMenu(menu)
    trayIcon.showMessage('uSSync is running!', 'Click to open window\nRight click for menu')
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

