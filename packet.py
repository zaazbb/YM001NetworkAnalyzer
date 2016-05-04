
from ctypes import Structure, c_ushort, c_ubyte, c_uint

from crcmod import predefined


SHR = b'\xFE' * 4


class _MacFCD(Structure):
    _fields_ = [('FTD',         c_ushort, 3),
                ('secureEn',    c_ushort, 1),
                ('frmHangup',   c_ushort, 1),
                ('ackReq',      c_ushort, 1),
                ('panIdCompr',  c_ushort, 1),
                ('reserve',     c_ushort, 1),
                ('frmIdxcompr', c_ushort, 1),
                ('extInfoInd',  c_ushort, 1),
                ('dstAddrMode', c_ushort, 2),
                ('frmVer',      c_ushort, 2),
                ('srcAddrMode', c_ushort, 2)]

_MacFrmType = ('Beacon', 'Data', 'Ack', 'Cmd',
               'Reserve', 'Reserve', 'Reserve', 'Reserve')



class _NwkFCD(Structure):
    _fields_ = [('FTD',         c_ubyte, 2),
                ('dstAddrMode', c_ubyte, 2),
                ('srcAddrMode', c_ubyte, 2),
                ('reserve',     c_ubyte, 1),
                ('routeInd',    c_ubyte, 1)]

class _NwkRouteInfo(Structure):
    _fields_ = [('number',      c_uint, 5),
                ('index',       c_uint, 5),
                ('addrMode0',   c_uint, 2),
                ('addrMode1',   c_uint, 2),
                ('addrMode2',   c_uint, 2),
                ('addrMode3',   c_uint, 2),
                ('addrMode4',   c_uint, 2),
                ('addrMode5',   c_uint, 2),
                ('reserve',     c_uint, 2)]

_NwkFrmType = 'Data', 'Cmd', 'Reserve', 'Reserve'


class _ApsFCD(Structure):
    _fields_ = [('FTD',         c_ubyte, 3),
                ('OEI',         c_ubyte, 1),
                ('reserve',     c_ubyte, 4)]

_ApsFrmType = ('AckNAck',  'Cmd', 'Route', 'Report', 
               'Reserve', 'Reserve', 'Reserve', 'Reserve')

    

_AddrLen = 0, 0, 2, 6


