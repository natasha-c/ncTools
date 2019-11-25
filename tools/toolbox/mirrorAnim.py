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
from ncTools.tools.ncToolboxGlobals import ncToolboxGlobals as G


class MirrorAnim_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        G.mirrorAnim = MirrorAnim()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Mirror Animation", base_width=self.w[1], base_height=self.h[1])

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
        self.mirror_single_frame = uiMod.push_button(label="Mirror Animation", size=(self.w[6], self.h[1]))
        self.mirror_single_frame.clicked.connect(G.mirrorAnim.mirror_animation)
        self.main_layout.addWidget(self.mirror_single_frame, 1, 0, 1, 6)


        return self.frame_widget

class MirrorAnim(object):

    def __init__(self):
        G.mirrorAnim = self

    def mirror_animation(self):
        """
        Mirrors the animation based on the selected controls, selected anim layer(if any) and selected selected frames
        """
        controls = animMod.get_controls(selected=True)
        selected_frames = animMod.get_frames()
        anim_layers = animMod.get_anim_layers(selected=True)
        if len(anim_layers) > 0:
            for anim_layer in anim_layers:
                for control in controls:
                    opposite_control = animMod.get_opposite_control(node=control)
                    attributes = animMod.get_attributes(node=control, attribute_options=["unlocked", "c", "keyable"]) or []
                    for attribute in attributes:
                        for frame in selected_frames:
                            if cmds.copyKey(control, time=(frame, frame), at=attribute, option="keys", al=anim_layer) != None:
                                cmds.animLayer(anim_layer, edit=True, at="{0}.{1}".format(opposite_control, attribute))
                                cmds.setKeyframe(opposite_control, time=(frame,frame), at=attribute, al=anim_layer)
                                cmds.pasteKey(opposite_control, time=(frame, frame), option="replaceCompletely", al=anim_layer)
        else:
            for control in controls:
                opposite_control = animMod.get_opposite_control(node=control)
                attributes = animMod.get_attributes(node=control, attribute_options=["unlocked", "c", "keyable"]) or []
                for attribute in attributes:
                    for frame in selected_frames:
                        current_key = cmds.copyKey(control, time=(frame, frame), at=attribute, option="keys")
                        if current_key > 0:
                            cmds.setKeyframe(opposite_control, time=(frame), at=attribute)
                            cmds.pasteKey(opposite_control, animation="keysOrObjects", option="replace")
