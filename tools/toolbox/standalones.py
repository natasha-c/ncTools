# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# python
import weakref
from functools import partial
import re

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



class Standalones_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        standalones = Standalones()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Standalones")

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
        G.standalones.scripts.sort()
        row=0
        for script in G.standalones.scripts:
            row +=1
            parts = map(lambda x:x.capitalize(), re.findall("[a-zA-Z0-9][^A-Z^0-9]*", script))
            label = " ".join(parts)
            button = uiMod.push_button(label = label, size=(self.w[6], self.h[1]))
            button.clicked.connect(partial(standalones.run_script, script))
            self.main_layout.addWidget(button, row, 0, 1, 6)
        return self.frame_widget


class Standalones(object):

    def __init__(self):
        if G.standalones:
            return
        G.standalones = self

        self.get_scripts()

    def get_scripts(self):
        uad = cmds.internalVar(uad=True)
        scripts_standalone = "{uad}scripts/ncTools/tools/standalone".format(uad=uad)
        files = cmds.getFileList(fld=scripts_standalone, fs="*.py")
        files.remove("__init__.py")
        G.standalones.scripts = []

        for script in files:
            script = script.rpartition(".")[0]
            G.standalones.scripts.append(script)

    def run_script(self, script):
        exec("import ncTools.tools.standalone.{script} as {script}; reload({script}); {script}.show();".format(script=script))
