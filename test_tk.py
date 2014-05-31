from tkinter import Tk, Frame

class PRGTest(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)

    def __init__(self, parent=None, width=0, height=0):
        Frame.__init__(self, parent, width=width, height=height)

root = Tk()
frm = PRGTest(root)
frm.pack()
frm2 = PRGTest(root, width=100, height=100)
frm2.pack()
root.mainloop()
