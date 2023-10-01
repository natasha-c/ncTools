# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# python
import weakref
from functools import partial

# maya
import maya.cmds as cmds
import maya.OpenMayaUI as omui

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets

# ncTools
from ncTools.mods                   import uiMod;       reload(uiMod)
from ncTools.mods                   import animMod;     reload(animMod)
from ncTools.tools.ncToolboxGlobals   import ncToolboxGlobals as G


class KeyCleanupTools_UI(uiMod.BaseSubUI):

    def create_layout(self):
        keyCleanupTools = KeyCleanupTools()

        self.keyCleanupTools = KeyCleanupTools()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Key Cleanup Tools")

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
        self.average_keys = uiMod.push_button(label = "Average Keys", size = (self.w[6], self.h[1]))
        self.average_keys.clicked.connect(self.on_average_keys_clicked)
        self.main_layout.addWidget(self.average_keys, 1, 0, 1, 6)

        self.smooth_keys = uiMod.push_button(label = "Smooth Keys", size = (self.w[6], self.h[1]))
        self.smooth_keys.clicked.connect(self.on_smooth_keys_clicked)
        self.main_layout.addWidget(self.smooth_keys, 2, 0, 1, 6)

        self.delete_redundant_keys = uiMod.push_button(label = "Delete Redundant", size = (self.w[6], self.h[1]))
        self.delete_redundant_keys.clicked.connect(G.keyCleanupTools.delete_redundant_keys)
        self.main_layout.addWidget(self.delete_redundant_keys, 3, 0, 1, 6)

        self.keep_extreme_keys = uiMod.push_button(label = "Keep Extreme Keys", size = (self.w[6], self.h[1]))
        self.keep_extreme_keys.clicked.connect(G.keyCleanupTools.keep_extreme_keys)
        self.main_layout.addWidget(self.keep_extreme_keys, 4, 0, 1, 6)

        self.delete_outside_timeline = uiMod.push_button(label = "Delete Outside Timeline", size = (self.w[6], self.h[1]))
        self.delete_outside_timeline.clicked.connect(G.keyCleanupTools.delete_outside_timeline)
        self.main_layout.addWidget(self.delete_outside_timeline, 5, 0, 1, 6)


        return self.frame_widget


    def on_average_keys_clicked(self):
        self.keyCleanupTools.average()


    def on_smooth_keys_clicked(self):
        self.keyCleanupTools.smooth_keys()


