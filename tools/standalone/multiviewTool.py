# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: To duplicate the animated model to allow for multiviews in playblast.
# -----------------------------------------------------------------------------
# Wishlist
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya 
from unicodedata import name
from maya import cmds 
from maya import OpenMayaUI as omui
from maya import mel as mel 

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# Pymel
import pymel.core as pm 

# Traceback
import traceback

# shiboken
from shiboken2 import wrapInstance

# os
import os

# functools
from functools import wraps

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------

class MultiviewToolGlobals(object):

    def __getattr__(self, attr):             
        return None

G = MultiviewToolGlobals()

# -----------------------------------------------------------------------------
# Contants
# -----------------------------------------------------------------------------
VIEWS = {
    "left" : {
        "name": "Left",
        "translate": (-300, 0, 0),
        "rotate": (0, 0, 90)
    },
    "right" : {
        "name": "Right",
        "translate": (300, 0, 0),
        "rotate": (0, 0, -90)
    },
    "left_front" : {
        "name": "Left Front",
        "translate": (-300, 0, 300),
        "rotate": (0, 0, 45)
    },
    "right_front" : {
        "name": "Right Front",
        "translate": (300, 0, 300),
        "rotate": (0, 0, -45)
    },
    "top" : {
        "name": "Top",
        "translate": (100, 0, 300),
        "rotate": (90, 0, 0)
    },
    "bottom" : {
        "name": "Bottom",
        "translate": (-100, 0, 300),
        "rotate": (-90, 0, )
    },
    "back" : {
        "name": "Back",
        "translate": (200, 0, 300),
        "rotate": (0, 0, 180)
    },
    "back_left" : {
        "name": "Back Left",
        "translate": (-300, 0, 0),
        "rotate": (0, 0, 135)
    },
    "back_right" : {
        "name": "Back Right",
        "translate": (300, 0, 0),
        "rotate": (0, 0, -135)
    }
}

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def get_main_window():
    pointer = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(long(pointer), QtWidgets.QMainWindow)
    return main_window

def show(mode="refresh"):
    G.multiviewTool = G.multiviewTool or MultiviewTool_UI()
    if mode == "refresh":
        G.multiviewTool = MultiviewTool_UI(parent=get_main_window())
        G.multiviewTool.start()

