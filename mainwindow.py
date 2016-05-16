
import os.path
import pickle
from datetime import datetime
import traceback

from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QMenu, QFileDialog#, QInputDialog
from PyQt5.QtGui import QBrush, QCursor
from PyQt5.QtCore import QTimer, pyqtSlot, Qt, QPoint

from Ui_mainwindow import Ui_MainWindow

import upgrade



class MainWindow(QMainWindow):
    def __init__(self, conn_file, nodes, config):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.splitter.setStretchFactor(0, 1)
        
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
            nodes['node'][k]['item'] = item
            if v['color']:
                color = getattr(Qt, v['color'])
                item.setBackground(0, color)
                self.highlight[k] = color
            self.ui.treeWidget_node.addTopLevelItem(item)
        if nodes['xnode']:
            root = QTreeWidgetItem(None, ['xnode'])
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
        
        self.buf = []
        self.conn = None
        if conn_file:
            if isinstance(conn_file, str):
                if os.path.exists(conn_file):
                    self.load_file(conn_file)
            else:
                self.conn = conn_file
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update)
                self.timer.start(100)     
                
        self.ui.pushButton_upgrade.setEnabled(bool(self.conn))
        
        if self.conn:
            self.upgsrcaddr = self.config['upgrade']['srcaddr'][:12].zfill(12)
            self.upgtimer = QTimer(self)
            self.upgtimer.setSingleShot(True)
            self.upgtimer.timeout.connect(self.upgrade)
            self.txtimer = QTimer(self)
            self.txtimer.setSingleShot(True)
            self.txtimer.timeout.connect(self.txpacket)
            
        
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
        for i in range(5, 5+len(rdata[0][5:9])):
            if rdata[0][i] in self.highlight:
                item.setBackground(i, QBrush(self.highlight[rdata[0][i]]))
        self.ui.treeWidget.addTopLevelItem(item)
        # rowdata[0][?]: 5 - ndst, 6 - msrc, 7 - ndst, 8 - nsrc.
        if rdata[0][1] == 'acRdNdCfgUp':
            if rdata[0][8] in self.node['node']:
                self.node['node'][rdata[0][8]]['item'] .setText(1, rdata[1]['sVer'])
                self.ui.treeWidget_node.resizeColumnToContents(1)
        elif rdata[0][1] == 'mcUpgBpStsAck':
            if rdata[0][6] in self.node['node']:
                print(rdata)
                self.node['node'][rdata[0][6]]['bpFlag'] = rdata[1]['bpFlag']
                upgrate = 'upgRate'if 'upgRate' in rdata[1] else 'bpRate'
                self.node['node'][rdata[0][6]]['item'] .setText(2, rdata[1][upgrate])
                self.node['node'][rdata[0][6]]['item'] .setText(3, rdata[1]['bpFlag'])
                self.ui.treeWidget_node.resizeColumnToContents(2)
                self.ui.treeWidget_node.resizeColumnToContents(3)
        
        #plainTextEdit
    def update(self):
        if self.conn.poll():
            msg = self.conn.recv()
            if msg[0] == 'pkt':
                self.buf.append(msg[1:])
                self.add_treeitem(msg[1:])
                for i in range(self.ui.treeWidget.columnCount()):
                     self.ui.treeWidget.resizeColumnToContents(i)
            elif msg[0] == 'err':
                self.ui.plainTextEdit_log.appendPlainText(msg[1])
            
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_itemClicked(self, item, column):
        index = self.ui.treeWidget.indexOfTopLevelItem(item)
        self.ui.treeWidget_cmdinfo.clear()
        if self.buf[index][1]:
            self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, ('cmdType', item.text(1))))
            self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, ('--', '--')))
            for i in self.buf[index][1].items():
                self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, i))
            self.ui.treeWidget_cmdinfo.resizeColumnToContents(0)
        # routeLsg
        if column == 11:
            self.ui.plainTextEdit_pktdata.setPlainText(item.text(column))
        else:
            self.ui.plainTextEdit_pktdata.setPlainText(self.buf[index][2])
        
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_cmdinfo_itemClicked(self, item, column):
        self.ui.plainTextEdit_pktdata.setPlainText(item.text(1))
 
    @pyqtSlot(QPoint)
    def on_treeWidget_customContextMenuRequested(self, pos):
        popMenu =QMenu(self)
        popMenu.addAction(self.ui.actionSaveAs)
        popMenu.addAction(self.ui.actionLoad)
        popMenu.popup(QCursor.pos())
        
    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        t = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        file = QFileDialog.getSaveFileName(self, 'Save file', t, 'data file(*.dat)')[0]
        if file:
            with open(file, 'wb') as f:
                pickle.dump(self.buf, f)
            
    @pyqtSlot()
    def on_actionLoad_triggered(self):
        file = QFileDialog.getOpenFileName(self, 'Load file', filter='data file(*.dat)')[0]
        if file:
            self.load_file(file)
            
    @pyqtSlot()
    def on_actionRdSnCfg_triggered(self):    
        if self.txtimer.isActive() or self.upgtimer.isActive():
            self.ui.plainTextEdit_log.appendPlainText('Tx busy.')
            return
        self.txpkt = []
        for item in self.ui.treeWidget_node.selectedItems():
            addr = item.text(0)
            if addr in self.node['node']:
                self.txpkt.append(upgrade.mk_rdsncfg(addr, self.upgsrcaddr))
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
                self.txpkt.append(upgrade.mk_bpsts(addr, self.upgsrcaddr))
                item.setText(2, '')
                item.setText(3, '')
        if self.txpkt:
            self.txtimer.start(1000)

    @pyqtSlot()
    def on_actionUpgTxm_triggered(self):
        items=self.ui.treeWidget_node.selectedItems()     
        addr = items[0].text(0)
        pkt = upgrade.mk_chng2txm(addr, self.upgsrcaddr)
        self.conn.send(pkt)
        self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
            
