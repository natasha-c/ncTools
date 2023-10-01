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


class ToggleTangents_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        toggleTangents = ToggleTangents()

        #Create tool instance
        self.copyAnimLayer = CopyAnimLayer()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "ToggleTangents")

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
        return self.frame_widget


class ToggleTangents(object):

    def __init__(self):
        if G.ncToolbox.toggleTangents:
            return
        G.ncToolbox.toggleTangents = self


    def toggle_tangents(self):
