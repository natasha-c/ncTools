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

# shiboken
from shiboken import wrapInstance

# mpc
from mpc.maya.animationTools.ACPManager import ACPManager as _ACPManager
from mpc.maya.animationTools.ACPManager import contexts as _ACPManagerContexts
from mpc.maya.animationTools.ACPManager.widgets import widgets
from mpc.maya.animationTools.ACPManager.ACPManagerDataContainers import ACPManagerDataContainer
from mpc.maya.animationTools.ACPManager.ACPManagerDataContainers import ACPAsset
from mpc.maya.animationTools.ACPManager.ACPManagerDataContainers import ACPSessionContext
from mpc.maya.animationTools.ACPManager import hubUtils
from mpc.maya.animationTools.ACPManager import mayaSceneUtils
from mpc.maya.animationTools.ACPManager.types import ACPState


# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class FeyWingConstrainGlobals(object):

    def __getattr__(self, attr):
        return None

G = FeyWingConstrainGlobals()

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
WING_DICT = {

    "feyBorraAvA"                   :           "wingsDesertMaleAvA",
    "feyBorraAvB"                   :           "wingsDesertMaleAvA",
    "feyConallAvA"                  :           "wingsForestMaleAvA",
    "feyConallAvB"                  :           "wingsForestMaleAvA",
    "feyConallAvC"                  :           "wingsForestMaleAvA",
    "feyIniAvA"                     :           "wingsDesertFemaleAvA",
    "feyIniAvB"                     :           "wingsDesertFemaleAvA",
    "feyShrikeAvA"                  :           "wingsJungleFemaleAvA",
    "feyShrikeAvB"                  :           "wingsJungleFemaleAvA",
    "feyUdoAvA"                     :           "wingsTundraMaleAvA",
    "feyUdoAvB"                     :           "wingsTundraMaleAvA",
    "feyBiomeMaleAvA"               :           "wingsDesertMaleAvB",
    "feyBiomeMaleAvB"               :           "wingsDesertMaleAvC",
    "feyBiomeMaleAvC"               :           "wingsDesertMaleAvD",
    "feyBiomeFemaleAvA"             :           "wingsDesertFemaleAvB",
    "feyBiomeFemaleAvB"             :           "wingsDesertFemaleAvC",
    "desertFeyChildAvA"             :           "wingsDesertChildAvA",
    "feyBiomeJungleMaleAvA"         :           "wingsJungleMaleAvA",
    "feyBiomeJungleMaleAvB"         :           "wingsJungleMaleAvB",
    "feyBiomeJungleFemaleAvA"       :           "wingsJungleFemaleAvB",
    "feyBiomeJungleFemaleAvB"       :           "wingsJungleFemaleAvC",
    "feyJungleChildAvA"             :           "wingsJungleChildAvA",
    "feyBiomeFemaleAvC"             :           "wingsForestFemaleAvA",
    "feyForestChildAvA"             :           "wingsForestChildAvA",
    "feyForestChildBvA"             :           "wingsForestChildAvB",
    "feyBiomeMaleAvD"               :           "wingsTundraMaleAvB",
    "feyBiomeMaleAvE"               :           "wingsTundraMaleAvC",
    "feyBiomeFemaleAvD"             :           "wingsTundraFemaleAvA",
    "feyTundraChildAvA"             :           "wingsTundraChildAvA",
    "maleficentBvB"                 :           "wingsWarriorAvA"

}

STATUS_DICT = {

    0:"WINGS NOT IN SHOT PACKAGE",
    1:"NOT GATHERED",
    2:"NOT CONNECTED",
    3:"CONNECTED",

}

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def get_main_window():
    pointer = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(long(pointer), QtWidgets.QMainWindow)
    return main_window

def show(mode="refresh"):
    G.feyWingConstrain = G.feyWingConstrain or FeyWingConstrain_UI()
    if mode == "refresh":
        G.feyWingConstrain = FeyWingConstrain_UI(parent=get_main_window())
        G.feyWingConstrain.start()

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

