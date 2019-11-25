# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# python
import weakref
from functools import partial

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


class Template_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        template = Template()

        #Create tool instance
        self.copyAnimLayer = CopyAnimLayer()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Template")

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
        self.copy_anim_layer = uiMod.push_button(label = "Copy Anim Layer", size=(self.w[6], self.h[1]))
        self.copy_anim_layer.clicked.connect(self.on_copy_anim_layer_clicked)
        self.main_layout.addWidget(self.copy_anim_layer, 1, 0, 1, 6)

        return self.frame_widget


class Template(object):

    def __init__(self):
        if G.template:
            return
        G.template = self