def PacketParser(pkt):
#    print(' '.join('%02X' % i for i in pkt))
#    if len(pkt) < 6 or pkt[0] != len(pkt) - 3:
#        return None, 'packet length < 6'
#    if pkt[3] != pkt[0] ^ pkt[1] ^ pkt[2]:
#        return None, 'PHR check error'
#    if predefined.mkCrcFun('x-25')(pkt) != int.from_bytes(pkt[-2:], 'little'):
#        return None, 'crc error'
    #pktdict = {'phy': {'infoChnlIdx': pkt[1], 'stdInd': pkt[2]}}

    i = 4
    
    # parse mac.
    macfcd = _MacFCD.from_buffer(pkt[i:i+2])
    #pktdict['mac'] = {'frmType': macfcd.FTD,
    #                  'frmHangup': macfcd.frmHangup,
    #                  'ackReq': macfcd.ackReq,
    #                  'frmVer': macfcd.frmVer}
    baseinfo = [_MacFrmType[macfcd.FTD], str(macfcd.ackReq)]
    i += 2
    if macfcd.frmIdxcompr:
        #pktdict['mac']['frmIdx'] = pkt[i]
        baseinfo.append(str(pkt[i]))
        i += 1
    else:
        baseinfo.append('')
    if macfcd.panIdCompr:
        #pktdict['mac']['panId'] = int.from_bytes(pkt[i:i+2], 'little')
        baseinfo.append('%02X %02X' % (pkt[i+1], pkt[i]))
        i += 2
    else:
        baseinfo.append('')
    n = _AddrLen[macfcd.dstAddrMode]
    #pktdict['mac']['dstAddr'] = pkt[i:i+n]
    baseinfo.append(' '.join('%02X' % ii for ii in pkt[i:i+n]))
    i += n
    n = _AddrLen[macfcd.srcAddrMode]
    #pktdict['mac']['srcAddr'] = pkt[i:i+n]
    baseinfo.append(' '.join('%02X' % ii for ii in pkt[i:i+n]))
    i += n
    if macfcd.extInfoInd:
        extlen = pkt[i]
        i += 1
        #pktdict['mac']['extInfo'] = pkt[i:i+extlen]
        i += extlen

    if macfcd.FTD == 0:
        # beacon.
        pass
    elif macfcd.FTD == 2:
        # ack.
        pass
    elif macfcd.FTD == 3:
        # command
        pass
    elif macfcd.FTD == 1:
        # data.
        # parse nwk.
        nwkfcd = _NwkFCD.from_buffer(pkt[i:i+1])
        #pktdict['nwk'] = {'frmType': nwkfcd.FTD}
        baseinfo.append(_NwkFrmType[nwkfcd.FTD])
        i += 1
        n = _AddrLen[nwkfcd.dstAddrMode]
        #pktdict['nwk']['dstAddr'] = pkt[i:i+n]
        baseinfo.append(' '.join('%02X' % ii for ii in pkt[i:i+n]))
        i += n
        n = _AddrLen[nwkfcd.srcAddrMode]
        #pktdict['nwk']['srcAddr'] = pkt[i:i+n]
        baseinfo.append(' '.join('%02X' % ii for ii in pkt[i:i+n]))
        i += n
        #pktdict['nwk']['radius'] = pkt[i] & 0x0F
        #pktdict['nwk']['frmIdx'] = pkt[i] >> 4
        baseinfo.append(str(pkt[i] >> 4))
        baseinfo.append(str(pkt[i] & 0x0F))
        i += 1
        if nwkfcd.routeInd:
            routeinfo = _NwkRouteInfo.from_buffer(pkt[i:i+3])
            #pktdict['nwk']['relayIdx'] = routeinfo.index
            routeaddrs = []
            i += 3
            #pktdict['nwk']['relayLst'] = []
            for ii in range(routeinfo.number):
                n = _AddrLen[getattr(routeinfo, 'addrMode%i' % ii)]
                #pktdict['nwk']['relayLst'].append(pkt[i:i+n])
                routeaddrs.append(' '.join('%02X' % ii for ii in pkt[i:i+n]))
                i += n
            baseinfo.append('-'.join(routeaddrs))
        else:
            baseinfo.append('')
                
        if nwkfcd.FTD == 1:
            # command.
            pass
        elif nwkfcd.FTD == 0:
            # data.
            # parse aps.
            apsfcd = _ApsFCD.from_buffer(pkt[i])
            i += 1
            #pktdict['aps'] = {'frmType': apsfcd.FTD, 'frmIdx': pkt[i]}
            baseinfo.append(_ApsFrmType[apsfcd.FTD])
            baseinfo.append(str(pkt[i]))
            if apsfcd.OEI:
                extlen = pkt[i]
                i += 1
                #pktdict['aps']['vendId'] = pkt[i:i+2]
                i += 2
                #pktdict['aps']['extData'] = pkt[i:i+extlen]
                i += extlen
            #pktdict['aps']['DUI'] = pkt[i]
            baseinfo.append(str(pkt[i]))
            i += 1
            if apsfcd.FTD == 0:
                # ack/nack.
                pass
            elif apsfcd.FTD == 1:
                # command.
                pass
            elif apsfcd.FTD == 2:
                # data route.
                pass
            elif apsfcd.FTD == 3:
                # report.
                pass
    #return pktdict
    return baseinfo,
    
if __name__ == '__main__':
    d = bytearray.fromhex(
        '24 00 01 25 40 CD 01 FF FF FF FF FF FF FF FF 06 05 04 03 02 '
        '01 00 01 1A 04 02 00 23 5F DA 3D AA AA AA AA AA AA 1B EA')
    print(PacketParser(d))
