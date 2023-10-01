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



class WorldspaceSnap_UI(uiMod.BaseSubUI):


    def create_layout(self):

        worldspaceSnap = WorldspaceSnap()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text="Worldspace Snap")

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
        row = 0
        row += 1
        self.snap_selected = uiMod.push_button(label="Snap All", size=(self.w[6], self.h[1]))
        self.snap_selected.clicked.connect(lambda: worldspaceSnap.snap(all=True))
        self.main_layout.addWidget(self.snap_selected, row, 0, 1, 6)

        row += 1
        self.snap_translate = uiMod.push_button(label="Snap Translate", size=(self.w[6], self.h[1]))
        self.snap_translate.clicked.connect(lambda: worldspaceSnap.snap(translation=True))
        self.main_layout.addWidget(self.snap_translate, row, 0, 1, 6)

        row += 1
        self.snap_rotate = uiMod.push_button(label="Snap Rotate", size=(self.w[6], self.h[1]))
        self.snap_rotate.clicked.connect(lambda: worldspaceSnap.snap(rotation=True))
        self.main_layout.addWidget(self.snap_rotate, row, 0, 1, 6)

        return self.frame_widget


class WorldspaceSnap():

    def __init__(self):
        G.WorldspaceSnap = self

    def snap(self, translation=False, rotation=False, all=False):
        """
        Procedure that retrieves the xform position of the first selected object
        and applies it to the rest of the selected objects
        """
        print "Translation:", translation, "Rotation:", rotation
        # Get the selection - the first selected object is the parent
        selection = cmds.ls(sl=True)
        source = selection.pop(0)
        targets = selection
        # Get the xform position of the source object
        source_translate = cmds.xform(source, query=True, ws=True, t=True)
        source_rotation = cmds.xform(source, query=True, ws=True, ro=True)
        source_matrix = cmds.xform(source, query=True, ws=True, m=True)
        # Depending on arguments apply xform to targets
        for target in targets:
            if translation==True:
                cmds.xform(target, ws=True, t=source_translate)
            if rotation==True:
                cmds.xform(target, ws=True, ro=source_rotation)
            if all==True:
                cmds.xform(target, ws=True, m=source_matrix)
















































        #
