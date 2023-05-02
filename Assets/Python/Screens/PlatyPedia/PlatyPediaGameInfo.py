from CvPythonExtensions import *
import CvUtil
import ScreenInput
gc = CyGlobalContext()

class CvPediaGameInfo:
	def __init__(self, main):
		self.top = main
		self.iType = -1
		self.iEntry = -1
		self.sIcon = ""

	def interfaceScreen(self, iType, iEntry):
		self.iType = iType
		self.iEntry = iEntry

		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_REQUIRES = 110
		self.Y_REQUIRES = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_REQUIRES# - 10

		self.W_CONCEPT = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.X_CONCEPT = self.top.X_ITEMS_PANE + self.W_CONCEPT + self.top.W_BORDER
		self.Y_CONCEPT = self.top.Y_ITEMS_PANE - 20
		self.H_CONCEPT = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_CONCEPT
		self.H_SHORTCONCEPT = self.H_CONCEPT - self.H_REQUIRES - 10

		if self.iType == 6791:
			self.placeCultureLevelSpecial()
			self.sIcon = "[ICON_CULTURE] "
			sDescription =gc.getCultureLevelInfo(iEntry).getDescription()
		elif self.iType == 6792:
			self.placeGameSpeedSpecial()
			self.sIcon = "[ICON_MOVES] "
			sDescription =gc.getGameSpeedInfo(iEntry).getDescription()
		elif self.iType == 6793:
			self.placeHandicapSpecial()
			self.sIcon = "[ICON_OCCUPATION] "
			sDescription =gc.getHandicapInfo(iEntry).getDescription()
		elif self.iType == 6795:
			self.placeStartEraSpecial()
			self.sIcon = "[ICON_RESEARCH] "
			sDescription =gc.getEraInfo(iEntry).getDescription()
		elif self.iType == 6796:
			self.placeUpkeepSpecial()
			self.sIcon = "[ICON_GOLD] "
			if self.iEntry == 999:
				sDescription = CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
			else:
				sDescription =gc.getUpkeepInfo(iEntry).getDescription()
		elif self.iType == 6797:
			self.placeWorldSpecial()
			self.sIcon = "[ICON_MAP] "
			sDescription =gc.getWorldInfo(iEntry).getDescription()

		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.sIcon, ()) + sDescription.upper() + " " + CyTranslator().getText(self.sIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_GAME_INFO, -1)
		self.placeLinks(self.top.iLastScreen == self.top.PLATYPEDIA_GAME_INFO and screen.isActive())
		self.top.iLastScreen = self.top.PLATYPEDIA_GAME_INFO
		
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)

		listSorted0 = self.top.sortCultureLevels()
		listSorted1 = self.top.sortEra()
		listSorted2 = self.top.sortGameSpeeds()
		listSorted3 = self.top.sortHandicaps()
		listSorted4 = self.top.sortUpkeep()
		listSorted5 = self.top.sortWorld()

		Icon1 = CyTranslator().getText(self.top.sGameInfoIcon, ())
		self.top.placePediaLinks(listSorted0, Icon1, self.iEntry, WidgetTypes.WIDGET_PYTHON, 6791, self.iType, CyTranslator().getText("[ICON_CULTURE] ", ()))
		iRow = screen.appendTableRow("PlatyTable")
		screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		self.top.placePediaLinks(listSorted1, Icon1, self.iEntry, WidgetTypes.WIDGET_PYTHON, 6795, self.iType, CyTranslator().getText("[ICON_RESEARCH] ", ()))
		iRow = screen.appendTableRow("PlatyTable")
		screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		self.top.placePediaLinks(listSorted2, Icon1, self.iEntry, WidgetTypes.WIDGET_PYTHON, 6792, self.iType, CyTranslator().getText("[ICON_MOVES] ", ()))
		iRow = screen.appendTableRow("PlatyTable")
		screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		self.top.placePediaLinks(listSorted3, Icon1, self.iEntry, WidgetTypes.WIDGET_PYTHON, 6793, self.iType, CyTranslator().getText("[ICON_OCCUPATION] ", ()))
		iRow = screen.appendTableRow("PlatyTable")
		screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		self.top.placePediaLinks(listSorted4, Icon1, self.iEntry, WidgetTypes.WIDGET_PYTHON, 6796, self.iType, CyTranslator().getText("[ICON_GOLD] ", ()))
		iRow = screen.appendTableRow("PlatyTable")
		screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		self.top.placePediaLinks(listSorted5, Icon1, self.iEntry, WidgetTypes.WIDGET_PYTHON, 6797, self.iType, CyTranslator().getText("[ICON_MAP] ", ()))
		iRow = screen.appendTableRow("PlatyTable")
		screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
	
	def placeCultureLevelSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_CONCEPT, self.W_CONCEPT, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		CultureLevelInfo = gc.getCultureLevelInfo(self.iEntry)
		szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + str(CultureLevelInfo.getCityDefenseModifier()) + "%" + CyTranslator().getText("[ICON_DEFENSE]", ()) + "\n\n"
		for iGameSpeed in xrange(gc.getNumGameSpeedInfos()):
			i = gc.getNumGameSpeedInfos() - iGameSpeed - 1
			GameSpeedInfo = gc.getGameSpeedInfo(i)
			szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + GameSpeedInfo.getDescription() + ": " + str(CultureLevelInfo.getSpeedThreshold(i)) + CyTranslator().getText("[ICON_CULTURE]", ()) + "\n"
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_CONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()), "", true, false, self.X_CONCEPT, self.Y_CONCEPT, self.W_CONCEPT, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		szText = CyTranslator().getText("TXT_KEY_CONCEPT_CULTURE_PEDIA", ())
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_CONCEPT+10, self.Y_CONCEPT+30, self.W_CONCEPT-20, self.H_CONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeGameSpeedSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_CONCEPT, self.W_CONCEPT, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		GameSpeedInfo = gc.getGameSpeedInfo(self.iEntry)
		szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_FOOD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_FOOD", ()) + ": " + str(GameSpeedInfo.getGrowthPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_RESEARCH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_RESEARCH", ()) + ": " + str(GameSpeedInfo.getResearchPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_CULTURE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CULTURE", ()) + ": " + str(GameSpeedInfo.getUnitGreatWorkPercent()) + "%\n"	## Fake
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_UNITS", ()) + ": " + str(GameSpeedInfo.getTrainPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_BUILDINGS", ()) + ": " + str(GameSpeedInfo.getConstructPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()) + ": " + str(GameSpeedInfo.getCreatePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_IMPROVEMENTS", ()) + ": " + str(GameSpeedInfo.getBuildPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_POWER]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_UPGRADE", ()) + ": " + str(GameSpeedInfo.getImprovementPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ()) + ": " + str(GameSpeedInfo.getFeatureProductionPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLDENAGE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_GOLDEN_AGE", ()) + ": " + str(GameSpeedInfo.getGoldenAgePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_UNHAPPY]", ()) + CyTranslator().getText("TXT_KEY_WB_ANARCHY", (GameSpeedInfo.getAnarchyPercent(),)) + "%\n"
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_CONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.X_CONCEPT, self.Y_CONCEPT, self.W_CONCEPT, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GREATPEOPLE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_GREAT_PEOPLE", ()) + ": " + str(GameSpeedInfo.getGreatPeoplePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GREATPEOPLE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_RESEARCH", ()) + ": " + str(GameSpeedInfo.getUnitDiscoverPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GREATPEOPLE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_HURRY_PRODUCTION", ()) + ": " + str(GameSpeedInfo.getUnitHurryPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GREATPEOPLE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ()) + ": " + str(GameSpeedInfo.getUnitTradePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GREATPEOPLE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CULTURE", ()) + ": " + str(GameSpeedInfo.getUnitGreatWorkPercent()) + "%\n"
		szSpecialText += "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_OCCUPATION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_BARBARIANS", ()) + ": " + str(GameSpeedInfo.getBarbPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_HURRY_PRODUCTION", ()) + ": " + str(GameSpeedInfo.getHurryPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_UNHAPPY]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_HURRY_PRODUCTION", ()) + ", " + CyTranslator().getText("TXT_KEY_CONCEPT_DRAFT", ()) + ": " + str(GameSpeedInfo.getHurryConscriptAngerPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_INFLATION", ()) + ": " + str(GameSpeedInfo.getInflationPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_INFLATION_OFFSET", ()) + ": " + str(GameSpeedInfo.getInflationOffset()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_POWER]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_VICTORY_DELAY", ()) + ": " + str(GameSpeedInfo.getVictoryDelayPercent()) + "%\n"
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_CONCEPT+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_CONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeHandicapSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_CONCEPT, self.W_CONCEPT, self.H_SHORTCONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		HandicapInfo = gc.getHandicapInfo(self.iEntry)
		szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_DEFENSE", ()) + ": " + str(HandicapInfo.getStartingDefenseUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_UNIT_EXPLORER", ()) + ": " + str(HandicapInfo.getStartingExploreUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_UNIT_WORKER", ()) + ": " + str(HandicapInfo.getStartingWorkerUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_ANIMALS", ()) + ": " + str(HandicapInfo.getAnimalCombatModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_BARBARIANS", ()) + ": " + str(HandicapInfo.getBarbarianCombatModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getDescription() + ": " + str(HandicapInfo.getStartingGold()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_UNITS", ()) + ": " + str(HandicapInfo.getUnitCostPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_RESEARCH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_RESEARCH", ()) + ": " + str(HandicapInfo.getResearchPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_DISTANCE", ()) + ": " + str(HandicapInfo.getDistanceMaintenancePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()) + ": " + str(HandicapInfo.getNumCitiesMaintenancePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_COLONIES", ()) + ": " + str(HandicapInfo.getColonyMaintenancePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()) + ": " + str(HandicapInfo.getCorporationMaintenancePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UPKEEP", ()) + ": " + str(HandicapInfo.getCivicUpkeepPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_INFLATION", ()) + ": " + str(HandicapInfo.getInflationPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_HEALTHY]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_HEALTH", ()) + ": " + str(HandicapInfo.getHealthBonus()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_HAPPY]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_HAPPINESS", ()) + ": " + str(HandicapInfo.getHappyBonus()) + "\n"
		szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_HANDICAP_ATTITUDE",(HandicapInfo.getAttitudeChange(),))
		szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_HANDICAP_BARB_FREE_WINS",(HandicapInfo.getFreeWinsVsBarbs(),))
		szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_HANDICAP_FREE_UNITS",(HandicapInfo.getFreeUnits(),))
		szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_HANDICAP_BARB_INITIAL_UNITS",(HandicapInfo.getBarbarianInitialDefenders(),))
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_SHORTCONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.addPanel(self.top.getNextWidgetName(), "A.I.", "", true, false, self.X_CONCEPT, self.Y_CONCEPT, self.W_CONCEPT, self.H_SHORTCONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_DEFENSE", ()) + ": " + str(HandicapInfo.getAIStartingDefenseUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_UNIT_EXPLORER", ()) + ": " + str(HandicapInfo.getAIStartingExploreUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_UNIT_WORKER", ()) + ": " + str(HandicapInfo.getAIStartingWorkerUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_ANIMALS", ()) + ": " + str(HandicapInfo.getAIAnimalCombatModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_BARBARIANS", ()) + ": " + str(HandicapInfo.getAIBarbarianCombatModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_FOOD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_FOOD", ()) + ": " + str(HandicapInfo.getAIGrowthPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_UNITS", ()) + ": " + str(HandicapInfo.getAITrainPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_WORLD_UNIT", ()) + ": " + str(HandicapInfo.getAIWorldTrainPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_BUILDINGS", ()) + ": " + str(HandicapInfo.getAIConstructPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ()) + ": " + str(HandicapInfo.getAIWorldConstructPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()) + ": " + str(HandicapInfo.getAICreatePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_WORLD_PROJECT", ()) + ": " + str(HandicapInfo.getAIWorldCreatePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_IMPROVEMENTS", ()) + ": " + str(HandicapInfo.getAIWorkRateModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UPKEEP", ()) + ": " + str(HandicapInfo.getAICivicUpkeepPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_UNITS", ()) + ": " + str(HandicapInfo.getAIUnitCostPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_SUPPLY", ()) + ": " + str(HandicapInfo.getAIUnitSupplyPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_UPGRADE", ()) + ": " + str(HandicapInfo.getAIUnitUpgradePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_INFLATION", ()) + ": " + str(HandicapInfo.getAIInflationPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_OCCUPATION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WAR", ()) + ": " + str(HandicapInfo.getAIDeclareWarProb()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_OCCUPATION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WAR_WEARINESS", ()) + ": " + str(HandicapInfo.getAIWarWearinessPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_HANDICAP_PER_ERA_AI",(HandicapInfo.getAIPerEraModifier(),))
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_LATE_START", ()) + ": " + str(HandicapInfo.getAIAdvancedStartPercent()) + "%"
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText,  self.X_CONCEPT+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_SHORTCONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_FREE_TECHS", ()), "", false, true,  self.top.X_ITEMS_PANE, self.Y_REQUIRES, self.W_CONCEPT, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName2 = self.top.getNextWidgetName()
		screen.addPanel(panelName2, CyTranslator().getText("TXT_KEY_FREE_TECHS", ()), "", false, true, self.X_CONCEPT, self.Y_REQUIRES, self.W_CONCEPT, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )		
		for iTech in xrange(gc.getNumTechInfos()):
			if HandicapInfo.isFreeTechs(iTech):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			if HandicapInfo.isAIFreeTechs(iTech):
				screen.attachImageButton( panelName2, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

	def placeStartEraSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_CONCEPT, self.W_CONCEPT, self.H_SHORTCONCEPT - (self.H_REQUIRES + 10) * 2, PanelStyles.PANEL_STYLE_BLUE50 )	
		EraInfo = gc.getEraInfo(self.iEntry)
		szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_MULTIPLIER", ()) + ": " + str(EraInfo.getStartingUnitMultiplier()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_DEFENSE", ()) + ": " + str(EraInfo.getStartingDefenseUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_UNIT_EXPLORER", ()) + ": " + str(EraInfo.getStartingExploreUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_UNIT_WORKER", ()) + ": " + str(EraInfo.getStartingWorkerUnits()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getDescription() + ": " + str(EraInfo.getStartingGold()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_ANGRYPOP]", ()) + CyTranslator().getText("TXT_KEY_WB_POPULATION",()) + " " + str(EraInfo.getFreePopulation()) + "\n"
		if EraInfo.isNoGoodies():
			szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_GAME_OPTION_NO_GOODY_HUTS", ()) + "\n"
		if EraInfo.isNoAnimals():
			szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_MAIN_MENU_BARBARIANS_NO_ANIMALS", ()) + "\n"
		if EraInfo.isNoBarbUnits():
			szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_START_ERA_NO_BARB_UNITS",())
		if EraInfo.isNoBarbCities():
			szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_START_ERA_NO_BARB_CITY",())
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()) + ": " + str(EraInfo.getStartPercent()) + "%"
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_SHORTCONCEPT - (self.H_REQUIRES + 10) * 2 - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.X_CONCEPT, self.Y_CONCEPT, self.W_CONCEPT, self.H_SHORTCONCEPT - (self.H_REQUIRES + 10) * 2, PanelStyles.PANEL_STYLE_BLUE50 )	
		szSpecialText = ""
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_FOOD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_FOOD", ()) + ": " + str(EraInfo.getGrowthPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_UNITS", ()) + ": " + str(EraInfo.getTrainPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_BUILDINGS", ()) + ": " + str(EraInfo.getConstructPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()) + ": " + str(EraInfo.getCreatePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_RESEARCH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_RESEARCH", ()) + ": " + str(EraInfo.getResearchPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_IMPROVEMENTS", ()) + ": " + str(EraInfo.getBuildPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_POWER]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_UPGRADE", ()) + ": " + str(EraInfo.getImprovementPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GREATPEOPLE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_GREAT_PEOPLE", ()) + ": " + str(EraInfo.getGreatPeoplePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_CULTURE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CULTURE", ()) + ": " + str(EraInfo.getGreatPeoplePercent()) + "%\n"	## Fake
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_UNHAPPY]", ()) + CyTranslator().getText("TXT_KEY_WB_ANARCHY", (EraInfo.getAnarchyPercent(),)) + "%"
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_CONCEPT+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_SHORTCONCEPT - (self.H_REQUIRES + 10) * 2 - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_START_ERA_FREE_BUILDINGS", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES, self.top.W_ITEMS_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName2 = self.top.getNextWidgetName()
		screen.addPanel(panelName2, CyTranslator().getText("TXT_KEY_PEDIA_START_ERA_MAX_START_WONDERS", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES - self.H_REQUIRES - 10, self.top.W_ITEMS_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			BuildingInfo = gc.getBuildingInfo(iBuilding)
			if BuildingInfo.getFreeStartEra() == self.iEntry:
				screen.attachImageButton( panelName, "", BuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )
			if BuildingInfo.getMaxStartEra() == self.iEntry:
				screen.attachImageButton( panelName2, "", BuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES - (self.H_REQUIRES + 10) * 2, self.top.W_ITEMS_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		for iTech in xrange(gc.getNumTechInfos()):
			Info = gc.getTechInfo(iTech)
			if Info.getEra() == self.iEntry:
				screen.attachImageButton(panelName, "", Info.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)
		
	def placeUpkeepSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_CONCEPT, self.W_CONCEPT, self.H_SHORTCONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )
		if self.iEntry < 999:
			UpkeepInfo = gc.getUpkeepInfo(self.iEntry)
			szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES",()) + ": " + str(UpkeepInfo.getCityPercent()) + "%\n"
			szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_ANGRYPOP]", ()) + CyTranslator().getText("TXT_KEY_WB_POPULATION",()) + " " + str(UpkeepInfo.getPopulationPercent()) + "%\n"
			screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_SHORTCONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()), "", true, false, self.X_CONCEPT, self.Y_CONCEPT, self.W_CONCEPT, self.H_SHORTCONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		szText = CyTranslator().getText("TXT_KEY_CONCEPT_CIVICS_PEDIA", ())
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_CONCEPT +10, self.Y_CONCEPT+30, self.W_CONCEPT-20, self.H_SHORTCONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES, self.top.W_ITEMS_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		for iCivic in xrange(gc.getNumCivicInfos()):
			CivicInfo = gc.getCivicInfo(iCivic)
			if CivicInfo.getUpkeep() == self.iEntry or (self.iEntry == 999 and CivicInfo.getUpkeep() == -1):
				screen.attachImageButton( panelName, "", CivicInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1, False )

	def placeWorldSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_CONCEPT, self.W_CONCEPT, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		WorldInfo = gc.getWorldInfo(self.iEntry)
		szSpecialText = CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_MAP]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_GRID_WIDTH", ()) + ": " + str(WorldInfo.getGridWidth()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_MAP]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_GRID_HEIGHT", ()) + ": " + str(WorldInfo.getGridHeight()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_MAP]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_TERRAIN_GRAIN_CHANGE", ()) + ": " + str(WorldInfo.getTerrainGrainChange()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_MAP]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_FEATURE_GRAIN_CHANGE", ()) + ": " + str(WorldInfo.getFeatureGrainChange()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_ANGRYPOP]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_DEFAULT_PLAYERS", ()) + ": " + str(WorldInfo.getDefaultPlayers()) + "\n"
		szSpecialText += "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_HAPPY]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_FREE_BUILDING_BONUS", ()) + ": " + str(WorldInfo.getNumFreeBuildingBonuses()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_BUILDING_CLASS_PREREQ", ()) + ": " + str(WorldInfo.getBuildingClassPrereqModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_PRODUCTION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_TARGET_NUM_CITIES", ()) + ": " + str(WorldInfo.getTargetNumCities()) + "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_STRENGTH]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_UNIT_NAME", ()) + ": " + str(WorldInfo.getUnitNameModifier()) + "%\n"
		szSpecialText += "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_UNHAPPY]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_MAX_CONSCRIPT", ()) + ": " + str(WorldInfo.getMaxConscriptModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_UNHAPPY]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WAR_WEARINESS", ()) + ": " + str(WorldInfo.getWarWearinessModifier()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_UNHAPPY]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_NUM_CITIES_ANARCHY", ()) + ": " + str(WorldInfo.getNumCitiesAnarchyPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_RESEARCH]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_RESEARCH", ()) + ": " + str(WorldInfo.getResearchPercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_TRADE]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ()) + ": " + str(WorldInfo.getTradeProfitPercent()) + "%\n"
		szSpecialText += "\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_DISTANCE", ()) + ": " + str(WorldInfo.getDistanceMaintenancePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()) + ": " + str(WorldInfo.getNumCitiesMaintenancePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_COLONIES", ()) + ": " + str(WorldInfo.getColonyMaintenancePercent()) + "%\n"
		szSpecialText += CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()) + ": " + str(WorldInfo.getCorporationMaintenancePercent()) + "%\n"
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_CONCEPT+30, self.W_CONCEPT-30, self.H_CONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()), "", true, false, self.X_CONCEPT, self.Y_CONCEPT, self.W_CONCEPT, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		szText = CyTranslator().getText("TXT_KEY_CONCEPT_EXPLORATION_PEDIA", ())
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_CONCEPT+10, self.Y_CONCEPT+30, self.W_CONCEPT-20, self.H_CONCEPT-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)


	def handleInput (self, inputClass):
		return 0