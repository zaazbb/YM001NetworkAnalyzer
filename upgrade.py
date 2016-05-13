
import time
from datetime import datetime

import serial

from packet import PacketParser


port = 'COM12'

#selfaddr = 112233445566
selfaddr = 3102133
sn = 111111111111

fcb = r'D:\work\repository\YM001\software\YM001_APP2\obj\ht8910_g3_trans\ht8910_g3_phy_band3_robo_all.fcb'


def mk_upg02(src, flen, sver, crc):
    template = '43 CD 01 FF FF FF FF FF FF FF FF 33 21 10 03 00 00 F0 02 01 00 01 00 02 6E 01 88 77 1D 4D 95 28 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
    pkt = bytearray.fromhex(template)
    i = 11
    srcaddr = bytearray.fromhex('%012i' % src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 7
    pkt[i:i+2] = flen.to_bytes(2, 'little')
    i += 2
    sver &= 0xFFFF
    pkt[i:i+2] = sver.to_bytes(2, 'little')
    i += 2
    pkt[i:i+4] = crc.to_bytes(4, 'little')
    return pkt

def mk_upg04(src, flen, crc, index, d):
    template = '43 CD 01 FF FF FF FF FF FF FF FF 33 21 10 03 00 00 F0 04 01 00 6E 01 1D 4D 95 28 01 00 80'
    pkt = bytearray.fromhex(template)
    i = 11
    srcaddr = bytearray.fromhex('%012i' % src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 4
    pkt[i:i+2] = flen.to_bytes(2, 'little')
    i += 2
    pkt[i:i+4] = crc.to_bytes(4, 'little')
    i += 4
    pkt[i:i+2] = index.to_bytes(2, 'little')
    pkt.extend(d)
    return pkt

def mk_chng2txm(dst, src):
    template = '63 CD 01 FF FF 11 11 22 22 33 33 FF FF FF FF FF FF F0 03 01 00 01 FF FF FF FF FF FF 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
    pkt = bytearray.fromhex(template)
    i = 5
    srcaddr = bytearray.fromhex('%012i' % dst)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    srcaddr = bytearray.fromhex('%012i' % src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    return pkt

def mk_bpsts(dst, src):
    template = '63 CD 01 FF FF 11 11 22 22 33 33 FF FF FF FF FF FF F0 06'
    pkt = bytearray.fromhex(template)
    i = 5
    srcaddr = bytearray.fromhex('%012i' % dst)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    srcaddr = bytearray.fromhex('%012i' % src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    return pkt

def addphy(payload):
    pkt = bytearray(b'\xFE\xFE\xFE\xFE\x00\x00\x01\x00')
    pkt.extend(payload)
    pkt[4] = len(payload) + 3
    pkt[7] = pkt[4] ^ pkt[5] ^ pkt[6]
    return pkt
    

def get_app_code(fcb):
    with open(fcb, 'rb') as f:
        d = f.read()
        # 0 - reserve, 1 - ht8550, 3 - ht8910/ht8912.
        if d[8] != 3:
            print('fcb is not for ht8912')
            return
        # 0 - download file, 1 - iap file.
        if d[12] != 0:
            print('fcb is not a download file')
            return
        i = 32
        while i < len(d):
            
            length = int.from_bytes(d[i:i+2], 'little')
            i += 2
            addr = int.from_bytes(d[i:i+3], 'little')
            i += 3
            # 0 - global addr, 1 - int_flash addr, 2 - ext_flash addr.
            addrtype = d[i]
            i += 1
            i += 10
            #print(hex(length))
            #print(hex(addr))
            #print(addrtype)
            if addrtype == 1 and addr == 0x10000:
                return d[i:i+length]
            else:
                i += length

def printbuf(buf):
    print(' '.join(['%02X' % i for i in buf]))

def read_pkt(ser, pktname, src, timeout):
    srcaddr = bytearray.fromhex('%012i' % src)
    srcaddr.reverse()
    srcstr = srcaddr.hex().upper()
    buf = bytearray()
    tt = time.time()
    while time.time() - tt < timeout:
        print(time.time() - tt)
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
                    #conn.send([baseinfo, extinfo, ' '.join('%02X'%ii for ii in buf[i+8: i+buf[4]+5])])
                    if baseinfo[1] == pktname and baseinfo[6] == srcstr:
                        return baseinfo, extinfo
                    del buf[: i+buf[4]+7]
            else:
                i = buf.find(b'\xFE')
                if i != -1:
                    del buf[:i]
                else:
                    del buf[:]
        #time.sleep(0.01)

def is_recv_all_pkt(totfrm):
    bits = {0,0x01,0x03,0x07,0x0F,0x1F,0x3F,0x7F};

    d = totfrm // 8
    r = totfrm % 8

    if r:
        if sflag[d] != bits[r]:
            return False

    for i in range(d):
        if sflag[i] != 0xFF:
            return False
    return True

if __name__ == '__main__':
    
    
    d = get_app_code(fcb)

##    with open('app.bin', 'rb') as f:
##        d = f.read()[:0xb700]
    
    flen = d[0x400+2]+d[0x400+7]*0x100
    sver = int.from_bytes(d[0x100:0x100+4], 'big')
    crc = int.from_bytes(d[-4:], 'big')
    
    ser = serial.Serial(port,  115200, parity=serial.PARITY_EVEN, timeout=0)

    while True:
        ser.write(addphy(mk_bpsts(sn, selfaddr)))
        
        resp = read_pkt(ser, 'mcUpgBpStsAck', selfaddr, 2)
        bpflag = b'\xFF' * 64
        if resp:
            print(resp[1]['bpFlag'])
            print(resp[1]['bpRate'])
            bpflag = bytes.frombytes(resp[1]['bpFlag'])
            if is_recv_all_pkt(flen):
                break
        ser.write(addphy(mk_upg02(selfaddr, flen, sver, crc)))
        n = 0
        goto = 0
        for flag in bpflag:
            for i in range(8):
                if ((flag >> i) & 1) == 0:
                    ser.write(addphy(mk_upg04(selfaddr, flen, crc, n+1,
                                              d[n*128:n*128+128])))
                    print(n, end='-')
                n += 1
                if n == flen:
                    goto = 1
                    break
            if goto:
                break
    print('upgrade finished.')
    
