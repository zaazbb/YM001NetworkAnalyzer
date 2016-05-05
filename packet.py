
from ctypes import Structure, c_ushort, c_ubyte, c_uint

#from crcmod import predefined


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
               
class TimeslotLevel(Structure):
    _fields_ = [('timeSlot',    c_ushort,  10), 
                    ('level',   c_ushort,  4), 
                    ('reserve',  c_ushort,  2)]

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

#NwkCmdType = (
#    '--',  'joinNwkReq', 'joinNwkResp', 'routeErr', 
#    '--',  '--',  '--',  '--',  '--',  '--',  
#    'fiGatherCmd', 'fiGatherResp',  'cfgSn',  
#    'cfgSnResp',  '--',  '--',  
#    'fNdRdy')

class NwkCfgSnOpt(Structure):
    _fields_ = [('timeSlot', c_ubyte, 1), 
                    ('level', c_ubyte, 1), 
                    ('chnlGrp', c_ubyte, 1), 
                    ('shortAddr', c_ubyte, 1), 
                    ('panId', c_ubyte, 1), 
                    ('relayLst', c_ubyte, 1), 
                    ('reserve', c_ubyte, 1), 
                    ('offline', c_ubyte, 1)]


class _ApsFCD(Structure):
    _fields_ = [('FTD',         c_ubyte, 3),
                ('OEI',         c_ubyte, 1),
                ('reserve',     c_ubyte, 4)]

_ApsFrmType = ('AckNAck',  'Cmd', 'Route', 'Report', 
               'Reserve', 'Reserve', 'Reserve', 'Reserve')

ApsBaudrate = 'auto', '1200', '2400', '4800',  '9600', '19200'
ApsTsmtPower = {0:'16dBm', 1:'10dBm', 2:'4dBm', 3:'-2dBm'}

_AddrLen = 0, 0, 2, 6


