# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: To import latest environment from fbx, clean up and orient around activity actor
# -----------------------------------------------------------------------------
# Wishlist
# --- Add function to search over faces and if none in the safe zone delete the object:
# --- Add function to export a mobu ready file 
# --- Add function to get file name based on import fbx 
# --- Add function to add map to asset library
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
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

class EnvironmentToolGlobals(object):

    def __getattr__(self, attr):             
        return None

G = EnvironmentToolGlobals()



# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def get_main_window():
    pointer = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(long(pointer), QtWidgets.QMainWindow)
    return main_window

def show(mode="refresh"):
    G.environmentTool = G.environmentTool or EnvironmentTool_UI()
    if mode == "refresh":
        G.environmentTool = EnvironmentTool_UI(parent=get_main_window())
        G.environmentTool.start()

def get_map_directory():
    # Get Maps directory based on current scene 
    current_maya_file = cmds.file(q=True, sn=True)
    cutscene_directory = os.path.dirname(current_maya_file)
    map_directory = "{cutscene_directory}/Maps".format(cutscene_directory=cutscene_directory)
    return map_directory

# UI FUNCTIONS (usually stored in ui.Mod)
def check_box(parent=None, label="", size=(25,25)):
    check_box = QtWidgets.QCheckBox(label, parent=parent)
    check_box.setMinimumSize(*size)
    check_box.setMaximumSize(*size)
    return check_box

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

