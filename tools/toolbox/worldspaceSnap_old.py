# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

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



class WorldspaceSnap_UI(uiMod.BaseSubUI):


    def create_layout(self):

        worldspaceSnap = WorldspaceSnap()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text="Worldspace Snap")

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
        self.snap_selected = uiMod.push_button(label="Snap Selection", size=(self.w[6], self.h[1]))
        self.snap_selected.clicked.connect(worldspaceSnap.snap_selection)
        self.main_layout.addWidget(self.snap_selected, row, 0, 1, 6)

        row += 1
        self.snap_translate = uiMod.push_button(label="Snap Translate", size=(self.w[6], self.h[1]))
        self.snap_translate.clicked.connect(worldspaceSnap.snap_translate)
        self.main_layout.addWidget(self.snap_translate, row, 0, 1, 6)

        row += 1
        self.snap_rotate = uiMod.push_button(label="Snap Rotate", size=(self.w[6], self.h[1]))
        self.snap_rotate.clicked.connect(worldspaceSnap.snap_rotate)
        self.main_layout.addWidget(self.snap_rotate, row, 0, 1, 6)
        """
        self.snap_rig = uiMod.push_button(label="Snap Rigs", size=(self.w[6], self.h[1]))
        self.snap_rig.clicked.connect(worldspaceSnap.snap_rig)
        self.main_layout.addWidget(self.snap_rig, 2, 0, 1, 6)

        self.snap_selected_to_rig = uiMod.push_button(label="Snap Selected to Rig", size=(self.w[6], self.h[1]))
        self.snap_selected_to_rig.clicked.connect(worldspaceSnap.snap_selected_to_rig)
        self.main_layout.addWidget(self.snap_selected_to_rig, 3, 0, 1, 6)

        self.make_locators = uiMod.push_button(label="Make Locators", size=(self.w[6], self.h[1]))
        self.make_locators.clicked.connect(worldspaceSnap.make_locators)
        self.main_layout.addWidget(self.make_locators, 4, 0, 1, 6)

        self.test = uiMod.push_button(label="test", size=(self.w[6], self.h[1]))
        self.test.clicked.connect(worldspaceSnap.test)
        self.main_layout.addWidget(self.test, 5, 0, 1, 6)"""

        return self.frame_widget


