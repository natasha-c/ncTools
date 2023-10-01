# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin



# Python
import inspect

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

###############################################################################
# Dockable UI
###############################################################################
"""
A maya bug - global holds all the widgets restored from maya preferences so that
qt doesn't garbage collect them if they aren't currently visible
"""
restored_widgets = []

# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------
class DockManager(object):
    def __init__(self):
        """
        Will be overriden by each UI
        """
        self.mixin = None
        self.window_name = None

    @classmethod
    def show(widget, debug=True):
        """
        Method to reshow or initiate the UI
        """
        # Initiate dock manager
        instance = widget()
        # Test if tool is already open
        if cmds.workspaceControl(instance.window_name + "WorkspaceControl", ex=True):
            if debug:
                # Deletes existing UI
                cmds.deleteUI(instance.window_name + "WorkspaceControl")
                # Initiate new dock manager
                instance.__init__()
                # Rerun to show the new UI
                instance.show()
            cmds.workspaceControl(instance.window_name + "WorkspaceControl", edit=True, restore=True)
        else:
            # Cretae mixin widget
            workspace_widget = instance.mixin()
            print "Workspace_widget", workspace_widget
            # Get class name of widget
            class_name = instance.__class__.__name__
            print "class_name", class_name
            # Get module name of widget
            module_name = inspect.getmodule(instance).__name__
            print "module_name", module_name
            # Show widget and attach uiScript for restoring widget from maya close
            workspace_widget.show(dockable=True, uiScript="import {0}\n{0}.{1}.restore_from_close()".format(module_name, class_name))

    @classmethod
    def restore_from_close(widget):
        """
        Method to restore last session's ui
        """
        # Initiate dock manager
        instance = widget()
        # Get the current maya control that the mixin widget should parent to
        restored_control = omui.MQtUtil.getCurrentParent()
        # Create mixin widget
        widget = instance.mixin()
        # Find the mixin widget create as a maya control
        mixin_ptr = omui.MQtUtil.findControl(widget.objectName())
        # Hold onto pointer so isn't garbage collected
        restored_widgets.append(widget)
        # Add misin widget to container ui
        omui.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(restored_control))

class MayaMixin(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, window_name, main_widget, title, minimum_width, **kwargs):
        """
        Creates a QWidget that registers as a maya control that will contain custom ui
        """
        super(MayaMixin, self).__init__(**kwargs)
        # Set the ui object name. Use to find UI as maya control class
        self.setObjectName(window_name)
        # Layout to hold main_widget
        self.main_layout = QtWidgets.QVBoxLayout()
        # Set no margins
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # Set layout
        self.setLayout(self.main_layout)
        # Initiate main_widget class
        self.mainWidget = main_widget
        # Add mainWidget to the layout
        self.main_layout.addWidget(self.mainWidget)
        # Set the title of the mixin widget
        self.setWindowTitle(title)
        # Set mimimum and maximum widths
        print minimum_width
        self.setMinimumWidth(minimum_width)
        self.setMaximumWidth(minimum_width)

class DockableWindowUI(DockManager):
    WINDOW_NAME = "DockableWindowUI"
    WINDOW_TITLE = "Dockable Window"
    def __init__(self):
        super(DockableWindowUI, self).__init__()
        self.window_name = self.WINDOW_NAME
        self.window_title = self.WINDOW_TITLE
        self.main_widget = QtWidgets.QWidget()


        self.mixin = lambda: MayaMixin(window_name = self.window_name,
                                                 main_widget = self.main_widget,
                                                 title=self.window_title,
                                                 minimum_width = self.minimum_width)

        self.build_ui()

    def __getattr____(self, attr):
        return None

    def build_ui(self):
        # Override with subclass ui
        pass

###############################################################################
# Base Sub UI
###############################################################################
class BaseSubUI(object):

    def __init__(self, parent, width_dict, height_dict, spacing):
        self.w = width_dict
        self.h = height_dict
        self.parent_layout = parent
        # Spacing
        self.spacing = spacing
        print "help"

