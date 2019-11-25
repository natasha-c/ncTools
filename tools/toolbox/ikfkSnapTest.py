# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel
from functools import wraps

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets

# ncTools
from ncTools.mods                   import uiMod;   reload(uiMod)
from ncTools.mods                   import animMod; reload(animMod)
from ncTools.tools.ncToolboxGlobals   import ncToolboxGlobals as G

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

# -----------------------------------------------------------------------------
# Class UI
# -----------------------------------------------------------------------------

class IkfkSnapTest_UI(uiMod.BaseSubUI):


    def create_layout(self):

        ikfkSnapTest = IkfkSnapTest()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text="IK/FK")

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
        self.all_frames_radio = uiMod.radio_button(label="All Frames", size=(self.w[6], self.h[1]))
        self.all_frames_radio.clicked.connect(lambda : setattr(ikfkSnapTest, "frame_type", "all"))
        self.main_layout.addWidget(self.all_frames_radio, 1, 0, 1, 6)

        self.keyed_frames_radio = uiMod.radio_button(label="Keyed Frames", size=(self.w[6], self.h[1]))
        self.keyed_frames_radio.clicked.connect(lambda : setattr(ikfkSnapTest, "frame_type", "keyed"))
        self.main_layout.addWidget(self.keyed_frames_radio, 2, 0, 1, 6)

        self.current_frame_radio = uiMod.radio_button(label="Current Frame", size=(self.w[6], self.h[1]))
        self.current_frame_radio.setChecked(True)
        self.current_frame_radio.clicked.connect(lambda : setattr(ikfkSnapTest, "frame_type", "current"))
        self.main_layout.addWidget(self.current_frame_radio, 3, 0, 1, 6)

        self.wing_switch = uiMod.push_button(label="Wing Switch To FK", size=(self.w[6], self.h[1]))
        self.wing_switch.clicked.connect(ikfkSnapTest.wing_switch_to_fk)
        self.main_layout.addWidget(self.wing_switch, 4, 0, 1, 6)

        self.switch_to_ik = uiMod.push_button(label="Wing Switch To IK", size=(self.w[6], self.h[1]))
        self.switch_to_ik.clicked.connect(ikfkSnapTest.wing_switch_to_ik)
        self.main_layout.addWidget(self.switch_to_ik, 5, 0, 1, 6)

        return self.frame_widget


