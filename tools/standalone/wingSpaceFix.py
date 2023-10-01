# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: To fix the spacing on wings so that crowd are able to use
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel
from functools import wraps

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets

# shiboken
from shiboken import wrapInstance

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class WingSpaceFixGlobals(object):

    def __getattr__(self, attr):
        return None

G = WingSpaceFixGlobals()

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

SPACE_DICT = {  "wingFKA_CTRL"                :       "Clavicle",
                "wingPrimariesOuter_CTRL"     :       "Default",
                "wingSecondariesOuter_CTRL"   :       "Interp",
                "wingSecondariesInner_CTRL"   :       "WingFKA",
                "wingPV_CTRL"                 :       "wingJA",
                "secMidCTweak_CTRL"           :       "Default",
                "secMidBTweak_CTRL"           :       "Default",
                "wingElbowTweak_CTRL"         :       "WingFKA",
                "secInnerATweak_CTRL"         :       "Default",
                "secOuterATweak_CTRL"         :       "Default",
                "primOuterATweak_CTRL"        :       "Default",
}

# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------

def viewport_off(func):
    """
    Decorator to turn off viewport_off
    """
    @wraps(func)
    def wrap(*args, **kwargs):

        # Turn off main panel:
        mel.eval("paneLayout -e -manage false $gMainPane")

        try:
            return func(*args, **kwargs)
        except Exception:
            raise # will raise original setVerticalScrollBar
        finally:
            mel.eval("paneLayout -e -manage true $gMainPane")

    return wrap

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def get_main_window():
    pointer = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(long(pointer), QtWidgets.QMainWindow)
    return main_window

def show():
    G.wingSpaceFix = WingSpaceFix_UI(parent=get_main_window())
    G.wingSpaceFix.start()

def label(label="Label", width=200, height=15, font_size=8, align="left", word_wrap=True):
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
        text.setAlignment(QtCore.Qt.AlignRight)
    text.setFont(font)
    return text

