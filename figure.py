import shelve
from math import cos,sin

def transform(x,y,a,etalon):
        """
        внешняя функция - здесь, для хранения и последующего использования
        точка отсчета - в центре эталона
        """
        new = list()
        for item in etalon:
            ca = cos(a)
            sa = sin(a)
            x2,y2 = item[0]-x, item[1]-y
            
            new.append([x2*ca + y2*sa+x, x2*sa - y2*ca+y])
        return new
        
class figure(object):
    '''
    загружает, сохраняет, хранит и обрабатывает шаблоны для отображения компонентов
    '''
    def __init__(self,name):
        self.name = name
        self.loadpattern()
            
    def loadpattern(self):
        '''
        загружает шаблон из базы
        '''
        try:
            db         = shelve.open("figure")
            self.pattern = db[self.name]
        except:
            self.pattern = None
        finally:
            db.close()
            
    def savepattern(self):
        '''
        сохраняет шаблон в базе
        '''
        if self.pattern!=None:
            try:
                db            = shelve.open("figure")
                db[self.name] = self.pattern
            except:
                self.pattern = None
            finally:
                db.close()
                
    def transform(self,x,y,angle):
        """
        рассчитывает новые координаты по опорной точке и углу поворота (x,y,a)
        угол поворота должен быть в радианах
        точка отсчета - в центре эталона
        """
        ca = cos(angle)
        sa = sin(angle)
        nX = lambda it: (it[0]-x)*ca+(it[1]-y)*sa+x
        nY = lambda it: (it[0]-x)*sa-(it[1]-y)*ca+y
        return [[nX(item),nY(item)] for item in self.pattern]
        
if __name__=="__main__":
    #тест на поведение при отсутствии компонента в хранилище
    fig1 = figure("SOT723")
    
    #тест поведения при наличии компонента в хранилище
    #тест удачного сохранения компонента в хранилище
    fig2 = figure("SOT723")
    fig2.pattern = []
    #тест неудачного сохранения компонента в хранилище