class IkfkSnapTest():

    def __init__(self):

        if G.IkfkSnapTest:
            return
        G.IkfkSnapTest = self

        self.frame_type = "current"
        self.frames = []


    def wing_switch_to_fk(self):
        cmds.undoInfo(ock=True)
        self.setup_switch()
        self.match_fk()
        cmds.undoInfo(cck=True)
        print "done"


    def wing_switch_to_ik(self):
        cmds.undoInfo(ock=True)
        self.setup_switch()
        self.match_ik()
        cmds.undoInfo(cck=True)
        print "done"


    def get_frames(self):
        self.current_frame = int(cmds.currentTime(query=True))
        self.min_time = int(cmds.playbackOptions(query = True, min=True))
        self.max_time = int(cmds.playbackOptions(query=True, max=True))

        if self.frame_type == "all":
            self.frames = list(range(self.min_time, self.max_time+1))
        elif self.frame_type == "keyed":
            print self.controls
            for control in self.controls:
                frames = cmds.keyframe(control, query=True, timeChange=True)
                if frames:
                    self.frames = self.frames + frames
        elif self.frame_type == "current":
            self.frames = [self.current_frame]
        self.frames = list(set(self.frames))
        self.frames.sort()
        print "FRAMES: {frames}".format(frames=self.frames)
        return self.frames


    def setup_switch(self):
        # Define selection
        self.selection = cmds.ls(sl=1)

        # Define variables base on selection
        self.define_variables()

        # Make and bake locators for joints
        self.locators = []
        for joint in self.joint_names:
            for direction in self.direction:
                locator = self.make_locator(parent_object=self.nodes[joint][direction]["node"],
                                            name=self.nodes[joint][direction]["locator"],
                                            parent=True)
                self.locators.append(locator[0])
        self.bake(self.locators)

        # Zero all controls
        self.zero_controls(self.controls)

        # Create zero locators at zeroed joints
        for joint in self.joint_names:
            for direction in self.direction:
                locator = self.make_locator(parent_object=self.nodes[joint][direction]["node"],
                                            name=self.nodes[joint][direction]["zero_loc"],
                                            parent=False)
                self.locators.append(locator[0])


    def define_variables(self):

        # Node Names
        self.wingFKA = "wingFKA"
        self.wingFKB = "wingFKB"
        self.wingFKC = "wingFKC"
        self.wingFKD = "wingFKD"
        self.wingIK = "wingIK"
        self.wingPV = "wingPV"
        self.wingJA = "wingJA"
        self.wingJB = "wingJB"
        self.alulaJA = "alulaJA"
        self.alulaJB = "alulaJB"
        self.left = "l"
        self.right = "r"


        # FK Constraint pairs:
        self.fk_constraints = [(self.wingJA, self.wingFKA),
                               (self.wingJB, self.wingFKB),
                               (self.alulaJA, self.wingFKC),
                               (self.alulaJB, self.wingFKD)
                               ]

        # IK Constraint pairs:
        self.ik_constraints = [(self.alulaJA, self.wingIK),
                               (self.alulaJB, self.wingFKD)
                               ]


        # Variables base on selection
        self.namespace = self.selection[0].rpartition(":")[0]

        # Define direction
        self.direction = []
        for control in self.selection:
            if ":l_" in control:
                self.direction.append(self.left)
            elif ":r_" in control:
                self.direction.append(self.right)
        self.direction = list(set(self.direction))

        # Get nodes
        self.fk_controls = [self.wingFKA, self.wingFKB, self.wingFKC, self.wingFKD]
        self.ik_controls = [self.wingIK, self.wingPV]
        self.control_names = [self.wingFKA, self.wingFKB, self.wingFKC, self.wingFKD, self.wingIK, self.wingPV]
        self.joint_names = [self.wingJA, self.wingJB, self.alulaJA, self.alulaJB]

        # Node dictionary
        self.nodes = {}

        for control in self.control_names:
            self.nodes[control] = {}
            for direction in self.direction:
                self.nodes[control][direction] = {}
                self.nodes[control][direction]["node"] = "{0}:{1}_{2}_CTRL".format(self.namespace, direction, control)
        for joint in self.joint_names:
            self.nodes[joint] = {}
            for direction in self.direction:
                self.nodes[joint][direction] = {}
                self.nodes[joint][direction]["node"] = "{0}:{1}_{2}_JNT".format(self.namespace, direction, joint)
                self.nodes[joint][direction]["locator"] = "{0}_LOC".format(self.nodes[joint][direction]["node"])
                self.nodes[joint][direction]["zero_loc"] = "{0}_ZEROLOC".format(self.nodes[joint][direction]["node"])
                for pair in self.fk_constraints:
                    if joint == pair[0]:
                        fkChild = "{0}:{1}_{2}_CTRL".format(self.namespace, direction, pair[1])
                        self.nodes[joint][direction]["fkChild"] = fkChild
                for pair in self.ik_constraints:
                    if joint == pair[0]:
                        ikChild = "{0}:{1}_{2}_CTRL".format(self.namespace, direction, pair[1])
                        self.nodes[joint][direction]["ikChild"] = ikChild


        # Controls
        self.controls = []
        for control in self.control_names:
            for direction in self.direction:
                self.controls.append(self.nodes[control][direction]["node"])

        # Joints
        self.joints = []
        for joint in self.joint_names:
            for direction in self.direction:
                self.joints.append(self.nodes[control][direction]["node"])

        # Locators
        self.locators = []

        self.get_frames()


    def make_locator(self, parent_object=None, parent=False, name=None):
        locator = cmds.spaceLocator(name=name)
        if parent == True:
            cmds.parentConstraint(parent_object, locator)
        if parent == False:
            xform = cmds.xform(parent_object, m=True, ws=True, q=True)
            cmds.xform(locator, m=xform, ws=True)
        return locator


    @viewport_off
    def bake(self, objects):
        for frame in self.frames:
            cmds.currentTime(frame)
            for obj in objects:
                cmds.setKeyframe(obj)
                try:
                    cmds.setAttr(obj+".blendParent1", 1)
                except:
                    pass
                try:
                    cmds.setAttr(obj+".blendOrient1", 1)
                except:
                    pass
                try:
                    cmds.setAttr(obj+".blendPoint1", 1)
                except:
                    pass

        cmds.currentTime(self.current_frame)
        cmds.delete(objects, cn=True)


    def zero_controls(self, objects):
        # Zero controls
        for obj in objects:
            for tr in ["translate", "rotate"]:
                for xyz in ["X", "Y", "Z"]:

                    attribute = "{0}{1}".format(tr, xyz)
                    # Delete animation
                    if self.frame_type is not "current":
                        cmds.cutKey(obj, at=attribute, cl=True)
                    if self.frame_type is "current":
                        cmds.cutKey(obj, at=attribute, cl=True, time=(self.current_frame, self.current_frame))

                    try:
                        # Zero attribute
                        cmds.setAttr(obj+"."+attribute, 0)
                    except:
                        pass


    def match_fk(self):
        # Constrain zero joints to fk control
        for joint in self.joint_names:
            for direction in self.direction:
                zero_loc = self.nodes[joint][direction]["zero_loc"]
                control = self.nodes[joint][direction]["fkChild"] or None
                rotate_axis = ["x", "y", "z"]
                skip = []
                for xyz in rotate_axis:
                    attribute = "rotate{0}".format(xyz.upper())
                    attr = cmds.listAttr(control, k=True, st=[attribute])
                    if attr is None:
                        skip.append(xyz)
                try:
                    cmds.orientConstraint(zero_loc, control, skip=skip, mo=True)
                except:
                    pass


        # Match zero_loc to self.locators
        for joint in self.joint_names:
            for direction in self.direction:
                locator = self.nodes[joint][direction]["locator"]
                zero_loc = self.nodes[joint][direction]["zero_loc"]
                cmds.parentConstraint(locator, zero_loc)

        # Bake controls
        self.bake(self.controls)

        # Delete all locators
        cmds.delete(self.locators)

        # Euler filter controls
        self.euler_filter(self.controls)


    def euler_filter(self, controls):
        curves = cmds.ls(controls, l=True)
        cmds.filterCurve(curves)


    def match_ik(self):
        for pair in self.ik_constraints:
            for direction in self.direction:
                joint = pair[0]
                zero_loc = self.nodes[joint][direction]["zero_loc"]
                control = self.nodes[joint][direction]["ikChild"] or None
                axis = ["x", "y", "z"]
                skip = []
                for xyz in axis:
                    attribute = "rotate{0}".format(xyz.upper())
                    attr = cmds.listAttr(control, k=True, st=[attribute])
                    if attr is None:
                        skip.append(xyz)
                try:
                    cmds.orientConstraint(zero_loc, control, skip=skip, mo=True)
                    print control + "orientConstraint"
                except:
                    pass

                skip = []
                for xyz in axis:
                    attribute = "translate{0}".format(xyz.upper())
                    attr = cmds.listAttr(control, k=True, st=[attribute])
                    if attr is None:
                        skip.append(xyz)
                try:
                    cmds.pointConstraint(zero_loc, control, skip=skip, mo=True)
                    print control +"constrained"
                except:
                    pass


        # Match zero locs to locs
        for pair in self.ik_constraints:
            joint = pair[0]
            for direction in self.direction:
                locator = self.nodes[joint][direction]["locator"]
                zero_loc = self.nodes[joint][direction]["zero_loc"]
                cmds.parentConstraint(locator, zero_loc)

        # Create pole vector locator
        self.match_pole_vector()

        # Bake controls
        self.bake(self.controls)


        # Delete all locators
        cmds.delete(self.locators)

    @viewport_off
    def match_pole_vector(self):

        for frame in self.frames:
            cmds.currentTime(frame)

            for direction in self.direction:
                wingJA_VEC = [cmds.xform(self.nodes["wingJB"][direction]["locator"], t=True, ws=True, q=True)[i] - cmds.xform(self.nodes["wingJA"][direction]["locator"], t=True, ws=True, q=True)[i] for i in range(3)]
                wingJB_VEC = [cmds.xform(self.nodes["wingJB"][direction]["locator"], t=True, ws=True, q=True)[i] - cmds.xform(self.nodes["alulaJA"][direction]["locator"], t=True, ws=True, q=True)[i] for i in range(3)]
                cmds.xform(self.nodes["wingPV"][direction]["node"], t=[cmds.xform(self.nodes["wingJB"][direction]["locator"], t=True, q=True, ws=True)[i] + wingJA_VEC[i] * .75 + wingJB_VEC[i] * .75 for i in range(3)], ws=1)
                cmds.setKeyframe(self.nodes["wingPV"][direction]["node"])

        cmds.currentTime(self.current_frame)
