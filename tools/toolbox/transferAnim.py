# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# python
import weakref
from functools import partial
import pymel as pm

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


class TransferAnim_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        G.transferAnim = TransferAnim()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Transfer Animation", base_width=self.w[1], base_height=self.h[1])

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
        self.bake_to_locator = uiMod.push_button(label="Bake To Locators", size=(self.w[6], self.h[1]))
        self.bake_to_locator.clicked.connect(G.transferAnim.bake_to_locator)
        self.main_layout.addWidget(self.bake_to_locator, 1, 0, 1, 6)

        self.transfer_paste = uiMod.push_button(label="Paste All", size=(self.w[6], self.h[1]))
        self.transfer_paste.clicked.connect(G.transferAnim.paste_all)
        self.main_layout.addWidget(self.transfer_paste, 2, 0, 1, 6)

        self.transfer_paste_selected = uiMod.push_button(label="Paste Selected", size=(self.w[6], self.h[1]))
        self.transfer_paste_selected.clicked.connect(G.transferAnim.paste_selected)
        self.main_layout.addWidget(self.transfer_paste_selected, 3, 0, 1, 6)



        return self.frame_widget

class TransferAnim(object):

    def __init__(self):
        G.transferAnim = self

    def paste_all(self):
        self.paste(selected=False)

    def paste_selected(self):
        self.paste(selected=True)

    @animMod.undo_chunk
    @animMod.viewport_off
    def bake_to_locator(self):
        self.rig = animMod.get_top_node(node=cmds.ls(sl=1)[0])
        self.rig_controls = animMod.get_controls(rig=self.rig)
        self.rig_namespace = animMod.get_namespace(node=self.rig)

        # Create baked locator group
        self.locator_group = "rig_matcher_locators"
        self.rig_matcher_locators = []
        if cmds.objExists(self.locator_group):
            cmds.delete(self.locator_group)
        cmds.group(empty=True, name=self.locator_group)

        # Create locators for each control
        control_attr_type = dict.fromkeys(self.rig_controls)
        control_locator = {}
        for control in control_attr_type:
            if cmds.objExists(control):
                transform_matrix = cmds.xform(query=True, matrix=True, worldSpace=True)
                control_attributes = animMod.get_attributes(node=control, attribute_options=["keyable"]) 
                if control_attributes == None:
                    continue
                else:
                    control_attr_type[control] = dict.fromkeys(control_attributes)                 
                for attr in control_attr_type[control]: 
                    attribute = "{0}.{1}".format(control, attr)
                    control_attr_type[control][attr] = cmds.getAttr(attribute, type=True)


                locator_name = "{control}_LOC".format(control=control.rpartition(":")[2])
                baked_locator = cmds.spaceLocator(name=locator_name)
                self.rig_matcher_locators.append(locator_name)
                control_locator[control] = baked_locator
                for attr in control_attr_type[control]:
                    if cmds.attributeQuery(attr, node=locator_name, exists=True) == False:
                        type = control_attr_type[control][attr]
                        if type == "string":
                            cmds.addAttr(baked_locator, keyable=True, longName=attr, niceName=attr, dataType=type)
                        else:
                            cmds.addAttr(baked_locator, keyable=True, longName=attr, niceName=attr, attributeType=type)
                    control_attr = "{0}.{1}".format(control, attr)
                    locator_attr = "{0}.{1}".format(locator_name, attr)
                    cmds.connectAttr(control_attr, locator_attr)

                cmds.parent(baked_locator, self.locator_group)
                cmds.parentConstraint(control, baked_locator)
        
              
        start_frame = int(cmds.playbackOptions(min=True, query=True))
        end_frame = int(cmds.playbackOptions(max=True, query=True))
        cmds.bakeResults(self.rig_matcher_locators, t=(start_frame, end_frame), simulation=True)
        cmds.delete(self.rig_matcher_locators, cn=True)  

    @animMod.undo_chunk
    @animMod.viewport_off
    def paste(self, selected=False):
        print "paste"

        self.target_rig = animMod.get_top_node(node=cmds.ls(sl=1)[0])
        self.target_rig_controls = animMod.get_controls(rig=self.target_rig)
        self.target_rig_namespace = animMod.get_namespace(node=self.target_rig)
        self.locator_group = "rig_matcher_locators"
        self.rig_matcher_locators = cmds.listRelatives(self.locator_group, c=True)

        start_frame = int(cmds.playbackOptions(min=True, query=True))
        end_frame = int(cmds.playbackOptions(max=True, query=True))

        # Define paste controls 
        if selected == True:
            paste_controls = cmds.ls(sl=1)
        elif selected == False:
            paste_controls = self.target_rig_controls

        for frame in range(start_frame, end_frame+1):
            cmds.currentTime(frame, edit=True)
            for control in paste_controls:
                control_name = control.rpartition(":")[2]
                locator = "{0}_LOC".format(control_name) 
                cmds.setKeyframe(control)
            
            difference = self.snap(paste_controls)
            new_difference = self.snap(paste_controls)
            print difference
            print new_difference
            
            loop_counter = 1 
            print round(difference, 2)
            while round(difference, 2) != round(new_difference, 2):
                print "LOOP", loop_counter
                loop_counter = loop_counter + 1 
                if loop_counter >50:
                    break
                    
                difference = new_difference
                new_difference = self.snap(paste_controls)


    def snap(self, controls):

        difference = []
        for control in controls:
            control_name = control.rpartition(":")[2]
            locator = "{0}_LOC".format(control_name) 

            if cmds.objExists(locator):
                # Align ws values 
                locator_xform = cmds.xform(locator, query=True, m=True, ws=True)
                cmds.xform(control, m=locator_xform, ws=True, a=True)
                control_xform = cmds.xform(control, query=True, m=True, ws=True)
                print "Locator xform", locator, locator_xform
                print "Control xform", control, control_xform
                cmds.setKeyframe(control)
                for c,l in zip(control_xform, locator_xform):
                    c = round(c, 5)
                    l = round(l, 5)
                    dif = l - c
                    difference.append(dif)
        sum_diff = sum(difference)
        print sum_diff
        return sum_diff
        

        
















    

        #Bake target_rig controls 

        #Delete constraints 



    