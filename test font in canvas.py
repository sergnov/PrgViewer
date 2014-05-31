from tkinter import Tk, Canvas

root = Tk()
c = Canvas(root,height=500,width=500)
c.pack()
c.create_text(100,100,text="hello",font="Verdana 8 bold",fill="black")
root.mainloop()