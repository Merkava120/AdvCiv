from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import os
gc = CyGlobalContext()
bType = False

class MirrorImage:
	def __init__(self):
		self.lType = [		"Mods/Platy UI/Assets/Modules/UltraPack/UltraPack_CIV4ArtDefines_Interface.xml",
					"Mods/Platy UI/Assets/Modules/UltraPack/UltraPack_CIV4ArtDefines_Movie.xml",
					"Mods/Platy UI/Assets/Modules/UltraPack/UltraPack_CIV4BasicInfos.xml",
					"Mods/Platy UI/Assets/Modules/Platypedia/Platypedia_CIV4ArtDefines_Interface.xml",
				]

		self.lText = [		"Mods/Platy UI/Assets/Modules/UltraPack/Ultrapack_CIV4GameText.xml",
					"Mods/Platy UI/Assets/Modules/UltraPack/WorldBuilder_CIV4GameText.xml",
					"Mods/Platy UI/Assets/Modules/Platypedia/Platypedia_CIV4GameText.xml",
					"Mods/Platy UI/Assets/Modules/Platypedia/AdditionalText_CIV4GameText.xml",
				]

	def interfaceScreen(self):
		screen = CyGInterfaceScreen("MirrorImage", CvScreenEnums.MIRRORIMAGE)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setLabel("MirrorImageHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_MIRROR_IMAGE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText("MirrorImageExit", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 25, screen.getYResolution() - 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		screen.addDropDownBoxGFC("MirrorType", 20, 20, 180, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("MirrorType", CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()).upper(), 0, 0, bType)
		screen.addPullDownString("MirrorType", "TEXT", 0, 0, not bType)

		self.drawTable()

	def drawTable(self):
		screen = CyGInterfaceScreen("MirrorImage", CvScreenEnums.MIRRORIMAGE)
		iWidth = screen.getXResolution() - 40
		iHeight = screen.getYResolution() - 100
		screen.addTableControlGFC("MirrorImage", 2, 20, 60, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("MirrorImage", 0, "", iWidth/2)
		screen.setTableColumnHeader("MirrorImage", 1, "", iWidth/2)

		lCheck = self.lText
		sCheck = "<Tag>"
		if bType:
			lCheck = self.lType
			sCheck = "<Type>"
		lMirror = []
		for sFilePath in lCheck:
			if not os.path.isfile(sFilePath): continue
			MyFile = open(sFilePath)
			for sCurrent in MyFile.readlines():
				if sCheck in sCurrent:
					sType = self.cutString(sCurrent)
					lMirror.append([sType, sFilePath])
			MyFile.close()
		lMirror.sort()

		sOld = ""
		for item in lMirror:
			iRow = screen.appendTableRow("MirrorImage")
			if item[0] == sOld:
				screen.setTableText("MirrorImage", 0, iRow - 1, CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + item[0] + "</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("MirrorImage", 0, iRow, CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + item[0] + "</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				screen.setTableText("MirrorImage", 0, iRow, item[0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				sOld = item[0]
			sLocation = item[1][item[1].find("Assets"):]
			screen.setTableText("MirrorImage", 1, iRow, sLocation, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def cutString(self, string):   
		string = string[string.find(">") + 1:]
		string = string[:string.find("<")]
		return string

	def handleInput (self, inputClass):
		if inputClass.getFunctionName() == "MirrorType":
			global bType
			bType = not bType
			self.drawTable()
		return 0

	def update(self, fDelta):
		return 1