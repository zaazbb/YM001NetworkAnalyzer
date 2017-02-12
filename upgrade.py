
#import os.path
 

def get_app_code(fcb):
    with open(fcb, 'rb') as f:
        d = f.read()
#        if os.path.splitext(fcb)[1] == '.bin':
#            return d[:0xb700]
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
    
def mk_rdsncfg(dst, src):
    template = '41 CD 01 FF FF 11 11 22 22 33 33 00 00 00 00 00 00 7C 11 11 22 22 33 33 00 00 00 00 00 00 11 01 01 04'
    pkt = bytearray.fromhex(template)
    i = 5
    dstaddr = bytearray.fromhex(dst.zfill(12))
    dstaddr.reverse()
    pkt[i:i+6] = dstaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    # nwk control
    i += 1
    pkt[i:i+6] = dstaddr
    i += 6
    pkt[i:i+6] = srcaddr
    i += 6
    return pkt

def mk_rdverinfo(dst, src):
    template = '41 CD 03 FF FF 09 01 50 24 03 15 66 55 44 33 22 11 7C 09 01 50 24 03 15 66 55 44 33 22 11 20 01 02 FE 4D 59 06'
    pkt = bytearray.fromhex(template)
    i = 5
    dstaddr = bytearray.fromhex(dst.zfill(12))
    dstaddr.reverse()
    pkt[i:i+6] = dstaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    # nwk control
    i += 1
    pkt[i:i+6] = dstaddr
    i += 6
    pkt[i:i+6] = srcaddr
    i += 6
    return pkt
    

if __name__ == '__main__':
    d = get_app_code(r'D:\work\repository\YM001\trunk\software\proj\app\obj\app_with_boot.fcb')
    print(' '.join('%02X'%i for i in d[:128]))
    print(' '.join('%02X'%i for i in d[-256:-128]))
    print(' '.join('%02X'%i for i in d[-128:]))
