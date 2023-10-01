##################################################################################
# RIG SELECTION                                    | BLEND VALUE       | DISPLAY # 
# -------------------------------------------------------------------- | ------- #
# Add parent rig [-------rig1-----------] [>] [x]  | [-.--]            |   [ ]   #
# Add parent rig [-------rig2-----------] [>] [x]  | [-.--]            |   [ ]   #
# Add parent rig [-------rig3-----------] [>] [x]  | [-.--]            |   [ ]   #
# -------------------------------------------------|------------------ | ------- #
# Add child rig  [-------endrig---------] [>] [x]  | [KEY] [DELETEKEY] |   [ ]   #
# -------------------------------------------------------------------- | ------- #
# [BAKE TO CHILD]      [] Remove parent rigs                                     #
##################################################################################

"""
This tool allows for the blending of animations from various parent rigs onto a final child rig. Allowing to key the blends if necessary. 
Good for blending between different clips of animation, and takes from mocap. 
Move the main_ctrl around to line up in the scene
Once finished user can bake to the child rig and optionally delete the parent rigs and clean up the scene.
"""

# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.1
# Purpose: To match differences in animation after updating rigs
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
from maya import OpenMayaUI as omui
from maya import cmds
from maya import mel

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# shiboken
from shiboken2 import wrapInstance

# regEdit
from re import split

# functools
from functools import partial

# ncTools
from ncTools.mods import uiMod; reload(uiMod)

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class ConstrainBlendGlobals(object):

    def __getattr__(self, attr):
        return None

G = ConstrainBlendGlobals()

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def get_main_window():
    pointer = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(long(pointer), QtWidgets.QMainWindow)
    return main_window

def show(mode="refresh"):
    G.constrainBlend = G.constrainBlend or ConstrainBlend_UI()
    if mode == "refresh":
        G.constrainBlend = ConstrainBlend_UI(parent=get_main_window())
        G.constrainBlend.start()

# GUI OBJECTS 
def label(label="Label", width=50, height=15, font_size=8, align="left", word_wrap=True):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    text = QtWidgets.QLabel(label)
    text.setMinimumSize(width, height)
    text.setMaximumSize(width, height)
    text.setWordWrap(word_wrap)
    if align == "left":
        text.setAlignment(QtCore.Qt.AlignLeft)
    elif align == "center":
        text.setAlignment(QtCore.Qt.AlignCenter)
    elif align == "right":
        text.setAlignment(constrain_widget_layout)
    text.setFont(font)
    return text

