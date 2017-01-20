
import os.path
import pickle
from datetime import datetime
#import traceback

from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QMenu, QFileDialog
from PyQt5.QtGui import QBrush, QCursor
from PyQt5.QtCore import QTimer, pyqtSlot, Qt, QPoint

from Ui_mainwindow import Ui_MainWindow

import upgrade
import rdebug

# known issue:
# 1, packet disp data error, when parse pkt disped.


class MainWindow(QMainWindow):
    def __init__(self, conn_file, nodes, chnlgrp, config):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.splitter_cmdinfo.setStretchFactor(0, 1)
        self.ui.splitter_h.setStretchFactor(0, 1)
        self.ui.splitter_v.setStretchFactor(0, 1)
        self.__rightSideBar_isShrinked = False
        self.__rightSideBar_lastIndex = self.ui.tabWidget_rightSideBar.currentIndex()
        self.__bottomSideBar_isShrinked = False
        self.__bottomSideBar_lastIndex = self.ui.tabWidget_bottomSideBar.currentIndex()
        
        self.node = nodes
        self.config = config
        self.highlight = {}
        
        node = nodes['mnode'][0]
        root = QTreeWidgetItem(None, [node])
        if nodes['mnode'][1]:
            color = getattr(Qt, nodes['mnode'][1])
            self.highlight[node] = color
            root.setBackground(0, color)
        self.ui.treeWidget_node.addTopLevelItem(root)
        for k, v in nodes['node'].items():
            item = QTreeWidgetItem(root, [k])
            item.setTextAlignment(0, Qt.AlignRight)
            nodes['node'][k]['item'] = item
            if v['color']:
                color = getattr(Qt, v['color'])
                item.setBackground(0, color)
                self.highlight[k] = color
            self.ui.treeWidget_node.addTopLevelItem(item)
        if nodes['xnode']:
            root = QTreeWidgetItem(None, ['xnode'])
            root.setTextAlignment(0, Qt.AlignRight)
            self.ui.treeWidget_node.addTopLevelItem(root)
            for k, v in nodes['xnode'].items():
                item = QTreeWidgetItem(root, [k])
                if v:
                    color = getattr(Qt, v)
                    item.setBackground(0, color)
                    self.highlight[k] = color
                self.ui.treeWidget_node.addTopLevelItem(item)
        self.ui.treeWidget_node.expandAll()
        for i in range(self.ui.treeWidget_node.columnCount()):
             self.ui.treeWidget_node.resizeColumnToContents(i)

        if os.path.exists(config['rdebug']['mapfile']):
            self.rdbglst = rdebug.get_xval(config['rdebug']['mapfile'])
            for i in self.rdbglst:
                item = QTreeWidgetItem(None, [i[0], '%04X'%i[1],  str(i[2])])
                self.ui.treeWidget_rdbglst.addTopLevelItem(item)
                if i[0] == 'gParamData':
                    self.ui.treeWidget_rdbglst.setCurrentItem(item)
                    self.on_treeWidget_rdbglst_itemClicked(item, 0)
            for i in range(self.ui.treeWidget_rdbglst.columnCount()):
                 self.ui.treeWidget_rdbglst.resizeColumnToContents(i)
             
        self.rdbgidx = 0
        self.ui.comboBox_cmd.keyReleaseEvent = self.keyReleaseEvent
        
        self.buf = []
        self.conn = None
        if conn_file:
            if isinstance(conn_file, str):
                if os.path.exists(conn_file):
                    self.load_file(conn_file)
            else:
                self.conn = conn_file
                self.ui.comboBox_chnlgrp.setEnabled(True)
                self.ui.pushButton_parsepkt.setEnabled(True)
                self.ui.pushButton_upgrade.setEnabled(True)
                self.ui.pushButton_rdbgsend.setEnabled(True)
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update)
                self.timer.start(100)     
                self.upgsrc = self.config['upgrade']['srcaddr'][:12].lstrip('0')
                self.upgtimer = QTimer(self)
                self.upgtimer.setSingleShot(True)
                self.upgtimer.timeout.connect(self.upgrade)
                self.txtimer = QTimer(self)
                self.txtimer.setSingleShot(True)
                self.txtimer.timeout.connect(self.txpacket)
                self.ui.comboBox_chnlgrp.setCurrentIndex(chnlgrp)
                sendchnls = config['DEFAULT']['sendchannel']
                self.__sendchnl = int(sendchnls, 16 if sendchnls.startswith('0x') else 10)

        self.__whosyourdaddy = os.path.exists('whosyourdaddy')
        if not self.__whosyourdaddy:
            self.ui.pushButton_rdbgsend.setEnabled(False)
            self.ui.pushButton_rfplcsw.setEnabled(False)
            self.ui.pushButton_upgrade.setEnabled(False)
            

    def load_file(self, file):
        with open(file, 'rb') as f:
            self.buf = pickle.load(f)
            self.ui.treeWidget.clear()
            for i in self.buf:
                self.add_treeitem(i)
            for i in range(self.ui.treeWidget.columnCount()):
                 self.ui.treeWidget.resizeColumnToContents(i)

    def add_treeitem(self, rdata):
        item = QTreeWidgetItem(None, rdata[0])
        for i in range(6, 6+len(rdata[0][6:10])):
            if rdata[0][i] in self.highlight:
                item.setBackground(i, QBrush(self.highlight[rdata[0][i]]))
            item.setTextAlignment(i, Qt.AlignRight)
        self.ui.treeWidget.addTopLevelItem(item)
        # rowdata[0][?]: 6 - mdst, 7 - msrc, 8 - ndst, 9 - nsrc.
        if rdata[0][2] == 'acRdNdCfgUp':
            if rdata[0][9] in self.node['node']:
                self.node['node'][rdata[0][9]]['item'] .setText(1, rdata[1]['sVer'])
                self.ui.treeWidget_node.resizeColumnToContents(1)
        elif rdata[0][2] == 'acxRdVerInfoUp':
            if rdata[0][9] in self.node['node']:
                self.node['node'][rdata[0][9]]['item'] .setText(1, rdata[1]['sver'])
                self.node['node'][rdata[0][9]]['item'] .setText(2, rdata[1]['date'])
                self.node['node'][rdata[0][9]]['item'] .setText(3, rdata[1]['time'])
                self.ui.treeWidget_node.resizeColumnToContents(1)
                self.ui.treeWidget_node.resizeColumnToContents(2)
                self.ui.treeWidget_node.resizeColumnToContents(3)
        elif rdata[0][2] == 'mcUpgBpStsAck':
            if rdata[0][7] in self.node['node']:
                #print(rdata)
                self.node['node'][rdata[0][7]]['bpFlag'] = rdata[1]['bpFlag']
                self.node['node'][rdata[0][7]]['item'] .setText(4, rdata[1]['upgRate'])
                self.node['node'][rdata[0][7]]['item'] .setText(5, rdata[1]['bpFlag'])
                self.ui.treeWidget_node.resizeColumnToContents(4)
                self.ui.treeWidget_node.resizeColumnToContents(5)
        elif rdata[0][2].startswith('mcDbg'):
            if rdata[0][7] in self.node['node']:
                self.ui.plainTextEdit_rdbgresp.setPlainText(rdata[1]['dat'])
        
        #plainTextEdit
    def update(self):
        if self.conn.poll():
            msg = self.conn.recv()
            if msg[0] == 'pkt':
                if msg[1][0] == 'parsepkt':
                    if self.ui.treeWidget.topLevelItemCount() and self.ui.treeWidget.topLevelItem(0).text(0) == 'parsepkt':
                        self.ui.treeWidget.takeTopLevelItem(0)
                    item = QTreeWidgetItem(None, msg[1])
                    for i in range(self.ui.treeWidget.columnCount()):
                        item.setBackground(i, QBrush(Qt.green))
                        if 5 < i < 10:
                            item.setTextAlignment(i, Qt.AlignRight)
                    self.ui.treeWidget.insertTopLevelItem(0, item)
                    self.ui.treeWidget.scrollToTop()
                    self.parsepkt = msg[1:]
                else:
                    self.buf.append(msg[1:])
                    self.add_treeitem(msg[1:])
                    if self.ui.checkBox_autoscroll.isChecked():
                        self.ui.treeWidget.scrollToBottom()
                for i in range(self.ui.treeWidget.columnCount()):
                     self.ui.treeWidget.resizeColumnToContents(i)
            elif msg[0] == 'msg':
                self.ui.plainTextEdit_log.appendPlainText('[msg]%s.' % msg[1])
            elif msg[0] == 'err':
                self.ui.plainTextEdit_log.appendPlainText(msg[1])
            
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_itemClicked(self, item, column):
        index = self.ui.treeWidget.indexOfTopLevelItem(item)
        self.ui.treeWidget_cmdinfo.clear()
        if self.ui.treeWidget.topLevelItem(0).text(0) == 'parsepkt':
            if index == 0:
                pktinfo = self.parsepkt
            else:
                pktinfo = self.buf[index-1]
        else:
            pktinfo = self.buf[index]
        if pktinfo[1]:
            self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, ('cmdType', item.text(2))))
            self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, ('--', '--')))
            for i in pktinfo[1].items():
                self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, i))
            self.ui.treeWidget_cmdinfo.resizeColumnToContents(0)
        # routeLsg
        if column == 12:
            self.ui.plainTextEdit_pktdata.setPlainText(item.text(column))
        else:
            self.ui.plainTextEdit_pktdata.setPlainText(pktinfo[2])
        
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_cmdinfo_itemClicked(self, item, column):
        self.ui.plainTextEdit_pktdata.setPlainText(item.text(1))
 
    @pyqtSlot(QPoint)
    def on_treeWidget_customContextMenuRequested(self, pos):
        popMenu =QMenu(self)
        if self.ui.treeWidget.topLevelItemCount():
            popMenu.addAction(self.ui.actionSaveAs)
            popMenu.addAction(self.ui.actionLoad)
            popMenu.addSeparator()
            popMenu.addAction(self.ui.actionClear)
        else:
            popMenu.addAction(self.ui.actionLoad)
        if self.ui.treeWidget.topLevelItemCount() and self.ui.treeWidget.topLevelItem(0).text(0) == 'parsepkt':
            popMenu.addSeparator()
            popMenu.addAction(self.ui.actionRmParsed)
        popMenu.popup(QCursor.pos())
        
    @pyqtSlot()
    def on_actionClear_triggered(self):
        self.buf = []
        self.ui.treeWidget.clear()
        
    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        t = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        file = QFileDialog.getSaveFileName(self, 'Save file', './dat/' + t, 'data file(*.dat)')[0]
        if file:
            with open(file, 'wb') as f:
                pickle.dump(self.buf, f)
            
    @pyqtSlot()
    def on_actionLoad_triggered(self):
        file = QFileDialog.getOpenFileName(self, 'Load file',  './dat',  'data file(*.dat)')[0]
        if file:
            self.load_file(file)
            
    @pyqtSlot()
    def on_actionRmParsed_triggered(self):
        self.ui.treeWidget.takeTopLevelItem(0)
        
    @pyqtSlot()
    def on_pushButton_parsepkt_clicked(self):
        text = self.ui.plainTextEdit_pktdata.toPlainText()
        self.conn.send(['parsepkt', bytearray.fromhex(text)])
            
    @pyqtSlot()
    def on_actionRdSnCfg_triggered(self):    
        if self.txtimer.isActive() or self.upgtimer.isActive():
            self.ui.plainTextEdit_log.appendPlainText('Tx busy.')
            return
        self.txpkt = []
        for item in self.ui.treeWidget_node.selectedItems():
            addr = item.text(0)
            if addr in self.node['node']:
                self.txpkt.append(upgrade.mk_rdsncfg(addr, self.upgsrc))
                item.setText(1, '')
        if self.txpkt:
            self.txtimer.start(1000)
    
    @pyqtSlot()
    def on_actionRdVerInfo_triggered(self): 
        if self.txtimer.isActive() or self.upgtimer.isActive():
            self.ui.plainTextEdit_log.appendPlainText('Tx busy.')
            return
        self.txpkt = []
        for item in self.ui.treeWidget_node.selectedItems():
            addr = item.text(0)
            if addr in self.node['node']:
                self.txpkt.append(upgrade.mk_rdverinfo(addr, self.upgsrc))
                item.setText(1, '')
        if self.txpkt:
            self.txtimer.start(1000)
            
    @pyqtSlot()
    def on_actionUpgBpSts_triggered(self):
        if self.txtimer.isActive() or self.upgtimer.isActive():
            self.ui.plainTextEdit_log.appendPlainText('Tx busy.')
            return
        self.txpkt = []
        for item in self.ui.treeWidget_node.selectedItems():
            addr = item.text(0)
            if addr in self.node['node']:
                self.txpkt.append(upgrade.mk_bpsts(addr, self.upgsrc))
                item.setText(2, '')
                item.setText(3, '')
        if self.txpkt:
            self.txtimer.start(1000)

    @pyqtSlot()
    def on_actionRdbgPoolType_triggered(self):
        self.ui.plainTextEdit_rdbgresp.setPlainText('') 
        items = self.ui.treeWidget_node.selectedItems()     
        if items:
            addr = items[0].text(0)
            self.rdbgidx += 1
            pkt = rdebug.mk_pooltype(addr, self.upgsrc, self.rdbgidx % 128)
            self.conn.send(['send',  self.__sendchnl, pkt])
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))

    @pyqtSlot()
    def on_actionEraseParam_triggered(self):
        self.ui.plainTextEdit_rdbgresp.setPlainText('') 
        items = self.ui.treeWidget_node.selectedItems()     
        if items:
            addr = items[0].text(0)
            self.rdbgidx += 1
            pkt = rdebug.mk_eraseparam(addr, self.upgsrc, self.rdbgidx % 128)
            self.conn.send(['send',  self.__sendchnl, pkt])
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))

    @pyqtSlot()
    def on_actionUpgTxm_triggered(self):
        items=self.ui.treeWidget_node.selectedItems()     
        addr = items[0].text(0)
        pkt = upgrade.mk_chng2txm(addr, self.upgsrc,  not self.ui.checkBox_bcast.isChecked())
        self.conn.send(['send',  self.__sendchnl, pkt])
        self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
            
    @pyqtSlot()
    def on_actionUpgRdBack_triggered(self):
        items=self.ui.treeWidget_node.selectedItems()     
        addr = items[0].text(0)
        pkt = upgrade.mk_readback(addr, self.upgsrc)
        self.conn.send(['send',  self.__sendchnl, pkt])
        self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))

    def txpacket(self):
        if self.txpkt:
            self.conn.send(['send',  self.__sendchnl, self.txpkt[0]])
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in self.txpkt[0]]))
            del self.txpkt[0]
            self.txtimer.start(1000)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_node_itemClicked(self, item, column):
        self.ui.lineEdit_curnode.setText(item.text(0))

    @pyqtSlot(QPoint)
    def on_treeWidget_node_customContextMenuRequested(self, pos):
        if self.conn and self.ui.treeWidget_node.selectedItems():
            popMenu =QMenu(self)
            popMenu.addAction(self.ui.actionRdSnCfg)
            popMenu.addAction(self.ui.actionRdVerInfo)
            if self.__whosyourdaddy:
                popMenu.addAction(self.ui.actionUpgBpSts)
                popMenu.addAction(self.ui.actionRdbgPoolType)
                popMenu.addSeparator()
                popMenu.addAction(self.ui.actionEraseParam)
                popMenu.addSeparator()
                popMenu.addAction(self.ui.actionUpgTxm)  
                popMenu.addSeparator()
                popMenu.addAction(self.ui.actionUpgRdBack)  
            popMenu.popup(QCursor.pos())

    @pyqtSlot()
    def on_pushButton_upgrade_clicked(self):
        if self.txtimer.isActive() or self.upgtimer.isActive():
            self.ui.plainTextEdit_log.appendPlainText('Tx busy.')
            return
        if self.ui.checkBox_bcast.isChecked():
            self.upgdst = 'FFFFFFFFFFFF'
        else:
            items = self.ui.treeWidget_node.selectedItems()    
            if len(items) == 1:
                self.upgdst = items[0].text(0)
            else:
                self.ui.plainTextEdit_log.appendPlainText('[upg]Please select only one node.')
                return
        self.upgrdbplst = []
        self.upgi = 0
        self.upgdata = upgrade.get_app_code(self.config['upgrade']['file'])
        self.upgflen = self.upgdata[0x400+2]+self.upgdata[0x400+7]*0x100
        self.upgsver = int.from_bytes(self.upgdata[0x100:0x104], 'big')
        self.upghver = int.from_bytes(self.upgdata[0x104:0x106], 'big')
        self.upgvid = int.from_bytes(self.upgdata[0x106:0x108], 'big')
        self.upgcrc = int.from_bytes(self.upgdata[-4:], 'big')
        # auto = 1, change mode - send data - read bp - calc bp , and loop.
        # auto = 0, change mode - send data.
        # when auto = 0, usebp = 1, calc bp - change mode - send data.
        # when auto = 0, usebp = 0, change mode - send data.
        if self.ui.checkBox_upgauto.isChecked() or not self.ui.checkBox_usebp.isChecked():
            # 0 - change mode, 1 - send data, 2 - calc bpflag
            self.upgsts = 0
            self.upgbpflag = ['0'] * self.upgflen
            self.ui.progressBar_upgrade.setValue(0)
            self.ui.progressBar_upgrade.setMaximum(self.upgflen)
        else:
            self.upgsts = 2
        self.upgtimer.start(100)
        
    def upgrade(self):
        if self.upgrdbplst:
            node = self.upgrdbplst[self.upgi]
            self.ui.plainTextEdit_log.appendPlainText('[upgrade]read bpflag %s' % node)
            #print('[upgrade]read bpflag %s' % node)
            self.node['node'][node]['bpFlag'] = ''
            self.node['node'][node]['item'] .setText(4, '')
            self.node['node'][node]['item'] .setText(5, '')
            pkt = upgrade.mk_bpsts(node, self.upgsrc)
            self.conn.send(['send',  self.__sendchnl, pkt])
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
            self.upgi += 1
            if self.upgi == len(self.upgrdbplst):
                self.upgi = 0
                self.upgrdbplst = []
                self.upgsts = 2
            self.upgtimer.start(1000)
        else:
            if self.upgsts == 0:
                self.ui.plainTextEdit_log.appendPlainText('[upgrade]switch upgrade rxd mode.')
                #print('[upgrade]switch upgrade rxd mode.')
                pkt = upgrade.mk_upg02(self.upgdst, self.upgsrc, self.upgvid, self.upghver, self.upgflen, self.upgsver, self.upgcrc)
                self.conn.send(['send',  self.__sendchnl, pkt]) 
                #self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
                #print('Tx:'+' '.join(['%02X'%i for i in pkt]))
                self.upgi += 1
                # send chngm 5 times.
                if self.upgi < 5:
                    self.upgtimer.start(500)
                else:
                    self.upgsts = 1
                    self.upgi = 0
                    self.upgtimer.start(2000)
            elif self.upgsts == 1:
                for i in range(self.upgi, self.upgflen):
                    if self.upgbpflag[i] == '0':
                        #self.ui.plainTextEdit_log.appendPlainText('[upgrade]send packet %i.' % i)
                        #print('[upgrade]: send packet %i.' % i)
                        pkt = upgrade.mk_upg04(
                            self.upgdst,  self.upgsrc, self.upgvid, self.upgflen, self.upgcrc, i+1, self.upgdata[i*128:i*128+128])
                        self.conn.send(['send',  self.__sendchnl, pkt]) 
                        #self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%ii for ii in pkt]))
                        #print('Tx:'+' '.join(['%02X'%ii for ii in pkt]))
                        self.upgbpflag[i] = '1'
                        max = self.ui.progressBar_upgrade.maximum()
                        self.ui.progressBar_upgrade.setValue(max - self.upgbpflag.count('0'))
                        self.upgi = i+1
                        if self.upgdst == 'FFFFFFFFFFFF':
                            self.upgtimer.start(300)
                        else:
                            self.upgtimer.start(500)
                        break
                else:
                    if self.ui.checkBox_upgauto.isChecked():
                        self.upgi = 0
                        if self.upgdst == 'FFFFFFFFFFFF':
                            self.upgrdbplst = list(self.node['node'].keys())
                        else:
                            self.upgrdbplst =[self.upgdst]
                        self.upgtimer.start(500)
                    else:
                        self.ui.plainTextEdit_log.appendPlainText('[upgrade]upgrade finished.')
                        #print('[upgrade]upgrade finished.')
            else:
                self.upgsts = 0
                self.upgi = 0
                totbpflag = bytearray(b'\xFF' * 64)
                if self.upgdst == 'FFFFFFFFFFFF':
                    for node in self.node['node']:
                        if self.node['node'][node]['bpFlag']:
                            bpflag = bytes.fromhex(self.node['node'][node]['bpFlag'])
                            for i in range(64):
                                totbpflag[i] &= bpflag[i]
                else:
                    if self.upgdst in self.node['node'] and self.node['node'][self.upgdst]['bpFlag']:
                            bpflag = bytes.fromhex(self.node['node'][self.upgdst]['bpFlag'])
                            for i in range(64):
                                totbpflag[i] &= bpflag[i]
                self.upgbpflag = []
                for i in range(64):
                    flag = list('{:08b}'.format(totbpflag[i]))
                    flag.reverse()
                    self.upgbpflag.extend(flag)
                self.upgbpflag = self.upgbpflag[:self.upgflen]
                self.ui.plainTextEdit_log.appendPlainText('[upgrade]totbpflag %s' % ''.join(self.upgbpflag))
                #print('[upgrade]totbpflag %s' % ''.join(self.upgbpflag))
                max = self.upgbpflag.count('0')
                if max:
                    self.ui.progressBar_upgrade.setMaximum(max)
                    self.ui.progressBar_upgrade.setValue(0)
                    self.upgtimer.start(1000)
                else:
                    self.ui.plainTextEdit_log.appendPlainText('[upgrade]upgrade finished.')
                    #print('[upgrade]upgrade finished.')

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_rdbglst_itemClicked(self, item, column):
        row = self.ui.treeWidget_rdbglst.indexOfTopLevelItem(item)
        self.ui.spinBox_rdbgaddr.setValue(self.rdbglst[row][1])
        len = self.rdbglst[row][2]
        val = len if len < 128 else 128
        self.ui.spinBox_rdbglen.setValue(val)

    @pyqtSlot()
    def on_pushButton_rdbgsend_clicked(self):
        self.ui.plainTextEdit_rdbgresp.setPlainText('')
        items = self.ui.treeWidget_node.selectedItems()    
        if items:
            addr = items[0].text(0)
            self.rdbgidx += 1
            pkt = rdebug.mk_rxval(addr, self.upgsrc, self.rdbgidx % 128, 
                self.ui.spinBox_rdbgaddr.value(), self.ui.spinBox_rdbglen.value())
            self.conn.send(['send',  self.__sendchnl, pkt])
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
        else:
            self.ui.plainTextEdit_log.appendPlainText('[rdbg]read xdata: Need select a node.')
            
    @pyqtSlot(int)
    def on_comboBox_chnlgrp_currentIndexChanged(self, index):
        self.conn.send(['setchnlgrp', index])
        self.ui.plainTextEdit_log.appendPlainText('[msg]channel group set to %i.' % index)

    @pyqtSlot()
    def on_pushButton_rfplcsw_clicked(self):
        rfplc = 0
        if self.ui.checkBox_rf.isChecked():
            rfplc += 1
        if self.ui.checkBox_plc.isChecked():
            rfplc += 2
        if rfplc:
            self.rdbgidx += 1
            pkt = rdebug.mk_rfplcswitch(self.ui.lineEdit_curnode.text(), self.upgsrc,  self.rdbgidx % 128, rfplc)
            self.conn.send(['send',  self.__sendchnl, pkt])
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
        else:
            self.ui.plainTextEdit_log.appendPlainText('[err]must select one in rf and plc.')

    def _CmdPro(self, s):
        if s.startswith('send '):
            cmd = s.split(maxsplit=2)
            if len(cmd) > 1:
