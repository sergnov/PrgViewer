from prgLibrary import prg

def setMashtab(group,width,height):
    '''Эта функция устанавливает текущий масштаб, так чтобы вся плата была в зоне видимости'''
    def findcoord(field):
        sX,sY,mX,mY = field[0][0],field[0][1],field[0][0],field[0][1]
        for c in field:
            if c[0]<sX: sX = c[0]
            elif c[0]>mX: mX = c[0]
            if c[1]<sY: sY = c[1]
            elif c[1]>mY: mY = c[1]
        return [sX,sY,mX,mY]
    sX,sY,mX,mY=findcoord(group)
    print(sX,sY,mX,mY)
    lX = width
    lY = height
    lengthX = abs(mX-sX)
    lengthY = abs(mY-sY)
    if lengthX>0 and lengthY>0:
        cX = lX/lengthX
        cY = lY/lengthY
    else:
        cX,cY=1.0,1.0
    mashtab = min(cX,cY) 
    sXY     = [abs(0-sX),abs(0-sY)] 
    print("sXY",sX,sY)
    return [mashtab,sXY]
        
def load(fileprogram):
    _p = prg(fileprogram)
    _p.download()
    # print(_p.program)
    _p.extract()
    
    group = [x[1:4] for x in _p.progdigit if "25" in x[3]]
    return group

# print("ex-changefeeder.prg")
# group = load("ex-changefeeder.prg")
# msh   = setMashtab(group,800,600)
# print(msh)

print("\nmulti.prg")
group = load("multi.prg")
msh   = setMashtab(group,800,600)
# print(msh)