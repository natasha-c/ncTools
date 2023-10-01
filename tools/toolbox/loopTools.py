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


class LoopTools_UI(uiMod.BaseSubUI):

    def create_layout(self):
        #Create tool instance
        loopTools = LoopTools()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Loop Tools")

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
        self.frame_range_start_display = uiMod.line_edit(size=(self.w[3], self.h[1]))
        self.frame_range_start_display.setText(str(G.loopTools.start_loop))
        self.main_layout.addWidget(self.frame_range_start_display, 0, 0, 1, 6)

        self.frame_range_end_display = uiMod.line_edit(size=(self.w[3], self.h[1]))
        self.frame_range_end_display.setText(str(G.loopTools.end_loop))
        self.main_layout.addWidget(self.frame_range_end_display, 0, 3, 1, 6)

        self.store_frame_range_button = uiMod.push_button(label = "Store Frame Range", size=(self.w[6], self.h[1]))
        self.store_frame_range_button.clicked.connect(G.loopTools.store_frame_range)
        self.store_frame_range_button.clicked.connect(self.set_frame_range)
        self.main_layout.addWidget(self.store_frame_range_button, 1, 0, 1, 6)

        self.delete_outside_timeline_button = uiMod.push_button(label = "Delete Outside Timeline", size=(self.w[6], self.h[1]))
        self.delete_outside_timeline_button.clicked.connect(G.loopTools.delete_keyframes_outside_timeline)
        self.main_layout.addWidget(self.delete_outside_timeline_button, 2, 0, 1, 6)

        self.cycle_all_animation_curves_button = uiMod.push_button(label = "Cycle All Curves", size=(self.w[6], self.h[1]))
        self.cycle_all_animation_curves_button.clicked.connect(G.loopTools.cycle_anim_curves)
        self.main_layout.addWidget(self.cycle_all_animation_curves_button, 3, 0, 1, 6)

        self.add_loop_cycle_button = uiMod.push_button(label = "Add Loop Cycle", size=(self.w[6], self.h[1]))
        self.add_loop_cycle_button.clicked.connect(G.loopTools.add_loop_cycle)
        self.main_layout.addWidget(self.add_loop_cycle_button, 4, 0, 1, 6)

        self.offset_timeline_by_half_button = uiMod.push_button(label = "Offset Timeline By Half Loop", size=(self.w[6], self.h[1]))
        self.offset_timeline_by_half_button.clicked.connect(G.loopTools.offset_timeline_by_half_loop)
        self.main_layout.addWidget(self.offset_timeline_by_half_button, 5, 0, 1, 6)

        self.cleanup_loop_button = uiMod.push_button(label = "Cleanup Loop", size=(self.w[6], self.h[1]))
        self.cleanup_loop_button.clicked.connect(G.loopTools.cleanup_loop)
        self.main_layout.addWidget(self.cleanup_loop_button, 6, 0, 1, 6)

        return self.frame_widget

    def set_frame_range(self):
        self.frame_range_start_display.setText(str(G.loopTools.start_loop))
        self.frame_range_end_display.setText(str(G.loopTools.end_loop))


class LoopTools(object):

    def __init__(self):
        #if G.loopTools:
        #    return
        G.loopTools = self
        self.store_frame_range()

    @animMod.viewport_off
    @animMod.undo_chunk
    def store_frame_range(self):
        # Get timeline
        timeline = animMod.get_playback_range()

        # Define Start Loop Global
        G.loopTools.start_loop = timeline[0]

        # Define End Loop Global
        G.loopTools.end_loop = timeline[1]       



    def delete_keyframes_outside_timeline(self):

        # Get all controls
        controls = animMod.get_controls(selected=True)

        # Get timeline frame range 
        timeline = animMod.get_playback_range()

        # Get first and last keyframe in scene
        first_keyframe = cmds.findKeyframe(which="first")
        last_keyframe = cmds.findKeyframe(which="last")

        # Get anim curves for each control, set a keyframe at start and end of timeline and delete keyframes outside of timeline
        for control in controls:
            # Set a keyframe on the first and last frame of the timeline
            cmds.setKeyframe(insert=True, time=timeline)

            # Cut keyframes outside timeline
            if first_keyframe != timeline[0]:
                    cmds.cutKey(control, time=(first_keyframe, (timeline[0]-1)))
            if last_keyframe != timeline[1]:
                    cmds.cutKey(control, time=((timeline[1]+1), last_keyframe)) 


    @animMod.viewport_off
    @animMod.undo_chunk
    def cycle_anim_curves(self):
        # animCurveEditor -edit -displayInfinities false graphEditor1GraphEd;
        # Ensure graphEditor is showing infinity 
        if cmds.animCurveEditor('graphEditor1GraphEd', exists=True):
            print True
            cmds.animCurveEditor('graphEditor1GraphEd', edit=True, displayInfinities='on')
        # Set infinity 
        cmds.setInfinity(pri="cycle", poi="cycle")


    @animMod.viewport_off
    @animMod.undo_chunk
    def add_loop_cycle(self):

        # Get all controls
        controls = animMod.get_controls(selected=True)

        # Get timeline frame range 
        timeline = animMod.get_playback_range()

        # Copy animation 
        cmds.copyKey(controls, time=timeline)

        # Paste animation with an offset equal to timeline range 
        cmds.pasteKey(controls, to=(timeline[1]-timeline[0]))



    @animMod.viewport_off
    @animMod.undo_chunk
    def offset_timeline_by_half_loop(self):

        # Get timeline frame range 
        timeline = animMod.get_playback_range()

        # Halfway point of range 
        midpoint = int((timeline[1]-timeline[0])/2)

        # Set playback range
        cmds.playbackOptions(min=(midpoint+timeline[0]), max=midpoint+(timeline[1]) )



     

    @animMod.viewport_off
    @animMod.undo_chunk
    def cleanup_loop(self):
        # Get controls
        controls = animMod.get_controls(selected=False)
        
        # Delete outside current timeline loop 
        self.delete_keyframes_outside_timeline()

        # Cycle animations
        self.cycle_anim_curves()

        # Set timeline to saved loop range 
        cmds.playbackOptions(min=G.loopTools.start_loop, max=G.loopTools.end_loop)

        # Bake animation
        cmds.bakeResults(controls, simulation=True, time=(G.loopTools.start_loop, G.loopTools.end_loop), sampleBy=1, preserveOutsideKeys=False)
        print("Cleanup")
