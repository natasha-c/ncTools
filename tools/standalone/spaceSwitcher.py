# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: To switch space etc to same on all selected G.controls
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
import os
import re

# maya
from maya import OpenMayaUI as omui
from maya import cmds
from maya import mel
from functools import wraps

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# shiboken
from shiboken2 import wrapInstance

from functools import partial


# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class ncSpaceSwitcherGlobals(object):

    def __getattr__(self, attr):
        return None

G = ncSpaceSwitcherGlobals()


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
# UI Standard Sizes
WIDTH = 200
HEIGHT = 24
SPACING = 5


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

def show(mode="refresh"):
    G.UI = G.UI or NcSpaceSwitcher_UI()
    if mode == "refresh":
        G.UI = NcSpaceSwitcher_UI(parent=get_main_window())
        G.UI.start()

def label(label="Label", width=WIDTH, HEIGHT=HEIGHT/2, font_size=8, align="left", word_wrap=True):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    text = QtWidgets.QLabel(label)
    text.setMinimumSize(WIDTH, HEIGHT)
    text.setMaximumSize(WIDTH, HEIGHT)
    text.setWordWrap(word_wrap)
    if align == "left":
        text.setAlignment(QtCore.Qt.AlignLeft)
    elif align == "center":
        text.setAlignment(QtCore.Qt.AlignCenter)
    elif align == "right":
        text.setAlignment(QtCore.Qt.AlignRight)
    text.setFont(font)
    return text

