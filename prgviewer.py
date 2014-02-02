from tkinter import Tk
from tkinter import Menu, Button, Scale, Radiobutton, Frame
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import IntVar
from tkinter import VERTICAL

from os import _exit

class commands:
    def __init__(self,root):
        self.root = root
        
    def descOpen(self):
        self.op = askopenfilename()
        
    def descAbout(self):
        showinfo(title="About",message="PRG File Viewer version 0.0.1")
        
    def descExit(self):
        _exit(0)
        
class prgMenu:
    def __init__(self,root,cm):
        self.m = Menu(root)
        self.root = root
        self.root.config(menu=self.m)
         
        self.fm = Menu(self.m)
        self.m.add_cascade(label="File",menu=self.fm) 
        self.fm.add_command(label="Open",command=cm.descOpen) 
        self.fm.add_command(label="Exit",command=cm.descExit)
        
        self.m.add_command(label="About",command=cm.descAbout)

class rB:
    def __init__(self,root):
        self.root=root
        self.var=IntVar()
        self.var.set(0)
        self.nazv = ["Show components","Hide components"]
        self.valz = [True,False]
        self.raD = [Radiobutton(self.root,text=x, font="Verdana 10", variable=self.var,value=y) for x,y in zip(self.nazv,self.valz)]
        
    def _pack(self):
        for r in self.raD: r.pack()
        
    def _grid(self):
        for r,y in zip(self.raD,range(0,2)): r.grid(row=0,column=y)

root = Tk()

c=commands(root)
p=prgMenu(root,c)

frHolst = Frame(root)
frHolstInner = Frame(frHolst,bg = "white", height=500, width=500)
sca = Scale(frHolst, orient=VERTICAL,length=300,from_=0,to=10,tickinterval=1,resolution=1)

frCommand = Frame(root)
r=rB(frCommand)
bNext = Button(frCommand,text="Next")
bPrev = Button(frCommand,text="Prev")

frHolst.pack(expand="yes",fill='y')
frHolstInner.pack(side="left",expand="yes",fill='y')
sca.pack(side="right",expand="yes")

frCommand.pack()
r._grid()
bNext.grid(row=1,column=0)
bPrev.grid(row=1,column=1)
root.mainloop()