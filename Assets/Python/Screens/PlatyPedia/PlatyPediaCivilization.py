from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaCivilization:
	def __init__(self, main):
		self.iCivilization = -1
		self.top = main
		self.bDisplayCivic = False
		for iOption in xrange(gc.getNumCivicOptionInfos()):
			for i in xrange(1, gc.getNumCivilizationInfos()):
				if gc.getCivilizationInfo(i).getCivilizationInitialCivics(iOption) != gc.getCivilizationInfo(i - 1).getCivilizationInitialCivics(iOption):
					self.bDisplayCivic = True
					break
			if self.bDisplayCivic:
				break
		
	def interfaceScreen(self, iCivilization):
		self.iCivilization = iCivilization
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_ICON = 150
		self.H_MAIN_PANE = 210
		self.X_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.X_ITEMS_PANE
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE

		self.X_BUILDING = self.top.X_ITEMS_PANE + self.H_MAIN_PANE + 20
		self.Y_BUILDING = self.top.Y_ITEMS_PANE - 20
		self.W_BUILDING = (self.top.W_ITEMS_PANE - self.H_MAIN_PANE - self.top.W_BORDER * 2)/2
		self.H_UNIT = 110
		self.Y_UNIT = self.Y_BUILDING + self.H_UNIT + 10
		self.X_TECH = self.X_BUILDING + self.W_BUILDING+ 20
		self.Y_CITIES = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_CITIES = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_CITIES
		self.Y_TEXT = self.Y_CITIES + self.H_UNIT + 10
		self.W_TEXT = self.top.W_ITEMS_PANE - self.H_MAIN_PANE - self.top.W_BORDER
		self.H_TEXT = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_TEXT

		szHeader = gc.getCivilizationInfo(self.iCivilization).getShortDescription(0).upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sCivIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sCivIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_CIV, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.H_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), CyArtFileMgr().getCivilizationArtInfo(gc.getCivilizationInfo(self.iCivilization).getArtDefineTag()).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		if self.bDisplayCivic:	
			self.placeCivics()
		else:
			self.H_TEXT = self.H_CITIES
			self.Y_TEXT = self.Y_CITIES
		self.placeCities()
		self.placeTech()
		self.placeBuilding()
		self.placeUnit()
		self.placeLeader()
		self.placeText()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_CIVILIZATION and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_CIVILIZATION

	def placeCities(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), "", True, True, self.top.X_ITEMS_PANE, self.Y_CITIES, self.H_MAIN_PANE, self.H_CITIES, PanelStyles.PANEL_STYLE_BLUE50 )
		Info = gc.getCivilizationInfo(self.iCivilization)
		szText = ""
		for i in xrange(Info.getNumCityNames()):
			if i == 0:
				szText += CyTranslator().getText("[ICON_STAR]", ())
			else:
				szText += "\n" + CyTranslator().getText("[ICON_BULLET]", ())
			szText += CyTranslator().getText(Info.getCityNames(i), ())
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.top.X_ITEMS_PANE + 10, self.Y_CITIES + 30, self.H_MAIN_PANE - 20, self.H_CITIES - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeCivics(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_CONCEPT_CIVICS", ()), "", False, True, self.X_BUILDING, self.Y_CITIES, self.W_TEXT, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50 )
		for iOption in xrange(gc.getNumCivicOptionInfos()):
			iCivic = gc.getCivilizationInfo(self.iCivilization).getCivilizationInitialCivics(iOption)
			screen.attachImageButton(panelName, "", gc.getCivicInfo(iCivic).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1, False )
	
	def placeTech(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_FREE_TECHS", ()), "", False, True, self.X_TECH, self.Y_UNIT, self.W_BUILDING, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50 )
		for iTech in xrange(gc.getNumTechInfos()):
			if gc.getCivilizationInfo(self.iCivilization).isCivilizationFreeTechs(iTech):
				screen.attachImageButton(panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
	
	def placeBuilding(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_UNIQUE_BUILDINGS", ()), "", False, True, self.X_BUILDING, self.Y_BUILDING, self.W_BUILDING, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50 )
		for iBuilding in xrange(gc.getNumBuildingClassInfos()):
			iUniqueBuilding = gc.getCivilizationInfo(self.iCivilization).getCivilizationBuildings(iBuilding)
			iDefaultBuilding = gc.getBuildingClassInfo(iBuilding).getDefaultBuildingIndex()
			if iUniqueBuilding > -1 and iDefaultBuilding != iUniqueBuilding:
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(iUniqueBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iUniqueBuilding, 1, False )
				
	def placeUnit(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_FREE_UNITS", ()), "", False, True, self.X_BUILDING, self.Y_UNIT, self.W_BUILDING, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50 )
		for iUnit in xrange(gc.getNumUnitClassInfos()):
			iUniqueUnit = gc.getCivilizationInfo(self.iCivilization).getCivilizationUnits(iUnit)
			iDefaultUnit = gc.getUnitClassInfo(iUnit).getDefaultUnitIndex()
			if iUniqueUnit > -1 and iDefaultUnit != iUniqueUnit:
				szButton = gc.getUnitInfo(iUniqueUnit).getButton()
				if self.top.iActivePlayer != -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(iUniqueUnit)
				screen.attachImageButton( panelName, "", gc.getUnitInfo(iUniqueUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUniqueUnit, 1, False )
		
	def placeLeader(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_CONCEPT_LEADERS", ()), "", False, True, self.X_TECH, self.Y_BUILDING, self.W_BUILDING, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50 )
		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			if gc.getCivilizationInfo(self.iCivilization).isLeaders(iLeader):
				screen.attachImageButton( panelName, "", gc.getLeaderHeadInfo(iLeader).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, self.iCivilization, False )
		
	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_BUILDING, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getCivilizationInfo(self.iCivilization).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		szText += gc.getCivilizationInfo(self.iCivilization).getCivilopedia()		
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_BUILDING + 10, self.Y_TEXT + 30, self.W_TEXT - 20, self.H_TEXT - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortCivilizations(self.top.iSortCivilizations)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sCivIcon, ()), self.iCivilization, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, -1)

	def handleInput (self, inputClass):
		return 0