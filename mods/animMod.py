"""
Import this mod to access functions that are repeatedly needed in tools
"""

# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import traceback
from functools import wraps

# ncTools
from ncTools.tools.ncToolboxGlobals import ncToolboxGlobals as G


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

CTRL_id = ["_ctrl", "_anim", "_poleVector"]
LEFT_id = "_l"
RIGHT_id = "_r"
TOP_NODE = "master_anim"

# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------

def viewport_off(func):
    """
    Decorator to turn off viewport_off
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

def undo_chunk(func):
    """
    Decorator to undo the function
    """
    @wraps(func)
    def undo(*args, **kwargs):
        result = None 
        try:
            # Open undo chunk
            cmds.undoInfo(openChunk=True)
            result = func(*args, **kwargs)
        except Exception as e:
            # If error, print the error
            print traceback.format_exc()
            pm.displayError("## Error, see script editor: %s"%e)
        finally:
            # Close the chunk 
            cmds.undoInfo(closeChunk=True)
        return result 
    return undo 


# -----------------------------------------------------------------------------
# Copy 
# -----------------------------------------------------------------------------

def copy_animation(source=None, destination=None, pasteMethod="replace", offset=0, start=None, end=None, sourceLayer=None, rotateOrder=True):
    """
    Copy animation from source node to destination node
    """ 
    # Check is destination is a list or tuple, if not make it a list 
    if not isinstance(destination, (list, tuple)):
        destination = [destination]
    
    # Define paste layer and add selected destination targets to it 
    if not pasteLayer:
        pasteLayer = sourceLayer    
    
    cmds.select(destination)       
    cmds.animLayer(pasteLayer, edit=True, addSelectedObjects=True)


# -----------------------------------------------------------------------------
# Get things
# -----------------------------------------------------------------------------

def get_anim_curves(node=None, selected=True):
    """
    NEEDS UPDATING
    Function gets anim_curves based on given node and get_attributes
    either all or selected
    """
    anim_curves = []
    if selected == True:
        anim_curves = cmds.keyframe(query=True, sl=True, name=True)
    elif selected == False:
        anim_curves = cmds.keyframe(query=True, name=True)
    return anim_curves


def get_anim_layers(selected=True):
    """
    Function gets anim layers either all or selected
    """
    all_anim_layers = cmds.ls(type="animLayer")
    anim_layers = []
    if selected==True:
        for anim_layer in all_anim_layers:
            if cmds.animLayer(anim_layer, query = True, sel=True):
                anim_layers.append(anim_layer)
    else:
        anim_layers = all_anim_layers
    return anim_layers


def get_attributes(node=None, attribute_options=None):
    """
    Function returns a list of attributes based on the given node, and the
    attribute options such as keyable, c, unlocked etc
    """
    options_true = []
    for option in attribute_options:
        option_true = "{0} = True".format(option)
        options_true.append(option_true)
    options_string = ", ".join(options_true)
    attributes = eval("cmds.listAttr('{0}', {1})".format(node, options_string))
    return attributes


def get_controls(selected=None):
    if selected == False:
        rig = get_top_node(cmds.ls(sl=1)[0])
        controls = get_rig_controls(rig=rig)
    elif selected == True:
        controls = []
        controls = cmds.ls(sl=1, type="transform")
    return controls
        

def get_rig_controls(rig=None):
    nurbsCurves = cmds.listRelatives(rig, ad=True, type=["nurbsCurve", "locator"])
    controls = []
    for curve in nurbsCurves:
            control = cmds.listRelatives(curve, parent=True, type="transform")[0]
            controls.append(control)
    controls = list(dict.fromkeys(controls))
    return controls

def get_child_controls(node=None): 
    children = []
    nurbsCurves = cmds.listRelatives(node, ad=True, type="nurbsCurve")
    for curve in nurbsCurves:
        control = cmds.listRelatives(curve, parent=True, type="transform")[0]
        children.append(control)
    return children

def get_current_frame():
    """
    Function gets current frame on the timeline
    """
    current_frame = cmds.currentTime(query=True)
    return current_frame

def get_frames():
    """
    Function gets selected frames():
    """
    G.playback_slider = G.playback_slider or mel.eval("$tmpVar = $gPlayBackSlider")
    timeline_frames = []
    timeline_frame_range = cmds.timeControl(G.playback_slider, query=True, rangeArray=True)
    timeline_frames = range(int(timeline_frame_range[0]), int(timeline_frame_range[1]))
    #graphEditor_frames = cmds.keyframe(query=True, selected=True, timeChange=True)

    frames = timeline_frames
    #elif graphEditor_frames is None:
    #    frames = timeline_frames
    #elif len(timeline_frames) == 1 and len(graphEditor_frames) > 0:
    #    frames = graphEditor_frames

    return frames


def get_keys(anim_curve=None, selected=True):
    """
    Function gets the keys on the given anim curve, can be all or selected
    """
    keys = []
    if selected == True:
        keys = cmds.keyframe(anim_curve, query=True, selected=True)
    elif selected == False:
        keys = cmds.keyframe(anim_curve, query=True)
    keys = list(set(keys))
    return keys


def get_key_times(anim_curve=None, selected=True):
    """
    Function gets the times of the keys on a given anim curve, can be all or selected
    """
    key_times = []
    if selected == True:
        key_times = cmds.keyframe(anim_curve, query=True, selected=True, timeChange=True)
    elif selected == False:
        key_times = cmds.keyframe(anim_curve, query=True, selected=False, timeChance=True)
    return key_times


def get_key_values(anim_curve=None, selected=True):
    """
    Function gets the values of the keys on a given anim curve, can be all or selected
    """
    key_values = []
    if selected == True:
        key_values = cmds.keyframe(anim_curve, query=True, selected=True, valueChange=True)
    elif selected == False:
        key_values = cmds.keyframe(anim_curve, query=True, selected=False, valueChange=True)
    return key_values


def get_namespace(node=None):
    """
    Function gets namespace of given node
    """
    namespace = node.rpartition(":")[0]
    return namespace


def get_opposite_control(node=None):
    """
    Function gets the opposite control based on node, if no opposite returns node
    """
    if LEFT_id in node:
        opposite_control = node.replace(LEFT_id, RIGHT_id)
    elif RIGHT_id in node:
        opposite_control = node.replace(RIGHT_id, LEFT_id)
    else:
        opposite_control = node
    return opposite_control


def get_playback_range():
    """
    Function returns the playback range 
    """ 
    start_frame = cmds.playbackOptions(min=True, query=True)
    end_frame = cmds.playbackOptions(max=True, query=True)
    return (start_frame, end_frame)


def get_prev_current_next(iterable):
    previous, current, next = tee(iterable, 3)
    previous = chain([None], previous)
    next = chain(islice(next, 1, None), [None])
    return izip(previous, current, next)


def get_selected():
    """
    Function gets all selected objects
    """
    selected = cmds.ls(sl=1)
    return selected


def get_top_node(node=None):
    """
    Function gets top node of given node
    """
    current_node = [node]
    parent = cmds.listRelatives(current_node, p=True, fullPath=True, type="transform")
    while parent is not None:
        current_node = parent
        parent = cmds.listRelatives(current_node, p=True, fullPath=True, type="transform")
    top_node = current_node[0]
    return top_node




# -----------------------------------------------------------------------------
# Querys
# -----------------------------------------------------------------------------

def is_control_in_anim_layer(control, anim_layer):
    # Get all the anim layers this control is a part of
    affected_layers = cmds.animLayer([control], query=True, affectedLayers=True)
    if affected_layers==None:
        affected_layers = ["BaseAnimation"]
    # Query if the given anim layer is one of the affected layers
    if anim_layer in affected_layers:
        return True
    else:
        return False

# -----------------------------------------------------------------------------
# Edit Values
# -----------------------------------------------------------------------------
       
def zero_attribute(node=None, attribute=None):
    """
    Function to zero out the attributes on the selected control
    """
    for axis in ["X", "Y", "Z", ""]:
        control_attr = "{0}.{1}{2}".format(node, attribute, axis)
        try:
            cmds.setAttr(control_attr, 0)
        except:
            pass


def zero_translate(node):
    """
    Function to zero out the translate attributes on the selected control
    """
    zero_attribute(node=node, attribute="translate")


def zero_rotate(node):
    """
    Function to zero out the rotation attributes on the selected control
    """
    zero_attribute(node=node, attribute="rotate")

def zero_scale(node):
    """
    Function to zero out the scale attributes on the selected control
    """
    zero_attribute(node=node, attribute="scale")

