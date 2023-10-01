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



    def copy_pose(self):
        G.WSPOSE = {}
        G.POSE={}
        controls = animMod.get_controls(selected=False)
        selected_controls = animMod.get_controls(selected=True)

        for control in controls and selected_controls:
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




    
