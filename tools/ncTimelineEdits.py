# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: Add tools to the marking menu to aid in editting keyframes from the timeline
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
import maya.cmds as cmds 
import maya.mel as mel
import maya.OpenMayaUI as omui

# shiboken 
from shiboken2 import wrapInstance

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets


# -----------------------------------------------------------------------------
# Globals  
# -----------------------------------------------------------------------------
global TIMELINE_EDITS
TIMELINE_EDITS = None 



# -----------------------------------------------------------------------------
# Install
# -----------------------------------------------------------------------------
def install():
    
    global TIMELINE_EDITS

    # Check if installed 
    if TIMELINE_EDITS:
        raise RuntimeError("Timeline Edits is already installed!")

    # Get parent
    parent = get_timeline()
    layout = parent.layout()

    # Create layout if non exists 
    if not layout:
        layout = QtWidgets.QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        parent.setLayout(layout)

    # Create timeline edits 
    TIMELINE_EDITS = TimelineEdits()
    TIMELINE_EDITS.setParent(parent)
    layout.addWidget(TIMELINE_EDITS)



# -----------------------------------------------------------------------------
# Functions 
# -----------------------------------------------------------------------------

def get_maya_timeline():
    """
    Get the object name of Maya's timeline
    """
    return mel.eval('$tmpVar=$gPlayBackSlider')


def get_all_keyframes():
    """
    Get a list of all frames which have keys in the entire scene
    """
    anim_curves = cmds.ls(type="animCurve")
    all_key_frames = cmds.keyframe(anim_curves, query=True, timeChange=True)
    return sorted(list(set(all_key_frames)))


def get_last_keyframe():
    """
    Get last keyframe in scene
    """
    return int(get_all_keyframes()[-1])
     

def get_selection():
    """
    Get selected objects
    """
    return cmds.ls(sl=1)


def get_timeline_range():
    """
    Get current timeline selection and return it as a tuple (first_frame, last_Frame)
    """
    timeline_range = cmds.timeControl(get_maya_timeline(), query=True, rangeArray=True)
    return (int(timeline_range[0]), int(timeline_range[1]-1))


def to_qwidget(name):
    """
    Given the name of a Maya UI element, return the corresponding QWidget or
    QAction. If the object does not exist, return None
    """
    ptr = omui.MQtUtil.findControl(name)
    if ptr is None:
        ptr = omui.MQtUtil.findLayout(name)
    if ptr is None:
        ptr = omui.MQtUtil.findMenuItem(name)
    if ptr is not None:
        return wrapInstance(long(ptr), QtWidgets.QWidget)


def get_timeline_menu():
    """
    Get the QWidget of Maya's timeline menu
    """
    # Initialize timeline menu
    mel.eval("updateTimeSliderMenu TimeSliderMenu;")

    # Get time slider menu 
    timeline_menu = to_qwidget("TimeSliderMenu")
    return timeline_menu


def get_timeline():
    """ 
    Get the QWidget of Maya's timeline.
    """
    timeline_parent = to_qwidget(get_maya_timeline())

    for timeline in timeline_parent.children():
        if type(timeline) == QtWidgets.QWidget:
            return timeline 


# -----------------------------------------------------------------------------
# Timeline Edits 
# -----------------------------------------------------------------------------

class TimelineEdits(QtWidgets.QWidget):

    def __init__(self):

        # Get parent 
        QtWidgets.QWidget.__init__(self)

        self.setObjectName("timelineEdits")

        # Set Menu
        self.menu = TimelineEditsMenu(self)

        # Initialize 
        self.update()


    def update(self):
        QtWidgets.QWidget.update(self)
   
  
    def ripple_delete(self):
        """
        Takes the selected frame range in the timeline, deletes the keyframes and shifts everything 
        """
       
        # Identify the keys to be deleted 
        delete_range = get_timeline_range()

        # Identify the keys to be moved 
        move_range = (delete_range[1]+1,get_last_keyframe())

        # Calculate ripple length
        time_change = int(abs(delete_range[1] - delete_range[0])+1)

        # Identiy the selected objects 
        selection = get_selection()

        # Delete keys on selection
        cmds.cutKey(selection, time=delete_range)

        # Move frames 
        cmds.keyframe(selection, time=move_range, timeChange=-time_change, relative=True)


    def ripple_insert(self):
        """
        Takes the selected frame range in the timeline and shifts the animation to create a space
        """

        # Identify the expansion range 
        insert_range = get_timeline_range()

        # Identify the keys to be moved
        move_range = (insert_range[0], get_last_keyframe())

        # Calculate ripple length
        time_change = int(abs(insert_range[1] - insert_range[0])+1)

        # Identiy the selected objects 
        selection = get_selection()

        # Move frames 
        cmds.keyframe(selection, time=move_range, timeChange=time_change, relative=True)



# -----------------------------------------------------------------------------
# Timeline Edits Menu
# -----------------------------------------------------------------------------

class TimelineEditsMenu(object):

    def __init__(self, parent):
        # Get timeline menu
        self.menu = get_timeline_menu()

        # Add separator 
        self.add_separator()

        # Add buttons 
        self.add_button("Ripple Delete", parent.ripple_delete)
        self.ripple_insert_button = self.add_button("Ripple Insert", parent.ripple_insert)

        # Add separators
        self.add_separator()


    def add_separator(self):
        """
        Add separator to menu
        """
        separator = QtWidgets.QAction(self.menu)
        separator.setSeparator(True)

        self.menu.addAction(separator)
        return separator


    def add_button(self, label, command=None):
        """
        Add button QAction to menu
        """
        button = QtWidgets.QAction(self.menu)
        button.setText(label)

        if command:
            button.triggered.connect(command)
        
        self.menu.addAction(button)
        return button

    









        
    

