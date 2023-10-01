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
import shiboken2 as shiboken

# my mods
#from mods                   import uiMod;   reload(uiMod)
#from mods                   import animMod; reload(animMod)

# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------
class CustomGraphEditorGlobals(object):

    def __getattr__(self, attr):
        return None

G = CustomGraphEditorGlobals()

graphEditorPanel = "customGraphEditor"
graphEditorPanelWindow = "%sWindow" % graphEditorPanel
graphEditorGraphEd = "%sGraphEd" % graphEditorPanel
paneLayoutName = None
# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
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
        return wrap_instance(long(ptr), QtWidgets.QWidget)

def toQtObject(maya_name):
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
        return wrap_instance(long(ptr), QtCore.QObject)

def wrap_instance(ptr, base=None):
    """
    Utility to convert a pointer to a Qt class instance
    """
    if ptr is None:
        return None
    ptr = long(ptr)
    if globals().has_key("shiboken"):
        if base is None:
            qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtWidgets, cls):
                base = getattr(QtWidgets, cls)
            elif hasattr(QtWidgets, superCls):
                base = getattr(QtWidgets, superCls)
            else:
                base = QtWidgets.QWidget()
        return shiboken.wrapInstance(long(ptr), base)
    elif globals().has_key("sip"):
        base = QtCore.QObject
        return sip.wrapinstance(long(ptr), base)
    else:
        return None

def get_maya_window():
    """
    Get the main maya windows
    """
    ptr = omui.MQtUtil.mainWindow()
    return wrap_instance(long(ptr), QtWidgets.QWidget)

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


        # Create graph editor widget layout
        self.graph_editor_w = QtWidgets.QWidget()
        self.graph_editor_l = QtWidgets.QGridLayout()
        self.graph_editor_w.setLayout(self.graph_editor_l)
        self.vertical_layout.addWidget(self.graph_editor_w)

        # Get graph editor

        if cmds.scriptedPanel("customGraphEditor", query=True, exists=True):
            print "exists"
            cmds.deleteUI("customGraphEditor", panel=True)
        custom_editor_panel = cmds.scriptedPanel("customGraphEditor", type="graphEditor")

        graph_Editor_qt = to_QWidget(custom_editor_panel)
        print graph_Editor_qt

        self.graph_editor_l.addWidget(graph_Editor_qt, 0, 0, 1, 1)







        """
        # Add graph editor
        graph_editor = to_QWidget(cmds.animCurveEditor())
        self.graph_editor_l.addWidget(graph_editor, 0, 1, 1, 1)

        # Add graph outliner
        graph_outliner = to_QWidget(cmds.outlinerEditor(mainListConnection="graphEditorList",
                                                        #selectionConnection="modelList",
                                                        autoExpand=True,
                                                        #expandAttribute=True,
                                                        expandObjects=True,
                                                        showAttributes=True,
                                                        showAnimCurvesOnly=True,
                                                        showConnected=True,
                                                        showPinIcons=True,
                                                        showSelected=True))
        self.graph_editor_l.addWidget(graph_outliner, 0, 0, 1, 1)"""
