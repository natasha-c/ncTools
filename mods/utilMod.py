# -----------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------

# maya
import maya.cmds as cmds

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def look_thru_render_cam(render_cam_id):
    render_camera = None
    allCameras = cmds.listCameras(p = True)
    for camera in allCameras:
        if render_cam_id in camera:
            render_camera = camera
    if render_camera == None:
        cmds.confirmDialog(title="Camera Error",
                           message="Please import "+render_cam_id,
                           button=["Ok"],
                           defaultButton="Ok")
        render_camera = cmds.lookThru(query=True)
    cmds.lookThru(render_camera)



def get_namespace(selected):
    return selected.rpartition(":")[0]
