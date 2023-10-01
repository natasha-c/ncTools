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


class ScaleAnimLayer_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        scaleAnimLayer = ScaleAnimLayer()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Scale Anim Layer")

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
        self.scale_anim_layer = uiMod.push_button(label = "Scale Anim Layer", size=(self.w[6], self.h[1]))
        self.scale_anim_layer.clicked.connect(G.scaleAnimLayer.scale_anim_layer)
        self.main_layout.addWidget(self.scale_anim_layer, 1, 0, 1, 6)

        return self.frame_widget

class ScaleAnimLayer(object):

    def __init__(self):
        G.scaleAnimLayer = self

    def scale_anim_layer(self):
        controls = animMod.get_controls(selected=True)
        source_anim_layers = animMod.get_anim_layers(selected=True)
        print "here"
        for anim_layer in source_anim_layers:
            anim_layer_name = str(anim_layer)
            anim_layer_override = cmds.animLayer(anim_layer, query=True, override=True)

            #Create new anim layer
            new_anim_layer_name = "{0}_scale".format(anim_layer_name)
            new_anim_layer = cmds.animLayer(new_anim_layer_name, override=anim_layer_override)

            for control in controls:
                attributes = animMod.get_attributes(node=control, attribute_options=["unlocked", "c", "keyable"]) or []
               
                for attribute in attributes:
                    #Is it in the source layer?
                    if not animMod.is_control_in_anim_layer(control, anim_layer):
                        pass
                    else:

                        #Are there curves on the attribute?
                        anim_curves = cmds.copyKey(control, time = [], at=attribute, option="curve", animLayer=anim_layer)


                        if anim_curves > 0:

                            #Add the control to the new layer
                            cmds.animLayer(new_anim_layer, edit=True, at=control + "." + attribute)
                            cmds.setKeyframe(control, at=attribute, al=new_anim_layer)
                            cmds.pasteKey(control, option="replaceCompletely", al=new_anim_layer)

                            new_anim_curve = animMod.get_target("anim_curve", node=control, attribute=attribute, anim_layer=new_anim_layer)

                            current_time = cmds.playbackOptions(query=True, minTime=True)
                            print current_time

                            current_value = cmds.getAttr(new_anim_curve, time=current_time)
                            print current_value

                            cmds.keyframe(new_anim_curve, edit=True, relative=True, valueChange=-current_value)
            cmds.animLayer(new_anim_layer_name, edit=True, override=False)
