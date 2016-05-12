
import os.path
import pickle
from datetime import datetime
import traceback

from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QMenu, QFileDialog, QInputDialog
from PyQt5.QtGui import QBrush, QCursor
from PyQt5.QtCore import QTimer, pyqtSlot, Qt, QPoint

from Ui_mainwindow import Ui_MainWindow


#colors = ('red', 'green', 'cyan','magenta','yellow',  'lightGray'
#         'darkGreen', 'darkCyan', 'darkMagenta', 'darkYellow', 'gray','darkGray')
highlights = (
    (1054500001, 'lightGray'), # basenode
    #(111111111111, 'red'),  #testnode
    #(141111561911, 'red'), 
    (10203040506, 'red'), 
    #(222222222222, 'green'),
    (3103261, 'green'),
    (3100063, 'cyan'), (3103045, 'magenta'), (3102133, 'yellow')
)


class MainWindow(QMainWindow):
    def __init__(self, conn_file):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.splitter.setStretchFactor(0, 1)
        
        self.highlights = {}
        global highlights
        for i in highlights:
            self.highlights['%012i' % i[0]] = getattr(Qt, i[1])
        
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
    
        self.cur_addr = ''
        
    def load_file(self, file):
        with open(file, 'rb') as f:
            self.buf = pickle.load(f)
            self.ui.treeWidget.clear()
            for i in self.buf:
                self.add_treeitem(i[0])
            for i in range(self.ui.treeWidget.columnCount()):
                 self.ui.treeWidget.resizeColumnToContents(i)

    def add_treeitem(self, rowdata):
        item = QTreeWidgetItem(None, rowdata)
        for i in range(5, 5+len(rowdata[5:9])):
            if rowdata[i] in self.highlights:
                item.setBackground(i, QBrush(self.highlights[rowdata[i]]))
        self.ui.treeWidget.addTopLevelItem(item)
        
        #plainTextEdit
    def update(self):
        if self.conn.poll():
            msg = self.conn.recv()
            #print(msg)
            self.buf.append(msg)
            self.add_treeitem(msg[0])
            for i in range(self.ui.treeWidget.columnCount()):
                 self.ui.treeWidget.resizeColumnToContents(i)
            #self.ui.treeWidget.scrollToItem(item)
            
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
        self.ui.plainTextEdit_rawdata.setPlainText(self.buf[index][2])
        self.ui.plainTextEdit_cinfoval.setPlainText(item.text(column))
        
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_cmdinfo_itemClicked(self, item, column):
        self.ui.plainTextEdit_cinfoval.setPlainText(item.text(1))
 
    @pyqtSlot(QPoint)
    def on_treeWidget_customContextMenuRequested(self, pos):
        popMenu =QMenu(self)
        
        popMenu.addAction(self.ui.actionSaveAs)
        popMenu.addAction(self.ui.actionLoad)

        if self.conn:
            popMenu.addSeparator()
            popMenu.addAction(self.ui.actionRdSnCfg)
            popMenu.addSeparator()
            popMenu.addAction(self.ui.actionUpgBpSts)
            popMenu.addAction(self.ui.actionUpgTxm)  
            
            col = self.ui.treeWidget.columnAt(pos.x())
            #item = self.ui.treeWidget.itemAt(pos.x())
            items=self.ui.treeWidget.selectedItems()            
            if 5<=col<=8 and items:
                self.cur_addr = items[0].text(col)
            else:
                self.cur_addr = ''
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
            
    def send_pkt(self, template):
        addr = self.cur_addr
        if not addr:
            addr, ok = QInputDialog.getText(self, 'Input Addr', 'address:')
            if not ok or not addr:
                return
        try:
            addr = bytearray.fromhex(addr.replace(' ', '')[:12].zfill(12))
            addr.reverse()
            pkt = bytearray.fromhex(template.replace('xx xx xx xx xx xx', ' '.join(['%02X'%i for i in addr])))
            self.conn.send(pkt)
            self.ui.plainTextEdit_log.appendPlainText('Tx:'+' '.join(['%02X'%i for i in pkt]))
        except ValueError:
            self.ui.plainTextEdit_log.appendPlainText(traceback.format_exc())
            
    @pyqtSlot()
    def on_actionRdSnCfg_triggered(self):
        self.send_pkt(
            '41 CD 01 FF FF xx xx xx xx xx xx 00 00 00 00 00 00 '
            '7C xx xx xx xx xx xx 00 00 00 00 00 00 11 01 01 04')
        
    @pyqtSlot()
    def on_actionUpgBpSts_triggered(self):
        self.send_pkt('63 CD 01 FF FF xx xx xx xx xx xx FF FF FF FF FF FF F0 06')

    @pyqtSlot()
    def on_actionUpgTxm_triggered(self):
        self.send_pkt(
            '63 CD 01 FF FF xx xx xx xx xx xx FF FF FF FF FF FF '
            'F0 03 01 00 01 FF FF FF FF FF FF 02 '
            '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')

