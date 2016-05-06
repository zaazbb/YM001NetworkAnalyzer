
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QTimer, pyqtSlot, Qt

from Ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, conn):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.splitter.setStretchFactor(0, 1)
        
        self.conn = conn
        self.buf = []
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        
        #plainTextEdit
    def update(self):
        if self.conn.poll():
            msg = self.conn.recv()
            #print(msg)
            
            self.buf.append((msg[0], msg[1][0], msg[1][1], msg[2]))
            msg[1][0].insert(0, str(msg[0]))
            item = QTreeWidgetItem(None, msg[1][0])
            for i in range(5, 5+len(msg[1][0][5:9])):
                if msg[1][0][i] == '111111111111':
                    item.setBackground(i, QBrush(Qt.cyan))
#            if '000003103261' in msg[1][0]:
#                item.setBackground(msg[1][0].index('000003103261'), QBrush(Qt.lightGray))
#            if '000003100063' in msg[1][0]:
#                item.setBackground(msg[1][0].index('000003100063'), QBrush(Qt.cyan))
#            if '000003103045' in msg[1][0]:
#                item.setBackground(msg[1][0].index('000003103045'), QBrush(Qt.magenta))
#            if '000003102133' in msg[1][0]:
#                item.setBackground(msg[1][0].index('000003102133'), QBrush(Qt.gray))
            #item.setBackground(1, QBrush(Qt.lightGray))
            self.ui.treeWidget.addTopLevelItem(item)
            for i in range(self.ui.treeWidget.columnCount()):
                 self.ui.treeWidget.resizeColumnToContents(i)
            #self.ui.treeWidget.scrollToItem(item)
            
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_itemClicked(self, item, column):
        index = self.ui.treeWidget.indexOfTopLevelItem(item)
        self.ui.treeWidget_cmdinfo.clear()
        if self.buf[index][2]:
            self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, ('cmdType', item.text(1))))
            self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, ('--', '--')))
            for i in self.buf[index][2].items():
                self.ui.treeWidget_cmdinfo.addTopLevelItem(QTreeWidgetItem(None, i))
            self.ui.treeWidget_cmdinfo.resizeColumnToContents(0)
        self.ui.plainTextEdit_rawdata.setPlainText(self.buf[index][3])
        
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_cmdinfo_itemClicked(self, item, column):
        self.ui.plainTextEdit_cinfoval.setPlainText(item.text(1))
