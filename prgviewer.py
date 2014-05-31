#__encoding=utf-8
#Программа для просмотра файлов prg в заданном каталоге
#поддержка файлов формата prg v2, v1
#27/03/2014  вместо кнопки Show/Hide флажки
#TODO заменить кнопки на список
#TODO кнопка для сброса фильтра

from sys import argv as sys_argv
from os import path as path2program
from os import listdir
from os import _exit
from os import chdir

from tkinter import Tk
from tkinter import Canvas
from tkinter import Event, StringVar, IntVar, BooleanVar
from tkinter import Menu, Button, Scale, Radiobutton, Frame, Label
from tkinter import Listbox, Scrollbar
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import END, VERTICAL, RIGHT, LEFT, BOTH, Y

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
        self.form = "rectangle"
        self.jakors = ["ALL"]
        
    

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

    def configure(self,file=None,filter= None):
        if file!=None:
            self.fileprogram = file
        if filter!=None:
            self.filter=filter

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
        
        self.canvas.delete("FIG")
        self.canvas.delete("DESC")

        for c in self.field.group:
            cx = (c[x]+self.sXY[x])*self.mashtab[x]+self.reper[x]
            cy = (c[y]+self.sXY[y])*self.mashtab[y]+self.reper[y]
            # print(c[d][2])
            if self.filter!=None:
                _color1,_color2 = ["red","red"] if self.filter(c[d][2]) else ["black","black"]
            else:
                _color1,_color2 = "black","black"
            
            self.canvas.create_rectangle(cx-1,cy-1,cx+1,cy+1,outline=_color1,fill=_color2,tag="FIG")
            if self.flagDescription:
                self.canvas.create_text(cx,cy,anchor="nw",text=str(c[d][1]), fill=_color1,font="Verdana 8",tag="DESC")

    def move(self,x,y):
        #в группы
        self.reper[0]+=x
        self.reper[1]+=y
        self.canvas.move("FIG",x,y)
        self.canvas.move("DESC",x,y)

    def load(self):
        _p = prg(self.fileprogram)
        _p.download()
        _p.extract()
        #здесь можно разместить фильтрацию по группам, только фильтр(фильтры) нужно передавать через параметр
        self.field.group = [x[1:4] for x in _p.progdigit if "25" in x[3]]
        print(self.field)

    def paint(self):
        self.load()
        try:
            self.setMashtab()
            self.genfield()
        except ZeroDivisionError:
            print("Zero division")

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
        #иконка
        _lst = sys_argv[0].split('\\')
        self.window.iconbitmap('\\'.join(_lst[:-1])+'\\PRGViewer-logo.ico')
        
        self.rightframe = Frame(self.window, bg="light grey",height=500, width=200)
        
        #рамка для списка
        self.inframe = Frame(self.rightframe, bg="yellow")
        # self.lstButton = None
        scrollbar = Scrollbar(self.inframe, orient=VERTICAL) #нужен для отображения длинных списков
        self.lstFilter = Listbox(self.inframe, yscrollcommand=scrollbar.set, bg="grey") #синхронизируем
        scrollbar.config(command=self.lstFilter.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        #вносим первый элемент
        self.lstFilter.insert(END,"Nothing")
        ''''-------------------------------'''
        self.canvas = prgCanvas(self.window,500,500)
        self.canvas.configure(file=self.lst[self.currentfileindex])
        self.canvas.paint()

        self.showDescriptions = BooleanVar()
        self.showDescriptions.set(1)
        self.rbDescShow = Radiobutton(self.rightframe, text = "Hide description",width=20,
                                      variable = self.showDescriptions, value = 0)
        self.rbDescHide = Radiobutton(self.rightframe, text = "Show description",width=20,
                                      variable = self.showDescriptions, value = 1)

        self.infoText = StringVar()
        self.infoText.set("Current file: "+self.lst[self.currentfileindex])
        self.info = Label(self.rightframe,text=self.infoText.get())
        self.listFilesText = StringVar()
        self.listFilesText.set("\n".join(self.lst))
        self.listfiles = Label(self.rightframe,text=self.listFilesText.get())
        self.lmashtab = Label(self.rightframe, text=":".join([str(x) for x in self.canvas.mashtab]))
        self.helpText = Label(self.rightframe, text="Use mouse wheel to select file\n"+
            "Use left mouse button to load file\n"+
            "Use Up,Down,Right,Left buttons to move field\n"+
            "Use Show/Hide descriptions button\n"+
            "Use +/- buttons to change scale of field",anchor="n",justify=LEFT)

    def set_path_and_current(self, filename):
        '''
        эта функция обрабатывает полный путь до файла
        '''
        try:
            _lst = filename.split('\\')
            self.path    = '\\'.join(_lst[:-2])
            chdir('\\'.join(_lst[:-1]))
            print(listdir("."))
            self.lst     = [x for x in listdir(".")  if ".prg" in x]
            self.currentfileindex = self.lst.index(_lst[-1])
            
            self.infoText.set("Current file: "+self.lst[self.currentfileindex])
            self.info.configure(text=self.infoText.get())
            
            self.listFilesText.set("\n".join(self.lst))
            self.listfiles.configure(text=self.listFilesText.get())
            
            self.canvas.configure(self.lst[self.currentfileindex])
            self._genAll()
        except IOError:
            self.infoText.set("Error")
            self.info.configure(text=self.infoText.get())
            

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
        '''
        '''
        self.canvas.flagDescription = self.showDescriptions.get()
        self.canvas.genfield()

    def _changemashtab(self,event,dmX,dmY):
        x,y=0,1
        self.canvas.mashtab[x]*=dmX
        self.canvas.mashtab[y]*=dmY
        self.canvas.genfield()

    def _selectGroup(self,name):
        print("select"+name)
        #устанавливаем фильтр
        self.canvas.configure(filter=lambda x: x==name)
        #перерисовываем
        self.canvas.paint()

    def _genAll(self):
        '''
        сгенерировать список кнопок, удалить перед использованием
        '''
        #рисуем
        self.canvas.paint()
        #здесь мы создаем группу
        gr = list()
        for item in self.canvas.field.group:
            print(item[2][2])
            if not (item[2][2] in gr):#выделяем уникальные данные
                gr.append(item[2][2])
        
        self.lstFilter.delete(1,END)
        
        for item in gr:
            self.lstFilter.insert(END,item)

    def configure(self):
        self.window.bind("<MouseWheel>",lambda event:self._wheel(event))
        self.canvas.canvas.bind("<Button-1>",lambda event:self._genAll())
        self.window.bind("<Key-Right>",lambda event:self.canvas.move(10,0))
        self.window.bind("<Key-Left>",lambda event:self.canvas.move(-10,0))
        self.window.bind("<Key-Down>",lambda event:self.canvas.move(0,10))
        self.window.bind("<Key-Up>",lambda event:self.canvas.move(0,-10))
        self.window.bind("<Key-plus>",lambda event:self._changemashtab(event,1.1,1.1))
        self.window.bind("p",lambda event:self._changemashtab(event,1.1,1.1))
        self.window.bind("<Key-minus>",lambda event:self._changemashtab(event,0.9,0.9))
        self.window.bind("m",lambda event:self._changemashtab(event,0.9,0.9))
        self.trace_show = self.showDescriptions.trace_variable("w",lambda v,i,m:self._hideshowdescriptions(v))
        self.lstFilter.bind("<<ListboxSelect>>", lambda event: self._selectGroup(self.lstFilter.get(self.lstFilter.curselection())))
        self.lstFilter.unbind("<Key-Up>")
        self.lstFilter.unbind("<Key-Down>")

    def startloop(self):
        self.rightframe.pack(side="right",expand="y",fill="y")
        self.rbDescHide.pack(side="top")
        self.rbDescShow.pack(side="top")
        self.info.pack(side="top")
        self.listfiles.pack(side="top")
        self.lmashtab.pack(side="top")
        self.inframe.pack(side="top")
        self.lstFilter.pack(side=LEFT, fill=BOTH, expand=1)
        self.helpText.pack(side="bottom")
        self.window.mainloop()

if __name__ == "__main__":
    PRGviewerapp = App()
    if (len(sys_argv)==2):
        PRGviewerapp.set_path_and_current(sys_argv[1])
    PRGviewerapp.configure()
    PRGviewerapp.startloop()