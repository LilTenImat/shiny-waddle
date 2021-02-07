import design
import sys
import json
import os
from time import sleep
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon,\
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp, QPushButton
from PyQt5.QtCore import QSize, QCoreApplication
from PyQt5 import QtGui
import PyQt5.QtCore as QtCore
from intiligance import Worker
import threading

worker = Worker()

os.environ["WORKING"] = 'False'
os.environ["RESULT"] = ""

class CommandHandler(QtCore.QObject):
    running = False
    finished = QtCore.pyqtSignal(str, str)

    def run(self, text=None):

        res = worker.on_command(text)
        self.finished.emit(res, "user")

class Application(QMainWindow, design.Ui_MainWindow):
    check_box = None
    tray_icon = None
    active = False
    commandHandler = CommandHandler()
    text = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initTrayIcon()
        self.initMicList()
        self.setWindowIcon(QtGui.QIcon('./assets/images/icon.png'))


        self.thread = QtCore.QThread()
        self.commandHandler.moveToThread(self.thread)
        # self.thread.started.connect(self.commandHandler.run)
        self.commandHandler.finished.connect(self.updateText)
        self.thread.start()
        self.pushButton_7.clicked.connect(self.commandHandler.run)
        self.pushButton_7.setIconSize(QSize(64, 32))

        self.lineEdit.returnPressed.connect(self.commandHandler.run, text=self.lineEdit.text())

        if os.path.exists('settings.json'):
            self.dropSettings()
        else:
            self.saveSettings()


    @QtCore.pyqtSlot(str, str)
    def updateText(self, string, f):
        if f == "user":
            html = f'''
                    <div style="text-align:center;">
                        <div style="width:50%; background-color:#E0E0E2; border:000; border-radius:5px;">
                            <p>{string}</p>
                        </div>
                    </div>
                    '''
        elif f == "ai":
            html = f'''
                    <div style="text-align:center;">
                        <div style="width:50%; background-color:#494993; border:000; border-radius:5px;">
                            <p>{string}</p>
                        </div>
                    </div>
                    '''
        
        self.textBrowser.append(html)

    def switchActive(self):
        self.show()
        _translate = QCoreApplication.translate
        if self.pushButton_7.text() == "Push":
            # self.active = not (self.active)
            # self.pushButton_7.setText(_translate("MainWindow", "Speak"))
            self.text += 'This is returned string'; worker.on_command()
            self.textBrowser.setText(self.text)

    def saveSettings(self):
        settings = {}
        settings['cb1'] = self.checkBox.isChecked()
        settings['cb2'] = self.checkBox_2.isChecked()
        settings['cb3'] = self.checkBox_3.isChecked()
        settings['cb4'] = self.checkBox_4.isChecked()
        with open("settings.json", 'w') as setts:
            json.dump(settings, setts)

    def dropSettings(self):
        with open("settings.json") as setts:
            settings = json.load(setts)
            self.checkBox.setChecked(settings['cb1'])
            self.checkBox_2.setChecked(settings['cb2'])
            self.checkBox_3.setChecked(settings['cb3'])
            self.checkBox_4.setChecked(settings['cb4'])

    def initTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon('./assets/images/icon.png'))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.onTrayIconActivated)
        # self.tray_icon.activated.connect(self.pushButton_7.click)
        self.tray_icon.show()

    def initMicList(self):
        _translate = QCoreApplication.translate
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, _translate("MainWindow", ""))

    def onTrayIconActivated(self, reason):
        # print("onTrayIconActivated:", reason)
        if reason == 3:
            self.activateWindow()
            self.show()
        if reason == 2:
            self.pushButton_7.click()
            

    def closeEvent(self, event):
        self.saveSettings()
        if self.checkBox.isChecked():
            event.ignore()
            self.hide()
            if self.checkBox_2.isChecked():
                self.tray_icon.showMessage(
                    "Shiny waddle",
                    "Application was minimized to Tray! \nDouble click to activate",
                    QSystemTrayIcon.Information,
                    2000
                )
        # elif self.checkBox_2.isChecked():
        #     reply = QMessageBox.question(self, 'Quit',
        #         "Are you sure to quit?", QMessageBox.Yes |
        #         QMessageBox.No, QMessageBox.No)

        #     if reply == QMessageBox.Yes:
        #         event.accept()
        #     else:
        #         event.ignore()
        else:
            self.thread.exit()
            event.accept()

    def quit(self):
        self.thread.exit()
        qApp.quit()

def main():
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
    threading._shutdown()
