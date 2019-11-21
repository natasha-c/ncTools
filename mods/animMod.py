"""
Import this mod to access functions that are repeatedly needed in tools
"""
# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
# maya
import maya.cmds as cmds
import maya.mel as mel

# ncTools
from ncTools.tools.ncToolboxGlobals import ncToolboxGlobals as G

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
CTRL_sfx = "_CTRL"
LEFT_pfx = ":l_"
RIGHT_pfx = ":r_"


# -----------------------------------------------------------------------------
# Get things
# -----------------------------------------------------------------------------
def get_anim_curves(node=None, attribute=None, anim_curve=None):
    """
    Function gets anim_curves based on given node and get_attributes
    either all or selected
    """
    anim_curves = []
    return anim_curves


def get_anim_layers(node=None, selected=True):
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


def get_controls(selected=True):
    """
    Function gets controls either all or selected
    """
    controls = []
    if selected==True:
        selection = cmds.ls(sl=1)
        for control in selection:
            if control.endswith(CTRL_sfx):
                controls.append(control)
    return controls


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
    timeline_frame_range = cmds.timeControl(G.playback_slider, query = True, rangeArray = True)
    timeline_frames = range(int(timeline_frame_range[0]), int(timeline_frame_range[1]))
    graphEditor_frames = cmds.keyframe(query=True, selected=True, timeChange=True)

    if len(timeline_frames) > 1:
        frames = timeline_frames
    elif graphEditor_frames is None:
        frames = timeline_frames
    elif len(timeline_frames) == 1 and len(graphEditor_frames) > 0:
        frames = graphEditor_frames

    return frames

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
    if LEFT_pfx in node:
        opposite_control = node.replace(LEFT_pfx, RIGHT_pfx)
    elif RIGHT_pfx in node:
        opposite_control = node.replace(RIGHT_pfx, LEFT_pfx)
    else:
        opposite_control = node
    return opposite_control


def get_rigs(node=None, selected=True):
    """
    Function gets rigs, either all or selected
    """
    rigs = []
    return rigs


def get_selected():
    """
    Function gets all selected objects
    """
    selected = cmds.ls(sl=1)
    return selected


def get_timeline_range():
    """
    Function reutrns the timeline frame range
    """
    G.playback_slider = G.playback_slider or mel.eval("$tmpVar = $gPlayBackSlider")
    timeline_range = cmds.timeControl(G.playback_slider, query=True, rangeArray=True)
    return timeline_range


def get_top_node(node=None):
    """
    Function gets top node of given node
    """
    top_nodes = []
    return top_nodes

