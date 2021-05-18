import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

CSS ={
    'QWidget':
    {
        'background-color': '#333333',
    },
    'QLabel#label':
    {
        'color': '#888888',
        'background-color': '#444444',
        'font-weight': 'bold',
    },
    'QLabel#label:active':
    {
        'color': '#1d90cd',
    },
    'QPushButton#button':
    {
        'color': '#888888',
        'background-color': '#444444',
        'font-weight': 'bold',
        'border': 'none',
        'padding': '5px',
    },
    'QPushButton#button:active':
    {
        'color': '#ffffff',
    },
    'QPushButton#button:hover':
    {
        'color': '#1d90cd',
    }
}

def dictToCSS(dictionnary):
    stylesheet = ""
    for item in dictionnary:
        stylesheet += item + "\n{\n"
        for attribute in dictionnary[item]:
            stylesheet += "  " + attribute + ": " + dictionnary[item][attribute] + ";\n"
        stylesheet += "}\n"
    return stylesheet

class Main_GUI(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet(dictToCSS(CSS))

        self.vert_lay = QtWidgets.QVBoxLayout()

        self.ticker_vert_layout = QtWidgets.QVBoxLayout()
        self.ticker_vert_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        #self.ticker_vert_layout.setObjectName("ticker_vert_layout")

        self.dateTimeEdit = QtWidgets.QDateTimeEdit()
        self.dateTimeEdit.setMinimumSize(QtCore.QSize(150, 30))
        self.dateTimeEdit.setMaximumSize(QtCore.QSize(150, 30))
        #self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.ticker_vert_layout.addWidget(self.dateTimeEdit)

        self.asset_watch_label = QtWidgets.QLabel()
        self.asset_watch_label.setMinimumSize(QtCore.QSize(0, 15))
        self.asset_watch_label.setMaximumSize(QtCore.QSize(150, 20))
        #self.asset_watch_label.setObjectName("asset_watch_label")
        self.ticker_vert_layout.addWidget(self.asset_watch_label, 0, QtCore.Qt.AlignTop)

        self.spy_ticker = QtWidgets.QLabel()
        self.spy_ticker.setMinimumSize(QtCore.QSize(150, 10))
        self.spy_ticker.setMaximumSize(QtCore.QSize(150, 20))
        #self.spy_ticker.setObjectName("spy_ticker")
        self.ticker_vert_layout.addWidget(self.spy_ticker)

        self.eth_ticker = QtWidgets.QLabel()
        self.eth_ticker.setMinimumSize(QtCore.QSize(150, 10))
        self.eth_ticker.setMaximumSize(QtCore.QSize(150, 20))
        #self.eth_ticker.setObjectName("eth_ticker")
        self.ticker_vert_layout.addWidget(self.eth_ticker)

        self.btc_ticker = QtWidgets.QLabel()
        self.btc_ticker.setMinimumSize(QtCore.QSize(150, 10))
        self.btc_ticker.setMaximumSize(QtCore.QSize(150, 20))
        #self.btc_ticker.setObjectName("btc_ticker")
        self.ticker_vert_layout.addWidget(self.btc_ticker)

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(150, 10))
        self.pushButton.setMaximumSize(QtCore.QSize(150, 20))
        #self.pushButton.setObjectName("pushButton")
        self.ticker_vert_layout.addWidget(self.pushButton)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ticker_vert_layout.addItem(spacerItem)

        self.vert_lay.addItem(self.ticker_vert_layout)

        self.setLayout(self.vert_lay)

        #File menu actions
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        #initialize statusbar and menubar
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        self.menubar = self.menuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 857, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalysis = QtWidgets.QMenu(self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)

        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        #self.retranslateUi(MainWindow)
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.show()
if __name__== '__main__':
    app = QtWidgets.QApplication([])
    gui = Main_GUI(app)
    sys.exit(app.exec_())
