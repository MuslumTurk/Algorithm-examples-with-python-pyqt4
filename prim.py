from PyQt4 import QtGui, QtCore
import pprint,math,sys
from collections import defaultdict
from heapq import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import subprocess
import time

class Window(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.showDialog()
        self.dialog = QDialog()
        self.algoritms = 0
        self.algoritms_name = "Prim Algorithms"
        self.view = View(self,int(self.deneme))
        self.resultButton = QtGui.QPushButton('Result', self)
        self.resultButton.setMaximumHeight(40)
        self.resultButton.setStyleSheet("background-color: green; color: white;")
        self.restartButton = QtGui.QPushButton('Restart', self)
        self.restartButton.setMaximumHeight(40)
        self.restartButton.setStyleSheet("background-color: blue; color: white;")
        self.exitButton = QtGui.QPushButton('Exit', self)
        self.exitButton.setMaximumHeight(34)
        self.exitButton.setStyleSheet("background-color: red; color: white;")
        self.cb = QComboBox(self)
        self.cb.addItem("Prim Algorithms")
        self.cb.addItem("Dijkstra Algorithms")
        self.cb.currentIndexChanged.connect(self.selectionchange)
        self.layout = QtGui.QHBoxLayout(self)
        self.resultButton.clicked.connect(self.result)
        self.restartButton.clicked.connect(self.restart)
        self.exitButton.clicked.connect(self.exit)
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.resultButton)
        self.splitter1.addWidget(self.restartButton)
        self.splitter1.addWidget(self.exitButton)
        self.splitter1.addWidget(self.cb)
        self.splitter2.addWidget(self.view)
        self.splitter2.addWidget(self.splitter1)
        self.layout.addWidget(self.splitter2)

    def showDialog(self):
        number, ok = QtGui.QInputDialog.getInteger(self, 'Algorithms', 'How many nodes would you like to add?',45, 2, 50, 1)
        if ok:
            self.deneme = number

    def selectionchange(self,i):
        self.algoritms = i
        self.algoritms_name = self.cb.currentText()

    def exit(self):
        self.close() 

    def result(self):

        if self.algoritms == 0:
            print 'Calculated According To -- >> ' , self.algoritms_name
            nodes = self.view.nodes
            edges = self.view.edges
            prim = self.prim(nodes,edges)
            self.view.ciz(prim,nodes)

        if self.algoritms == 1:
            print 'Calculated According To -- >> ' , self.algoritms_name
            nodes = self.view.nodes
            edges = self.view.edges
            dijkstra = self.dijkstra(nodes,edges)
            self.view.ciz(dijkstra,nodes)


    def dijkstra(self,nodes,edges):
        if len(nodes) < 2 or len(edges) < 1:
            button = QPushButton("Restart",self.dialog)
            button.move(60,110)
            self.dialog.setWindowTitle("Node Not Selected")
            button.clicked.connect(self.restart)
            self.dialog.setWindowModality(Qt.ApplicationModal)
            self.dialog.exec_()

        if len(nodes) < 2 or len(edges) < 1:
            self.close()        
        
        conn = defaultdict( list )
        for n1,n2,c in edges:
            conn[ n1 ].append( (c, n1, n2) )
            conn[ n2 ].append( (c, n2, n1) )
            print c , n1 , n2

        mst = []
        used = set( nodes[ 0 ] )
        usable_edges = conn[ nodes[0] ][:]
        heapify( usable_edges )

        while usable_edges:
            cost, n1, n2 = heappop( usable_edges )
            if n2 not in used:
                used.add( n2 )
                mst.append( ( n1, n2, cost ) )
                for e in conn[ n2 ]:
                    if e[ 2 ] not in used:
                        heappush( usable_edges, e )
        return mst


    def prim(self,nodes,edges):
        if len(nodes) < 2 or len(edges) < 1:
            button = QPushButton("Restart",self.dialog)
            button.move(60,110)
            self.dialog.setWindowTitle("Node Not Selected")
            button.clicked.connect(self.restart)
            self.dialog.setWindowModality(Qt.ApplicationModal)
            self.dialog.exec_()

        if len(nodes) < 2 or len(edges) < 1:
            self.close()        
        
        conn = defaultdict( list )
        for n1,n2,c in edges:
            conn[ n1 ].append( (c, n1, n2) )
            conn[ n2 ].append( (c, n2, n1) )

        mst = []
        used = set( nodes[ 0 ] )
        usable_edges = conn[ nodes[0] ][:]
        heapify( usable_edges )

        while usable_edges:
            cost, n1, n2 = heappop( usable_edges )
            if n2 not in used:
                used.add( n2 )
                mst.append( ( n1, n2, cost ) )
                for e in conn[ n2 ]:
                    if e[ 2 ] not in used:
                        heappush( usable_edges, e )
        return mst

    def restart(self):
        self.dialog.accept()
        self.close()
        subprocess.call("python" + " prim.py", shell=True)

