#__encoding=utf-8
#Программа для просмотра файлов prg в заданном каталоге
#поддержка файлов формата prg v2, v1
#Увеличение/уменьшение - крутить колесо мыши
#TODO - первый запуск на tkinter

from os import path as path2program
from os import listdir
from os import _exit

from tkinter import Tk
from tkinter import Canvas
from tkinter import Event, StringVar, IntVar
from tkinter import Menu, Button, Scale, Radiobutton, Frame, Label
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import VERTICAL,LEFT

from random import randint

from prgLibrary import prg

class prgGroup(object):
    '''
    Этот класс хранит в себе информацию о группе и как ее обрабатывать
    '''
    def __init__(self):
        self.group = None #исходные данные
        self.primitives = None #группа примитивов
        self.descriptions = None #группа описаний
        #self.form = "rectangle"
    
class prgCanvas(object):
    def __init__(self,window,height,width):
        self.canvas = Canvas(window, bg="grey", height=height, width=width)
        self.canvas.pack(side="left")
        self.flagDescription = True
        self.mashtab = [1.00,1.00]
        self.reper = [0.00,0.00]
        self.sXY = [0.00,0.00]
        
        self.field = prgGroup() #данные, блоки групп, графические примитивы, точки, #графические примитивы, надписи
        self.fileprogram = None #имя файла для загрузки
        
        self.filter = None #фильтр, по которому определяется выделенный фрагмент
        
    def configure(self,file,filter= None):
        self.fileprogram = file
        if filter!=None:
            self.filter=filter
        else:
            self.filter = lambda x: x=="1999"#тестовый
    
    def setMashtab(self):
        '''Эта функция устанавливает текущий масштаб, так чтобы вся плата была в зоне видимости'''
        def findcoord(field):
            sX,sY,mX,mY = 0,0,0,0
            for c in field:
                if c[0]<sX: sX = c[0]
                elif c[0]>mX: mX = c[0]
                if c[1]<sY: sY = c[1]
                elif c[1]>mY: mY = c[1]
            return [sX,sY,mX,mY]
        sX,sY,mX,mY=findcoord(self.field.group)
        self.sXY=[abs(0-sX),abs(0-sY)]
        lX = int(self.canvas["width"])
        lY = int(self.canvas["height"])
        lengthX = abs(mX-sX)
        lengthY = abs(sY-mY)
        cX = lX/lengthX
        cY = lY/lengthY
        print("MSH",cX,cY)
        self.mashtab = [cX,cY]
        
    def genfield(self):
        x,y,d=0,1,2
        #нужно научиться обрабатывать группу
        if self.field.primitives != None:
            for c in self.field.primitives:
                self.canvas.delete(c)
        if self.field.descriptions != None:
            for c in self.field.descriptions:
                self.canvas.delete(c)
        self.field.primitives = list()
        self.field.descriptions = list()
        
        for c in self.field.group:
            cx = (c[x]+self.sXY[x])*self.mashtab[x]+self.reper[x]
            cy = (c[y]+self.sXY[y])*self.mashtab[y]+self.reper[y]
            # print(c[d][2])
            if self.filter!=None:
                _color1,_color2 = ["red","red"] if self.filter(c[d][2]) else ["black","black"]
            else:
                _color1,_color2 = "black","black"
            #
            self.field.primitives.append(self.canvas.create_rectangle(cx-1,cy-1,cx+1,cy+1,outline=_color1,fill=_color2))
            if self.flagDescription:
                self.field.descriptions.append(self.canvas.create_text(cx,cy,anchor="nw",text=str(c[d][1]), fill=_color1,font="Verdana 8"))

    def move(self,event,x,y):
        #в группы
        self.reper[0]+=x
        self.reper[1]+=y
        if self.field.primitives != None:
            for c in self.field.primitives:
                self.canvas.move(c,x,y)
        if (self.field.descriptions != None) and (self.flagDescription):
            for c in self.field.descriptions:
                self.canvas.move(c,x,y)
    
    def load(self):
        _p = prg(self.fileprogram)
        _p.download()
        _p.extract()
        #здесь можно разместить фильтрацию по группам, только фильтр(фильтры) нужно передавать через параметр
        self.field.group = [x[1:4] for x in _p.progdigit if "25" in x[3]]
        print(self.field)
        
    def paint(self):
        self.load()
        self.setMashtab()
        self.genfield()
    
class stringsApp(object):
    def __init__(self):
        self.currentfile="Current file"
        
