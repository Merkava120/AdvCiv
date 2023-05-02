from CvPythonExtensions import *
import string
import CvUtil
import ScreenInput
import CvScreenEnums
import CvPediaScreen
import PlatyPediaTech
import PlatyPediaUnit
import PlatyPediaBuilding
import PlatyPediaPromotion
import PlatyPediaUnitChart
import PlatyPediaBonus
import PlatyPediaTerrain
import PlatyPediaFeature
import PlatyPediaImprovement
import PlatyPediaCivic
import PlatyPediaCivilization
import PlatyPediaLeader
import PlatyPediaSpecialist
import PlatyPediaHistory
import PlatyPediaProject
import PlatyPediaReligion
import PlatyPediaCorporation
import PlatyUpgradesGraph
import PlatyPediaTrait
import PlatyPediaRoute
import PlatyPediaProcess
import PlatyPediaGameInfo
import PlatyPediaMovie
import PlatyPediaTechTree
import PlatyPediaBuildingChart
import PlatyPediaCredits
import PlatyPediaIntro

gc = CyGlobalContext()

class CvPediaMain( CvPediaScreen.CvPediaScreen ):
	def __init__(self):
		self.PLATYPEDIA_INTRO		= 0
		self.PLATYPEDIA_TECH		= self.PLATYPEDIA_INTRO + 1
		self.PLATYPEDIA_UNIT		= self.PLATYPEDIA_TECH + 1
		self.PLATYPEDIA_UNIT_GROUP	= self.PLATYPEDIA_UNIT + 1
		self.PLATYPEDIA_PROMOTION	= self.PLATYPEDIA_UNIT_GROUP + 1
		self.PLATYPEDIA_BUILDING	= self.PLATYPEDIA_PROMOTION + 1
		self.PLATYPEDIA_WONDER		= self.PLATYPEDIA_BUILDING + 1
		self.PLATYPEDIA_B_CHART		= self.PLATYPEDIA_WONDER + 1
		self.PLATYPEDIA_PROJECT		= self.PLATYPEDIA_B_CHART + 1
		self.PLATYPEDIA_PROCESS		= self.PLATYPEDIA_PROJECT + 1
		self.PLATYPEDIA_TERRAIN		= self.PLATYPEDIA_PROCESS + 1
		self.PLATYPEDIA_FEATURE		= self.PLATYPEDIA_TERRAIN + 1
		self.PLATYPEDIA_BONUS		= self.PLATYPEDIA_FEATURE + 1
		self.PLATYPEDIA_IMPROVEMENT	= self.PLATYPEDIA_BONUS + 1
		self.PLATYPEDIA_ROUTE		= self.PLATYPEDIA_IMPROVEMENT + 1
		self.PLATYPEDIA_TREE		= self.PLATYPEDIA_ROUTE + 1
		self.PLATYPEDIA_CIV		= self.PLATYPEDIA_TREE + 1
		self.PLATYPEDIA_LEADER		= self.PLATYPEDIA_CIV + 1
		self.PLATYPEDIA_TRAIT		= self.PLATYPEDIA_LEADER + 1
		self.PLATYPEDIA_SPECIALIST	= self.PLATYPEDIA_TRAIT + 1
		self.PLATYPEDIA_RELIGION	= self.PLATYPEDIA_SPECIALIST + 1
		self.PLATYPEDIA_CORPORATION	= self.PLATYPEDIA_RELIGION + 1
		self.PLATYPEDIA_CIVIC		= self.PLATYPEDIA_CORPORATION + 1
		self.PLATYPEDIA_GAME_INFO	= self.PLATYPEDIA_CIVIC + 1
		self.PLATYPEDIA_CONCEPT		= self.PLATYPEDIA_GAME_INFO + 1
		self.PLATYPEDIA_GAMEOPTION	= self.PLATYPEDIA_CONCEPT + 1
		self.PLATYPEDIA_HINTS		= self.PLATYPEDIA_GAMEOPTION + 1
		self.PLATYPEDIA_INDEX		= self.PLATYPEDIA_HINTS + 1
		self.PLATYPEDIA_MOVIE		= self.PLATYPEDIA_INDEX + 1
		self.PLATYPEDIA_CREDIT		= self.PLATYPEDIA_MOVIE + 1

		self.lAdvisors = 		["TXT_KEY_ADVISOR_MILITARY", "TXT_KEY_ADVISOR_RELIGION", "TXT_KEY_ADVISOR_ECONOMY",
						"TXT_KEY_ADVISOR_SCIENCE", "TXT_KEY_ADVISOR_CULTURE", "TXT_KEY_ADVISOR_GROWTH"]

		self.Y_TITLE = 8
		self.X_BACK = 50
		self.X_FORWARD = 200
		self.pediaLeader = PlatyPediaLeader.CvPediaLeader(self)
		self.pediaHistorical = PlatyPediaHistory.CvPediaHistory(self)
		self.nWidgetCount = 0

		self.pediaHistory = []
		self.pediaFuture = []
		self.listCategories = []
		self.iLastScreen = -1

		self.iCategory = -1
		self.iActivePlayer = -1
		self.iCount = 0
		self.iExtraRow = 0
		self.iExtraSpace = 0
		self.iNumColumns = 1
		self.iNumRows = 1
		self.sTableName = ""

		self.mapCategories = {
			self.PLATYPEDIA_INTRO		: self.placeIntro,
			self.PLATYPEDIA_TECH		: self.placeTechs,
			self.PLATYPEDIA_UNIT		: self.placeUnits,
			self.PLATYPEDIA_BUILDING	: self.placeBuildings,
			self.PLATYPEDIA_WONDER		: self.placeWonders,
			self.PLATYPEDIA_TERRAIN		: self.placeTerrains,
			self.PLATYPEDIA_FEATURE		: self.placeFeatures,
			self.PLATYPEDIA_BONUS		: self.placeBoni,
			self.PLATYPEDIA_IMPROVEMENT	: self.placeImprovements,
			self.PLATYPEDIA_SPECIALIST	: self.placeSpecialists,
			self.PLATYPEDIA_PROMOTION	: self.placePromotions,
			self.PLATYPEDIA_UNIT_GROUP	: self.placeUnitGroups,
			self.PLATYPEDIA_CIV		: self.placeCivs,
			self.PLATYPEDIA_LEADER		: self.placeLeaders,
			self.PLATYPEDIA_RELIGION	: self.placeReligions,
			self.PLATYPEDIA_CORPORATION	: self.placeCorporations,
			self.PLATYPEDIA_CIVIC		: self.placeCivics,
			self.PLATYPEDIA_PROJECT		: self.placeProjects,
			self.PLATYPEDIA_CONCEPT		: self.placeConcepts,
			self.PLATYPEDIA_HINTS		: self.placeHints,
			self.PLATYPEDIA_TRAIT		: self.placeTraits,
			self.PLATYPEDIA_ROUTE		: self.placeRoutes,
			self.PLATYPEDIA_PROCESS		: self.placeProcesses,
			self.PLATYPEDIA_GAME_INFO	: self.placeGameInfos,
			self.PLATYPEDIA_MOVIE		: self.placeMovies,
			self.PLATYPEDIA_INDEX		: self.placeIndex,
			self.PLATYPEDIA_GAMEOPTION	: self.placeGameOptions,
			self.PLATYPEDIA_B_CHART		: self.placeBuildingChart,
			self.PLATYPEDIA_TREE		: self.placeUpgradeTree,
			self.PLATYPEDIA_CREDIT		: self.placeCredits,
			}
########################################### Customization Start ################################
		self.bLeft = False
## Sort Type ##
		self.iSortTechs = 2		#	[Alphabetic Order, Cost, Era, Advisor, Abilities]
		self.iSortUnits = 3		#	[Alphabetic Order, Cost, Combat Class, Era, Domain, Limit Class, Advisor, Special Class]
		self.iSortPromotions = 0	#	[Alphabetic Order, Combat Class, Era]
		self.iSortBuildings = 2		#	[Alphabetic Order, Cost, Era, Advisor]
		self.iSortWonders = 2		#	[Alphabetic Order, Cost, Limit Class, Era, Great People, Advisor]
		self.iSortProjects = 2		#	[Alphabetic Order, Cost, Limit Class, Era]
		self.iSortTerrains = 1		#	[Alphabetic Order, Domain]
		self.iSortBonus = 1		#	[Alphabetic Order, Type, Era, Domain, Corporation]
		self.iSortImprovements = 2	#	[Alphabetic Order, Era, Domain]
		self.iSortRoutes = 1		#	[Alphabetic Order, Value, Era]
		self.iSortCivics = 1		#	[Alphabetic Order, Type, Era, Upkeep]
		self.iSortCivilizations = 1	#	[Alphabetic Order, Type, Tech]
		self.iSortLeaders = 1		#	[Alphabetic Order, Civilization, Trait, Religion]
		self.iSortSpecialists = 1	#	[Alphabetic Order, Type]
		self.iSortReligions = 1		#	[Alphabetic Order, Era]
		self.iSortCorporations = 1	#	[Alphabetic Order, Era, Great People, Resources]
		self.iSortProcesses = 2		#	[Alphabetic Order, Era, Commerce]
		self.iSortIndex = -1		#	-1: All
		self.iSortPTree = -1		#	-1: All
		self.iSortUTree = -1		#	-1: All
		self.iSortBChart = -1		#	-1: All	[National, Team, World]
		self.iSortBChartType = 0
		self.iSortTree = 0
## Colors ##
		self.color = "<color=80,200,250,0>"	## Section Header
		self.color2 = "<color=200,255,200,0>"	## Category Names
		self.color3 = "<color=100,220,100,0>"	## Individual Items
		self.color4 = "<color=255,220,30,0>"	## Title
## Icons ##
		self.sIntroIcon = "[ICON_ESPIONAGE] "
		self.sTechIcon = "[ICON_RESEARCH] "
		self.sUnitIcon = "[ICON_STRENGTH] "
		self.sBuildingIcon = "[ICON_PRODUCTION] "
		self.sWonderIcon = "[ICON_CULTURE] "
		self.sBonusIcon = "[ICON_HAPPY] "
		self.sTerrainIcon = "[ICON_FOOD] "
		self.sFeatureIcon = "[ICON_DEFENSE] "
		self.sImprovementIcon = "[ICON_COMMERCE] "
		self.sSpecialistIcon = "[ICON_GREATPEOPLE] "
		self.sPromotionIcon = "[ICON_STAR] "
		self.sUnitCombatIcon = "[ICON_SILVER_STAR] "
		self.sCivIcon = "[ICON_MAP] "
		self.sLeaderIcon = "[ICON_ANGRYPOP] "
		self.sReligionIcon = "[ICON_RELIGION] "
		self.sCorporationIcon = "[ICON_GOLD] "
		self.sCivicIcon = "[ICON_BAD_GOLD] "
		self.sProjectIcon = "[ICON_POWER] "
		self.sHelpIcon = "[ICON_DEFENSIVEPACT] "
		self.sTraitIcon = "[ICON_OCCUPATION] "
		self.sRouteIcon = "[ICON_MOVES] "
		self.sProcessIcon = "[ICON_TRADE] "
		self.sGameInfoIcon = "[ICON_GOLDENAGE] "
		self.sMovieIcon = "[ICON_CULTURE] "
		self.sUpgradeIcon = "[ICON_HEALTHY] "

