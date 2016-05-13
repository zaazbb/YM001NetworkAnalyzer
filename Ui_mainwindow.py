# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\repository\YM001NetworkAnalyzer\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.setIndentation(0)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setObjectName("treeWidget")
        self.plainTextEdit_log = QtWidgets.QPlainTextEdit(self.splitter)
        self.plainTextEdit_log.setObjectName("plainTextEdit_log")
        self.horizontalLayout.addWidget(self.splitter)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget_cmdinfo = QtWidgets.QTreeWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget_cmdinfo.sizePolicy().hasHeightForWidth())
        self.treeWidget_cmdinfo.setSizePolicy(sizePolicy)
        self.treeWidget_cmdinfo.setIndentation(0)
        self.treeWidget_cmdinfo.setObjectName("treeWidget_cmdinfo")
        self.treeWidget_cmdinfo.header().setVisible(True)
        self.verticalLayout.addWidget(self.treeWidget_cmdinfo)
        self.plainTextEdit_cinfoval = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.plainTextEdit_cinfoval.setObjectName("plainTextEdit_cinfoval")
        self.verticalLayout.addWidget(self.plainTextEdit_cinfoval)
        self.plainTextEdit_rawdata = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.plainTextEdit_rawdata.setObjectName("plainTextEdit_rawdata")
        self.verticalLayout.addWidget(self.plainTextEdit_rawdata)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionUpgBpSts = QtWidgets.QAction(MainWindow)
        self.actionUpgBpSts.setObjectName("actionUpgBpSts")
        self.actionUpgTxm = QtWidgets.QAction(MainWindow)
        self.actionUpgTxm.setObjectName("actionUpgTxm")
        self.actionRdSnCfg = QtWidgets.QAction(MainWindow)
        self.actionRdSnCfg.setObjectName("actionRdSnCfg")
        self.actionUpgRdBack = QtWidgets.QAction(MainWindow)
        self.actionUpgRdBack.setObjectName("actionUpgRdBack")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "time"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "mFType"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "ack"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "fIdx"))
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "pid"))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "mDst"))
        self.treeWidget.headerItem().setText(6, _translate("MainWindow", "mSrc"))
        self.treeWidget.headerItem().setText(7, _translate("MainWindow", "nDst"))
        self.treeWidget.headerItem().setText(8, _translate("MainWindow", "nSrc"))
        self.treeWidget.headerItem().setText(9, _translate("MainWindow", "fIdx"))
        self.treeWidget.headerItem().setText(10, _translate("MainWindow", "r"))
        self.treeWidget.headerItem().setText(11, _translate("MainWindow", "routeLst"))
        self.treeWidget.headerItem().setText(12, _translate("MainWindow", "aDUI"))
        self.treeWidget_cmdinfo.headerItem().setText(0, _translate("MainWindow", "key"))
        self.treeWidget_cmdinfo.headerItem().setText(1, _translate("MainWindow", "value"))
        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionUpgBpSts.setText(_translate("MainWindow", "upgBpSts"))
        self.actionUpgTxm.setText(_translate("MainWindow", "upgTxm"))
        self.actionRdSnCfg.setText(_translate("MainWindow", "rdSnCfg"))
        self.actionUpgRdBack.setText(_translate("MainWindow", "upgRdBack"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

