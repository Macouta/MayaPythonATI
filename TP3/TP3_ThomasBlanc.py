# Importation des commandes Maya en Python
import maya.cmds as cmds
from math import sqrt

#clear file
cmds.file(f=True, new=True)

cmds.window(t="Temple Generator")
cmds.showWindow()
# ======================
# variables
# ======================
length = 20
width = 12
stairs = 10
height = 10

#length, width and height must be even
if(length % 2 != 0):
    length += 1
if(width % 2 != 0):
    width += 1
if(height % 2 != 0):
    height -= 1
    
# ======================
# Pillar creation
# ======================
pillarArr = []
pillarArr += cmds.polyCube(n="BottomCube", h=0.1)
cmds.move(0, 0.05, 0)

pillarArr += cmds.polyCube(n="BottomCube2", h=0.15, w= 0.9, d=0.9)
cmds.move(0, 0.1, 0)

pillarArr += cmds.polyCylinder(n="BottomCyl", h=0.3, r=0.40, sa=10)
cmds.move(0, 0.30, 0)

pillarArr += cmds.polyCylinder(n="BodyCyl", h=height, r=0.35, sa=10)
cmds.move(0, height/2, 0)

pillarArr += cmds.polyCylinder(n="TopCyl", h=0.3, r=0.40, sa=10)
cmds.move(0, height - 0.30, 0)

pillarArr += cmds.polyCube(n="TopRect", h=0.15, w= 0.9, d=0.9)
cmds.move(0, height - 0.1, 0)

pillarArr += cmds.polyCube(n="TopRect2", h=0.1)
cmds.move(0, height - 0.05, 0)

pillar = cmds.group(*pillarArr, n="pillar")
cmds.move(0, stairs/2, 0, pillar)
# cmds.hide(pillar)

# ======================
# draw inside
# ======================
if(length > 6 and width > 6):
    cmds.polyCube(h= height, w=length - 4, d=width - 4)
    cmds.move(0, height/2 + stairs/2, 0)

# ======================
# draw length pillars
# ======================
for i in range(-length/2 + 2, length/2, 2):

    pillarLeft = cmds.instance(pillar)
    pillarRight = cmds.instance(pillar)

    cmds.move( i, stairs/2 , width/2, pillarLeft )
    cmds.move( i, stairs/2 , - width/2, pillarRight )

# ======================
# draw width pillars
# ======================
for i in range(-width/2, width/2 + 2, 2):

    pillarLeft = cmds.instance(pillar)
    pillarRight = cmds.instance(pillar)

    cmds.move( length/2, stairs/2 , i, pillarLeft )
    cmds.move( -length/2, stairs/2 , i, pillarRight )

# ======================
# draw base roof
# ======================
cmds.polyCube(h= 0.50, w=length + 1.5, d=width + 1.5)
cmds.move(0, height + stairs/2 + 0.25, 0)
cmds.polyCube(h= 1, w=length + 1, d=width + 1)
cmds.move(0, height + stairs/2 + 1, 0)
cmds.polyCube(h= 0.20, w=length + 1.5, d=width + 1.5)
cmds.move(0, height + stairs/2 + 1.60, 0)

# ======================
# draw roof decoration length
# ======================
for i in range(-length/2, length/2 + 1, 2):
    cmds.polyCylinder(h=1, r=0.1, sa=10)
    cmds.move(i, height + stairs/2 + 1, width/2 + 0.5)
    cmds.duplicate()
    cmds.move(i + 0.15, height + stairs/2 + 1, width/2 + 0.5)
    cmds.duplicate()
    cmds.move(i - 0.15, height + stairs/2 + 1, width/2 + 0.5)

    cmds.duplicate()
    cmds.move(i, height + stairs/2 + 1, - width/2 - 0.5)
    cmds.duplicate()
    cmds.move(i + 0.15, height + stairs/2 + 1, - width/2 - 0.5)
    cmds.duplicate()
    cmds.move(i - 0.15, height + stairs/2 + 1, - width/2 - 0.5)

# ======================
# draw roof decoration width
# ======================
for i in range(-width/2, width/2 + 1, 2):
    cmds.polyCylinder(h=1, r=0.1, sa=10)
    cmds.move(length/2 + 0.5, height + stairs/2 + 1, i)
    cmds.duplicate()
    cmds.move(length/2 + 0.5, height + stairs/2 + 1, i - 0.15)
    cmds.duplicate()
    cmds.move(length/2 + 0.5, height + stairs/2 + 1, i + 0.15)

    cmds.duplicate()
    cmds.move(-length/2 - 0.5, height + stairs/2 + 1, i)
    cmds.duplicate()
    cmds.move(-length/2 - 0.5, height + stairs/2 + 1, i - 0.15)
    cmds.duplicate()
    cmds.move(-length/2 - 0.5, height + stairs/2 + 1, i + 0.15)

# ======================
# draw roof
# ======================
roof = cmds.polyPrism(l=length + 1.5, w=width + 1.5)
cmds.move(0, 0, 0, roof[0]+".scalePivot",roof[0]+".rotatePivot", absolute=True)
cmds.rotate(0, 0, 90)
cmds.scale(0.2, 1, 1);
cmds.move(0, height + stairs/2 + 0.85 + (width + 1.5)/2*0.2, 0)

# ======================
# #draw stairs
# ======================
for i in range(stairs, 0, -1):
    cmds.polyCube(h= 0.5, width=length + i + 1, depth=width + i + 1)
    cmds.move(0, (stairs/2 - i * 0.5) + 0.25, 0);