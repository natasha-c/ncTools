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

BUTTONS = {"Button1"        :       "G.templateTools.button_1",
           "Button2"        :       "G.templateTools.button_2",
           "Button3"        :       "G.templateTools.button_3"
           }


class TemplateToolbar(TemplateToolbarBase):

    def create_layout(self):
        G.templateTools = TemplateTools()
        self.add_buttons(BUTTONS)
        return self.widget


class TemplateTools(object):

    def __init__(self):
        pass

    def button_1(self):
        print "BUTTON 1"

    def button_2(self):
        print "BUTTON 2"

    def button_3(self):
        print "BUTTON 3"
