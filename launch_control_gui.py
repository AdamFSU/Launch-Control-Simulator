from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import os
import sys
import random


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('k')
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))
        self.y = [random.randint(0,100) for _ in range(100)]

        # plot data: x, y values
        self.my_line_ref = self.graphWidget.plot(self.x, self.y)

        # for future reference, use a qthread that contains a socket connection,
        # have socket connection run repeatedly (while true) checking for new data,
        # once new data is received fire off qt signal which calls function
        # update_plot_data() and feeding it the received data
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]
        self.y.append(random.randint(0, 100))

        self.my_line_ref.setData(self.x, self.y)


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
