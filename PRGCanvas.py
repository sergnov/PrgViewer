from PRGComponent import PRGComponent

class PRGCanvas(PRGComponent):
    pass
    
if __name__=="__main__":
    from tkinter import Tk
    root = Tk()
    cnv = PRGCanvas(root)
    root.mainloop()
