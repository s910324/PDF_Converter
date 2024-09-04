from   PyQt5.Qt                 import Qt, QApplication, pyqtSignal
from   PyQt5.QtWidgets          import QWidget, QLabel, QProgressBar, QPushButton, QGridLayout

class TaskListWidget(QWidget):
	remove = pyqtSignal(object)
	def __init__(self, path, item=None, parent=None):
		super(TaskListWidget, self).__init__(parent)
		self.item           = item
		self.fileName_label = QLabel(path.split("/")[-1])
		self.process_label  = QLabel("0%")
		self.progress_bar   = QProgressBar()
		self.delete_button  = QPushButton("x")

		self.filePath       = path
		self.progress       = 0
		self.layout         = QGridLayout()
		self.delete_button.clicked.connect(lambda : self.remove.emit(self.item))

		self.layout.addWidget (self.fileName_label, 0, 0, 1, 3)
		self.layout.addWidget (self.progress_bar,   1, 0, 1, 3)
		self.layout.addWidget (self.process_label,  0, 3, 2, 1)
		self.layout.addWidget (self.delete_button,  0, 4, 2, 1)	
			

		self.process_label.setFixedSize(35,35)
		self.fileName_label.setFixedHeight(15)
		self.progress_bar.setFixedHeight(3)
		self.delete_button.setFixedSize(25,25)

		self.progress_bar.setTextVisible(False)
		self.setLayout(self.layout)

	def setProgress(self, progress:int):
		self.process_label.setText(f"{progress:d}%")
		self.progress_bar.setValue(progress)

	def setError(self, error:str):
		self.process_label.setText(f"{error:s}")
		self.progress_bar.setValue(0)

if __name__ == '__main__':
	import sys
	app    = QApplication(sys.argv)
	window = TaskListWidget("test/Path")
	window.show()
	sys.exit(app.exec_())