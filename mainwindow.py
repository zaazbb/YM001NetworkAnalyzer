
import os.path
import pickle
from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QFileDialog
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QTimer, pyqtSlot, Qt

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
        if conn_file:
            if isinstance(conn_file, str):
                if os.path.exists(conn_file):
                    self.load_file(conn_file)
            else:
                self.conn = conn_file
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update)
                self.timer.start(100)                
        else:
            self.ui.treeWidget.addAction(self.ui.actionLoad)
        self.ui.treeWidget.addAction(self.ui.actionSaveAs)
        
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
