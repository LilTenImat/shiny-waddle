import sys
import json
import os
from time import sleep 
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon,\
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp, QPushButton
from PyQt5.QtCore import QSize, QCoreApplication
from intiligance import Worker

worker = Worker()



import design

class Application(QMainWindow, design.Ui_MainWindow):
    check_box = None
    tray_icon = None
    active = False
    text = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initTrayIcon()
        self.initMicList()
        self.pushButton_7.clicked.connect(self.switchActive)
        # self.buttonBox.rejected.connect(self.dropSettings)
        # self.buttonBox.accepted.connect(self.saveSettings)
        # self.checkBox.setChecked(True)
        # self.sounds = {'mic_on': ("mic_alert.wav")}
        if os.path.exists('settings.json'):
            self.dropSettings()
        else:
            self.saveSettings()

    def switchActive(self):
        self.text += "<h1 style='color: magenta;'>This is head 1!</h1>"
        _translate = QCoreApplication.translate
        if self.pushButton_7.text() == "Push":
            # self.active = not (self.active)
            self.textBrowser.setText(self.text)
            # self.pushButton_7.setText(_translate("MainWindow", "Speak"))
            worker.on_command()

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
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        # tray_menu = QPushButton()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        # tray_menu.clicked.connect(self.switchActive)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def initMicList(self):
        _translate = QCoreApplication.translate
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, _translate("MainWindow", ""))

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
        elif self.checkBox_2.isChecked():
            reply = QMessageBox.question(self, 'Quit',
                "Are you sure to quit?", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
def main():
    app = QApplication(sys.argv) 
    window = Application() 
    window.show() 
    app.exec_() 

if __name__ == '__main__':
    main()