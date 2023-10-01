# -----------------------------------------------------------------------------
# Author: natasha-c
# Version: 1.0
# Purpose: To match differences in animation after updating rigs
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
from maya import OpenMayaUI as omui
from maya import cmds

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets


# shiboken
import shiboken

# my mods
from mods                   import uiMod;   reload(uiMod)
#from mods                   import animMod; reload(animMod)

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class CustomGraphEditorGlobals(object):

    def __getattr__(self, attr):
        return None

G = CustomGraphEditorGlobals()


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def get_maya_window():
    """
    Get the main maya windows
    """
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = shiboken.wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

def to_QWidget(maya_name):
    """
    Given the name of a Maya UI element, return the corresponding QWidget or
    QAction. If the object does not exist, return None
    """
    ptr = omui.MQtUtil.findControl(maya_name)
    if ptr is None:
        ptr = omui.MQtUtil.findLayout(maya_name)
    if ptr is None:
        ptr = omui.MQtUtil.findMenuItem(maya_name)
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)

def show():
    customGraphEditor = CustomGraphEditor()
    customGraphEditor.start()


class CustomGraphEditor(QtWidgets.QDialog):

    WINDOW_NAME = "Custom Graph Editor"
    UI_NAME = "CustomGraphEditor"
    WINDOWS = [WINDOW_NAME, UI_NAME]


    def __init__(self, parent=get_maya_window()):
        super(CustomGraphEditor, self).__init__(parent)


    def start(self):
        self.delete_windows()
        self.create_main_window()
        self.show()


    def delete_windows(self):
        for windows in self.WINDOWS:
            if cmds.window(windows, query=True, exists=True):
                cmds.deleteUI(windows)


    def create_main_window(self):
        # Set window name, size and title
        self.setObjectName(self.UI_NAME)
        self.setWindowTitle(self.WINDOW_NAME)
        self.resize(800,600)
        self.setWindowState(QtCore.Qt.WindowNoState)




        # Create the layout for the window and set its name
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setObjectName("mainLayout")

        # Unwrap the layout into a pointer, then get the full path to the UI in maya as a string
        main_layout = omui.MQtUtil.fullName(long(shiboken.getCppPointer(self.vertical_layout)[0]))
        cmds.setParent(main_layout)

        # Render Camera View
        self.camera_panel_widget = QtWidgets.QWidget()
        self.vertical_layout.addWidget(self.camera_panel_widget)

        self.camera_panel_layout = QtWidgets.QVBoxLayout()
        self.camera_panel_widget.setLayout(self.camera_panel_layout)








    def showEvent(self, event):
        super(CustomGraphEditor, self).showEvent(event)
        """
        Maya can lag in how it repaints UI. Force it to repaint when we show the
        window
        """
        print "SHOW"
        #self.modelPanel.repaint()
