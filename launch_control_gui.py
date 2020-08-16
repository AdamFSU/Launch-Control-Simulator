from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import os
import sys
import random
import socket


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


class SocketConnection(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def establish_connection(self):
        HOST = '127.0.0.1'  # localhost
        PORT = 1234  # port number to use for socket connection

        # AF_INET specifies IPv4, SOCK_STREAM specifies TCP data stream
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # binds socket to our host and port values
            s.bind((HOST, PORT))
            # listen() enables our server to accept() connections
            s.listen()
            # accept() blocks (waits indefinitely) for an incoming connection
            # once a client connects it returns a new socket object representing
            # the connection and a tuple holding the address of the client
            conn, addr = s.accept()
            # with statement is used with conn to automatically close the socket
            # at the end of the block
            with conn:
                print('Connected by', addr)
                # indefinitely loop over blocking calls to conn.recv()
                # reading whatever data the client sends and echo it back
                # using conn.sendall()
                while True:
                    # max buffer size of 1024 bytes
                    data = conn.recv(1024)
                    # if conn.recv() returns an empty bytes object b'', then
                    # the client closed the connection and the loop is terminated.
                    if not data:
                        break
                    conn.sendall(data)


def main():
    sc = SocketConnection()
    sc_thread = QThread()
    sc.moveToThread(sc_thread)
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