def line_edit(size=(25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    line_edit = QtWidgets.QLineEdit()
    line_edit.setMinimumSize(*size)
    line_edit.setMaximumSize(*size)
    line_edit.setFont(font)
    return line_edit
    
def push_button(label="Button", size=(200,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    button = QtWidgets.QPushButton(label)
    button.setMinimumSize(*size)
    button.setMaximumSize(*size)
    button.setFont(font)
    return button

def slider_horizontal(value=0, min=0, max=1000):
    slider = QtWidgets.QSlider()
    slider.setOrientation((QtCore.Qt.Horizontal))  
    slider.setRange(min, max)
    slider.setValue(value)
    return slider

def spin_box(size=(200,25), value=0, min=0, max=1000):
    box = QtWidgets.QSpinBox()
    box.setRange(min, max)
    box.setValue(value)
    return box

def text_edit(size=(25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    text_edit = QtWidgets.QTextEdit()
    text_edit.setMinimumSize(*size)
    text_edit.setMaximumSize(*size)
    text_edit.setFont(font)
    return text_edit

def tool_button(icon=":fileOpen.png", size=(25,25)):
    button = QtWidgets.QToolButton()
    button.setFixedSize(*size)
    button.setIcon(QtGui.QIcon(icon))
    button.setIconSize(QtCore.QSize(*size))
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

class EnvironmentTool_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "Environment Tool"
    UI_NAME = "environment_tool"
    WINDOWS = [WINDOW_NAME, UI_NAME]


    def __init__(self, *args, **kwargs):
        super(EnvironmentTool_UI, self).__init__(*args, **kwargs)

        G.map_directory = get_map_directory()
        G.map_file = None
        G.selected_objects = []
    

    def __getattr__(self, attr):
        return None 


    def start(self):
        self.delete_windows()
        self.create_window()
        #self.setup_script_job()
        #self.update_selections()
        self.show()
        

    def delete_windows(self):
        # Delete all windows 
        for window in self.WINDOWS:
            if pm.window(window, query=True, exists=True):
                pm.deleteUI(window)
    

    def create_window(self):
        # Create instance of tool
        environment_tool = EnvironmentTool()

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
        self.instruction_text = label(label="Use this tool to import a fbx map and position it in relation to the cutscene activity actor. This can take a short while so be patient.", size=(310,40))
        self.display_grid.addWidget(self.instruction_text, 0, 0, 1, 12)
        
        # Add Import map text
        self.import_map_label = label(label="Import Map:  ", size=(75,15), align="left")
        self.display_grid.addWidget(self.import_map_label, 1, 0, 1, 3)

        # Add line edit for file path
        self.open_file_line_edit = line_edit(size=(200,25))
        if G.map_name:
            self.open_file_line_edit.setText(G.map_name)
        self.display_grid.addWidget(self.open_file_line_edit, 1, 3, 1, 8)

        # Add open file button
        self.open_file_button = tool_button(icon=":/fileOpen.png", size=(25,25))
        self.open_file_button.clicked.connect(self.on_open_button_clicked)
        self.display_grid.addWidget(self.open_file_button, 1, 11, 1, 1)

        # Add import button
        self.import_map_button = push_button(label="Import Map", size=(310,25))
        self.import_map_button.clicked.connect(G.environment_tool.import_map)
        self.display_grid.addWidget(self.import_map_button, 2, 0, 1, 12)

        # Add divider
        self.divider01 = horizontal_line(size=(310,2))
        self.display_grid.addWidget(self.divider01, 3, 0, 1, 12)
        """
        # Add mocap assets label
        self.mocap_assets_label = label(label="Select objects and add them to the mocap/mobu export group", size=(310,40), align="left")
        self.display_grid.addWidget(self.mocap_assets_label, 4, 0, 1, 12)

        # Add select object display
        self.selected_objects_display = line_edit(size=(310,25))
        self.display_grid.addWidget(self.selected_objects_display, 5, 0, 1, 12)

        # Add mocap group buttons
        self.mocap_group_add_button = push_button(label=("Add to Mocap Env"), size=(150, 25))
        self.mocap_group_add_button.clicked.connect(G.environment_tool.add_to_mocap_group)
        self.display_grid.addWidget(self.mocap_group_add_button, 6, 0, 1, 6)

        self.mocap_group_remove_button = push_button(label=("Remove from Mocap Env"), size=(150, 25))
        self.mocap_group_remove_button.clicked.connect(G.environment_tool.remove_from_mocap_group)
        self.display_grid.addWidget(self.mocap_group_remove_button, 6, 6, 1, 6)
        """


    #---------------------------------------------------------------------------
    # Button clicked functions / UI updates
    # --------------------------------------------------------------------------
    def setup_script_job(self):
        """
        Procedure to create a script job that will update the UI when
        selections change
        """

        JOB_number = pm.scriptJob(e=["SelectionChanged", self.update_selections], cu=True, kws=True, rp=True, p=self.UI_NAME)


    def update_selections(self):
        """
        Procedure to update the UI based on the selection
        """

        selection = pm.ls(sl=1)
        G.selected_objects = selection
        print G.selected_objects
        self.selected_objects_display.setText(str(G.selected_objects))


    def on_open_button_clicked(self):
        # Get file name
        G.map_name = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open file', dir=G.map_directory)[0]

        # If there is a filename display it in import file line edit
        if G.map_name:
            self.open_file_line_edit.setText(G.map_name)

# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------

class EnvironmentTool(object):

    def __init__(self, *args, **kwargs):
        G.environment_tool = self
        G.environment_group = "EnvironmentToolImportGroup"
        G.environment_display_layer = "Environment"
        G.cleanup = ['LOD', 'Character', 'FirstPerson', 'Skeletal', 'border', 'icon', 'NODE', 'WBX', 'Volume', 'Default_Floor']
        #G.cleanup = []
        G.mocap_selection = []
        G.mocap_layer_name = "Mocap_Environment"
        G.mocap_layer = self.get_display_layer(layer_name=G.mocap_layer_name) or None


#--------------------------------------------------------------------------
# Import Map Functions 
#--------------------------------------------------------------------------
    def set_fbx_properties(self):
        mel.eval('FBXImportCameras -v false')
        mel.eval('FBXImportCameras -v false')
        mel.eval('FBXImportConstraints -v false')
        mel.eval('FBXImportFillTimeline -v false')
        mel.eval('FBXImportLights -v false')
        mel.eval('FBXImportSetMayaFrameRate -v false')
        mel.eval('FBXImportAudio -v false')

    @undo
    def import_map(self):
        # Set properties for fbx import
        self.set_fbx_properties()

        # Import map fbx
        import_objects = cmds.file(G.map_name, i=True, groupName=G.environment_group, groupReference=True, preserveReferences=True, importTimeRange="combine", ignoreVersion=True, mergeNamespacesOnClash=False, returnNewNodes=True, type="FBX")

        # Get activity actor 
        G.activity_actor = self.get_activity_actor(import_objects)

        # Get scene_geometry
        G.scene_geometry = self.get_scene_geometry(import_objects)

        # Reparent scene geometry to acitivity actor
        pm.parent(G.scene_geometry, G.activity_actor)

        # Delete old import group 
        pm.delete(G.environment_group)
        
        # Zero transforms on activity actor
        pm.xform(G.activity_actor, ws=True, a=True, t=[0,0,0], ro=[0,0,0])

        # Put in a parent group that can be named
        pm.group(G.activity_actor, n="Environment_GRP")
        
        # Cleanup map
        self.clean_map()

        # Create environment display layer
        #environment_display = self.make_display_layer(layer_name="Environment", layer_colour=[1,1,0])

        # Add environment assets to display layer
        #self.add_assets_to_display_layer(assets=G.scene_geometry, layer_name="Environment")



    def get_activity_actor(self, import_objects):
        # Search through list of import objects to get activity actor 
        for obj in pm.listRelatives(import_objects, ad=True, pa=True):
            if 'ActivityActor' in str(obj):
                # Parent the activity actor to world space
                pm.parent(obj, w=True)
                return obj


    def get_scene_geometry(self, import_objects):
        # Get all shape nodes in scene, as this only gets one instance we will need to get parent tranform nodes to get all geometry.
        shapes = pm.ls(import_objects, dag=True, type="shape")
        # Array to store transform nodes
        geometry_transforms = []
        for shape in shapes:
            # Get all parents of shapes to include instances 
            shape_parents = pm.listRelatives(shape, ap=True)
            # Add each parent to geometry_transform array
            for shape_parent in shape_parents:
                geometry_transforms.append(shape_parent)
        return geometry_transforms


    def clean_map(self):
        delete_object = []
        objects = pm.listRelatives(G.activity_actor, c=True)         
        for obj in objects:  
            for tag in G.cleanup:
                if tag in str(obj):
                    G.scene_geometry.remove(obj)
                    delete_object.append(obj)
        list(set(delete_object))
        pm.delete(delete_object)


#--------------------------------------------------------------------------
# Mocap Export Functions 
#--------------------------------------------------------------------------
    def get_display_layer(self, layer_name):
        # Return display layer with specified layer_name otherwise return None.
        display_layers = pm.ls(long=True, type="displayLayer")
        for layer in display_layers:
            if layer == layer_name:
                return layer
            else:
                print "No layer with the name ", layer_name, " exists."
                return None

    def make_display_layer(self, layer_name, layer_colour):
        #Check if display layer with layer_name already exists, and if not create it.
        display_layer = self.get_display_layer(layer_name)
        if not display_layer:
            print "Making display layer called ", layer_name
            # Create display layer
            display_layer = pm.createDisplayLayer(name=layer_name, empty=True, makeCurrent=True)
            # Enable layer colour
            pm.setAttr("{}.color".format(display_layer), True)
            # Set layer to use RGB color
            pm.setAttr("{}.overrideRGBColors".format(display_layer), True)
            # Set the layer's color
            pm.setAttr("{}.overrideColorRGB".format(display_layer), *layer_colour)
        else:
            print "Display layer called", layer_name, "already exists. Returning layer"
        return display_layer


    def delete_display_layer(self, layer_name):
        # Check if display layer exists and then delete
        display_layer = self.get_display_layer(layer_name)
        if display_layer:
            pm.delete(display_layer)
        else:
            print "Display layer named ", layer_name, "does not exist."


    def add_assets_to_display_layer(self, assets, layer_name):
        # Add asset array to display layer 
        # Check if display_layer exists 
        display_layer = self.get_display_layer(layer_name=layer_name)
        # If layer name doesn't exist return error
        if not display_layer:
            print "There is no display layer named:", layer_name
        # If layer does exist add assets to it
        else:
            for asset in assets:
                print asset, pm.objectType(asset)
                # Check if asset exists, if true add to display_layer, if false print error
                if pm.objExists(asset):
                    pm.editDisplayLayerMembers(display_layer, asset, noRecurse=True)
                else:
                    print asset, "does not exist. Can't add it to", layer_name


    def remove_assets_from_display_layer(self, assets, layer_name):
        # Remove asset array from display layer
        # Check if display_layer
        display_layer = self.get_displayer_layer(layer_name=layer_name)
        # If layer doesn't exist print error 
        if not display_layer:
            print "There is no display layer named", layer_name
        else:
            for asset in assets:
                # Check if asset exists, if true remove it from display layer, if false print error
                if pm.objExist(asset):
                    pm.editDisplayLayerMembers("defaultLayer", asset, noRecurse=True)
                else:
                    print asset, "does not exist. Can't remove from", layer_name

    def add_to_mocap_group(self):
        # Does mocap display layer exist?
        if not G.mocap_layer:
            # Create mocap layer
            G.mocap_layer = self.make_display_layer(layer_name=G.mocap_layer_name, layer_colour=[1,0,1])
        else:
            print ("Mocap_Environment layer already exists; adding selected assets to layer")               
            
        # Add to mocap selection
        for obj in G.selected_objects:
            G.mocap_selection.append(obj)
        
            # Add mocap_selection to display layer
            pm.editDisplayLayerMembers(G.mocap_layer, obj, noRecurse=True)

    def remove_from_mocap_group(self):
        print ("Remove from mocap group")
        # Add to mocap selection
        for obj in G.selected_objects:
            if obj in G.mocap_selection:
                G.mocap_selection.remove(obj)
                # Add mocap_selection to display layer
                pm.editDisplayLayerMembers("defaultLayer", obj)
            else:
                print obj, "is not in mocap selection"
        




