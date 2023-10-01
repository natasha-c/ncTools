"""
Import this mod to access quick short cuts, or setup hotkeys
"""
# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
import maya.cmds as cmds
import maya.mel as mel

# ncToolbox
from ncTools.mods                 import animMod;     reload(animMod)

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
CTRL_id = ["fk_ctrl", "_anim", "_poleVector"]
LEFT_id = "_l"
RIGHT_id = "_r"



# -----------------------------------------------------------------------------
# Reset translate, rotate, scale, zero keyframes
# -----------------------------------------------------------------------------
def zero_attribute(attribute):
    """
    Function to zero out the attributes on the selected control
    """
    # Get selected controls
    controls = cmds.ls(sl=1, type="transform")

    # For each selected control, set the translate x,y,z values to 0
    for control in controls:
        for axis in ["X", "Y", "Z"]:
            control_attr = "{0}.{1}{2}".format(control, attribute, axis)
            try:
                cmds.setAttr(control_attr, 0)
            except:
                pass


def zero_translate():
    """
    Function to zero out the translate attributes on the selected control
    """
    zero_attribute(attribute="translate")


def zero_rotate():
    """
    Function to zero out the rotation attributes on the selected control
    """
    zero_attribute(attribute="rotate")

def zero_scale():
    """
    Function to zero out the scale attributes on the selected control
    """
    zero_attribute(attribute="scale")

def zero_graph_keys():
    """
    Fucntion to zero out the selected keys in the graph editor. Doesn't rely on
    rotate, translate etc. Don't do anything if no keys are selected
    """
    key_count = cmds.keyframe(animation="keys", query=True, keyframeCount=True)
    if key_count != 0:
        cmds.keyframe(valueChange=0)



# -----------------------------------------------------------------------------
# Selection Shortcuts
# -----------------------------------------------------------------------------
def select_all_controls():
    """
    Fucntion to select all animation controls based on identifying string
    e.g _CTRL, _ctrl,
    """
    all_controls = animMod.get_controls(selected=False)
    cmds.select(all_controls)

def add_to_select_group():
    """
    Function to add selected controls to a temporary global group for quick select
    """

    from ncTools.mods import animMod 
    global tempSelectGroup

    #Create list of currently selected controls
    selected_controls = animMod.get_controls(selected=True)

    # Does tempSelectGroup exist, if not create it.
    try: 
        print "Adding", selected_controls, "to", tempSelectGroup
    except:
        tempSelectGroup = []
        print "Creating temp select group"

    #Add selected controls to temp global list
    for i in selected_controls:
        tempSelectGroup.append(i)
    tempSelectGroup = list(set(tempSelectGroup))

def clear_select_group():
    """
    Function to clear the temporary select group
    """
    global tempSelectGroup

    try:
        tempSelectGroup = []
        cmds.warning("Previous temp select group cleared")
    except:
        cmds.warning("No previous groups saved this session")

def select_select_group():
    """
    Function to select the temporary select group
    """
    global tempSelectGroup

    cmds.select(tempSelectGroup)
    cmds.warning("Selected temp select group")
# -----------------------------------------------------------------------------
# Toggle Visibilities
# -----------------------------------------------------------------------------
def viewport_toggle(toggle_option=None):
    """
    Function to toggle the given element in the viewport
    args: toggle_option: "polymeshes", "nurbsCurves", etc (see link for others)
    https://download.autodesk.com/us/maya/2008help/CommandsPython/modelEditor.html
    """
    # Get the current panel in focus or if no current focus panel the last one that was in focuserfghmnj bv
    current_panel = cmds.getPanel(withFocus=True)
    # If the current panel is a model panel then query the visibility of the element
    # and change the visibility
    if cmds.getPanel(typeOf=current_panel) == "modelPanel":
        visibility = eval("cmds.modelEditor(current_panel, query=True, {0}=True)".format(toggle_option))
        eval("cmds.modelEditor(current_panel, edit=True, {0}=1-visibility)".format(toggle_option))



# -----------------------------------------------------------------------------
# Key shortcuts
# -----------------------------------------------------------------------------
def move_key_forward():
    """
    Function to move the current keyframe forward one frame
    """
    # Clear the selected key
    cmds.selectKey(clear=True)
    # Get the current frame
    current_frame = cmds.currentTime(query=True)
    # Move the keyframe forward one frame
    cmds.keyframe(time=(current_frame, current_frame), edit=True, timeChange=1, relative=True)
    # Move the timeslider 
    cmds.currentTime(current_frame+1, edit=True)

def move_key_backward():
    """
    Function to move the current keyframe backward one frame
    """
    # Clear the selected key
    cmds.selectKey(clear=True)
    # Get the current frame
    current_frame = cmds.currentTime(query=True)
    # Move the keyframe forward one frame
    cmds.keyframe(time=(current_frame, current_frame), edit=True, timeChange=-1, relative=True)
    # Move the timeslider 
    cmds.currentTime(current_frame-1, edit=True)

def add_frame():
    """
    Function to add a frame at the current position and shift all keys
    after current frame forwards
    """
    mel.eval("timeSliderEditKeys addInbetween;")

def remove_frame():
    """
    Function to remove a frame at the current position and shift all keys after
    current frame backwards
    """
    mel.eval("timeSliderEditKeys removeInbetwen;")

def delete_key():
    """
    Function to delete the key at the current frame
    """
    mel.eval("timeSliderClearKey;")

def copy_key():
    """
    Function to copy the current key
    """
    mel.eval(timeSliderCopyKey)

def paste_key():
    """
    Function to copy the current key
    """
    mel.eval("timeSliderPasteKey false;")

def copy_to_opposite_control():
    """
    Function to copy the key from the selected control to the opposite control, eg copy left control to right control
    """
    selected_controls = cmds.ls(sl=1)
    current_frame = cmds.currentTime(query=True)
    print current_frame
    for control in selected_controls:
        if "_l_" in control:
            opposite = control.replace("_l_", "_r_")
        elif "_r_" in control:
            opposite = control.replace("_r_", "_l_")
        else:
            opposite = control       
        cmds.copyKey(control, time = (current_frame, current_frame))
        cmds.pasteKey(opposite, time =(current_frame, current_frame), option="merge")
 
