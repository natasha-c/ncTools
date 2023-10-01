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
        self.mirror_single_frame = uiMod.push_button(label="Single Frame", size=(self.w[6], self.h[1]))
        self.mirror_single_frame.clicked.connect(G.mirrorAnim.mirror_animation)
        self.main_layout.addWidget(self.mirror_single_frame, 1, 0, 1, 6)

        self.mirror_animation_selected_frames = uiMod.push_button(label="Selected Frames", size=(self.w[6], self.h[1]))
        self.mirror_animation_selected_frames.clicked.connect(G.mirrorAnim.mirror_animation)
        self.main_layout.addWidget(self.mirror_animation_selected_frames, 2, 0, 1, 6)


        self.negative_translate = uiMod.push_button(label="Negative Translate", size=(self.w[6], self.h[1]))
        self.negative_translate.clicked.connect(G.mirrorAnim.negative_translate)
        self.main_layout.addWidget(self.negative_translate, 2, 0, 1, 6)

        self.negative_rotate = uiMod.push_button(label="Negative Rotate", size=(self.w[6], self.h[1]))
        self.negative_rotate.clicked.connect(G.mirrorAnim.negative_rotate)
        self.main_layout.addWidget(self.negative_rotate, 3, 0, 1, 6)


        return self.frame_widget

class MirrorAnim(object):

    def __init__(self):
        G.mirrorAnim = self

    def mirror_single_frame(self):
        controls = animMod.get_controls(selected=True)
        anim_layers = animMod.get_anim_layers(selected=True)
        current_frame = animMod.get_start_current_end_frame()[1]
        print current_frame
        if len(anim_layers) > 0:
            for anim_layer in anim_layers:
                for control in controls:
                    opposite_control = animMod.get_opposite_control(node=control)
                    attributes = animMod.get_attributes(node=control, attribute_options=["unlocked", "c", "keyable"]) or []
                    for attribute in attributes:
                            current_key = cmds.copyKey(control, time=(current_frame, current_frame), at=attribute, option="keys")
                            if current_key > 0:
                                print current_key
                                cmds.animLayer(anim_layer, edit=True, at="{0}.{1}".format(opposite_control, attribute))
                                cmds.setKeyframe(opposite_control, time=(current_frame,current_frame), at=attribute, al=anim_layer)
                                cmds.pasteKey(opposite_control, time=(current_frame, current_frame), option="merge", al=anim_layer)
                                print "Mirrored"


    def mirror_animation(self):
        """
        Mirrors the animation based on the selected controls, selected anim layer(if any) and selected selected frames
        """
        cmds.undoInfo(openChunk=True)
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
                            current_key = cmds.copyKey(control, time=(frame, frame), at=attribute, option="keys")
                            if current_key > 0:
                                cmds.animLayer(anim_layer, edit=True, at="{0}.{1}".format(opposite_control, attribute))
                                cmds.setKeyframe(opposite_control, time=(frame,frame), at=attribute, al=anim_layer)
                                cmds.pasteKey(opposite_control, time=(frame, frame), option="replaceCompletely", al=anim_layer)
                                print "Mirrored"
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
        cmds.undoInfo(closeChunk=True)

    def negative_attribute(self, attribute):
        "Use to apply negative fix to mirrored values" 
        controls = animMod.get_controls(selected=True)
        for control in controls: 
            print "making negative" 

            for axis in ["X", "Y", "Z"]:
                control_attr = "{0}.{1}{2}".format(control, attribute, axis)
                try:
                    attr = cmds.getAttr(control_attr)
                    negative_attr = -attr
                    cmds.setAttr(control_attr, negative_attr)
                except:
                    pass
    
    def negative_translate(self):
        cmds.undoInfo(openChunk=True)
        self.negative_attribute(attribute="translate")
        cmds.undoInfo(closeChunk=True)

        
    def negative_rotate(self):
        cmds.undoInfo(openChunk=True)
        self.negative_rotate(attribute="rotate")
        cmds.undoInfo(closeChunk=True)