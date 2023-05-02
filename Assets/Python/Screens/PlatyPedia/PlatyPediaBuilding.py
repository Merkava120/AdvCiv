from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaBuilding:
	def __init__(self, main):
		self.iBuilding = -1
		self.top = main
		
	def interfaceScreen(self, iBuilding):	
		self.iBuilding = iBuilding
		self.top.deleteAllWidgets()										
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()
                
		self.H_ICON = 150
		self.W_MAIN_PANE = screen.getXResolution() * 2/5
		self.H_MAIN_PANE = 210
		self.X_ICON = self.top.X_ITEMS_PANE + 30
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
                
		self.X_STATS_PANE = self.X_ICON + self.H_ICON
		self.Y_STATS_PANE = self.Y_ICON + self.H_ICON /4
		self.W_STATS_PANE = self.W_MAIN_PANE - self.H_ICON - self.top.W_BORDER * 2
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE
		
		self.X_ANIMATION = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_ANIMATION = self.top.Y_ITEMS_PANE + 8
		self.W_ANIMATION = self.top.W_ITEMS_PANE - self.top.W_BORDER - self.W_MAIN_PANE
		self.H_ANIMATION = self.H_MAIN_PANE - 10
		self.X_ROTATION_ANIMATION = -20
		self.Z_ROTATION_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0

		self.Y_PREREQ_PANE = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_PREREQ_PANE = 110
		self.Y_SPECIAL_PANE = self.Y_PREREQ_PANE + self.H_PREREQ_PANE + 10
		self.H_SPECIAL_PANE = screen.getYResolution() - self.Y_SPECIAL_PANE - self.top.Y_ITEMS_PANE
		self.H_HISTORY_PANE = screen.getYResolution() - self.Y_PREREQ_PANE - self.top.Y_ITEMS_PANE
		
		link = self.top.PLATYPEDIA_BUILDING
		sIcon = self.top.sBuildingIcon
		if isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):
			link = self.top.PLATYPEDIA_WONDER
			sIcon = self.top.sWonderIcon

		szHeader = gc.getBuildingInfo(self.iBuilding).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(sIcon, ()) + szHeader + " " + CyTranslator().getText(sIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, link, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBuildingInfo(self.iBuilding).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addBuildingGraphicGFC(self.top.getNextWidgetName(), self.iBuilding, self.X_ANIMATION, self.Y_ANIMATION, self.W_ANIMATION, self.H_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_ANIMATION, self.Z_ROTATION_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()
		self.placeRequires()
		self.placeSpecial()
		self.placeHistory()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_BUILDING and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_BUILDING

	def placeStats(self):
		screen = self.top.getScreen()	
		buildingInfo = gc.getBuildingInfo(self.iBuilding)
		
		if isWorldWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxGlobalInstances()
			szType = CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ())
			if iMaxInstances > 1:
				szType += " " + CyTranslator().getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
			screen.setLabel(self.top.getNextWidgetName(), "", u"<font=4>" + szType + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 8,  self.Y_STATS_PANE - 28, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		elif isTeamWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxTeamInstances()
			szType = CyTranslator().getText("TXT_KEY_PEDIA_TEAM_WONDER", ())
			if iMaxInstances > 1:
				szType += " " + CyTranslator().getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
			screen.setLabel(self.top.getNextWidgetName(), "", u"<font=4>" + szType + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 8,  self.Y_STATS_PANE - 28, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		elif isNationalWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxPlayerInstances()
			szType = CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ())
			if iMaxInstances > 1:
				szType += " " + CyTranslator().getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
			screen.setLabel(self.top.getNextWidgetName(), "", u"<font=4>" + szType + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 8,  self.Y_STATS_PANE - 28, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		if buildingInfo.getProductionCost() > 0:
			if self.top.iActivePlayer == -1:
				sText = CyTranslator().getText("TXT_KEY_PEDIA_COST", ((buildingInfo.getProductionCost() * gc.getDefineINT("BUILDING_PRODUCTION_PERCENT"))/100,))
			else:
				sText = CyTranslator().getText("TXT_KEY_PEDIA_COST", (gc.getPlayer(self.top.iActivePlayer).getBuildingProductionNeeded(self.iBuilding),))
			sText += u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
			screen.appendListBoxString(panelName, "<font=4>" + sText + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		sText = ""
		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			if buildingInfo.getYieldChange(k) != 0:
				sText += u"%+d%c" % (buildingInfo.getYieldChange(k), gc.getYieldInfo(k).getChar())
		if len(sText):
			sText = "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_YIELDS", ()) + ": " + sText + "</font>"
			screen.appendListBoxString(panelName, sText, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
			
		sText = ""
		for k in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			iTotalCommerce = buildingInfo.getObsoleteSafeCommerceChange(k) + buildingInfo.getCommerceChange(k)
			if iTotalCommerce != 0:
				sText += u"%+d%c" % (iTotalCommerce, gc.getCommerceInfo(k).getChar())
		if len(sText):
			sText = "<font=4>" + CyTranslator().getText("TXT_KEY_CONCEPT_COMMERCE", ()) + ": " + sText + "</font>"
			screen.appendListBoxString(panelName, sText, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		sText = ""
		iHappiness = buildingInfo.getHappiness()
		if self.top.iActivePlayer != -1:
			if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
				iHappiness += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHappiness(self.iBuilding)
		if iHappiness > 0:
			sText += u"%+d%c" % (iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
		elif iHappiness < 0:
			sText += u"%+d%c" % (- iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

		iHealth = buildingInfo.getHealth()
		if self.top.iActivePlayer != -1:
			if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
				iHealth += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHealth(self.iBuilding)
		if iHealth > 0:
			sText += u"%+d%c" % (iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
		elif iHealth < 0:
			sText += u"%+d%c" % (-iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

		iGreat = buildingInfo.getGreatPeopleRateChange()
		if iGreat != 0:
			sText += u"%+d%c" % (iGreat, CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR))
		if len(sText):
			sText = "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()) + ": " + sText + "</font>"
			screen.appendListBoxString(panelName, sText, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_PREREQ_PANE, self.W_MAIN_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		Info = gc.getBuildingInfo(self.iBuilding)
		for iPrereq in xrange(gc.getNumTechInfos()):
			if isTechRequiredForBuilding(iPrereq, self.iBuilding):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )

		iPrereq = Info.getPrereqAndBonus()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )
			
		for k in xrange(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
			iPrereq = Info.getPrereqOrBonuses(k)
			if iPrereq > -1:
				screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )
		
		iCorporation = Info.getFoundsCorporation()
		bFirst = true
		if iCorporation > -1:
			for k in xrange(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
				iPrereq = gc.getCorporationInfo(iCorporation).getPrereqBonus(k)
				if iPrereq > -1:
					if not bFirst:
						screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_OR", ()))
					else:
						bFirst = false
					screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		iPrereq = Info.getPrereqReligion()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, -1, False )

		iPrereq = Info.getPrereqCorporation()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getCorporationInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, iPrereq, -1, False )
## Coastal and Rivers ##
		if Info.isRiver():
			screen.attachImageButton(panelName, "", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_RIVER_PLACEMENT").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PYTHON, 6783, -1, CvUtil.FONT_LEFT_JUSTIFY)
		if Info.isWater():
			item = gc.getInfoTypeForString("TERRAIN_COAST")
			screen.attachImageButton(panelName, "", gc.getTerrainInfo(item).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, item, 1, False)

	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_SPECIAL_PANE, self.W_MAIN_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		listName = self.top.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getBuildingHelp(self.iBuilding, True, False, False, None)[1:]
## Vote Effects ##
		BuildingInfo = gc.getBuildingInfo(self.iBuilding)
		iVoteSource = BuildingInfo.getVoteSourceType()
		if iVoteSource > -1:
			bFirst = True
			VoteSourceInfo = gc.getVoteSourceInfo(iVoteSource)
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = VoteSourceInfo.getReligionYield(k)
				if (iYieldChange != 0):
					if bFirst:
						szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_VOTESOURCE_RELIGION",())
						bFirst = False
					szSpecialText += (u"%i%c" % (iYieldChange, gc.getYieldInfo(k).getChar()))
			for k in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				iCommerceChange = VoteSourceInfo.getReligionCommerce(k)
				if (iCommerceChange != 0):
					if bFirst:
						szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_VOTESOURCE_RELIGION",())
						bFirst = False
					szSpecialText += (u"%i%c" % (iCommerceChange, gc.getCommerceInfo(k).getChar()))
## Vote Effects ##
## State Religion Requirement ##
		iStateReligion = BuildingInfo.getStateReligion()
		if iStateReligion > -1:
			szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_UNIT_STATE_RELIGION", (gc.getReligionInfo(iStateReligion).getDescription(),))
## State Religion Requirement ##
		screen.addMultilineText(listName, szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_SPECIAL_PANE+30, self.W_MAIN_PANE-10, self.H_SPECIAL_PANE-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

	def placeHistory(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_ANIMATION, self.Y_PREREQ_PANE, self.W_ANIMATION, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getBuildingInfo(self.iBuilding).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getBuildingInfo(self.iBuilding).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_ANIMATION + 10, self.Y_PREREQ_PANE + 30, self.W_ANIMATION - 20, self.H_HISTORY_PANE - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)

		if isLimitedWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()):
			listSorted = self.top.sortWonders(self.top.iSortWonders)
			sIcon = self.top.sWonderIcon
		else:
			listSorted = self.top.sortBuildings(self.top.iSortBuildings)
			sIcon = self.top.sBuildingIcon
		self.top.placePediaLinks(listSorted, CyTranslator().getText(sIcon, ()), self.iBuilding, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, -1)

	def handleInput (self, inputClass):
		return 0