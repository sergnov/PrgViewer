import xml.dom.minidom
from decimal import Decimal

def multipleMatrix(m1,m2):
    pass

def readTransform(dom):
    '''получаем смещения'''
    g = dom.getElementsByTagName("g")[0]
    s = g.getAttribute("transform")
    
    #определяем тип трансформации и выделяем данные
    if "matrix" in s:
        #print("matrix")
        ln = len("matrix(")
        s2 = s[ln:-1]
        l = s2.split(",")
        return l,"matrix"
    elif "translate" in s:
        #print("translate")
        ln = len("translate(")
        s2 = s[ln:-1]
        l = s2.split(",")
        return l,"translate"
    elif "scale" in s:
        #print("translate")
        ln = len("scale(")
        s2 = s[ln:-1]
        l = s2.split(",")
        return l,"scale"
    elif "rotate" in s:
        pass
    elif "skewX" in s or "skewY" in s:
        pass #не планирую поддерживать
    return None
    
#открыть файл и загрузить в парсер
dom = xml.dom.minidom.parse("sot457-sc74.svg")

#сосчитать матрицу перехода, если нет - создать единичную
transform = readTransform(dom)
if transform == None:
    transform = [1,0,0,1,1,1]

#получить список элементов
#перебрать список
    #есть ли матрица? есть - считать и перемножить с исходной
    #тип элемента - прямоугольник
    #тип элемента - path + arc
    #тип элемента - path