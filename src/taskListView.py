
from   PyQt5.Qt                 import Qt, QApplication
from   PyQt5.QtCore             import QSize
from   PyQt5.QtWidgets          import QListWidget, QListWidgetItem, QAbstractItemView
from   taskListWidget           import TaskListWidget
from   misc                     import *


file_ext = ["doc", "docx", "ppt", "pptx", "pdf"]
debug    = Debugger()

class TaskListView(QListWidget):
	def __init__(self, parent=None):
		super(TaskListView, self).__init__(parent)
		self.setAcceptDrops(True)
		self.setIconSize(QSize(72, 72))
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.viewport().setAutoFillBackground( False )
		self.itemChanged.connect(lambda : self.viewport().setAutoFillBackground( self.count() > 0 ))
		self.model().rowsRemoved.connect(lambda: self.viewport().setAutoFillBackground( self.count() > 0 ))
		# self.model().modelReset.connect(lambda: self.viewport().setAutoFillBackground( self.count() > 0 ))


	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls:
			event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls:
			event.setDropAction(Qt.CopyAction)
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasUrls:
			event.setDropAction(Qt.CopyAction)
			event.accept()
			links = []
			for url in event.mimeData().urls():
				links.append(str(url.toLocalFile()))
			self.addFileItems(links)
		else:
			event.ignore()


	def addFileItems(self, filePath_list):
		for filePath in filePath_list:
			if (filePath.lower().split(".")[-1] in file_ext):
				debug.print("add file %s" % filePath)
				item        = QListWidgetItem(self)
				row         = TaskListWidget(filePath, item)
				row.remove.connect(lambda  i: self.takeItem (self.row(i)))
				self.addItem(item)
				item.setSizeHint(row.minimumSizeHint())
				self.setItemWidget(item, row)
			else:
				debug.print("add file error %s" % filePath)

if __name__ == '__main__':
	import sys
	debug.debug  = True
	app    = QApplication(sys.argv)
	window = TaskListView()
	window.show()
	sys.exit(app.exec_())