def push_button(label="Button", size = (WIDTH, HEIGHT), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    button = QtWidgets.QPushButton(label)
    button.setMinimumSize(*size)
    button.setMaximumSize(*size)
    button.setFont(font)
    return button

def divider():
    divider = QtGui.QLabel("")
    divider.setStyleSheet("QLabel {background-color: #3e3e3e; padding: 0; margin: 0; border-bottom: 1 solid #666; border-top: 1 solid #2a2a2a;}")
    divider.setMaximumHeight(2)
    return divider

def line_edit(size=(WIDTH,HEIGHT), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    line_edit = QtWidgets.QLineEdit()
    line_edit.setMinimumSize(*size)
    line_edit.setMaximumSize(*size)
    line_edit.setFont(font)
    return line_edit

def radio_button(label="Radio Button", size=(WIDTH,HEIGHT), font_size=8):
    radio_button = QtWidgets.QRadioButton(label)
    font = QtGui.QFont()
    font.setPointSize(font_size)
    radio_button.setFont(font)
    radio_button.setMinimumSize(*size)
    radio_button.setMaximumSize(*size)
    return radio_button

def drop_down(size=(WIDTH,HEIGHT), options=[], font_size=8):
    drop_down = QtWidgets.QComboBox()
    font = QtGui.QFont()
    font.setPointSize(font_size)
    drop_down.setFont(font)
    for key in options:
        drop_down.addItem(key)
    drop_down.setMinimumSize(*size)
    drop_down.setMaximumSize(*size)
    return drop_down

def checkbox(label="Checkbox", size=(12,24), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    checkbox = QtWidgets.QCheckBox(label)
    checkbox.setMinimumSize(*size)
    checkbox.setMaximumSize(*size)
    checkbox.setFont(font)
    return checkbox

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def set_enum_attr_with_string(node, attr, value):
    enum_string = cmds.attributeQuery(attr, node=node, listEnum=1)[0]
    enum_list = enum_string.split(":")
    index = enum_list.index(value)
    cmds.setAttr(node+"."+attr, index)


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
class NcSpaceSwitcher_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "ncSpaceSwitcher"
    UI_NAME = "nc_space_switcher"
    WINDOWS = [WINDOW_NAME, UI_NAME]

    def __init__(self, *args, **kwargs):
        super(NcSpaceSwitcher_UI, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        return None

    def start(self):
        self.delete_windows()
        # Create instance of tool
        G.tool = NcSpaceSwitcher()
        G.tool.build_dict()
        self.create_window()
        self.setup_script_job()
        self.show()

    def delete_windows(self, onOff=True, forceOff=False):
        # Delete all windows
        for window in self.WINDOWS:
            if cmds.window(window, query=True, exists=True):
                cmds.deleteUI(window)

    def create_window(self):


        # Set object name and window title
        self.setObjectName(self.UI_NAME)
        self.setWindowTitle(self.WINDOW_NAME)

        # Create central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Create main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(SPACING*2, SPACING*2, SPACING*2, SPACING*2)
        self.main_layout.setSpacing(SPACING)
        #self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.central_widget.setLayout(self.main_layout)

        # Add refresh button
        self.refresh_button = push_button(label="Refresh")
        self.refresh_button.clicked.connect(G.tool.update_selections)
        self.main_layout.addWidget(self.refresh_button)

        # Create scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Create scroll bar
        self.scroll_bar = QtWidgets.QScrollBar()
        self.scroll_bar.setStyleSheet("QScrollBar:vertical {\
                            width: 20;\
                            }")
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)

        # Add widgets
        self.control_widget = QtWidgets.QWidget()
        self.control_layout = QtWidgets.QGridLayout()
        self.control_layout.setContentsMargins(SPACING, SPACING, SPACING, SPACING)
        self.control_layout.setSpacing(SPACING)
        #self.control_layout.setVerticalSpacing(SPACING)
        self.control_layout.setAlignment(QtCore.Qt.AlignTop)
        self.control_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.control_widget.setLayout(self.control_layout)
        self.scroll_area.setWidget(self.control_widget)

        self.add_control_widgets()

        # Create the run button
        self.run_button = push_button(label="RUN")
        self.run_button.clicked.connect(G.tool.run)
        self.main_layout.addWidget(self.run_button)

        width = 32 + (WIDTH*(len(G.spaceAttr)+1)) + ((len(G.spaceAttr)+7)*SPACING) # Width of scroll bar and checkbox
        height = (HEIGHT/2) + (len(G.controls)+3)*HEIGHT + ((len(G.controls)+10)*SPACING)  # Height of label
        self.resize(width, height)
        self.setMaximumWidth(width)
        self.setMaximumHeight(height)
    #---------------------------------------------------------------------------
    # Button clicked functions / UI updates
    # --------------------------------------------------------------------------
    def setup_script_job(self):
        """
        Procedure to create a script job that will update the UI when
        selections change
        """
        #JOB_number = cmds.scriptJob(e=["SelectionChanged", G.tool.update_selections], cu=True, kws=True, rp=True, p=self.UI_NAME)


    def add_control_widgets(self):
        self.controls_widget = QtWidgets.QWidget()
        self.control_grid = QtWidgets.QGridLayout()
        self.control_grid.setContentsMargins(0, 0, 0, 0)
        self.control_grid.setSpacing(SPACING)
        self.control_grid.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.controls_widget.setLayout(self.control_grid)
        self.control_layout.addWidget(self.controls_widget, 2, 0, 1, 1)

        # Add headings
        self.control_label = label(label="Control")
        self.control_grid.addWidget(self.control_label, 0, 1, 1, 1)
        for attr in G.spaceAttr:
            index = G.spaceAttr.index(attr)
            label_string = (re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', attr)).title()
            attr_label = label(label=label_string)
            self.control_grid.addWidget(attr_label, 0, 2+index, 1, 1)

        # Create checkbox widgets and drop down boxes
        controls = ["ALL"] + G.controls
        for control in controls:
            control_index = controls.index(control)
            # Create checkbox
            G.DICT[control]["checkbox"] = checkbox(label="")
            G.DICT[control]["checkbox"].setObjectName("checkbox_{0}".format(control))
            G.DICT[control]["checkbox"].setChecked(1)
            G.DICT[control]["checkbox"].stateChanged.connect(partial(self.checkbox_changed, control))
            self.control_grid.addWidget(G.DICT[control]["checkbox"], 1+control_index, 0, 1, 1)

            # Create line edit
            G.DICT[control]["lineEdit"] = line_edit()
            G.DICT[control]["lineEdit"].setObjectName("lineEdit_{0}".format(control))
            G.DICT[control]["lineEdit"].setText(control)
            G.DICT[control]["lineEdit"].setReadOnly(True)
            self.control_grid.addWidget(G.DICT[control]["lineEdit"], 1+control_index, 1, 1, 1)

            # for each attr add drop down
            for attr in G.spaceAttr:
                attr_index = G.spaceAttr.index(attr)
                G.DICT[control][attr]["dropdown"] = drop_down(options=G.DICT[control][attr]["options"])
                G.DICT[control][attr]["dropdown"].setObjectName("dropDown_{0}_{1}".format(control, attr))
                G.DICT[control][attr]["dropdown"].currentIndexChanged.connect(partial(self.dropdown_changed, control, attr))
                self.control_grid.addWidget(G.DICT[control][attr]["dropdown"], 1+control_index, 2+attr_index, 1, 1)

                # Set to the current value
                current = G.DICT[control][attr]["current"]
                option_index = G.DICT[control][attr]["dropdown"].findText(current, QtCore.Qt.MatchFixedString)
                if option_index >= 0:
                    G.DICT[control][attr]["dropdown"].setCurrentIndex(option_index)
                    if control != "ALL" and G.DICT[control][attr]["dropdown"].currentText() == "":
                        G.DICT[control][attr]["dropdown"].setEnabled(False)

                # Starting disable all controls and drop downs
                if control != "ALL":
                    G.DICT[control]["checkbox"].setEnabled(False)
                    G.DICT[control]["lineEdit"].setEnabled(False)
                    G.DICT[control][attr]["dropdown"].setEnabled(False)


        self.all_checked()


    def all_checked(self):
        # If ALL is checked disable all other checkboxes
        if G.DICT["ALL"]["checkbox"].isChecked():
            for control in G.controls:
                G.DICT[control]["checkbox"].setEnabled(False)
                G.DICT[control]["checkbox"].setChecked(1)
                G.DICT[control]["lineEdit"].setEnabled(False)
                for attr in G.spaceAttr:
                    G.DICT["ALL"][attr]["dropdown"].setEnabled(True)
                    G.DICT[control][attr]["dropdown"].setEnabled(False)
        if not G.DICT["ALL"]["checkbox"].isChecked():
            for control in G.controls:
                G.DICT["ALL"]["lineEdit"].setEnabled(False)
                G.DICT[control]["checkbox"].setEnabled(True)
                G.DICT[control]["lineEdit"].setEnabled(True)
                for attr in G.spaceAttr:
                    G.DICT["ALL"][attr]["dropdown"].setEnabled(False)
                    G.DICT[control][attr]["dropdown"].setEnabled(True)


    def dropdown_changed(self, control, attr, *args):
        # Change dictionary entry for new
        G.DICT[control][attr]["new"] = G.DICT[control][attr]["dropdown"].currentText()
        # If all change the controls as well
        if control == "ALL":
            all_value = G.DICT["ALL"][attr]["dropdown"].currentText()
            for control in G.controls:
                option_index = G.DICT[control][attr]["dropdown"].findText(all_value, QtCore.Qt.MatchFixedString)
                if option_index >= 0:
                    G.DICT[control][attr]["dropdown"].setCurrentIndex(option_index)
                if all_value == "":
                    current = G.DICT[control][attr]["current"]
                    option_index = G.DICT[control][attr]["dropdown"].findText(current, QtCore.Qt.MatchFixedString)
                    if option_index >= 0:
                        G.DICT[control][attr]["dropdown"].setCurrentIndex(option_index)


    def checkbox_changed(self, control, int):
        if control == "ALL":
            self.all_checked()
        for attr in G.spaceAttr:
            if G.DICT[control]["checkbox"].isChecked():
                # If checkbox is not ALL and the drop down options are availabe
                if control != "ALL" and G.DICT[control][attr]["dropdown"].currentText() != "":
                    G.DICT[control]["lineEdit"].setEnabled(True)
                    G.DICT[control][attr]["dropdown"].setEnabled(True)
                # If checkbox is ALL
                elif control =="ALL":
                    G.DICT[control]["lineEdit"].setEnabled(True)
                    G.DICT[control][attr]["dropdown"].setEnabled(True)
            else:
                current = G.DICT[control][attr]["current"]
                option_index = G.DICT[control][attr]["dropdown"].findText(current, QtCore.Qt.MatchFixedString)
                if option_index >= 0:
                    G.DICT[control][attr]["dropdown"].setCurrentIndex(option_index)
                G.DICT[control]["lineEdit"].setEnabled(False)
                G.DICT[control][attr]["dropdown"].setEnabled(False)


class NcSpaceSwitcher(object):

    def __init__(self):
        G.tool = self

    def get_controls(self):
        G.controls = []
        selected = cmds.ls(sl=1, type="transform")
        for control in selected:
            if control.endswith("_CTRL"):
                G.controls.append(control)
        list(set(G.controls))
        return G.controls


    def get_spaceAttr(self):
        """
        Function gets the attributes with space in their name
        """
        working_attr_options = ["space", "pointSpace", "orientSpace"]
        G.spaceAttr = []
        for control in G.controls:
            attributes = cmds.listAttr(w=True, l=False, u=True)
            for attr in attributes:
                if attr in working_attr_options:
                    G.spaceAttr.append(attr)

        # ------------------------
        # Edit this to override space list
        # ------------------------

        G.spaceAttr = list(set(G.spaceAttr))
        G.spaceAttr.sort()
        return G.spaceAttr


    def build_dict(self):
        G.DICT = {}
        G.controls = self.get_controls()
        G.spaceAttr = self.get_spaceAttr()
        # Create all options
        G.DICT["ALL"] = {}
        for attr in G.spaceAttr:
            G.DICT["ALL"][attr] = {}
            G.DICT["ALL"][attr]["options"] = [""]
            G.DICT["ALL"][attr]["current"] = ""
            G.DICT["ALL"][attr]["new"] = ""


        # For each control, loop through and get the space attributes, the current values and the options available
        for control in G.controls:
            G.DICT[control] = {}
            for attr in G.spaceAttr:
                G.DICT[control][attr] = {}
                attr_name = "{0}.{1}".format(control, attr)
                if cmds.objExists(attr_name):
                    G.DICT[control][attr]["current"] = cmds.getAttr(attr_name, asString=True)
                    G.DICT[control][attr]["new"] = G.DICT[control][attr]["current"]
                    options =  cmds.attributeQuery(attr, node=control, listEnum=True)
                    if options != None:
                        G.DICT[control][attr]["options"] = options[0].split(":")
                    else:
                        G.DICT[control][attr]["options"] = [""]


                    # Add the options to the 'ALL' key in the dictionary
                    G.DICT["ALL"][attr]["options"] = list(set(G.DICT["ALL"][attr]["options"]+G.DICT[control][attr]["options"]))

                else:
                    G.DICT[control][attr]["current"] = ""
                    G.DICT[control][attr]["new"] = ""
                    G.DICT[control][attr]["options"] = [""]


    def update_selections(self):
        show()

    @viewport_off
    def run(self):
        cmds.undoInfo(openChunk=True)
        print "------------------------ RUN ------------------------------"

        start_frame, current_frame, end_frame = self.get_start_current_end_frame()

        # Create locator for each control
        G.locators = []
        for control in G.controls:
            G.DICT[control]["locator"] = self.create_constrained_loc(control)
            G.locators.append(G.DICT[control]["locator"])

        # Set keys on extremes to maintain animation
        frames = [start_frame-1, start_frame, end_frame, end_frame+1]
        for frame in frames:
            print frame
            cmds.currentTime(frame)
            cmds.setKeyframe(G.controls, insert=True)

        # Bake the locators
        self.bake(G.locators, start_frame, end_frame)

        # Delete the constraints on the locators
        self.delete_constraints(G.locators)

        for control in G.controls:
            # Constrain controls to locators:
            self.constrain(G.DICT[control]["locator"], control)

            # Get keyframe times
            G.DICT[control]["keyframes"] = list(set(cmds.keyframe(control, query=True, timeChange=True)))


        self.switch_attr(start_frame, end_frame, current_frame)


        cmds.select(G.controls)
        cmds.currentTime(current_frame, edit=True)
        cmds.delete(G.locators)
        

        print "------------------------ DONE ------------------------------"
        cmds.undoInfo(closeChunk=True)

    def get_start_current_end_frame(self):
        current_frame = cmds.currentTime(query=True)
        start_frame = cmds.playbackOptions(query = True, min=True)
        end_frame = cmds.playbackOptions(query=True, max=True)
        return start_frame, current_frame, end_frame

    def create_constrained_loc(self, control):
        """
        Procedure to create a locator and constrain it to the input control
        """
        if cmds.objExists(control):
            # Get the world space position of the control
            transform_matrix = cmds.xform(control, query=True, matrix=True, worldSpace=True)
            # Create locator
            baked_locator = cmds.spaceLocator(name="{0}_LOC".format(control))[0]
            # Copy world space to locator
            cmds.xform(baked_locator, m=transform_matrix, a=True, ws=True)
            # Constrain locator to control
            cmds.parentConstraint(control, baked_locator)
        return baked_locator

    def bake(self, nodes, start_frame, end_frame):
        """
        Procedure to bake the input nodes for the frames in the timeline
        """
        # Bake nodes
        cmds.bakeResults(nodes, t=(start_frame, end_frame), simulation=True)

    def delete_constraints(self, nodes):
        """
        Procedure to delete the constraints on the given nodes
        """
        cmds.delete(nodes, cn=True)

    def constrain(self, parent, child):
        """
        Procedure to constrain the child to the parent
        """
        skip_rotation = []
        skip_translation = []
        list_attr = cmds.listAttr(child, connectable=True, w=True, k=True)

        for axis in ["X", "Y", "Z"]:
            if "translate{0}".format(axis) not in list_attr:
                skip_translation.append(axis.lower())
            if "rotate{0}".format(axis) not in list_attr:
                skip_rotation.append(axis.lower())

        if skip_translation == []:
            skip_translation = ["none"]
        if skip_rotation == []:
            skip_rotation = ["none"]

        cmds.parentConstraint(parent, child, sr=skip_rotation, st=skip_translation)

    def switch_attr(self, start_frame, end_frame, current_frame):
        # Loop through frames and switch attr
        for frame in range(int(start_frame), int(end_frame+1)):
            cmds.currentTime(frame, edit=True)
            for control in G.controls:
                if frame in G.DICT[control]["keyframes"]:
                    for attr in G.spaceAttr:
                        value = G.DICT[control][attr]["new"]
                        if value != "":
                            set_enum_attr_with_string(control, attr, value)
                        cmds.setKeyframe(control)
        cmds.currentTime(start_frame)
