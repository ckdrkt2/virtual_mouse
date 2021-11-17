from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import PyQt5

class Button(QPushButton):
    def __init__(self):
        QPushButton.__init__(self, "OFF")
        # self.setFixedSize(1200, 800)
        self.showFullScreen()
        self.setStyleSheet("background-color: red")

        self.setCheckable(True)
        self.toggled.connect(self.slot_toggle)

    @pyqtSlot(bool)
    def slot_toggle(self, state):
        self.setStyleSheet("background-color: %s" % ({True: "green", False: "red"}[state]))
        self.setText({True: "ON", False: "OFF"}[state]) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Button()
    form.show()
    exit(app.exec_())
