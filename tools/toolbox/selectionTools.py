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
from PySide2 import QtGui
from PySide2 import QtWidgets

# ncTools
from ncTools.mods                   import uiMod;   reload(uiMod)
from ncTools.mods                   import utilMod; reload(utilMod)
from ncTools.mods                   import animMod; reload(animMod)
from ncTools.tools.ncToolboxGlobals import ncToolboxGlobals as G;



class SelectionTools_UI(uiMod.BaseSubUI):

    def create_layout(self):
        # Create instance of tool
        selectionTools = SelectionTools()

        # Create collapsible frame
        self.frame_widget = uiMod.CollapsibleFrame(text = "Selection Tools")

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
        self.select_all = uiMod.push_button(label = "All", size=(self.w[6], self.h[1]))
        self.select_all.clicked.connect(selectionTools.select_all)
        self.main_layout.addWidget(self.select_all, row, 0, 1, 6)

        row += 1
        self.select_side_button = uiMod.push_button(label = "Side", size=(self.w[6], self.h[1]))
        self.select_side_button.clicked.connect(selectionTools.select_side)
        self.main_layout.addWidget(self.select_side_button, row, 0, 1, 6)

        row += 1
        self.select_display_group = uiMod.push_button(label = "Display Group", size=(self.w[6], self.h[1]))
        self.select_display_group.clicked.connect(selectionTools.select_display_group)
        self.main_layout.addWidget(self.select_display_group, row, 0, 1, 6)

        row += 1
        self.select_global_display_ik = uiMod.push_button(label = "Global Display IK", size=(self.w[6], self.h[1]))
        self.select_global_display_ik.clicked.connect(selectionTools.select_global_display_ik)
        self.main_layout.addWidget(self.select_global_display_ik, row, 0, 1, 6)
        return self.frame_widget


