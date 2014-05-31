from PRGComponent import PRGComponent

class PRGSettings(PRGComponent):
    pass

if __name__=="__main__":
    from tkinter import Tk
    root = Tk()
    frm = PRGSettings(root)
    root.mainloop()