def combo_box(size = (200, 25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)
    combo_box = QtWidgets.QComboBox()
    combo_box.setMinimumSize(*size)
    combo_box.setMaximumSize(*size)
    combo_box.setFont(font)
    return combo_box

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

def drop_down(size=(200,25), options={}, font_size=8):
    drop_down = QtWidgets.QComboBox()
    font = QtGui.QFont()
    font.setPointSize(font_size)
    drop_down.setFont(font)
    for key in options:
        drop_down.addItem(options[key])
    drop_down.setMinimumSize(*size)
    drop_down.setMaximumSize(*size)
    return drop_down

def text_edit(size=(25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    text_edit = QtWidgets.QTextEdit()
    text_edit.setMinimumSize(*size)
    text_edit.setMaximumSize(*size)
    text_edit.setFont(font)
    return text_edit

def check_box(parent=None):
    check_box = QtWidgets.QCheckBox(parent=parent)
    return check_box


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
class FeyWingConstrain_UI(QtWidgets.QMainWindow):

    WINDOW_NAME = "Fey Wing Constrain"
    UI_NAME = "fey_wing_constrain"
    WINDOWS = [WINDOW_NAME, UI_NAME]

    def __init__(self, *args, **kwargs):
        super(FeyWingConstrain_UI, self).__init__(*args, **kwargs)


    def __getattr__(self, attr):
        return None


    def start(self):
        self.delete_windows()
        self.create_window()
        self.show()
        self.refresh()


    def delete_windows(self, onOff=True, forceOff=False):
        # Delete all windows
        for window in self.WINDOWS:
            if cmds.window(window, query=True, exists=True):
                cmds.deleteUI(window)


    def create_window(self):
        # Create instance of tool
        feyWingConstrain = FeyWingConstrain()

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
        self.display_grid.setSpacing(2)
        self.display_grid.setContentsMargins(0, 0, 0, 0)
        self.display_widget.setLayout(self.display_grid)

        self.refresh_button = push_button(label="Refresh", size=(502, 25))
        self.refresh_button.clicked.connect(self.refresh)
        self.display_grid.addWidget(self.refresh_button, 0, 2, 1, 2)

        constrain_gather_index = len(G.feyWingConstrain.feyWingConstrain.shotACPS) + 2
        self.constrain_button = push_button(label = "CONSTRAIN", size=(502, 35))
        self.constrain_button.clicked.connect(feyWingConstrain.constrain_wings)
        self.constrain_button.setStyleSheet('''
                QPushButton{
                    color:rgb(0, 0, 0);
                    background-color: rgb(239, 219, 0);

                }
            ''')
        self.display_grid.addWidget(self.constrain_button, constrain_gather_index, 2 , 1, 2)

        self.gather_button = push_button(label = "GATHER", size=(200, 35))
        self.gather_button.clicked.connect(feyWingConstrain.gather_wings)
        self.gather_button.setStyleSheet('''
                QPushButton{
                    color:rgb(0, 0, 0);
                    background-color: rgb(186, 100, 0);

                }
            ''')
        self.display_grid.addWidget(self.gather_button, constrain_gather_index, 5, 1, 1)

        sizeHint = self.sizeHint()
        self.setMaximumSize(sizeHint)


    # -----------------------------------------------------------------------------
    # Button clicked functions / UI updates
    # -----------------------------------------------------------------------------

    def refresh(self):

        G.feyWingConstrain.feyWingConstrain.initialise_acpManager()
        G.feyWingConstrain.feyWingConstrain.get_rigs()
        for acp in G.feyWingConstrain.feyWingConstrain.wingShotPkg:
            print acp.name()
        self.feyScene = G.feyWingConstrain.feyWingConstrain.feyScene
        self.feyWingDict = G.feyWingConstrain.feyWingConstrain.feyWingDict
        print self.feyWingDict
        self.constrain_checks = []
        self.gather_checks = []
        self.state_pickers = []

        for feyACP in self.feyScene:
            self.create_fey_wing_box(feyACP)

        print "DONE"


    def create_fey_wing_box(self, fey):
        feyACP = fey
        feyName = self.feyWingDict[fey]["feyName"]
        feyTopNode = self.feyWingDict[fey]["feyTopNode"]
        wingACP = self.feyWingDict[fey]["wingsACP"]
        wingName = self.feyWingDict[fey]["wingsName"]
        status = self.feyWingDict[fey]["status"]
        index = self.feyScene.index(fey)

        # Create checkbox for constrain fey
        constrain_widget = QtWidgets.QWidget()
        constrain_widget_layout = QtWidgets.QVBoxLayout()

        constrain_widget.setLayout(constrain_widget_layout)
        constrain_widget_layout.setAlignment(QtCore.Qt.AlignRight)
        constrain_widget_layout.setSpacing(0)
        constrain_widget_layout.setContentsMargins(0, 0, 0, 0)

        constrain_check = check_box()
        constrain_widget_layout.addWidget(constrain_check)
        constrain_check.setObjectName("constrain:{fey}".format(fey=feyName))
        G.feyWingConstrain.constrain_checks.append(constrain_check)
        self.display_grid.addWidget(constrain_widget, index+1, 1, 1, 1)

        # Create line edit for fey
        fey_display_box = line_edit(size=(250, 25))
        fey_display_box.setText(feyName)
        fey_display_box.setReadOnly(True)
        self.display_grid.addWidget(fey_display_box, index+1, 2, 1, 1)

        # Create line edit for wings
        wing_display_box = line_edit(size=(250,25))
        set_text = set_text = "{status_dict}: {wings}".format(status_dict = STATUS_DICT[status], wings=wingName)
        wing_display_box.setText(set_text)
        wing_display_box.setReadOnly(True)
        self.display_grid.addWidget(wing_display_box, index+1, 3, 1, 1)

        # Create checkbox for gather wings
        gather_widget = QtWidgets.QWidget()
        gather_widget_layout = QtWidgets.QVBoxLayout()
        gather_widget.setMinimumSize(25,25)
        gather_widget.setMaximumSize(25,25)

        gather_widget.setLayout(gather_widget_layout)
        gather_widget_layout.setAlignment(QtCore.Qt.AlignRight)
        gather_widget_layout.setSpacing(0)
        gather_widget_layout.setContentsMargins(0, 0, 0, 0)
        gather_check = check_box()
        gather_widget_layout.addWidget(gather_check)
        gather_check.setObjectName("gather:{wings}".format(wings=wingName))
        G.feyWingConstrain.gather_checks.append(gather_check)
        self.display_grid.addWidget(gather_widget, index+1, 4, 1, 1)

        # Create State Chooser for Gather
        self.state_picker = combo_box(size=(200, 25))
        self.state_picker.setObjectName("state:{wings}".format(wings=wingName))
        self.state_pickers.append(self.state_picker)
        self.display_grid.addWidget(self.state_picker, index+1, 5, 1, 1)

        # Add states to picker
        for state in self.feyWingDict[fey]["wingsStateList"]:
            index = state[0]
            string = state[1]
            self.state_picker.insertItem(index, string)


        # Colour formatting
        if self.feyWingDict[feyACP]["status"] == 3: # Connected
            constrain_check.setChecked(False)
            constrain_check.setEnabled(False)
            gather_check.setChecked(False)
            gather_check.setEnabled(False)
            wing_display_box.setStyleSheet('''
                QLineEdit{
                    color: rgb(0, 0, 0);
                    background-color: rgb(8, 132, 0);
                }
            ''')
        elif self.feyWingDict[feyACP]["status"] == 2: # Gather not connected
            constrain_check.setChecked(True)
            constrain_check.setEnabled(True)
            gather_check.setChecked(False)
            gather_check.setEnabled(False)
            wing_display_box.setStyleSheet('''
                QLineEdit{
                    color: rgb(0, 0, 0);
                    background-color: rgb(239, 219, 0);
                }
            ''')
        elif self.feyWingDict[feyACP]["status"] == 1: # Not gathered
            constrain_check.setChecked(False)
            constrain_check.setEnabled(False)
            gather_check.setChecked(True)
            gather_check.setEnabled(True)
            wing_display_box.setStyleSheet('''
                QLineEdit{
                    color: rgb(0, 0, 0);
                    background-color: rgb(186, 100, 0);
                }
            ''')
        elif self.feyWingDict[feyACP]["status"] == 0: # Not in shot package
            constrain_check.setChecked(False)
            constrain_check.setEnabled(False)
            gather_check.setChecked(False)
            gather_check.setEnabled(False)
            wing_display_box.setStyleSheet('''
                QLineEdit{
                    color: rgb(0, 0, 0);
                    background-color: rgb(137, 18, 0);
                }
            ''')

# -----------------------------------------------------------------------------
# Tool
# -----------------------------------------------------------------------------

class FeyWingConstrain(object):

    def __init__(self):
        if G.feyWingConstrain.feyWingConstrain:
            return
        G.feyWingConstrain.feyWingConstrain = self

        self.feyWingDict = {}
        self.initialise_acpManager()

    def initialise_acpManager(self):
        self.acpManager = _ACPManager.ACPManager()
        self.sessionContext = ACPSessionContext()
        self.dataModel = ACPManagerDataContainer(self.sessionContext)
        self.acpManagerDialog = self.acpManager._createACPManagerDialog()
        self.acpState = ACPState()
        self.shotACPS = self.dataModel._loadACPSFromLatestShotPkg()


    def get_rigs(self):
        self.feyShotPkg = []
        self.wingShotPkg = []
        self.feyScene = []

        for acp in self.shotACPS:
            if "wings" in acp.name():
                self.wingShotPkg.append(acp)

            if "fey" in acp.name() or "maleficent" in acp.name():
                fey = acp
                self.feyShotPkg.append(fey)

        for fey in self.feyShotPkg:
            acpState = mayaSceneUtils.findAnimateStateForACP(fey)
            if acpState == self.acpState.ANIMATE_HIGH_RES or acpState == self.acpState.ANIMATE_LOW_RES:
                self.feyScene.append(fey)
                self.feyWingDict[fey] = {}
                self.feyWingDict[fey]["feyName"] = fey.name()
                self.feyWingDict[fey]["feyTopNode"] = mayaSceneUtils.getRigPuppetTopNodeForACP(fey)
                wings = self.get_wings_for_fey(fey)



    def get_wings_for_fey(self, fey):
        name = fey.name()
        feyParts = name.partition("0")
        feyType = feyParts[0]
        feyNumber = feyParts[1]+feyParts[2]

        wingType = WING_DICT[feyType]
        wingName = wingType+feyNumber
        self.feyWingDict[fey]["wingsName"] = wingName
        self.feyWingDict[fey]["wingsTopNode"] = wingName
        self.feyWingDict[fey]["wingsACP"] = None
        self.feyWingDict[fey]["status"] = 0 # Not in shot package
        self.feyWingDict[fey]["wingsStateList"] = []
        for wings in self.wingShotPkg:
            if wings.name() == wingName:
                self.feyWingDict[fey]["wingsACP"] = wings
                self.feyWingDict[fey]["status"] = self.get_status(fey, wings)
                self.feyWingDict[fey]["wingsTopNode"] = mayaSceneUtils.getRigPuppetTopNodeForACP(wings)
                self.get_states(fey, wings)



    def get_status(self, fey, wings):
        wingACPState = mayaSceneUtils.findAnimateStateForACP(wings)
        print wings.name()
        print wingACPState
        status = 1 # Not in shot package
        if wingACPState >= 1 << 8:
            print "...512"
            if self.is_connected(fey, wings) == False:
                print "FALSE"
                status = 2 # In scene but not connected
            elif self.is_connected(fey, wings) == True:
                print "TRUE"
                status = 3 # In scene and connected
        return status

    def get_states(self, fey, wings):
        low_res = wings.getPkgRigPuppet(self.acpState.ANIMATE_LOW_RES)
        high_res = wings.getPkgRigPuppet(self.acpState.ANIMATE_HIGH_RES)
        if low_res:
            self.feyWingDict[fey]["wingsStateList"].append([1,"ANIMATE_LOW_RES"])
        if high_res:
            self.feyWingDict[fey]["wingsStateList"].append([2, "ANIMATE_HIGH_RES"])



    def is_connected(self, fey, wings):
        feyShoulder = "{feyName}:rp:spineShoulderGimbal_CTRL".format(feyName=fey.name())
        wingType = wings.name().partition("Av")[0]
        if "maleficent" in fey.name():
            wingType = "wingsForestMale"
        wingPivot = "{0}:rp:{1}{2}WingPivot_LOC".format(wings.name(), wingType.partition("wings")[2][0].lower(),wingType.partition("wings")[2][1:])

        # Does the shoulder have constraints?
        connections = cmds.listConnections(feyShoulder, type="constraint")
        if connections:
            for conn in connections:
                con = cmds.listConnections(conn, type="transform")

                for c in con:
                    if c == wingPivot:
                        return True
        else:
            return False

    def constrain_wings(self):
        for box in G.feyWingConstrain.constrain_checks:
            if box.isChecked():
                name = box.objectName()
                feyName = name.partition(":")[2]
                for fey in self.feyWingDict:
                    if self.feyWingDict[fey]["feyName"] == feyName:
                        mel_string = 'rig_connectRigs({"' + self.feyWingDict[fey]["feyTopNode"] + '", "' + self.feyWingDict[fey]["wingsTopNode"] + '"}, 1)'
                        mel.eval(mel_string)
        G.feyWingConstrain.refresh()


    def gather_wings(self):
        for box in G.feyWingConstrain.gather_checks:
            if box.isChecked():
                name = box.objectName()
                wingsName = name.partition(":")[2]
                for fey in self.feyWingDict:
                    if self.feyWingDict[fey]["wingsName"] == wingsName:
                        for box in G.feyWingConstrain.state_pickers:
                            if box.objectName() == "state:{wings}".format(wings=wingsName):
                                current_state = box.currentText()
                                state = eval("self.acpState."+ current_state)
                                self.gather_wing_rig(self.feyWingDict[fey]["wingsACP"], state)
        G.feyWingConstrain.refresh()

    def gather_wing_rig(self, asset, state):

        """
        Using the hubUtils module, gather the ACP for the wings based on the
        asset and the state required.
        """

        hubUtils.gatherACPPackage(asset, state)
