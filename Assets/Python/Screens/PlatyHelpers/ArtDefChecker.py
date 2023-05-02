from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import os

gc = CyGlobalContext()
bUnused = False
lModArtDefines = {}
lBTSArtDefines = {}
lItemTypes = {}
lFiles = [[],[]]

	###########
	## Add Mod Files here
	## Adding "Mods/Charlemagne/Assets/XML/Art/"
	## will automatically check for 
	## "Mods/Charlemagne/Assets/XML/Art/CIV4ArtDefines_Bonus.xml"
	## "Mods/Charlemagne/Assets/XML/Art/CIV4ArtDefines_Building.xml"
	## "Mods/Charlemagne/Assets/XML/Art/CIV4ArtDefines_Civilization.xml"
	## etc, so there is no need to include every single filepath, just the folder will do
	## In the case of modules:
	## "Mods/Platy UI/Assets/Modules/Gigapack/Gigapack_"
	## If the full file path is supposed to be "Mods/Platy UI/Assets/Modules/Gigapack/Gigapack_CIV4ArtDefines_Bonus.xml"
	## The items added below are samples. You can remove them if you like, though they won't cause any errors if the files do not exist.
	###########

class ArtDefChecker:
	def __init__(self):
		self.lModArt = 	["Mods/Platy UI/Assets/Modules/Gigapack/Gigapack_",
				#"Mods/Charlemagne/Assets/XML/Art/",
				]

		self.lModItems = ["Mods/Platy UI/Assets/Modules/Gigapack/Gigapack_",
				#"Mods/Charlemagne/Assets/XML/Terrain/",
				#"Mods/Charlemagne/Assets/XML/Buildings/",
				#"Mods/Charlemagne/Assets/XML/Civilizations/",
				#"Mods/Charlemagne/Assets/XML/Units/",
				]

