import os
import pickle
from   PyQt5.Qt                 import *
from   PyQt5.QtCore             import *
from   PyQt5.QtWidgets          import *
from   pathlib                  import Path
from reportlab.pdfbase          import _fontdata


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
		if color.isValid():
			self.setColor(color.name())

	def setColor(self, color):
		color = QColor(color)
		if color.isValid():
			self.currentColor = color
			textRGB           = 0 if  max([color.red(), color.green(), color.blue()]) > 127 else 255
			textColor         = QColor(textRGB, textRGB, textRGB)
			self.setText(color.name().upper())
			self.setStyleSheet(f"QLineEdit{{ Background-color : {color.name()}; color : {textColor.name()} }}")

	def getColor(self):
		return self.currentColor.name()

class FontEdit(QComboBox):
	def __init__(self, font_name = "Helvetica-Bold", parent=None):
		super(FontEdit, self).__init__(parent)
		self.font_names = _fontdata.standardFonts#QFontDatabase().families()
		self.addItems(self.font_names)
		self.setFont(font_name)


	def setFont(self, font_name):
		index = 0

		if font_name in self.font_names:
			index = self.font_names.index(font_name)

		self.setCurrentIndex(index)


	def getFont(self):
		return self.font_names[self.currentIndex()]

class NumberSpinBox(QDoubleSpinBox):
	def __init__(self, min_value:float = 0, max_value:float = 100, default_value = 0, step:float = 1 , decimal:int = 2, ):
		super(NumberSpinBox, self).__init__()
		self.default_value = default_value
		self.setRange(min_value, max_value)
		self.setSingleStep (step)
		self.setDecimals (decimal)
		self.setValue(default_value)
		self.setTheme()

	def value(self):
		value = super(NumberSpinBox, self).value()
		return int(value) if (self.decimals() == 0) else float(value)

	def setValue(self, value):

		corce_val = self.default_value
		try:
			corce_val = round(float(value), self.decimals())
			corce_val = sorted([self.minimum(), corce_val, self.maximum()])[1]
	
		except:
			pass

		super(NumberSpinBox, self).setValue(corce_val)


	def wheelEvent(self, *args, **kwargs):
		pass

	def setTheme(self):

		style = """

			QDoubleSpinBox {
				border-style: solid;
				border-width: 1px;
				border-color: #7e7e7e;
			}

			QDoubleSpinBox::down-button, QDoubleSpinBox::up-button {
				subcontrol-origin: margin;
				background: rgba(150, 150, 150, 50);
				width: 15px;
				height: 15px;
			}

			QDoubleSpinBox::down-button {
				subcontrol-position: center left;
				margin-left: 3px;
			}
			 
			QDoubleSpinBox::up-button {
				subcontrol-position: center right;
				margin-right: 3px;
			}
			 
			QDoubleSpinBox::down-button,
			QDoubleSpinBox::up-button {
				border-radius: 3px;
			}
			 
			QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
				subcontrol-origin: content;
				width: 10px;
				height: 10px;
			}

			"""
		self.setAlignment(Qt.AlignHCenter)
		self.setStyleSheet(style)
		


class WatermarkUI(QWidget):
	def __init__(self, parent=None):
		super(WatermarkUI, self).__init__(parent)
		self.watermark    = QLineEdit("SAMPLE")
		self.font_name    = FontEdit( "Helvetica-Bold")
		self.color        = ColorEdit("#DD8888")
		self.font_size    = NumberSpinBox(    1,  200,   25,   1, 0) 
		self.fill_opacity = NumberSpinBox(    0,    1, 0.35, 0.1, 2) 
		self.rotate       = NumberSpinBox( -360,  360,   30,   1, 0) 
		self.row          = NumberSpinBox(    1,  100,    4,   1, 0) 
		self.column       = NumberSpinBox(    1,  100,    5,   1, 0) 
		self.grid         = QGridLayout()

		self.grid.addWidget(QLabel("Text")          , 0, 0, 1, 1)
		self.grid.addWidget(QLabel("Color")         , 1, 0, 1, 1)
		self.grid.addWidget(QLabel("Font")          , 2, 0, 1, 1)
		self.grid.addWidget(QLabel("Size")          , 3, 0, 1, 1)
		self.grid.addWidget(QLabel("Opacity")       , 4, 0, 1, 1)
		self.grid.addWidget(QLabel("Rotation")      , 5, 0, 1, 1)
		self.grid.addWidget(QLabel("Row counts")    , 6, 0, 1, 1)
		self.grid.addWidget(QLabel("Column counts") , 7, 0, 1, 1)

		self.grid.addWidget(self.watermark          , 0, 1, 1, 1)
		self.grid.addWidget(self.color              , 1, 1, 1, 1)
		self.grid.addWidget(self.font_name          , 2, 1, 1, 1)
		self.grid.addWidget(self.font_size          , 3, 1, 1, 1)
		self.grid.addWidget(self.fill_opacity       , 4, 1, 1, 1)
		self.grid.addWidget(self.rotate             , 5, 1, 1, 1)
		self.grid.addWidget(self.row                , 6, 1, 1, 1)
		self.grid.addWidget(self.column             , 7, 1, 1, 1)
		self.grid.setRowStretch(8, 1)
		self.grid.setColumnMinimumWidth(1, 225)
		self.setLayout(self.grid)

		
		for ctrl in [self.watermark, self.font_name, self.font_size, self.color, self.fill_opacity, self.rotate , self.row, self.column, ]:
			ctrl.setMinimumHeight(25)
			try:
				ctrl.setAlignment(Qt.AlignCenter)
			except:
				pass

	def value(self):

		return {
				"watermark"     : self.watermark.text(), 
				"font_name"     : self.font_name.getFont(), 
				"font_size"     : self.font_size.value(), 
				"fill_color"    : self.color.getColor(),        
				"fill_opacity"  : self.fill_opacity.value(), 
				"rotate"        : self.rotate.value(), 
				"row"           : self.row.value(), 
				"column"        : self.column.value(), 
		}


	def setValue(self, value_pack):
		self.watermark    .setText(value_pack.get("watermark"   , "SAMELE"))
		self.font_name    .setFont(value_pack.get("font_name"   , "Helvetica-Bold"))
		self.color       .setColor(value_pack.get("fill_color"  , "#DD8888"))
		self.font_size   .setValue(value_pack.get("font_size"   ,  None))
		self.fill_opacity.setValue(value_pack.get("fill_opacity",  None))
		self.rotate      .setValue(value_pack.get("rotate"      ,  None))
		self.row         .setValue(value_pack.get("row"         ,  None))
		self.column      .setValue(value_pack.get("column"      ,  None))

	def saveValue(self):
		parent_path  = Path(os.path.realpath(__file__)).parent.absolute()
		setting_path = os.path.abspath(os.path.join(parent_path, "setting.pickle" ))
		
		with open(setting_path, 'wb') as handle:
			pickle.dump(self.value(), handle)

	def loadValue(self):
		value_pack   = {}
		parent_path  = Path(os.path.realpath(__file__)).parent.absolute()
		setting_path = os.path.abspath(os.path.join(parent_path, "setting.pickle" ))
		try:
			with open(setting_path, 'rb') as handle:
				value_pack = pickle.load(handle)
		except:
			pass

		self.setValue(value_pack)
		

if __name__ == '__main__':
	import sys
	app    = QApplication(sys.argv)
	window = WatermarkUI()
	window.show()
	sys.exit(app.exec_())