from tkinter import Tk, Frame, Canvas
from tkinter import LEFT,RIGHT

root = Tk()
root.minsize(width=300, height=200)

fr = Frame (root,width=120,height=120,bg="green")
ri = Frame (root,width=120,height=120,bg="blue")
cn = Canvas(fr,  width=10,height=10,bg="red")

fr.pack(side=LEFT, expand="y",fill="both")
ri.pack(side=RIGHT,expand="y",fill="x")
# ri.pack(side=RIGHT,fill="both")
cn.pack(side=LEFT)

root.mainloop()