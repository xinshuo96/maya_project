import maya.cmds as cmds
import maya.app.general.createImageFormats as createImageFormats
import maya.mel as mel

def take_screenshot(cam_name):
	cmds.select(allDagObjects=True)

	#place the camera to front view and fit the entire obj inside the camera view
	cmds.viewSet(f=True, fit= True)

	#take screenshot from the selected view-point, here front
	formatManager = createImageFormats.ImageFormats()

	cmds.setAttr('hardwareRenderingGlobals.renderMode', 4)
	cmds.setAttr('hardwareRenderingGlobals.lightingMode', 0)

	mel.eval('RenderViewWindow')

	tmp_image_path = cmds.ogsRender(cam=cam_name)
	print(tmp_image_path)
	formatManager.pushRenderGlobalsForDesc('PNG')
	cmds.refresh(cv=True, fe = "jpg", fn = "imageSnapshot")
	# editor = 'renderView'
	
	# mel.eval('renderWindowRender redoPreviousRender renderView')
	# editor = 'renderView'
	# formatManager = createImageFormats.ImageFormats()

	# formatManager.pushRenderGlobalsForDesc("PNG")
	# cmds.renderWindowEditor(editor, e=True, writeImage='~/desktop/testImage.png')
	# formatManager.popRenderGlobals()

take_screenshot("front")
