from PRGComponent import PRGComponent

class PRGInfo(PRGComponent):
    pass
    
if __name__=="__main__":
    from tkinter import Tk
    root = Tk()
    frm = PRGInfo(root)
    root.mainloop()