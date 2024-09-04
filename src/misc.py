from   PyQt5.QtWidgets          import QFrame
from   PyQt5.QtCore             import QSize, QByteArray
from   PyQt5.QtGui              import QIcon, QPixmap

class Debugger(object):
	def __init__(self):
		self.debug = False

	def print(self, *args, **argv):
		if self.debug:
			print(*args, **argv)

class QLine(QFrame):
	def __init__(self):
		super(QLine, self).__init__()
		self.setFrameShape(QFrame.VLine)
		self.setFrameShadow(QFrame.Plain)
		theme = """
			QFrame {
				color: rgba(150, 150, 150, 200);
			}
		"""
		self.setStyleSheet(theme)

class QVLine(QLine):
	def __init__(self):
		super(QVLine, self).__init__()
		self.setFrameShape(QFrame.VLine)

class QHLine(QLine):
	def __init__(self):
		super(QHLine, self).__init__()
		self.setFrameShape(QFrame.HLine)	

class PorotechIcon(object):
	def __init__(self):
		super().__init__()
		self.icon = self.iconFromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABsAAAAbCAYAAACN1PRVAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA69JREFUSIm1lttPXFUUxn9rnzMzzHCGywwEKNMEG5DpcGs0EsHEWh9Ka7y96Etj4oO26QvR9EG03q2miZWkqUlN9E/QGG+kIVZEglQzWqBAUy8hKFQHGG0bQgszzPIBZsQRa4Dhe9vfWfv8ztrZ59tbVJX1Klz92ZuqPA5MI/p1ypf3KaGqMz92VS/cbJ5ZNwlQEKAEiKDyhJQ7TxnP1cnww98fq390zMkpLEsJ8dlhoERFjyYS18fChy/duzWwAs+3iJSnh+L3/EF5/pnwK5PtOYG58uafw9aQwv0Uej9AmALAMnHdUVSB4kI5mQ2UjWyQbO3Z86U9VVzwtAkHH8Jt3bXqUVIrvPsuHQqezRksrZ0vTrWopZ+gBMVtx7Q6MIFttieW7J0/P8LVXGyQjC6+WjkgmAcJ+vq1NujCNs1AhdtOdkCOO0sr/GHyGZTjq6z4wjU7lNPO0nJm7E7gdwCRuZjb+81oUej9ti3pDKC+q7/Ddo8eEJOoYzkE3tuSzgBcnsHvxCTqV0AArVsGU7HGsqwyu6eq4XVVsdJOYan7hduj0cRmYXZh158mob3psWUkaaMclOVQBSB+JdEJTG8WZlLjQdttdq+yLhtFfvvHFy2mdm0WBGBbVlOW9asR0T4AY5j3FnKuoJKWXMBqJNXsFR0A5lesAemra9znBPRlcdEA+EBnC1Nz26t6xm9sFPTshcZiUZkA/EswF1MGL6vpMMnSwOfiIrQMApCSa8Z5fpONnQD8ABY42wSne9f5fnNPT09SkdPpKrF0omiHtEwcbGjdCKV7pKE1YqSG1ZtMpRNWsvGn+2o88wve8y6HmfxyrRWhDIgb5IHKd4YH1gPCmI+B4KISiy4xnoDkG43DdyuqmbgaP1DfbPulH7DTk/P89OeXS7dvzn2Cl6Lz/8GA4ab8xTw5ci7J3hto5jxTSExbqdbHai9EM52l9cuhhnYRTgIYm+miKrVAgkDc8vOWFBBdEteozzFXrjuJgNFUUypg1VpePQoEFpX4QJKkLq8MIO17I4On0u//VxBPHq5/UlXeLr6FEbG4LVNYJqNiUQcgAXrJYzeAeOiVoGR+3lnVoZEliYAcWQ2CNe4godMj7/pKdb9YlGZMS2JiEVlrBXWRO0AzwVAiEgzZ7M8GrQkDCL428sW8TyOqcgyYweEH/k7vLBo+TcqQwizocbcuRCK3Dp1dq/T/z7NTNZ6FAl9byk61IXInyjYJ6kW8UocSU/jKOPqRp2Suj6qbB8FfcZpVXdo/DbkAAAAASUVORK5CYII=")

	def iconFromBase64(self, base64):
		pixmap = QPixmap()
		pixmap.loadFromData(QByteArray.fromBase64(base64))
		icon = QIcon(pixmap)
		return icon
		