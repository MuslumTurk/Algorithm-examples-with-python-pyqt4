#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
from copy import deepcopy
from PyQt4 import QtCore, QtGui
from heapq import heappush, heappop 
import math
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class node:
    xPos = 0 
    yPos = 0 
    gn = 0 
    fn = 0 
    
    #f(n) = g(n) + h(n)

    def __init__(self, xPos, yPos, gn, fn):
        self.xPos = xPos
        self.yPos = yPos
        self.gn = gn
        self.fn = fn
    
    def __lt__(self, diger): #Oncelik sirasini belirleme
        return self.fn < diger.fn
    
    def fnGuncelle(self, xDest, yDest): 
        self.fn = self.gn + self.hn(xDest, yDest) * 10  #A*

    def hareket(self, kalip, yon): 
        if kalip == 8 and yon % 2 != 0:
            self.gn += 14 # Capraz hareket
        else:
            self.gn += 10 # Dikey hareket
    
    def hn(self, xDest, yDest): # A noktasi ile B noktasi arasi kus ucumu uzaklik
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = math.sqrt(xd * xd + yd * yd)
        return(d)


class Ekran(QtGui.QWidget):

	def __init__(self, parent=None):

		super(Ekran, self).__init__(parent)


		self.kalip = 8 
		if self.kalip == 8: # Köşeler için
			self.dx = [1, 1, 0, -1, -1, -1, 0, 1]
			self.dy = [0, 1, 1, 1, 0, -1, -1, -1]

		self.genislik = 30 # Yatay Genislik
		self.boy = 30 # Dikey Uzunluk

		self.harita = []
		self.satir = [0] * self.genislik

		for i in range(self.boy): 
			self.harita.append(list(self.satir))

		self.xA = 2
		self.yA = 15

		self.xB = 28
		self.yB = 15



		self.table = QtGui.QTableWidget(self)
		self.nbrow, self.nbcol = self.genislik, self.boy
		self.table.setRowCount(self.nbrow)
		self.table.setColumnCount(self.nbcol)
		self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		#self.table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
		self.table.itemEntered.connect(self.ciz)

		self.buttonhesapla = QtGui.QPushButton('Hesapla')
		self.connect(self.buttonhesapla, SIGNAL('pressed()'), self.hesapla)

		self.table.horizontalHeader().hide()
		self.table.verticalHeader().hide()

		for row in xrange(0, self.nbrow):
			self.table.setRowHeight(row, 25)
		for col in xrange(0, self.nbcol):
			self.table.setColumnWidth(col, 25)


		for row in xrange(0, self.nbrow):
			for col in xrange(0, self.nbcol):
				item = QtGui.QTableWidgetItem()
				item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
				item.setFlags( item.flags() ^ QtCore.Qt.ItemIsEditable)
				self.table.setItem(row, col, item)



		font = QtGui.QFont()
		font.setFamily(u"DejaVu Sans")
		font.setPointSize(16)
		self.table.setFont(font)


		self.resize(27*30, 27*30)

		pos = QtGui.QGridLayout()
		pos.addWidget(self.table, 0, 0)
		pos.addWidget(self.buttonhesapla, 28, 0)
		self.setLayout(pos)

		self.g = deepcopy(self.harita)
		self.afis(self.g)

		self.table.setFocus()
		self.table.setCurrentCell(0, 0)

	def afis(self, g):

		for row in xrange(0, len(g[0])):
			for col in xrange(0, len(g)):
				if g[row][col]==0:
					self.table.item(row, col).setText(u"")
					self.table.item(row, col).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
				else:
					self.table.item(row, col).setText(unicode(g[row][col]))
					self.table.item(row, col).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

		couleur = QtGui.QColor(160, 255, 160, 255) 
		self.table.item(self.yA, self.xA).setBackgroundColor(couleur)

		couleur = QtGui.QColor(255, 160, 160, 255)
		self.table.item(self.yB, self.xB).setBackgroundColor(couleur)

	def hesapla(self):
		rota = self.yolbul(self.harita, self.genislik, self.boy, self.kalip, self.dx, self.dy, self.xA, self.yA, self.xB, self.yB)
		print 'Rota:'
		rota = rota.replace('.','')
		print rota
		print ">>>>>",len(rota)
		if len(rota) > 0:
		    x = self.xA
		    y = self.yA
		    self.harita[y][x] = 2
		    for i in range(len(rota)):
		        j = int(rota[i])
		        x += self.dx[j]
		        y += self.dy[j]
		        print ">>",x,y,self.dx[j],self.dy[j]
		        self.harita[y][x] = 3
		    self.harita[y][x] = 4


		for y in range(self.boy):
		    for x in range(self.genislik):
		        xy = self.harita[y][x]
		        if xy == 3:
		            self.table.item(y, x).setBackgroundColor(QtGui.QColor(10, 10, 10))

		    


	def ciz(self, item):
		print 'cor : ', item.column(),",",item.row()
		if item.row() == self.yA and item.column() == self.xA:
			couleur = QtGui.QColor(160, 255, 160, 255)
		elif item.row() == self.yB and item.column() == self.xB:
			couleur = QtGui.QColor(255, 160, 160, 255)
		else:
			couleur = QtGui.QColor(169,169,169,169) 
			self.harita[item.row()][item.column()] = 1	 

		self.table.item(item.row(), item.column()).setBackgroundColor(couleur)

		s = [[str(e) for e in row] for row in self.harita]
		lens = [max(map(len, col)) for col in zip(*s)]
		fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
		table = [fmt.format(*row) for row in s]
		print '\n'.join(table)

 
	def yolbul(self,harita, genislik, boy, kalip, dx, dy, xA, yA, xB, yB):




		kapali_node = [] 
		acik_node = [] 
		kalip_harita = []
		satir = [0] * genislik

		for i in range(boy): # Matris
			kapali_node.append(list(satir))
			acik_node.append(list(satir))
			kalip_harita.append(list(satir))



		kuyruk = [[], []] 
		kuyruk_id = 0 
		n0 = node(xA, yA, 0, 0) #Baslangic node u olusturuluyor.
		n0.fnGuncelle(xB, yB) # Baslangic ile hedef arasi kus ucumu (tahmini) uzaklik,f(n) = g(n)+h(n)

		heappush(kuyruk[kuyruk_id], n0) #ilk node kuyruga ekleniyor.
		acik_node[yA][xA] = n0.fn 

		# A* search
		while len(kuyruk[kuyruk_id]) > 0:

			n1 = kuyruk[kuyruk_id][0] #ilk node
			x = n1.xPos
			y = n1.yPos
			#print ">>>x,y",x,y
			heappop(kuyruk[kuyruk_id]) #Acik listeden siliyoruz,cunku bu node a ugramis sayildik. kuyrktan cikti(ilk giren).
			acik_node[y][x] = 0
			kapali_node[y][x] = 1 

			if x == xB and y == yB: # B noktasi bulundu mu?
				yol = ''
				while not (x == xA and y == yA):
					print "test 0",x,y,kalip_harita[y][x]
					j = kalip_harita[y][x]
					print "test 1 :",j
					c = str(int((j + kalip / 2) % kalip))
					print "test 2 :",c
					yol = c + yol
					print "test 3 :",yol
					x += dx[j]
					y += dy[j]
				return yol

			#Node un tum alt nodelarini inceliyoruz.
			for i in range(kalip): # 8 defa döngü,sol,solcapraz,ust,sagcapraz,sag,altsagcapraz,alt,altsolcapraz
				xdx = x + dx[i]
				ydy = y + dy[i]

				if not (xdx < 0 or xdx > genislik-1 or ydy < 0 or ydy > boy - 1 #Cercevenin disina tasti mi?
				or harita[ydy][xdx] == 1 or kapali_node[ydy][xdx] == 1): #Duvar var mi? yada onceden ugranildi mi?

					#Node olusturuluyor.
					m0 = node(xdx, ydy, n1.gn, n1.fn)
					m0.hareket(kalip, i)
					m0.fnGuncelle(xB, yB)

					#Acik listede degilse ekleyelim.
					if acik_node[ydy][xdx] == 0:
						acik_node[ydy][xdx] = m0.fn
						heappush(kuyruk[kuyruk_id], m0)
						# Yonu isaretleniyor
						
						kalip_harita[ydy][xdx] = int((i + kalip / 2) % kalip)

					# Yol degistirilmeli
					elif acik_node[ydy][xdx] > m0.fn:
						#Guncelleniyor.
						acik_node[ydy][xdx] = m0.fn
						#Yonu Guncelleniyor
			
						kalip_harita[ydy][xdx] = int((i + kalip / 2) % kalip)
						while not (kuyruk[kuyruk_id][0].xPos == xdx and kuyruk[kuyruk_id][0].yPos == ydy):
							heappush(kuyruk[1 - kuyruk_id], kuyruk[kuyruk_id][0])
							heappop(kuyruk[kuyruk_id])

						heappop(kuyruk[kuyruk_id]) # hedef silindi
						# empty the larger size priority queue to the smaller one
						if len(kuyruk[kuyruk_id]) > len(kuyruk[1 - kuyruk_id]):
							kuyruk_id = 1 - kuyruk_id

						while len(kuyruk[kuyruk_id]) > 0:
							heappush(kuyruk[1-kuyruk_id], kuyruk[kuyruk_id][0])
							heappop(kuyruk[kuyruk_id])

						kuyruk_id = 1 - kuyruk_id
						heappush(kuyruk[kuyruk_id], m0)
		return '' # Bulunamadi.




if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	ekran = Ekran()
	ekran.show()
	sys.exit(app.exec_())