# -----------------------------------------------------------------------------
# UI Elements
# -----------------------------------------------------------------------------
def checkbox(label="Checkbox", size=(25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    checkbox = QtWidgets.QCheckBox(label)
    checkbox.setMinimumSize(*size)
    checkbox.setMaximumSize(*size)
    checkbox.setFont(font)
    return checkbox

def label(label="Label", size = (25,25), h_adjust=0, font_size=8, align="left"):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    text = QtWidgets.QLabel(label)
    text.setMinimumSize((size[0]), (size[1]-h_adjust))
    text.setMaximumSize((size[0]), (size[1]-h_adjust))
    if align == "left":
        text.setAlignment(QtCore.Qt.AlignLeft)
    elif align == "center":
        text.setAlignment(QtCore.Qt.AlignCenter)
    elif align == "right":
        text.setAlignment(QtCore.Qt.AlignRight)
    text.setFont(font)
    return text

def line_edit(size=(25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    line_edit = QtWidgets.QLineEdit()
    line_edit.setMinimumSize(*size)
    line_edit.setMaximumSize(*size)
    line_edit.setFont(font)
    return line_edit

def push_button(label="Button", size = (25, 25), context_menu=None, tool_tip=None, status_tip=None, connect=None, font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    button = QtWidgets.QPushButton(label)
    button.setMinimumSize(*size)
    button.setMaximumSize(*size)
    button.setFont(font)

    if connect:
        button.clicked.connect(eval(connect))

    if tool_tip:
        button.setToolTip(tool_tip)

    if status_tip:
        button.setStatusTip(status_tip)

    if context_menu:
        add_context_menu(parent=button, context_menu=context_menu)

    return button

def radio_button(label="Radio Button", size = (25,25), font_size=8):
    font = QtGui.QFont()
    font.setPointSize(font_size)

    radio_button = QtWidgets.QRadioButton(label)
    radio_button.setMinimumSize(*size)
    radio_button.setMaximumSize(*size)
    radio_button.setFont(font)

    return radio_button

def add_context_menu(parent=None, context_menu=None):
    parent.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    for key in context_menu:
        action = QtWidgets.QAction(key, parent)
        action.triggered.connect(eval(context_menu[key]))
        parent.addAction(action)

def add_hotkey(parent=None, hotkey=None, connect=None):
    parent.setShortcut(QtWidgets.QKeySequence(hotkey))

# -----------------------------------------------------------------------------
# Collapsible Frame
# -----------------------------------------------------------------------------

class CollapsibleArrow(QtWidgets.QFrame):
    def __init__(self, parent = None):
        QtWidgets.QFrame.__init__(self, parent = parent)

        self.isCollapsed = True
        self.setMaximumSize(24, 24)
        self.horizontal_arrow_points = [QtCore.QPointF(4.0, 8.0), QtCore.QPointF(20.0, 8.0), QtCore.QPointF(12.0, 16.0)]
        self.horizontal_arrow = QtGui.QPolygonF(self.horizontal_arrow_points)
        self.vertical_arrow_points =[QtCore.QPointF(8.0, 4.0), QtCore.QPointF(16.0, 12.0), QtCore.QPointF(8.0, 20.0)]
        self.vertical_arrow = QtGui.QPolygonF(self.vertical_arrow_points)
        self.arrow = self.vertical_arrow
    def setArrow(self, arrow_dir):
        if arrow_dir:
            self.arrow = self.horizontal_arrow
        else:
            self.arrow = self.vertical_arrow

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(192, 192, 192))
        qp.setPen(QtGui.QColor(64, 64, 64))
        qp.drawPolygon(self.arrow)
        qp.end()



class TitleFrame(QtWidgets.QFrame):
    def __init__(self, parent = None):
        QtWidgets.QFrame.__init__(self, parent = parent)

        self.titleLabel = None
        self.arrow = None
        self.initTitleFrame()

    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL('clicked()'))
        return super(TitleFrame, self).mousePressEvent(event)

    def initTitleFrame(self, colour="40, 40, 40, 255"):
        self.setMinimumHeight(24)
        self.setStyleSheet("QFrame {\
           background-color: rgba("+colour+");\
           margin: 0px, 0px, 0px, 0px;\
           padding: 0px, 0px, 0px, 0px;\
           }")
        self.arrow = CollapsibleArrow(self)
        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setMinimumHeight(24)
        self.titleLabel.move(QtCore.QPoint(24, 0))


class CollapsibleFrame(QtWidgets.QFrame):
    def __init__(self, parent=None, text=None, base_width=None, base_height=None):
        QtWidgets.QFrame.__init__(self, parent = parent)

        self.text = text
        self.isCollapsed = False
        self.mainLayout = None
        self.titleFrame = None
        self.contentFrame = None
        self.contentLayout = None
        self.label = None
        self.arrow = None

        self.base_height = base_height
        self.base_width = base_width

        self.initFrameLayout()

    def text(self):
        return self.text

    def addWidget(self, widget):
        self.contentLayout.addWidget(widget)

    def initMainLayout(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

    def initTitleFrame(self):
        self.titleFrame = TitleFrame(self)
        self.mainLayout.addWidget(self.titleFrame)

    def initContentFrame(self):
        self.contentFrame = QtWidgets.QFrame(self)
        self.contentFrame.setContentsMargins(0, 0, 0, 0)
        self.contentFrame.setStyleSheet("QFrame {\
              margin: 2px, 0px, 0px, 0px;\
              padding: 0px, 0px, 0px, 0px;\
              }")
        self.contentLayout = QtWidgets.QVBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentFrame.setLayout(self.contentLayout)
        self.contentFrame.setVisible(self.isCollapsed)
        self.mainLayout.addWidget(self.contentFrame)

    def toggleCollapsed(self):
        self.contentFrame.setVisible(not self.isCollapsed)
        self.isCollapsed = not self.isCollapsed
        self.arrow.setArrow(self.isCollapsed)

    def setText(self, text):
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setText(text)
        self.label.setFont(font)

    def initFrameLayout(self):
        self.initMainLayout()
        self.initTitleFrame()
        self.initContentFrame()

        self.arrow = self.titleFrame.arrow
        self.label = self.titleFrame.titleLabel
        QtCore.QObject.connect(self.titleFrame, QtCore.SIGNAL('clicked()'), self.toggleCollapsed)

        if self.text:
            self.setText(self.text)