class App(object):
    def __init__(self):
        #настройка окружения
        self.pathtoapp = path2program.abspath(".")
        self.lst = [x for x in listdir(".")  if ".prg" in x] #получаем список файлов с расширением prg
        if len(self.lst)==0:
            print("No prg file found in directory")
            input()
            _exit(0)
        self.currentfileindex = 0 #устанавливаем индекс текущего файла
        #настройка графики
        self.window = Tk()
        self.window.title("PRG Viewer by Novicov: "+self.pathtoapp)
        self.window.minsize(width=510,height=510)
        self.window.maxsize(width=800,height=800)
        self.rightframe = Frame(self.window, bg="light grey",height=500, width=200)
        self.inframe = Frame(self.rightframe, bg="yellow")
        self.lstButton = None
        ''''-------------------------------'''
        self.canvas = prgCanvas(self.window,500,500)
        self.canvas.configure(file=self.lst[self.currentfileindex])
        self.canvas.paint()
        
        
        self.showbutton = Button(self.rightframe,text="Hide descriptions",width=20)
        self.infoText = StringVar()
        self.infoText.set("Current file: "+self.lst[self.currentfileindex])
        self.info = Label(self.rightframe,text=self.infoText.get())
        self.listfiles = Label(self.rightframe,text="\n".join(self.lst))
        self.lmashtab = Label(self.rightframe, text=":".join([str(x) for x in self.canvas.mashtab]))
        self.helpText = Label(self.rightframe, text="Use mouse wheel to select file\n"+
            "Use left mouse button to load file\n"+
            "Use Up,Down,Right,Left buttons to move field\n"+
            "Use Show/Hide descriptions button\n"+
            "Use +/- buttons to change scale of field",anchor="n",justify=LEFT)
        
    def _wheel(self,event):
        """
        реакция на прокрутку колеса мыши
        меняем текущее имя файла
        обнуляем начальные координаты загрузки и перерисовываем текущее имя файла
        """
        self.currentfileindex+=1 if abs(event.delta)==event.delta else -1
        if self.currentfileindex<0:
            self.currentfileindex = len(self.lst)-1
        elif self.currentfileindex>len(self.lst)-1:
            self.currentfileindex = 0
            
        self.canvas.reper = [0.00,0.00]
        self.infoText.set("Current file: "+self.lst[self.currentfileindex])
        self.info.configure(text=self.infoText.get())
        self.canvas.configure(self.lst[self.currentfileindex])
   
    def _hideshowdescriptions(self,event):
        if self.canvas.flagDescription:
            txt = "Show descriptions"
        else:
            txt = "Hide descriptions"
        self.canvas.flagDescription = not self.canvas.flagDescription
        self.showbutton["text"] = txt
        # self.canvas.paint()
        self.canvas.genfield()
        
    def _changemashtab(self,event,dmX,dmY):
        x,y=0,1
        self.canvas.mashtab[x]*=dmX
        self.canvas.mashtab[y]*=dmY
        self.canvas.genfield()
        
    def _genAll(self,event):
        '''
        сгенерировать список кнопок, удалить перед использованием
        '''
        self.canvas.paint()
        #здесь мы создаем группу кнопок
        gr = list()
        for item in self.canvas.field.group:
            print(item[2][2])
            if not (item[2][2] in gr):#выделяем уникальные данные
                gr.append(item[2][2])
        if self.lstButton!=None:
            for item in self.lstButton:
                item.destroy()
        self.lstButton = list()
        for g in gr:
            b = Button(self.inframe,text=g)
            b.pack()
            self.lstButton.append(b)
        
    
    def configure(self):
        self.window.bind("<MouseWheel>",lambda event:self._wheel(event))
        self.canvas.canvas.bind("<Button-1>",lambda event:self._genAll(event))
        self.window.bind("<Key-Right>",lambda event:self.canvas.move(event,10,0)) 
        self.window.bind("<Key-Left>",lambda event:self.canvas.move(event,-10,0))
        self.window.bind("<Key-Down>",lambda event:self.canvas.move(event,0,10))
        self.window.bind("<Key-Up>",lambda event:self.canvas.move(event,0,-10))
        self.window.bind("<Key-plus>",lambda event:self._changemashtab(event,1.1,1.1))
        self.window.bind("<Key-minus>",lambda event:self._changemashtab(event,0.9,0.9))
        self.showbutton.bind("<Button-1>",lambda event:self._hideshowdescriptions(event))
        
    def startloop(self):
        self.rightframe.pack(side="right",expand="y",fill="y")
        self.showbutton.pack(side="top")
        self.info.pack(side="top")
        self.listfiles.pack(side="top")
        self.lmashtab.pack(side="top")
        self.inframe.pack(side="top")
        self.helpText.pack(side="bottom")
        self.window.mainloop()

if __name__ == "__main__":
    PRGviewerapp = App()
    PRGviewerapp.configure()
    PRGviewerapp.startloop()
