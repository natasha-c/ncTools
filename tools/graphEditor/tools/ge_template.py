# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
import maya.cmds as cmds

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from ncTools.tools.ncToolboxGlobals import ncToolboxGlobals as G


buttons = {"Button1"        :       "G.templateTools.button_1()",
           "Button2"        :       "G.templateTools.button_2()",
           "Button3"        :       "G.templateTools.button_3()"
           }


class TemplateToolbar(QtWidgets.QWidget):

    def __init__(self):
        super(TemplateBar, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.add_buttons()

    def add_buttons(self):
        for button in buttons:
            label = button[0]
            command = button[1]
            push_button = uiMod.push_button(size=(25,25), label=label)
            push_button.clicked.connect(command)
            self.layout.addWidget(push_button)


class Template(object):

    def __init__(self):
        G.templateTools = self

    def button_1(self):
        print "BUTTON 1"

    def button_2(self):
        print "BUTTON 2"

    def button_3(self):
        print "BUTTON 3"
