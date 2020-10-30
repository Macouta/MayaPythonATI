import maya.cmds as cmds
import functools as func


class TempleGenerator:
    def __init__(self):
        self.columnsX = 10
        self.columnsY = 10
        self.columnsHeight = 8
        self.step = 2

        self.stairsEnabled = True
        self.stairsHeight = 0.5
        self.stairsNb = 4
        self.stairsGrowth = 1.0

    def updateValues(self, UI):
        self.columnsX = cmds.intSliderGrp(UI.columnsX, q=True, v=True)
        self.columnsY = cmds.intSliderGrp(UI.columnsY, q=True, v=True)
        self.columnsHeight = cmds.intSliderGrp(
            UI.columnsHeight, q=True, v=True)
        self.step = cmds.intSliderGrp(UI.step, q=True, v=True)

        self.stairsEnabled = cmds.checkBoxGrp(
            UI.stairsEnabled, q=True, v1=True)

        self.stairsHeight = cmds.floatSliderGrp(
            UI.stairsHeight, q=True, v=True)
        self.stairsNb = cmds.intSliderGrp(UI.stairsNb, q=True, v=True)
        self.stairsGrowth = cmds.floatSliderGrp(
            UI.stairsGrowth, q=True, v=True)

    def generate(self, UI):
        self.updateValues(UI)

        templeArr = []
        # PILLAR ========================================================
        pillarArr = []
        pillarArr += cmds.polyCube(n="BottomCube", h=0.1)
        cmds.move(0, 0.05, 0)

        pillarArr += cmds.polyCube(n="BottomCube2", h=0.15, w=0.9, d=0.9)
        cmds.move(0, 0.1, 0)

        pillarArr += cmds.polyCylinder(n="BottomCyl", h=0.3, r=0.40, sa=10)
        cmds.move(0, 0.30, 0)

        pillarArr += cmds.polyCylinder(n="BodyCyl",
                                       h=self.columnsHeight, r=0.35, sa=10)
        cmds.move(0, self.columnsHeight/2.0, 0)

        pillarArr += cmds.polyCylinder(n="TopCyl", h=0.3, r=0.40, sa=10)
        cmds.move(0, self.columnsHeight - 0.30, 0)

        pillarArr += cmds.polyCube(n="TopRect", h=0.15, w=0.9, d=0.9)
        cmds.move(0, self.columnsHeight - 0.1, 0)

        pillarArr += cmds.polyCube(n="TopRect2", h=0.1)
        cmds.move(0, self.columnsHeight - 0.05, 0)

        pillar = cmds.group(*pillarArr, n="pillar")

        # VALUES =========================================================
        stairsZ = (0.5, self.stairsNb * self.stairsHeight)[self.stairsEnabled]

        templeLenght = (self.columnsX - 1) * self.step
        templeWidth = (self.columnsY - 1) * self.step

        # PILLARS LENGTH =================================================
        for i in range(-templeLenght/2, templeLenght/2 + 1, self.step):
            pillarLeft = cmds.instance(pillar)
            pillarRight = cmds.instance(pillar)
            templeArr += pillarLeft
            templeArr += pillarRight
            cmds.move(i, stairsZ, -templeWidth/2, pillarLeft)
            cmds.move(i, stairsZ, templeWidth/2, pillarRight)

        # PILLARS WIDTH ==================================================
        for i in range(-templeWidth/2 + self.step, templeWidth/2 + 1 - self.step, self.step):
            pillarTop = cmds.instance(pillar)
            pillarBack = cmds.instance(pillar)
            templeArr += pillarTop
            templeArr += pillarBack
            cmds.move(-templeLenght/2, stairsZ, i, pillarTop)
            cmds.move(templeLenght/2, stairsZ, i, pillarBack)

        # STAIRS =========================================================
        if(self.stairsEnabled):
            for i in range(self.stairsNb, 0, -1):
                templeArr += cmds.polyCube(h=self.stairsHeight,
                                           width=templeLenght + 1 + i * self.stairsGrowth,
                                           depth=templeWidth + 1 + i * self.stairsGrowth)
                stairPos = self.stairsHeight/2 + \
                    (stairsZ - i * self.stairsHeight)
                cmds.move(0, stairPos, 0)
        else:
            templeArr += cmds.polyCube(h=0.5, width=templeLenght + 2, depth=templeWidth + 2)
            cmds.move(0, 0.25, 0)

        cmds.hide(pillar)

        cmds.group(*templeArr, n="Temple")


