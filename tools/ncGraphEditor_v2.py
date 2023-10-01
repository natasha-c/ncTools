# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
import maya.cmds as cmds

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# ncTools
from ncTools.mods import dock;              reload(dock)
from ncTools.mods import uiMod;             reload(uiMod)

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
WINDOW_NAME = "ncGraphEditor"
WINDOW_TITLE = "nc Graph Editor "
GE_TOOLS = ["Bk1", "Bk2", "Bk3", "Bk4"]
# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
def run():
    """
    Entry point to call ui from maya
    """
    ncGraphEditorUI.show()

# -----------------------------------------------------------------------------
# Class UI
# -----------------------------------------------------------------------------
class ncGraphEditorUI(dock.DockManager):
    """
    overridden
    """
    def __init__(self):
        super(ncGraphEditorUI, self).__init__()
        self.window_name = WINDOW_NAME
        self.mixin_cls = lambda: dock.MayaMixin(window_name=self.window_name,
                                                main_widget_cls=ncGraphEditorWidget,
                                                title="ncGraph Editor")

class ncGraphEditorWidget(QtWidgets.QWidget):
    def __init__(self):
        """
        Main widget
        """
        super(ncGraphEditorWidget, self).__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.layout)
        self.add_graph_editor()
        self.add_graph_editor_toolbar()


    def add_graph_editor(self):
        """
        Create a scripted panel graph editor and add it to the main layout
        """
        # Created scripted panel, unparent and parent to ui
        if cmds.scriptedPanel("graphEditorUI", exists=True):
            cmds.deleteUI("graphEditorUI")
        cmds.scriptedPanel("graphEditorUI", unParent=True, type="graphEditor")
        cmds.scriptedPanel("graphEditorUI", e=True, type="graphEditor", parent=WINDOW_NAME)

        # Convert mel ui to qt widget and add to layout
        self.graph_editor_w = uiMod.to_QWidget("graphEditorUI")
        self.layout.addWidget(self.graph_editor_w)


    def add_graph_editor_toolbar(self):
        """
        Add the custom toolbar to the graph editor panel
        """
        ge_children = cmds.layout("graphEditorUI", query=True, childArray=True)
        ge_layout = "{0}|{1}".format("graphEditorUI", ge_children[0])
        ge_layout_children = cmds.layout(ge_layout, query=True, childArray=True)
        ge_toolbar_layout = "{0}|{1}".format(ge_layout, ge_layout_children[0])
        ge_toolbar_layout_qt = uiMod.to_QWidget(ge_toolbar_layout)

        # create label
        toolbar = QtWidgets.QWidget()
        toolbar_layout = QtWidgets.QHBoxLayout()
        toolbar_layout.setAlignment(QtCore.Qt.AlignLeft)
        toolbar_layout.setContentsMargins(1, 1, 1, 1)
        toolbar_layout.setSpacing(2)
        toolbar.setLayout(toolbar_layout)

        # add label to status line layout
        ge_toolbar_layout_qt.layout().addWidget(toolbar)

        for tool in GE_TOOLS:
            button = uiMod.push_button(label=tool, size=(25,25))
            toolbar_layout.addWidget(button)
