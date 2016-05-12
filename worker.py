
import sys
import time
from datetime import datetime

import serial

from packet import PacketParser


testdata = [
'41 CD E0 FF FF 51 01 50 79 08 13 01 00 50 54 10 00 3D 51 01 50 79 08 13 01 00 50 54 10 00 01 12 80'
#'40 CD 01 FF FF FF FF FF FF FF FF 06 05 04 03 02 01 00 01 1A 04 02 00 23 5F DA 3D AA AA AA AA AA AA', 
#'43 CD 10 45 12 35 00 00 00 00 00 06 05 04 03 02 01 01 03 16 00 00 00 00 00 35 00 00 00 00 00 66 55 44 33 22 11 73 00', 
#'41 CD 3D FF FF 45 30 10 03 00 00 01 00 50 54 10 00 3C 45 30 10 03 00 00 01 00 50 54 10 00 11 02 0F 02 68 45 30 10 03 00 00 68 11 04 33 32 34 33 39 16', 
#'41 CF 35 88 88 16 00 00 00 00 00 07 00 00 00 10 00 01 3C 3C 16 00 00 00 00 00 AA AA AA AA AA AA B1 02 23 01 68 59 75 00 00 00 00 68 01 02 43 C3 A7 16', 
#'41 CF 43 88 88 AA AA AA AA AA AA 16 00 00 00 00 00 01 3C 3C AA AA AA AA AA AA 16 00 00 00 00 00 81 00 30 00 00', 
]


def worker(conn, port):
    ser = serial.Serial(port,  115200, parity=serial.PARITY_EVEN, timeout=0)
    buf = bytearray()
    
    while True:
        if ser.in_waiting:
            buf.extend(ser.read(ser.in_waiting))
            #buf.extend(ser.read())
            #print(ser.read(ser.in_waiting))
            i = buf.find(b'\xFE\xFE\xFE\xFE')
            if i != -1:
                if len(buf) >= i + buf[4] + 7:
                    t = datetime.now().strftime('%H:%M:%S %f')
                    #print(' '.join('%02X'%ii for ii in buf[i+8: i+buf[4]+5]))
                    baseinfo, extinfo = PacketParser(buf[i+8: i+buf[4]+5])
                    baseinfo.insert(0, str(t))
                    conn.send([baseinfo, extinfo, ' '.join('%02X'%ii for ii in buf[i+8: i+buf[4]+5])])
                    del buf[: i+buf[4]+7]
            else:
                i = buf.find(b'\xFE')
                if i != -1:
                    del buf[:i]
                else:
                    del buf[:]
        if conn.poll():
            payload = conn.recv()
            pkt = bytearray(b'\xFE\xFE\xFE\xFE\x00\x00\x01\x00')
            pkt.extend(payload)
            pkt[4] = len(payload) + 3
            pkt[7] = pkt[4] ^ pkt[5] ^ pkt[6]
            
            #print(' '.join('%02X'%i for i in pkt))
            ser.write(pkt)

        time.sleep(0.01)

#    for i in testdata:
#        time.sleep(0.5)
#        d = bytearray.fromhex(i)
#        print(' '.join('%02X'%ii for ii in d))
#        t = datetime.now().strftime('%H:%M:%S %f')
#        baseinfo, extinfo = PacketParser(d)
#        baseinfo.insert(0, str(t))
#        conn.send([baseinfo, extinfo, ' '.join('%02X'%ii for ii in d)])
#
#    while True:
#        time.sleep(1)
