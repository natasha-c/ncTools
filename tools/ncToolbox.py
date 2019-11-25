# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# Maya
import maya.cmds as cmds

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# ncToolbox
from ncTools.mods                 import uiMod;       reload(uiMod)
from ncTools.mods                 import animMod;     reload(animMod)
from ncTools.tools.ncToolboxGlobals     import ncToolboxGlobals as G

# -----------------------------------------------------------------------------
# Script Editor
# -----------------------------------------------------------------------------
"""
from ncTools.tools import ncToolbox
reload(ncToolbox)
ncToolbox.run()
"""

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------

def run():
    """
    Start point to call ui
    """
    ncToolboxUI.show()


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

#SUB_UI_MODS   = ["mayaTools", "mpcTools", "ikfkSnapTest", "selectionTools", "shiftAnimation", "mirrorAnim", "scaleAnimLayer", "worldspaceSnap", "toggleCamera", "keyCleanupTools", "rigSettings", "copyPose", "copyAnimLayer", "standalones"]
SUB_UI_MODS   = ["mayaTools", "mpcTools", "mirrorAnim", "selectionTools"]

# Import subUI modules
for mod in SUB_UI_MODS:
    exec("import ncTools.tools.toolbox.{0} as {1}; reload({2})".format(mod, mod, mod))


# -----------------------------------------------------------------------------
# UI Class
# -----------------------------------------------------------------------------

class ncToolboxUI(uiMod.DockableWindowUI):
    WINDOW_NAME = "ncToolbox_UI"
    WINDOW_TITLE = "ncToolbox"

    # ---------------------------------------------------------------------
    # Design variables
    # ---------------------------------------------------------------------
    #Grid Spacing
    grid_columns = 6
    spacing = 0
    margin = 3
    #Button sizes
    base_width = 24
    base_height = 24
    button_width = {}
    button_height = {}
    for i in range(grid_columns):
        i = i+1
        width=(i*base_width) + (spacing*(i-1))
        height=(i*base_height) + (spacing*(i-1))
        button_width[i] = width
        button_height[i] = height

    minimum_width = (grid_columns*base_width)+((grid_columns-1)*spacing)+(2*margin)+20
    print minimum_width

    # ---------------------------------------------------------------------
    # Other
    # ---------------------------------------------------------------------
    barOffset      = 0
    barHotkeys     = {}
    G.ncToolsUIs         = {}

    # ---------------------------------------------------------------------
    # SUB UIS
    # ---------------------------------------------------------------------
    ui_list         = None
    sub_uis         = None

    def __init__(self):
        super(ncToolboxUI, self).__init__()




    def build_ui(self):
        # ---------------------------------------------------------------------
        # Build UI
        # ---------------------------------------------------------------------
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)

        # Create scroll area
        self.tools_scrollArea = QtWidgets.QScrollArea()
        self.tools_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tools_scrollArea.setWidgetResizable(True)
        self.main_layout.addWidget(self.tools_scrollArea)

        # Create scroll bar
        self.tools_tab_scrollBar = QtWidgets.QScrollBar()
        self.tools_tab_scrollBar.setStyleSheet("QScrollBar:vertical {\
                            width: 20px;\
                            }")
        self.tools_scrollArea.setVerticalScrollBar(self.tools_tab_scrollBar)

        # Create tools widget
        self.tools_widget = QtWidgets.QWidget()
        self.tools_widget_layout = QtWidgets.QVBoxLayout(self.tools_widget)
        #self.tools_widget_layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        self.tools_widget_layout.setSpacing(0)
        self.tools_widget_layout.setAlignment(QtCore.Qt.AlignTop)
        self.tools_widget.setLayout(self.tools_widget_layout)
        self.tools_scrollArea.setWidget(self.tools_widget)

        # Create sub ui widget
        self.sub_ui_widget = QtWidgets.QWidget()
        self.sub_ui_layout = QtWidgets.QVBoxLayout()
        self.sub_ui_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_ui_layout.setSpacing(2)
        self.sub_ui_widget.setLayout(self.sub_ui_layout)
        self.tools_widget_layout.addWidget(self.sub_ui_widget)

        # Sub UIs
        self.add_sub_uis()


    def add_sub_uis(self):
        for ui in SUB_UI_MODS:
            ui_class = "{0}.{1}{2}_UI".format(ui, ui[0].upper(), ui[1:])
            sub_ui = eval(ui_class)(self.sub_ui_layout, self.button_width, self.button_height, self.spacing)
            G.ncToolsUIs[ui] = sub_ui
            sub_ui_layout = sub_ui.create_layout()
            self.sub_ui_layout.addWidget(sub_ui_layout)