########################################### Customization End #################################################

	def getScreen(self):
		return CyGInterfaceScreen("PediaMainScreen", CvScreenEnums.PEDIA_MAIN)

	def placePediaLinks(self, listSorted, SectionIcon, iSelected, Widget, iPython, iType = -1, ItemIcon = ""):
		screen = self.getScreen()
		if iType == -1:
			iType = iPython
		if not ItemIcon:
			ItemIcon = SectionIcon
		for iList in xrange(len(listSorted)):
			lTemp = listSorted[iList]
			if lTemp[0]:
				iRow = screen.appendTableRow("PlatyTable")
				sList = lTemp[0]
				sButton = ""
				if lTemp[1]:
					sButton = lTemp[1]
				else:
					sList = SectionIcon + sList
				sText = "<font=3>" + self.color + sList + "</font></color>"
				screen.setTableText("PlatyTable", 0, iRow, sText, sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			for item in lTemp[2]:
				iRow = screen.appendTableRow("PlatyTable")
				if item[1] == iSelected and iType == iPython:
					screen.selectRow("PlatyTable", iRow, True)
				sText = item[0]
				if not item[2]:
					sText = ItemIcon + sText
				if iPython > -1:
					iData1 = iPython
					iData2 = item[1]
				else:
					iData1 = item[1]
					iData2 = 1
				screen.setTableText("PlatyTable", 0, iRow, "<font=3>" + self.color3 + sText + "</color></font>", item[2], Widget, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
			if lTemp[0]:
				iCount = iList
				while iCount < len(listSorted) - 1:
					if len(listSorted[iCount + 1]) > 0:
						iRow = screen.appendTableRow("PlatyTable")
						screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						break
					iCount += 1

	def setPediaCommonWidgets(self):
		self.iLastScreen = -1
		self.EXIT_TEXT = u"<font=4>" + self.color4 + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</color></font>"
		self.BACK_TEXT = u"<font=4>" + self.color4 + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_BACK", ()).upper() + "</color></font>"
		self.FORWARD_TEXT = u"<font=4>" + self.color4 + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_FORWARD", ()).upper() + "</color></font>"
		self.MENU_TEXT = u"<font=4>" + self.color4 + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_TOP", ()).upper() + "</color></font>"
		
		self.lSpecial = 	[CyTranslator().getText("TXT_KEY_PEDIA_FIRST_BENEFITS", ()),
					CyTranslator().getText("TXT_KEY_WB_MAP_CENTERING", ()),
					CyTranslator().getText("TXT_KEY_PEDIA_MAP_VISIBLE", ()),
					CyTranslator().getText("TXT_KEY_WB_MAP_TRADING", ()),
					CyTranslator().getText("TXT_KEY_WB_TECH_TRADING", ()),
					CyTranslator().getText("TXT_KEY_WB_GOLD_TRADING", ()),
					CyTranslator().getText("TXT_KEY_MISC_OPEN_BORDERS", ()),
					CyTranslator().getText("TXT_KEY_MISC_DEFENSIVE_PACT", ()),
					CyTranslator().getText("TXT_KEY_MISC_PERMANENT_ALLIANCE", ()),
					CyTranslator().getText("TXT_KEY_WB_VASSAL_TRADING", ()),
					CyTranslator().getText("TXT_KEY_WB_BRIDGE_BUILDING", ()),
					CyTranslator().getText("TXT_KEY_CONCEPT_IRRIGATION", ()),
					CyTranslator().getText("TXT_KEY_WB_IGNORE_IRRIGATION", ()),
					CyTranslator().getText("TXT_KEY_WB_WATER_WORK", ()),
					CyTranslator().getText("TXT_KEY_WB_EXTRA_WATER_SIGHT", ()),
					CyTranslator().getText("TXT_KEY_MISC_RIVERS", ()) + " " + CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ())]

		self.listCategories = [	CyTranslator().getText(self.sIntroIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_INTRO", ()),
					CyTranslator().getText(self.sTechIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()),
					CyTranslator().getText(self.sUnitIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()),
					CyTranslator().getText(self.sUnitCombatIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()),
					CyTranslator().getText(self.sPromotionIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()),
					CyTranslator().getText(self.sBuildingIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()),
					CyTranslator().getText(self.sWonderIcon, ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()),
					CyTranslator().getText(self.sUnitCombatIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BCHART", ()),
					CyTranslator().getText(self.sProjectIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()),
					CyTranslator().getText(self.sProcessIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROCESS", ()),
					CyTranslator().getText(self.sTerrainIcon, ()) + CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN", ()),
					CyTranslator().getText(self.sFeatureIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ()),
					CyTranslator().getText(self.sBonusIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()),
					CyTranslator().getText(self.sImprovementIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()),
					CyTranslator().getText(self.sRouteIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE", ()),
					CyTranslator().getText(self.sUpgradeIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_TREE", ()),
					CyTranslator().getText(self.sCivIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()),
					CyTranslator().getText(self.sLeaderIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()),
					CyTranslator().getText(self.sTraitIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_TRAITS", ()),
					CyTranslator().getText(self.sSpecialistIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ()),
					CyTranslator().getText(self.sReligionIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()),
					CyTranslator().getText(self.sCorporationIcon, ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()),
					CyTranslator().getText(self.sCivicIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()),
					CyTranslator().getText(self.sGameInfoIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_GAME_INFO", ()),
					CyTranslator().getText(self.sHelpIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()),
					CyTranslator().getText(self.sHelpIcon, ()) + CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()),
					CyTranslator().getText(self.sHelpIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_HINTS", ()),
					CyTranslator().getText(self.sHelpIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_INDEX", ()),
					CyTranslator().getText(self.sMovieIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_MOVIES", ()),
					CyTranslator().getText(self.sSpecialistIcon, ()) + CyTranslator().getText("TXT_KEY_PEDIA_CREDITS", ())]

		screen = self.getScreen()
		screen.setRenderInterfaceOnly(True);
		screen.setScreenGroup(1)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addDDSGFC("PediaMainBackground", CyArtFileMgr().getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel("PediaMainTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel("PediaMainBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.setText("PediaMainExitWidget", "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
		screen.setText("PediaMainBack", "Background", self.BACK_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_BACK, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK, 1, -1)
		screen.setText("PediaMainForward", "Background", self.FORWARD_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_FORWARD, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)

		if self.bLeft:
			screen.setButtonGFC("ChangeSide", u"", "", screen.getXResolution() - 20 - 32, self.Y_TITLE, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
		else:
			screen.setButtonGFC("ChangeSide", u"", "", 20, self.Y_TITLE, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
		
		self.W_BORDER = 20
		self.W_PANEL = 225
		self.Y_ITEMS_PANE = 55 + self.W_BORDER
		self.X_ITEMS_PANE = self.W_BORDER + self.W_PANEL * self.bLeft
		self.X_PANEL = (screen.getXResolution() - self.W_PANEL) * (not self.bLeft)
		self.W_ITEMS_PANE = screen.getXResolution() - self.W_PANEL - self.W_BORDER * 2
		self.H_ITEMS_PANE = (screen.getYResolution() - self.Y_ITEMS_PANE - 65)/24 * 24 + 2

		self.X_SORT = self.X_ITEMS_PANE
		self.Y_SORT = self.Y_ITEMS_PANE - 25
		self.W_SORT = screen.getXResolution()/6

		sText = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())
		if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY"):
			sText = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		sText += CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ()) + "</color>"
		screen.setText("HideInactive", "Background", "<font=3b>" + sText + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_ITEMS_PANE + self.W_ITEMS_PANE - self.W_BORDER, self.Y_SORT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, -1)
		screen.hide("HideInactive")
		
	def showScreen(self, iCategory):
		self.iCategory = iCategory
		screen = self.getScreen()
		self.deleteAllWidgets()
		if not screen.isActive():
			self.setPediaCommonWidgets()

		szHeader = u"<font=4b>" + self.color4 + "PLATYPEDIA" + u"</color></font>"
		screen.setLabel(self.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, -1, -1)
		if self.iLastScreen != CvScreenEnums.PEDIA_MAIN or not screen.isActive():
			screen.addListBoxGFC("PlatyTable", "", self.X_PANEL, 55, self.W_PANEL, screen.getYResolution() - 110, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSelect("PlatyTable", True)
			screen.setStyle("PlatyTable", "Table_StandardCiv_Style")
			for i in xrange(len(self.listCategories)):
				screen.appendListBoxString("PlatyTable", self.color3 + self.listCategories[i] + "</color>", WidgetTypes.WIDGET_PEDIA_MAIN, i, 0, CvUtil.FONT_LEFT_JUSTIFY )
		screen.show("PlatyTable")
		screen.setSelectedListBoxStringGFC("PlatyTable", self.iCategory)
		self.iLastScreen = CvScreenEnums.PEDIA_MAIN

		if self.mapCategories.has_key(iCategory):
			self.mapCategories.get(iCategory)()

	def setNewTable(self, iSort, listSorted, nEntries = 0):
		screen = self.getScreen()
		for item in listSorted:
			nEntries += len(item[2])
		if iSort:
			nEntries += (len(listSorted) * 2 - 1)
		iMaxRows = self.H_ITEMS_PANE / 24
		iMaxColumns = self.W_ITEMS_PANE / 180
		self.iNumColumns = max(1, min(iMaxColumns, (nEntries + iMaxRows - 1) /iMaxRows))
		self.iNumRows = (nEntries + self.iNumColumns - 1) / self.iNumColumns + self.iExtraRow
		self.iExtraSpace = self.iNumColumns * self.iNumRows - nEntries
		self.sTableName = self.getNextWidgetName()
		screen.addTableControlGFC(self.sTableName, self.iNumColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE + 10, self.W_ITEMS_PANE, self.H_ITEMS_PANE, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		for i in xrange(self.iNumColumns):
			screen.setTableColumnHeader(self.sTableName, i, "", self.W_ITEMS_PANE/self.iNumColumns)
		for i in xrange(self.iNumRows):
			screen.appendTableRow(self.sTableName)
		self.iCount = 0

	def placePedia(self, listSorted, SectionIcon, Widget, iPython, bDone, ItemIcon = ""):
		screen = self.getScreen()
		iCount = self.iCount
		if not ItemIcon:
			ItemIcon = SectionIcon
		for iList in xrange(len(listSorted)):
			lTemp = listSorted[iList]
			if lTemp[0]:
				iRow = self.iCount % self.iNumRows
				if iRow == self.iNumRows - 1:
					if self.iExtraSpace > 0:
						self.iCount += 1
						self.iExtraSpace -= 1
					else:
						self.iExtraRow += 1
						self.iCount = iCount
						self.showScreen(self.iCategory)
						return
				iRow = self.iCount % self.iNumRows
				iColumn = self.iCount / self.iNumRows
				sList = lTemp[0]
				sButton = ""
				if lTemp[1]:
					sButton = lTemp[1]
				else:
					sList = SectionIcon + sList
				screen.setTableText(self.sTableName, iColumn, iRow, "<font=3>" + self.color + sList + u"</color></font>", sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				self.iCount += 1
			for item in lTemp[2]:
				iRow = self.iCount % self.iNumRows
				iColumn = self.iCount / self.iNumRows
				sText = item[0]
				if not item[2]:
					sText = ItemIcon + sText
				if iPython > -1:
					iData1 = iPython
					iData2 = item[1]
				else:
					iData1 = item[1]
					iData2 = 1
				screen.setTableText(self.sTableName, iColumn, iRow, u"<font=3>" + self.color2 + sText + u"</color></font>", item[2], Widget, iData1, iData2, CvUtil.FONT_LEFT_JUSTIFY)
				self.iCount += 1
			if lTemp[0]:
				if iList < len(listSorted) - 1:
					iRow = self.iCount % self.iNumRows
					if iRow == 0:
						self.iExtraSpace += 1
						continue
					iColumn = self.iCount / self.iNumRows
					screen.setTableText(self.sTableName, iColumn, iRow, " ", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					self.iCount += 1
		if bDone:
			self.iExtraRow = 0
		else:
			iRow = self.iCount % self.iNumRows
			if iRow == 0:
				self.iExtraSpace += 1
			else:
				iColumn = self.iCount / self.iNumRows
				screen.setTableText(self.sTableName, iColumn, iRow, " ", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				self.iCount += 1

	def placeMovies(self):
		screen = self.getScreen()

		List0 = self.sortWonders(-1)
		List1 = self.sortProjects(-1)
		List2 = self.sortReligions(-1)
		List3 = self.sortCorporations(-1)
		List4 = self.sortVictories()
		self.setNewTable(1, List0 + List1 + List2 + List3 + List4)
		if List0 and List0[0][2]:
			self.placePedia(List0, CyTranslator().getText(self.sWonderIcon, ()), WidgetTypes.WIDGET_PYTHON, 7870, False)
		if List1 and List1[0][2]:
			self.placePedia(List1, CyTranslator().getText(self.sProjectIcon, ()), WidgetTypes.WIDGET_PYTHON, 6785, False)
		if List2 and List2[0][2]:
			self.placePedia(List2, CyTranslator().getText(self.sReligionIcon, ()), WidgetTypes.WIDGET_PYTHON, 7869, False)
		if List3 and List3[0][2]:
			self.placePedia(List3, CyTranslator().getText(self.sCorporationIcon, ()), WidgetTypes.WIDGET_PYTHON, 8201, False)
		if List4 and List4[0][2]:
			self.placePedia(List4, CyTranslator().getText("[ICON_OCCUPATION] ", ()), WidgetTypes.WIDGET_PYTHON, 6786, True)

	def placeIntro(self):
		screen = self.getScreen()
		PlatyPediaIntro.CvPediaIntro(self).interfaceScreen()

	def placeTechs(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortTechs)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_COST", ()), 1, 1, 1 == self.iSortTechs)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 2, 2, 2 == self.iSortTechs)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_ADVISOR", ()), 3, 3, 3 == self.iSortTechs)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), 4, 4, 4 == self.iSortTechs)

		listSorted = self.sortTechs(self.iSortTechs)
		self.setNewTable(self.iSortTechs, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sTechIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, -1, True)

	def placeUnits(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortUnits)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_COST", ()), 1, 1, 1 == self.iSortUnits)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()), 2, 2, 2 == self.iSortUnits)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 3, 3, 3 == self.iSortUnits)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 4, 4, 4 == self.iSortUnits)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 5, 5, 5 == self.iSortUnits)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_ADVISOR", ()), 6, 6, 6 == self.iSortUnits)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL", ()), 7, 7, 7 == self.iSortUnits)

		listSorted = self.sortUnits(self.iSortUnits)
		self.setNewTable(self.iSortUnits, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sUnitIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, -1, True)

	def placeUnitGroups(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		listSorted = self.sortUnitGroups(0)
		self.setNewTable(0, listSorted, 2)		
		screen.setTableText(self.sTableName, 0, 0, "<font=3>" + self.color2 + CyTranslator().getText("TXT_KEY_PEDIA_ALL_GROUPS", ()) + "</color></font>", ",Art/Interface/Buttons/Promotions/Combat5.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,5,10", WidgetTypes.WIDGET_PYTHON, 6781, -2, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(self.sTableName, 0, 1, "<font=3>" + self.color2 + CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ()) + "</color></font>", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), WidgetTypes.WIDGET_PYTHON, 6781, -1, CvUtil.FONT_LEFT_JUSTIFY)
		self.iCount += 2
		self.placePedia(listSorted, CyTranslator().getText(self.sUnitCombatIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, -1, True)

	def placePromotions(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortPromotions)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()), 1, 1, 1 == self.iSortPromotions)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 2, 2, 2 == self.iSortPromotions)

		listSorted = self.sortPromotions(self.iSortPromotions)
		self.setNewTable(self.iSortPromotions, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sPromotionIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, -1, True)

	def placeBuildings(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortBuildings)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_COST", ()), 1, 1, 1 == self.iSortBuildings)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 2, 2, 2 == self.iSortBuildings)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_ADVISOR", ()), 3, 3, 3 == self.iSortBuildings)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_CONCEPT_VICTORY", ()), 4, 4, 4 == self.iSortBuildings)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL", ()), 5, 5, 5 == self.iSortBuildings)

		listSorted = self.sortBuildings(self.iSortBuildings)
		self.setNewTable(self.iSortBuildings, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sBuildingIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, -1, True)

	def placeBuildingChart(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), -1, -1, self.iSortBChart == -1)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ()), 0, 0, self.iSortBChart == 0)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_TEAM_WONDER", ()), 1, 1, self.iSortBChart == 1)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ()), 2, 2, self.iSortBChart == 2)

		screen.addDropDownBoxGFC("TreeSort", self.X_SORT + self.W_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("TreeSort", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL",()), 0, 0, 0 == self.iSortBChartType)
		screen.addPullDownString("TreeSort", CyTranslator().getText("TXT_KEY_PEDIA_YIELDS",()), 1, 1, 1 == self.iSortBChartType)
		screen.addPullDownString("TreeSort", CyTranslator().getText("TXT_KEY_CONCEPT_COMMERCE",()), 2, 2, 2 == self.iSortBChartType)
		screen.addPullDownString("TreeSort", CyTranslator().getText("TXT_KEY_CONCEPT_TRADE",()), 3, 3, 3 == self.iSortBChartType)
		PlatyPediaBuildingChart.CvPediaBuildingChart(self).interfaceScreen()

	def placeWonders(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortWonders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_COST", ()), 1, 1, 1 == self.iSortWonders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 2, 2, 2 == self.iSortWonders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 3, 3, 3 == self.iSortWonders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_CONCEPT_GREAT_PEOPLE", ()), 4, 4, 4 == self.iSortWonders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_ADVISOR", ()), 5, 5, 5 == self.iSortWonders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_CONCEPT_VICTORY", ()), 6, 6, 6 == self.iSortWonders)

		listSorted = self.sortWonders(self.iSortWonders)
		self.setNewTable(self.iSortWonders, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sWonderIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, -1, True)

	def placeProjects(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortProjects)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_COST", ()), 1, 1, 1 == self.iSortProjects)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 2, 2, 2 == self.iSortProjects)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 3, 3, 3 == self.iSortProjects)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_CONCEPT_VICTORY", ()), 4, 4, 4 == self.iSortProjects)

		listSorted = self.sortProjects(self.iSortProjects)
		self.setNewTable(self.iSortProjects, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sProjectIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, -1, True)

	def placeProcesses(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortProcesses)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 1, 1, 1 == self.iSortProcesses)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_CONCEPT_COMMERCE", ()), 2, 2, 2 == self.iSortProcesses)

		listSorted = self.sortProcesses(self.iSortProcesses)
		self.setNewTable(self.iSortProcesses, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sProcessIcon, ()), WidgetTypes.WIDGET_PYTHON, 6787, True)

	def placeTerrains(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortTerrains)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 1, 1, 1 == self.iSortTerrains)

		listSorted = self.sortTerrains(self.iSortTerrains)
		self.setNewTable(self.iSortTerrains, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sTerrainIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, -1, True)

	def placeFeatures(self):
		screen = self.getScreen()
		listSorted = self.sortFeatures(0)
		self.setNewTable(0, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sFeatureIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, -1, True)

	def placeBoni(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortBonus)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, 1 == self.iSortBonus)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 2, 2, 2 == self.iSortBonus)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 3, 3, 3 == self.iSortBonus)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), 4, 4, 4 == self.iSortBonus)

		listSorted = self.sortBonus(self.iSortBonus)
		self.setNewTable(self.iSortBonus, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sBonusIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, -1, True)

	def placeImprovements(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortImprovements)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 1, 1, 1 == self.iSortImprovements)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()), 2, 2, 2 == self.iSortImprovements)

		listSorted = self.sortImprovements(self.iSortImprovements)
		self.setNewTable(self.iSortImprovements, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sImprovementIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, -1, True)

	def placeRoutes(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortRoutes)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DEMO_SCREEN_VALUE_TEXT", ()), 1, 1, 1 == self.iSortRoutes)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 2, 2, 2 == self.iSortRoutes)

		listSorted = self.sortRoutes(self.iSortRoutes)
		if self.iSortRoutes < 2:
			self.setNewTable(0, listSorted)
		else:
			self.setNewTable(self.iSortRoutes, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sRouteIcon, ()), WidgetTypes.WIDGET_PYTHON, 6788, True)

	def placeUpgradeTree(self):
		screen = self.getScreen()
		self.UPGRADES_GRAPH_ID = self.getNextWidgetName()
		screen.addScrollPanel(self.UPGRADES_GRAPH_ID, "", self.X_ITEMS_PANE - self.W_BORDER/2, self.Y_ITEMS_PANE - self.W_BORDER/2, self.W_ITEMS_PANE + self.W_BORDER, self.H_ITEMS_PANE + self.W_BORDER/2, PanelStyles.PANEL_STYLE_STANDARD)
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH",()), 0, 0, 0 == self.iSortTree)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT",()), 1, 1, 1 == self.iSortTree)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION",()), 2, 2, 2 == self.iSortTree)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING",()), 3, 3, 3 == self.iSortTree)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT",()), 4, 4, 4 == self.iSortTree)
		screen.addPullDownString("PlatySort", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT",()), 5, 5, 5 == self.iSortTree)

		if self.iSortTree == 0:
			PlatyPediaTechTree.CvPediaTechTree(self).interfaceScreen()
			return

		elif self.iSortTree == 1:
			screen.addDropDownBoxGFC("TreeSort", self.X_SORT + self.W_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			screen.addPullDownString("TreeSort", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -1, -1, -1 == self.iSortUTree)
			for i in xrange(DomainTypes.NUM_DOMAIN_TYPES):
				screen.addPullDownString("TreeSort", gc.getDomainInfo(i).getDescription(), i, i, i == self.iSortUTree)

		elif self.iSortTree == 2:
			screen.addDropDownBoxGFC("TreeSort", self.X_SORT + self.W_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			screen.addPullDownString("TreeSort", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -1, -1, -1 == self.iSortPTree)
			for iClass in xrange(gc.getNumUnitCombatInfos()):
				screen.addPullDownString("TreeSort", gc.getUnitCombatInfo(iClass).getDescription(), iClass, iClass, iClass == self.iSortPTree)

		upgradesGraph = PlatyUpgradesGraph.UnitUpgradesGraph(self)
		upgradesGraph.getGraph()
		upgradesGraph.drawGraph()

	def placeCivs(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortCivilizations)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, 1 == self.iSortCivilizations)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 2, 2, 2 == self.iSortCivilizations)

		listSorted = self.sortCivilizations(self.iSortCivilizations)
		self.setNewTable(self.iSortCivilizations, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sCivIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, -1, True)

	def placeLeaders(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortLeaders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()), 1, 1, 1 == self.iSortLeaders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_TRAITS", ()), 2, 2, 2 == self.iSortLeaders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()), 3, 3, 3 == self.iSortLeaders)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), 4, 4, 4 == self.iSortLeaders)

		listSorted = self.sortLeaders(self.iSortLeaders)
		self.setNewTable(self.iSortLeaders, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sLeaderIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, -1, True)

	def placeTraits(self):
		screen = self.getScreen()									
		listSorted = self.sortTraits()
		self.setNewTable(0, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sTraitIcon, ()), WidgetTypes.WIDGET_PYTHON, 6789, True)

	def placeSpecialists(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortSpecialists)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, 1 == self.iSortSpecialists)

		listSorted = self.sortSpecialists(self.iSortSpecialists)
		self.setNewTable(self.iSortSpecialists, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sSpecialistIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, -1, True)

	def placeReligions(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortReligions)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 1, 1, 1 == self.iSortReligions)

		listSorted = self.sortReligions(self.iSortReligions)
		self.setNewTable(self.iSortReligions, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sReligionIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, -1, True)

	def placeCorporations(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortCorporations)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 1, 1, 1 == self.iSortCorporations)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_CONCEPT_GREAT_PEOPLE", ()), 2, 2, 2 == self.iSortCorporations)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()), 3, 3, 3 == self.iSortCorporations)

		listSorted = self.sortCorporations(self.iSortCorporations)
		self.setNewTable(self.iSortCorporations, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sCorporationIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, -1, True)

	def placeCivics(self):
		screen = self.getScreen()
		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 0, 0, 0 == self.iSortCivics)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), 1, 1, 1 == self.iSortCivics)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_PEDIA_ERA", ()), 2, 2, 2 == self.iSortCivics)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UPKEEP", ()), 3, 3, 3 == self.iSortCivics)

		listSorted = self.sortCivics(self.iSortCivics)
		self.setNewTable(self.iSortCivics, listSorted)
		self.placePedia(listSorted, CyTranslator().getText(self.sCivicIcon, ()), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, -1, True)

	def placeGameInfos(self):
		screen = self.getScreen()
		List0 = self.sortCultureLevels()
		List1 = self.sortEra()
		List2 = self.sortGameSpeeds()
		List3 = self.sortHandicaps()
		List4 = self.sortUpkeep()
		List5 = self.sortWorld()
		self.setNewTable(1, List0 + List1 + List2 + List3 + List4 + List5)
		if List0[0][2]:
			self.placePedia(List0, CyTranslator().getText(self.sGameInfoIcon, ()), WidgetTypes.WIDGET_PYTHON, 6791, False, CyTranslator().getText("[ICON_CULTURE] ", ()))
		if List1[0][2]:
			self.placePedia(List1, CyTranslator().getText(self.sGameInfoIcon, ()), WidgetTypes.WIDGET_PYTHON, 6795, False, CyTranslator().getText("[ICON_RESEARCH] ", ()))
		if List2[0][2]:
			self.placePedia(List2, CyTranslator().getText(self.sGameInfoIcon, ()), WidgetTypes.WIDGET_PYTHON, 6792, False, CyTranslator().getText("[ICON_MOVES] ", ()))
		if List3[0][2]:
			self.placePedia(List3, CyTranslator().getText(self.sGameInfoIcon, ()), WidgetTypes.WIDGET_PYTHON, 6793, False, CyTranslator().getText("[ICON_OCCUPATION] ", ()))
		if List4[0][2]:
			self.placePedia(List4, CyTranslator().getText(self.sGameInfoIcon, ()), WidgetTypes.WIDGET_PYTHON, 6796, False, CyTranslator().getText("[ICON_GOLD] ", ()))
		if List5[0][2]:
			self.placePedia(List5, CyTranslator().getText(self.sGameInfoIcon, ()), WidgetTypes.WIDGET_PYTHON, 6797, True, CyTranslator().getText("[ICON_MAP] ", ()))

	def placeConcepts(self):
		screen = self.getScreen()
		List0 = self.sortConcepts()
		List1 = self.sortNewConcepts()
		self.setNewTable(1, List0 + List1)
		self.placePedia(List0, CyTranslator().getText(self.sHelpIcon, ()), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, False)
		self.placePedia(List1, CyTranslator().getText(self.sHelpIcon, ()), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, True)

	def placeGameOptions(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		self.szAreaId = self.getNextWidgetName()
		screen.addListBoxGFC(self.szAreaId, "", self.X_ITEMS_PANE, self.Y_ITEMS_PANE + 10, self.W_ITEMS_PANE, self.H_ITEMS_PANE, TableStyles.TABLE_STYLE_STANDARD )

		lList = []
		for i in xrange(gc.getNumGameOptionInfos()):
			if CyGame().isFinalInitialized() and gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY"):
				if not CyGame().isOption(i): continue
			Info = gc.getGameOptionInfo(i)
			if Info.getVisible() or CyGame().isDebugMode():
				lList.append([Info.getDescription(), i])
		lList.sort()
		for i in lList:
			sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
			if CyGame().isFinalInitialized():
				if CyGame().isOption(i[1]):
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				else:
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			Info = gc.getGameOptionInfo(i[1])
			sText = CyTranslator().getText("[ICON_BULLET]", ()) + "<b>" + sColor + i[0] + self.color2 + "</b>\n" + Info.getHelp() + "</color>"
			screen.appendListBoxString(self.szAreaId, sText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeHints(self):
		screen = self.getScreen()  
		self.szAreaId = self.getNextWidgetName()
		screen.addListBoxGFC(self.szAreaId, "", self.X_ITEMS_PANE, self.Y_ITEMS_PANE + 10, self.W_ITEMS_PANE, self.H_ITEMS_PANE, TableStyles.TABLE_STYLE_STANDARD )

		szHintsText = CyGameTextMgr().buildHintsList()
		hintText = string.split( szHintsText, "\n" )
		for hint in hintText:
			if len(hint) > 0:
				screen.appendListBoxString(self.szAreaId, self.color2 + hint + "</color>", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeIndex(self):
		screen = self.getScreen()
		if CyGame().isFinalInitialized(): screen.show("HideInactive")
		listSorted = []
		listSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_ALL_GROUPS", ()), ",Art/Interface/Buttons/Promotions/Combat5.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,5,10", "", WidgetTypes.WIDGET_PYTHON, 6781, -2])
		listSorted.append([CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ()), CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), "", WidgetTypes.WIDGET_PYTHON, 6781, -1])
		temp = self.sortTechs(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getTechInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item[1], 1])
		temp = self.sortUnits(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getUnitInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item[1], 1])
		temp = self.sortBuildings(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getBuildingInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1])
		temp = self.sortWonders(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getBuildingInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1])
		temp = self.sortProjects(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getProjectInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, item[1], 1])
		temp = self.sortBonus(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getBonusInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, item[1], 1])
		temp = self.sortImprovements(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getImprovementInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item[1], 1])
		temp = self.sortPromotions(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getPromotionInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1])
		temp = self.sortUnitGroups(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getUnitCombatInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, item[1], 1])
		temp = self.sortCivilizations(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getCivilizationInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, item[1], 1])
		temp = self.sortLeaders(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getLeaderHeadInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, item[1], 1])
		temp = self.sortReligions(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getReligionInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, item[1], 1])
		temp = self.sortCorporations(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getCorporationInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, item[1], 1])
		temp = self.sortCivics(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getCivicInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item[1], 1])
		temp = self.sortTerrains(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getTerrainInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, item[1], 1])
		temp = self.sortFeatures(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getFeatureInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, item[1], 1])
		temp = self.sortSpecialists(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getSpecialistInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, item[1], 1])
		temp = self.sortConcepts()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText(self.sHelpIcon, ()), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, item[1]])
		temp = self.sortNewConcepts()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText(self.sHelpIcon, ()), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, item[1]])
		temp = self.sortTraits()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText(self.sTraitIcon, ()), WidgetTypes.WIDGET_PYTHON, 6789, item[1]])
		temp = self.sortProcesses(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getProcessInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PYTHON, 6787, item[1]])
		temp = self.sortRoutes(0)
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], gc.getRouteInfo(item[1]).getButton(), "", WidgetTypes.WIDGET_PYTHON, 6788, item[1]])
		temp = self.sortCultureLevels()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText("[ICON_CULTURE] ", ()), WidgetTypes.WIDGET_PYTHON, 6791, item[1]])
		temp = self.sortGameSpeeds()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText("[ICON_MOVES] ", ()), WidgetTypes.WIDGET_PYTHON, 6792, item[1]])
		temp = self.sortHandicaps()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText("[ICON_OCCUPATION] ", ()), WidgetTypes.WIDGET_PYTHON, 6793, item[1]])
		temp = self.sortEra()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText("[ICON_RESEARCH] ", ()), WidgetTypes.WIDGET_PYTHON, 6795, item[1]])
		temp = self.sortUpkeep()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText("[ICON_GOLD] ", ()), WidgetTypes.WIDGET_PYTHON, 6796, item[1]])
		temp = self.sortWorld()
		if temp:
			for item in temp[0][2]:
				listSorted.append([item[0], "", CyTranslator().getText("[ICON_MAP] ", ()), WidgetTypes.WIDGET_PYTHON, 6797, item[1]])

		lIndex = {}
		for item in listSorted:
			sKey = unicode(" ")
			sDescription = unicode(item[0])
			if sDescription:
				sKey = sDescription[0]
			if not sKey in lIndex:
				lIndex[sKey] = []
			lIndex[sKey].append(item)
		lIndex = lIndex.items()
		lIndex.sort()

		listSorted = []
		for item in lIndex:
			if self.iSortIndex != -1 and self.iSortIndex != item[0]: continue
			item[1].sort()
			listSorted.append([item[0], "", item[1]])
		self.setNewTable(self.iSortIndex == -1, listSorted)

		screen.addDropDownBoxGFC("PlatySort", self.X_SORT, self.Y_SORT, self.W_SORT, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("PlatySort",  CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), -1, -1, -1 == self.iSortIndex)
		for item in lIndex:
			i = item[0]
			screen.addPullDownString("PlatySort",  i, ord(i), ord(i), i == self.iSortIndex)

		iCount = 0
		for iList in xrange(len(listSorted)):
			list = listSorted[iList]
			if self.iSortIndex == -1:
				iRow = iCount % self.iNumRows
				if iRow == self.iNumRows - 1:
					if self.iExtraSpace:
						iCount += 1
						self.iExtraSpace -= 1
					else:
						self.iExtraRow += 1
						self.showScreen(self.iCategory)
						return
				iRow = iCount % self.iNumRows
				iColumn = iCount / self.iNumRows
				sList = CyTranslator().getText("[ICON_STAR]", ()) + list[0] + CyTranslator().getText("[ICON_STAR]", ())
				screen.setTableText(self.sTableName, iColumn, iRow, u"<font=3>" + self.color + sList + u"</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				iCount += 1
			for item in list[2]:
				iRow = iCount % self.iNumRows
				iColumn = iCount / self.iNumRows
				sText = u"<font=3>" + self.color2 + item[2] + item[0] + u"</color></font>"
				screen.setTableText(self.sTableName, iColumn, iRow, sText, item[1], item[3], item[4], item[5], CvUtil.FONT_LEFT_JUSTIFY)
				iCount += 1
			if self.iSortIndex == -1:
				if iList < len(listSorted) - 1:
					iRow = iCount % self.iNumRows
					if iRow == 0:
						self.iExtraSpace += 1
						continue
					iColumn = iCount / self.iNumRows
					screen.setTableText(self.sTableName, iColumn, iRow, " ", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					iCount += 1
		self.iExtraRow = 0

	def placeCredits(self):
		screen = self.getScreen()
		PlatyPediaCredits.CvPediaCredits(self).interfaceScreen()

	def getNextWidgetName(self):
		szName = "PediaMainWidget" + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
		
	def pediaJump(self, iScreen, iEntry, bRemoveFwdList):
		if iEntry < 0 and iScreen != CvScreenEnums.PEDIA_UNIT_CHART: return
		self.iActivePlayer = CyGame().getActivePlayer()

		self.pediaHistory.append((iScreen, iEntry))
		if bRemoveFwdList:
			self.pediaFuture = []

		if iScreen == CvScreenEnums.PEDIA_MAIN:
			self.showScreen(iEntry)
		elif iScreen == CvScreenEnums.PEDIA_TECH:
			PlatyPediaTech.CvPediaTech(self).interfaceScreen(iEntry)
		elif iScreen == CvScreenEnums.PEDIA_UNIT:
			PlatyPediaUnit.CvPediaUnit(self).interfaceScreen(iEntry)
		elif iScreen == CvScreenEnums.PEDIA_BUILDING:
			PlatyPediaBuilding.CvPediaBuilding(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_PROMOTION:
			PlatyPediaPromotion.CvPediaPromotion(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_UNIT_CHART:
			PlatyPediaUnitChart.CvPediaUnitChart(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_BONUS:
			PlatyPediaBonus.CvPediaBonus(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_TERRAIN:
			PlatyPediaTerrain.CvPediaTerrain(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_FEATURE:
			PlatyPediaFeature.CvPediaFeature(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_IMPROVEMENT:
			PlatyPediaImprovement.CvPediaImprovement(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_CIVIC:
			PlatyPediaCivic.CvPediaCivic(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_CIVILIZATION:
			PlatyPediaCivilization.CvPediaCivilization(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_LEADER:
			self.pediaLeader.interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_SPECIALIST:
			PlatyPediaSpecialist.CvPediaSpecialist(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_PROJECT:
			PlatyPediaProject.CvPediaProject(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_RELIGION:
			PlatyPediaReligion.CvPediaReligion(self).interfaceScreen(iEntry)	
		elif iScreen == CvScreenEnums.PEDIA_CORPORATION:
			PlatyPediaCorporation.CvPediaCorporation(self).interfaceScreen(iEntry)
		elif iScreen == self.PLATYPEDIA_TRAIT:
			PlatyPediaTrait.CvPediaTrait(self).interfaceScreen(iEntry)
		elif iScreen == self.PLATYPEDIA_ROUTE:
			PlatyPediaRoute.CvPediaRoute(self).interfaceScreen(iEntry)
		elif iScreen == self.PLATYPEDIA_PROCESS:
			PlatyPediaProcess.CvPediaProcess(self).interfaceScreen(iEntry)
		elif iScreen == self.PLATYPEDIA_GAME_INFO:
			iData1 = iEntry / 10000
			iData2 = iEntry % 10000
			PlatyPediaGameInfo.CvPediaGameInfo(self).interfaceScreen(iData1, iData2)
		elif iScreen == self.PLATYPEDIA_MOVIE:
			iData1 = iEntry / 10000
			iData2 = iEntry % 10000
			PlatyPediaMovie.CvPediaMovie(self).interfaceScreen(iData1, iData2)
		elif iScreen == CvScreenEnums.PEDIA_HISTORY:
			self.pediaHistorical.interfaceScreen(iEntry)

	def back(self):
		if len(self.pediaHistory) > 1:
			self.pediaFuture.append(self.pediaHistory.pop())
			current = self.pediaHistory.pop()
			self.pediaJump(current[0], current[1], False)
		return 1

	def forward(self):
		if self.pediaFuture:
			current = self.pediaFuture.pop()
			self.pediaJump(current[0], current[1], False)
		return 1

	def pediaShow(self):
		if not self.pediaHistory:
			self.pediaHistory.append((CvScreenEnums.PEDIA_MAIN, 0))
		current = self.pediaHistory.pop()
		self.pediaFuture = []
		self.pediaHistory = []
		self.pediaJump(current[0], current[1], False)

	def link(self, szLink):
		for i in xrange(gc.getNumConceptInfos()):
			if gc.getConceptInfo(i).isMatchForLink(szLink, False):
				iEntryId = self.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, i)
				return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
		for i in xrange(gc.getNumNewConceptInfos()):
			if gc.getNewConceptInfo(i).isMatchForLink(szLink, False):
				iEntryId = self.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, i)
				return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
		for i in xrange(gc.getNumTechInfos()):
			if gc.getTechInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_TECH, i, True)
		for i in xrange(gc.getNumUnitInfos()):
			if gc.getUnitInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT, i, True)
		for i in xrange(gc.getNumCorporationInfos()):
			if gc.getCorporationInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_CORPORATION, i, True)
		for i in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_BUILDING, i, True)
		for i in xrange(gc.getNumPromotionInfos()):
			if gc.getPromotionInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_PROMOTION, i, True)
		for i in xrange(gc.getNumUnitCombatInfos()):
			if gc.getUnitCombatInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT_CHART, i, True)
		for i in xrange(gc.getNumBonusInfos()):
			if gc.getBonusInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_BONUS, i, True)	
		for i in xrange(gc.getNumTerrainInfos()):
			if gc.getTerrainInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_TERRAIN, i, True)
		for i in xrange(gc.getNumFeatureInfos()):
			if gc.getFeatureInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_FEATURE, i, True)
		for i in xrange(gc.getNumImprovementInfos()):
			if gc.getImprovementInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_IMPROVEMENT, i, True)
		for i in xrange(gc.getNumCivicInfos()):
			if gc.getCivicInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVIC, i, True)
		for i in xrange(gc.getNumCivilizationInfos()):
			if gc.getCivilizationInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVILIZATION, i, True)
		for i in xrange(gc.getNumLeaderHeadInfos()):
			if gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_LEADER, i, True)
		for i in xrange(gc.getNumSpecialistInfos()):
			if gc.getSpecialistInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_SPECIALIST, i, True)
		for i in xrange(gc.getNumProjectInfos()):
			if gc.getProjectInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_PROJECT, i, True)
		for i in xrange(gc.getNumReligionInfos()):
			if gc.getReligionInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(CvScreenEnums.PEDIA_RELIGION, i, True)
		for i in xrange(gc.getNumTraitInfos()):
			if gc.getTraitInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_TRAIT, i, True)
		for i in xrange(gc.getNumRouteInfos()):
			if gc.getRouteInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_ROUTE, i, True)
		for i in xrange(gc.getNumProcessInfos()):
			if gc.getProcessInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_PROCESS, i, True)
		for i in xrange(gc.getNumCultureLevelInfos()):
			if gc.getCultureLevelInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_GAME_INFO, 6791 * 10000 + i, True)
		for i in xrange(gc.getNumGameSpeedInfos()):
			if gc.getGameSpeedInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_GAME_INFO, 6792 * 10000 + i, True)
		for i in xrange(gc.getNumHandicapInfos()):
			if gc.getHandicapInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_GAME_INFO, 6793 * 10000 + i, True)
		for i in xrange(gc.getNumEraInfos()):
			if gc.getEraInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_GAME_INFO, 6795 * 10000 + i, True)
		for i in xrange(gc.getNumUpkeepInfos()):
			if gc.getUpkeepInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_GAME_INFO, 6796 * 10000 + i, True)
		for i in xrange(gc.getNumWorldInfos()):
			if gc.getWorldInfo(i).isMatchForLink(szLink, False):
				return self.pediaJump(self.PLATYPEDIA_GAME_INFO, 6797 * 10000 + i, True)

	def deleteAllWidgets(self):
		screen = self.getScreen()
		iNumWidgets = self.nWidgetCount
		self.nWidgetCount = 0
		for i in xrange(iNumWidgets):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0
		screen.deleteWidget("PlatySort")
		screen.deleteWidget("TreeSort")
		screen.hide("HideInactive")

	def handlePlatySort(self) :
		screen = self.getScreen()
		iIndex = screen.getPullDownData("PlatySort", screen.getSelectedPullDownID("PlatySort"))
		if self.iCategory == self.PLATYPEDIA_TECH:
			self.iSortTechs = iIndex
		elif self.iCategory== self.PLATYPEDIA_UNIT:
			self.iSortUnits = iIndex
		elif self.iCategory == self.PLATYPEDIA_PROMOTION:
			self.iSortPromotions = iIndex
		elif self.iCategory == self.PLATYPEDIA_BUILDING:
			self.iSortBuildings = iIndex
		elif self.iCategory == self.PLATYPEDIA_WONDER:
			self.iSortWonders = iIndex
		elif self.iCategory == self.PLATYPEDIA_PROJECT:
			self.iSortProjects = iIndex
		elif self.iCategory == self.PLATYPEDIA_PROCESS:
			self.iSortProcesses = iIndex
		elif self.iCategory == self.PLATYPEDIA_TERRAIN:
			self.iSortTerrains = iIndex
		elif self.iCategory == self.PLATYPEDIA_BONUS:
			self.iSortBonus = iIndex
		elif self.iCategory == self.PLATYPEDIA_IMPROVEMENT:
			self.iSortImprovements = iIndex
		elif self.iCategory == self.PLATYPEDIA_ROUTE:
			self.iSortRoutes = iIndex
		elif self.iCategory == self.PLATYPEDIA_CIV:
			self.iSortCivilizations = iIndex
		elif self.iCategory == self.PLATYPEDIA_LEADER:
			self.iSortLeaders = iIndex
		elif self.iCategory == self.PLATYPEDIA_RELIGION:
			self.iSortReligions = iIndex
		elif self.iCategory == self.PLATYPEDIA_CORPORATION:
			self.iSortCorporations = iIndex
		elif self.iCategory == self.PLATYPEDIA_CIVIC:
			self.iSortCivics = iIndex
		elif self.iCategory == self.PLATYPEDIA_SPECIALIST:
			self.iSortSpecialists = iIndex
		elif self.iCategory == self.PLATYPEDIA_INDEX:
			if iIndex == -1:
				self.iSortIndex = iIndex
			else:
				self.iSortIndex = chr(iIndex)
		elif self.iCategory == self.PLATYPEDIA_B_CHART:
			self.iSortBChart = iIndex
		elif self.iCategory == self.PLATYPEDIA_TREE:
			self.iSortTree = iIndex
		self.showScreen(self.iCategory)

	def handleTreeSort(self) :
		screen = self.getScreen()
		iIndex = screen.getPullDownData("TreeSort", screen.getSelectedPullDownID("TreeSort"))
		if self.iCategory == self.PLATYPEDIA_TREE:
			if self.iSortTree == 1:
				self.iSortUTree = iIndex
			elif self.iSortTree == 2:
				self.iSortPTree = iIndex
		elif self.iCategory == self.PLATYPEDIA_B_CHART:
			self.iSortBChartType = iIndex
		self.showScreen(self.iCategory)

	def handleInput (self, inputClass):
		if inputClass.getFunctionName() == "PlatySort":
			self.handlePlatySort()
			return
		if inputClass.getFunctionName() == "TreeSort":
			self.handleTreeSort()
			return
		if inputClass.getFunctionName() == "ChangeSide":
			self.bLeft = not self.bLeft
			self.setPediaCommonWidgets()
			self.showScreen(self.iCategory)
			return
		if inputClass.getFunctionName() == "HideInactive":
			gc.setDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY", not gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY"))
			self.setPediaCommonWidgets()
			self.showScreen(self.iCategory)
			return
		if inputClass.getButtonType() == WidgetTypes.WIDGET_PYTHON:
			iData1 = inputClass.getData1()
			iData2 = inputClass.getData2()
			if iData1 == 6781:
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT_CHART, iData2, True)
			elif iData1 == 8201 or iData1 == 6785 or iData1 == 6786 or iData1 == 7869 or iData1 == 7870:
				return self.pediaJump(self.PLATYPEDIA_MOVIE, iData1 * 10000 + iData2, True)
			elif iData1 == 6787:
				return self.pediaJump(self.PLATYPEDIA_PROCESS, iData2, True)
			elif iData1 == 6788:
				return self.pediaJump(self.PLATYPEDIA_ROUTE, iData2, True)
			elif iData1 == 6789:
				return self.pediaJump(self.PLATYPEDIA_TRAIT, iData2, True)
			elif iData1 > 6789 and iData1 < 6800:
				return self.pediaJump(self.PLATYPEDIA_GAME_INFO, iData1 * 10000 + iData2, True)
		if self.iLastScreen == CvScreenEnums.PEDIA_LEADER:
			return self.pediaLeader.handleInput(inputClass)
		return 0

