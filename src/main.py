
import os
import sys
from   PyQt5.Qt                 import Qt
from   PyQt5.QtWidgets          import QButtonGroup, QLabel, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QProgressBar, QListWidget, QListWidgetItem, QWidget, QApplication, QAbstractItemView, QSlider, QSpinBox, QDoubleSpinBox, QRadioButton, QFrame
from   PyQt5.QtCore             import QSize, QByteArray, pyqtSignal
from   PyQt5.QtGui              import QIcon, QPixmap
from   multiprocessing          import Process

from   taskListView             import TaskListView
from   misc                     import PorotechIcon
from   watermarkSetup           import WatermarkUI
from   pyqttoast                import Toast, ToastPreset
from   pdfProcessor             import *

file_ext = ["doc", "docx", "ppt", "pptx", "pdf"]
debug    = Debugger()

class PDFConvertWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.runState         = False
		self.currentProcessor = None
		self.control          = WatermarkUI()
		self.layout           = QGridLayout()
		
		self.layout.addWidget (self.control,          0, 0, 2, 1)
		self.layout.addLayout (self.listUISetup(),    0, 1, 1, 1)
		self.layout.addLayout (self.executeUISetup(), 1, 1, 1, 1)
		self.layout.setColumnStretch(1, 1)

		self.setLayout(self.layout)
		self.signalSetup()
		self.resize(950,300)
		self.setWindowTitle ("PDF Converter")
		self.setWindowIcon(PorotechIcon().icon);
		self.control.loadValue()
			
	def listUISetup(self):
		self.float_layout     = QGridLayout()
		self.task_listwidget  = TaskListView()
		self.background_label = QLabel(f"Drag / Drop documents\n\n\nSupported format: \n{', '.join([e.lower() for e in file_ext])}")
		self.delete_button    = QPushButton("clear")

		self.delete_button.setFixedSize(45, 25)
		self.background_label.setAlignment(Qt.AlignCenter)
		self.background_label.setStyleSheet("font-size: 20px; color:#aaa; font-family: Calibri; font-style: normal;font-size: 18pt; ")
		self.delete_button.clicked.connect(lambda : self.task_listwidget.clear())
		self.task_listwidget.setDragDropMode(QAbstractItemView.DragDrop)
		self.task_listwidget.setMinimumHeight(200)

		self.float_layout.addWidget (self.background_label, 0, 0, 4, 4)
		self.float_layout.addWidget (self.task_listwidget,  0, 0, 4, 4)
		self.float_layout.addWidget (self.delete_button,    3, 3, 1, 1)
		return self.float_layout

		
	def executeUISetup(self):
		self.execute_layout = QHBoxLayout()
		self.execute_button = QPushButton("execute")
		self.execute_layout.addStretch()
		self.execute_layout.addWidget (self.execute_button)
		self.execute_layout.addStretch()
		return self.execute_layout

	def signalSetup(self):
		self.execute_button.clicked.connect(self.executeProcess)

	def closeEvent(self, event):
		self.task_listwidget.model().modelReset.disconnect()
		self.control.saveValue()
		event.accept()

	def executeProcess(self):
		self.setRunState(not(self.runState))
		
		if self.runState:
			arg = self.control.value()
			p   = Process(target = self.processFile(arg))
			p.start()
			p.join()

		else:
			if self.currentProcessor:
				self.currentProcessor.run = False

	def notice(self, title, information):
		self.toast = Toast()
		self.toast.setDuration(5000)  # Hide after 5 seconds
		self.toast.setTitle(title)
		self.toast.setText(information)
		self.toast.applyPreset(ToastPreset.SUCCESS)  # Apply style preset
		self.toast.show()				


	def processFile(self, arg):

		for row in range(self.task_listwidget.count()):
			if not(self.runState):break

			QCoreApplication.processEvents()
			item      = self.task_listwidget.item(row)
			widget    = self.task_listwidget.itemWidget(item)
			in_name   = widget.filePath
			procrssor = PDFProcessor(self)


			if procrssor:
				arg = arg | {"filePath" :in_name}
				self.currentProcessor = procrssor
				procrssor.percentage.connect(lambda value : widget.setProgress(int(value)))
				procrssor.fileError.connect( lambda       : widget.setError("Not exist"))
				procrssor.finished.connect( lambda  path  : self.notice("File saved", f"Path {path}"))
				procrssor.process(**arg)
			else:
				debug.print("Invalid item %s" % in_name)

		self.currentProcessor = None
		self.setRunState(False)

	def setRunState(self, status):
		self.runState = status
		self.execute_button.setText("cancel" if status else "execute")
		_ = [widget.setEnabled(not(self.runState)) for widget in [
			self.task_listwidget, 
			self.delete_button,
		]]



if __name__ == '__main__':
	debug.debug  = True
	app    = QApplication(sys.argv)
	window = PDFConvertWidget()
	window.show()
	sys.exit(app.exec_())