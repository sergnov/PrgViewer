from PRGComponent import PRGComponent
from PRGCanvas import PRGCanvas
from PRGSettings import PRGSettings
from PRGInfo import PRGInfo
from PRGFilter import PRGFilter
from tkinter import LEFT,RIGHT

class App(PRGComponent):
    def makeWidgets(self):
        cnv = PRGCanvas(self,side=LEFT,height=500,width=500)
        set = PRGSettings(self,side=RIGHT,height=100,width=100)
        flt = PRGFilter(self,side=RIGHT,height=100,width=100)
        inf = PRGInfo(self,side=RIGHT, height=100, width=100)
    
if __name__=="__main__":
    PRGViewer = App()
