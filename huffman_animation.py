import heapq
from collections import defaultdict
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,subprocess,math


class Window(QtGui.QWidget):

	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.initUI()
	def initUI(self):
		self.showDialog()
		self.dialog = QDialog()
		self.list = QtGui.QListWidget(self)
		self.list.resize(300,120)
		self.view = View(self, self.text,self.list)
		self.view.setMinimumWidth(850)
		self.restartButton = QtGui.QPushButton('Restart', self)
		self.restartButton.setMaximumHeight(50)
		self.restartButton.setMinimumHeight(50)
		self.restartButton.setMinimumWidth(150)
		self.restartButton.setMaximumWidth(150)
		self.restartButton.clicked.connect(self.restart)
		self.restartButton.setStyleSheet("background-color: blue; color: white;")
		self.exitButton = QtGui.QPushButton('Exit', self)
		self.exitButton.setMaximumHeight(50)
		self.exitButton.setMinimumHeight(50)
		self.exitButton.clicked.connect(self.exit)
		self.exitButton.setStyleSheet("background-color: red; color: white;")
		
		self.layout = QtGui.QHBoxLayout(self)
		self.splitter1 = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
		self.splitter1.addWidget(self.restartButton)
		self.splitter1.addWidget(self.exitButton)
		self.splitter2.addWidget(self.view)
		self.splitter2.addWidget(self.splitter1)
		self.splitter1.addWidget(self.list)
		self.layout.addWidget(self.splitter2)
		if(len(self.text) < 1):
			self.showDialog()

	def showDialog(self):
		message, ok = QtGui.QInputDialog.getText(self, 'Algorithms', 'How many nodes would you like to add?')
		if ok:
			self.text = message

	def exit(self):
		self.close() 

	def restart(self):
		self.dialog.accept()
		self.close()
		subprocess.call("python" + " huffman.py", shell=True)

