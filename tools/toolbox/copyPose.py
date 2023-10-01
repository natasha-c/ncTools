# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# python
import weakref
from functools import partial
from importlib import reload 


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



class CopyPose_UI(uiMod.BaseSubUI):

    def create_layout(self):
        copyPose = CopyPose()

        self.copyPose = CopyPose()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Copy Paste Pose")

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
        self.copy_pose = uiMod.push_button(label = "Copy Pose", size = (self.w[6], self.h[1]))
        self.copy_pose.clicked.connect(self.on_copy_pose_clicked)
        self.main_layout.addWidget(self.copy_pose, 0, 0, 1, 6)

        self.copy_animation = uiMod.push_button(label = "Copy Animation", size = (self.w[6], self.h[1]))
        self.copy_animation.clicked.connect(self.on_copy_animation_clicked)
        self.main_layout.addWidget(self.copy_animation, 1, 0, 1, 6)

        self.translate_label = uiMod.label(label = "Translate", size = (self.w[2], self.h[1]))
        self.main_layout.addWidget(self.translate_label, 2, 0, 1, 2)

        self.translate_all = uiMod.checkbox(label="All", size = (self.w[1], self.h[1]))
        self.translate_all.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="translate", axis="all"))
        self.main_layout.addWidget(self.translate_all, 2, 2, 1, 1)

        self.translate_x = uiMod.checkbox(label="X", size = (self.w[1], self.h[1]))
        self.translate_x.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="translate", axis="x"))
        self.main_layout.addWidget(self.translate_x, 2, 3, 1, 1)

        self.translate_y = uiMod.checkbox(label="Y", size = (self.w[1], self.h[1]))
        self.translate_y.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="translate", axis="y"))
        self.main_layout.addWidget(self.translate_y, 2, 4, 1, 1)

        self.translate_z = uiMod.checkbox(label="Z", size = (self.w[1], self.h[1]))
        self.translate_z.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="translate", axis="z"))
        self.main_layout.addWidget(self.translate_z, 2, 5, 1, 1)

        self.rotate_label = uiMod.label(label = "Rotate", size = (self.w[2], self.h[1]))
        self.main_layout.addWidget(self.rotate_label, 3, 0, 1, 2)

        self.rotate_all = uiMod.checkbox(label="All", size = (self.w[1], self.h[1]))
        self.rotate_all.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="rotate", axis="all"))
        self.main_layout.addWidget(self.rotate_all, 3, 2, 1, 1)

        self.rotate_x = uiMod.checkbox(label="X", size = (self.w[1], self.h[1]))
        self.rotate_x.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="rotate", axis="x"))
        self.main_layout.addWidget(self.rotate_x, 3, 3, 1, 1)

        self.rotate_y = uiMod.checkbox(label="Y", size = (self.w[1], self.h[1]))
        self.rotate_y.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="rotate", axis="y"))
        self.main_layout.addWidget(self.rotate_y, 3, 4, 1, 1)

        self.rotate_z = uiMod.checkbox(label="Z", size = (self.w[1], self.h[1]))
        self.rotate_z.clicked.connect(partial(self.on_checkbox_checked, translate_rotate="rotate", axis="z"))
        self.main_layout.addWidget(self.rotate_z, 3, 5, 1, 1)

        self.other_label = uiMod.label(label = "Other Attr", size = (self.w[2], self.h[1]))
        self.main_layout.addWidget(self.other_label, 4, 0, 1, 3)

        self.other_all = uiMod.checkbox(label="", size = (self.w[1], self.h[1]))
        self.main_layout.addWidget(self.other_all, 4, 2, 1, 1)

        self.paste_pose = uiMod.push_button(label="Paste Pose", size=(self.w[6], self.h[1]))
        self.paste_pose.clicked.connect(self.on_paste_pose_clicked)
        self.main_layout.addWidget(self.paste_pose, 5, 0, 1, 6)

        self.paste_animation = uiMod.push_button(label="Paste Animation", size=(self.w[6], self.h[1]))
        self.paste_animation.clicked.connect(self.on_paste_animation_clicked)
        self.main_layout.addWidget(self.paste_animation, 6, 0, 1, 6)

        self.default_checkbox_state()

        return self.frame_widget


    def default_checkbox_state(self):
        for attribute in ["translate", "rotate"]:
            all_checkbox = eval("self.{0}_all".format(attribute))
            all_checkbox.setCheckState(QtCore.Qt.Checked)
            for axis in ["x", "y", "z"]:
                axis_checkbox = eval("self.{0}_{1}".format(attribute, axis))
                axis_checkbox.setCheckState(QtCore.Qt.Checked)
                axis_checkbox.setEnabled(False)
        self.other_all.setCheckState(QtCore.Qt.Checked)


    def on_copy_pose_clicked(self):
        print "copy"
        self.source_rig = animMod.get_target("rigs", selected=True)[0]
        self.anim_data = self.copyPose.copy_pose(rig=self.source_rig)

    def on_copy_animation_clicked(self):
        self.source_rig = animMod.get_target("rigs", selected=True)[0]
        self.anim_data = self.copyPose.copy_animation(rig=self.source_rig)

    def on_checkbox_checked(self, translate_rotate=None, axis=None):
        checkbox = eval("self.{0}_{1}".format(translate_rotate, axis))
        checked = checkbox.isChecked()

        if axis == "all":
            if checked == True:
                for axis in ["x", "y", "z"]:
                    axis_checkbox = eval("self.{0}_{1}".format(translate_rotate, axis))
                    axis_checkbox.setCheckState(QtCore.Qt.Checked)
                    axis_checkbox.setEnabled(False)
            if checked == False:
                for axis in ["x", "y", "z"]:
                    axis_checkbox = eval("self.{0}_{1}".format(translate_rotate, axis))
                    axis_checkbox.setEnabled(True)
        else:
            if checked == True:
                eval("self.{0}_all".format(translate_rotate)).setCheckState(QtCore.Qt.Unchecked)



    def on_paste_pose_clicked(self):
        self.checked_attributes = self.get_checked_attributes()
        self.paste_attributes = self.get_paste_attributes(self.checked_attributes)
        self.copyPose.paste_pose(self.anim_data, self.paste_attributes) #self, source_rig, anim_data, paste_attributes

    def on_paste_animation_clicked(self):
        self.checked_attributes = self.get_checked_attributes()
        self.paste_attributes = self.get_paste_attributes(self.checked_attributes)
        self.copyPose.paste_animation(self.anim_data, self.paste_attributes) #self, source_rig, anim_data, paste_attributes

    def get_checked_attributes(self):
        checked_attributes = []
        for attribute in ["translate", "rotate"]:
            for axis in ["x", "y", "z"]:
                attribute_name = "{0}{1}".format(attribute, axis.upper())
                if eval("self.{0}_{1}".format(attribute, axis)).isChecked():
                    checked_attributes.append(attribute_name)
        if self.other_all.isChecked():
            checked_attributes.append("other")
        return checked_attributes

    def get_paste_attributes(self, checked_attributes):
        all_attributes = animMod.get_control_attributes(node=self.source_rig)
        other_attributes = animMod.get_control_attributes(node=self.source_rig)
        paste_attributes = []

        #Work out 'other' attributes - remove translate and rotate  from all attributes
        for attribute in all_attributes:
            for translate_rotate in ["translate", "rotate"]:
                for axis in ["x", "y", "z"]:
                    attribute_name = "{0}{1}".format(translate_rotate, axis.upper())
                    if attribute_name in attribute:
                        other_attributes.remove(attribute)

        #Add translate and rotate attributes
        for attribute in all_attributes:
            for translate_rotate in ["translate", "rotate"]:
                for axis in ["x", "y", "z"]:
                    attribute_name = "{0}{1}".format(translate_rotate, axis.upper())
                    if attribute_name in checked_attributes:
                        if attribute_name in attribute:
                            paste_attributes.append(attribute)

        #Add other attributes
        if "other" in checked_attributes:
            paste_attributes = paste_attributes + other_attributes

        return paste_attributes




