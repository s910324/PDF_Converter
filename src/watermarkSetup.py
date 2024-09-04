
from   PyQt5.Qt                 import *
from   PyQt5.QtCore             import *
from   PyQt5.QtWidgets          import *

class ColorEdit(QLineEdit):
	def __init__(self, color = "#FFFFFF", parent=None):
		super(ColorEdit, self).__init__(parent)
		self.colorSelector = QColorDialog()
		self.currentColor  = None
		self.setColor(color)
		self.setReadOnly(True)
		self.setAlignment(Qt.AlignCenter)

	def mousePressEvent(self, e):
		color = self.colorSelector.getColor(initial = self.currentColor or Qt.white)
		self.setColor(color.name())

	def setColor(self, color):
		color = QColor(color)
		if color.isValid():
			self.currentColor = color
			self.setText(color.name().upper())
			self.setStyleSheet(f"QLineEdit{{ Background-color : {color.name()} }}")

class FontEdit(QComboBox):
	def __init__(self, font_name = "Calibri", parent=None):
		super(FontEdit, self).__init__(parent)
		self.font_names = QFontDatabase().families()
		self.addItems(self.font_names)
		self.setFont(font_name)


	def setFont(self, font_name):
		index = 0

		if font_name in self.font_names:
			index = self.font_names.index(font_name)

		self.setCurrentIndex(index)
		#self.currentIndexChanged.connect(lambda i : self.setStyleSheet(f"QComboBox{{ font-family : {self.names[i]} }}"))


class WatermarkUI(QWidget):
	def __init__(self, parent=None):
		super(WatermarkUI, self).__init__(parent)
		self.watermark    = QLineEdit()
		self.font_name    = FontEdit()
		self.font_size    = QSpinBox() 
		self.color        = ColorEdit()
		self.fill_opacity = QDoubleSpinBox() 
		self.x            = QSpinBox() 
		self.y            = QSpinBox() 
		self.rotate       = QSpinBox() 
		self.row          = QSpinBox() 
		self.column       = QSpinBox() 
		self.grid         = QGridLayout()

		self.grid.addWidget(QLabel("Water mark")    , 0, 0, 1, 1)
		self.grid.addWidget(QLabel("Font")          , 1, 0, 1, 1)
		self.grid.addWidget(QLabel("Font size")     , 2, 0, 1, 1)
		self.grid.addWidget(QLabel("Font color")    , 3, 0, 1, 1)
		self.grid.addWidget(QLabel("Font opacity")  , 4, 0, 1, 1)
		self.grid.addWidget(QLabel("Font location") , 5, 0, 1, 1)
		self.grid.addWidget(QLabel("Font size")     , 6, 0, 1, 1)
		self.grid.addWidget(QLabel("Font rotation") , 7, 0, 1, 1)
		self.grid.addWidget(QLabel("Row counts")    , 8, 0, 1, 1)
		self.grid.addWidget(QLabel("Column counts") , 9, 0, 1, 1)

		self.grid.addWidget(self.watermark          , 0, 1, 1, 1)
		self.grid.addWidget(self.font_name          , 1, 1, 1, 1)
		self.grid.addWidget(self.font_size          , 2, 1, 1, 1)
		self.grid.addWidget(self.color              , 3, 1, 1, 1)
		self.grid.addWidget(self.fill_opacity       , 4, 1, 1, 1)
		self.grid.addWidget(self.x                  , 5, 1, 1, 1)
		self.grid.addWidget(self.y                  , 6, 1, 1, 1)
		self.grid.addWidget(self.rotate             , 7, 1, 1, 1)
		self.grid.addWidget(self.row                , 8, 1, 1, 1)
		self.grid.addWidget(self.column             , 9, 1, 1, 1)
		self.grid.setRowStretch(10, 1)
		self.setLayout(self.grid)

		
		for ctrl in [self.watermark, self.font_name, self.font_size, self.color, self.fill_opacity, self.x, self.y, self.rotate , self.row, self.column, ]:
			ctrl.setMinimumHeight(25)
			try:
				ctrl.setAlignment(Qt.AlignCenter)
			except:
				pass

	def value(self):
		return {
				"watermark"     : self.watermark.text(), 
				"font_name"     : "Helvetica-Bold", 
				"font_size"     : 25, 
				"fill_color"    : '#DD5555',        
				"fill_opacity"  : 0.15, 
				"x"             : -500, 
				"y"             : 500, 
				"rotate"        : 30, 
				"row"           : 15, 
				"column"        : 15, 
				"row_pitch"     : None, 
				"column_pitch"  : None
			}
if __name__ == '__main__':
	import sys

	app    = QApplication(sys.argv)

	window = WatermarkUI()
	window.show()
	sys.exit(app.exec_())