def line_edit(width=25, height=25, font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    line_edit = QtWidgets.QLineEdit()
    line_edit.setMinimumSize(width, height)
    line_edit.setMaximumSize(width, height)
    line_edit.setFont(font)
    return line_edit

def push_button(label="Button", width=200, height=25, font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    button = QtWidgets.QPushButton(label)
    button.setMinimumSize(width, height)
    button.setMaximumSize(width, height)
    button.setFont(font)
    return button

def custom_spinbox(width=100, height=25, font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    custom_spinbox = uiMod.CustomSpinBox(spinbox_type=1, value=0)
    custom_spinbox.setMinimumSize(width, height)
    custom_spinbox.setMaximumSize(width, height)
    custom_spinbox.setFont(font)
    return custom_spinbox

def checkbox(label="Checkbox", width=50, height=25, font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    checkbox = QtWidgets.QCheckBox(label)
    checkbox.setMinimumSize(width, height)
    checkbox.setMaximumSize(width, height)
    checkbox.setFont(font)
    return checkbox

def vertical_line():
    divider = QtWidgets.QLabel("")
    divider.setStyleSheet("QLabel {background-color: #3e3e3e; padding: 0; margin: 0; border-left: 1 solid #666; border-right: 1 solid #2a2a2a;}")
    divider.setMaximumWidth(2)
    return divider

def horizontal_line():
    divider = QtWidgets.QLabel("")
    divider.setStyleSheet("QLabel {background-color: #3e3e3e; padding: 0; margin: 0; border-top: 1 solid #666; border-bottom: 1 solid #2a2a2a;}")
    divider.setMaximumHeight(2)
    return divider



# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
class ConstrainBlend_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "Constrain Blend"
    UI_NAME = "constrain_blend"
    WINDOWS = [WINDOW_NAME, UI_NAME]

    rigs = {} 

    
    def __init__(self, *args, **kwargs):
        super(ConstrainBlend_UI, self).__init__(*args, **kwargs)


    def __getattr__(self, attr):
        return None


    def start(self):
        self.delete_windows()
        self.create_window()
        self.show()


    def delete_windows(self, onOff=True, forceOff=False):
        # Delete all windows
        for window in self.WINDOWS:
            if cmds.window(window, query=True, exists=True):
                cmds.deleteUI(window)


    def create_window(self):
        # Create instance of tool
        constrainBlend = ConstrainBlend()

        # Set object name and window title
        self.setObjectName(self.UI_NAME)
        self.setWindowTitle(self.WINDOW_NAME)

        # Create central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Create main layout
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)
        self.central_widget.setLayout(self.main_layout)

        self.display_widget = QtWidgets.QWidget()
        self.main_layout.addWidget(self.display_widget)
        self.display_grid = QtWidgets.QGridLayout()
        self.display_grid.setSpacing(5)
        self.display_grid.setContentsMargins(0, 0, 0, 0)
        self.display_widget.setLayout(self.display_grid)

        # Add buttons and other GUI objects to layout
        # INSTRUCTION
        self.how_to_label = label(label="Choose the parent rigs and child rig. Key the blend points. Bake.", width=400) #?# Need to look at width later.
        self.display_grid.addWidget(self.how_to_label, 0, 0, 1, 8)
        self.display_grid.addWidget(horizontal_line(), 1, 0, 1, 8)
        
        # SELECTION HEADER
        self.rig_selection_label = label(label="RIG SELECTION", width=100)
        self.display_grid.addWidget(self.rig_selection_label, 2, 2, 1, 4)

        # BLEND HEADER
        self.blend_value_label = label(label="BLEND VALUE", width = 100)
        self.display_grid.addWidget(self.blend_value_label, 2, 6, 1, 2)

        # RIG SELECTIONS        
        # Add selection boxes for parent rigs, button to add selected, button to delete, blend values and display tickbox
        self.parent_count=3
        for count in range(self.parent_count):
            count = count+1
            self.create_rig_row_ui(rig_type="parent_rig", count=count, blend=True)
        print (self.parent_count)
        self.display_grid.addWidget(horizontal_line(), self.parent_count+5, 0, 1, 8)

        # Add child rig row 
        self.create_rig_row_ui(rig_type="child_rig", count=self.parent_count+2, blend=False)

        # Key and delete button for keying blend values
        self.key_button = push_button(label="KEY", width=45)
        self.key_button.clicked.connect(constrainBlend.add_key)
        self.display_grid.addWidget(self.key_button, self.parent_count+6, 6, 1, 1)

        self.delete_key_button = push_button(label="DELETE", width=45)
        self.delete_key_button.clicked.connect(constrainBlend.delete_key)
        self.display_grid.addWidget(self.delete_key_button, self.parent_count+6, 7, 1 , 1) 

        self.display_grid.addWidget(horizontal_line(), self.parent_count+7, 0, 1, 8)

        # Constrain, delete constraints and bake buttons.
        self.three_button_layout_widget=QtWidgets.QWidget()
        self.three_button_layout = QtWidgets.QGridLayout()
        self.three_button_layout.setContentsMargins(0, 0, 0, 0)
        self.three_button_layout.setSpacing(5)
        self.three_button_layout_widget.setLayout(self.three_button_layout)
        self.display_grid.addWidget(self.three_button_layout_widget, self.parent_count+8, 0, 1, 8)

        self.constrain_button = push_button(label="CONSTRAIN", width=155, height=50)
        self.constrain_button.clicked.connect(constrainBlend.constrain)
        self.three_button_layout.addWidget(self.constrain_button, 0, 0, 1, 1)

        self.delete_constrain_button = push_button(label="DELETE CONSTRAINTS", width=155, height=50)
        self.delete_constrain_button.clicked.connect(constrainBlend.delete)
        self.three_button_layout.addWidget(self.delete_constrain_button, 0, 1, 1, 1)

        self.bake_constrain_button = push_button(label="BAKE", width=155, height=50)
        self.bake_constrain_button.clicked.connect(constrainBlend.bake)
        self.three_button_layout.addWidget(self.bake_constrain_button, 0, 2, 1, 1)

        # Size UI
        sizeHint = self.sizeHint()
        self.setMaximumSize(sizeHint)


    # -----------------------------------------------------------------------------
    # Button clicked functions / UI updates
    # -----------------------------------------------------------------------------

    def create_rig_row_ui(self, rig_type, count, blend):
        print rig_type
        print count
        # Create label of rig type: Parent and number, or child.
        if rig_type == "parent_rig":
            label_string = " ".join(a.capitalize() for a in split("([^a-zA-Z0-9])", rig_type) if a.isalnum()) + " " +str(count)
            rig_id = "{rig_type}_{count}".format(rig_type=rig_type, count=count)
        if rig_type == "child_rig":
            label_string = " ".join(a.capitalize() for a in split("([^a-zA-Z0-9])", rig_type) if a.isalnum()) + " " +str(count-self.parent_count-1)    
            rig_id = "{rig_type}_{count}".format(rig_type=rig_type, count=count-self.parent_count-1)      
        print (label_string)

        print(rig_id)
        self.rigs[rig_id + "_label"] = label(label=label_string, width=75)
        self.rigs[rig_id + "_label"].setAlignment(QtCore.Qt.AlignRight)
        self.display_grid.addWidget((self.rigs[rig_id + "_label"]), count+4, 1, 1, 1)

        self.rigs[rig_id + "_display"] = line_edit(width=200)
        self.rigs[rig_id + "_display"].setReadOnly(True)
        self.display_grid.addWidget(self.rigs[rig_id + "_display"], count+4, 2, 1, 1)

        self.rigs[rig_id + "_add"] = push_button(label="<<", width=25)
        self.rigs[rig_id + "_add"].clicked.connect(partial(self.on_rig_add_clicked, rig_id))
        self.display_grid.addWidget(self.rigs[rig_id + "_add"], count+4, 3, 1, 1)

        self.rigs[rig_id + "_delete"] = push_button(label="Clear", width=50)
        self.rigs[rig_id + "_delete"].clicked.connect(partial(self.on_rig_delete_clicked, rig_id))
        self.display_grid.addWidget(self.rigs[rig_id + "_delete"], count+4, 4, 1, 1)

        self.display_grid.addWidget(vertical_line(), count+4, 5, 1, 1)

        if blend:
            self.parent_rig_blend = custom_spinbox(width=100)
            self.display_grid.addWidget(self.parent_rig_blend, count+4, 6, 1, 2)

    def on_rig_add_clicked(self, rig_id):
        # Update UI and rig lists
        selected_rig = G.constrainBlend.constrainBlend.get_selected_rig()

        # Update rig lists 
        if "parent" in rig_id:
            if selected_rig not in G.constrainBlend.constrainBlend.parent_rigs:
                # Add rig to parent rig dict and display in ui
                G.constrainBlend.constrainBlend.parent_rigs[selected_rig]=[]
                self.rigs[rig_id + "_display"].setText(selected_rig)  
            else:
                cmds.error ("This rig is already a parent")
        elif "child" in rig_id:
            # Add rig to child rig dict and display in ui
            G.constrainBlend.constrainBlend.child_rig[selected_rig] = []
            self.rigs[rig_id + "_display"].setText(selected_rig)  
        else:
            print ("Please Select a Rig")


    def on_rig_delete_clicked(self, rig_id):
        # Check what is in the rig selection
        current_rig = self.rigs[rig_id + "_display"].displayText()
        if current_rig == "":
            cmds.error("No rig selected")
        if "parent" in rig_id:
            if current_rig in G.constrainBlend.constrainBlend.parent_rigs:
                # Remove deleted rig from parent rig dict
                G.constrainBlend.constrainBlend.parent_rigs.pop(current_rig, None)
        elif "child" in rig_id:
            print "CHILD"
            # Remove deleted rig from child rig dict
            G.constrainBlend.constrainBlend.child_rig[current_rig] = None

        # Clear the lineedit display box
        self.rigs[rig_id + "_display"].clear()

    






        

            
##################################################################################
# RIG SELECTION                                    | BLEND VALUE       | DISPLAY # 
# -------------------------------------------------------------------- | ------- #
# Add parent rig [-------rig1-----------] [>] [x]  | [-.--]            |   [ ]   #
# Add parent rig [-------rig2-----------] [>] [x]  | [-.--]            |   [ ]   #
# Add parent rig [-------rig3-----------] [>] [x]  | [-.--]            |   [ ]   #
# -------------------------------------------------|------------------ | ------- #
# Add child rig  [-------endrig---------] [>] [x]  | [KEY] [DELETEKEY] |   [ ]   #
# -------------------------------------------------------------------- | ------- #
# [CONSTRAIN] [DELETE CONSTRAINTS]                                               #
# -------------------------------------------------------------------- | ------- #
# [BAKE TO CHILD]      [] Remove parent rigs                                     #
##################################################################################


class ConstrainBlend(object):

    def __init__(self):
        if G.constrainBlend.constrainBlend:
            return
        G.constrainBlend.constrainBlend = self

        self.parent_rigs = {}
        self.child_rig = {} 


    def constrain(self):
        cmds.undoInfo(openChunk=True)
        print ("Constraining")
        # For each parent rig, get the controls 
        for parent in self.parent_rigs:
            self.parent_rigs[parent] = self.get_controls(parent)
        
        # For child rig get controls and attributes to constrain
        for child in self.child_rig:
            self.master_constraint = "{child}:master_anim_cbConstraint".format(child=child)
            self.child_rig[child] = {}
            controls = self.get_controls(child)
            for control in controls:
                print "________________________________________________"
                print "CONTROL", control
                parent_controls = []
                for parent in self.parent_rigs:
                    parent_control_match = control.replace(child, parent)
                    if parent_control_match in self.parent_rigs[parent]:
                        parent_controls.append(parent_control_match)
                print "PARENT CTRLS", parent_controls
            
        
                # Is control keyable?
                keyable_attributes = []
                skip = {}
                for attr in ["rotate", "translate"]:
                    skip[attr] = []
                    for axis in ["X", "Y", "Z"]:
                        attribute = control + "." + attr + axis
                        if cmds.listAttr(attribute, v=True, u=True, k=True):
                            keyable_attributes.append(attribute)
                        else:
                            skip[attr].append(axis.lower())

                print "KEYABLE", keyable_attributes
                if len(skip["translate"]) == 3 and len(skip["rotate"]) == 3:
                    pass
                elif cmds.listConnections(attribute, type="constraint"):
                    pass
                else:
                    constraint_name = "{control}_cbConstraint".format(control=control)                     
                    self.child_constraint = cmds.parentConstraint(parent_controls, control, name=constraint_name, skipTranslate=skip["translate"], skipRotate=skip["rotate"])
                    self.child_rig[child][control] = self.child_constraint
                    print "constraint", self.child_rig[child][control]

        
        print "################################################"
        print self.child_rig
        for child in self.child_rig:
            for control in self.child_rig[child]:
                for constraint in self.child_rig[child][control]:
                        print "CONSTRAINT", constraint
                        count = 0
                        if constraint != self.master_constraint:
                            for i in range(len(self.parent_rigs)):
                                print control
                                parent_attr = "{master}.master_animW{count}".format(master=self.master_constraint, count=count)
                                target_attr = "{constraint}.{control}W{count}".format(constraint=constraint, control=control.rpartition(":")[2], count=count)
                                print "PARENT", parent_attr
                                print "TARGET", target_attr
                                cmds.connectAttr(parent_attr, target_attr, f=True)
                                count+=1

                        

        cmds.undoInfo(closeChunk=True)

    def delete(self):
        for child in self.child_rig:
            for control in self.get_controls(child):
                cmds.select(control)
                cmds.delete(cn=True)
        print ("Delete")

    def bake(self):
        print ("Bake")

    def add_key(self):
        print ("Key added")

    def delete_key(self):
        print ("Key deleted")

    def get_selected_rig(self):
        selection = cmds.ls(sl=1)
        if selection == []:
            cmds.error("Please select a rig")
        else:
            rig_namespace = selection[0].rpartition(":")[0]
        return rig_namespace

    def get_controls(self, rig):
        rig_controls = []
        for node in cmds.ls(assemblies=True):
            if rig in node:
                relatives = cmds.listRelatives(node, ad=True, pa=True, type="nurbsCurve")
                for curve in relatives or []:
                    control = cmds.listRelatives(curve, parent=True, pa=True, type="transform")[0]
                    rig_controls.append(control)
        return rig_controls









        

    