class UI:
    def __init__(self, id):
        self.generator = TempleGenerator()

        if cmds.window('window1', ex=True):
            cmds.deleteUI('window1', window=True)

        if cmds.uiTemplate('templeTemplate', exists=True):
            cmds.deleteUI('templeTemplate', uiTemplate=True)

        cmds.uiTemplate("templeTemplate")
        cmds.frameLayout(dt="templeTemplate", cll=True, bgc=[0.2, 0.2, 0.2])

        w = cmds.window(title=id,
                        sizeable=False, resizeToFitChildren=True)

        cmds.setUITemplate('templeTemplate', pushTemplate=True)

        cmds.rowColumnLayout(numberOfColumns=1, co=(1, "both", 15))

        cmds.text(label="Temple Generator", al="center", h=30)

        # =========================================================
        # BASE
        # =========================================================
        cmds.frameLayout(label='Base')
        cmds.columnLayout(adj=True)
        self.columnsX = cmds.intSliderGrp(field=True, label='Number of columns X',
                                          min=2, value=self.generator.columnsX,
                                          cal=(1, "left"))
        self.columnsY = cmds.intSliderGrp(field=True, label='Number of columns Y',
                                          min=2, value=self.generator.columnsY,
                                          cal=(1, "left"))
        self.columnsHeight = cmds.intSliderGrp(field=True, label='Height of columns',
                                               min=6, max=12, value=self.generator.columnsHeight,
                                               cal=(1, "left"))
        self.step = cmds.intSliderGrp(field=True, label='Step between columns',
                                      min=2, max=10, value=self.generator.step,
                                      cal=(1, "left"))

        cmds.setParent('..')
        cmds.setParent('..')
        cmds.separator(style="none", h=10)

        # =========================================================
        # PILLAR
        # =========================================================
        cmds.frameLayout(label='Pillar')
        cmds.columnLayout(adj=True)

        cmds.setParent('..')
        cmds.setParent('..')
        cmds.separator(style="none", h=10)

        # =========================================================
        # STAIRS
        # =========================================================
        cmds.frameLayout(label='Stairs')
        cmds.columnLayout(adj=True)

        self.stairsHeight = cmds.floatSliderGrp(field=True, label='stairs height',
                                                min=0.2, max=3.0, value=self.generator.stairsHeight,
                                                cal=(1, "left"))

        self.stairsNb = cmds.intSliderGrp(field=True, label='Number of stairs',
                                          min=1, max=25, value=self.generator.stairsNb,
                                          cal=(1, "left"))
        self.stairsGrowth = cmds. floatSliderGrp(field=True, label='stairs growth',
                                                 min=1.0, max=3.0, value=self.generator.stairsGrowth,
                                                 cal=(1, "left"))

        if(not self.generator.stairsEnabled):
            self.toggle(self.stairsHeight, self.stairsNb)

        self.stairsEnabled = cmds.checkBoxGrp(ncb=1, l1="Enable stairs", v1=self.generator.stairsEnabled, cal=(1, "left"),
                                              ofc=func.partial(
                                                  self.toggle, self.stairsHeight, self.stairsNb, self.stairsGrowth),
                                              onc=func.partial(self.toggle, self.stairsHeight, self.stairsNb, self.stairsGrowth))

        cmds.setParent('..')
        cmds.setParent('..')
        cmds.separator(style="none", h=10)

        # =========================================================
        # ROOF
        # =========================================================
        cmds.frameLayout(label='Roof')
        cmds.columnLayout(adj=True)
        cmds.checkBoxGrp(ncb=1, l1="Enable roof decorations", v1=True, cal=(1, "left"),
                         ofc="", onc="")
        cmds.intSliderGrp(field=True, label='Number of decorations',
                          min=1, value=3, cal=(1, "left"))
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.separator(style="none", h=10)

        cmds.columnLayout(adjustableColumn=True,
                          columnAttach=('both', 5), rowSpacing=10)
        cmds.button(l="Generate new temple", c=self.generate, align="center")
        cmds.button(l="Regenerate temple", c=self.generate, align="center")
        cmds.setParent('..')
        cmds.separator(style="none", h=10)  # indentation

        cmds.showWindow()

    def generate(self, *args):
        self.generator.generate(self)

    @staticmethod
    def toggle(*args):
        for slider in args:
            isFloatGroup = cmds.floatSliderGrp(slider, q=True, ex=True)
            isIntGroup = cmds.intSliderGrp(slider, q=True, ex=True)
            if (isFloatGroup):
                value = cmds.floatSliderGrp(slider, q=True, en=True)
                cmds.floatSliderGrp(slider, e=True, en=not value)
            elif (isIntGroup):
                value = cmds.intSliderGrp(slider, q=True, en=True)
                cmds.intSliderGrp(slider, e=True, en=not value)


cmds.file(f=True, new=True)

window = UI("Temple Generator")