class WorldspaceSnap():

    def __init__(self):
        G.WorldspaceSnap = self

    def snap(self, source=None, target=None, translation=False, rotation=False):
        """
        Procedure that retrieves the xform position of one object and applies it to the target
        """
        source_translate = cmds.xform(source, query=True, ws=True, t=True)
        source_rotation = cmds.xform(source, query=True, ws=True, ro=True)
        if translation==True:
            cmds.xform(target, ws=True, t=source_translate)
        if rotation==True:
            cmds.xform(target, ws=True, ro=source_rotation)


    def snap_selection(self):
        """
        Procedure that snaps the controls to the the world position of the first selected
        """
        selection = cmds.ls(sl=1)
        source_control = selection[0]
        selection.remove(source_control)
        targets = selection
        for target in targets:
            self.snap(source=source_control, target=target, translation=True, rotation=True)


    def snap_translate(self):
        """
        Procedure that snaps the controls to the the world translation position of the first selected
        """
        selection = cmds.ls(sl=1)
        source_control = selection[0]
        selection.remove(source_control)
        targets = selection
        for target in targets:
            self.snap(source=source_control, target=target, translation=True, rotation=False)


    def snap_rotate(self):
        """
        Procedure that snaps the controls to the the world translation position of the first selected
        """
        selection = cmds.ls(sl=1)
        source_control = selection[0]
        selection.remove(source_control)
        targets = selection
        for target in targets:
            self.snap(source=source_control, target=target, translation=False, rotation=True)


    def snap_rig(self):
        print "snap rig"
        source_rig = cmds.ls(sl=1)[0]
        target_rig = cmds.ls(sl=1)[1]

        source_namespace = source_rig.rpartition(":")[0]
        target_namespace = target_rig.rpartition(":")[0]

        source_controls = animMod.get_target("controls", selected=False, node=source_rig)
        print source_controls

        for source_control in source_controls:
            control = source_control.rpartition(":")[2]
            target_control = target_namespace + ":" + control

            if cmds.objExists(target_control):
                self.snap(source_control, target_control)
            else:
                print target_control, "doesn't exist"




    """
    def snap(self, source, target):
        source_xform = cmds.xform(source, query=True, ws=True, m=True)
        cmds.xform(target, ws=True, m=source_xform)"""

    def snap_selected_to_rig(self):
        selection = cmds.ls(sl=1)
        print selection
        source_rig = selection[-1]
        selection.remove(source_rig)
        target_controls = selection
        print target_controls

        source_namespace = source_rig.rpartition(":")[0]
        target_namespace = target_controls[0].rpartition(":")[0]

        for target_control in target_controls:
            control_name = target_control.rpartition(":")[2]
            source_control = source_namespace + ":" + control_name

            self.snap(source_control, target_control)

    def make_locators(self):
        print "make locators"



    def test2(self):
        print "test"

        source_rig = cmds.ls(sl=1)[0]
        #target_rig = cmds.ls(sl=1)[1]

        source_namespace = source_rig.rpartition(":")[0]
        #target_namespace = target_rig.rpartition(":")[0]

        source_relatives = cmds.listRelatives(source_rig, type="transform", ad=True)
        source_relatives.reverse()
        source_relatives = [source_rig] + source_relatives
        print source_relatives
        print len(source_relatives)

        parent_list = []
        parent_list = set(parent_list)
        naughty_list = []
        naughty_list = set(naughty_list)

        for node in source_relatives:

            node_index = source_relatives.index(node)
            print node_index, ":", node, "---------------------"
            """if node_index == 5:
                break"""


            #Does it have children?
            child_connection = cmds.listConnections(node, type="transform", s=False, d=True)
            child_group = cmds.listRelatives(node, type="transform", ad=True)
            child_constraint = cmds.listConnections(node, type="constraint", s=False, d=True)
            children = []
            for list in [child_connection, child_group, child_constraint]:
                if list:
                    children = children + list
            print "CHILDREN:", children

            # Are there children in the parent list?
            child_in_parent_list = []
            for child in children:
                if child in parent_list:
                    child_in_parent_list.append(child)
            if len(child_in_parent_list) > 0:
                print node, "has children:", child_in_parent_list, "in parent list"
                print "Remove children from parent_list"

                for child in child_in_parent_list:
                    if child in parent_list:
                        parent_list.remove(child)
                        naughty_list.add(child)

            # Add node to parent list
            parent_list.add(node)

            # For child in naughty list, find it's lowest parent in the parent list
            parent_list = (parent_list)

            for child in naughty_list:
                parent_connection = cmds.listConnections(node, type="transform", s=True, d=False)
                parent_group = cmds.listRelatives(node, type="transform", p=True)
                parent_constraint = cmds.listConnections(node, type="constraint", s=True, d=False)




        print parent_list
        print naughty_list


    def test(self):

        source_rig = cmds.ls(sl=1)[0]
        #target_rig = cmds.ls(sl=1)[1]

        source_namespace = source_rig.rpartition(":")[0]
        #target_namespace = target_rig.rpartition(":")[0]

        source_relatives = cmds.listRelatives(source_rig, type="transform", ad=True)
        source_relatives.reverse()
        source_relatives = [source_rig] + source_relatives
        source_controls = []
        for node in source_relatives:
            if node.endswith("_CTRL"):
                source_controls.append(node)
        print source_controls

        ordered_controls = source_controls
        controls_constrained = []

        for control in source_controls:
            parent = cmds.listRelatives(control, type="transform", p=True)

            #Does parent have constraints on it?
            constraint = cmds.listConnections(parent, type="constraint", s=True, d=False)
            if constraint:
                controls_constrained.append(control)
                ordered_controls.remove(control)

                print "-------------------------"
                print control
                print parent
                print constraint

        """for control in ordered_controls:
            print control"""
























































































        #
