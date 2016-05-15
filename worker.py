
#import sys
import time
from datetime import datetime
import traceback

import serial

from packet import PacketParser


testdata = [
'41 CD 01 FF FF 00 00 00 00 00 00 11 11 11 11 11 11 7C 00 00 00 00 00 00 11 11 11 11 11 11 11 01 01 04 11 11 11 11 11 11 03 FF FF 00 00 01 00 01 00 66 55 00 00 00 00 00 00 00 00 00', 
'43 CD 01 FF FF FF FF FF FF FF FF 11 11 11 11 11 11 F0 96 6E 01 F5 FD FF FF FF 26 E0 FA FF FF FF 7F FF FE FF FF FF FF FF FF FF FF FF FF FF FF DF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00', 
]


def worker(conn, port):
    try:
        ser = serial.Serial(port,  115200, parity=serial.PARITY_EVEN, timeout=0)
    except:
        #conn.send(['err', "can't open %s" % port])
        conn.send(['err', traceback.format_exc()])
    buf = bytearray()
    
    while True:
        if ser.in_waiting:
            try:
                buf.extend(ser.read(ser.in_waiting))
            except:
                conn.send(['err', traceback.format_exc()])
            #buf.extend(ser.read())
            #print(ser.read(ser.in_waiting))
            i = buf.find(b'\xFE\xFE\xFE\xFE')
            if i != -1:
                if len(buf) >= i + buf[4] + 7:
                    t = datetime.now().strftime('%H:%M:%S %f')
                    #print(' '.join('%02X'%ii for ii in buf[i+8: i+buf[4]+5]))
                    try:
                        pktstr = ' '.join('%02X'%ii for ii in buf[i+8: i+buf[4]+5])
                        baseinfo, extinfo = PacketParser(buf[i+8: i+buf[4]+5])
                        baseinfo.insert(0, str(t))
                        conn.send(['pkt', baseinfo, extinfo, pktstr])
                    except:
                        #conn.send(['err', 'parsePktError:' + pktstr])
                        conn.send(['err', traceback.format_exc()])
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
            try:
                ser.write(pkt)
            except:
                conn.send(['err', traceback.format_exc()])

        time.sleep(0.01)


#    for i in testdata:
#        time.sleep(0.5)
#        d = bytearray.fromhex(i)
#        print(' '.join('%02X'%ii for ii in d))
#        t = datetime.now().strftime('%H:%M:%S %f')
#        baseinfo, extinfo = PacketParser(d)
#        baseinfo.insert(0, str(t))
#        conn.send(['pkt', baseinfo, extinfo, ' '.join('%02X'%ii for ii in d)])
#    
#    rxded = [0, 0]
#
#    while True:
#        if conn.poll():
#            payload = conn.recv()
#            if payload[17:17+2] == b'\xF0\x06':
#                addr = payload[5:5+6]
#                addr.reverse()
#                d = None
#                if addr == b'\x11' * 6:
#                    if rxded[0] == 0:
#                        rxded[0] = 1
#                        d = bytearray.fromhex('43 CD 01 FF FF FF FF FF FF FF FF 11 11 11 11 11 11 F0 96 6E 01 F5 FD FF FF FF 26 E0 FA FF FF FF 7F FF FE FF FF FF FF FF FF FF FF FF FF FF FF DF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
#                    else:
#                        rxded[0] = 1
#                elif addr == bytes.fromhex('000003100063'):
#                    if rxded[1] == 0:
#                        rxded[1] = 1
#                        d = bytearray.fromhex('43 CD 01 FF FF FF FF FF FF FF FF 63 00 10 03 00 00 F0 96 6E 01 FF FF FF F0 0F FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
#                if d:
#                    t = datetime.now().strftime('%H:%M:%S %f')
#                    baseinfo, extinfo = PacketParser(d)
#                    baseinfo.insert(0, str(t))
#                    conn.send(['pkt', baseinfo, extinfo, ' '.join('%02X'%ii for ii in d)])
#        time.sleep(0.01)
