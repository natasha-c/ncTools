# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: To match differences in animation after updating rigs
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
import os

# maya
from maya import OpenMayaUI as omui
from maya import cmds
from maya import mel
from functools import wraps

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets

# shiboken
from shiboken import wrapInstance




# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class RigMatcherGlobals(object):

    def __getattr__(self, attr):
        return None

G = RigMatcherGlobals()

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# UI Standard Sizes
WIDTH = 320

HEIGHT = 24

# Shot info
JOB = os.environ["JOB"]
SCENE = os.environ["SCENE"]
SHOT = os.environ["SHOT"].rpartition("/")[2]

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
    G.rigMatcher = G.rigMatcher or RigMatcher_UI()
    if mode == "refresh":
        G.rigMatcher = RigMatcher_UI(parent=get_main_window())
        G.rigMatcher.start()

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
    divider = QtWidgets.QLabel("")
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



# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
class RigMatcher_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "Rig Matcher"
    UI_NAME = "rig_matcher_ui"
    WINDOWS = [WINDOW_NAME, UI_NAME]

    def __init__(self, *args, **kwargs):
        super(RigMatcher_UI, self).__init__(*args, **kwargs)


    def __getattr__(self, attr):
        return None

    def start(self):
        self.delete_windows()
        self.create_window()
        self.setup_script_job()
        self.update_selections()


    def delete_windows(self, onOff=True, forceOff=False):
        # Delete all windows
        for window in self.WINDOWS:
            if cmds.window(window, query=True, exists=True):
                cmds.deleteUI(window)

    def create_window(self):
        # Create instance of tool
        rigMatcher = RigMatcher()

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
        self.main_grid = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setVerticalSpacing(5)
        self.main_grid.setLayout(self.grid_layout)
        self.main_layout.addWidget(self.main_grid)

        self.select_label = label(label="1. Select the rig")
        self.grid_layout.addWidget(self.select_label, 0, 0, 1, 2)

        self.rig_display = line_edit()
        self.rig_display.setReadOnly(True)
        self.grid_layout.addWidget(self.rig_display, 1, 0, 1, 2)

        self.divider_1 = divider()
        self.grid_layout.addWidget(self.divider_1, 2, 0, 1, 2)

        self.copy_label = label(label="2. Copy animation onto locators")
        self.grid_layout.addWidget(self.copy_label, 3, 0, 1, 2)

        self.copy = push_button(label = "Copy")
        self.copy.clicked.connect(rigMatcher.copy)
        self.grid_layout.addWidget(self.copy, 4, 0, 1, 2)

        self.divider_2 = divider()
        self.grid_layout.addWidget(self.divider_2, 5, 0, 1, 2)

        self.export_label = label(label="3. Select the locators:")
        self.grid_layout.addWidget(self.export_label, 6, 0, 1, 2)

        self.locator_display = line_edit()
        self.locator_display.setReadOnly(True)
        self.grid_layout.addWidget(self.locator_display, 7, 0, 1, 2)

        self.export_locators = push_button(label="Export Locators",
                                           size=(WIDTH/2, HEIGHT))
        self.export_locators.clicked.connect(rigMatcher.export_locators)
        self.grid_layout.addWidget(self.export_locators, 8, 0, 1, 1)

        self.import_locators = push_button(label="Import Locators",
                                           size=(WIDTH/2, HEIGHT))
        self.import_locators.clicked.connect(rigMatcher.import_locators)
        self.grid_layout.addWidget(self.import_locators, 8, 1, 1, 1)

        self.divider_3 = divider()
        self.grid_layout.addWidget(self.divider_3, 9, 0, 1, 2)

        self.paste_label = label(label="4. Paste the animation onto:")
        self.grid_layout.addWidget(self.paste_label, 10, 0, 1, 2)

        self.all_radio = radio_button(label="All Ctrls",
                                      size=(WIDTH/2, HEIGHT/2))
        self.all_radio.setChecked(True)
        self.grid_layout.addWidget(self.all_radio, 11, 0, 1, 1)
        self.selected_radio = radio_button(label="Selected Ctrls",
                                           size=(WIDTH/2, HEIGHT/2))
        self.grid_layout.addWidget(self.selected_radio, 11, 1, 1, 1)

        self.paste = push_button(label = "Paste")
        self.paste.clicked.connect(rigMatcher.paste)
        self.grid_layout.addWidget(self.paste, 12, 0, 1, 2)


        sizeHint = self.sizeHint()
        self.setMaximumSize(sizeHint)

    #---------------------------------------------------------------------------
    # Button clicked functions / UI updates
    # --------------------------------------------------------------------------
    def setup_script_job(self):
        """
        Procedure to create a script job that will update the UI when
        selections change
        """

        JOB_number = cmds.scriptJob(e=["SelectionChanged", self.update_selections], cu=True, kws=True, rp=True, p=self.UI_NAME)


    def update_selections(self):
        """
        Procedure to update the UI based on the selection
        """

        selection = cmds.ls(sl=1, l=True)
        for node in selection:
            root=node.partition("|")[2].split("|")[0]
            if root.endswith("Top_GRP"):
                G.rigMatcher.rig = root
                self.rig_display.setText(G.rigMatcher.rig)
            if root.endswith("locators"):
                G.rigMatcher.locators = root
                self.locator_display.setText(G.rigMatcher.locators)


# -----------------------------------------------------------------------------
# Tool
# -----------------------------------------------------------------------------

