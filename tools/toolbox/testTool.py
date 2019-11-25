# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets

# ncTools
from ncTools.mods                   import uiMod;   reload(uiMod)
from ncTools.mods                   import animMod; reload(animMod)
from ncTools.tools.ncToolboxGlobals   import ncToolboxGlobals as G



class TestTool_UI(uiMod.BaseSubUI):


    def create_layout(self):

        testTool = TestTool()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text="Test Tools")

        # Create main widget
        self.main_widget = QtWidgets.QWidget()
        # Add widget to frame
        self.frame_widget.addWidget(self.main_widget)
        # Create main widget layout
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setSpacing(self.spacing)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # Add layout to widget
        self.main_widget.setLayout(self.main_layout)

        # Create buttons
        button_label = "a"
        button_size = (self.w[1], self.h[1])
        connect = "G.ncToolsUIs['testTool'].start_a"
        button_context_menu = {"start": "start_a",
                               "stop": "start_a",
                               "options": "start_a",
                               "hotkey": "start_a"}

        print button_label, button_size, connect, button_context_menu



        self.button_a = uiMod.push_button(label = "a",
                                          size = (self.w[1], self.h[1]),
                                          connect="G.ncToolsUIs['testTool'].start_a",
                                          tool_tip="Will print 'a'",
                                          status_tip="press the button",
                                          context_menu={"start": "G.ncToolsUIs['testTool'].start_a",
                                                        "stop": "G.ncToolsUIs['testTool'].start_a",
                                                        "options": "G.ncToolsUIs['testTool'].start_a",
                                                        "hotkey": "G.ncToolsUIs['testTool'].start_a"}

                                          )
        self.main_layout.addWidget(self.button_a, 1, 0, 1, 1)
        """self.button_b = uiMod.push_button(label = "b", size = (self.w[1], self.h[1]))
        self.main_layout.addWidget(self.button_b, 1, 1, 1, 1)
        self.button_c = uiMod.push_button(label = "c", size = (self.w[1], self.h[1]))
        self.main_layout.addWidget(self.button_c, 1, 2, 1, 1)
        self.button_d = uiMod.push_button(label = "d", size = (self.w[1], self.h[1]))
        self.main_layout.addWidget(self.button_d, 1, 3, 1, 1)
        self.button_e = uiMod.push_button(label = "e", size = (self.w[1], self.h[1]))
        self.main_layout.addWidget(self.button_e, 1, 4, 1, 1)
        self.button_f = uiMod.push_button(label = "f", size = (self.w[1], self.h[1]))
        self.main_layout.addWidget(self.button_f, 1, 5, 1, 1)

        self.button_1 = uiMod.push_button(label = "1", size = (self.w[2], self.h[1]))
        self.main_layout.addWidget(self.button_1, 2, 0, 1, 2)
        self.button_2 = uiMod.push_button(label = "2", size = (self.w[2], self.h[1]))
        self.main_layout.addWidget(self.button_2, 2, 2, 1, 2)
        self.button_3 = uiMod.push_button(label = "3", size = (self.w[2], self.h[1]))
        self.main_layout.addWidget(self.button_3, 2, 4, 1, 2)

        self.button_a = uiMod.push_button(label = "a", size = (self.w[3], self.h[1]))
        self.main_layout.addWidget(self.button_a, 3, 0, 1, 3)
        self.button_b = uiMod.push_button(label = "b", size = (self.w[3], self.h[1]))
        self.main_layout.addWidget(self.button_b, 3, 3, 1, 3)

        self.button_full = uiMod.push_button(label = "full", size = (self.w[6], self.h[1]))
        self.main_layout.addWidget(self.button_full, 4, 0, 1, 6)"""

        return self.frame_widget

    def start_a(self):
        print "clicked a"

class TestTool():

    def __init__(self):

        if G.testTool:
            return
        G.testTool = self

    def print_this(self):
        print 'this'
