# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# python
import weakref
from functools import partial

# maya
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets

# ncTools
from ncTools.mods                   import uiMod;   reload(uiMod)
from ncTools.tools.ncToolboxGlobals   import ncToolboxGlobals as G

#---------------------------
mpcTools = {"HUB"   :   "mel.eval('hubInterface()')",
            "MHV"   :   "import mpc.modelHierarchyManager.ui.controlsWindow as controlsWindow; controlsWindow.showMhmWinMaya()",
            "Character Manager"     :   "from mpc.maya.animationTools.ACPManager import ACPManager as _ACPManager; acpManagerInstance = _ACPManager.instantiate(); acpManagerInstance.show()",
            "Reference Updater"  :   "mel.eval('rig_referenceUpdaterUI("");')",
            "Video Reference"   :   "from mpc.maya.animationTools.general.db_tools import db_videoReferenceManager; db_videoReferenceManager.db_videoReferenceManagerRun()",
            "Anim Library"      :   "from mpc.maya.animationTools.general import animationLibrary; animationLibrary.runPoseLibrary()",
            "Switchboard"       :   "mel.eval('rig_animSwitchWin();')",
            "MPC Camera"        :   'mel.eval(\"$version = `getenv \"MPCCAMERA_VERSION\"`; vcLoadModule(\"mpcCamera\", $version); runMpcCamera();\")',
}
#----------------------------

class MpcTools_UI(uiMod.BaseSubUI):

    def create_layout(self):

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "MPC Tools")

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

        tools = []
        for tool in mpcTools:
            tools.append(tool)
        tools.sort()

        row=0
        for script in tools:
            row+=1
            exec_string = mpcTools[script]
            button = uiMod.push_button(label = script, size = (self.w[6], self.h[1]))
            button.clicked.connect(partial(self.on_button_press, exec_string))
            self.main_layout.addWidget(button, row, 0, 1, 6)

        return self.frame_widget

    def on_button_press(self, exec_string):
        exec(exec_string)