class View(QtGui.QGraphicsView):
   
	edges = []
	tane = 2
	nodes = []

	def __init__(self, parent, text,liste):
		QtGui.QGraphicsView.__init__(self, parent)
		self.setScene(QtGui.QGraphicsScene(self))
		self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
		self.text = text
		self.list = liste
		self.huffman()
		


	def huffman(self):
		data = str(self.text)
		frequency = defaultdict(int)
		for symbol in data:
			frequency[symbol] += 1

		huff = self.encode(frequency)
		nodes = []
		for p in huff:
			node =  p[0]
			frequencies = str(frequency[p[0]])
			weight = p[1]
			nodes.append([node,frequencies,weight])

		item = callbackEllipse(QtCore.QRectF(5, -252, 30, 30))
		ilk = self.scene().addSimpleText("MT")
		ilk.setPos(9,-245)
		#item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.scene().addItem(item)
		yazi = self.scene().addSimpleText('GIRILEN METIN :%s' %data)
		yazi.setBrush(QtCore.Qt.red)
		yazi.setPos(-90,-310)
		
		for node,frequencies,weight in nodes:
			koordinat = 250
			koorx = 0
			koory = 0
			baslangicx = 20
			baslangicy = -220

			self.list.addItem("%s     -   %s     -   %s" %(node,frequencies,weight))
			for edge in weight:
				if edge == '0':
					koorx += 0 - koordinat
					koordinat /=2
					koory += 50

					item = QtGui.QGraphicsLineItem(QtCore.QLineF(baslangicx,baslangicy,10+koorx,-210+koory))
					item.setPen(QtGui.QPen(QtCore.Qt.blue, 4))
					self.scene().addItem(item)
					baslangicx = 10+koorx
					baslangicy = -210+koory

					self.tl = QtCore.QTimeLine(5500)
					self.tl.setFrameRange(0, 5200)
					self.a = QtGui.QGraphicsItemAnimation(self)
					self.a.setItem(item)
					self.a.setTimeLine(self.tl)
					self.a.setRotationAt(1, -360)
					self.tl.start()

					item2 = callbackEllipse(QtCore.QRectF(koorx,-210+koory, 20, 20))
					item2.setBrush(QtGui.QBrush(QtCore.Qt.red))
					self.scene().addItem(item2)

					self.tl = QtCore.QTimeLine(4500)
					self.tl.setFrameRange(0, 4500)
					self.a = QtGui.QGraphicsItemAnimation(self)
					self.a.setItem(item2)
					self.a.setTimeLine(self.tl)
					self.a.setRotationAt(1, 360)
					self.tl.start()

				if edge == "1":
					koorx += koordinat
					koordinat /=2
					koory += 50

					item21 = QtGui.QGraphicsLineItem(QtCore.QLineF(baslangicx,baslangicy,10+koorx,-210+koory))
					item21.setPen(QtGui.QPen(QtCore.Qt.blue, 4))
					self.scene().addItem(item21)
					baslangicx = 10+koorx
					baslangicy = -210+koory

					self.tl = QtCore.QTimeLine(5000)
					self.tl.setFrameRange(0, 5000)
					self.a = QtGui.QGraphicsItemAnimation(self)
					self.a.setItem(item21)
					self.a.setTimeLine(self.tl)
					self.a.setRotationAt(1, 360)
					self.tl.start()

					item23 = callbackEllipse(QtCore.QRectF(koorx,-210+koory, 20, 20))
					item23.setBrush(QtGui.QBrush(QtCore.Qt.yellow))
					self.scene().addItem(item23)

					self.tl = QtCore.QTimeLine(4000)
					self.tl.setFrameRange(0, 5000)
					self.a = QtGui.QGraphicsItemAnimation(self)
					self.a.setItem(item23)
					self.a.setTimeLine(self.tl)
					self.a.setRotationAt(1, -360)
					self.tl.start()

			frec = self.scene().addSimpleText('%s' %frequencies)
			frec.setBrush(QtCore.Qt.red)
			frec.setPos(koorx-10,-195+koory)

			self.tl = QtCore.QTimeLine(4000)
			self.tl.setFrameRange(0, 5000)
			self.a = QtGui.QGraphicsItemAnimation(self)
			self.a.setItem(frec)
			self.a.setTimeLine(self.tl)
			self.a.setRotationAt(1, -360)
			self.tl.start()

			yazi = self.scene().addSimpleText('%s' %node)
			yazi.setBrush(QtCore.Qt.blue)
			yazi.setPos(koorx+5,-210+koory)

			self.tl = QtCore.QTimeLine(4000)
			self.tl.setFrameRange(0, 5000)
			self.a = QtGui.QGraphicsItemAnimation(self)
			self.a.setItem(yazi)
			self.a.setTimeLine(self.tl)
			self.a.setRotationAt(1, 360)
			self.tl.start()

	def encode(self, frequency):
		heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
		heapq.heapify(heap)
		while len(heap) > 1:
			lo = heapq.heappop(heap)
			hi = heapq.heappop(heap)
			for pair in lo[1:]:
				pair[1] = '0' + pair[1]
			for pair in hi[1:]:
				pair[1] = '1' + pair[1]
			heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
		return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

class callbackEllipse(QtGui.QGraphicsEllipseItem):
	x = 0
	y = 0
	index = 0

	def __init__(self, parent):
		QtGui.QGraphicsEllipseItem.__init__(self, parent)
		self.index= callbackEllipse.index
		callbackEllipse.index += 1
		if callbackEllipse.index == 91:
			callbackEllipse.index = 97 

	def mousePressEvent(self, event):

		self.x = QtGui.QGraphicsEllipseItem.rect(self).x()
		self.y = QtGui.QGraphicsEllipseItem.rect(self).y()

		brush = QtGui.QBrush(QtCore.Qt.yellow)
		QtGui.QGraphicsEllipseItem.setBrush(self, brush)
		return QtGui.QGraphicsEllipseItem.mouseReleaseEvent(self, event)


if __name__ == '__main__':
	
	app = QtGui.QApplication(sys.argv)
	window = Window()
	window.resize(1000, 800)
	window.showMaximized()
	sys.exit(app.exec_())