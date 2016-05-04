
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem
from PyQt5.QtCore import QTimer
from Ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, conn):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.conn = conn
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        
        #plainTextEdit
    def update(self):
        if self.conn.poll():
            msg = self.conn.recv()
            print(msg)
            self.ui.treeWidget.insertTopLevelItems(
                0, [QTreeWidgetItem(None, msg[0])])
