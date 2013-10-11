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
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final_dev_main.ui'
#
# Created: Sun Sep 29 17:34:28 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

import os
import sys
import time

from PyQt4 import QtCore, QtGui

import conf
from app import USSyncApp

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class BackgroundWorker(QtCore.QThread):
    filesUpdated = QtCore.pyqtSignal(list)
    progressUpdated = QtCore.pyqtSignal(int)
    
    def __init__(self, ui):
        QtCore.QThread.__init__(self)
        self.ui = ui
    
    def run(self):
        self.ui.uSSyncApp.run(self.ui.conf_file, self.ui.onProgress)


class Ui_MainWindow(object):
    CONF_FILE = os.path.expanduser('~/app.conf')
    MAX_FILES = 10
    
    def __init__(self):
        self.conf_file = Ui_MainWindow.CONF_FILE
        self.uSSyncApp = USSyncApp()
        if not os.path.exists(self.conf_file):
            self.uSSyncApp.create_default_conf(self.conf_file)
        self.confs = conf.read_conf(self.conf_file)
        self.files = []
        self.times = []
        # start sync automatically on background
        self.backgroundWorker = BackgroundWorker(self)
        self.backgroundWorker.filesUpdated.connect(self.displayFiles)
        self.backgroundWorker.progressUpdated.connect(self.displayProgress)
        self.backgroundWorker.start()
        #self.uSSyncApp.run_async(self.conf_file, self.onProgress)
    
    def onProgress(self, progress):
        current_file = progress[0]
        current_status = progress[1]
        percentage = int(current_status.percentage)
        print '%s %d%%' % (current_file, percentage)
        self.backgroundWorker.progressUpdated.emit(percentage)
        #self.progressSync.setProperty('value', percentage)
        if len(self.files) == 0:
            self.files.append(current_file)
        elif self.files[-1] == current_file:
            pass
        else:
            now = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
            self.times.append(now)
            self.files.append(current_file)
            if len(self.files) > Ui_MainWindow.MAX_FILES:
                del self.files[0]
                del self.times[0]
        self.backgroundWorker.filesUpdated.emit(self.files)
        #self.displayFiles()
    
    def displayProgress(self, percentage):
        self.progressSync.setProperty('value', percentage)
    
    def displayFiles(self, files):
        lines = []
        for index,filename in enumerate(self.files):
            basename = os.path.basename(filename)
            if index >= len(self.times):
                continue
            sync_time = self.times[index]
            line = '<p>%s -> %s</p>' % (sync_time, basename)
            lines.append(line)
        html = ''.join(lines)
        self.textBrowserStatus.setHtml(html)
        html = '<p>Syncing %s...</p>' % basename
        self.textBrowserLog.setHtml(html)
        self.showMessage('Syncing %s' % basename)
    
    def onSyncClicked(self):
        self.uSSyncApp.sync()
        self.showMessage('Sync completed!')
        #self.uSSyncApp.run(self.conf_file, self.onProgress)
    
    def chooseDestinationFolder(self):
        folder = QtGui.QFileDialog.getExistingDirectory(
                self.tab, 
                _fromUtf8('Choose Destination Folder'), 
                os.path.expanduser('~'), 
                QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        self.txtDestination.setText(folder)
    
    def chooseSourceFolder(self):
        folder = QtGui.QFileDialog.getExistingDirectory(
                self.tab, 
                _fromUtf8('Choose Source Folder'), 
                os.path.expanduser('~'), 
                QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        self.txtSource.setText(folder)
    
    def saveSettings(self):
        folder = self.txtDestination.text()
        if folder is not None and len(folder.trimmed()) > 0:
            self.confs['target_folder'] = str(folder)
        folder = self.txtSource.text()
        if folder is not None and len(folder.trimmed()) > 0:
            self.confs['source_folder'] = str(folder)
        disable_recursion = self.chkDisableRecursion.isChecked()
        preserve_time = self.chkPreserveTime.isChecked()
        verbose = self.chkVerbose.isChecked()
        checksum = self.chkChecksum.isChecked()
        preserve_permissions = self.chkPreservePermissions.isChecked()
        self.confs['disable_recursion'] = disable_recursion
        self.confs['preserve_time'] = preserve_time
        self.confs['verbose'] = verbose
        self.confs['checksum'] = checksum
        self.confs['preserve_permissions'] = preserve_permissions
        with open(Ui_MainWindow.CONF_FILE, 'w') as f:
            conf.write_conf(self.confs, f)
        self.showMessage('Settings saved!')
    
    def showMessage(self, message):
        self.trayIcon.showMessage(_fromUtf8('uSSync'), _fromUtf8(message))
    
    def setCheckBoxes(self):
        disable_recursion = self.confs.get('disable_recursion') or False
        preserve_time = self.confs.get('preserve_time') or False
        verbose = self.confs.get('verbose') or False
        checksum = self.confs.get('checksum') or False
        preserve_permissions = self.confs.get('preserve_permissions') or False
        self.chkDisableRecursion.setChecked(self.toBool(disable_recursion))
        self.chkPreserveTime.setChecked(self.toBool(preserve_time))
        self.chkVerbose.setChecked(self.toBool(verbose))
        self.chkChecksum.setChecked(self.toBool(checksum))
        self.chkPreservePermissions.setChecked(self.toBool(preserve_permissions))

    def setFolders(self):
        source_folder = self.confs.get('source_folder')
        target_folder = self.confs.get('target_folder')
        self.txtSource.setText(str(source_folder))
        self.txtDestination.setText(str(target_folder))
    
    def toBool(self, text):
        text = text.lower()
        if text == 'true':
            return True
        else:
            return False
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("uSSync App"))
        MainWindow.setEnabled(True)
        MainWindow.resize(450, 466)
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.btnSyncNow = QtGui.QPushButton(self.tab)
        self.btnSyncNow.setGeometry(QtCore.QRect(160, 240, 98, 27))
        self.btnSyncNow.setAcceptDrops(False)
        self.btnSyncNow.setAutoFillBackground(False)
        self.btnSyncNow.setDefault(True)
        self.btnSyncNow.setFlat(False)
        self.btnSyncNow.setObjectName(_fromUtf8("btnSyncNow"))
        self.btnSyncNow.clicked.connect(self.onSyncClicked)
        self.txtSource = QtGui.QLineEdit(self.tab)
        self.txtSource.setGeometry(QtCore.QRect(100, 20, 291, 27))
        self.txtSource.setText(_fromUtf8(""))
        self.txtSource.setObjectName(_fromUtf8("txtSource"))
        self.btnChooseDestinationFolder = QtGui.QToolButton(self.tab)
        self.btnChooseDestinationFolder.setGeometry(QtCore.QRect(400, 60, 31, 25))
        self.btnChooseDestinationFolder.setObjectName(_fromUtf8("btnChooseDestinationFolder"))
        self.btnChooseDestinationFolder.clicked.connect(self.chooseDestinationFolder)
        self.lblSourceFolder = QtGui.QLabel(self.tab)
        self.lblSourceFolder.setGeometry(QtCore.QRect(30, 20, 59, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblSourceFolder.setFont(font)
        self.lblSourceFolder.setObjectName(_fromUtf8("lblSourceFolder"))
        self.txtDestination = QtGui.QLineEdit(self.tab)
        self.txtDestination.setGeometry(QtCore.QRect(100, 60, 291, 27))
        self.txtDestination.setObjectName(_fromUtf8("txtDestination"))
        self.lblDestinationFolder = QtGui.QLabel(self.tab)
        self.lblDestinationFolder.setGeometry(QtCore.QRect(-2, 60, 91, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblDestinationFolder.setFont(font)
        self.lblDestinationFolder.setObjectName(_fromUtf8("lblDestinationFolder"))
        self.btnChooseSourceFolder = QtGui.QToolButton(self.tab)
        self.btnChooseSourceFolder.setGeometry(QtCore.QRect(400, 20, 31, 25))
        self.btnChooseSourceFolder.setObjectName(_fromUtf8("btnChooseSourceFolder"))
        self.btnChooseSourceFolder.clicked.connect(self.chooseSourceFolder)
        self.line_2 = QtGui.QFrame(self.tab)
        self.line_2.setGeometry(QtCore.QRect(20, 90, 401, 31))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.textBrowserLog = QtGui.QTextBrowser(self.tab)
        self.textBrowserLog.setGeometry(QtCore.QRect(10, 350, 421, 71))
        self.textBrowserLog.setObjectName(_fromUtf8("textBrowserLog"))
        self.progressSync = QtGui.QProgressBar(self.tab)
        self.progressSync.setGeometry(QtCore.QRect(10, 310, 421, 23))
        self.progressSync.setProperty("value", 0)
        self.progressSync.setObjectName(_fromUtf8("progressSync"))
        self.line_3 = QtGui.QFrame(self.tab)
        self.line_3.setGeometry(QtCore.QRect(20, 220, 401, 31))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.lblProgress = QtGui.QLabel(self.tab)
        self.lblProgress.setGeometry(QtCore.QRect(10, 280, 66, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblProgress.setFont(font)
        self.lblProgress.setTextFormat(QtCore.Qt.AutoText)
        self.lblProgress.setObjectName(_fromUtf8("lblProgress"))
        self.grpAdvanced = QtGui.QGroupBox(self.tab)
        self.grpAdvanced.setGeometry(QtCore.QRect(30, 110, 371, 121))
        self.grpAdvanced.setObjectName(_fromUtf8("grpAdvanced"))
        self.chkVerbose = QtGui.QCheckBox(self.grpAdvanced)
        self.chkVerbose.setGeometry(QtCore.QRect(10, 60, 151, 22))
        self.chkVerbose.setObjectName(_fromUtf8("chkVerbose"))
        self.chkVerbose.setChecked(False)
        self.chkPreserveTime = QtGui.QCheckBox(self.grpAdvanced)
        self.chkPreserveTime.setGeometry(QtCore.QRect(190, 30, 151, 22))
        self.chkPreserveTime.setObjectName(_fromUtf8("chkPreserveTime"))
        self.chkPreserveTime.setChecked(True)
        self.chkChecksum = QtGui.QCheckBox(self.grpAdvanced)
        self.chkChecksum.setGeometry(QtCore.QRect(190, 60, 151, 22))
        self.chkChecksum.setObjectName(_fromUtf8("chkChecksum"))
        self.chkChecksum.setChecked(False)
        self.chkDisableRecursion = QtGui.QCheckBox(self.grpAdvanced)
        self.chkDisableRecursion.setGeometry(QtCore.QRect(10, 30, 151, 22))
        self.chkDisableRecursion.setObjectName(_fromUtf8("chkDisableRecursion"))
        self.chkDisableRecursion.setChecked(False)
        self.chkPreservePermissions = QtGui.QCheckBox(self.grpAdvanced)
        self.chkPreservePermissions.setGeometry(QtCore.QRect(10, 90, 171, 22))
        self.chkPreservePermissions.setObjectName(_fromUtf8("chkPreservePermissions"))
        self.chkPreservePermissions.setChecked(True)
        self.btnSave = QtGui.QPushButton(self.tab)
        self.btnSave.setGeometry(QtCore.QRect(330, 240, 98, 27))
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.btnSave.clicked.connect(self.saveSettings)
        MainWindow.addTab(self.tab, _fromUtf8(""))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.textBrowserStatus = QtGui.QTextBrowser(self.tab1)
        self.textBrowserStatus.setGeometry(QtCore.QRect(10, 40, 421, 381))
        self.textBrowserStatus.setObjectName(_fromUtf8("textBrowserStatus"))
        self.lblStatus = QtGui.QLabel(self.tab1)
        self.lblStatus.setGeometry(QtCore.QRect(10, 10, 191, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblStatus.setFont(font)
        self.lblStatus.setTextFormat(QtCore.Qt.AutoText)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        MainWindow.addTab(self.tab1, _fromUtf8(""))

        self.retranslateUi(MainWindow)
        MainWindow.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # added
        self.MainWindow = MainWindow
        self.initUI(MainWindow)
    
    def show(self):
        self.MainWindow.show()
    
    def hide(self):
        self.MainWindow.hide()
        self.showMessage('uSSync is still running. Click exit to quit!')
    
    def exit(self):
        result = QtGui.QMessageBox.question(
                self.MainWindow, 
                _fromUtf8('uSSync'), 
                _fromUtf8('Are you sure you want to quit?'),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            QtGui.QApplication.quit()
    
    def closeEvent(self, event):
        # minimize
        self.hide()
        #self.trayIcon.show()
        event.ignore()
    
    def initUI(self, MainWindow):
        #traySignal = 'activated(QSystemTrayIcon::ActivationReason)'
        #QtCore.QObject.connect(self.trayIcon, QtCore.SIGNAL(traySignal), self.iconActivated)
        closeSignal = 'triggered()'
        MainWindow.connect(MainWindow, QtCore.SIGNAL(closeSignal), self.closeEvent)
        MainWindow.closeEvent = self.closeEvent
        # 
        MainWindow.setWindowIcon(QtGui.QIcon('gui/images/uSSync.png'))
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        # 
        self.setCheckBoxes()
        self.setFolders()
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "uSSync", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSyncNow.setText(QtGui.QApplication.translate("MainWindow", "Sync Now", None, QtGui.QApplication.UnicodeUTF8))
        self.btnChooseDestinationFolder.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSourceFolder.setText(QtGui.QApplication.translate("MainWindow", "   Source", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDestinationFolder.setText(QtGui.QApplication.translate("MainWindow", "  Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.btnChooseSourceFolder.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowserLog.setHtml(QtGui.QApplication.translate("MainWindow", "uSSync", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProgress.setText(QtGui.QApplication.translate("MainWindow", "Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.grpAdvanced.setTitle(QtGui.QApplication.translate("MainWindow", "Advanced Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.chkVerbose.setText(QtGui.QApplication.translate("MainWindow", "Verbose ", None, QtGui.QApplication.UnicodeUTF8))
        self.chkPreserveTime.setText(QtGui.QApplication.translate("MainWindow", "Preserve Time", None, QtGui.QApplication.UnicodeUTF8))
        self.chkChecksum.setText(QtGui.QApplication.translate("MainWindow", "Always Checksum", None, QtGui.QApplication.UnicodeUTF8))
        self.chkDisableRecursion.setText(QtGui.QApplication.translate("MainWindow", "Disable Recursion", None, QtGui.QApplication.UnicodeUTF8))
        self.chkPreservePermissions.setText(QtGui.QApplication.translate("MainWindow", "Preserve permissions", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setTabText(MainWindow.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowserStatus.setHtml(QtGui.QApplication.translate("MainWindow", "uSSync", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setText(QtGui.QApplication.translate("MainWindow", "Recently Synchorized Files", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setTabText(MainWindow.indexOf(self.tab1), QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))



def trayIcon(app, ui):
    trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("gui/images/uSSync.png"), app)
    trayIcon.setToolTip('uSSync')
    menu = QtGui.QMenu('uSSync')
    openAction = menu.addAction('Show')
    openAction.triggered.connect(lambda: ui.show())
    openAction = menu.addAction('Hide')
    openAction.triggered.connect(lambda: ui.hide())
    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(lambda: ui.exit())
    trayIcon.setContextMenu(menu)
    trayIcon.showMessage('uSSync is running!', 'Click to open window Right click for menu')
    return trayIcon

def main(args):
    app = QtGui.QApplication(sys.argv)
    #MainWindow = QtGui.QMainWindow()
    MainWindow = QtGui.QTabWidget()
    global ui
    ui = Ui_MainWindow()
    ui.trayIcon = trayIcon(app, ui)
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.trayIcon.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
