from tkinter import Frame, Listbox, Scrollbar, Tk
from tkinter import SINGLE, END, LEFT, BOTH, VERTICAL, RIGHT, Y

class PRGListBox(Frame):
    def __init__(self, master=None,**args):
        Frame.__init__(self, master,**args)
        scrollbar = Scrollbar(self, orient=VERTICAL) #нужен для отображения длинных списков
        scrollbar.unbind("<Key-Up>")
        scrollbar.unbind("<Key-Down>")
        scrollbar.unbind("<Key-Left>")
        scrollbar.unbind("<Key-Right>")
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.lst = Listbox(self, yscrollcommand=scrollbar.set, bg="grey", selectmode=SINGLE) 
        self.lst.insert(END,"Hide All")
        self.lst.insert(END,"Show All")
        self.lst.select_set(0)
        self.lst.pack(side=LEFT, fill=BOTH, expand=1)
        
        scrollbar.config(command=self.lst.yview)
        
        # (self.window, bg="light grey",height=500, width=200)
        
if __name__ == "__main__":
    root = Tk()
    r = PRGListBox(root)
    for i in range(30):
        r.lst.insert(END,str(i))
    r.pack()
    root.mainloop()
