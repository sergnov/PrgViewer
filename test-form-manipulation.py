from tkinter import Tk, Frame, Canvas, Button
from tkinter import LEFT, RIGHT, TOP, BOTTOM

root = Tk()
root.minsize(width=510,height=510)
root.maxsize(width=800,height=800)

leftframe = Frame(root,width=600,height=500,bg="white")
rightframe = Frame(root, width=200, height=500,bg="dark gray")

bt = (Button(rightframe,text=str(x),width=10) for x in range(10))

topleftframe = Frame(leftframe,width=600, height=100, bg="yellow")
bottomleftframe = Frame(leftframe, width=600, height=100, bg="red")

canvas = Canvas(topleftframe,width=550, height=450)
btnext = Button(bottomleftframe,text="Next")
btprev = Button(bottomleftframe,text="Prev")

leftframe.pack(side=LEFT,expand="y",fill="y")
rightframe.pack(side=RIGHT,expand="y",fill="y")

for b in bt:
    b.pack(side=TOP)

topleftframe.pack(side=TOP, expand="y",fill="y")
bottomleftframe.pack(side=BOTTOM, expand="y",fill="y")
canvas.pack(expand="y",fill="y")
btnext.pack(side=RIGHT)
btprev.pack(side=LEFT)

root.mainloop()