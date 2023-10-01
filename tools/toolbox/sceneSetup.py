# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
import maya.cmds as cmds

# PySide2
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

# ncToolbox
from ncTools.mods                 import uiMod;       reload(uiMod)
from ncTools.mods                 import animMod;     reload(animMod)
from ncTools.tools.ncToolboxGlobals     import ncToolboxGlobals as G


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------

def viewport_off(func):
    """
    Decorator to turn viewport_off
    """
    @wraps(func)
    def wrap(*args, **kwargs):

        # Turn off main panel:
        mel.eval("paneLayout -e -manage false $gMainPane")

        try:
            return func(*args, **kwargs)
        except Exception:
            raise # will raise original setVerticalScrollBar
        finally:
            mel.eval("paneLayout -e -manage true $gMainPane")

    return wrap


# -----------------------------------------------------------------------------
# Class UI
# -----------------------------------------------------------------------------

class SceneSetup_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        sceneSetup = SceneSetup()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Scene Setup", base_width=self.w[1], base_height=self.h[1])

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
        row = 0
        row += 1
        self.cut_animation = uiMod.push_button(label = "Cut and Shift", size=(self.w[6], self.h[1]))
        self.cut_animation.clicked.connect(sceneSetup.cut_and_shift)
        self.main_layout.addWidget(self.cut_animation, row, 0, 1, 6)

        row += 1
        self.move_to_origin = uiMod.push_button(label = "Move To Origin", size=(self.w[6], self.h[1]))
        self.move_to_origin.clicked.connect(sceneSetup.move_to_origin)
        self.main_layout.addWidget(self.move_to_origin, row, 0, 1, 6)

        row += 1
        self.prep_mocap = uiMod.push_button(label = "Prep Mocap", size=(self.w[6], self.h[1]))
        self.prep_mocap.clicked.connect(sceneSetup.prep_mocap)
        self.main_layout.addWidget(self.prep_mocap, row, 0, 1, 6)

        return self.frame_widget

# -----------------------------------------------------------------------------
# Class Tool
# -----------------------------------------------------------------------------

class SceneSetup(object):

    def __init__(self):
        G.sceneSetup = self
    
    def cut_and_shift(self):
        """
        Cut and shift the animation based on the frame range
        """
        self.cut_animation()
        self.shift_animation()
        self.create_mocap_locator()

    
    def create_mocap_locator(self):
        """
        Create a locator to add annotation to store mocap frame range and data
        """
        mocap_loc = cmds.spaceLocator(name="mocap_loc")


    def cut_animation(self):
        """
        Adjust the working range to the required mocap selection
        Delete all other keys 
        Move to frame zero
        """
        (self.start_frame, self.end_frame) = animMod.get_playback_range()
        
        self.all_controls = animMod.get_controls(selected=False)  

        first_key = cmds.findKeyframe(self.all_controls, which="first")
        last_key = cmds.findKeyframe(self.all_controls, which="last")
        cmds.setKeyframe(self.all_controls, time=self.start_frame, insert=True)
        cmds.cutKey(self.all_controls, time=(first_key, self.start_frame-1), option="keys", cl=True)            
        cmds.setKeyframe(self.all_controls, time=self.end_frame, insert=True)
        cmds.cutKey(self.all_controls, time=(self.end_frame+1, last_key), option="keys", cl=True)     
        

    def shift_animation(self):
        """
        Shift the current frame range to start at zero
        """
        cmds.keyframe(  self.all_controls, 
                        time=(self.start_frame, self.end_frame),
                        timeChange=-self.start_frame,
                        option="over",
                        relative=True,
                        )

        #Set new playback range 
        cmds.playbackOptions(min=0, max=self.end_frame-self.start_frame, aet=self.end_frame-self.start_frame)
        cmds.currentTime(0)

    #@viewport_off
    def move_to_origin(self):
        """
        Move the bodyAnim control to (x,y)=(0,0)
        """
        # Get all_controls 
        self.all_controls = animMod.get_controls(selected=False)

        # Get namesapce 
        namespace = animMod.get_namespace(node=self.all_controls[0])

        # Create locator 
        space_loc = cmds.spaceLocator(name="space_loc")[0]
        cmds.setAttr(space_loc+".localScaleX", 30)
        cmds.setAttr(space_loc+".localScaleY", 30)
        cmds.setAttr(space_loc+".localScaleZ", 30)
        
        # Match translation to bodyanim 
        body_anim_ctrl = "{0}:body_anim".format(namespace)
        body_anim_t = cmds.xform(body_anim_ctrl, query=True, translation=True, ws=True)

        cmds.xform(space_loc, translation=body_anim_t, ws=True)
        cmds.setAttr(space_loc+".translateZ", 0)
        body_anim_rx = cmds.getAttr(body_anim_ctrl+".rotateX")
        cmds.setAttr(space_loc+".rotateZ", body_anim_rx)

        # Create control locator
        control_loc = "{0}_loc".format(body_anim_ctrl)
        cmds.spaceLocator(name=control_loc)

        # Parent the control locator beneath the space locator 
        cmds.parent(control_loc, space_loc)

        # Parent constrain the control locator to the control 
        cmds.parentConstraint(body_anim_ctrl, control_loc)

        # Bake the control locator 
        start_frame = cmds.playbackOptions(query=True, min=True)
        end_frame = cmds.playbackOptions(query=True, max=True)
        cmds.bakeResults(control_loc, simulation=True, time=(start_frame, end_frame))
        
        # Delete the constraint 
        cmds.delete(control_loc, constraints=True)

        # Constrain control to control locator 
        cmds.parentConstraint(control_loc, body_anim_ctrl)

        # Zero animation on space locator
        animMod.zero_translate(node=space_loc)
        animMod.zero_rotate(node=space_loc)

        # Bake the control 
        cmds.bakeResults(body_anim_ctrl, simulation=True, time=(start_frame, end_frame), sb=True)

        # Delete the constraint 
        cmds.delete(body_anim_ctrl, constraints=True)

        # Delete the locators 
        cmds.delete(space_loc)


    def prep_mocap(self):
        """
        Copy mocap animation on base layer to new mocap layer
        Duplicate layer - base layer 
        Delete leg animation 
        cut body_anim to spine_1 
        Divide spine translate value by 4 
        Match IK to FK, and back again 
        """ 

        # Create new override layer with all controls 
        base_anim_layer = cmds.animLayer(root=True, query=True)

        # Copy base layer to new layers - mocap and base 
        all_controls = animMod.get_controls(selected=False)
        cmds.select(all_controls)
        mocap_layer = cmds.animLayer("mocap",
                                     override=True,
                                     addSelectedObjects=True,
                                     copyAnimation=base_anim_layer)

        base_layer = cmds.animLayer("base",
                                    override=True,
                                    addSelectedObjects=True,
                                    copyAnimation=base_anim_layer)

        # Delete leg animation on base layer 
        namespace = animMod.get_namespace(node=all_controls[0])
        leg_group = "{0}:leg_sys_grp".format(namespace)
        leg_controls = animMod.get_child_controls(node=leg_group)
        cmds.cutKey(leg_controls, animLayer="base", option="curve")

        # Cut body_anim animation, paste on spine_01
        spine_control = "{0}:spine_01_anim".format(namespace)
        cmds.cutKey(body_anim_ctrl, animLayer="base", option="curve")
        cmds.pasteKey(spine_control, animLayer="base", option="curve")

        #  



        print "DONE"

        

        






        


        