# -----------------------------------------------------------------------------
# UI FUNCTIONS (usually stored in ncTools.uiMod)
# -----------------------------------------------------------------------------
def checkbox(label="Checkbox", size=(25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    checkbox = QtWidgets.QCheckBox(label)
    checkbox.setMinimumSize(*size)
    checkbox.setMaximumSize(*size)
    checkbox.setFont(font)
    return checkbox


def horizontal_line(size=(100,2)):
    divider = QtWidgets.QFrame()
    divider.setFrameShape(QtWidgets.QFrame.HLine)
    divider.setFrameShadow(QtWidgets.QFrame.Sunken)
    divider.setFixedSize(*size)
    return divider


def label(label="Label", size=(100,25), font_size=8, align="left", word_wrap=True):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    text = QtWidgets.QLabel(label)
    text.setMinimumSize(*size)
    text.setMaximumSize(*size)
    text.setWordWrap(word_wrap)
    if align == "left":
        text.setAlignment(QtCore.Qt.AlignLeft)
    elif align == "center":
        text.setAlignment(QtCore.Qt.AlignCenter)
    elif align == "right":
        text.setAlignment(QtCore.Qt.AlignRight)
    text.setFont(font)
    return text


def push_button(label="Button", size=(200,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    button = QtWidgets.QPushButton(label)
    button.setMinimumSize(*size)
    button.setMaximumSize(*size)
    button.setFont(font)
    return button


# -----------------------------------------------------------------------------
# Decorators (usually stored in ncTools.animMod)
# -----------------------------------------------------------------------------
def undo(function):
    """
    Decorator to undo the function, use by adding @undo one line above any function.
    """
    @wraps(function)
    def _undofunc(*args, **kwargs):
        try:
            # Open undo chunk
            pm.undoInfo(openChunk=True)
            return function(*args, **kwargs)
        except Exception as e:
            # If error, print the error
            print (traceback.format_exc())
            
        finally:
            # Close the chunk 
            pm.undoInfo(closeChunk=True)

    return _undofunc 

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
class MultiviewTool_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "Multiview Tool"
    UI_NAME = "multiview_tool"
    WINDOWS = [WINDOW_NAME, UI_NAME]

    def __init__(self, *args, **kwargs):
        super(MultiviewTool_UI, self).__init__(*args, **kwargs)
   

    def __getattr__(self, attr):
        return None 


    def start(self):
        self.delete_windows()
        self.create_window()
        self.show()


    def delete_windows(self):
        # Delete all windows 
        for window in self.WINDOWS:
            if pm.window(window, query=True, exists=True):
                pm.deleteUI(window)
    

    def create_window(self):
        # Create instance of tool
        multiview_tool = MultiviewTool()

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

        # Create display layout
        self.display_widget = QtWidgets.QWidget()
        self.main_layout.addWidget(self.display_widget)
        self.display_grid = QtWidgets.QGridLayout()
        self.display_grid.setSpacing(5)
        self.display_grid.setContentsMargins(0, 0, 0, 0)
        self.display_widget.setLayout(self.display_grid)

        # Add buttons 
        self.add_widgets()

        # Set size 
        size_hint = self.sizeHint()
        self.setMaximumSize(size_hint)

    def add_widgets(self):
        # Add buttons to display grid layout of main window 
       
        # Add instructions 
        row = 0
        self.instruction_text = label(
            label="Use this tool to create duplicate instances of a rig to view from multiple angles.", 
            size=(310,40)
            )
        self.display_grid.addWidget(self.instruction_text, row, 0, 1, 12)

        # Create camera button 
        row +=1
        self.create_camera_button = push_button(label="Create Multiview Camera", size=(310,25))
        self.create_camera_button.clicked.connect(G.multiview_tool.create_multiview_camera)
        self.display_grid.addWidget(self.create_camera_button, row, 0, 1, 12)

        # Create select rig geo
        row +=1
        self.select_rig_geo_button = push_button(label="Select rig geometry", size=(310,25))
        self.select_rig_geo_button.clicked.connect(G.multiview_tool.select_rig_geo)
        self.display_grid.addWidget(self.select_rig_geo_button, row, 0, 1, 12)

        # Duplicate special 
        row +=1
        self.duplicate_special_button = push_button(label="Duplicate special", size=(310,25))
        self.duplicate_special_button.clicked.connect(G.multiview_tool.duplicate_special_selected)
        self.display_grid.addWidget(self.duplicate_special_button, row, 0, 1, 12)

        # Add divider
        row +=1
        self.divider01 = horizontal_line(size=(310,2))
        self.display_grid.addWidget(self.divider01, row, 0, 1, 12)

        # Add instructions 
        row +=1
        self.instruction_text = label(
            label="Change the orientation of the selected duplicate. These are just shortcuts.", 
            size=(310,40)
            )
        self.display_grid.addWidget(self.instruction_text, row, 0, 1, 12)

        # Create view options 
        row +=1
        column = 0
        for view in sorted(VIEWS):
            view_button = push_button(label=VIEWS[view]["name"], size=(100,25))
            self.display_grid.addWidget(view_button, row, column, 1, 4)
            column += 4
            if column >= 12:
                row += 1
                column = 0




    #---------------------------------------------------------------------------
    # Button clicked functions / UI updates
    # --------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------

class MultiviewTool(object):

    def __init__(self, *args, **kwargs):
        G.multiview_tool = self
        G.multiview_group = "MultiviewGroup"
        G.multiview_display_layer = "Multiview"
        G.multiview_camera = "MultiviewCamera"
        G.rig_geo = []

        # Setup Multiview Namespace
        G.namespace = "Multiview"
        self.create_namespace(G.namespace)



    def create_namespace(self, namespace):
        # Check to see if namespace exists: 
        print namespace
        if pm.namespace(exists=namespace):
            pass
        else:
            new_namespace = pm.namespace(add=namespace)

        


    def create_multiview_camera(self):
        # Check to see if multiview camera exists
        if pm.objExists(G.multiview_camera):
            pm.delete(G.multiview_camera)
        else:
            pass

        # Create a perspective camera 
        camera_multiview = pm.camera(focalLength=500, nearClipPlane=10, farClipPlane=100000) 

        # Rename camera 
        pm.rename(camera_multiview[0], G.multiview_camera)

        # Position camera 
        pm.xform(G.multiview_camera, worldSpace=True, absolute=True, translation=(0, -15000, 250), rotation=(90, 0, 0))

        # Lock the multiview camera
        for attribute in ["translate", "rotate"]:
            for axis in ["X", "Y", "Z"]:
                camera_attr = "{0}.{1}{2}".format(G.multiview_camera, attribute, axis)
                try: 
                    pm.setAttr(camera_attr, lock=True)
                except:
                    pass
        
        # Look through camera 
        cmds.lookThru(G.multiview_camera)

    def select_rig_geo(self):
        # Identify selected namespaces 
        selected_namespaces = self.get_selected_namespaces()

        # Get geo associated with namespaces
        G.rig_geo = []
        for namespace in selected_namespaces:
            geo = self.get_namespace_geo(namespace)
            for obj in geo:
                G.rig_geo.append(obj)

        G.rig_geo = list(set(G.rig_geo))

        # Select geo
        pm.select(G.rig_geo)


    def get_selected_namespaces(self):
        selected = self.get_selected()

        selected_namespaces = []
        for obj in selected:
            namespace = self.get_namespace(obj)
            selected_namespaces.append(namespace)
        selected_namespaces = list(set(selected_namespaces))
        return selected_namespaces

    def duplicate_special_selected(self):
        instance = pm.instance(G.rig_geo)
        instance_group = pm.group(instance, world=True, name="Duplicate")
        duplicate_ctrl = self.create_control()
        # Parent duplicate group beneath control
        print duplicate_ctrl
        pm.parent(instance_group, "Duplicate_CTRL")

    def create_control(self):
        control = pm.circle(name="Duplicate_CTRL")
        print "Make control", control
        return control




        



    def get_selected(self):
        selected = pm.ls(sl=1)
        return selected


    def get_namespace(self, node):
        namespace = node.rpartition(":")[0]
        return namespace 

    
    def get_namespace_geo(self, namespace):
        namespace_geo = []
        namespace_groups = []
        assemblies = pm.ls(assemblies=1)
        for group in pm.ls(assemblies=1):
            if namespace in group.name():
                namespace_groups.append(group)
        namespace_shapes = pm.listRelatives(namespace_groups, allDescendents=True, type="mesh")
        for shape in namespace_shapes:
            shape_parents = pm.listRelatives(shape, ap=True)
            for shape_parent in shape_parents:
                namespace_geo.append(shape_parent)
        return namespace_geo




    def get_scene_rigs(self):
        scene_rigs = []
        assemblies = cmds.ls(assemblies=1)
        for node in assemblies: 
            print node
            if node.endswith("rig_grp"):
                scene_rigs.append(node)
        scene_rigs = list(set(scene_rigs))
        return scene_rigs







    


    

