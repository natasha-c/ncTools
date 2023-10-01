# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: A custom graph editor
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
from maya import OpenMayaUI as omui
from maya import cmds
#from maya import mel

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# shiboken
from shiboken2 import wrapInstance

# functools
#from functools import partial

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class CustomGraphEditorGlobals(object):

    def __getattr__(self, attr):
        return None

G = CustomGraphEditorGlobals()


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def show():
    customGraphEditorUI = CustomGraphEditor_UI()
    customGraphEditorUI.start()

def get_maya_window():
    """
    Get the main maya windows
    """
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtWidgets.QWidget)

def to_QWidget(name):
    """
    Given the name of a Maya UI element, return the corresponding QWidget or
    QAction. If the object does not exist, return None
    """
    ptr = omui.MQtUtil.findControl(name)
    if ptr is None:
        ptr = omui.MQtUtil.findLayout(name)
    if ptr is None:
        ptr = omui.MQtUtil.findMenuItem(name)
    if ptr is not None:
        return wrapInstance(long(ptr), QtWidgets.QWidget)


# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------
class CustomGraphEditor_UI(QtWidgets.QDialog):
        WINDOW_TITLE = "Custom Graph Editor"
        WINDOW_NAME = "CustomGraphEditor"
        WINDOWS = [WINDOW_NAME, WINDOW_TITLE]
        GE_NAME = "ge_ui"


        def __init__(self, parent=get_maya_window()):
            super(CustomGraphEditor_UI, self).__init__(parent)


        def start(self):
            self.delete_windows()
            print "windows deleted"
            self.create_main_window()
            print "window created"
            self.show()
            print "shown window"


        def delete_windows(self):
            for window in self.WINDOWS:
                if cmds.window(window, query=True, exists=True):
                    cmds.deleteUI(window)


        def create_main_window(self):
            # Set window name, size and title
            self.setObjectName(self.WINDOW_NAME)
            self.setWindowTitle(self.WINDOW_TITLE)
            self.resize(800,600)
            self.setWindowState(QtCore.Qt.WindowNoState)

            # Create the layout for the window and set its name
            self.vertical_layout = QtWidgets.QVBoxLayout(self)
            self.vertical_layout.setContentsMargins(0, 0, 0, 0)
            self.vertical_layout.setObjectName("mainLayout")

            # Create graph editor widget layout
            self.main_widget= QtWidgets.QWidget()
            self.main_layout = QtWidgets.QGridLayout()
            self.main_layout.setContentsMargins(2, 2, 2, 2)
            self.main_widget.setLayout(self.main_layout)
            self.vertical_layout.addWidget(self.main_widget)

            # Add graph editor panel
            self.add_graph_editor()

            # Add custom graph editor tool bar
            self.add_ge_toolbar()


        def add_graph_editor(self):
            # If the graph editor ui exists, delete, create and reparent it.
            if cmds.scriptedPanel(self.GE_NAME, exists=True):
                cmds.deleteUI(self.GE_NAME)
            self.ge_panel = cmds.scriptedPanel(self.GE_NAME, unParent=True, type="graphEditor")
            cmds.scriptedPanel(self.GE_NAME, e=True, parent=self.WINDOW_NAME)

            # Get the graph editor as a pyside qt object
            self.ge_qt = to_QWidget(self.ge_panel)

            # Add it to the window layout
            self.main_layout.addWidget(self.ge_qt, 0 ,0, 1, 1)


        def add_ge_toolbar(self):
            ge_children = cmds.layout(self.GE_NAME, query=True, childArray=True)
            ge_layout = "{0}|{1}".format(self.GE_NAME, ge_children[0])

            ge_layout_children = cmds.layout(ge_layout, query=True, childArray=True)
            ge_toolbar_layout = "{0}|{1}".format(ge_layout, ge_layout_children[0])

            ge_toolbar_layout_qt = to_QWidget(ge_toolbar_layout)

            # create label
            label = QtWidgets.QLabel(ge_toolbar_layout_qt)
            label.setText("Buttons will go here!")

            # add label to status line layout
            ge_toolbar_layout_qt.layout().addWidget(label)


        def custom_ge_toolbar(self):
            tools = []
