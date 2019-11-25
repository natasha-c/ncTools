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
from ncTools.mods                   import animMod; reload(animMod)
from ncTools.tools.ncToolboxGlobals   import ncToolboxGlobals as G


class ToggleCamera_UI(uiMod.BaseSubUI):

    def create_layout(self):

        self.toggleCamera = ToggleCamera()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Toggle Camera")

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

        # Create buttons
        self.setup_toggle = uiMod.push_button(label="Setup", size=(self.w[6], self.h[1]))
        self.setup_toggle.clicked.connect(self.on_setup_toggle_clicked)
        self.main_layout.addWidget(self.setup_toggle, 1, 0, 1, 6)

        self.camera_1 = uiMod.push_button(label="Camera 1 ", size=(self.w[2], self.h[1]))
        self.camera_1.clicked.connect(self.on_camera_1_clicked)
        self.camera_1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.camera_1.customContextMenuRequested.connect(self.on_camera_1_assign_clicked)
        self.main_layout.addWidget(self.camera_1, 2, 0, 1, 2)

        self.camera_1_assign = uiMod.push_button(label=">", size=(self.w[1], self.h[1]))
        self.camera_1_assign.clicked.connect(self.on_camera_1_assign_clicked)
        self.main_layout.addWidget(self.camera_1_assign, 2, 2, 1, 1)

        self.camera_1_label = uiMod.line_edit(size=(self.w[3], self.h[1]))
        self.main_layout.addWidget(self.camera_1_label, 2, 3, 1, 4)

        self.camera_2 = uiMod.push_button(label="Camera 2 ", size=(self.w[2], self.h[1]))
        self.camera_2.clicked.connect(self.on_camera_2_clicked)
        self.main_layout.addWidget(self.camera_2, 3, 0, 1, 2)

        self.camera_2_assign = uiMod.push_button(label=">", size=(self.w[1], self.h[1]))
        self.camera_2_assign.clicked.connect(self.on_camera_2_assign_clicked)
        self.main_layout.addWidget(self.camera_2_assign, 3, 2, 1, 1)

        self.camera_2_label = uiMod.line_edit(size=(self.w[3], self.h[1]))
        self.main_layout.addWidget(self.camera_2_label, 3, 3, 1, 4)

        self.toggle_camera = uiMod.push_button(label="Toggle Camera", size=(self.w[6], self.h[1]))
        self.toggle_camera.clicked.connect(self.on_toggle_camera_clicked)
        self.main_layout.addWidget(self.toggle_camera, 4, 0, 1, 6)

        return self.frame_widget

    def on_setup_toggle_clicked(self):
        G.toggle_cam_1, G.toggle_cam_2 = self.toggleCamera.setup()
        self.camera_1_label.setText(G.toggle_cam_1)
        self.camera_2_label.setText(G.toggle_cam_2)

    def on_camera_1_clicked(self):
        self.toggleCamera.look_through_camera(camera=G.toggle_cam_1)

    def on_camera_1_assign_clicked(self):
        self.toggleCamera.assign_camera(camera=1)
        self.camera_1_label.setText(G.toggle_cam_1)

    def on_camera_2_clicked(self):
        self.toggleCamera.look_through_camera(camera=G.toggle_cam_2)

    def on_camera_2_assign_clicked(self):
        self.toggleCamera.assign_camera(camera=2)
        self.camera_2_label.setText(G.toggle_cam_2)

    def on_toggle_camera_clicked(self):
        self.toggleCamera.toggle_camera()

class ToggleCamera(object):

    def __init__(self):
        if G.toggleCamera:
            return
        G.toggleCamera = self

    def setup(self):
        G.toggle_cam_1 = "persp"
        G.toggle_cam_2 = self.get_current_camera()
        return G.toggle_cam_1, G.toggle_cam_2


    def look_through_camera(self, camera=None):
        current_panel = cmds.getPanel(underPointer = True) or cmds.getPanel(withFocus = True)
        mel.eval("lookThroughModelPanel {0} {1}".format(camera, current_panel))

    def assign_camera(self, camera=None):
        current_camera = self.get_current_camera()
        if camera == 1:
            G.toggle_cam_1 = current_camera
        elif camera == 2:
            G.toggle_cam_2 = current_camera

    def get_current_camera(self):
        current_panel = cmds.getPanel(withFocus = True)
        if current_panel !="":
            panel_type = cmds.getPanel(typeOf=current_panel)
            if panel_type == "modelPanel":
                current_camera = cmds.modelPanel(current_panel, query=True, camera=True)
        return current_camera

    def toggle_camera(self):
        current_camera = self.get_current_camera()
        if current_camera == G.toggle_cam_1:
            self.look_through_camera(camera=G.toggle_cam_2)
        else:
            self.look_through_camera(camera=G.toggle_cam_1)
