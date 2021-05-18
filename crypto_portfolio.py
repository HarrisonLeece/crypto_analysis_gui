import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, qApp, QWidget
from PyQt5.QtGui import QIcon

import OpenGL.GL as gl        # python wrapping of OpenGL
from OpenGL import GLU

import logging

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

#Copy-past from https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
class QPlainTextEditLogger(logging.Handler):
	def __init__(self, parent):
		super().__init__()
		self.widget = QtWidgets.QPlainTextEdit(parent)
		self.widget.setReadOnly(True)

	def emit(self, record):
		msg = self.format(record)
		self.widget.appendPlainText(msg)

#Some copy-past from https://nrotella.github.io/journal/first-steps-python-qt-opengl.html
#which uses pyqt4
class GLWidget(QtWidgets.QOpenGLWidget):
	def __init__(self, parent=None):
		self.parent = parent
		QtWidgets.QOpenGLWidget.__init__(self, parent)
		#super().__init__(self, parent)

	def initializeGL(self):
		self.qglClearColor(QtGui.QColor(0, 0, 255))    # initialize the screen to blue
		gl.glEnable(gl.GL_DEPTH_TEST)                  # enable depth testing

class Main(QtWidgets.QMainWindow):
	def __init__(self, parent):
		super().__init__()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setStyleSheet(dictToCSS(CSS))
		self.resize(857, 555)

		#You can't set a QLayout directly on the QMainWindow. You need to create
		# a QWidget and set it as the central widget on the QMainWindow and
		#assign the QLayout to that. https://stackoverflow.com/questions/37304684/qwidgetsetlayout-attempting-to-set-qlayout-on-mainwindow-which-already
		self.main_widget = QWidget(self)
		self.setCentralWidget(self.main_widget)

		#Establish vertical layout for the whole screen
		self.big_vertical_layout = QtWidgets.QVBoxLayout()
		#self.big_vertical_layout.setObjectName("big_vertical_layout")
		self.ticker_plotter_layout = QtWidgets.QHBoxLayout()
		self.ticker_plotter_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
		#self.ticker_plotter_layout.setObjectName("ticker_plotter_layout")
		self.ticker_vert_layout = QtWidgets.QVBoxLayout()
		self.ticker_vert_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
		#self.ticker_vert_layout.setObjectName("ticker_vert_layout")

		self.dateTimeEdit = QtWidgets.QDateTimeEdit()
		self.dateTimeEdit.setMinimumSize(QtCore.QSize(150, 30))
		self.dateTimeEdit.setMaximumSize(QtCore.QSize(150, 30))
		self.check_time_thread = QtCore.QTimer(self)
		self.check_time_thread.setInterval(500) #.5 seconds
		self.check_time_thread.timeout.connect(self.update_clock)
		#self.dateTimeEdit.setObjectName("dateTimeEdit")
		self.ticker_vert_layout.addWidget(self.dateTimeEdit)

		self.asset_watch_label = QtWidgets.QLabel("Asset Watcher")
		self.asset_watch_label.setMinimumSize(QtCore.QSize(0, 15))
		self.asset_watch_label.setMaximumSize(QtCore.QSize(150, 20))
		#self.asset_watch_label.setObjectName("asset_watch_label")
		self.ticker_vert_layout.addWidget(self.asset_watch_label, 0, QtCore.Qt.AlignTop)

		self.spy_ticker = QtWidgets.QLabel('SPY')
		self.spy_ticker.setMinimumSize(QtCore.QSize(150, 10))
		self.spy_ticker.setMaximumSize(QtCore.QSize(150, 20))
		#self.spy_ticker.setObjectName("spy_ticker")
		self.ticker_vert_layout.addWidget(self.spy_ticker)

		self.eth_ticker = QtWidgets.QLabel('ETH')
		self.eth_ticker.setMinimumSize(QtCore.QSize(150, 10))
		self.eth_ticker.setMaximumSize(QtCore.QSize(150, 20))
		#self.eth_ticker.setObjectName("eth_ticker")
		self.ticker_vert_layout.addWidget(self.eth_ticker)

		self.btc_ticker = QtWidgets.QLabel('BTC')
		self.btc_ticker.setMinimumSize(QtCore.QSize(150, 10))
		self.btc_ticker.setMaximumSize(QtCore.QSize(150, 20))
		#self.btc_ticker.setObjectName("btc_ticker")
		self.ticker_vert_layout.addWidget(self.btc_ticker)

		self.pushButton = QtWidgets.QPushButton('+ asset' )
		self.pushButton.setMinimumSize(QtCore.QSize(150, 10))
		self.pushButton.setMaximumSize(QtCore.QSize(150, 20))
		#self.pushButton.setObjectName("pushButton")
		self.ticker_vert_layout.addWidget(self.pushButton)

		spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.ticker_vert_layout.addItem(spacerItem)
		self.ticker_plotter_layout.addLayout(self.ticker_vert_layout)

		#Setup plotter viewport
		self.ploter_viewport = GLWidget(self)
		self.ploter_viewport.setMinimumSize(QtCore.QSize(400, 400))
		self.ploter_viewport.setObjectName("ploter_viewport")
		self.ticker_plotter_layout.addWidget(self.ploter_viewport)
		self.ticker_plotter_layout.setStretch(0, 1)
		self.big_vertical_layout.addLayout(self.ticker_plotter_layout)

		#Console log and options grid setup
		self.console_log = QPlainTextEditLogger(self)
		self.console_log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
		#https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt
		logging.getLogger().addHandler(self.console_log)
		self.console_log.widget.setMaximumSize(QtCore.QSize(16777215, 50))
		#self.console_log.setObjectName("console_log")
		#You must add the object>.widget< to allow custom objects to add to layout
		self.big_vertical_layout.addWidget(self.console_log.widget)
		self.options_grid = QtWidgets.QGridLayout()
		self.options_grid.setObjectName("options_grid")
		self.load_data_button = QtWidgets.QPushButton("Load Data")
		self.load_data_button.setObjectName("load_data_button")
		self.options_grid.addWidget(self.load_data_button, 0, 0, 1, 1)
		self.log_axes_button = QtWidgets.QPushButton("Toggle Axes")
		self.log_axes_button.setObjectName("log_axes_button")
		self.options_grid.addWidget(self.log_axes_button, 0, 1, 1, 1)
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.options_grid.addItem(spacerItem1, 0, 2, 1, 1)
		#Add options gtrid to the bottom of the big vertical layout
		self.big_vertical_layout.addLayout(self.options_grid)

		###Connect buttons to functions
		##Load Data
		self.load_data_button.clicked.connect(self.logger_test)
		##Toggle Axes

		# Set the window's main layout
		self.main_widget.setLayout(self.big_vertical_layout)

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

	def logger_test(self):
		logging.debug('debug')
		logging.info('info')
		logging.warning('Test')
		logging.error('successful')

	def update_clock(self):
		pass

if __name__== '__main__':
	app = QtWidgets.QApplication([])
	gui = Main(app)
	sys.exit(app.exec_())