def push_button(label="Button", size = (200, 25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    button = QtWidgets.QPushButton(label)
    button.setMinimumSize(*size)
    button.setMaximumSize(*size)
    button.setFont(font)
    return button

def divider():
    divider = QtWidgets.QLabel("")
    divider.setStyleSheet("QLabel {background-color: #3e3e3e; padding: 0; margin: 0; border-bottom: 1 solid #666; border-top: 1 solid #2a2a2a;}")
    divider.setMaximumHeight(2)
    return divider

def line_edit(size=(25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    line_edit = QtWidgets.QLineEdit()
    line_edit.setMinimumSize(*size)
    line_edit.setMaximumSize(*size)
    line_edit.setFont(font)
    return line_edit

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
class WingSpaceFix_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "Fix Wings For Crowd"
    UI_NAME = "fix_wings_for_crowd"
    WINDOWS = [WINDOW_NAME, UI_NAME]

    def __init__(self, *args, **kwargs):
        super(WingSpaceFix_UI, self).__init__(*args, **kwargs)

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
        wingSpaceFix = WingSpaceFix()

        # Set object name and window title
        self.setObjectName(self.UI_NAME)
        self.setWindowTitle(self.WINDOW_NAME)

        # Create central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)
        self.central_widget.setLayout(self.main_layout)

        # Add widgets
        self.select_rig_label = label(label="Select the rig")
        self.main_layout.addWidget(self.select_rig_label)

        self.select_grid = QtWidgets.QWidget()
        self.select_grid_layout = QtWidgets.QGridLayout()
        self.select_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.select_grid_layout.setSpacing(0)
        self.select_grid.setLayout(self.select_grid_layout)
        self.main_layout.addWidget(self.select_grid)

        self.select_button = push_button(label = ">", size=(25,25))
        self.select_button.clicked.connect(self.update_selected_rig)
        self.select_button.clicked.connect(wingSpaceFix.get_selected_namespace)
        self.select_grid_layout.addWidget(self.select_button, 1, 0, 1, 1)

        self.select_display = line_edit(size=(175,25))
        self.select_display.setReadOnly(True)
        self.select_grid_layout.addWidget(self.select_display, 1, 1, 1, 1)

        self.run_button = push_button(label = "RUN")
        self.run_button.clicked.connect(wingSpaceFix.run)
        self.main_layout.addWidget(self.run_button)

        sizeHint = self.sizeHint()
        self.setMaximumSize(sizeHint)

    # -----------------------------------------------------------------------------
    # Button clicked functions / UI updates
    # -----------------------------------------------------------------------------

    def update_selected_rig(self):
        selection = cmds.ls(sl=1)
        rig = selection[0].rpartition(":")[0]
        self.select_display.setText(rig)

# -----------------------------------------------------------------------------
# Tool
# -----------------------------------------------------------------------------

class WingSpaceFix(object):

    def __init__(self):
        if G.wingSpaceFix.wingSpaceFix:
            return
        G.wingSpaceFix.wingSpaceFix = self

    @viewport_off
    def run(self):
        cmds.undoInfo(ock=True)
        print "FIXING"
        #1. Get the selected rig namespace
        self.get_selected_namespace()

        #2. Get the controls that need to be fixed
        self.get_controls(self.namespace)

        #3. Get the frame range for the scene
        self.get_frames()

        #4. Create a locator for the controls that need to be fixed
        self.create_locators()

        #5. Parent the locators to the controls
        for control in self.controls_locs:
            locator = self.controls_locs[control]
            self.parent(parent=control, child=locator)

        #6. Bake the locators
        self.bake(self.locators)

        #7. Parent controls to locators
        for control in self.controls_locs:
            locator = self.controls_locs[control]
            self.parent(parent=locator, child=control)

        #8. Change spacing on controls
        self.change_spaces()

        #9. Bake the controls
        self.bake(self.controls)

        #10. Delete the locators
        cmds.delete(self.locators)

        #11. Euler filter on controls
        self.euler_filter(self.controls)

        print "COMPLETE"
        cmds.undoInfo(cck=True)




    def get_selected_namespace(self):
        selection = cmds.ls(sl=1)[0]
        self.namespace = selection.rpartition(":")[0]


    def get_controls(self, namespace):
        self.controls = []
        self.controls_spaces = {}
        for control in SPACE_DICT:
            for direction in ["l_", "r_"]:
                control_name = "{namespace}:{direction}{control}".format(namespace=self.namespace, direction=direction, control=control)
                space = SPACE_DICT[control]
                self.controls.append(control_name)
                self.controls_spaces[control_name] = space


    def euler_filter(self, controls):
        curves = cmds.ls(controls, l=True)
        cmds.filterCurve(curves)

    def create_locators(self):
        self.locators = []
        self.controls_locs = {}
        for control in SPACE_DICT:
            for direction in ["l_", "r_"]:
                control_name = "{namespace}:{direction}{control}".format(namespace=self.namespace, direction=direction, control=control)
                space = SPACE_DICT[control]
                locator_name = "{control_name}_LOC".format(control_name=control_name)
                if cmds.objExists(control_name):
                    cmds.spaceLocator(name=locator_name)
                    self.controls_locs[control_name] = locator_name
                    self.locators.append(locator_name)

    def parent(self, parent=None, child=None):
        axis = ["x", "y", "z"]

        orient_skip = []
        for xyz in axis:
            attribute = "rotate{xyz}".format(xyz=xyz.upper())
            attr = cmds.listAttr(child, k=True, st=[attribute])
            if attr is None:
                orient_skip.append(xyz)
        try:
            cmds.orientConstraint(parent, child, skip=orient_skip, mo=False)
        except:
            pass

        point_skip = []
        for xyz in axis:
            attribute = "rotate{xyz}".format(xyz=xyz.upper())
            attr = cmds.listAttr(child, k=True, st=[attribute])
            if attr is None:
                orient_skip.append(xyz)
        try:
            cmds.pointConstraint(parent, child, skip=point_skip, mo=False)
        except:
            pass

    def change_spaces(self):
        for control in self.controls_spaces:
            space = self.controls_spaces[control]
            for attribute in ["Space", "space"]:
                cmds.cutKey(control, at=attribute)
                try:
                    self.set_enum_with_string(control, attribute, space)
                    cmds.setKeyframe(control, at=attribute)
                except:
                    pass



    def set_enum_with_string(self, node, attribute, value):
        enum_string = cmds.attributeQuery(attribute, node=node, listEnum=1)[0]
        enum_list = enum_string.split(":")
        index = enum_list.index(value)
        cmds.setAttr(node+"."+attribute, index)


    def get_frames(self):
        self.current_frame = int(cmds.currentTime(query=True))
        self.min_time = int(cmds.playbackOptions(query = True, min=True))
        self.max_time = int(cmds.playbackOptions(query=True, max=True))
        self.frames = list(range(self.min_time, self.max_time+1))

    def bake(self, objects):
        for frame in self.frames:
            cmds.currentTime(frame)
            for obj in objects:
                cmds.setKeyframe(obj)
                try:
                    cmds.setAttr(obj+".blendParent1", 1)
                except:
                    pass
                try:
                    cmds.setAttr(obj+".blendOrient1", 1)
                except:
                    pass
                try:
                    cmds.setAttr(obj+".blendPoint1", 1)
                except:
                    pass
        cmds.currentTime(self.current_frame)
        cmds.delete(objects, cn=True)
