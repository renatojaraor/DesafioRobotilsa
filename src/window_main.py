
from datetime import datetime
import random
from typing import List
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, traceback
from src.personaje import Personaje
from src.funciones import generar_personaje_aleatorio, encontrar_personaje
from threading import *
from src.window_caracteristicas import Ui_SecondWindow


class VentanaPrincipal(QtWidgets.QMainWindow):
    
    lista_personajes: List[Personaje] = []
    
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        uic.loadUi('main.ui', self)
        
        self.threadpool = QThreadPool()
        self.lcd = self.findChild(QLCDNumber, 'lcdNumber')
        self.button_request.clicked.connect(self.funcion_hilo)
        self.button_request.setIcon(QIcon('search.png'))
        self.label_fecha.setText(datetime.now().strftime("%d-%m-%Y"))
        
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)
        
        self.listWidget.installEventFilter(self)
        
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listWidget:
            menu = QMenu()
            menu.addAction('Informacion del personaje')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.openWindow(item.text())
                
            return True
        return super().eventFilter(source, event)
         
    def displayTime(self):
        currentTime = QTime.currentTime()
        displayText = currentTime.toString('hh:mm:ss')
        self.lcd.setDigitCount(12)
        self.lcd.display(displayText)
        
    def funcion_hilo(self):
        worker = Worker(self.request_action)
        worker.signals.progress.connect(self.print_output)
        self.threadpool.start(worker)
            
    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")    
        
        
    def request_action(self, progress_callback):
        self.lista_personajes = []
        numeros = []
        self.listWidget.clear()
        c=0
        while c<10: 
            numero = random.randint(1,17)  
            if not (numero in numeros):
                numeros.append(numero)
                personaje = generar_personaje_aleatorio(numero)
                if not personaje:
                    continue
                self.lista_personajes.append(personaje)
                self.listWidget.addItem(personaje.name)
                c+=1
    
        
    def openWindow(self, personaje_seleccionado: str):
        personaje = encontrar_personaje(personaje_buscado=personaje_seleccionado, personajes=self.lista_personajes)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow(personaje)
        self.ui.setupUi(self.window)
        self.window.show()




class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(Personaje)   
    
    

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit() 



app = QtWidgets.QApplication(sys.argv)
window = VentanaPrincipal()
window.show()
app.exec_()