###############################################		Sort Methods Start		##############################################
	def sortByCost(self, lItems):
		lSorted = []
		lTemp = []
		iCostMin = -1
		iCostMax = 1
		for item in lItems:
			iCost = item[3]
			if iCost < iCostMax:
				lTemp.append(item)
			else:
				if lTemp:
					sDescription = ""
					if iCostMin > -1:
						sDescription = "%d - %d" % (iCostMin, iCostMax - 1)
					lSorted.append([sDescription, "", lTemp])
				lTemp = [item]
				iCostMin = iCostMax
				while iCostMax <= iCost:
					sFirst = str(iCostMax)[0]
					if iCostMax < 10:
						iCostMax = 10
					else:
						iPower = len(str(iCostMax)) - 1
						iIncrement = 10**iPower * 25/10
						if sFirst == "1":
							iCostMax = iIncrement
						else:
							iCostMax += iIncrement
		if lTemp:
			sDescription = ""
			if iCostMin > -1:
				sDescription = "%d - %d" % (iCostMin, iCostMax - 1)
			lSorted.append([sDescription, "", lTemp])
		return lSorted

	def sortTechs(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumTechInfos()):
			ItemInfo = gc.getTechInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			iActiveTeam = CyGame().getActiveTeam()
			for i in xrange(len(lItems)):
				iItem = lItems[i][1]
				ItemInfo = gc.getTechInfo(iItem)
				iCost = ItemInfo.getResearchCost()
				if iActiveTeam > -1:
					iCost = gc.getTeam(iActiveTeam).getResearchCost(iItem)
				lItems[i].append(iCost)
			lItems = sorted(lItems, key = lambda x: x[3])
			lSorted = self.sortByCost(lItems)
		elif iType == 2:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getTechInfo(item[1])
					if ItemInfo.getEra() == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 3:
			for iAdvisor in xrange(-1, 6):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getTechInfo(item[1])
					if ItemInfo.getAdvisorType() == iAdvisor:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					if iAdvisor > -1:
						sDescription = CyTranslator().getText(self.lAdvisors[iAdvisor], ())
					lSorted.append([sDescription, "", lTemp])
			lSorted.sort()
		elif iType == 4:
			lSpecial = []
			lTerrain = []
			lCommerce = []
			lReligion = []
			for i in xrange(len(self.lSpecial)):
				lSpecial.append([])
			for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				lCommerce.append([])
			for i in xrange(gc.getNumTerrainInfos()):
				lTerrain.append([])
			for item in lItems:
				ItemInfo = gc.getTechInfo(item[1])
				if ItemInfo.getFirstFreeTechs() > 0 or ItemInfo.getFirstFreeUnitClass() > -1:
					lSpecial[0].append(item)
				if ItemInfo.isMapCentering():
					lSpecial[1].append(item)
				if ItemInfo.isMapVisible():
					lSpecial[2].append(item)
				if ItemInfo.isMapTrading():
					lSpecial[3].append(item)
				if ItemInfo.isTechTrading():
					lSpecial[4].append(item)
				if ItemInfo.isGoldTrading():
					lSpecial[5].append(item)
				if ItemInfo.isOpenBordersTrading():
					lSpecial[6].append(item)
				if ItemInfo.isDefensivePactTrading():
					lSpecial[7].append(item)
				if ItemInfo.isPermanentAllianceTrading():
					lSpecial[8].append(item)
				if ItemInfo.isVassalStateTrading():
					lSpecial[9].append(item)
				if ItemInfo.isBridgeBuilding():
					lSpecial[10].append(item)
				if ItemInfo.isIrrigation():
					lSpecial[11].append(item)
				if ItemInfo.isIgnoreIrrigation():
					lSpecial[12].append(item)
				if ItemInfo.isWaterWork():
					lSpecial[13].append(item)
				if ItemInfo.isExtraWaterSeeFrom():
					lSpecial[14].append(item)
				if ItemInfo.isRiverTrade():
					lSpecial[15].append(item)
				for i in xrange(gc.getNumTerrainInfos()):
					if ItemInfo.isTerrainTrade(i):
						lTerrain[i].append(item)
				for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
					if ItemInfo.isCommerceFlexible(i):
						lCommerce[i].append(item)
				for i in xrange(gc.getNumReligionInfos()):
					if gc.getReligionInfo(i).getTechPrereq() == item[1]:
						lReligion.append(item)

			if lReligion:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), "", lReligion])
			for i in xrange(len(lSpecial)):
				lList = lSpecial[i]
				if lList:
					lSorted.append([self.lSpecial[i], "", lList])
			lTemp = []
			for i in xrange(len(lTerrain)):
				lList = lTerrain[i]
				if lList:
					lTemp.append([gc.getTerrainInfo(i).getDescription() + " " + CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ()), "", lList])
			lTemp.sort()
			lSorted += lTemp
			lTemp = []
			for i in xrange(len(lCommerce)):
				lList = lCommerce[i]
				if lList:
					sInput = gc.getCommerceInfo(i).getDescription()
					lTemp.append([CyTranslator().getText("TXT_KEY_PEDIA_FLEXIBLE", (sInput,)), "", lList])
			lTemp.sort()
			lSorted += lTemp
		if iType > 0 and not lSorted[0][0]:
			lSorted[0][0] = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
		return lSorted

	def sortUnits(self, iType):
		lSorted = []
		lItems = []
		iActivePlayer = CyGame().getActivePlayer()
		for iItem in xrange(gc.getNumUnitInfos()):
			ItemInfo = gc.getUnitInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			sButton = ItemInfo.getButton()
			if CyGame().isFinalInitialized():
				if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY"):
					if not CyGame().isUnitEverActive(iItem): continue
				if iActivePlayer > -1:
					sButton = gc.getPlayer(iActivePlayer).getUnitButton(iItem)
			lItems.append([ItemInfo.getDescription(), iItem, sButton])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for i in xrange(len(lItems)):
				iItem = lItems[i][1]
				ItemInfo = gc.getUnitInfo(iItem)
				iCost = ItemInfo.getProductionCost()
				if iCost > -1 and not ItemInfo.isFound():
					if iActivePlayer > -1:
						iCost = gc.getActivePlayer().getUnitProductionNeeded(iItem)
				lItems[i].append(iCost)
			lItems = sorted(lItems, key = lambda x: x[3])
			lSorted = self.sortByCost(lItems)
		elif iType == 2:
			for iClass in xrange(-1, gc.getNumUnitCombatInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getUnitInfo(item[1])
					if ItemInfo.getUnitCombatType() == iClass:
						lTemp.append(item)
				if lTemp:
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					sDescription = ""
					if iClass > -1:
						sButton = gc.getUnitCombatInfo(iClass).getButton()
						sDescription = gc.getUnitCombatInfo(iClass).getDescription()
					lSorted.append([sDescription, sButton, lTemp])
			lSorted.sort()
		elif iType == 3:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getUnitInfo(item[1])
					iItemEra = -1
					iTech = ItemInfo.getPrereqAndTech()
					if iTech > -1:
						iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					for i in xrange(gc.getNUM_UNIT_AND_TECH_PREREQS()):
						iTech = ItemInfo.getPrereqAndTechs(i)
						if iTech > -1:
							iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					iItemEra = max(iItemEra, self.getBonusEra(ItemInfo.getPrereqAndBonus()))
					for i in xrange(gc.getNUM_UNIT_AND_TECH_PREREQS()):
						iItemEra = max(iItemEra, self.getBonusEra(ItemInfo.getPrereqOrBonuses(i)))
					iReligion = ItemInfo.getPrereqReligion()
					if iReligion > -1:
						iTech = gc.getReligionInfo(iReligion).getTechPrereq()
						if iTech > -1:
							iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					iCorporation = ItemInfo.getPrereqCorporation()
					if iCorporation > -1:
						for iBuilding in xrange(gc.getNumBuildingInfos()):
							BuildingInfo = gc.getBuildingInfo(iBuilding)
							if BuildingInfo.getFoundsCorporation() == iCorporation:
								iItemEra = max(iItemEra, self.getBuildingEra(iBuilding))
								break
					iBuilding = ItemInfo.getPrereqBuilding()
					if iBuilding > -1:
						iItemEra = max(iItemEra, self.getBuildingEra(iBuilding))
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 4:
			for iDomain in xrange(DomainTypes.NUM_DOMAIN_TYPES):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getUnitInfo(item[1])
					if ItemInfo.getDomainType() == iDomain:
						lTemp.append(item)
				if lTemp:
					lSorted.append([gc.getDomainInfo(iDomain).getDescription(), "", lTemp])
		elif iType == 5:
			lNormal = []
			lNational = []
			lTeam = []
			lWorld = []
			for item in lItems:
				ItemInfo = gc.getUnitInfo(item[1])
				iUnitClass = ItemInfo.getUnitClassType()
				if isNationalUnitClass(iUnitClass):
					lNational.append(item)
				elif isTeamUnitClass(iUnitClass):
					lTeam.append(item)
				elif isWorldUnitClass(iUnitClass):
					lWorld.append(item)
				else:
					lNormal.append(item)
			if lNormal:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()), "", lNormal])
			if lNational:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_UNIT", ()), "", lNational])
			if lTeam:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_TEAM_UNIT", ()), "", lTeam])
			if lWorld:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_WORLD_UNIT", ()), "", lWorld])
		elif iType == 6:
			for iAdvisor in xrange(-1, 6):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getUnitInfo(item[1])
					if ItemInfo.getAdvisorType() == iAdvisor:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					if iAdvisor > -1:
						sDescription = CyTranslator().getText(self.lAdvisors[iAdvisor], ())
					lSorted.append([sDescription, "", lTemp])
			lSorted.sort()
		elif iType == 7:
			for iSpecial in xrange(-1, gc.getNumSpecialUnitInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getUnitInfo(item[1])
					if ItemInfo.getSpecialUnitType() == iSpecial:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					if iSpecial > -1:
						sDescription = gc.getSpecialUnitInfo(iSpecial).getDescription()
					lSorted.append([sDescription, "", lTemp])
			lSorted.sort()
		if iType > 0 and not lSorted[0][0]:
			lSorted[0][0] = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
		return lSorted

	def sortUnitGroups(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumUnitCombatInfos()):
			ItemInfo = gc.getUnitCombatInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		return lSorted

	def sortPromotions(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumPromotionInfos()):
			ItemInfo = gc.getPromotionInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iClass in xrange(gc.getNumUnitCombatInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getPromotionInfo(item[1])
					if ItemInfo.getUnitCombat(iClass):
						lTemp.append(item)
				if lTemp:
					SortInfo = gc.getUnitCombatInfo(iClass)
					lSorted.append([SortInfo.getDescription(), SortInfo.getButton(), lTemp])
			lSorted.sort()
		elif iType == 2:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					iPreEra = -1
					ItemInfo = gc.getPromotionInfo(item[1])
					iTech = ItemInfo.getTechPrereq()
					if iTech > -1:
						iPreEra = gc.getTechInfo(iTech).getEra()
					if iPreEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		return lSorted

	def sortBuildings(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumBuildingInfos()):
			if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and CyGame().isFinalInitialized():
				if not CyGame().isBuildingEverActive(iItem): continue
			ItemInfo = gc.getBuildingInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			if isLimitedWonderClass(ItemInfo.getBuildingClassType()): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(len(lItems)):
				iItem = lItems[i][1]
				ItemInfo = gc.getBuildingInfo(iItem)
				iCost = ItemInfo.getProductionCost()
				if iCost > -1 and iActivePlayer > -1:
					iCost = gc.getActivePlayer().getBuildingProductionNeeded(iItem)
				lItems[i].append(iCost)
			lItems = sorted(lItems, key = lambda x: x[3])
			lSorted = self.sortByCost(lItems)
		elif iType == 2:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					if self.getBuildingEra(item[1]) == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 3:
			for iAdvisor in xrange(-1, 6):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getBuildingInfo(item[1])
					if ItemInfo.getAdvisorType() == iAdvisor:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					if iAdvisor > -1:
						sDescription = CyTranslator().getText(self.lAdvisors[iAdvisor], ())
					lSorted.append([sDescription, "", lTemp])
			lSorted.sort()
		elif iType == 4:
			for iVictory in xrange(-1, gc.getNumVictoryInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getBuildingInfo(item[1])
					if ItemInfo.getVictoryPrereq() == iVictory:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					if iVictory > -1:
						sDescription = gc.getVictoryInfo(iVictory).getDescription()
						sButton = gc.getVictoryInfo(iVictory).getButton()
					lSorted.append([sDescription, sButton, lTemp])
			lSorted.sort()
		elif iType == 5:
			for iSpecial in xrange(-1, gc.getNumSpecialBuildingInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getBuildingInfo(item[1])
					if ItemInfo.getSpecialBuildingType() == iSpecial:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					sButton = ""
					if iSpecial > -1:
						sDescription = gc.getSpecialBuildingInfo(iSpecial).getDescription()
						sButton = gc.getSpecialBuildingInfo(iSpecial).getButton()
					lSorted.append([sDescription, sButton, lTemp])
			lSorted.sort()
		if iType > 0 and not lSorted[0][0]:
			lSorted[0][0] = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
		return lSorted

	def sortWonders(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumBuildingInfos()):
			if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and CyGame().isFinalInitialized():
				if not CyGame().isBuildingEverActive(iItem): continue
			ItemInfo = gc.getBuildingInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			if isLimitedWonderClass(ItemInfo.getBuildingClassType()):
				lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == -1:
			lTemp = []
			for item in lItems:
				ItemInfo = gc.getBuildingInfo(item[1])
				if ItemInfo.getMovie():
					lTemp.append(item)
			lSorted.append([CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()), "", lTemp])
		elif iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(len(lItems)):
				iItem = lItems[i][1]
				ItemInfo = gc.getBuildingInfo(iItem)
				iCost = ItemInfo.getProductionCost()
				if iCost > -1 and iActivePlayer > -1:
					iCost = gc.getActivePlayer().getBuildingProductionNeeded(iItem)
				lItems[i].append(iCost)
			lItems = sorted(lItems, key = lambda x: x[3])
			lSorted = self.sortByCost(lItems)
		elif iType == 2:
			lNational = []
			lTeam = []
			lWorld = []
			for item in lItems:
				ItemInfo = gc.getBuildingInfo(item[1])
				iClass = ItemInfo.getBuildingClassType()
				if isNationalWonderClass(iClass):
					lNational.append(item)
				if isTeamWonderClass(iClass):
					lTeam.append(item)
				if isWorldWonderClass(iClass):
					lWorld.append(item)
			if lNational:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ()), "", lNational])
			if lTeam:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_TEAM_WONDER", ()), "", lTeam])
			if lWorld:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ()), "", lWorld])
		elif iType == 3:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					if self.getBuildingEra(item[1]) == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 4:
			for iUnitClass in xrange(-1, gc.getNumUnitClassInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getBuildingInfo(item[1])
					if ItemInfo.getGreatPeopleUnitClass() == iUnitClass:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					if iUnitClass > -1:
						iUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()
						if CyGame().isFinalInitialized():
							iUnit = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(iUnitClass)
						if iUnit > -1:
							sDescription = gc.getUnitInfo(iUnit).getDescription()
							sButton = gc.getUnitInfo(iUnit).getButton()
					lSorted.append([sDescription, sButton, lTemp])
		elif iType == 5:
			for iAdvisor in xrange(-1, 6):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getBuildingInfo(item[1])
					if ItemInfo.getAdvisorType() == iAdvisor:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					if iAdvisor > -1:
						sDescription = CyTranslator().getText(self.lAdvisors[iAdvisor], ())
					lSorted.append([sDescription, "", lTemp])
			lSorted.sort()
		elif iType == 6:
			for iVictory in xrange(-1, gc.getNumVictoryInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getBuildingInfo(item[1])
					if ItemInfo.getVictoryPrereq() == iVictory:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					if iVictory > -1:
						sDescription = gc.getVictoryInfo(iVictory).getDescription()
						sButton = gc.getVictoryInfo(iVictory).getButton()
					lSorted.append([sDescription, sButton, lTemp])
			lSorted.sort()
		if iType > 0 and not lSorted[0][0]:
			lSorted[0][0] = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
		return lSorted

	def sortProjects(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumProjectInfos()):
			ItemInfo = gc.getProjectInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == -1:
			lTemp = []
			for item in lItems:
				ItemInfo = gc.getProjectInfo(item[1])
				if not ItemInfo.getMovieArtDef(): continue
				lTemp.append(item)
			lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), "", lTemp])
		elif iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			iActivePlayer = CyGame().getActivePlayer()
			for i in xrange(len(lItems)):
				iItem = lItems[i][1]
				ItemInfo = gc.getProjectInfo(iItem)
				iCost = ItemInfo.getProductionCost()
				if iCost > -1 and iActivePlayer > -1:
					iCost = gc.getActivePlayer().getProjectProductionNeeded(iItem)
				lItems[i].append(iCost)
			lItems = sorted(lItems, key = lambda x: x[3])
			lSorted = self.sortByCost(lItems)
		elif iType == 2:
			lNormal = []
			lTeam = []
			lWorld = []
			for item in lItems:
				ItemInfo = gc.getProjectInfo(item[1])
				if isWorldProject(item[1]):
					lWorld.append(item)
				if isTeamProject(item[1]):
					lTeam.append(item)
				if not isWorldProject(item[1]) and not isTeamProject(item[1]):
					lNormal.append(item)
			if lNormal:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), "", lNormal])
			if lTeam:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_TEAM_PROJECT", ()), "", lTeam])
			if lWorld:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_WORLD_PROJECT", ()), "", lWorld])
		elif iType == 3:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getProjectInfo(item[1])
					iItemEra = -1
					iTech = ItemInfo.getTechPrereq()
					if iTech > -1:
						iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 4:
			for iVictory in xrange(-1, gc.getNumVictoryInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getProjectInfo(item[1])
					if ItemInfo.getVictoryPrereq() == iVictory:
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					if iVictory > -1:
						sDescription = gc.getVictoryInfo(iVictory).getDescription()
						sButton = gc.getVictoryInfo(iVictory).getButton()
					lSorted.append([sDescription, sButton, lTemp])
			lSorted.sort()
		if iType > 0 and not lSorted[0][0]:
			lSorted[0][0] = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
		return lSorted

	def sortProcesses(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumProcessInfos()):
			ItemInfo = gc.getProcessInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getProcessInfo(item[1])
					iItemEra = -1
					iTech = ItemInfo.getTechPrereq()
					if iTech > -1:
						iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 2:
			for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getProcessInfo(item[1])
					if ItemInfo.getProductionToCommerceModifier(iCommerce) > 0:
						lTemp.append(item)
				if lTemp:
					lItems = sorted(lItems, key = lambda x: gc.getProcessInfo(x[1]).getProductionToCommerceModifier(iCommerce))
					lSorted.append([gc.getCommerceInfo(iCommerce).getDescription(), gc.getCommerceInfo(iCommerce).getButton(), lTemp])
		return lSorted

	def sortTerrains(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumTerrainInfos()):
			ItemInfo = gc.getTerrainInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			lLand = []
			lSea = []
			for item in lItems:
				ItemInfo = gc.getTerrainInfo(item[1])
				if ItemInfo.isWater():
					lSea.append(item)
				else:
					lLand.append(item)
			sInput = CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN", ())
			if lLand:
				lSorted.append([CyTranslator().getText("TXT_PEDIA_LAND_STUFF", (sInput,)), "", lLand])
			if lSea:
				lSorted.append([CyTranslator().getText("TXT_PEDIA_SEA_STUFF", (sInput,)), "", lSea])
		return lSorted

	def sortFeatures(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumFeatureInfos()):
			ItemInfo = gc.getFeatureInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		return lSorted

	def sortBonus(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumBonusInfos()):
			ItemInfo = gc.getBonusInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			iBonusClass = 0
			while True:
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getBonusInfo(item[1])
					if ItemInfo.getBonusClassType() == iBonusClass:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL",())
					if iBonusClass > 0:
						sDescription = gc.getBonusClassInfo(iBonusClass).getType()
						sDescription = sDescription[sDescription.find("_") +1:]
						sDescription = sDescription.lower()
						sDescription = sDescription.capitalize()
					lSorted.append([sDescription, "", lTemp])
				iBonusClass += 1
				if gc.getBonusClassInfo(iBonusClass) == None: break
			lSorted.sort()
		elif iType == 2:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					iItemEra = self.getBonusEra(item[1])
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 3:
			lNone = []
			lLand = []
			lSea = []
			for item in lItems:
				ItemInfo = gc.getBonusInfo(item[1])
				bLand = False
				bSea = False
				for iTerrain in xrange(gc.getNumTerrainInfos()):
					if ItemInfo.isTerrain(iTerrain) or ItemInfo.isFeatureTerrain(iTerrain):
						if gc.getTerrainInfo(iTerrain).isWater():
							bSea = True
						else:
							bLand = True
				if bLand:
					lLand.append(item)
				if bSea:
					lSea.append(item)
				if not bLand and not bSea:
					lNone.append(item)
			sInput = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
			if lNone:
				lSorted.append([CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ()), "", lNone])
			if lLand:
				lSorted.append([CyTranslator().getText("TXT_PEDIA_LAND_STUFF", (sInput,)), "", lLand])
			if lSea:
				lSorted.append([CyTranslator().getText("TXT_PEDIA_SEA_STUFF", (sInput,)), "", lSea])
		elif iType == 4:
			for iCorporation in xrange(gc.getNumCorporationInfos()):
				lTemp = []
				for i in xrange(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
					iBonus = gc.getCorporationInfo(iCorporation).getPrereqBonus(i)
					if iBonus > -1:
						Info = gc.getBonusInfo(iBonus)
						lTemp.append([Info.getDescription(), iBonus, Info.getButton()])
				if lTemp:
					SortedInfo = gc.getCorporationInfo(iCorporation)
					lSorted.append([SortedInfo.getDescription(), SortedInfo.getButton(), lTemp])
			lSorted.sort()
		return lSorted

	def sortImprovements(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumImprovementInfos()):
			ItemInfo = gc.getImprovementInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					iItemEra = -1
					ItemInfo = gc.getImprovementInfo(item[1])
					for iBuild in xrange(gc.getNumBuildInfos()):
						if gc.getBuildInfo(iBuild).getImprovement() == item[1]:	 
							iTech = gc.getBuildInfo(iBuild).getTechPrereq()
							if iTech > -1:
								iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 2:
			lLand = []
			lSea = []
			for item in lItems:
				ItemInfo = gc.getImprovementInfo(item[1])
				if ItemInfo.isWater():
					lSea.append(item)
				else:
					lLand.append(item)
			sInput = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
			if lLand:
				lSorted.append([CyTranslator().getText("TXT_PEDIA_LAND_STUFF", (sInput,)), "", lLand])
			if lSea:
				lSorted.append([CyTranslator().getText("TXT_PEDIA_SEA_STUFF", (sInput,)), "", lSea])
		return lSorted

	def sortRoutes(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumRouteInfos()):
			ItemInfo = gc.getRouteInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			lItems = sorted(lItems, key = lambda x: gc.getRouteInfo(x[1]).getValue())
			lSorted.append(["", "", lItems])
		elif iType == 2:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getRouteInfo(item[1])
					iItemEra = -1
					for iBuild in xrange(gc.getNumBuildInfos()):
						if gc.getBuildInfo(iBuild).getRoute() == item[1]:	 
							iTech = gc.getBuildInfo(iBuild).getTechPrereq()
							if iTech > -1:
								iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		return lSorted

	def sortCivilizations(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumCivilizationInfos()):
			if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and CyGame().isFinalInitialized():
				if not CyGame().isCivEverActive(iItem): continue
			ItemInfo = gc.getCivilizationInfo(iItem)
			if not CyGame().isDebugMode():
				if ItemInfo.isGraphicalOnly(): continue
				if not ItemInfo.isPlayable(): continue
			lItems.append([ItemInfo.getShortDescription(0), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iArtStyle in xrange(gc.getNumArtStyleTypes()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getCivilizationInfo(item[1])
					if ItemInfo.getArtStyleType() == iArtStyle:
						lTemp.append(item)
				if lTemp:
					sText = gc.getArtStyleTypes(iArtStyle)
					sDescription = ""
					while len(sText):
						sText = sText[sText.find("_") +1:]
						sText = sText.lower()
						sText = sText.capitalize()
						if sText.find("_") == -1:
							sDescription += sText
							break
						else:
							sDescription += sText[:sText.find("_")] + " "
							sText = sText[sText.find("_") +1:]
					lSorted.append([sDescription, "", lTemp])
			lSorted.sort()
		elif iType == 2:
			for iTech in xrange(gc.getNumTechInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getCivilizationInfo(item[1])
					if ItemInfo.isCivilizationFreeTechs(iTech):
						lTemp.append(item)
				if lTemp:
					SortedInfo = gc.getTechInfo(iTech)
					lSorted.append([SortedInfo.getDescription(), SortedInfo.getButton(), lTemp])
			lSorted.sort()
		return lSorted

	def sortLeaders(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumLeaderHeadInfos()):
			if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and CyGame().isFinalInitialized():
				if not CyGame().isLeaderEverActive(iItem): continue
			ItemInfo = gc.getLeaderHeadInfo(iItem)
			if not CyGame().isDebugMode():
				if ItemInfo.isGraphicalOnly(): continue
				if iItem == gc.getDefineINT("BARBARIAN_LEADER"): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iCivilization in xrange(gc.getNumCivilizationInfos()):
				lTemp = []
				CivInfo = gc.getCivilizationInfo(iCivilization)
				for item in lItems:
					if CivInfo.isLeaders(item[1]):
						lTemp.append(item)
				if lTemp:
					lSorted.append([CivInfo.getShortDescription(0), CivInfo.getButton(), lTemp])
		elif iType == 2:
			for iTrait in xrange(gc.getNumTraitInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getLeaderHeadInfo(item[1])
					if ItemInfo.hasTrait(iTrait):
						lTemp.append(item)
				if lTemp:
					lSorted.append([gc.getTraitInfo(iTrait).getDescription(), "", lTemp])
		elif iType == 3:
			for iCivic in xrange(-1, gc.getNumCivicInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getLeaderHeadInfo(item[1])
					if iCivic == ItemInfo.getFavoriteCivic():
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					if iCivic > -1:
						sDescription = gc.getCivicInfo(iCivic).getDescription()
						sButton = gc.getCivicInfo(iCivic).getButton()
					lSorted.append([sDescription, sButton, lTemp])
		if iType == 4:
			for iReligion in xrange(-1, gc.getNumReligionInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getLeaderHeadInfo(item[1])
					if iReligion == ItemInfo.getFavoriteReligion():
						lTemp.append(item)
				if lTemp:
					sDescription = ""
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					if iReligion > -1:
						sDescription = gc.getReligionInfo(iReligion).getDescription()
						sButton = gc.getReligionInfo(iReligion).getButton()
					lSorted.append([sDescription, sButton, lTemp])
		lSorted.sort()
		if iType > 0 and not lSorted[0][0]:
			lSorted[0][0] = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
		return lSorted

	def sortTraits(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumTraitInfos()):
			ItemInfo = gc.getTraitInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ""])
		if not lItems: return lSorted
		lItems.sort()
		lSorted.append(["", "", lItems])
		return lSorted

	def sortSpecialists(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumSpecialistInfos()):
			ItemInfo = gc.getSpecialistInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			lSpecialist = []
			lGreat = []
			for item in lItems:
				ItemInfo = gc.getSpecialistInfo(item[1])
				if ItemInfo.getType().find("GREAT_") > -1:
					lGreat.append(item)
				else:
					lSpecialist.append(item)
			if lSpecialist:
				lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ()), "", lSpecialist])
			if lGreat:
				lSorted.append([CyTranslator().getText("TXT_KEY_CONCEPT_GREAT_PEOPLE", ()), "", lGreat])
		return lSorted

	def sortReligions(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumReligionInfos()):
			ItemInfo = gc.getReligionInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == -1:
			lTemp = []
			for item in lItems:
				ItemInfo = gc.getReligionInfo(item[1])
				sMovie = ItemInfo.getMovieFile()
				if sMovie == "NONE" or not sMovie: continue
				lTemp.append(item)
			lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()), "", lTemp])
		elif iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					iItemEra = -1
					ItemInfo = gc.getReligionInfo(item[1])
					iTech = ItemInfo.getTechPrereq()
					if iTech > -1:
						iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		return lSorted

	def sortCorporations(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumCorporationInfos()):
			ItemInfo = gc.getCorporationInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == -1:
			lTemp = []
			for item in lItems:
				ItemInfo = gc.getCorporationInfo(item[1])
				sMovie = ItemInfo.getMovieFile()
				if sMovie == "NONE" or not sMovie: continue
				lTemp.append(item)
			lSorted.append([CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), "", lTemp])
		elif iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getCorporationInfo(item[1])
					iItemEra = -1
					iTech = ItemInfo.getTechPrereq()
					if iTech > -1:
						iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					for iBuilding in xrange(gc.getNumBuildingInfos()):
						BuildingInfo = gc.getBuildingInfo(iBuilding)
						if BuildingInfo.getFoundsCorporation() == item[1]:
							iItemEra = max(iItemEra, self.getBuildingEra(iBuilding))
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 2:
			Buildings = {}
			for iClass in xrange(gc.getNumBuildingClassInfos()):
				iBuilding = gc.getBuildingClassInfo(iClass).getDefaultBuildingIndex()
				if CyGame().isFinalInitialized():
					iBuilding = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationBuildings(iClass)
				if iBuilding > -1:
					iItem = gc.getBuildingInfo(iBuilding).getFoundsCorporation()
					if iItem > -1:
						ItemInfo = gc.getCorporationInfo(iItem)
						Buildings[iBuilding] = [ItemInfo.getDescription(), iItem, ItemInfo.getButton()]

			for iClass in xrange(gc.getNumUnitClassInfos()):
				iUnit = gc.getUnitClassInfo(iClass).getDefaultUnitIndex()
				if CyGame().isFinalInitialized():
					iUnit = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(iClass)
				if iUnit > -1:
					lTemp = []
					UnitInfo = gc.getUnitInfo(iUnit)
					for iBuilding in Buildings.keys():
						if UnitInfo.getBuildings(iBuilding) or UnitInfo.getForceBuildings(iBuilding):
							lTemp.append(Buildings[iBuilding])
					if lTemp:
						lTemp.sort()
						lSorted.append([UnitInfo.getDescription(), UnitInfo.getButton(), lTemp])
		elif iType == 3:
			for iBonus in xrange(gc.getNumBonusInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getCorporationInfo(item[1])
					for i in xrange(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
						iItemBonus = ItemInfo.getPrereqBonus(i)
						if iItemBonus == iBonus:
							lTemp.append(item)
							break
				if lTemp:
					sButton = gc.getBonusInfo(iBonus).getButton()
					sDescription = gc.getBonusInfo(iBonus).getDescription()
					lSorted.append([sDescription, sButton, lTemp])
			lSorted.sort()
		return lSorted

	def sortCivics(self, iType):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumCivicInfos()):
			ItemInfo = gc.getCivicInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		if iType == 0:
			lSorted.append(["", "", lItems])
		elif iType == 1:
			for iCivicOption in xrange(gc.getNumCivicOptionInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getCivicInfo(item[1])
					if ItemInfo.getCivicOptionType() == iCivicOption:
						lTemp.append(item)
				if lTemp:
					lSorted.append([gc.getCivicOptionInfo(iCivicOption).getDescription(), "", lTemp])
		elif iType == 2:
			for iEra in xrange(-1, gc.getNumEraInfos()):
				lTemp = []
				for item in lItems:
					iItemEra = -1
					ItemInfo = gc.getCivicInfo(item[1])
					iTech = ItemInfo.getTechPrereq()
					if iTech > -1:
						iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
					if iItemEra == iEra:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_MAIN_MENU_NONE", ())
					if iEra > -1:
						sDescription = gc.getEraInfo(iEra).getDescription()
					lSorted.append([sDescription, "", lTemp])
		elif iType == 3:
			for iUpkeep in xrange(-1, gc.getNumUpkeepInfos()):
				lTemp = []
				for item in lItems:
					ItemInfo = gc.getCivicInfo(item[1])
					if ItemInfo.getUpkeep() == iUpkeep:
						lTemp.append(item)
				if lTemp:
					sDescription = CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
					if iUpkeep > -1:
						sDescription = gc.getUpkeepInfo(iUpkeep).getDescription()
					lSorted.append([sDescription, "", lTemp])
		return lSorted

	def sortCultureLevels(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumCultureLevelInfos()):
			ItemInfo = gc.getCultureLevelInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ""])
		if not lItems: return lSorted
		lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CULTURE_LEVEL", ()), "", lItems])
		return lSorted

	def sortGameSpeeds(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumGameSpeedInfos()):
			ItemInfo = gc.getGameSpeedInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, "", ItemInfo.getGoldenAgePercent()])
		if not lItems: return lSorted
		lItems = sorted(lItems, key = lambda x: x[3])
		lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_GAME_SPEED", ()), "", lItems])
		return lSorted

	def sortHandicaps(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumHandicapInfos()):
			ItemInfo = gc.getHandicapInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ""])
		if not lItems: return lSorted
		lSorted.append([CyTranslator().getText("TXT_KEY_PITBOSS_DIFFICULTY", ()), "", lItems])
		return lSorted

	def sortEra(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumEraInfos()):
			ItemInfo = gc.getEraInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ""])
		if not lItems: return lSorted
		lSorted.append([CyTranslator().getText("TXT_PEDIA_ERA", ()), "", lItems])
		return lSorted

	def sortUpkeep(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumUpkeepInfos()):
			ItemInfo = gc.getUpkeepInfo(iItem)
			if ItemInfo.isGraphicalOnly(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ""])
		lItems.insert(0, [CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ()), 999, ""])
		lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UPKEEP", ()), "", lItems])
		return lSorted

	def sortWorld(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumWorldInfos()):
			ItemInfo = gc.getWorldInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, "", ItemInfo.getGridWidth()])
		if not lItems: return lSorted
		lItems = sorted(lItems, key = lambda x: x[3])
		lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_WORLD", ()), "", lItems])
		return lSorted

	def sortConcepts(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumConceptInfos()):
			ItemInfo = gc.getConceptInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ""])
		if not lItems: return lSorted
		lItems.sort()
		lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()), "", lItems])
		return lSorted

	def sortNewConcepts(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumNewConceptInfos()):
			ItemInfo = gc.getNewConceptInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ""])
		if not lItems: return lSorted
		lItems.sort()
		lSorted.append([CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT_NEW", ()), "", lItems])
		return lSorted

	def sortVictories(self):
		lSorted = []
		lItems = []
		for iItem in xrange(gc.getNumVictoryInfos()):
			ItemInfo = gc.getVictoryInfo(iItem)
			if ItemInfo.isGraphicalOnly() and not CyGame().isDebugMode(): continue
			if not ItemInfo.getMovie(): continue
			lItems.append([ItemInfo.getDescription(), iItem, ItemInfo.getButton()])
		if not lItems: return lSorted
		lItems.sort()
		lSorted.append([CyTranslator().getText("TXT_KEY_CONCEPT_VICTORY", ()), "", lItems])
		return lSorted

	def getBonusEra(self, iBonus):
		iItemEra = -1
		if iBonus > -1:
			ItemInfo = gc.getBonusInfo(iBonus)
			iTech = ItemInfo.getTechReveal()
			if iTech > -1:
				iItemEra= max(iItemEra, gc.getTechInfo(iTech).getEra())
			iTech = ItemInfo.getTechCityTrade()
			if iTech > -1:
				iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
		return iItemEra

	def getBuildingEra(self, iBuilding):
		iItemEra = -1
		if iBuilding > -1:
			ItemInfo = gc.getBuildingInfo(iBuilding)
			iTech = ItemInfo.getPrereqAndTech()
			if iTech > -1:
				iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
			iSpecial = ItemInfo.getSpecialBuildingType()
			if iSpecial > -1:
				iTech = gc.getSpecialBuildingInfo(iSpecial).getTechPrereq()
				if iTech > -1:
					iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
			iReligion = ItemInfo.getPrereqReligion()
			if iReligion > -1:
				iTech = gc.getReligionInfo(iReligion).getTechPrereq()
				if iTech > -1:
					iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
			iReligion = ItemInfo.getHolyCity()
			if iReligion > -1:
				iTech = gc.getReligionInfo(iReligion).getTechPrereq()
				if iTech > -1:
					iItemEra = max(iItemEra, gc.getTechInfo(iTech).getEra())
			iItemEra = max(iItemEra, ItemInfo.getPrereqAndBonus())
			iTemp = 999999
			for i in xrange(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
				iBonus = ItemInfo.getPrereqOrBonuses(i)
				if iBonus > -1:
					iTemp = min(iTemp, self.getBonusEra(iBonus))
			if iTemp < 999999:
				iItemEra = max(iItemEra, iTemp)
		return iItemEra
################################		Sort Methods End		###############################