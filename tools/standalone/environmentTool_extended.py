# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: To import latest environment 
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

# shiboken
from shiboken2 import wrapInstance

# os
import os

#ncTools
from ncTools.mods import animMod

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
# UI
# -----------------------------------------------------------------------------

class EnvironmentTool_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "Environment Tool"
    UI_NAME = "environment_tool"
    WINDOWS = [WINDOW_NAME, UI_NAME]


    def __init__(self, *args, **kwargs):
        super(EnvironmentTool_UI, self).__init__(*args, **kwargs)

        G.area_cube_name = "EnvironmentToolAreaSphere"
        G.area_max = 10000
        G.area_min = 0
        G.area_value = 3000
        G.auto_reduce = False
        G.map_directory = get_map_directory()
        G.map_file = None
        G.material = "{x}_lambert".format(x=G.area_cube_name)
        G.shader_group = "{x}SG".format(x=G.material)
    

    def __getattr__(self, attr):
        return None 


    def start(self):
        self.delete_windows()
        self.create_window()
        self.show()
        

    def delete_windows(self):
        # Delete all windows 
        for window in self.WINDOWS:
            if cmds.window(window, query=True, exists=True):
                cmds.deleteUI(window)
    

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
        self.instruction_text = label(label="Use this tool to import a map and then reduce the area to include only what is necessary.", size=(300,30))
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

        # Add text description for 
        self.area_text = label(label="Adjust this value to include all objects this distance from the origin and cutscene activity actor.", size=(300,40))
        self.area_text.setContentsMargins(0, 10, 0, 0)
        self.display_grid.addWidget(self.area_text, 3, 0, 1, 12)

        # Add area distance text
        self.area_distance = label(label="Area Distance:  ", size=(75,15), align="left")
        self.display_grid.addWidget(self.area_distance, 4, 0, 1, 3)

        # Add area slider
        self.area_slider = slider_horizontal(value=G.area_value, max=G.area_max, min=G.area_min)
        self.area_slider.setTracking(True)
        self.area_slider.valueChanged.connect(self.on_area_slider_changed)
        self.display_grid.addWidget(self.area_slider, 4, 3, 1, 7)

        # Add area value box 
        self.area_value_box = spin_box(size=(50,25), value=G.area_value, max=G.area_max, min=G.area_min)
        self.area_value_box.valueChanged.connect(self.on_area_value_changed)
        self.display_grid.addWidget(self.area_value_box, 4, 10, 1, 2)

        # Add tick box to show area cube 
        self.cube_check_box = check_box(label="Show Area Sphere", size=(75,25))
        if cmds.objExists(G.area_cube_name):
            self.cube_check_box.setChecked(True)
        self.cube_check_box.stateChanged.connect(self.on_area_cube_check_changed)
        self.display_grid.addWidget(self.cube_check_box, 5, 0, 1, 3)

        # Add tick box to show area cube 
        self.auto_reduce_box = check_box(label="Auto reduce to area", size=(125,25))
        self.auto_reduce_box.setChecked(False)
        self.auto_reduce_box.stateChanged.connect(self.on_auto_reduce_check_changed)
        self.display_grid.addWidget(self.auto_reduce_box, 5, 7, 1, 5)

        # Add import button
        self.import_map_button = push_button(label="Import Map", size=(100,25))
        self.import_map_button.clicked.connect(G.environment_tool.import_map)
        self.display_grid.addWidget(self.import_map_button, 15, 0, 1, 4)

        # Add reduce button
        self.reduce_button = push_button(label="Reduce Map", size=(100,25))
        self.reduce_button.clicked.connect(G.environment_tool.reduce_map)
        self.display_grid.addWidget(self.reduce_button, 15, 4, 1, 4)

        # Add delete button
        self.delete_map_button = push_button(label="Delete Map", size=(100,25))
        self.delete_map_button.clicked.connect(G.environment_tool.delete_map)
        self.display_grid.addWidget(self.delete_map_button, 15, 8, 1, 4)


    def on_open_button_clicked(self):
        # Get file name
        G.map_name = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open file', dir=G.map_directory)[0]

        # If there is a filename display it in import file line edit
        if G.map_name:
            self.open_file_line_edit.setText(G.map_name)


    def on_area_slider_changed(self):
        # Get slider value
        G.area_value = self.area_slider.value()
        
        #Update spinbox value
        self.area_value_box.setValue(G.area_value)

        # Update cube scale
        self.update_cube_scale()


    def on_area_value_changed(self):
        # Get spin box value
        G.area_value = self.area_value_box.value()

        # Update slider
        self.area_slider.setValue(G.area_value)

        # Update cube scale
        self.update_cube_scale()


    def on_auto_reduce_check_changed(self):
        G.auto_reduce = self.auto_reduce_box.isChecked()


    def on_area_cube_check_changed(self):
        checked = self.cube_check_box.isChecked()
        if checked == True:  
            if cmds.objExists(G.area_cube_name) != True:        
                #area_cube = cmds.polySphere(n=G.area_cube_name, r=1)
                area_cube = cmds.polyCube(n=G.area_cube_name, w=2, h=2, d=2)
                self.apply_cube_shader()
                self.update_cube_scale()              
        else:
            if cmds.objExists(G.area_cube_name):
                cmds.delete(G.area_cube_name)
            if cmds.objExists(G.material):
                cmds.delete(G.material)
            if cmds.objExists(G.shader_group):
                cmds.delete(G.shader_group)


    def update_cube_scale(self):
        if cmds.objExists(G.area_cube_name):
            cmds.setAttr("{a}.scaleX".format(a=G.area_cube_name), G.area_value)
            cmds.setAttr("{a}.scaleY".format(a=G.area_cube_name), G.area_value)
            cmds.setAttr("{a}.scaleZ".format(a=G.area_cube_name), G.area_value)


    def apply_cube_shader(self):
        # Create material
        if cmds.objExists(G.material):
            cmds.delete(G.material)
        cmds.shadingNode('lambert', name=G.material, asShader=True)
        cmds.setAttr("{n}.color".format(n=G.material), 0, 1, 0, type="double3")
        cmds.setAttr("{n}.transparency".format(n=G.material), 0.6, 0.6, 0.6, type="double3")

        # Create shading group
        if cmds.objExists(G.shader_group):
            cmds.delete(G.shader_group)
        G.shader_group = cmds.sets(name=G.shader_group, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr("{n}.outColor".format(n=G.material), "{n}.surfaceShader".format(n=G.shader_group))

        # Apply 
        cmds.sets(G.area_cube_name, e=True, forceElement=G.shader_group)
        









# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------

class EnvironmentTool(object):

    def __init__(self, *args, **kwargs):
        G.environment_tool = self
        G.environment_group = "EnvironmentToolImportGroup"
        G.cleanup = ['LOD', 'Character', 'FirstPerson', 'Skeletal', 'border', 'icon', 'NODE', 'WBX', 'Volume', 'Default_Floor', 'FBXASC']


    def set_fbx_properties(self):
        mel.eval('FBXImportCameras -v false')
        mel.eval('FBXImportCameras -v false')
        mel.eval('FBXImportConstraints -v false')
        mel.eval('FBXImportFillTimeline -v false')
        mel.eval('FBXImportLights -v false')
        mel.eval('FBXImportSetMayaFrameRate -v false')
        mel.eval('FBXImportAudio -v false')


    @animMod.undo_chunk
    def import_map(self):
        # Set properties for fbx 
        self.set_fbx_properties()
        print "FBX properties set"

        # Import map fbx
        import_objects = cmds.file(G.map_name, i=True, groupName=G.environment_group, groupReference=True, preserveReferences=True, importTimeRange="combine", ignoreVersion=True, mergeNamespacesOnClash=False, returnNewNodes=True, type="FBX")
        # print "Imported map"

        # Get activity actor 
        G.activity_actor = self.get_activity_actor(import_objects)
        # print "Got activity actor"

        # Get scene_geometry
        scene_geometry = self.get_scene_geometry(import_objects)
        # print "Get scene geometry"

        # Reparent scene geometry to acitivity actor
        self.reparent_geometry(scene_geometry, G.activity_actor)
        # print "Geometry reparented"

        # Delete old group 
        pm.delete(G.environment_group)
        # print "Old group deleted"
        
        # Zero transforms
        pm.xform(G.activity_actor, ws=True, a=True, t=[0,0,0], ro=[0,0,0])
        pm.group(G.activity_actor, n="Environment_GRP")
        # print "Zeroed geometry"

        # If auto reduce is checked 
        if G.auto_reduce == True:
            self.reduce_map()
            print "Map reduced"

        # Cleanup map
        self.clean_map()
        #print "Cleaned map"


    def get_activity_actor(self, import_objects):
        # Search through list of import objects to get activity actor 
        for obj in pm.listRelatives(import_objects, ad=True, pa=True):
            if 'ActivityActor' in str(obj):
                activity_actor = obj
                # Parent the activity actor to world space
                pm.parent(activity_actor, w=True)
                return activity_actor


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


    def reparent_geometry(self, child, parent):
        pm.parent(child, parent)
        

    def clean_map(self):
        delete_object = []
        for obj in pm.listRelatives(G.activity_actor, c=True):            
            for tag in G.cleanup:
                if tag in str(obj):
                    print obj
                    delete_object.append(obj)
        list(set(delete_object))
        pm.delete(delete_object)
      


    @animMod.undo_chunk
    def delete_map(self):
        pm.delete("Environment_GRP")


    @animMod.undo_chunk
    def reduce_map(self):
        G.activity_actor = pm.ls(sl=1)[0]
        self.clean_map()
        for obj in pm.ls(sl=1):
            print obj
            faces = obj.faces
            for f in faces:
                pos = pm.xform(f, q=True, ws=True, t=True)
                print pos
                result_in_area = True in (abs(xyz) < G.area_value for xyz in pos)
                if result_in_area == False:
                    print obj
                    print "This object can be deleted"


'''
Wishlist
--- Add function to search over faces and if none in the safe zone delete the object:
--- Add function to export a mobu ready file 
--- Add function to get file name based on import fbx 
--- Add function to add map to asset library
'''
