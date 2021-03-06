

def get_xval(mapfile):
    with open(mapfile) as f:
        global_area = False
        module = ''
        gvar = []
        for line in f:
            if line.startswith('  -------         MODULE'):
                module = line.rsplit(maxsplit=1)[-1]
                if module[0] != '?':
                    global_area = True
            elif line.startswith('  X:'):
                if global_area:
                    attr = line.rsplit()
                    if attr[2][0] != '?':
                        gvar.append([attr[2], int(attr[0][2:-1], 16), 0, attr[1], module])
            elif line.startswith('  -------         PROC') \
                 or line.startswith('  -------         ENDMOD'):
                global_area = False


    gvar_by_addr = sorted(gvar, key=lambda d:d[1])
    for i in range(len(gvar_by_addr)-1):
        gvar_by_addr[i][2] = gvar_by_addr[i+1][1] - gvar_by_addr[i][1]
    gvar_by_addr[-1][2] = 0x8000 - gvar_by_addr[-1][1]

    return sorted(gvar_by_addr, key=lambda d:d[0])
    

def _chk_xor(d):
    xor = 0
    for i in d:
        xor ^= i
    return xor
    
def mk_rxval(dst, src, index, addr, len):
    template = '43 CD 0F FF FF 45 30 10 03 00 00 55 44 33 22 11 00 F1 06 00 01 00 4A 21 80'
    pkt = bytearray.fromhex(template)
    i = 5
    srcaddr = bytearray.fromhex(dst)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 2
    pkt[i] = index % 0x80
    i += 3
    pkt[i:i+2] = addr.to_bytes(2, 'little')
    i += 2
    pkt[i] = len
    i += 1
    pkt.append(sum(pkt[i-6:i]) % 0x100)
    pkt.append(_chk_xor(pkt[i-6:i]))
    
    return pkt
    
def mk_pooltype(dst, src, index):
    template = '43 CD 00 FF FF 33 21 10 03 00 00 66 55 44 33 22 11 F1 02 01 04'
    pkt = bytearray.fromhex(template)
    i = 5
    srcaddr = bytearray.fromhex(dst.zfill(12))
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 2
    pkt[i] = index % 0x80
    i += 2
    pkt.append(sum(pkt[i-2:i]) % 0x100)
    pkt.append(_chk_xor(pkt[i-2:i]))
    
    return pkt
    
def mk_eraseparam(dst, src, index):
    template = '43 CD 00 FF FF 33 21 10 03 00 00 66 55 44 33 22 11 F1 02 01 05'
    pkt = bytearray.fromhex(template)
    i = 5
    srcaddr = bytearray.fromhex(dst)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 2
    pkt[i] = index % 0x80
    i += 2
    pkt.append(sum(pkt[i-2:i]) % 0x100)
    pkt.append(_chk_xor(pkt[i-2:i]))
    
    return pkt

def mk_rfplcswitch(dst, src, index, rfplc):
    template = '43 CD 00 FF FF 33 21 10 03 00 00 66 55 44 33 22 11 F1 03 01 11 03'
    pkt = bytearray.fromhex(template)
    i = 5
    srcaddr = bytearray.fromhex(dst)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 2
    pkt[i] = index % 0x80
    i += 2
    pkt[i] = rfplc
    i += 1
    pkt.append(sum(pkt[i-3:i]) % 0x100)
    pkt.append(_chk_xor(pkt[i-3:i]))
    
    return pkt
