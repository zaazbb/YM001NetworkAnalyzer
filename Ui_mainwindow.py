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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.treeWidget = QtWidgets.QTreeWidget(self.tab)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.setIndentation(0)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setObjectName("treeWidget")
        self.horizontalLayout_3.addWidget(self.treeWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget_cmdinfo = QtWidgets.QTreeWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget_cmdinfo.sizePolicy().hasHeightForWidth())
        self.treeWidget_cmdinfo.setSizePolicy(sizePolicy)
        self.treeWidget_cmdinfo.setIndentation(0)
        self.treeWidget_cmdinfo.setObjectName("treeWidget_cmdinfo")
        self.treeWidget_cmdinfo.header().setVisible(True)
        self.verticalLayout.addWidget(self.treeWidget_cmdinfo)
        self.plainTextEdit_pktdata = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit_pktdata.setObjectName("plainTextEdit_pktdata")
        self.verticalLayout.addWidget(self.plainTextEdit_pktdata)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_parsepkt = QtWidgets.QPushButton(self.tab)
        self.pushButton_parsepkt.setEnabled(False)
        self.pushButton_parsepkt.setObjectName("pushButton_parsepkt")
        self.horizontalLayout.addWidget(self.pushButton_parsepkt)
        self.pushButton_mkpkt = QtWidgets.QPushButton(self.tab)
        self.pushButton_mkpkt.setEnabled(False)
        self.pushButton_mkpkt.setObjectName("pushButton_mkpkt")
        self.horizontalLayout.addWidget(self.pushButton_mkpkt)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_3.setStretch(0, 1)
        self.treeWidget.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeWidget_node = QtWidgets.QTreeWidget(self.tab_2)
        self.treeWidget_node.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_node.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_node.setObjectName("treeWidget_node")
        self.verticalLayout_3.addWidget(self.treeWidget_node)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar_upgrade = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar_upgrade.setProperty("value", 0)
        self.progressBar_upgrade.setObjectName("progressBar_upgrade")
        self.horizontalLayout_2.addWidget(self.progressBar_upgrade)
        self.checkBox_upgauto = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_upgauto.setObjectName("checkBox_upgauto")
        self.horizontalLayout_2.addWidget(self.checkBox_upgauto)
        self.checkBox_usebp = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_usebp.setObjectName("checkBox_usebp")
        self.horizontalLayout_2.addWidget(self.checkBox_usebp)
        self.pushButton_upgrade = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_upgrade.setEnabled(False)
        self.pushButton_upgrade.setObjectName("pushButton_upgrade")
        self.horizontalLayout_2.addWidget(self.pushButton_upgrade)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.plainTextEdit_log = QtWidgets.QPlainTextEdit(self.splitter)
        self.plainTextEdit_log.setObjectName("plainTextEdit_log")
        self.verticalLayout_2.addWidget(self.splitter)
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
        self.actionRmParsed = QtWidgets.QAction(MainWindow)
        self.actionRmParsed.setObjectName("actionRmParsed")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "time"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "from"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "mFType"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "ack"))
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "fIdx"))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "pid"))
        self.treeWidget.headerItem().setText(6, _translate("MainWindow", "mDst"))
        self.treeWidget.headerItem().setText(7, _translate("MainWindow", "mSrc"))
        self.treeWidget.headerItem().setText(8, _translate("MainWindow", "nDst"))
        self.treeWidget.headerItem().setText(9, _translate("MainWindow", "nSrc"))
        self.treeWidget.headerItem().setText(10, _translate("MainWindow", "fIdx"))
        self.treeWidget.headerItem().setText(11, _translate("MainWindow", "r"))
        self.treeWidget.headerItem().setText(12, _translate("MainWindow", "routeLst"))
        self.treeWidget.headerItem().setText(13, _translate("MainWindow", "aDUI"))
        self.treeWidget_cmdinfo.headerItem().setText(0, _translate("MainWindow", "key"))
        self.treeWidget_cmdinfo.headerItem().setText(1, _translate("MainWindow", "value"))
        self.pushButton_parsepkt.setText(_translate("MainWindow", "ParsePkt"))
        self.pushButton_mkpkt.setText(_translate("MainWindow", "MakePkt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "packet"))
        self.treeWidget_node.headerItem().setText(0, _translate("MainWindow", "node"))
        self.treeWidget_node.headerItem().setText(1, _translate("MainWindow", "sver"))
        self.treeWidget_node.headerItem().setText(2, _translate("MainWindow", "upgRate"))
        self.treeWidget_node.headerItem().setText(3, _translate("MainWindow", "bpFlag"))
        self.progressBar_upgrade.setFormat(_translate("MainWindow", "%v/%m"))
        self.checkBox_upgauto.setText(_translate("MainWindow", "auto"))
        self.checkBox_usebp.setText(_translate("MainWindow", "usebp"))
        self.pushButton_upgrade.setText(_translate("MainWindow", "upgrade"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "node"))
        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionUpgBpSts.setText(_translate("MainWindow", "upgBpSts"))
        self.actionUpgTxm.setText(_translate("MainWindow", "upgTxm"))
        self.actionRdSnCfg.setText(_translate("MainWindow", "rdSnCfg"))
        self.actionUpgRdBack.setText(_translate("MainWindow", "upgRdBack"))
        self.actionRmParsed.setText(_translate("MainWindow", "rmParsed"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

