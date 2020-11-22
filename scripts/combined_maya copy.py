import maya.app.general.createImageFormats as createImageFormats
import maya.cmds as cmds
import maya.mel as mel
import os


scene_path = '/Users/sh/Project/maya_project/Sample Project/Baseman_Layered.ma'
def openScene():
    cmds.file(new=True, force=True, ignoreVersion=True)
    cmds.file(scene_path, open=True)
openScene()

shader_name = 'projection_shader'
projection_name = "projection_node"
place3dTexture_name = 'place3dTexture_node'
color_file_name = 'color_file'
place2dTexture_name = 'place2dTexture_node'

def createNode():
    cmds.shadingNode('lambert', asShader=True, name=shader_name)
    cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name+'SG')
    cmds.connectAttr(shader_name+'.outColor', shader_name+'SG'+'.surfaceShader', force=True)
    cmds.select(allDagObjects=True)
    cmds.hyperShade(assign=shader_name)

    cmds.defaultNavigation(createNew=True, destination=shader_name+'.color')
    cmds.defaultNavigation(defaultTraversal=True, destination=shader_name+'.color')
    cmds.shadingNode('projection', asUtility=True, name=projection_name)
    cmds.defaultNavigation(force=True, connectToExisting=True, source=projection_name, destination=shader_name+'.color')
    cmds.connectAttr(projection_name+'.outColor', shader_name+'.color', force=True)

    # fit to bounding box
    cmds.shadingNode('place3dTexture', asUtility=True, name=place3dTexture_name)
    cmds.defaultNavigation(force=True, connectToExisting=True, source=place3dTexture_name+'.worldInverseMatrix', destination=projection_name+'.placementMatrix')
    cmds.setAttr(projection_name+'.vAngle', 90)
    cmds.setAttr(projection_name+'.uAngle', 180)
    cmds.setAttr(place3dTexture_name+'.scale', 11.95274, 15.46285, 2.891423, type='double3')
    cmds.setAttr(place3dTexture_name+'.translate', 0, 14.911491, 0, type='double3')

def addImageAsColor(front_color_path):
    cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=color_file_name)
    cmds.shadingNode('place2dTexture', asUtility=True, name=place2dTexture_name)
    cmds.connectAttr(place2dTexture_name+'.coverage', color_file_name+'.coverage', force=True)
    cmds.connectAttr(place2dTexture_name+'.translateFrame', color_file_name+'.translateFrame', force=True)
    cmds.connectAttr(place2dTexture_name+'.rotateFrame', color_file_name+'.rotateFrame', force=True)
    cmds.connectAttr(place2dTexture_name+'.mirrorU', color_file_name+'.mirrorU', force=True)
    cmds.connectAttr(place2dTexture_name+'.mirrorV', color_file_name+'.mirrorV', force=True)
    cmds.connectAttr(place2dTexture_name+'.stagger', color_file_name+'.stagger', force=True)
    cmds.connectAttr(place2dTexture_name+'.wrapU', color_file_name+'.wrapU', force=True)
    cmds.connectAttr(place2dTexture_name+'.wrapV', color_file_name+'.wrapV', force=True)
    cmds.connectAttr(place2dTexture_name+'.repeatUV', color_file_name+'.repeatUV', force=True)
    cmds.connectAttr(place2dTexture_name+'.offset', color_file_name+'.offset', force=True)
    cmds.connectAttr(place2dTexture_name+'.rotateUV', color_file_name+'.rotateUV', force=True)
    cmds.connectAttr(place2dTexture_name+'.noiseUV', color_file_name+'.noiseUV', force=True)
    cmds.connectAttr(place2dTexture_name+'.vertexUvOne', color_file_name+'.vertexUvOne', force=True)
    cmds.connectAttr(place2dTexture_name+'.vertexUvTwo', color_file_name+'.vertexUvTwo', force=True)
    cmds.connectAttr(place2dTexture_name+'.vertexUvThree', color_file_name+'.vertexUvThree', force=True)
    cmds.connectAttr(place2dTexture_name+'.vertexCameraOne', color_file_name+'.vertexCameraOne', force=True)
    cmds.connectAttr(place2dTexture_name+'.outUV', color_file_name+'.uv', force=True)
    cmds.connectAttr(place2dTexture_name+'.outUvFilterSize', color_file_name+'.uvFilterSize', force=True)

    cmds.defaultNavigation(force=True, connectToExisting=True, source=color_file_name, destination=projection_name+'.image')
    cmds.connectAttr(color_file_name+'.outColor', projection_name+'.image', force=True)

    cmds.setAttr(color_file_name+'.fileTextureName', front_color_path, type="string")


def take_screenshot(cam_name, file_path="~/Desktop/front.png"):
	cmds.select(allDagObjects=True)
	cmds.setAttr("defaultRenderGlobals.imageFormat", 32)
	#place the camera to front view and fit the entire obj inside the camera view
	cmds.viewSet(f=True, fit= True)

	#take screenshot from the selected view-point, here front
	formatManager = createImageFormats.ImageFormats()

	cmds.setAttr('hardwareRenderingGlobals.renderMode', 4)
	cmds.setAttr('hardwareRenderingGlobals.lightingMode', 0)

	mel.eval('RenderViewWindow')

	tmp_image_path = cmds.ogsRender(cam=cam_name)
	print(tmp_image_path)
	if os.name == 'nt':
		os.system("copy " + tmp_image_path + " " + file_path);
	else:
		os.system("cp " + tmp_image_path + " " + file_path);

	formatManager.pushRenderGlobalsForDesc('png')
	# cmds.refresh(cv=True, fe = "jpg", fn = "imageSnapshot")

	return tmp_image_path

createNode()
addImageAsColor('/Users/sh/Project/maya_project/Sample Project/Front_Color.psd')
front_img_path = take_screenshot("front", "~/Desktop/front.png")

addImageAsColor('/Users/sh/Project/maya_project/Sample Project/Back_Color.psd')
back_img_path = take_screenshot("front", "~/Desktop/back.png")


