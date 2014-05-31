'''
импорт документа и печать его содержимого
'''
import xml.dom.minidom
import tkinter as tk
from decimal import Decimal

def getTransform(dom,x,y):
    '''получаем смещения'''
    g = dom.getElementsByTagName("g")[0]
    s = g.getAttribute("transform")
    print(s)
    ln = len("translate(")
    s2 = s[ln:-1]
    l = s2.split(",")
    return x+float(l[0]),y+float(l[1])

def rects(canvas,dom,x0,y0,m):
    for item in dom.getElementsByTagName("rect"):
        #print(item)
        print("\t%s\t%s\t%s\t%s"%((item.getAttribute("x")),(item.getAttribute("y")),
            (item.getAttribute("width")),(item.getAttribute("height"))))

        x_= Decimal(str(x0))
        y_= Decimal(str(y0))
        x = Decimal(item.getAttribute("x"))
        y = Decimal(item.getAttribute("y"))
        h = Decimal(item.getAttribute("height"))
        w = Decimal(item.getAttribute("width"))
        
        #print("rectangle",x+x_,y+y_,h,w)

        k=10
        dx,dy = x+x_, y+y_
        dX,dY = dx+w, dy+h
        print("rectangle",dx,dy,dX,dY)
        canvas.create_rectangle(dx*k,dy*k,dX*k,dY*k)


def circles(canvas,dom,x0,y0,m):
    for item in dom.getElementsByTagName("path"):
        #print(item)
        #print("%s\t%s\t%s\t%s\t%s\t%s"%((item.getAttribute("sodipodi:type")),
            #(item.getAttribute("sodipodi:cx")),
            #(item.getAttribute("sodipodi:cy")),
            #(item.getAttribute("sodipodi:rx")),
            #(item.getAttribute("sodipodi:ry")),
            #(item.getAttribute("d"))))
        if item.getAttribute("sodipodi:type")=="arc":
            x_= Decimal(str(x0))
            y_= Decimal(str(y0))
            x = Decimal(item.getAttribute("sodipodi:cx"))
            y = Decimal(item.getAttribute("sodipodi:cy"))
            h = Decimal(item.getAttribute("sodipodi:rx"))
            w = Decimal(item.getAttribute("sodipodi:ry"))
        
            print("arc",x+x_,y+y_,h,w)

            ln = len("matrix(")
            transform  = item.getAttribute("transform")[ln:-1]
            print("tr",transform)
            l = transform.split(",")[-2:]
            print(l)
            tx = Decimal(l[0])
            ty = Decimal(l[1])
            
            
            k=10
            dx,dy = x+x_, y+y_
            dX,dY = dx+w, dy+h
            print("arc",dx,dy,dX,dY)
            canvas.create_oval(dx*k,dy*k,dX*k,dY*k)
    
root = tk.Tk()
canvas = tk.Canvas(root,width=500,height=500,bg="light grey")
canvas.pack()
x,y = 0,0



#dom = xml.dom.minidom.parse("sot23.svg")

dom = xml.dom.minidom.parse("sot457-sc74.svg")

x,y = getTransform(dom,x,y)
print(x,y)

rects(canvas,dom,x,y,5)
circles(canvas,dom,x,y,5)

#for item in dom.getElementsByTagName("path"):
#    print(item)
#    print((item.getAttribute("d")))

#for item in dom.getElementsByTagName("text"):
#    print(item)
#    print("\t%s\t%s"%(item.getAttribute("x"),item.getAttribute("y")))


#    it = item.getElementsByTagName("tspan")[0]
#    print(it)
#    print(it.tagName)
#    print("\t\t%s\t%s" % (it.getAttribute("x"),it.getAttribute("y")))
