import maya.cmds as cmds

scene_path = 'C:/Users/Yian Shi/Documents/GitHub/Maya_Projections2Textures/Sample Project/Baseman_Layered.ma'
def openScene():
    cmds.file(new=True, force=True, ignoreVersion=True)
    cmds.file(scene_path, open=True)
openScene()