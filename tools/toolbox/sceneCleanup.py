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

# dsdb
import dsdb_animation
import dsdb_utils
import dsdb_pyside


class SceneCleanup_UI(uiMod.BaseSubUI):

    def create_layout(self):
        #Create tool instance
        sceneCleanup = SceneCleanup()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Cleanup Scene")

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
        self.bake_all_layers = uiMod.push_button(label = "Bake All Layers", size=(self.w[6], self.h[1]))
        self.bake_all_layers.clicked.connect(G.sceneCleanup.bake_all_layers)
        self.main_layout.addWidget(self.bake_all_layers, 1, 0, 1, 6)

        
        self.bake_selected_rig = uiMod.push_button(label = "Bake Selected Rig", size=(self.w[6], self.h[1]))
        self.bake_selected_rig.clicked.connect(G.sceneCleanup.bake_selected_rig)
        self.main_layout.addWidget(self.bake_selected_rig, 2, 0, 1, 6)
        """
        self.paste_pose = uiMod.push_button(label = "Paste Pose", size=(self.w[6], self.h[1]))
        self.paste_pose.clicked.connect(G.sceneCleanup.paste_pose)
        self.main_layout.addWidget(self.paste_pose, 3, 0, 1, 6)

        self.hands_to_fingers= uiMod.push_button(label = "Hands To Fingers", size=(self.w[6], self.h[1]))
        self.hands_to_fingers.clicked.connect(G.sceneCleanup.hands_to_fingers)
        self.main_layout.addWidget(self.hands_to_fingers, 4, 0, 1, 6)
        """
        return self.frame_widget






class SceneCleanup(object):

    def __init__(self):
        G.sceneCleanup = self

    @dsdb_utils.disableViewport
    @animMod.undo_chunk
    def bake_all_layers(self):
        print "Bake All Layers"
        dsdb_animation.core.merge_layers()
    @dsdb_utils.disableViewport
    @animMod.undo_chunk
    def bake_selected_rig(self):
        print "Bake selected rig controls"
        # Get selected player from Asset Manager 

        # Select all rig controls 

        # Check if any have constraints

        # Bake those controls 
"""
    def set_worldspace_default(self):
        # Get selected player from Asset Manager 

        # Check space for each control

        # If space not default bake to default"""








    