class RigMatcher(object):

    def __init__(self):
        if G.rigMatcher.rigMatcher:
            return
        G.rigMatcher.rigMatcher = self

    def get_controls(self, rig):
        """
        Procedure to obtain all the controls for the given rig
        """
        self.rig = rig
        self.namespace = self.rig.rpartition(":")[0]
        self.global_control = "{0}:global_CTRL".format(self.namespace)
        relatives = cmds.listRelatives(self.global_control, ad=True, type="transform")
        self.controls = []
        for control in relatives:
            if control.endswith("_CTRL"):
                self.controls.append(control)
        self.controls.reverse()
        self.controls = [self.global_control]+self.controls


    @viewport_off
    def copy(self):
        """
        Prodecure to copy the world space animation of the rig controls, baking
        this onto locators
        """
        # Get controls to copy based on selected rig in UI
        self.get_controls(G.rigMatcher.rig)

        # Create baked locator group
        self.locator_group = "{namespace}:rig_matcher_locators".format(namespace=self.namespace)
        if cmds.objExists(self.locator_group):
            cmds.delete(self.locator_group)
        cmds.group(empty=True, name=self.locator_group)

        # Create locators and parent these to controls
        for control in self.controls:
            if cmds.objExists(control):
                transform_matrix = cmds.xform(query=True, matrix=True, worldSpace=True)
                baked_locator = "{control}_LOC".format(control=control)
                cmds.spaceLocator(name=baked_locator)
                cmds.parent(baked_locator, self.locator_group)
                cmds.xform(baked_locator, m=transform_matrix, a=True, ws=True)
                cmds.parentConstraint(control, baked_locator)

        # Get all locators beneath locator group top node
        self.rig_matcher_locators = cmds.listRelatives(self.locator_group, c=True)

        # Bake locators
        min_time = cmds.playbackOptions(query = True, min=True)
        max_time = cmds.playbackOptions(query=True, max=True)
        time_range=(min_time, max_time)
        cmds.bakeResults(self.rig_matcher_locators, t=time_range, simulation=True)
        cmds.delete(self.rig_matcher_locators, cn=True)


    @viewport_off
    def paste(self):
        """
        Procedure that pastes the world space positions of the locators onto the
        rig controls and keying on a seperate layer
        """
        # Get the time range to paste onto
        min_time = cmds.playbackOptions(query = True, min=True)
        max_time = cmds.playbackOptions(query=True, max=True)
        time_range=(min_time, max_time)

        # Query radio buttons to get paste controls
        if G.rigMatcher.all_radio.isChecked():
            self.get_controls(G.rigMatcher.rig)
            paste_controls = self.controls
        if G.rigMatcher.selected_radio.isChecked():
            paste_controls = cmds.ls(sl=1)

        # Get locators
        self.rig_matcher_locators = cmds.listRelatives(G.rigMatcher.locators, c=True)

        #Create anim layer
        if not cmds.objExists("rig_matcher_layer"):
            rig_fix_animLayer = cmds.animLayer("rig_matcher_layer")
        cmds.select(paste_controls)
        cmds.animLayer("rig_matcher_layer", edit=True, aso=True)

        # For frames in timeline step through and snap each controler to it's
        # locators position. Repeating to get closer results.
        for frame in range(int(time_range[0]), int(time_range[1]+1)):
            cmds.currentTime(frame, edit=True)
            for control in paste_controls:
                cmds.setKeyframe(control, al="rig_matcher_layer")

            difference = self.snap(paste_controls)
            new_difference = self.snap(paste_controls)
            loop_counter = 1
            while round(difference, 2) != round(new_difference, 2):
                loop_counter = loop_counter + 1
                if loop_counter > 50:
                    break

                difference = new_difference
                new_difference = self.snap(paste_controls)


    def snap(self, controls):
        """
        Procdure which snaps the controller to the locator position and returns
        a value that represents the difference between the positions
        """
        difference = []
        for control in controls:
            for locators in self.rig_matcher_locators:
                control_name = control.rpartition(":")[2]
                if control_name in locators:
                    locator = locators

            if cmds.objExists(locator):
                locator_xform = cmds.xform(locator, query=True, m=True, ws=True)
                control_xform = cmds.xform(control, query=True,m=True, a=True, ws=True)
                cmds.xform(control, a=True, ws=True, m=locator_xform)
                control_xform = cmds.xform(control, query=True,m=True, a=True, ws=True)
                cmds.setKeyframe(control, al="rig_matcher_layer")
                for c,l in zip(control_xform, locator_xform):
                    c = round(c, 5)
                    l = round(l, 5)
                    dif = c - l
                    difference.append(dif)
        sum_diff = sum(difference)
        return sum_diff

    def export_locators(self):
        # Export the locators to the anim folder of the shot folder
        filename = "/jobs/{job}/{scene}/{shot}/maya/scenes/anim/{locators}.ma".format(job=JOB, scene=SCENE, shot=SHOT, locators=G.rigMatcher.locators)
        cmds.select(G.rigMatcher.locators)
        cmds.file(filename, exportSelected=True, type="mayaAscii", force=True, options="v=0")
        confirm_message = "Locators exported to: {filename}".format(filename=filename)
        cmds.confirmDialog(title="Export Complete", message=confirm_message, button=["Ok"], defaultButton="Ok")

    def import_locators(self):
        # Using a file dialog get the file for import
        starting_directory = "/jobs/{job}/{scene}/{shot}/maya/scenes/anim/.ma".format(job=JOB, scene=SCENE, shot=SHOT)
        import_locators = cmds.fileDialog2(dialogStyle=2, caption="Import Locators", startingDirectory=starting_directory, fileMode=1, okCaption="Import")
        new_nodes = cmds.file(import_locators, i=True, ns="rigMatcher", returnNewNodes=True)

        # Find the top group for the baked locators
        for node in new_nodes:

            if node.endswith("rig_matcher_locators"):
                self.locator_group = node.rpartition("|")[2]

        # Update the UI
        cmds.select(self.locator_group)
        G.rigMatcher.update_selections()
