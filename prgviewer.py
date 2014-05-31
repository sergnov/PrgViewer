#__encoding=utf-8
#Программа для просмотра файлов prg в заданном каталоге
#поддержка файлов формата prg v2, v1

from sys import argv as sys_argv
from os import path as path2program
from os import listdir
from os import _exit
from os import chdir
from random import randint
from math import cos,sin,radians

from tkinter import Tk
from tkinter import Canvas
from tkinter import Event, StringVar, IntVar, BooleanVar
from tkinter import Menu, Button, Scale, Radiobutton, Frame, Label
from tkinter import Listbox, Scrollbar
from tkinter import END, VERTICAL, BOTH, X, Y, SINGLE, DISABLED, NORMAL
from tkinter import TOP, BOTTOM, RIGHT, LEFT

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

from prgLibrary import prg
from prgWidgets import PRGListBox

class prgCanvas(Frame):
    def __init__(self,window=None,height=500,width=500,bg="grey"):
        Frame.__init__(self,window,height=height,width=width,bg=bg)
        self.canvas = Canvas(self, bg=bg, height=height, width=width)
        self.flagDescription = False
        self.setdefault(mashtab=True,reper=True,normalization=True)
        self.canvas.pack(expand='y',fill="both")
        self.field = None #данные, блоки групп, графические примитивы, точки, #графические примитивы, надписи
        self.fileprogram = None #имя файла для загрузки

        self.filter = None #фильтр, по которому определяется выделенный фрагмент

    def setdefault(self,mashtab=False,reper=False,normalization=False):
        if mashtab:
            self.mashtab = 1.00 #масштаб
        if reper:
            self.reper = [10.00,10.00] #смещение
        if normalization:
            self.normalization = [0.00,0.00] #коэффициент для нормализации координат
        
    def configure(self,file=None,filter= None):
        if file!=None:
            self.fileprogram = file
        self.filter=filter

    def setMashtab(self):
        '''Эта функция устанавливает текущий масштаб, так чтобы вся плата была в зоне видимости'''
        def findcoord(field):
            mX,mY = field[0][0],field[0][1]
            # sX,sY = field[0][0],field[0][1]
            sX,sY = 0, 0
            for c in field:
                if c[0]<sX: sX = c[0]
                elif c[0]>mX: mX = c[0]
                if c[1]<sY: sY = c[1]
                elif c[1]>mY: mY = c[1]
            return [sX,sY,mX,mY]
        sX,sY,mX,mY=findcoord(self.field)
        lX = int(self.canvas["width"])
        lY = int(self.canvas["height"])
        lengthX = abs(mX-sX)
        lengthY = abs(mY-sY)
        if lengthX>0 and lengthY>0:
            cX = lX/lengthX
            cY = lY/lengthY
        else:
            cX,cY=1.0,1.0
        print("MSH",cX,cY)
        
        self.normalization = [abs(sX),abs(sY)]
        self.mashtab = int(min(cX,cY)*0.9)
    
    def transform(self,x,y,a,etalon):
        """
        точка отсчета - в центре эталона
        """
        new = list()
        for item in etalon:
            ca = cos(a)
            sa = sin(a)
            x2,y2 = item[0]-x, item[1]-y
            
            new.append([x2*ca + y2*sa+x, x2*sa - y2*ca+y])
        return new
        
    def genfield(self):
        x,y,d=0,1,2
        
        self.canvas.delete("all")

        for c in self.field:
            cx = (c[x]+self.normalization[x])*self.mashtab+self.reper[x]
            cy = (c[y]+self.normalization[y])*self.mashtab+self.reper[y]

            print("filter",self.filter)
            
            if self.flagDescription and self.filter==None:
                tag = "BLACK"
                _color1,_color2 = "black","black"
                font = "Verdana 8"
                self.canvas.create_text(cx,cy,anchor="nw",text=str(c[d][1]), fill=_color1,font=font,tag=("DESC",tag))
            elif (not self.flagDescription) and self.filter==None:
                tag = "BLACK"
                _color1,_color2 = "black","black"
            elif self.flagDescription and self.filter!=None and self.filter(c[d][2]):
                _color1,_color2 = ["red","red"]
                tag = "RED"
                font = "Verdana 10 bold"
                self.canvas.create_text(cx,cy,anchor="nw",text=str(c[d][1]), fill=_color1,font=font,tag=("DESC",tag))
            elif self.flagDescription:
                _color1,_color2 = "black","black"
                tag = "BLACK"
                # font = "Verdana 8"
                # self.canvas.create_text(cx,cy,anchor="nw",text=str(c[d][1]), fill=_color1,font=font,tag=("DESC",tag))
                pass
                
            # здесь может быть выбор фигуры
            # здесь может быть угол поворота
            print("c",c)
            if c[-2][0]=="25":
                angle = radians(c[-1])
                pattern = [[-3,-5.0],[3,-5.0],[0.0,3.0],[-3.0,-5.0]]
                et = [[cx+item[0],cy+item[1]] for item in pattern]
                new = self.transform(cx,cy,angle,et)
                self.canvas.create_polygon(new,activefill=_color1,fill=_color2,tag=("FIG",tag))
            else:
                self.canvas.create_rectangle(cx-1,cy-1,cx+1,cy+1,outline=_color1,fill=_color2,tag=("FIG",tag))
        self.canvas.tag_lower("RED")
        
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
        #вариант кода для загрузки информации о установке
        self.field = [x[1:4]+[x[0]] for x in _p.progdigit if ("25" in x[3]) or ("107" in x[3])]
        print(_p.progdigit)
        #вариант кода для загрузки информации о дозировании:
        # self.field.group = [x[1:4] for x in _p.progdigit if "107" in x[3]]
        # print(self.field)

    def paint(self):
        self.load()
        try:
            self.setMashtab()
            self.genfield()
        except ZeroDivisionError:
            print("Zero division")
        except IndexError:
            print("Index error")
            #рисуем надпись
            self.canvas.delete("all")
            x,y = int(self.canvas["width"]),int(self.canvas["height"])
            self.canvas.create_text(x//2,y//2,text="FILE IS CORRUPTED", font="Verdana 12 bold",fill="red",tag="del")

        
        
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
        w = 850
        h = 500
        self.window.minsize(width=w-100,height=h-100)
        self.window.maxsize(width=w,height=h)
        #иконка
        _lst = sys_argv[0].split('\\')
        self.window.iconbitmap('\\'.join(_lst[:-1])+'\\PRGViewer-logo.ico')
        
        #ПАНЕЛИ
        # self.leftframe       = Frame(self.window,    bg="blue",  width=int(w*0.667),height=h)
        self.leftframe       = Frame(self.window,    bg="grey",  width=int(w*0.667),height=h)
        # self.bottomleftframe = Frame(self.leftframe, bg="red",   width=w//4,        height=int(h*0.2))
        self.bottomleftframe = Frame(self.leftframe, bg="grey",   width=w//4,        height=int(h*0.2))
        # self.rightframe      = Frame(self.window,    bg="yellow",width=int(w*0.333),height=h)
        self.rightframe      = Frame(self.window,    bg="dark grey",width=int(w*0.333),height=h)
        
        #canvas
        self.set_canvas(             self.leftframe, bg="dark green", width=int(w*0.667),height=int(h*0.8))
        # self.set_canvas(             self.leftframe, bg="light green", width=100,height=100)
        
        #кнопки
        self.nextButton = Button(self.bottomleftframe,text="Next",width=10)
        self.prevButton = Button(self.bottomleftframe,text="Prev",width=10)
        
        #Список фильтров
        self.Filter = PRGListBox(self.rightframe,width=w-500)

        #Выбор файла платы
        self.infoText = StringVar()
        self.infoText.set("Current file: "+self.lst[self.currentfileindex])
        self.info = Label(self.rightframe,text=self.infoText.get())
        self.listFilesText = StringVar()
        self.listFilesText.set("\n".join(["Files:    "]+self.lst))
        self.listfiles = Label(self.rightframe,text=self.listFilesText.get(),anchor="w",justify=LEFT)
        
        self.helpText = Label(self.rightframe, text="Use Next/Prev (Pg Down/Up) buttons for change file\n"+
            "Use Up,Down,Right,Left buttons for move field\n"+
            "Select row in ListBox for change vision mode\n"+
            "Use +/- (p/m) buttons for scaling of field",anchor="n",justify=LEFT)
            
        

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
            self.canvas.setdefault(reper=True)
            #рисуем
            self.canvas.paint()
            #здесь мы создаем группу
            gr = list()
            for item in self.canvas.field:
                print(item[2][2])
                if not (item[2][2] in gr):#выделяем уникальные данные
                    gr.append(item[2][2])
            
            self.Filter.lst.delete(2,END)
            
            for item in gr:
                self.Filter.lst.insert(END,item)
        except IOError:
            self.infoText.set("Error")
            self.info.configure(text=self.infoText.get())
            
    def set_canvas(self,master=None,height=500,width=500,bg="grey"  ):
        if master==None:
            master=self.window
        self.canvas = prgCanvas(master,height=height,width=width,bg=bg)
        
        
    def nextprev(self,direction):
        self.currentfileindex+=1 if abs(direction)==direction else -1
        
        if self.currentfileindex<0:
            self.currentfileindex = len(self.lst)-1
        elif self.currentfileindex>len(self.lst)-1:
            self.currentfileindex = 0
        self.canvas.setdefault(reper=True)
        self.infoText.set("Current file: "+self.lst[self.currentfileindex])
        self.info.configure(text=self.infoText.get())
        self.canvas.configure(self.lst[self.currentfileindex]) 
        #рисуем
        self.canvas.paint()
        #здесь мы создаем группу
        gr = list()
        for item in self.canvas.field:
            print(item[2][2])
            if not (item[2][2] in gr):#выделяем уникальные данные
                gr.append(item[2][2])
        
        self.Filter.lst.delete(2,END)
        
        for item in gr:
            self.Filter.lst.insert(END,item)

    def _changemashtab(self,event,dm):
        self.canvas.mashtab*=dm
        self.canvas.genfield()

        
    def filter_selection(self):
        name = self.Filter.lst.get(self.Filter.lst.curselection())
        if name == "Hide All":
            print("Hide All")
            self.canvas.flagDescription = False
            self.canvas.filter = None
            self.canvas.genfield()
        elif name =="Show All":
            print("Show All")
            self.canvas.flagDescription = True
            self.canvas.filter = None
            self.canvas.genfield()
        else:
            print("Other filter"+name)
            self.canvas.flagDescription = True
            #устанавливаем фильтр
            self.canvas.configure(filter=lambda x: x==name)
            #перерисовываем
            self.canvas.paint()

    def configure(self):            
        self.window.bind("<Key-Right>",lambda event:self.canvas.move(10,0))
        self.window.bind("<Key-Left>",lambda event:self.canvas.move(-10,0))
        self.window.bind("<Key-Down>",lambda event:self.canvas.move(0,10))
        self.window.bind("<Key-Up>",lambda event:self.canvas.move(0,-10))
        self.window.bind("<Key-plus>",lambda event:self._changemashtab(event,1.1))
        self.window.bind("p",lambda event:self._changemashtab(event,1.1))
        self.window.bind("<Key-minus>",lambda event:self._changemashtab(event,0.9))
        self.window.bind("m",lambda event:self._changemashtab(event,0.9))
        self.Filter.lst.bind("<<ListboxSelect>>", lambda event: self.filter_selection())
        self.Filter.bind("<Leave>",lambda event: self.window.focus_force())
        
        self.nextButton.configure(command=lambda:self.nextprev(1))
        self.prevButton.configure(command=lambda:self.nextprev(-1))
        self.window.bind("<Key-Prior>",lambda event:self.nextprev(-1)) #Page Up
        self.window.bind("<Key-Next>",lambda event:self.nextprev(1)) #Page Down

    def startloop(self):
        self.leftframe.pack (side=LEFT,expand="y",fill="both")
        # self.leftframe.pack ()
        print("leftframe")
        
        self.canvas.pack         (expand="y",fill="both")
        self.canvas.canvas.pack  ()
        self.canvas.configure(file=self.lst[self.currentfileindex])
        self.canvas.paint()
        
        self.bottomleftframe.pack()
        self.nextButton.pack     (side=RIGHT)
        self.prevButton.pack     (side=LEFT)
        
        self.rightframe.pack(side=RIGHT,expand="y",fill="y")
        # self.rightframe.pack()
        print("rightframe")
        
        self.info.pack      (side=TOP,fill=X,expand=Y)
        self.listfiles.pack (side=TOP,fill=BOTH,expand=Y)
        self.Filter.pack    (side=TOP, fill=BOTH, expand=Y)
        self.helpText.pack  (side=BOTTOM)
        
        self.window.mainloop()

if __name__ == "__main__":
    PRGviewerapp = App()
    if (len(sys_argv)==2):
        PRGviewerapp.set_path_and_current(sys_argv[1])
    PRGviewerapp.configure()
    PRGviewerapp.startloop()