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

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

class RigSettings_UI(uiMod.BaseSubUI):

    def create_layout(self):
        rigSettings = RigSettings()

        # Create tools instance
        self.rigSettings = RigSettings()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Rig Settings")

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
        self.quick_select = uiMod.label(label="Quick Select", size = (self.w[6], self.h[1]), h_adjust=10, align="center")
        self.main_layout.addWidget(self.quick_select, 2, 0, 1, 6)

        self.select_rigs = uiMod.push_button(label="All Rigs", size = (self.w[3], self.h[1]))
        self.select_rigs.clicked.connect(self.on_select_rigs_clicked)
        self.main_layout.addWidget(self.select_rigs, 3, 0, 1, 3)

        self.select_all_controls = uiMod.push_button(label="All Controls", size = (self.w[3], self.h[1]))
        self.select_all_controls.clicked.connect(self.on_select_all_controls_clicked)
        self.main_layout.addWidget(self.select_all_controls, 3, 3, 1, 3)

        self.global_control= uiMod.push_button(label="Global", size=(self.w[2], self.h[1]))
        self.global_control.clicked.connect(self.on_global_control_clicked)
        self.main_layout.addWidget(self.global_control, 4, 0, 1, 2)

        self.display_control= uiMod.push_button(label="Display", size=(self.w[2], self.h[1]))
        self.display_control.clicked.connect(self.on_display_control_clicked)
        self.main_layout.addWidget(self.display_control, 4, 2, 1, 2)

        self.ikfk_control= uiMod.push_button(label="IK FK", size=(self.w[2], self.h[1]))
        self.ikfk_control.clicked.connect(self.on_ikfk_control_clicked)
        self.main_layout.addWidget(self.ikfk_control, 4, 4, 1, 2)

        self.rig_speed = uiMod.label(label="Rig Speed", size = (self.w[6], self.h[1]), h_adjust=10, align="center")
        self.main_layout.addWidget(self.rig_speed, 5, 0, 1, 6)

        self.fast_speed= uiMod.push_button(label="Fast", size=(self.w[2], self.h[1]))
        self.fast_speed.clicked.connect(self.on_fast_speed_clicked)
        self.main_layout.addWidget(self.fast_speed, 6, 0, 1, 2)

        self.medium_speed= uiMod.push_button(label="Medium", size=(self.w[2], self.h[1]))
        self.medium_speed.clicked.connect(self.on_medium_speed_clicked)
        self.main_layout.addWidget(self.medium_speed, 6, 2, 1, 2)

        self.slow_speed= uiMod.push_button(label="Slow", size=(self.w[2], self.h[1]))
        self.slow_speed.clicked.connect(self.on_slow_speed_clicked)
        self.main_layout.addWidget(self.slow_speed, 6, 4, 1, 2)

        return self.frame_widget

    def on_global_control_clicked(self):
        self.rigSettings.select_control("global")

    def on_display_control_clicked(self):
        self.rigSettings.select_control("globalDisplayToggle")

    def on_ikfk_control_clicked(self):
        self.rigSettings.select_control("globalIkFkToggle")

    def on_select_rigs_clicked(self):
        self.rigSettings.select_all_rigs()

    def on_select_all_controls_clicked(self):
        self.rigSettings.select_all_controls()

    def on_fast_speed_clicked(self):
        self.rigSettings.set_rig_speed(0)

    def on_medium_speed_clicked(self):
        self.rigSettings.set_rig_speed(1)

    def on_slow_speed_clicked(self):
        self.rigSettings.set_rig_speed(2)

# -----------------------------------------------------------------------------
# Tool Functions
# -----------------------------------------------------------------------------
class RigSettings(object):

    def __init__(self):
        if G.rigSettings:
            return
        G.rigSettings = self

    def set_rig_speed(self, speed):
        for rig in animMod.get_target(target="rigs", selected=True):
            global_control = animMod.get_target(target="control_name", node=rig, control_name="global", selected=True)
            cmds.setAttr(global_control + ".modelDisplayLevel", speed)

    def select_control(self, control_name):
        selected_rig = animMod.get_target(target="rigs", selected=True)
        controls = []
        for rig in animMod.get_target(target="rigs", selected=True):
            control = animMod.get_target(target="control_name", control_name=control_name, node=rig)
            controls.append(control)
        cmds.select(controls)

    def select_all_rigs(self):
        all_rigs = animMod.get_target(target="rigs", selected=False)
        cmds.select(all_rigs)

    def select_all_controls(self):
        selected_rigs = animMod.get_target(target="rigs", selected=True)
        print selected_rigs
        all_rig_controls = []
        for rig in selected_rigs:
            all_controls = animMod.get_target(target="controls", selected=False, node=rig) or []
            all_rig_controls = all_rig_controls + all_controls
        cmds.select(all_rig_controls)