class SelectionTools(object):

    def __init__(self):
        G.selectionTools = self

    # Main Tools
    def select_all(self):
        """
        Procedure to get all controls based on current selected node
        """
        self.get_selection_data()
        all_controls = []
        for namespace in self.namespaces:
            controls = self.get_all_controls(self.SD[namespace]["top_node"])
            all_controls = all_controls + controls
        cmds.select(all_controls)


    def select_side(self):
        """
        Procedure to get all controls based on current selected node and side
        """
        self.get_selection_data()
        side_controls = []
        for namespace in self.namespaces:
            controls = self.get_controls_on_side(self.SD[namespace]["selected"], self.SD[namespace]["sides"])
            side_controls = side_controls + controls
        cmds.select(side_controls)


    def select_display_group(self):
        # Define variable to eventually cycle through
        all_display_group = []
        side_display_group = []
        current_selection = cmds.ls(sl=1)

        # Get selection data
        self.get_selection_data()
        for namespace in self.namespaces:
            # Create a list of all display groups in selection
            display_groups = []
            for control in self.SD[namespace]["selected"]:
                display_group = self.get_display_group(control)
                if display_group not in display_groups:
                    display_groups.append(display_group)

                # Create the display group dictionaries inside the namespace dictionary
                if not self.SD[namespace].get(display_group):
                    self.SD[namespace][display_group] = {}
                if not self.SD[namespace][display_group].get("all"):
                    self.SD[namespace][display_group]["all"] = self.get_display_group_controls(display_group)
                if not self.SD[namespace][display_group].get("side"):
                    self.SD[namespace][display_group]["side"] = []


                # Add the controls for the display
                side = self.get_sides([control])
                print control, "_______", display_group
                for control in self.SD[namespace][display_group]["all"]:
                    if len(side) != 0:
                        if side[0] in control:
                            if control not in self.SD[namespace][display_group]["side"]:
                                self.SD[namespace][display_group]["side"].append(control)

                    else:
                        self.SD[namespace][display_group]["side"] = self.SD[namespace][display_group]["all"]

            for display_group in display_groups:
                all_display_group = all_display_group + self.SD[namespace][display_group]["all"]
                side_display_group = side_display_group + self.SD[namespace][display_group]["side"]

        self.cycle_selection("display_group_index", [side_display_group, all_display_group])


    def select_global_display_ik(self):
        # Define variables to eventually cycle through
        global_controls = []
        display_controls = []
        ikfk_controls = []

        # Get selection data
        self.get_selection_data()
        for namespace in self.namespaces:
            global_control = self.get_control(namespace, "global")
            if cmds.objExists(global_control):
                global_controls.append(global_control)
            display_control = self.get_control(namespace, "globalDisplayToggle")
            if cmds.objExists(display_control):
                display_controls.append(display_control)
            ikfk_control = self.get_control(namespace, "globalIkFkToggle")
            if cmds.objExists(ikfk_control):
                ikfk_controls.append(ikfk_control)
        cycle_list = [global_controls, display_controls, ikfk_controls]

        # Cycle through the lists
        self.cycle_selection("global_display_ik_index", cycle_list)


    def cycle_selection(self, index_attr, cycle_list):
        current_index = getattr(G, index_attr, 0)
        print "current inxed", current_index
        if current_index == None:
            current_index = 0
        max_index = len(cycle_list)-1

        current_selection = cmds.ls(sl=1)
        current_cycle = cycle_list[current_index]

        difference = []
        for i in current_cycle + current_selection:
            if i not in current_cycle or i not in current_selection:
                difference.append(i)

        if len(difference) == 0 and current_index < max_index:
            current_index = current_index + 1
        else:
            current_index = 0

        print "new index", current_index
        setattr(G, index_attr, current_index)

        cmds.select(cycle_list[current_index])


    def get_selection_data(self):
        """
        Procedure used to get the selection, first node, namespace, sides,
        all controls. Useful start info for other functions.
        """
        self.SD = {}
        self.global_selection = cmds.ls(sl=1)

        # Get each selected namespace and create a dictionary for each
        self.namespaces = []
        for node in self.global_selection:
            namespace = self.get_namespace(node)
            if namespace not in self.namespaces:
                self.namespaces.append(namespace)

        for namespace in self.namespaces:
            self.SD[namespace] = {}
            # For each namespace get the selected controls
            self.SD[namespace]["selected"] = []
            for control in self.global_selection:
                if control.startswith(namespace+":"):
                    self.SD[namespace]["selected"].append(control)

            # For each namespace get the selected sides
            self.SD[namespace]["sides"] = self.get_sides(self.SD[namespace]["selected"])

            # For each namespace get the top node
            self.SD[namespace]["top_node"] = self.get_top_node(self.SD[namespace]["selected"][0])

            # For each namespace get all the controls for that rig
            self.SD[namespace]["all"] = self.get_all_controls(self.SD[namespace]["top_node"])

    def select_fk_chain(self):
        """
        Procedure to select all the controls in an fk chain e.g fingers
        """

        self.get_selection_data()
        fk_controls = []

        root_names = []
        for namespace in self.namespaces:
            for control in self.SD[namespace]["selected"]:
                if "FK" in control:
                    root_name = control.rpartition("FK")[0]
                    if root_name not in root_names:
                        root_names.append(root_name)

        for root_name in root_names:
            root_control = "{root_name}FKA_CTRL".format(root_name=root_name)
            fk_controls.append(root_control)

            children = cmds.listRelatives(root_control, ad=True, type="transform")
            for child in children:
                if child.endswith("_CTRL"):
                    fk_controls.append(child)

        fk_controls.sort()
        cmds.select(fk_controls)

    def toggle_rig(self):
        """
        Procedure to toggle the visibility of the selected rig
        """
        self.get_selection_data()
        for namespace in self.namespaces:
            top_node = self.SD[namespace]["top_node"]
            print top_node, "TOP"
            if cmds.getAttr(top_node + ".visibility") == 0:
                cmds.setAttr(top_node + ".visibility", 1)
            else:
                cmds.setAttr(top_node + ".visibility", 0)



    # Other functions
    def get_namespace(self, node):
        """
        Procedure to get the namespace of the node
        """
        return node.rpartition(":")[0]


    def get_top_node(self, node):
        """
        Procedure to get the top node of the selected node
        """
        current_node = [node]
        parent = cmds.listRelatives(current_node, p=True, type="transform")
        while parent is not None:
            current_node = parent
            parent = cmds.listRelatives(current_node, p=True, type="transform")
        top_node = current_node[0]
        print top_node
        return top_node


    def select_control(self, namespace, name):
        """
        Procedure to select the control based on given namespace and name
        """
        control = get_control(namespace, name)
        cmds.select(control)


    def get_control(self, namespace, name):
        """
        Procedure to get control based on given namespace and name
        """
        control = "{namespace}:{name}_CTRL".format(namespace = namespace,
                                                   name = name)
        return control


    def get_sides(self, selection):
        """
        Procedure to determine if left, right or both side controls are selected
        """
        sides = []
        for control in selection:
            if ":l_" in control:
                sides.append(":l_")
            if ":r_" in control:
                sides.append(":r_")
        sides = list(set(sides))
        return sides


    def get_controls_on_side(self, selection, sides):
        """
        Procedure to get all controls on a certain side of the rig based on
        whether left or right is selected
        """
        all_controls = self.get_all_controls(selection[0])
        controls = []
        for control in all_controls:
            for side in sides:
                if side in control:
                    controls.append(control)
        return controls


    def get_all_controls(self, node):
        """
        Procedure to get all controls in a given rig
        """
        top_node = self.get_top_node(node)
        all_controls = []
        relatives = cmds.listRelatives(top_node, ad=True, type="transform")
        for control in relatives:
            if control.endswith("_CTRL"):
                all_controls.append(control)
        return all_controls


    def get_display_group(self, node):
        anim_switch_attr = "animSwitchOptions"
        anim_switch_option = None

        display_group = None
        current_node = node
        # Get the group node that is the overall parent of the display group
        while anim_switch_option == None:
            # Query if the current node has the anim_switch_attr
            if cmds.attributeQuery(anim_switch_attr, node=current_node, exists=True):
                anim_switch_option = cmds.getAttr(current_node+"."+anim_switch_attr)
                display_group = current_node
            else:
                anim_switch_option = None
                parent = cmds.listRelatives(current_node, parent=True, type="transform")[0]
                current_node = parent
        return display_group


    def get_display_group_controls(self, display_group):
        display_group_controls = []
        # Get all children of the display group
        relatives = cmds.listRelatives(display_group, ad=True, type="transform")
        for control in relatives:
            if control.endswith("_CTRL"):
                display_group_controls.append(control)
        return display_group_controls
