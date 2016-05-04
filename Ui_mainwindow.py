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
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralWidget)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setObjectName("treeWidget")
        self.horizontalLayout.addWidget(self.treeWidget)
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.centralWidget)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.horizontalLayout.addWidget(self.treeWidget_2)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout.setStretch(0, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "mFrmType"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "mAck"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "mFrmIdx"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "mPanId"))
        self.treeWidget.headerItem().setText(4, _translate("MainWindow", "mDstAddr"))
        self.treeWidget.headerItem().setText(5, _translate("MainWindow", "mSrcAddr"))
        self.treeWidget.headerItem().setText(6, _translate("MainWindow", "nFrmType"))
        self.treeWidget.headerItem().setText(7, _translate("MainWindow", "nDstAddr"))
        self.treeWidget.headerItem().setText(8, _translate("MainWindow", "nSrdAddr"))
        self.treeWidget.headerItem().setText(9, _translate("MainWindow", "nFrmIdx"))
        self.treeWidget.headerItem().setText(10, _translate("MainWindow", "nRadius"))
        self.treeWidget.headerItem().setText(11, _translate("MainWindow", "nRouteLst"))
        self.treeWidget.headerItem().setText(12, _translate("MainWindow", "aFrmType"))
        self.treeWidget.headerItem().setText(13, _translate("MainWindow", "aDUI"))
        self.treeWidget_2.headerItem().setText(0, _translate("MainWindow", "域"))
        self.treeWidget_2.headerItem().setText(1, _translate("MainWindow", "值"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

