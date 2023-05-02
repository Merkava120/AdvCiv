from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvPediaScreen
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaTech(CvPediaScreen.CvPediaScreen):
	def __init__(self, main):
		self.iTech = -1
		self.top = main

	def interfaceScreen(self, iTech):		
		self.iTech = iTech
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_ICON = 150
		self.W_MAIN_PANE = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.H_MAIN_PANE = 210
		self.X_ICON = self.top.X_ITEMS_PANE + 30
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
		
		self.X_STATS_PANE = self.X_ICON + self.H_ICON
		self.Y_STATS_PANE = self.Y_ICON + self.H_ICON /4
		self.W_STATS_PANE = self.W_MAIN_PANE - self.H_ICON - self.top.W_BORDER * 2
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE

		self.X_PREREQ = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_PREREQ = self.top.Y_ITEMS_PANE - 20
		self.H_PREREQ = 110

		self.Y_LEADS_TO = self.Y_PREREQ + self.H_PREREQ + 10
		self.Y_UNIT_PANE = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_PREREQ
		self.Y_QUOTE = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_HISTORY = self.Y_UNIT_PANE - self.Y_QUOTE - 10
		self.H_SPECIAL = (self.H_HISTORY - 10) /2
		self.Y_SPECIAL = self.Y_QUOTE + self.H_SPECIAL + 10

		szHeader = gc.getTechInfo(self.iTech).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sTechIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sTechIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_TECH, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTechInfo(self.iTech).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.placeStats()		
		self.placePrereqs()
		self.placeLeadsTo()
		self.placeUnits()
		self.placeBuildings()
		self.placeSpecial()
		self.placeQuote()
		self.placeHistory()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_TECH and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_TECH

	def placeQuote(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_QUOTE", ()), "", true, true, self.top.X_ITEMS_PANE, self.Y_QUOTE, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50)
		szText = ""
		sQuote = gc.getTechInfo(self.iTech).getQuote()
		if sQuote.find("TXT_KEY") == -1:
			szText += sQuote
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.top.X_ITEMS_PANE + 10, self.Y_QUOTE + 30, self.W_MAIN_PANE - 20, self.H_SPECIAL - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		iEra = gc.getTechInfo(self.iTech).getEra()
		if iEra > -1:
			screen.appendListBoxString(panelName, "<font=4>" + CyTranslator().getText("TXT_KEY_PITBOSS_ERA", ()) + " " + gc.getEraInfo(iEra).getDescription() + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		if self.top.iActivePlayer == -1:
			sText = CyTranslator().getText("TXT_KEY_PEDIA_COST", ( gc.getTechInfo(self.iTech).getResearchCost(), ) ) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		else:
			sText = CyTranslator().getText("TXT_KEY_PEDIA_COST", ( gc.getTeam(CyGame().getActiveTeam()).getResearchCost(self.iTech), ) ) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.top.X_ITEMS_PANE, self.Y_ICON + self.H_ICON - 4, self.W_MAIN_PANE, 34, 1, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		for i in xrange(gc.getNumCivilizationInfos()):
			Info = gc.getCivilizationInfo(i)
			if Info.isGraphicalOnly(): continue
			if not Info.isPlayable(): continue
			if Info.isCivilizationFreeTechs(self.iTech):
				screen.appendMultiListButton(rowListName, Info.getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, i, 1, False)

	def placeLeadsTo(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_LEADS_TO", ()), "", false, true, self.X_PREREQ, self.Y_LEADS_TO, self.W_MAIN_PANE, self.H_PREREQ, PanelStyles.PANEL_STYLE_BLUE50 )
		for j in xrange(gc.getNumTechInfos()):
			for k in range(gc.getNUM_OR_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqOrTechs(k)
				if iPrereq == self.iTech:
        					screen.attachImageButton( panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )
			for k in range(gc.getNUM_AND_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqAndTechs(k)
				if iPrereq == self.iTech:
        					screen.attachImageButton( panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )

	def placePrereqs(self):
		screen = self.top.getScreen()
		szRequires = CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ())
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, szRequires, "", false, true, self.X_PREREQ, self.Y_PREREQ, self.W_MAIN_PANE, self.H_PREREQ, PanelStyles.PANEL_STYLE_BLUE50 )
		bFirst = True
		for j in xrange(gc.getNUM_AND_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqAndTechs(j)
			if eTech > -1:
				if bFirst:
					bFirst = False
				else:
					screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()))
				screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False )

		nOrTechs = 0
		for j in xrange(gc.getNUM_OR_TECH_PREREQS()):
			if gc.getTechInfo(self.iTech).getPrereqOrTechs(j) > -1:
				nOrTechs += 1

		szRightDelimeter = ""
		if not bFirst:
			if nOrTechs > 1:
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()) + "( ")
				szRightDelimeter = " ) "
			elif nOrTechs > 0:
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()))
			else:
				return
			
		bFirst = True
		for j in xrange(gc.getNUM_OR_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqOrTechs(j)
			if eTech > -1:
				if bFirst:
					bFirst = False
				else:
					screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_OR", ()))
				screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False )					
			
		if len(szRightDelimeter):
			screen.attachLabel(panelName, "", szRightDelimeter)

	def placeUnits(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_UNITS_ENABLED", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_UNIT_PANE, self.W_MAIN_PANE, self.H_PREREQ, PanelStyles.PANEL_STYLE_BLUE50 )
		for eLoopUnit in xrange(gc.getNumUnitInfos()):
			if isTechRequiredForUnit(self.iTech, eLoopUnit):
				szButton = gc.getUnitInfo(eLoopUnit).getButton()
				if self.top.iActivePlayer > -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(eLoopUnit)
				screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

	def placeBuildings(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_BUILDINGS_ENABLED", ()), "", false, true, self.X_PREREQ, self.Y_UNIT_PANE, self.W_MAIN_PANE, self.H_PREREQ, PanelStyles.PANEL_STYLE_BLUE50 )
		for eLoopBuilding in xrange(gc.getNumBuildingInfos()):
			if isTechRequiredForBuilding(self.iTech, eLoopBuilding):
        				screen.attachImageButton(panelName, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )
						
		for eLoopProject in xrange(gc.getNumProjectInfos()):
			if isTechRequiredForProject(self.iTech, eLoopProject):
        				screen.attachImageButton( panelName, "", gc.getProjectInfo(eLoopProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, eLoopProject, 1, False )

	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_SPECIAL, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().getTechHelp(self.iTech, True, False, False, False, -1)[1:]
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_SPECIAL+30, self.W_MAIN_PANE-10, self.H_SPECIAL-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeHistory(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, true, self.X_PREREQ, self.Y_QUOTE, self.W_MAIN_PANE, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		szText = ""
		sStrategy = gc.getTechInfo(self.iTech).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getTechInfo(self.iTech).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_PREREQ + 10, self.Y_QUOTE + 30, self.W_MAIN_PANE - 20, self.H_HISTORY - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortTechs(self.top.iSortTechs)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sTechIcon, ()), self.iTech, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, -1)

	def handleInput (self, inputClass):
		return 0