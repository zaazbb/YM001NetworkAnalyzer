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
        self.treeWidget_cmdinfo.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget_cmdinfo)
        self.plainTextEdit_pktdata = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit_pktdata.setObjectName("plainTextEdit_pktdata")
        self.verticalLayout.addWidget(self.plainTextEdit_pktdata)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_autoscroll = QtWidgets.QCheckBox(self.tab)
        self.checkBox_autoscroll.setChecked(True)
        self.checkBox_autoscroll.setObjectName("checkBox_autoscroll")
        self.horizontalLayout.addWidget(self.checkBox_autoscroll)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_chnlgrp = QtWidgets.QComboBox(self.tab)
        self.comboBox_chnlgrp.setEnabled(False)
        self.comboBox_chnlgrp.setMaximumSize(QtCore.QSize(40, 16777215))
        self.comboBox_chnlgrp.setObjectName("comboBox_chnlgrp")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.comboBox_chnlgrp.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_chnlgrp)
        self.pushButton_parsepkt = QtWidgets.QPushButton(self.tab)
        self.pushButton_parsepkt.setEnabled(False)
        self.pushButton_parsepkt.setObjectName("pushButton_parsepkt")
        self.horizontalLayout.addWidget(self.pushButton_parsepkt)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_3.setStretch(0, 1)
        self.treeWidget.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.treeWidget_node = QtWidgets.QTreeWidget(self.tab_2)
        self.treeWidget_node.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_node.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_node.setObjectName("treeWidget_node")
        self.horizontalLayout_5.addWidget(self.treeWidget_node)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeWidget_rdbglst = QtWidgets.QTreeWidget(self.tab_2)
        self.treeWidget_rdbglst.setIndentation(0)
        self.treeWidget_rdbglst.setObjectName("treeWidget_rdbglst")
        self.verticalLayout_3.addWidget(self.treeWidget_rdbglst)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_rdbgaddr = QtWidgets.QLabel(self.tab_2)
        self.label_rdbgaddr.setObjectName("label_rdbgaddr")
        self.horizontalLayout_4.addWidget(self.label_rdbgaddr)
        self.spinBox_rdbglen = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_rdbglen.setMinimum(1)
        self.spinBox_rdbglen.setMaximum(128)
        self.spinBox_rdbglen.setDisplayIntegerBase(10)
        self.spinBox_rdbglen.setObjectName("spinBox_rdbglen")
        self.horizontalLayout_4.addWidget(self.spinBox_rdbglen)
        self.pushButton_rdbgsend = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_rdbgsend.setEnabled(False)
        self.pushButton_rdbgsend.setObjectName("pushButton_rdbgsend")
        self.horizontalLayout_4.addWidget(self.pushButton_rdbgsend)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.plainTextEdit_rdbgresp = QtWidgets.QPlainTextEdit(self.tab_2)
        self.plainTextEdit_rdbgresp.setMaximumSize(QtCore.QSize(16777215, 100))
        self.plainTextEdit_rdbgresp.setPlainText("")
        self.plainTextEdit_rdbgresp.setObjectName("plainTextEdit_rdbgresp")
        self.verticalLayout_3.addWidget(self.plainTextEdit_rdbgresp)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.setStretch(0, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar_upgrade = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar_upgrade.setProperty("value", 0)
        self.progressBar_upgrade.setObjectName("progressBar_upgrade")
        self.horizontalLayout_2.addWidget(self.progressBar_upgrade)
        self.checkBox_bcast = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_bcast.setObjectName("checkBox_bcast")
        self.horizontalLayout_2.addWidget(self.checkBox_bcast)
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
        self.horizontalLayout_2.setStretch(0, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
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
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionRdbgPoolType = QtWidgets.QAction(MainWindow)
        self.actionRdbgPoolType.setObjectName("actionRdbgPoolType")
        self.actionEraseParam = QtWidgets.QAction(MainWindow)
        self.actionEraseParam.setObjectName("actionEraseParam")

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
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "mI"))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "pid"))
        self.treeWidget.headerItem().setText(6, _translate("MainWindow", "mDst"))
        self.treeWidget.headerItem().setText(7, _translate("MainWindow", "mSrc"))
        self.treeWidget.headerItem().setText(8, _translate("MainWindow", "nDst"))
        self.treeWidget.headerItem().setText(9, _translate("MainWindow", "nSrc"))
        self.treeWidget.headerItem().setText(10, _translate("MainWindow", "nI"))
        self.treeWidget.headerItem().setText(11, _translate("MainWindow", "r"))
        self.treeWidget.headerItem().setText(12, _translate("MainWindow", "routeLst"))
        self.treeWidget.headerItem().setText(13, _translate("MainWindow", "aI"))
        self.treeWidget.headerItem().setText(14, _translate("MainWindow", "aDUI"))
        self.treeWidget_cmdinfo.headerItem().setText(0, _translate("MainWindow", "key"))
        self.treeWidget_cmdinfo.headerItem().setText(1, _translate("MainWindow", "value"))
        self.checkBox_autoscroll.setText(_translate("MainWindow", "autoscroll"))
        self.label.setText(_translate("MainWindow", "chnlgrp"))
        self.comboBox_chnlgrp.setItemText(0, _translate("MainWindow", "0"))
        self.comboBox_chnlgrp.setItemText(1, _translate("MainWindow", "1"))
        self.comboBox_chnlgrp.setItemText(2, _translate("MainWindow", "2"))
        self.comboBox_chnlgrp.setItemText(3, _translate("MainWindow", "3"))
        self.comboBox_chnlgrp.setItemText(4, _translate("MainWindow", "4"))
        self.comboBox_chnlgrp.setItemText(5, _translate("MainWindow", "5"))
        self.comboBox_chnlgrp.setItemText(6, _translate("MainWindow", "6"))
        self.comboBox_chnlgrp.setItemText(7, _translate("MainWindow", "7"))
        self.comboBox_chnlgrp.setItemText(8, _translate("MainWindow", "8"))
        self.comboBox_chnlgrp.setItemText(9, _translate("MainWindow", "9"))
        self.comboBox_chnlgrp.setItemText(10, _translate("MainWindow", "10"))
        self.comboBox_chnlgrp.setItemText(11, _translate("MainWindow", "11"))
        self.comboBox_chnlgrp.setItemText(12, _translate("MainWindow", "12"))
        self.comboBox_chnlgrp.setItemText(13, _translate("MainWindow", "13"))
        self.comboBox_chnlgrp.setItemText(14, _translate("MainWindow", "14"))
        self.comboBox_chnlgrp.setItemText(15, _translate("MainWindow", "15"))
        self.comboBox_chnlgrp.setItemText(16, _translate("MainWindow", "16"))
        self.comboBox_chnlgrp.setItemText(17, _translate("MainWindow", "17"))
        self.comboBox_chnlgrp.setItemText(18, _translate("MainWindow", "18"))
        self.comboBox_chnlgrp.setItemText(19, _translate("MainWindow", "19"))
        self.comboBox_chnlgrp.setItemText(20, _translate("MainWindow", "20"))
        self.comboBox_chnlgrp.setItemText(21, _translate("MainWindow", "21"))
        self.comboBox_chnlgrp.setItemText(22, _translate("MainWindow", "22"))
        self.comboBox_chnlgrp.setItemText(23, _translate("MainWindow", "23"))
        self.comboBox_chnlgrp.setItemText(24, _translate("MainWindow", "24"))
        self.comboBox_chnlgrp.setItemText(25, _translate("MainWindow", "25"))
        self.comboBox_chnlgrp.setItemText(26, _translate("MainWindow", "26"))
        self.comboBox_chnlgrp.setItemText(27, _translate("MainWindow", "27"))
        self.comboBox_chnlgrp.setItemText(28, _translate("MainWindow", "28"))
        self.comboBox_chnlgrp.setItemText(29, _translate("MainWindow", "29"))
        self.comboBox_chnlgrp.setItemText(30, _translate("MainWindow", "30"))
        self.comboBox_chnlgrp.setItemText(31, _translate("MainWindow", "31"))
        self.comboBox_chnlgrp.setItemText(32, _translate("MainWindow", "32"))
        self.pushButton_parsepkt.setText(_translate("MainWindow", "ParsePkt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "packet"))
        self.treeWidget_node.headerItem().setText(0, _translate("MainWindow", "node"))
        self.treeWidget_node.headerItem().setText(1, _translate("MainWindow", "sver"))
        self.treeWidget_node.headerItem().setText(2, _translate("MainWindow", "upgRate"))
        self.treeWidget_node.headerItem().setText(3, _translate("MainWindow", "bpFlag"))
        self.treeWidget_rdbglst.headerItem().setText(0, _translate("MainWindow", "var"))
        self.treeWidget_rdbglst.headerItem().setText(1, _translate("MainWindow", "addr"))
        self.treeWidget_rdbglst.headerItem().setText(2, _translate("MainWindow", "len"))
        self.label_rdbgaddr.setText(_translate("MainWindow", "addr"))
        self.pushButton_rdbgsend.setText(_translate("MainWindow", "Send"))
        self.progressBar_upgrade.setFormat(_translate("MainWindow", "%v/%m"))
        self.checkBox_bcast.setText(_translate("MainWindow", "bcast"))
        self.checkBox_upgauto.setToolTip(_translate("MainWindow", "after chngm&send,auto readbp & calcbp,and reloop,until bp is allone."))
        self.checkBox_upgauto.setText(_translate("MainWindow", "auto"))
        self.checkBox_usebp.setToolTip(_translate("MainWindow", "used when auto is unchecked.calcbp before chngm&send."))
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
        self.actionClear.setText(_translate("MainWindow", "clear"))
        self.actionRdbgPoolType.setText(_translate("MainWindow", "rdbgPoolType"))
        self.actionEraseParam.setText(_translate("MainWindow", "eraseParam"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

