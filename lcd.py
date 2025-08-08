from PyQt5.QtWidgets import QMainWindow, QApplication, QLCDNumber, QPushButton, QSpinBox
from PyQt5 import uic
from PyQt5.QtCore import QTimer
import sys



class CountdownTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("lcd.ui", self)
        self.lcd_display = self.findChild(QLCDNumber, "lcdNumber")
        self.start_btn = self.findChild(QPushButton, "btnStart")
        self.stop_btn = self.findChild(QPushButton, "btnStop")
        self.reset_btn = self.findChild(QPushButton, "btnReset")
        self.hr_spin = self.findChild(QSpinBox, "hourSpinBox")
        self.min_spin = self.findChild(QSpinBox, "minuteSpinBox")
        self.sec_spin = self.findChild(QSpinBox, "secondSpinBox")
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.time_left = 0
        self.running = False
        self.start_btn.clicked.connect(self._start)
        self.stop_btn.clicked.connect(self._stop)
        self.reset_btn.clicked.connect(self._reset)
        self._update_display()
        self.show()



    def _update_display(self):
        h = self.time_left // 3600
        m = (self.time_left % 3600) // 60
        s = self.time_left % 60
        self.lcd_display.display(f"{h:02d}:{m:02d}:{s:02d}")


    def _start(self):
        if not self.running:
            if self.time_left <= 0:
                h = self.hr_spin.value()
                m = self.min_spin.value()
                s = self.sec_spin.value()
                self.time_left = h * 3600 + m * 60 + s
            if self.time_left > 0:
                self.timer.start(1000)
                self.running = True
                self.start_btn.setEnabled(False)


    def _stop(self):
        if self.running:
            self.timer.stop()
            self.running = False
            self.start_btn.setEnabled(True)



    def _reset(self):
        self._stop()
        self.time_left = 0
        self._update_display()
        self.start_btn.setEnabled(True)

    def _tick(self):
        if self.time_left > 0:
            self.time_left -= 1
            self._update_display()
        else:
            self._stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownTimer()
    app.exec_()
