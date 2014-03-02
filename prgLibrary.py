#Модуль для открытия, разбора, преобразования и сохранения файлов prg
#TODO добавить отсечение на уровне содержимого строки, таким образом мы например сможем отсекать все строки, кроме строк с кодами 025 (см. функцию extract)

from csv import reader as csvreader

class prg(object):
    def __init__(self,path):
        self.program = None
        self.progdigit = None
        self.progscreen = None
        self.title = None
        self.path2prg = path
    
    def extract(self):
        if self.program != None:
            self.progdigit = list()
            for line in self.program:
                testdigit = line[-3:]
                try:
                    digit = list()
                    digit = [ float(x) for x in testdigit]
                    digit.append(line[0:-3])
                    self.progdigit.append(digit)
                except ValueError:
                    print("Line is corrupted")
    
    def screen(self, screenSize, mashtab, program):
        '''Вычисляет экранные координаты для заданного экрана'''
        def minmax(list):
            sX,sY,mX,mY = 0,0,0,0
            for c in list:
                c[0] = float(c[0])
                c[1] = float(c[1])
                if c[0]<sX: sX = c[0]
                elif c[0]>mX: mX = c[0]
                
                if c[1]<sY: sY = c[1]
                elif c[1]>mY: mY = c[1]
            return sX,sY,mX,mY
        x,y=0,1
        if program == None:
            program = self.progdigit
        sX,sY,mX,mY = minmax(program)
        self.progscreen = list()
        for c in program:
            screenX = (c[x]+abs(0-sX))*mashtab[x]
            screenY = (c[y]+abs(0-sY))*mashtab[y]
            self.progscreen.append([screenX,screenY])
        
    def download(self):
        try:
            reader = csvreader(open(self.path2prg, 'r'), delimiter="\t", skipinitialspace=True)
            self.program = list()
            self.title = list()
            for row in reader:
                #команда
                if (len(row)>=5):
                    line=row[0]
                    if (line[0]!=";"):
                        # Command=ExtXY(row)
                        # program.append(Command)
                        self.program.append(row)
                #заголовок или комментарий
                if len(row)>0 and ";" in row[0]:
                    self.title.append(row)
        except OSError as err:
            print(err)
            self.program = None
            self.title = None
    
    def complete(self):
        '''проверяет состояние класса'''
        return self.program!=None and self.title!=None
    
    def printcoords(self):
        if self.program != None:
            print("Body")
            for c in self.program:
                print(c)
        else:
            print("body is empty")
            
    def printtitle(self):
        if self.title != None:
            print("Title")
            for c in self.title:
                print(c)
        else:
            print("Title is empty")
        

if __name__ == "__main__":
    #перед тестом нужно создавать этот файл во временной папке, а не брать
    print("Test 1")
    p1=prg("1.prg")
    p1.download()
    p1.extract()
    p1.printtitle()
    p1.printcoords()
    lst  = [ x for x in p1.program if "25" in x]
    for c in lst:
        print(c)
    if p1.complete():
        for c in p1.progdigit:
            print(c)
    else:
        print("Nothing")
    m = [10.00,10.00]
    p1.screen([500,500],m,None)
    print()
    for c in p1.progscreen:
        print(c)
    
    print("Test 2")
    p2=prg("djnfjkfvh")
    p2.download()
    p2.extract()
    print(p2.complete())
    p2.screen([500,500],m,None)
    for c in p2.progscreen:
        print(c)