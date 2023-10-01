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


class MirrorAnim_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        mirrorAnim = MirrorAnim()

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
        self.mirror_single_frame = uiMod.push_button(label="Single Frame", size=(self.w[6], self.h[1]))
        self.mirror_single_frame.clicked.connect(G.mirrorAnim.mirror_single_frame)
        self.main_layout.addWidget(self.mirror_single_frame, 1, 0, 1, 6)

        self.mirror_single_frame = uiMod.push_button(label="Selected Frames", size=(self.w[6], self.h[1]))
        self.mirror_single_frame.clicked.connect(G.mirrorAnim.mirror_single_frame)
        self.main_layout.addWidget(self.mirror_single_frame, 2, 0, 1, 6)

        self.mirror_single_frame = uiMod.push_button(label="All Frames", size=(self.w[6], self.h[1]))
        self.mirror_single_frame.clicked.connect(G.mirrorAnim.mirror_single_frame)
        self.main_layout.addWidget(self.mirror_single_frame, 3, 0, 1, 6)

        return self.frame_widget

class MirrorAnim(object):

    def __init__(self):
        G.mirrorAnim = self

    def mirror_single_frame(self):
        print "Mirror frame"
        controls = animMod.get_controls(selected=True)
        selected_frames = animMod.get_frames(selected=True)
        for control in controls:
            target_control = animMod.get_opposite_control(node=control)
            attributes = animMod.get_target("attributes", attribute_options=["unlocked", "c", "keyable"], node=control) or []
            for attribute in attributes:
                for frame in selected_frames:
                    current_key = cmds.copyKey(control, time=(frame, frame), at=attribute, option="keys")
                    if current_key > 0:
                        cmds.setKeyframe(target_control, at=attribute)
                        cmds.pasteKey(target_control, option="replaceCompletely")

    def mirror_animation(self):
        """
        Mirrors the animation based on the selected controls, selected anim layer(if any) and selected selected frames
        """
        controls = animMod.get_target("controls", selected=True)
        selected_frames = animMod.get_target("frames", selected=True)
        anim_layers = animMod.get_target("anim_layers", selected=True)
        if len(anim_layers) > 0:
            for anim_layer in anim_layers:
                for control in controls:
                    target_control = animMod.get_target("opposite_control", node=control)
                    attributes = animMod.get_target("attributes", attribute_options=["unlocked", "c", "keyable"], node=control) or []
                    for attribute in attributes:
                        for frame in selected_frames:
                            current_key = cmds.copyKey(control, time=(frame, frame), at=attribute, option="keys")
                            if current_key > 0:
                                cmds.animLayer(anim_layer, edit=True, at="{0}.{1}".format(target_control, attribute))
                                cmds.setKeyframe(target_control, time=(frame,frame), at=attribute, al=anim_layer)
                                cmds.pasteKey(target_control, time=(frame, frame), option="replaceCompletely", al=anim_layer)
        else:
            for control in controls:
                target_control = animMod.get_target("opposite_control", node=control)
                attributes = animMod.get_target("attributes", attribute_options=["unlocked", "c", "keyable"], node=control) or []
                for attribute in attributes:
                    for frame in selected_frames:
                        current_key = cmds.copyKey(control, time=(frame, frame), at=attribute, option="keys")
                        if current_key > 0:
                            cmds.setKeyframe(target_control, time=(frame), at=attribute)
                            cmds.pasteKey(target_control, animation="keysOrObjects", option="replace")





    def mirror_anim_layer(self):
        print "Mirror"
        controls = animMod.get_target("controls", selected=True)
        source_anim_layers = animMod.get_target("anim_layers", selected=True)
        for anim_layer in source_anim_layers:
            for control in controls:
                target_control = animMod.get_target("opposite_control", node=control)
                attributes = animMod.get_target("attributes", attribute_options=["unlocked", "c", "keyable"], node=control) or []

                for attribute in attributes:
                    #Is it in the source layer?
                    if not animMod.is_control_in_anim_layer(control, anim_layer):
                        print "Not in layer"
                        pass

                    else:
                        #Are there cures on the attribute?
                        anim_curves = cmds.copyKey(control, time = [], at=attribute, option="curve", animLayer=anim_layer)

                        if anim_curves > 0:

                            #Add target control to layer
                            cmds.animLayer(anim_layer, edit=True, at="{0}.{1}".format(target_control, attribute))
                            cmds.setKeyframe(target_control, at=attribute, al=anim_layer)
                            cmds.pasteKey(target_control, option="replaceCompletely", al=anim_layer)