class CopyPose(object):

    def __init__(self):
        if G.copyPose:
            return
        G.copyPose = self

    def copy_pose(self, rig):
        self.source_time = cmds.currentTime(query=True)
        self.pose_data = animMod.store_animation_data(time_range=(self.source_time, self.source_time), rig=rig)

    def paste_pose(self, anim_data, paste_attributes):
        selected_frames = animMod.get_target("frames", selected=True)
        print selected_frames

        target_rig = animMod.get_target("rigs", selected=True)[0]
        target_namespace = animMod.get_target("namespace", node=target_rig)

        #Loop through selected controls on target rig and apply data
        for frame in selected_frames:
            print frame
            for control in animMod.get_target("controls", selected=True, node=target_rig):
                control_name = control.rpartition(":")[2]
                target_control = "{0}:{1}".format(target_namespace,control_name)
                for control_attribute in paste_attributes:
                    attribute = control_attribute.rpartition(".")[2]
                    if control_name in control_attribute:
                        attribute_value = self.pose_data[self.source_time][control_attribute]
                        target_attribute = "{0}:{1}".format(target_namespace,control_attribute)
                        try:
                            cmds.setAttr(target_attribute, attribute_value)
                            cmds.setKeyframe(target_control, attribute=attribute, time=frame)
                        except RuntimeError:
                            pass

    def copy_animation(self, rig):
        self.animation_source_frames = animMod.get_target("frames", selected = True)
        self.animation_data = animMod.store_animation_data(time_range=(self.animation_source_frames[0], self.animation_source_frames[-1]), rig=rig)

    def paste_animation(self, animation_data, paste_attributes):
        target_start = cmds.currentTime(query=True)
        source_start = self.animation_source_frames[0]
        time_offset = abs(int(target_start - source_start))

        target_rig = animMod.get_target("rigs", selected=True)[0]
        target_namespace = animMod.get_target("namespace", node=target_rig)

        for i in range(len(self.animation_source_frames)):
            target_frame = target_start + i
            source_frame = source_start + i

            for control in animMod.get_target("controls", selected=True, node=target_rig):
                control_name = control.rpartition(":")[2]
                target_control = "{0}:{1}".format(target_namespace,control_name)
                for control_attribute in paste_attributes:
                    attribute = control_attribute.rpartition(".")[2]
                    if control_name in control_attribute:
                        attribute_value = self.animation_data[source_frame][control_attribute]
                        target_attribute = "{0}:{1}".format(target_namespace,control_attribute)
                        try:
                            cmds.setAttr(target_attribute, attribute_value)
                            cmds.setKeyframe(target_control, attribute=attribute, time=target_frame)
                        except RuntimeError:
                            pass
