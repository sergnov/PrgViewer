'''
Базовая версия компонента для PRG
'''
from tkinter import Frame,YES,BOTH,Tk,Label,LEFT,Text,TOP

class PRGComponent(Frame):
    def __init__(self, root=None, height=0, width=0, side = TOP):
        if root==None:
            root = Tk()
        self.owner = root
        self.side = side
        Frame.__init__(self, self.owner, height=height, width=width)
        self.start()
        self.makeWidgets()

    def makeWidgets(self):
        '''для последующего переопределения'''
        pass

    def start(self):
        '''для последующего переопределения'''
        Frame.pack(self, expand=YES, fill=BOTH, side=self.side)
    
if __name__=="__main__":
    '''
    тестирование
    '''
    class PRGTestComponent(PRGComponent):
        '''
        класс для проверки работоспособности
        '''
        def makeWidgets(self):
            Label(self,text="TEST").pack()

    class PRGTest2(PRGComponent):            
        def start(self):
            Frame.pack(self, expand = YES, fill=BOTH, side=LEFT)

        def makeWidgets(self):
            Text(self,width=20).pack()
        
    root = Tk()
    frm  = PRGTestComponent(root, height=300, width=200)
    frm2 = PRGTestComponent(root)
    frm3 = PRGTest2(root)
    root.mainloop()
