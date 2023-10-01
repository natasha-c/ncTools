import maya.cmds as cmds
import maya.mel as mel

# ncTools
from ncTools.mods                   import utilMod;   reload(utilMod)
from ncTools.mods                    import constMod;    reload(constMod)

MENU_NAME = "markingMenu"

class MarkingMenu():

    def __init__(self):
        self.remove_old()
        self.build()


    def remove_old(self):
        """
        Checks if there is a marking menu, if so deletes it.
        """
        if cmds.popupMenu(MENU_NAME, exists=True):
            cmds.deleteUI(MENU_NAME)


    def build(self):
        """
        Creates the marking menu
        """
        menu = cmds.popupMenu(MENU_NAME,
                             markingMenu=True,
                             button=1,
                             allowOptionBoxes=True,
                             ctl=True,
                             alt=True,
                             sh=False,
                             parent="viewPanes",
                             postMenuCommandOnce=True,
                             postMenuCommand=self.build_marking_menu)


    def build_marking_menu(self, menu, parent):
        """
        Populates the marking menu with all the elements
        """
        # Radial positioned
        cmds.menuItem(p=menu, l="Perspective", rp="N", c="mel.eval('switchModelView persp')")
        cmds.menuItem(p=menu, l=constMod.CAMS["firstPerson"][0], rp="NE", c=lambda x:utilMod.look_thru_render_cam(constMod.CAMS["firstPerson"][1]))
        cmds.menuItem(p=menu, l="Asset Manager", rp="S", c=self.dsdb_AssetManager)

        # Sub menu option
        """render_cam_id
        sub_menu=cmds.menuItem(p=menu, l="Example", rp="E", subMenu=1)
        cmds.menuItem(p=sub_menu, l="Sub1")
        cmds.menuItem(p=sub_menu, l="Sub2")
        """

        # List
        """
        cmds.menuItem(p=menu, l="First")
        cmds.menuItem(p=menu, l="Second")
        """

        # Menu Items
        cmds.menuItem(p=menu, l="Hotkey Editor", c="mel.eval('HotkeyPreferencesWindow')")



    def dsdb_AssetManager(self, *args, **kwargs):
        import dsdb_pyside
        UI = dsdb_pyside.dsdb_assetManager.dsdb_assetManagerUI.instance("Asset Manager", run = False)

