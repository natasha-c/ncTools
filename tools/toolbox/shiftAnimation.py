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
from PySide2 import QtGui

# ncTools
from ncTools.mods                   import uiMod;   reload(uiMod)
from ncTools.mods                   import animMod; reload(animMod)
from ncTools.tools.ncToolboxGlobals   import ncToolboxGlobals as G

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

class ShiftAnimation_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        shiftAnimation = ShiftAnimation()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Shift Animation")

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
        self.absolute_radio = uiMod.radio_button(label = "Absolute", size=(self.w[3], self.h[1]))
        self.absolute_radio.clicked.connect(lambda : setattr(shiftAnimation, "relative", False))
        self.main_layout.addWidget(self.absolute_radio, 1, 0, 1, 3)

        self.relative_radio = uiMod.radio_button(label = "Relative", size=(self.w[3], self.h[1]))
        self.relative_radio.setChecked(True)
        self.relative_radio.clicked.connect(lambda : setattr(shiftAnimation, "relative", True))
        self.main_layout.addWidget(self.relative_radio, 1, 3, 1, 3)

        self.all_left = uiMod.push_button(label="<<", size=(self.w[1], self.h[1]))
        self.all_left.clicked.connect(partial(shiftAnimation.shift, all_keys=True, forward=False))
        self.main_layout.addWidget(self.all_left, 2, 0, 1, 1)

        self.frame_left = uiMod.push_button(label="<", size=(self.w[1], self.h[1]))
        self.frame_left.clicked.connect(partial(shiftAnimation.shift, all_keys=False, forward=False))
        self.main_layout.addWidget(self.frame_left, 2, 1, 1, 1)

        self.number_box = uiMod.line_edit(size=(self.w[2], self.h[1]))
        #self.number_box.setText(str(shiftAnimation.frame_number))
        self.number_box.setValidator(QtGui.QIntValidator())
        self.number_box.editingFinished.connect(lambda : setattr(shiftAnimation, "frame_number", self.number_box.text()))
        self.main_layout.addWidget(self.number_box, 2, 2, 1, 2)

        self.frame_right = uiMod.push_button(label=">", size=(self.w[1], self.h[1]))
        self.frame_right.clicked.connect(partial(shiftAnimation.shift, all_keys=False, forward=True))
        self.main_layout.addWidget(self.frame_right, 2, 4, 1, 1)

        self.all_right = uiMod.push_button(label=">>", size=(self.w[1], self.h[1]))
        self.all_right.clicked.connect(partial(shiftAnimation.shift, all_keys=True, forward=True))
        self.main_layout.addWidget(self.all_right, 2, 5, 1, 1)

        return self.frame_widget


# -----------------------------------------------------------------------------
# Tool
# -----------------------------------------------------------------------------

class ShiftAnimation(object):


    def __init__(self):
        if G.shiftAnimation:
            return
        G.shiftAnimation = self

        # Variables
        self.relative = True
        self.frame_number = 1

    def shift(self, all_keys=True, forward=True):
        cmds.undoInfo(openChunk=True)

        controls = cmds.ls(sl=True)
        current_frame = int(animMod.get_timeline_frame())
        frame = int(self.frame_number)

        if self.relative == True:
            time_change = frame
            if forward == False:
                time_change = -1*time_change
            target_frame = current_frame + time_change
        else:
            time_change = frame - current_frame
            target_frame = frame


        for control in controls:
            if all_keys == True:
                cmds.keyframe(control, edit=True, animation="objects", includeUpperBound=True, relative=True, timeChange=time_change, option="over")

            else:
                selected_keys = animMod.get_target("frames", node=control, selected=True)
                cmds.keyframe(control, edit=True, time=(selected_keys[0], selected_keys[-1]), relative=True, timeChange=time_change, option="over")

        cmds.currentTime(target_frame)

        cmds.undoInfo(closeChunk=True)