#    @pyqtSlot()
#    def on_actionUpgRdBack_triggered(self):
#        items=self.ui.treeWidget_node.selectedItems()     
#        addr = items[0].text(0)
#        pkt = upgrade.mk_readback(addr, self.upgsrcaddr)
#        self.conn.send(pkt)
#        self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))

    def txpacket(self):
        if self.txpkt:
            self.conn.send(self.txpkt[0])
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in self.txpkt[0]]))
            del self.txpkt[0]
            self.txtimer.start(1000)

    @pyqtSlot(QPoint)
    def on_treeWidget_node_customContextMenuRequested(self, pos):
        if self.conn and self.ui.treeWidget_node.selectedItems():
            popMenu =QMenu(self)
            popMenu.addAction(self.ui.actionRdSnCfg)
            popMenu.addAction(self.ui.actionUpgBpSts)
            popMenu.addSeparator()
            popMenu.addAction(self.ui.actionUpgTxm)  
            #popMenu.addSeparator()
            #popMenu.addAction(self.ui.actionUpgRdBack)  
            popMenu.popup(QCursor.pos())
        
    @pyqtSlot()
    def on_pushButton_upgrade_clicked(self):
        if self.txtimer.isActive() or self.upgtimer.isActive():
            self.ui.plainTextEdit_log.appendPlainText('Tx busy.')
            return
        self.upgrdbplst = []
        self.upgidx = 0
        self.upgdata = upgrade.get_app_code(self.config['upgrade']['file'])
        self.upgflen = self.upgdata[0x400+2]+self.upgdata[0x400+7]*0x100
        self.upgsver = int.from_bytes(self.upgdata[0x100:0x100+4], 'big')
        self.upgcrc = int.from_bytes(self.upgdata[-4:], 'big')
        if self.ui.checkBox_upgauto.isChecked() or not self.ui.checkBox_usebp.isChecked():
            # 0 - change mode, 1 - send data, 3 - calc bpflag
            self.upgsts = 0
            self.upgbpflag = ['0'] * self.upgflen
            self.ui.progressBar_upgrade.setValue(0)
            self.ui.progressBar_upgrade.setMaximum(self.upgflen)
        else:
            self.upgsts = 2
        self.upgtimer.start(100)
        
    def upgrade(self):
        if self.upgrdbplst:
            node = self.upgrdbplst[self.upgidx]
            self.ui.plainTextEdit_log.appendPlainText('[upgrade]read bpflag %s' % node)
            #print('[upgrade]read bpflag %s' % node)
            self.node['node'][node]['bpFlag'] = ''
            self.node['node'][node]['item'] .setText(2, '')
            self.node['node'][node]['item'] .setText(3, '')
            pkt = upgrade.mk_bpsts(node, self.upgsrcaddr)
            self.conn.send(pkt)
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
            self.upgidx += 1
            if self.upgidx == len(self.upgrdbplst):
                self.upgidx = 0
                self.upgrdbplst = []
                self.upgsts = 2
            self.upgtimer.start(1000)
        else:
            if self.upgsts == 0:
                self.upgsts = 1
                self.ui.plainTextEdit_log.appendPlainText('[upgrade]switch upgrade rxd mode.')
                #print('[upgrade]switch upgrade rxd mode.')
                pkt = upgrade.mk_upg02(self.upgsrcaddr, self.upgflen, self.upgsver, self.upgcrc)
                self.conn.send(pkt) 
                #self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
                #print('Tx:'+' '.join(['%02X'%i for i in pkt]))
                self.upgtimer.start(2000)
            elif self.upgsts == 1:
                for i in range(self.upgidx, self.upgflen):
                    if self.upgbpflag[i] == '0':
                        #self.ui.plainTextEdit_log.appendPlainText('[upgrade]send packet %i.' % i)
                        #print('[upgrade]: send packet %i.' % i)
                        pkt = upgrade.mk_upg04(self.upgsrcaddr, self.upgflen, self.upgcrc, i+1, self.upgdata[i*128:i*128+128])
                        self.conn.send(pkt) 
                        #self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%ii for ii in pkt]))
                        #print('Tx:'+' '.join(['%02X'%ii for ii in pkt]))
                        self.upgbpflag[i] = '1'
                        max = self.ui.progressBar_upgrade.maximum()
                        self.ui.progressBar_upgrade.setValue(max - self.upgbpflag.count('0'))
                        self.upgidx = i+1
                        self.upgtimer.start(500)
                        break
                else:
                    if self.ui.checkBox_upgauto.isChecked():
                        self.upgidx = 0
                        self.upgrdbplst = list(self.node['node'].keys())
                        self.upgtimer.start(500)
                    else:
                        self.ui.plainTextEdit_log.appendPlainText('[upgrade]upgrade finished.')
                        #print('[upgrade]upgrade finished.')
            else:
                self.upgsts = 0
                totbpflag = bytearray(b'\xFF' * 64)
                for node in self.node['node']:
                    if self.node['node'][node]['bpFlag']:
                        bpflag = bytes.fromhex(self.node['node'][node]['bpFlag'])
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
        