############################################ Do not Edit anything below this line ################################################

		self.DictType = {	"CIV4ArtDefines_Bonus.xml":		True,
					"CIV4ArtDefines_Building.xml":		True,
					"CIV4ArtDefines_Civilization.xml":	True,
					"CIV4ArtDefines_Feature.xml":		True,
					"CIV4ArtDefines_Improvement.xml":	True,
					"CIV4ArtDefines_Leaderhead.xml":	True,
					"CIV4ArtDefines_Terrain.xml":		True,
					"CIV4ArtDefines_Unit.xml":		True,
					"CIV4ArtDefines_Movie.xml":		True,
					}

		self.DictArtDefine = {	"CIV4BonusInfos.xml":			[["ArtDefineTag>"], True],
					"CIV4BuildingInfos.xml":		[["ArtDefineTag>", "<MovieDefineTag>"], True],
					"CIV4CivilizationInfos.xml":		[["ArtDefineTag>"], True],
					"CIV4FeatureInfos.xml":			[["ArtDefineTag>"], True],
					"CIV4ImprovementInfos.xml":		[["ArtDefineTag>"], True],
					"CIV4LeaderHeadInfos.xml":		[["ArtDefineTag>"], True],
					"CIV4TerrainInfos.xml":			[["ArtDefineTag>"], True],
					"CIV4UnitInfos.xml":			[["ArtDefineTag>"], True],
					"CIV4UnitArtStyleTypeInfos.xml":	[["ArtDefineTag>"], True],
					"CIV4ProjectInfo.xml":			[["<MovieDefineTag>"], True],
					"CIV4VictoryInfo.xml":			[["<VictoryMovie>"], True],
					"CIV4CorporationInfo.xml":		[["<MovieFile>"], True],
					"CIV4ReligionInfo.xml":			[["<MovieFile>"], True],
				}

		self.lBTSArt = ["Assets/XML/Art/"]

		self.lBTSItems = ["Assets/XML/Terrain/",
				"Assets/XML/Buildings/",
				"Assets/XML/Civilizations/",
				"Assets/XML/Buildings/",
				"Assets/XML/Units/",
				]
				

	def interfaceScreen(self):
		screen = CyGInterfaceScreen("ArtDefChecker", CvScreenEnums.ARTDEFCHECKER)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setLabel("ArtDefCheckerHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_ART_DEFINE_CHECKER", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText("ArtDefCheckerExit", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 25, screen.getYResolution() - 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		screen.addDropDownBoxGFC("CheckType", 20, 20, 180, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CheckType", CyTranslator().getText("TXT_KEY_UNUSED", ()), 0, 0, bUnused)
		screen.addPullDownString("CheckType", CyTranslator().getText("TXT_KEY_MISSING", ()), 0, 0, not bUnused)

		global lModArtDefines
		global lBTSArtDefines
		global lItemTypes
		global lFiles

		lFiles = [[],[]]

		lModArtDefines = {}
		for sFilePath in self.lModArt:
			for key in self.DictType.keys():
				self.updateDict(lModArtDefines, sFilePath, key, "<Type>")

		lBTSArtDefines = {}
		for sFilePath in self.lBTSArt:
			for key in self.DictType.keys():
				if self.DictType[key]:
					self.updateDict(lBTSArtDefines, sFilePath, key, "<Type>")

		lItemTypes = {}
		for sFilePath in self.lModItems:
			for key in self.DictArtDefine.keys():
				for sTag in self.DictArtDefine[key][0]:
					self.updateDict(lItemTypes, sFilePath, key, sTag)

		for sFilePath in self.lBTSItems:
			for key in self.DictArtDefine.keys():
				if self.DictArtDefine[key][1]:
					for sTag in self.DictArtDefine[key][0]:
						self.updateDict(lItemTypes, sFilePath, key, sTag)
		self.drawTable()

	def updateDict(self, Dict, sFilePath, sExt, sCheck):
		sFilePath += sExt
		if os.path.isfile(sFilePath):
			if sFilePath.find("Modules") == -1:
				if sExt in self.DictType:
					self.DictType[sExt] = False
				elif sExt in self.DictArtDefine:
					self.DictArtDefine[sExt][-1] = False
			if sExt in self.DictType:
				if not sFilePath in lFiles[0]:
					lFiles[0].append(sFilePath)
			else:
				if not sFilePath in lFiles[1]:
					lFiles[1].append(sFilePath)
		else:
			return
		MyFile = open(sFilePath)
		for sCurrent in MyFile.readlines():
			if sCheck in sCurrent:
				sType = self.cutString(sCurrent)
				Dict[sType] = sFilePath
		MyFile.close()

	def drawTable(self):
		screen = CyGInterfaceScreen("ArtDefChecker", CvScreenEnums.ARTDEFCHECKER)
		iWidth = screen.getXResolution() - 40
		iHeight = screen.getYResolution() - 100
		iTableY1 = 60
		iTableH1 = iHeight * 2/3
		screen.addTableControlGFC("ArtDefChecker", 2, 20, iTableY1, iWidth, iTableH1, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("ArtDefChecker", 0, "", iWidth/2)
		screen.setTableColumnHeader("ArtDefChecker", 1, "", iWidth/2)
		
		lProblems = []
	## Unused Art Info
		if bUnused:
			for item in lModArtDefines.items():
				if item[0] not in lItemTypes:
					lProblems.append(item)
	## Missing Art Info
		else:
			for item in lItemTypes.items():
				if item[0] not in lModArtDefines and item[0] not in lBTSArtDefines:
					if item[0] == "NONE": continue
					lProblems.append(item)
		lProblems.sort()

		for item in lProblems:
			iRow = screen.appendTableRow("ArtDefChecker")
			screen.setTableText("ArtDefChecker", 0, iRow, item[0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("ArtDefChecker", 1, iRow, item[1], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iTableY2 = iTableY1 + iTableH1 + 20
		iTableH2 = iHeight - iTableH1 - 20
		screen.addTableControlGFC("FilesChecked", 2, 20, iTableY2, iWidth, iTableH2, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("FilesChecked", 0, "", iWidth/2)
		screen.setTableColumnHeader("FilesChecked", 1, "", iWidth/2)

		iMaxRow = -1
		for i in xrange(len(lFiles[0])):
			if i > iMaxRow:
				screen.appendTableRow("FilesChecked")
				iMaxRow = i
			screen.setTableText("FilesChecked", 0, i, lFiles[0][i], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		for i in xrange(len(lFiles[1])):
			if i > iMaxRow:
				screen.appendTableRow("FilesChecked")
				iMaxRow = i
			screen.setTableText("FilesChecked", 1, i, lFiles[1][i], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def cutString(self, string):   
		string = string[string.find(">") + 1:]
		string = string[:string.find("<")]
		return string

	def handleInput (self, inputClass):
		if inputClass.getFunctionName() == "CheckType":
			global bUnused
			bUnused = not bUnused
			self.drawTable()
		return 0

	def update(self, fDelta):
		return 1