"""
Import this mod to access quick short cuts, or setup hotkeys
"""
# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
import maya.cmds as cmds
import maya.mel as mel



# -----------------------------------------------------------------------------
# Reset translate, rotate, scale, zero keyframes
# -----------------------------------------------------------------------------
def zero_translate():
    """
    Function to zero out the translate attributes on the selected control
    """

    # Get selected controls
    controls = cmds.ls(sl=1, type="transform")

    # For each selected control, set the translate x,y,z values to 0
    for control in controls:
        cmds.setAttr(control+".translateX", 0)
        cmds.setAttr(control+".translateY", 0)
        cmds.setAttr(control+".translateZ", 0)

def zero_rotate():
    """
    Function to zero out the rotation attributes on the selected control
    """

    # Get selected controls
    controls = cmds.ls(sl=1, type="transform")

    # For each selected control, set the translate x,y,z values to 0
    for control in controls:
        cmds.setAttr(control+".rotateX", 0)
        cmds.setAttr(control+".rotateY", 0)
        cmds.setAttr(control+".rotateZ", 0)

def zero_scale():
    """
    Function to zero out the scale attributes on the selected control
    """

    # Get selected controls
    controls = cmds.ls(sl=1, type="transform")

    # For each selected control, set the translate x,y,z values to 0
    for control in controls:
        cmds.setAttr(control+".scaleX", 0)
        cmds.setAttr(control+".scaleY", 0)
        cmds.setAttr(control+".scaleZ", 0)

def zero_graph_keys():
    """
    Fucntion to zero out the selected keys in the graph editor. Doesn't rely on
    rotate, translate etc. Don't do anything if no keys are selected
    """
    key_count = cmds.keyframe(animation=keys, query=True, keyframeCount=True)
    if key_count != 0:
        cmds.keyframe(valueChange=0)



# -----------------------------------------------------------------------------
# Selection Shortcuts
# -----------------------------------------------------------------------------
def select_all_controls(control_id="_CTRL"):
    """
    Fucntion to select all animation controls based on identifying string
    e.g _CTRL, _ctrl,
    """
    # To start we will create an empty list that we will add all the controls to
    all_controls = []

    # Create a list of the selected controls and take the first item [0]
    control = cmds.ls(sl=1)[0]

    # Add the control to the all_controls list
    all_controls.append(control)

    # As controls in a rig are all relatives of one another we can search for
    # all the relatives, we can narrow it down to transform nodes
    control_relatives = cmds.listRelatives(control, type="transform")

    # Generally the control_id is on the end of a controls name
    # e.g BoyRig:head_CTRL
    # So we can search through the relatives and if the relative endswith the
    # control_id then we add it to the list we made earlier
    for relative in control_relatives:
        if relative.endswith(control_id):
            all_controls.append(relative)
        else:
            pass

    # Select this all_controls list
    cmds.select(all_controls)



# -----------------------------------------------------------------------------
# Toggle Visibilities
# -----------------------------------------------------------------------------
def viewport_toggle(toggle_option=None):
    """
    Function to toggle the given element in the viewport
    args: toggle_option: "polymeshes", "nurbsCurves", etc (see link for others)
    https://download.autodesk.com/us/maya/2008help/CommandsPython/modelEditor.html
    """
    # Get the current panel in focus or if no current focus panel the last one that was in focus
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
    cmds.selectKey(clear)
    # Get the current frame
    current_frame = cmds.currentTime(query=True)
    # Move the keyframe forward one frame
    cmds.keyframe(current_frame,edit=True, timeChange=1)

def move_key_backward():
    """
    Function to move the current keyframe backward one frame
    """
    # Clear the selected key
    cmds.selectKey(clear)
    # Get the current frame
    current_frame = cmds.currentTime(query=True)
    # Move the keyframe forward one frame
    cmds.keyframe(current_frame,edit=True, timeChange=-1)

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
