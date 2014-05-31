from tkinter import Tk, Canvas, Frame, Checkbutton,Label
from tkinter import LEFT,RIGHT,TOP,BOTTOM
from tkinter import BooleanVar,StringVar

from prgLibrary import prg

import shelve



class Storage(object):
    '''
    класс для хранения настроек и шаблонов
    '''
    def __init__(self):
        self.db = shelve.open("PRGViewer")
    
class Field(Canvas):
    '''
    класс для хранения и управления отображением компонентов
    '''
    def __init__(self,parent=None):
        Canvas.__init__(self,parent,bg="light grey")
    
class Figure(object):
    """
    хранит в себе выделенную часть фигур,
    вспомогательный класс, должен рисовать только на внешнем Canvas
    """
    def __init__(self,canvas):
        self.canvas = canvas
    

class Controls(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.createWidgets()
        self.bindKeys()
        
    def createWidgets(self):
        self.ch1 = BooleanVar()
        Checkbutton(self, text="Hide/Show Descriptions", variable=self.ch1, onvalue=True, offvalue=False).pack(side=TOP)
        
        self.outval1 = StringVar()
        self.outval1.set("test")
        Label(self, textvariable = self.outval1).pack(side=TOP)
        
        self.outval2 = StringVar()
        self.outval2.set("test2")
        Label(self, textvariable = self.outval1).pack(side=BOTTOM)
        
        
        
class App():
    '''
    основной класс программы
    '''
    def __init__(self):
        self.createWidgets()
        self.configure()
        
    def createWidgets(self):
        '''
        создает и настраивает виджеты
        '''
        #основное окно
        self.window = Tk()
        self.window.title("PRG Viewer by Novicov")
        #вывод программы
        self.canv = Field(self.window)
        self.canv.pack(side=LEFT,fill="both",expand="y")
        #управляющие элементы
        self.cont = Controls(self.window)
        self.cont.pack(side=RIGHT,fill="y",expand="y")
    
    def configure(self):
        self.storage = Storage()
        #добавить в обработку выбор файла prg
        
    def start(self):
        self.window.mainloop()
    
if __name__=="__main__":
    App().start()