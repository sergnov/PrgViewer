#__encoding=utf-8
#Программа для просмотра файлов prg в заданном каталоге
#поддержка файлов формата prg v2
#Увеличение/уменьшение - крутить колесо мыши
#TODO - первый запуск на tkinter
#Todo - перенести интерфейс на kyivy

from os import path as path2program
from os import listdir
from os import _exit

from tkinter import Tk
from tkinter import Canvas
from tkinter import Event
from tkinter import StringVar
from tkinter import Menu, Button, Scale, Radiobutton, Frame
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import IntVar
from tkinter import VERTICAL

from random import randint

from prgLibrary import prg

class stringsApp(object):
    def __init__(self):
        self.currentfile="Current file"
        
class prgCanvas(object):
    def __init__(self,window):
        self.canvas = Canvas(window, bg="grey", height=500, width=500)

class App(object):
    def __init__(self):
        #настройка окружения
        self.pathtoapp = path2program.abspath(".")
        self.lst = [x for x in listdir(".")  if ".prg" in x] #получаем список файлов с расширением prg
        self.currentfileindex = 0 #устанавливаем индекс текущего файла
        #настройка графики
        self.window = Tk()
        self.window.title("PRG Viewer by Novicov: "+self.pathtoapp)
        self.window.minsize(width=510,height=510)
        self.window.maxsize(width=800,height=800)
        self.rightframe = Frame(self.window, bg="light grey",height=500, width=200)
        self.fields = None
        self.description = None
        self.canvas = prgCanvas(self.window)
        self.info = self.canvas.canvas.create_text(50,5,anchor="nw",text="Current file: "+self.lst[self.currentfileindex])
        self.infoText = StringVar()
        self.infoText.set("No wheel")
        
        self.showbutton = Button(self.rightframe,text="Hide descriptions",width=20)
        self.flagshow = True
        
        #настройка приложения
        self.mashtab = [1.00,1.00]
        self.reper = [0.00,0.00]
        self.fix = True
    
    def _wheel(self,event):
        if event.delta>0:
            self.currentfileindex-=1
            self.currentfileindex= len(self.lst)-1 if self.currentfileindex<0 else self.currentfileindex
        else:
            self.currentfileindex+=1
            self.currentfileindex= 0 if self.currentfileindex>len(self.lst)-1 else self.currentfileindex
        self.reper = [0.00,0.00]
        self.canvas.canvas.itemconfig(self.info,text="Current file: "+self.lst[self.currentfileindex])
    
    def paint(self):
        pass
    
    def setMashtab(self,sX,sY,mX,mY):
        '''Эта функция устанавливает текущий масштаб, так чтобы вся плата была в зоне видимости'''
        lX = int(self.canvas.canvas["width"])
        lY = int(self.canvas.canvas["height"])
        lengthX = abs(mX-sX)
        lengthY = abs(sY-mY)
        cX = lX/lengthX
        cY = lY/lengthY
        print("MSH",cX,cY)
        self.mashtab = [cX,cY]

    def findcoord(self,list):
        sX,sY,mX,mY = 0,0,0,0
        for c in list:
            if c[0]<sX: sX = c[0]
            elif c[0]>mX: mX = c[0]
            if c[1]<sY: sY = c[1]
            elif c[1]>mY: mY = c[1]
        return sX,sY,mX,mY    
        
    def _genfield(self,event):
        x,y,d=0,1,2
        if self.fields != None:
            for c in self.fields:
                self.canvas.canvas.delete(c)
        if self.description != None:
            for c in self.description:
                self.canvas.canvas.delete(c)
        self.fields = list()
        self.description = list()
        p = prg(self.lst[self.currentfileindex])
        p.download()
        p.extract()
        field =  [x[1:4] for x in p.progdigit if "25" in x[3]]
        sX,sY,mX,mY = self.findcoord(field)#ищем минимальные и максимальные координаты
        self.setMashtab(sX,sY,mX,mY)
        for c in field:
            c[x] = (c[x]+abs(0-sX))*self.mashtab[x]+self.reper[x]
            c[y] = (c[y]+abs(0-sY))*self.mashtab[y]+self.reper[y]
            print(c)
            self.fields.append(self.canvas.canvas.create_rectangle(c[x]-1,c[y]-1,c[x]+1,c[y]+1))
            if self.flagshow:
                self.description.append(self.canvas.canvas.create_text(c[x],c[y],anchor="nw",text=str(c[d][1]), font="Verdana 8"))

    def _move(self,event,x,y):
        
        self.reper[0]+=x
        self.reper[1]+=y
        
        if self.fields != None:
            for c in self.fields:
                self.canvas.canvas.move(c,x,y)
        if (self.description != None) and (self.flagshow):
            for c in self.description:
                self.canvas.canvas.move(c,x,y)
    
    def _hideshowdescriptions(self,event):
        if self.flagshow:
            txt = "Show descriptions"
        else:
            txt = "Hide descriptions"
        self.flagshow = not self.flagshow
        self.showbutton["text"] = txt
        self._genfield(event)
        
    def printlistofprg(self):
        # выводим список файлов prg
        self.lstdir = self.canvas.canvas.create_text(5,5,text="\n".join(self.lst),anchor="nw")
    
    def _changemashtab(self,event,dmX,dmY):
        self.mashtab[0]+=dmX
        self.mashtab[1]+=dmY
        self.fix = True
        self._genfield(event)
    
    def configure(self):
        self.window.bind("<MouseWheel>",lambda event:self._wheel(event))
        self.canvas.canvas.bind("<Button-1>",lambda event:self._genfield(event))
        self.window.bind("<Key-Right>",lambda event:self._move(event,10,0)) 
        self.window.bind("<Key-Left>",lambda event:self._move(event,-10,0))
        self.window.bind("<Key-Down>",lambda event:self._move(event,0,10))
        self.window.bind("<Key-Up>",lambda event:self._move(event,0,-10))
        self.window.bind("<Key-plus>",lambda event:self._changemashtab(event,5,5))
        self.window.bind("<Key-minus>",lambda event:self._changemashtab(event,-5,-5))
        self.showbutton.bind("<Button-1>",lambda event:self._hideshowdescriptions(event))
        
    def startloop(self):
        self.printlistofprg()
        self.canvas.canvas.pack(side="left")
        self.rightframe.pack(side="right",expand="y",fill="y")
        self.showbutton.pack(side="top")
        self._genfield(Event())
        self.window.mainloop()

if __name__ == "__main__":
    PRGviewerapp = App()
    PRGviewerapp.configure()
    PRGviewerapp.startloop()