def reverse_hex(addr):
    addr.reverse()
    return addr.hex().upper()

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
    cmdinfo = [{}, {}]
    i += 2
    if macfcd.frmIdxcompr:
        #pktdict['mac']['frmIdx'] = pkt[i]
        baseinfo.append(str(pkt[i]))
        i += 1
    else:
        baseinfo.append('')
    if macfcd.panIdCompr:
        #pktdict['mac']['panId'] = int.from_bytes(pkt[i:i+2], 'little')
        baseinfo.append(reverse_hex(pkt[i:i+2]))
        i += 2
    else:
        baseinfo.append('')
    n = _AddrLen[macfcd.dstAddrMode]
    #pktdict['mac']['dstAddr'] = pkt[i:i+n]
    baseinfo.append(reverse_hex(pkt[i:i+n]))
    i += n
    n = _AddrLen[macfcd.srcAddrMode]
    #pktdict['mac']['srcAddr'] = pkt[i:i+n]
    baseinfo.append(reverse_hex(pkt[i:i+n]))
    i += n
    if macfcd.extInfoInd:
        extlen = pkt[i]
        i += 1
        #pktdict['mac']['extInfo'] = pkt[i:i+extlen]
        i += extlen

    if macfcd.FTD == 0:
        # beacon.
        cmdinfo[0]['cmdInfo'] = 'mBeacon'
        cmdinfo[1] = parse_beacon(pkt[i:])
    elif macfcd.FTD == 2:
        # ack.
        #cmdinfo[0]['cmdInfo'] = 'mAck'
        pass
    elif macfcd.FTD == 3:
        # command
        cmdinfo[0]['cmdInfo'] = 'mCmd'
        i += 1
        if pkt[i] == 1:
            # network maintain req.
            cmdinfo[0]['cmdType'] = 'nwkMaintainReq'
            i += 1
            pathn = pkt[i] & 0x0F
            cmdinfo[1]['pathNodeNum'] = str(pathn)
            cmdinfo[1]['pathIdx'] = str(pkt[i] >> 4)
            i += 1
            # pkt[0]+1-i = xn+n-1, 
            # x = (pkt[0]+2-i)/n - 1
            n = (pkt[0]+2-i)//pathn - 1
            routers = []
            fipowers = []
            for ii in range(pathn):
                routers.append(reverse_hex(pkt[i:i+n]))
                i += n
            for ii in range(pathn-1):
                fipowers.append('%02X' % pkt[i])
                i += 1
            cmdinfo[1]['routers'] = '-'.join(routers)
            cmdinfo[1]['fiPowers'] = '-'.join(fipowers)
        else:
            # network maintain resp.
            cmdinfo[0]['cmdType'] = 'nwkMaintainResp'
            pathn = pkt[i] & 0x0F
            cmdinfo[1]['pathNodeNum'] = str(pathn)
            cmdinfo[1]['pathIdx'] = str(pkt[i] >> 4)
            i += 1
            # pkt[0]+1-i = xn+2n-2, 
            # x = (pkt[0]+3-i)/n - 2
            n = (pkt[0]+3-i)//pathn - 2
            routers = []
            fiDnpowers = []
            fiUpPowers = []
            for ii in range(pathn):
                routers.append(reverse_hex(pkt[i:i+n]))
                i += n
            for ii in range(pathn-1):
                fiDnpowers.append('%02X' % pkt[i])
                i += 1
            for ii in range(pathn-1):
                fiUpPowers.append('%02X' % pkt[i])
                i += 1
            cmdinfo[1]['routers'] = '-'.join(routers)
            cmdinfo[1]['fiDnPowers'] = '-'.join(fiDnpowers)
            cmdinfo[1]['fiUpPowers'] = '-'.join(fiUpPowers)
            
    elif macfcd.FTD == 1:
        # data.
        # parse nwk.
        nwkfcd = _NwkFCD.from_buffer(pkt[i:i+1])
        #pktdict['nwk'] = {'frmType': nwkfcd.FTD}
        baseinfo.append(_NwkFrmType[nwkfcd.FTD])
        i += 1
        n = _AddrLen[nwkfcd.dstAddrMode]
        #pktdict['nwk']['dstAddr'] = pkt[i:i+n]
        baseinfo.append(reverse_hex(pkt[i:i+n]))
        i += n
        n = _AddrLen[nwkfcd.srcAddrMode]
        #pktdict['nwk']['srcAddr'] = pkt[i:i+n]
        baseinfo.append(reverse_hex(pkt[i:i+n]))
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
                routeaddrs.append(reverse_hex(pkt[i:i+n]))
                i += n
            baseinfo.append('-'.join(routeaddrs))
        else:
            baseinfo.append('')
                
        if nwkfcd.FTD == 1:
            # command.
            cmdinfo[0]['cmdInfo'] = 'nCmd'
            if pkt[i] == 1:
                # joinNwkReq
                cmdinfo[0]['cmdType'] = 'joinNwkReq'
                i += 1
                cmdinfo[1]['cmdOpt'] = '%02X'%pkt[i]
            elif pkt[i] == 2:
                # joinNwkResp
                cmdinfo[0]['cmdType'] = 'joinNwkResp'
                i += 1
                cmdinfo[1]['cmdOpt'] = '%02X'%pkt[i]
                i += 1
                cmdinfo[1]['panId'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo[1]['cnAddr'] = reverse_hex(pkt[i:i+n])
                i += 6
                tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
                cmdinfo[1]['timeSlot'] = str(tslotlv.timeSlot)
                cmdinfo[1]['level'] = str(tslotlv.level)
                i += 2
                cmdinfo[1]['rssi'] = str(pkt[i])
                i += 1
                n = pkt[i]
                cmdinfo[1]['relayNum'] = str(pkt[i])
                i += 1
                relays = []
                for ii in range(n):
                    relays.append(reverse_hex(pkt[i:i+2]))
                    i += 2
                cmdinfo[1]['relays'] = '-'.join(relays)
            elif pkt[i] == 3:
                # routeErr
                cmdinfo[0]['cmdType'] = 'routeErr'
                i += 1
                cmdinfo[1]['errCode'] = 'noResp' if pkt[i] == 1 else '--'
                i += 1
                n = _AddrLen[nwkfcd.dstAddrMode]
                cmdinfo[1]['failAddr'] = reverse_hex(pkt[i:i+n])
            elif pkt[i] == 0x10:
                # fiGatherCmd
                cmdinfo[0]['cmdType'] = 'fiGatherCmd'
                i += 1
                cmdinfo[1]['pgIdx'] = str(pkt[i] & 0x0F)
            elif pkt[i] == 0x11:
                # fiGatherResp
                i += 1
                cmdinfo[0]['cmdType'] = 'fiGatherResp'
                cmdinfo[1]['pgIdx'] = str(pkt[i] & 0x0F)
                cmdinfo[1]['totPg'] = str(pkt[i] >> 4)
                i += 1
                n = pkt[i]
                neighbors = []
                for ii in range(n):
                    neighbors.append('%s:%02X',  (reverse_hex(pkt[i:i+6]),  pkt[i+6]))
                    i += 7
                cmdinfo[1]['neighbors'] = '-'.join(neighbors)
            elif pkt[i] == 0x12:
                # cfgSn
                cmdinfo[0]['cmdType'] = 'cfgSn'
                i += 1
                opt = NwkCfgSnOpt.from_buffer(pkt[i:i+1])
                i += 1
                cmdinfo[1]['offline'] = str(opt.offline)
                if opt.chnlGrp:
                    cmdinfo[1]['chnlGrp'] = str(pkt[i])
                    i += 1
                tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
                if opt.timeSlot:
                    cmdinfo[1]['timeSlot'] = str(tslotlv.timeSlot)
                if opt.level:
                    cmdinfo[1]['level'] = str(tslotlv.level)
                i += 2
                if opt.shortAddr:
                    cmdinfo[1]['shortAddr'] =  reverse_hex(pkt[i:i+2])
                    i += 2
                if opt.panId:
                    cmdinfo[1]['panId'] =  reverse_hex(pkt[i:i+2])
                    i += 2
                if opt.relayLst:
                    n = pkt[i]
                    cmdinfo[1]['relayNum'] = str(n)
                    i += 1
                    relayLst = []
                    for ii in range(n):
                        nn = pkt[i]
                        i += 1
                        relays = []
                        for iii in range(nn):
                            relays.append(reverse_hex(pkt[i:i+2]))
                            i += 2
                        relayLst.append('-'.join(relays))
                    cmdinfo[1]['relayLst'] = ','.join(relayLst) 
            elif pkt[i] == 0x13:
                # cfgSnResp
                cmdinfo[0]['cmdType'] = 'cfgSnResp'
                i += 1
                cmdinfo[1]['cmdOpt'] = str(pkt[i])
                i += 1
                cmdinfo[1]['hVer'] =  pkt[i:i+2].hex().upper()
                i += 2
                cmdinfo[1]['sVer'] =  pkt[i:i+3].hex().upper()
            elif pkt[i] == 0x16:
                # fNdRdy
                cmdinfo[0]['cmdType'] = 'fNdRdy'
                i += 1
                cmdinfo[1]['cmdOpt'] = str(pkt[i])
                i += 1
                tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
                cmdinfo[1]['timeSlot'] = str(tslotlv.timeSlot)
                cmdinfo[1]['level'] =str( tslotlv.level)
        elif nwkfcd.FTD == 0:
            # data.
            # parse aps.
            apsfcd = _ApsFCD.from_buffer(pkt[i:i+1])
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
            if apsfcd.FTD == 0:
                # ack/nack.
                cmdinfo[0]['cmdInfo'] = 'aAckNack'
                cmdinfo[0]['cmdType'] = 'ack' if pkt[i] else 'nack'
            elif apsfcd.FTD == 1:
                # command.
                cmdinfo[0]['cmdInfo'] = 'aCmd'
                if pkt[i] == 0:
                    cmdinfo[0]['cmdType'] = 'cfgUart'
                    i += 1
                    if pkt[i] > 5:
                        cmdinfo[1]['baudrate'] = '--'
                    else:
                        cmdinfo[1]['baudrate'] = ApsBaudrate[pkt[i]]
                    i += 1
                    if pkt[i] == 0:
                        cmdinfo[1]['parity'] = 'none'
                    elif pkt[i] == 1:
                        cmdinfo[1]['parity'] = 'odd'
                    elif pkt[i] == 2:
                        cmdinfo[1]['parity'] = 'even'
                    else:
                        cmdinfo[1]['parity'] = 'invalid'
                if pkt[i] == 1:
                    cmdinfo[0]['cmdType'] = 'setChnlGrp'
                    i += 1
                    cmdinfo[1]['chnlGrp'] = str(pkt[i])
                if pkt[i] == 2:
                    cmdinfo[0]['cmdType'] = 'setRssi'
                    i += 1
                    cmdinfo[1]['rssi'] = str(pkt[i])
                if pkt[i] == 3:
                    cmdinfo[0]['cmdType'] = 'setTsmtPower'
                    i += 1
                    cmdinfo[1]['tsmtPower'] = ApsTsmtPower.get(pkt[i], '--')
                if pkt[i] == 4:
                    cmdinfo[0]['cmdType'] = 'rdNodeCfg'
                    i += 1
                    cmdinfo[1]['factoryAddr'] = reverse_hex(pkt[i:i+6])
                    i += 6
                    cmdinfo[1]['nodeType'] = str(pkt[i])
                    i += 1
                    cmdinfo[1]['panId'] = reverse_hex(pkt[i:i+2])
                    i += 2
                    cmdinfo[1]['shortAddr'] = reverse_hex(pkt[i:i+2])
                    i += 2
                    cmdinfo[1]['vendId'] = reverse_hex(pkt[i:i+2])
                    i += 2
                    cmdinfo[1]['hVer'] = reverse_hex(pkt[i:i+2])
                    i += 2
                    cmdinfo[1]['sVer'] = reverse_hex(pkt[i:i+3])
                    i += 3
                    cmdinfo[1]['tsmtPower'] = ApsTsmtPower.get(pkt[i], '--')
                    i += 1
                    cmdinfo[1]['rssi'] = str(pkt[i])
                    i += 1
                    cmdinfo[1]['chnlGrp'] = str(pkt[i])
                    i += 1
                    tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
                    cmdinfo[1]['timeSlot'] = str(tslotlv.timeSlot)
                    cmdinfo[1]['level'] = str(tslotlv.level)
                    i += 2
                    cmdinfo[1]['nwkCapacity'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                    i += 2
                    n = pkt[i]
                    cmdinfo[1]['relayNum'] = str(n)
                    i += 1
                    relayLst = []
                    for ii in range(n):
                        nn = pkt[i]
                        i += 1
                        relays = []
                        for iii in range(nn):
                            relays.append(reverse_hex(pkt[i:i+2]))
                            i += 2
                        relayLst.append('-'.join(relays))
                    cmdinfo[1]['relayLst'] = ','.join(relayLst) 
                if pkt[i] == 5:
                    cmdinfo[0]['cmdType'] = 'devReboot'
                if pkt[i] == 6:
                    cmdinfo[0]['cmdType'] = 'softUpgrade'
                    i += 1
                    cmdinfo[0]['vendId'] = pkt[i:i+2].hex().upper()
                    i += 2
                    cmdinfo[0]['devType'] = str(pkt[i])
                    i += 1
                    cmdinfo[1]['totPkt'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                    i += 2
                    cmdinfo[1]['curPkt'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                if pkt[i] == 7:
                    cmdinfo[0]['cmdType'] = 'bcastTiming'
                    i += 1
                    cmdinfo[1]['bcastFrmIdx'] = str(pkt[i])
                    i += 1
                    tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
                    cmdinfo[1]['timeSlot'] = str(tslotlv.timeSlot)
                    cmdinfo[1]['level'] = str(tslotlv.level)
                    i += 2
                    cmdinfo[1]['maxDly'] = str(int.from_bytes(pkt[i:i+4], 'little'))
            elif apsfcd.FTD == 2:
                # data route.
                cmdinfo[0]['cmdInfo'] = 'aRoute'
                if pkt[i] > 5:
                    cmdinfo[1]['baudrate'] = '--'
                else:
                    cmdinfo[1]['baudrate'] = ApsBaudrate[pkt[i]]
            elif apsfcd.FTD == 3:
                # report.
                cmdinfo[0]['cmdInfo'] = 'aReport'
                if pkt[i] == 0:
                    cmdinfo[1]['reportType'] = 'evtReprot'
                    i += 1
                    if pkt[i] == 0:
                        cmdinfo[1]['reportInfo'] = 'meterEvt'
                    elif pkt[i] == 1:
                        cmdinfo[1]['reportInfo'] = 'snEvt'
                    else:
                        cmdinfo[1]['reportInfo'] = '--'
                else:
                    cmdinfo[1]['reportType'] = '--'
    #return pktdict
    return baseinfo, cmdinfo
    

def parse_beacon(pkt):
    i = 0
    cmdinfo = {}
    cmdinfo['tsmtRndDly'] = str(pkt[i])
    i += 1
    cmdinfo['beaconRound'] = str(pkt[i])
    i += 1
    tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
    cmdinfo['timeSlot'] = str(tslotlv.timeSlot)
    cmdinfo['level'] = str(tslotlv.level)
    i += 2
    cmdinfo['beaconInd'] = str(pkt[i])
    i += 1
    cmdinfo['nwkCapacity'] =  str(int.from_bytes(pkt[i:i+2], 'little'))
    i += 2
    cmdinfo['fiThreshold'] = str(pkt[i])
    i += 1
    cmdinfo['cnPanId'] =  reverse_hex(pkt[i:i+2])
    i += 2
    cmdinfo['cnAddr'] = reverse_hex(pkt[i:i+6])
    #i += 6
    return cmdinfo

    
if __name__ == '__main__':
    d = bytearray.fromhex(
        '24 00 01 25 40 CD 01 FF FF FF FF FF FF FF FF 06 05 04 03 02 '
        '01 00 01 1A 04 02 00 23 5F DA 3D AA AA AA AA AA AA 1B EA')
    print(PacketParser(d))
