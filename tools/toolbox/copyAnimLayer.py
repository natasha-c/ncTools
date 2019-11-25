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


class CopyAnimLayer_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        copyAnimLayer = CopyAnimLayer

        #Create tool instance
        self.copyAnimLayer = CopyAnimLayer()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Copy Anim Layer")

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
        self.copy_anim_layer = uiMod.push_button(label = "Copy Anim Layer", size=(self.w[6], self.h[1]))
        self.copy_anim_layer.clicked.connect(self.on_copy_anim_layer_clicked)
        self.main_layout.addWidget(self.copy_anim_layer, 1, 0, 1, 6)

        return self.frame_widget

    def on_copy_anim_layer_clicked(self):
        self.copyAnimLayer.copy_anim_layer()

class CopyAnimLayer(object):

    def __init__(self):
        if G.copyAnimLayer:
            return
        G.copyAnimLayer = self

    def copy_anim_layer(self):
        controls = animMod.get_target("controls", selected=True)
        source_anim_layers = animMod.get_target("anim_layers", selected=True)
        for anim_layer in source_anim_layers:
            anim_layer_name = str(anim_layer)
            anim_layer_override = cmds.animLayer(anim_layer, query=True, override=True)

            #Create new anim layer
            new_anim_layer_name = "{0}_copy".format(anim_layer_name)
            new_anim_layer = cmds.animLayer(new_anim_layer_name, override=anim_layer_override)

            for control in controls:
                print control
                attributes = animMod.get_target("attributes", attribute_options=["unlocked", "c", "keyable"], node=control) or []
                print attributes
                for attribute in attributes:

                    #Is it in the source layer?
                    if not animMod.is_control_in_anim_layer(control, anim_layer):
                        pass
                    else:

                        #Are there curves on the attribute?
                        anim_curves = cmds.copyKey(control, time = [], option="curve", animLayer=anim_layer)

                        if anim_curves > 0:
                            #Add the control to the new layer
                            cmds.select(control)
                            cmds.animLayer(new_anim_layer, edit=True, at=control + "." + attribute)
                            cmds.setKeyframe(control, at=attribute, al=new_anim_layer)
                            cmds.pasteKey(control, option="replaceCompletely", al=new_anim_layer)
