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


class CopyWorldSpace_UI(uiMod.BaseSubUI):

    def create_layout(self):
        #Create tool instance
        copyWorldSpace = CopyWorldSpace()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Copy World Space")

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
        self.copy_pose = uiMod.push_button(label = "Copy WS Pose", size=(self.w[6], self.h[1]))
        self.copy_pose.clicked.connect(G.copyWorldSpace.copy_pose)
        self.main_layout.addWidget(self.copy_pose, 1, 0, 1, 6)

        self.paste_wspose = uiMod.push_button(label = "Paste WS Pose", size=(self.w[6], self.h[1]))
        self.paste_wspose.clicked.connect(G.copyWorldSpace.paste_wspose)
        self.main_layout.addWidget(self.paste_wspose, 2, 0, 1, 6)

        self.paste_pose = uiMod.push_button(label = "Paste Pose", size=(self.w[6], self.h[1]))
        self.paste_pose.clicked.connect(G.copyWorldSpace.paste_pose)
        self.main_layout.addWidget(self.paste_pose, 3, 0, 1, 6)

        self.hands_to_fingers= uiMod.push_button(label = "Hands To Fingers", size=(self.w[6], self.h[1]))
        self.hands_to_fingers.clicked.connect(G.copyWorldSpace.hands_to_fingers)
        self.main_layout.addWidget(self.hands_to_fingers, 4, 0, 1, 6)

        self.fix_knees= uiMod.push_button(label = "Fix Knees", size=(self.w[6], self.h[1]))
        self.fix_knees.clicked.connect(G.copyWorldSpace.fix_knees)
        self.main_layout.addWidget(self.fix_knees, 5, 0, 1, 6)

        return self.frame_widget


class CopyWorldSpace(object):

    def __init__(self):
        G.copyWorldSpace = self

    @animMod.viewport_off
    @animMod.undo_chunk
    def paste_wspose(self):
        frame_range = animMod.get_frames()
        controls = animMod.get_controls(selected=True)
        for i in [1, 2]:
            for frame in frame_range:
                cmds.currentTime(frame)
                for control in controls:
                    ctrl = control.rpartition(":")[2]
                    if ctrl in G.WSPOSE:
                        cmds.xform(control, worldSpace=True, eu=True, matrix=G.WSPOSE[ctrl])
                        cmds.setKeyframe(control)

    @animMod.viewport_off
    @animMod.undo_chunk
    def paste_pose(self):
        frame_range = animMod.get_frames()
        controls = animMod.get_controls(selected=True)
        for i in [1, 2]:
            for frame in frame_range:
                cmds.currentTime(frame)
                for control in controls:
                    ctrl = control.rpartition(":")[2]

                    if ctrl in G.POSE:
                        cmds.xform(control, eu=True, matrix=G.POSE[ctrl])
                        cmds.setKeyframe(control)

    @animMod.viewport_off
    @animMod.undo_chunk
    def fix_knees(self):
        # Get the selected controls 
        controls = animMod.get_controls(selected=True)
        # Get the selected frame range 
        frame_range = animMod.get_frames()
        # Set the current time to the first selected frame
        cmds.currentTime(frame_range[0])
        # Get knee twist attributes
        knee_attrs = []
        for control in controls:
            ctrl = control.rpartition(":")[2]
            attributes = cmds.listAttr(control)
            for attr in attributes:
                if attr == "knee_twist":
                    control_attr = control + "." + attr
                    knee_attrs.append(control_attr)

        # Create a dictionary of previous values to compare 
        previous_values = {}
        for attr in knee_attrs:
            previous_values[attr] = None

        # Fix first value
        for frame in frame_range:
            for attr in knee_attrs:
                twist_value = cmds.getAttr(attr)
                if -180 < twist_value < 180:
                    new_value = twist_value
                elif twist_value >= 180:
                    difference = twist_value + 180
                    new_value = -180 + difference%360
                elif twist_value <= -180:
                    difference = twist_value - 180
                    new_value = -180 + difference%360
                else:
                    pass
                
                # Check if there needs to be an offset
                if previous_values[attr] != None:
                    difference = new_value - previous_values[attr]
                    print frame, previous_values[attr], new_value, difference
                    if difference > 180:
                        new_value = new_value - 360
                    elif difference <-180:
                        new_value = new_value + 360
                    else:
                        pass
                    print "Adjusted value", new_value
                previous_values[attr] = new_value
                cmds.setAttr(attr, previous_values[attr])
                cmds.setKeyframe(attr)
                cmds.currentTime(frame+1)













        """for frame in frame_range:
            for attr in knee_attrs:
                # Get knee twist value
                twist_value = cmds.getAttr(attr)
                print "Twist Value:", twist_value
                # Compare value 
                if twist_value > previous_values[attr]:
                    # Example 570 > 120
                    difference = twist_value - previous_values[attr]
                    print "Previous Value", previous_values[attr]
                    print "Difference:", difference # 450
                    if difference > 360:
                        # Remove a number of 360 from value
                        remainder = difference%360






        for frame in frame_range:
            for control in controls:
                ctrl = control.rpartition(":")[2]
                attributes = cmds.listAttr(control)
                for attr in attributes:
                    if attr == "knee_twist":
                        control_attr = control + "." + attr
                        twist_value = cmds.getAttr(control_attr)
                        new_value = twist_value%360
                        cmds.setAttr(control_attr, new_value)
                        cmds.setKeyframe(control)
                        previous_values[control] = new_value
                        cmds.currentTime(frame +1)"""




    def copy_pose(self):
        G.WSPOSE = {}
        G.POSE={}
        #controls = animMod.get_controls(selected=False)
        selected_controls = animMod.get_controls(selected=True)

        for control in selected_controls:
            namespace = control.rpartition(":")[0]
            ctrl = control.rpartition(":")[2]
            G.WSPOSE[ctrl] = cmds.xform(control, query=True, worldSpace=True, matrix=True)
            G.POSE[ctrl] = cmds.xform(control, query=True, matrix=True)

    @animMod.viewport_off
    @animMod.undo_chunk
    def hands_to_fingers(self):
        hand_attrs = ["ThumbBend", "IndexBend", "MiddleBend", "RingBend", "PinkyBend", "FingersSpread", "Cup"]
        frame_range = animMod.get_frames()
        controls = animMod.get_controls(selected=False)
        fingers = []
        for control in controls: 
            if "ik_wrist_l_anim" in control:
                left_hand = control
            if "ik_wrist_r_anim" in control:
                right_hand = control
            if "finger" in control:
                fingers.append(control)            
            else:
                pass
        
        
        for frame in frame_range:
                cmds.currentTime(frame)
                self.copy_pose()
                for i in [1, 2]: 
                    for attr in hand_attrs:
                        left_hand_attr = "{0}.{1}".format(left_hand, attr)
                        right_hand_attr = "{0}.{1}".format(right_hand, attr)
                        cmds.setAttr(left_hand_attr, 0)
                        #cmds.setKeyframe(left_hand)
                        cmds.setAttr(right_hand_attr, 0)
                        #cmds.setKeyframe(right_hand)
                    for control in fingers:
                        ctrl = control.rpartition(":")[2]
                        if ctrl in G.WSPOSE:
                            cmds.xform(control, worldSpace=True, eu=True, matrix=G.WSPOSE[ctrl])
                            cmds.setKeyframe(control)
                    

        

        


        # For each frame  




    
