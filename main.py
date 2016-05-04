
import sys
import time
from multiprocessing import Process, Pipe

import serial

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from Ui_mainwindow import Ui_MainWindow

from packet import PacketParser



def worker(conn):
    ser = serial.Serial('COM12',  115200, parity=serial.PARITY_EVEN, timeout=0)
    buf = bytearray()
    
    while True:
        if ser.in_waiting:
            buf.extend(ser.read(ser.in_waiting))
            #print(ser.read(ser.in_waiting))
            i = buf.find(b'\xFE\xFE\xFE\xFE')
            if i != -1:
                if len(buf) >= buf[i+4] + 7:
                    conn.send(PacketParser(buf[i+4:]))
                    del buf[:buf[i+4] + 7]
            else:
                del buf[:]
            
        time.sleep(0.1)
    
class MainWindow(QMainWindow):
    def __init__(self, conn):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.conn = conn
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        
        #plainTextEdit
    def update(self):
        if self.conn.poll():
            msg = self.conn.recv()
            print(msg)
            treeWidget

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()

    app = QApplication(sys.argv)
    mainWin = MainWindow(parent_conn)
    mainWin.show()
    
    sys.exit(app.exec_())
    
    p.join()
