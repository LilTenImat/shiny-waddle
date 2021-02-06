import design
import sys
import json
import os
# import concurrent.futures
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
    finished = QtCore.pyqtSignal(str)
    
    def run(self):
        res = worker.on_command()
        self.finished.emit(res)

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
        self.setWindowIcon(QtGui.QIcon('./assets/images/icon.ico'))
        

        self.thread = QtCore.QThread()
        self.commandHandler.moveToThread(self.thread)
        # self.thread.started.connect(self.commandHandler.run)
        self.commandHandler.finished.connect(self.updateText)
        self.thread.start()
        self.pushButton_7.clicked.connect(self.commandHandler.run)
        if os.path.exists('settings.json'):
            self.dropSettings()
        else:
            self.saveSettings()
       

<<<<<<< HEAD
    @QtCore.pyqtSlot(str)
    def updateText(self, string):
        html = f'''
                <div style="text-align:center;">
                    <div style="width:50%; background-color:#E0E0E2; border-radius:5px;">
                        <p>{string}</p>
                    </div>
                </div>
                '''
        self.textBrowser.append(html)
=======
    def switchActive(self):
        self.show()
        _translate = QCoreApplication.translate
        if self.pushButton_7.text() == "Push":
            # self.active = not (self.active)
            # self.pushButton_7.setText(_translate("MainWindow", "Speak"))
            self.text += 'This is returned string'; worker.on_command()
            self.textBrowser.setText(self.text)
>>>>>>> intilegence

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
        self.tray_icon.setIcon(QtGui.QIcon('./assets/images/icon.ico'))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.show)
        # self.tray_icon.activated.connect(self.commandHandler.run)
        self.tray_icon.show()

    def initMicList(self):
        _translate = QCoreApplication.translate
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, _translate("MainWindow", ""))

    def onTrayIconActivated(self, reason):
        print("onTrayIconActivated:", reason)
        if reason == QSystemTrayIcon.Trigger:
            self.disambiguateTimer.start(qApp.doubleClickInterval())
        elif reason == QSystemTrayIcon.DoubleClick:
            self.disambiguateTimer.stop()
            print("Tray icon double clicked")

    def closeEvent(self, event):
        self.saveSettings()
        if self.checkBox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Tray Program",
                "Application was minimized to Tray",
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
            event.accept()


def main():
    global window
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
    threading._shutdown()

