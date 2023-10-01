# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
import maya.cmds as cmds

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# ncTools
from ncTools.mods                   import uiMod;   reload(uiMod)
from ncTools.tools.ncToolboxGlobals import ncToolboxGlobals as G

BUTTONS = {"1s"         :       "G.bakeKeys.bake_1",
           "2s"         :       "G.bakeKeys.bake_2",
           "3s"         :       "G.bakeKeys.bake_3",
           "4s"         :       "G.bakeKeys.bake_4"
           }

print BUTTONS
class BakeKeysToolbar(uiMod.TemplateToolbarBase):

    def create_layout(self):
        G.bakeKeys = BakeKeys()
        self.add_buttons(BUTTONS)
        return self.widget


class BakeKeys(object):

    def __init__(self):
        pass

    def bake_1(self):
        print "BUTTON 1"
        """
        bakeResults -sampleBy 1 -oversamplingRate 1 -preserveOutsideKeys 1 -sparseAnimCurveBake 0;
        """
        self.bake(sample=1)
    def bake_2(self):
        print "BUTTON 2"

    def bake_3(self):
        print "BUTTON 3"

    def bake_4(self):
        print "BUTTON4"

    def bake(self, sample=1):
        cmds.bakeResults(sampleBy=sample, oversamplingRate=1, )