class View(QtGui.QGraphicsView):
   
    edges = []
    tane = 2
    nodes = []

    def __init__(self, parent,tane):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setScene(QtGui.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        
        self.tane = tane
        son_satir = 0
        ilk_sutun = 0
        baslangic = -230

        if self.tane > 9:
            sutun = 9
            satir = self.tane / 9
            if self.tane % 9 != 0:
                satir = satir + 1
                son_satir = self.tane % 9
        else:
            satir = 2
            if self.tane % 2 == 0:
                sutun = self.tane/2
            else:
                ilk_sutun = (self.tane/2)+1
                son_satir = (self.tane/2)
        
        for i in range(satir):
            if i == satir-1 and son_satir != 0:
                sutun = son_satir
                baslangic = (150 - (75*sutun)) / 2
            elif i == 0 and ilk_sutun != 0:
                sutun = ilk_sutun
                baslangic = (150 - (75*sutun)) / 2

            for j in range(sutun):
                item = callbackEllipse(QtCore.QRectF(baslangic+ (j*75), -170 + ( i*85), 30, 30))
                self.nodes = item.nodes
                self.edges = item.edges
                self.scene().addItem(item)

    def ciz(self,prim,nodes):

        self.scene().clear()
        for node in nodes:

            sira = ord(node)-65
            if sira > 9:
                satir = sira/9
                sutun = sira%9
            else:
                satir = 0
                sutun = sira

            item = callbackEllipse(QtCore.QRectF(-230+ (sutun*75), -170 + ( satir*85), 30, 30))
            yazi = self.scene().addSimpleText('%c' % ord(node))
            yazi.setBrush(QtCore.Qt.red)
            yazi.setPos(-220+ (sutun*75),-163 + ( satir*85))
            self.scene().addItem(item)
          
            for i in prim:
                sira = ord(i[0])-65
                if sira > 9:
                    satir = sira/9
                    sutun = sira%9
                else:
                    satir = 0
                    sutun = sira

                sira2 = ord(i[1])-65
                if sira2 > 9:
                    satir2 = sira2/9
                    sutun2 = sira2%9
                else:
                    satir2 = 0
                    sutun2 = sira2

                self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(-215+ (sutun*75), -160 + ( satir*85),-215+ (sutun2*75), -160 + ( satir2*85))))
class callbackEllipse(QtGui.QGraphicsEllipseItem):
    
    liste = []
    cor = []
    edges = []
    x = 0
    y = 0
    index = 65
    nodes = []

    def __init__(self, parent):
        QtGui.QGraphicsEllipseItem.__init__(self, parent)
        self.index= callbackEllipse.index
        callbackEllipse.index += 1

    def mousePressEvent(self, event):

        self.x = QtGui.QGraphicsEllipseItem.rect(self).x()
        self.y = QtGui.QGraphicsEllipseItem.rect(self).y()
        self.liste.append(self.x)
        self.liste.append(self.y)
        self.cor.append(self.index)
        self.nodes.append("%c" % self.index)

        if len(self.liste) > 2:
            self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(self.liste[0]+10,self.liste[1]+10,self.x+10,self.y+10)))  

            tup = ()
            node = '%c' % (self.cor[0])
            node2 = '%c' % (self.cor[1])
            tup = tup + (node,node2,int(self.mesafe_hesapla(self.liste)),)
            
            self.edges.append(tup)
            tup = ()
            self.cor[:] = []

            orta_kenar_yazi = self.scene().addSimpleText('(%d)' % (self.uzaklikHesapla(self.liste)))      #secili iki kenar arasinda yazi
            orta_kenar_yazi.setBrush(QtCore.Qt.black)
            orta_kenar_yazi.setPen(QPen(QColor('red')))                                                   #yazinin renigini ve kalinligini degistirdim
            orta_kenar_yazi.setPos((self.liste[2]+self.liste[0])/2,(self.liste[3]+self.liste[1])/2)
            self.liste[:] = []

        yazi = self.scene().addSimpleText('-%c-' % (self.index))
        yazi.setBrush(QtCore.Qt.green)
        yazi.setPen(QPen(QColor('green'))) 
        yazi.setPos(self.x+5,self.y+5)    #yazinin elipse uzerindeki konumu
        color = QtGui.QColor(0, 0, 0)
        brush = QtGui.QBrush(color)
        QtGui.QGraphicsEllipseItem.setBrush(self, brush)
        return QtGui.QGraphicsEllipseItem.mouseReleaseEvent(self, event)



    def mesafe_hesapla(self, liste):
        return math.sqrt( math.fabs(self.liste[2]-self.liste[0]) + math.fabs(self.liste[3]-self.liste[1]))

    def uzaklikHesapla(self,liste):
        self.liste = liste
        self.mesafe = 0
        self.dialog = QDialog()
        button = QPushButton("Okey",self.dialog)
        button.move(60,110)
        self.number = QLineEdit(self.dialog)
        self.number.setValidator(QtGui.QIntValidator(0, 999999))
        self.number.move(40,40)
        text = QLabel("Input a Cost",self.dialog)
        text.move(60,20)
        self.otomatik = QCheckBox("Automatic Cost",self.dialog)
        self.otomatik.move(40,70)
        self.dialog.setWindowTitle("Cost Calculate")
        button.clicked.connect(self.hesapla)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

        return int(self.mesafe)

    def hesapla(self):
        if self.otomatik.isChecked() == True:
            self.mesafe = math.sqrt( math.fabs(self.liste[2]-self.liste[0]) + math.fabs(self.liste[3]-self.liste[1]))
        else:
            self.mesafe = self.number.text()
        self.dialog.accept()

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(1000, 800)
    window.showMaximized()
    sys.exit(app.exec_())