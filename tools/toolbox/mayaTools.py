# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# python
import weakref
from functools import partial

# maya
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets

# ncTools
from ncTools.mods                   import uiMod;   reload(uiMod)
from ncTools.tools.ncToolboxGlobals   import ncToolboxGlobals as G


class MayaTools_UI(uiMod.BaseSubUI):

    def create_layout(self):

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Maya Tools")

        # Create main widget
        self.main_widget = QtWidgets.QWidget()
        # Add widget to frame
        self.frame_widget.addWidget(self.main_widget)
        # Create main widget layout
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setSpacing(self.spacing)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # Add layout to widget
        self.main_widget.setLayout(self.main_layout)

        # Create Buttons
        # Graph Editor
        self.graph_editor = uiMod.push_button(label = "Graph Editor", size = (self.w[3], self.h[1]))
        self.graph_editor.clicked.connect(self.on_graph_editor_clicked)
        self.main_layout.addWidget(self.graph_editor, 1, 0, 1, 3)

        # Dope Sheet
        self.dope_sheet = uiMod.push_button(label = "Dope Sheet", size = (self.w[3], self.h[1]))
        self.dope_sheet.clicked.connect(self.on_dope_sheet_clicked)
        self.main_layout.addWidget(self.dope_sheet, 1, 3, 1, 3)

        # Hypershade
        self.hypershade = uiMod.push_button(label = "Hypershade", size = (self.w[3], self.h[1]))
        self.hypershade.clicked.connect(self.on_hypersahde_clicked)
        self.main_layout.addWidget(self.hypershade, 2, 0, 1, 3)

        # Node Editor
        self.node_editor = uiMod.push_button(label = "Node Editor", size = (self.w[3], self.h[1]))
        self.node_editor.clicked.connect(self.on_node_editor_clicked)
        self.main_layout.addWidget(self.node_editor, 2, 3, 1, 3)



        return self.frame_widget


    def on_graph_editor_clicked(self):
        mel.eval("GraphEditor")

    def on_dope_sheet_clicked(self):
        mel.eval("DopeSheetEditor")

    def on_hypersahde_clicked(self):
        mel.eval("HypershadeWindow")

    def on_node_editor_clicked(self):
        mel.eval("NodeEditorWindow")