#                try:
                    cmd[1] = int(cmd[1], 16)
                    cmd[2] = bytearray.fromhex(cmd[2])
                    self.conn.send(cmd)
                    self.ui.plainTextEdit_log.appendPlainText(
                        '[Tx]chnl(%i) %s.' % (cmd[1], ' '.join('%02X'%ii for ii in cmd[2])))
#                except:
#                    self.ui.plainTextEdit_log.appendPlainText('[error]send data error.\n')
        elif s.startswith('sendx '):
            cmd = s.split(maxsplit=3)
            if len(cmd) > 1:
#                        try:
                        cmd[1] = int(cmd[1], 16)
                        cmd[2] = int(cmd[2])
                        cmd[3] = bytearray.fromhex(cmd[3])
                        self.conn.send(cmd)
                        self.ui.plainTextEdit_log.appendPlainText(
                            '[Tx]chnl(%02X-%i) %s.' % (cmd[1], cmd[2], ' '.join('%02X'%ii for ii in cmd[3])))
#                        except:
#                            self.ui.plainTextEdit_log.appendPlainText('[error]send data error.\n')

    def keyReleaseEvent(self, e):
        key = e.key()
        if key == Qt.Key_Return:
            self._CmdPro(self.ui.comboBox_cmd.currentText())
            self.ui.comboBox_cmd.setCurrentText('')

    @pyqtSlot()
    def on_pushButton_send_clicked(self):
        if self.ui.pushButton_send.text() == '发送':
            if self.ui.checkBox_autosend.isChecked():
                self.autosendtimer = QTimer(self)
                self.autosendtimer.timeout.connect(self._AutoSend)  
                self.autosendtimer.start(self.ui.spinBox_sendInterval.value())
                self.ui.pushButton_send.setText('停止')
            else:
                self._AutoSend()
        else:
            self.autosendtimer.stop()
            self.ui.pushButton_send.setText('发送')

    def _AutoSend(self):
        self._CmdPro(self.ui.comboBox_cmd.currentText())
    
    @pyqtSlot(int)
    def on_tabWidget_rightSideBar_tabBarClicked(self, index):        
        if self.__rightSideBar_isShrinked:
            self.ui.tabWidget_rightSideBar.resize(self.__rightSideBar_bigSize)
            minSize = max(self.__rightSideBar_minSize, self.ui.tabWidget_rightSideBar.minimumSizeHint().width())
            self.ui.tabWidget_rightSideBar.setMinimumWidth(minSize)
            self.ui.tabWidget_rightSideBar.setMaximumWidth(self.__rightSideBar_maxSize)
            self.ui.splitter_h.setSizes(self.__splitter_h_sizes)
            #self.ui.splitter_h.setStretchFactor(1, 1)
            self.__rightSideBar_isShrinked = False
        else:
            self.__rightSideBar_bigSize = self.ui.tabWidget_rightSideBar.size()
            if self.__rightSideBar_lastIndex == index:
                self.__rightSideBar_minSize = self.ui.tabWidget_rightSideBar.minimumSizeHint().width()
                self.__rightSideBar_maxSize = self.ui.tabWidget_rightSideBar.maximumWidth()
                self.__splitter_h_sizes = self.ui.splitter_h.sizes()
                self.ui.tabWidget_rightSideBar.setFixedWidth(self.ui.tabWidget_rightSideBar.tabBar().width())
                self.ui.splitter_h.setStretchFactor(1, 1)
                self.__rightSideBar_isShrinked = True
        self.ui.tabWidget_rightSideBar.setCurrentIndex(index)
        self.__rightSideBar_lastIndex = index
        
    @pyqtSlot(int)
    def on_tabWidget_bottomSideBar_tabBarClicked(self, index):        
        if self.__bottomSideBar_isShrinked:
            self.ui.tabWidget_bottomSideBar.resize(self.__bottomSideBar_bigSize)
            minSize = max(self.__bottomSideBar_minSize, self.ui.tabWidget_bottomSideBar.minimumSizeHint().height())
            self.ui.tabWidget_bottomSideBar.setMinimumHeight(minSize)
            self.ui.tabWidget_bottomSideBar.setMaximumHeight(self.__bottomSideBar_maxSize)
            self.ui.splitter_v.setSizes(self.__splitter_v_sizes)
            self.ui.splitter_v.setStretchFactor(1, 1)
            self.__bottomSideBar_isShrinked = False
        else:
            self.__bottomSideBar_bigSize = self.ui.tabWidget_bottomSideBar.size()
            if self.__bottomSideBar_lastIndex == index:
                self.__bottomSideBar_minSize = self.ui.tabWidget_bottomSideBar.minimumSizeHint().height()
                self.__bottomSideBar_maxSize = self.ui.tabWidget_bottomSideBar.maximumHeight()
                self.__splitter_v_sizes = self.ui.splitter_v.sizes()
                self.ui.tabWidget_bottomSideBar.setFixedHeight(self.ui.tabWidget_bottomSideBar.tabBar().height())
                self.ui.splitter_v.setStretchFactor(1, 1)
                self.__bottomSideBar_isShrinked = True
        self.ui.tabWidget_bottomSideBar.setCurrentIndex(index)
        self.__bottomSideBar_lastIndex = index
    
    @pyqtSlot()
    def on_pushButton_bcastAddr_clicked(self):
        self.ui.lineEdit_curnode.setText('FFFFFFFFFFFF')