class KeyCleanupTools(object):

    def __init__(self):
        G.keyCleanupTools = self

    def delete_outside_timeline(self):
        """
        Procedure to delete all keyframe outside the set timeline range
        """
        cmds.undoInfo(openChunk = True)
        # Get the frame range of the timeline
        frame_range = animMod.get_playback_range()
        # Get the selected controls
        controls = animMod.get_controls(selected=True)
        # For every control find the anim curves and delete the outside keyframes
        for control in controls:
            # Get the selected anim curves, if none selected get all for the selected control
            anim_curves = animMod.get_anim_curves(node=control, selected=True)
            if anim_curves is None:
                anim_curves = animMod.get_anim_curves(node=control, selected=False)
            # For each of the anim curves
            for anim_curve in anim_curves:
                # Set a keyframe on the first and last frame of the frame range
                cmds.setKeyframe(anim_curve, insert=True, time=frame_range)
                # Get the first and last keyframe
                first_keyframe = cmds.keyframe(anim_curve, query=True, index=(0,0))[0]
                last_index = cmds.keyframe(anim_curve, indexValue=True, query=True)[-1]
                last_keyframe = cmds.keyframe(anim_curve, query=True, index=(last_index, last_index))[0]

                # Delete keyframe ranges
                if first_keyframe != frame_range[0]:
                    cmds.cutKey(anim_curve, option="keys", time=(first_keyframe, (frame_range[0]-1)))
                if last_keyframe != frame_range[1]:
                    cmds.cutKey(anim_curve, option="keys", time=((frame_range[1]+1), last_keyframe))
        cmds.undoInfo(closeChunk = True)



    def average(self):
        cmds.undoInfo(openChunk = True)
        anim_curves = animMod.get_anim_curves(selected=True)
        for anim_curve in anim_curves:
            key_times = animMod.get_key_times(anim_curve=anim_curve, selected=True)
            key_values = animMod.get_key_values(anim_curve=anim_curve, selected=True)
            average_value = sum(key_values)/len(key_values)
            for key_time in key_times:
                cmds.keyframe(anim_curve, edit=True, time=(key_time, key_time), valueChange=average_value)
        cmds.undoInfo(closeChunk = True)


    def smooth_keys(self):
        cmds.undoInfo(openChunk = True)

        # Get the selected anim curves from the graph editor
        anim_curves = cmds.keyframe(q = True, sl = True, n = True)
        print "ANIM CURVES", anim_curves

        # Throw and error if no curve is selected
        if len(anim_curves) == 0:
            cmds.error("Please select at least 3 keys in the graph editor.")

        # For every anim curve selected
        for anim_curve in anim_curves:
            # Get the selected keys
            key_times = cmds.keyframe(anim_curve, q = True, sl = True)
            keyframe_count = len(key_times)

            # Create a duplicate curve
            anim_curve_copy = cmds.duplicate(anim_curve)[0]

            # Throw an error if less than three keys are selected
            if keyframe_count < 3:
                cmds.error("Please select at least 3 keys in the graph editor.")

            else:
                # Create a duplicate curve with average of keyframe values
                for i in range(1, keyframe_count-1): #exludes start and end
                    # Get the values of the previous, current and next keyframes
                    previous_frame = key_times[i-1]
                    current_frame = key_times[i]
                    next_frame = key_times[i+1]
                    previous_value = cmds.keyframe(anim_curve, query = True, time = (previous_frame, previous_frame), vc = True)[0]
                    current_value = cmds.keyframe(anim_curve, query = True, time = (current_frame, current_frame), vc = True)[0]
                    next_value = cmds.keyframe(anim_curve, query = True, time = (next_frame, next_frame), vc = True)[0]

                    # Get the average value
                    average_value = previous_value + ((current_frame-previous_frame)*(next_value - previous_value)/(next_frame-previous_frame))
                    print average_value
                    # Put new value on duplicate curve
                    cmds.keyframe(anim_curve_copy, time=(current_frame, current_frame), absolute=True, vc=average_value)

                # Once duplicate curve has been build, copy values to original curve

                for i in range(1, keyframe_count-1):
                    current_frame = key_times[i]
                    copy_value = cmds.keyframe(anim_curve_copy, query=True, time=(current_frame, current_frame), vc=True)[0]
                    cmds.keyframe(anim_curve, time=(current_frame, current_frame), absolute=True, vc=copy_value)

            # Delete the duplicate anim curve
            cmds.delete(anim_curve_copy)

        # Print done
        print "DONE"

        cmds.undoInfo(closeChunk = True)


    def keep_extreme_keys(self):
        cmds.undoInfo(openChunk = True)
        cut_keys = {}
        print "keep extreme"
        anim_curves = []
        for control in animMod.get_controls(selected=True):
            anim_curves = anim_curves + animMod.get_anim_curves(node=control, selected=True)
        print "ANIM CURVES", anim_curves
        for anim_curve in anim_curves:
            selected_keys = animMod.get_keys(anim_curve=anim_curve, selected=True)
            remove_keys = self.get_extreme_frames(anim_curve)
            print remove_keys
            cut_keys[anim_curve] = [x for x in selected_keys if x not in remove_keys]
        for anim_curve in cut_keys:
            select_keys = cut_keys[anim_curve]
            for frame in select_keys:
                cmds.selectKey(anim_curve, time=(frame,frame), keyframe=True)
                cmds.cutKey(animation="keys", clear=True)

        cmds.undoInfo(closeChunk = True)


    def get_extreme_frames(self, anim_curve):
        extreme_frames = []
        selected_frames = cmds.keyframe(anim_curve, query=True, selected=True, timeChange=True)

        for previous_frame, current_frame, next_frame in animMod.get_prev_current_next(selected_frames):
            if previous_frame is None:
                previous_frame = current_frame
            if next_frame is None:
                next_frame = current_frame

            previous_value = cmds.keyframe(anim_curve, query=True, time=(previous_frame, previous_frame), valueChange=True)
            current_value = cmds.keyframe(anim_curve, query=True, time=(current_frame, current_frame), valueChange=True)
            next_value = cmds.keyframe(anim_curve, query=True, time=(next_frame, next_frame), valueChange=True)

            if previous_value < current_value > next_value:
                extreme_frames.append(current_frame)
            if previous_value > current_value < next_value:
                extreme_frames.append(current_frame)
            """
            if previous_value == current_value:
                extreme_frames.append(current_frame)
            if next_value == current_value:
                extreme_frames.append(current_frame)
            """
            print "previous", previous_frame
            if previous_frame == current_frame:
                extreme_frames.append(current_frame)
            print "next", next_frame
            if next_frame == current_frame:
                extreme_frames.append(current_frame)

        extreme_frames = list(set(extreme_frames))

        print "extreme_frames", extreme_frames

        return extreme_frames


    def delete_redundant_keys(self):
        cmds.undoInfo(openChunk = True)
        # Get the selected controls
        controls = animMod.get_controls(selected=True)
        # For every control find the anim curves and delete the outside keyframes
        for control in controls:
            # Get the selected anim curves, if none selected get all for the selected control
            anim_curves = animMod.get_anim_curves(node=control, selected=True)
            if anim_curves is None:
                anim_curves = animMod.get_anim_curves(node=control, selected=False)
            # For each of the anim curves
            for anim_curve in anim_curves:
                redundant_keys = []
                # Get the selected keys, if none selected get all for the selected curve
                keyframes = animMod.get_keys(anim_curve=anim_curve, selected=True)
                if keyframes is None:
                    keyframes = animMod.get_keys(anim_curve=anim_curve, selected=False)
                for previous_frame, current_frame, next_frame in animMod.get_prev_current_next(keyframes):
                    if previous_frame is None:
                        previous_frame = current_frame
                    if next_frame is None:
                        next_frame = current_frame
                    previous_value = cmds.keyframe(anim_curve, query=True, time=(previous_frame, previous_frame), valueChange=True)
                    current_value = cmds.keyframe(anim_curve, query=True, time=(current_frame, current_frame), valueChange=True)
                    next_value = cmds.keyframe(anim_curve, query=True, time=(next_frame, next_frame), valueChange=True)
                    if previous_value == current_value == next_value:
                        redundant_keys.append(current_frame)
                redundant_keys.pop(0)
                redundant_keys.pop(-1)
                for key in redundant_keys:
                    cmds.cutKey(anim_curve, option="keys", time=(key, key))
        cmds.undoInfo(closeChunk = True)



        """
        for control in controls:
            print control
            attributes = animMod.get_target("attributes", attribute_options = ["keyable"], node=control)
            for attribute in attributes:
                anim_layers = animMod.get_target("anim_layers", selected=False)

                for anim_layer in anim_layers:
                    anim_curves = animMod.get_target("anim_curves", anim_layer=anim_layer, attribute=attribute, node=control)
                    for anim_curve in anim_curves:
                        print anim_curve
                        redundant_keys = []
                        keyframes = cmds.keyframe(anim_curve, query=True, timeChange=True)
                        for previous_frame, current_frame, next_frame in animMod.get_prev_current_next(keyframes):
                            if previous_frame is None:
                                previous_frame = current_frame
                            if next_frame is None:
                                next_frame = current_frame
                            break
                            previous_value = cmds.keyframe(anim_curve, query=True, time=(previous_frame, previous_frame), valueChange=True)
                            current_value = cmds.keyframe(anim_curve, query=True, time=(current_frame, current_frame), valueChange=True)
                            next_value = cmds.keyframe(anim_curve, query=True, time=(next_frame, next_frame), valueChange=True)

                            if previous_value == current_value == next_value:
                                redundant_keys.append(current_frame)

                        for frame in redundant_keys:
                            cmds.selectKey(anim_curve, time=(frame,frame), keyframe=True, remove=True)
                        cmds.cutKey(animation="keys", clear=True)"""
