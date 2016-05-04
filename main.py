
import sys
import time
from multiprocessing import Process, Pipe

import serial

from PyQt5.QtWidgets import QApplication

from packet import PacketParser
from mainwindow import MainWindow


testdata = [
    '24 00 01 25 40 CD 01 FF FF FF FF FF FF FF FF 06 05 04 03 02 01 00 01 '
    '1A 04 02 00 23 5F DA 3D AA AA AA AA AA AA 1B EA', 
    '2A 02 01 29 43 CD 10 45 12 35 00 00 00 00 00 06 05 04 03 02 01 01 03 '
    '16 00 00 00 00 00 35 00 00 00 00 00 66 55 44 33 22 11 73 00 E1 53', 
    '25 00 01 24 41 CD CA FF FF 23 AA AA AA AA AA 06 05 04 03 02 01 3C 23 '
    'AA AA AA AA AA 06 05 04 03 02 01 01 00 01 01 10 A8'
]

def worker(conn):
#    ser = serial.Serial('COM12',  115200, parity=serial.PARITY_EVEN, timeout=0)
#    buf = bytearray()
#    
#    while True:
#        if ser.in_waiting:
#            buf.extend(ser.read(ser.in_waiting))
#            #print(ser.read(ser.in_waiting))
#            i = buf.find(b'\xFE\xFE\xFE\xFE')
#            if i != -1:
#                if len(buf) >= buf[i+4] + 7:
#                    conn.send(PacketParser(buf[i+4:]))
#                    del buf[:buf[i+4] + 7]
#            else:
#                del buf[:]
#            
#        time.sleep(0.1)

    time.sleep(1)
    conn.send(PacketParser(bytearray.fromhex(testdata[0])))
    time.sleep(1)
    conn.send(PacketParser(bytearray.fromhex(testdata[1])))
    time.sleep(1)
    conn.send(PacketParser(bytearray.fromhex(testdata[2])))

    while True:
        time.sleep(1)
    


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()

    app = QApplication(sys.argv)
    mainWin = MainWindow(parent_conn)
    mainWin.show()
    
    sys.exit(app.exec_())
    
    p.join()
