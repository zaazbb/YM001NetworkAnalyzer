
import sys
import time
from datetime import datetime
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
]

def worker(conn):
    ser = serial.Serial('COM12',  115200, parity=serial.PARITY_EVEN, timeout=0)
    buf = bytearray()
    
    while True:
        if ser.in_waiting:
            buf.extend(ser.read(ser.in_waiting))
            #buf.extend(ser.read())
            #print(ser.read(ser.in_waiting))
            i = buf.find(b'\xFE\xFE\xFE\xFE')
            if i != -1:
                if len(buf) >= buf[i+4] + 7:
                    t = datetime.now().strftime('%H:%M:%S %f')
                    conn.send([t, PacketParser(buf[i+4:]), ' '.join('%02X'%ii for ii in buf[i+4:])])
                    del buf[:buf[i+4] + 7]
            else:
                del buf[:]
            
        time.sleep(0.1)

#    time.sleep(1)
#    d = bytearray.fromhex(testdata[0])
#    conn.send([time.time(), PacketParser(d), ' '.join('%02X'%ii for ii in d)])
#    time.sleep(1)
#    d = bytearray.fromhex(testdata[1])
#    conn.send([time.time(), PacketParser(d), ' '.join('%02X'%ii for ii in d)])
#
#    while True:
#        time.sleep(1)
    


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,), daemon=True)
    p.start()

    app = QApplication(sys.argv)
    mainWin = MainWindow(parent_conn)
    mainWin.show()
    
    sys.exit(app.exec_())
    
    p.join()
