from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaProject:
	def __init__(self, main):
		self.iProject = -1
		self.top = main
		
	def interfaceScreen(self, iProject):
		self.iProject = iProject
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
		self.W_STATS_PANE = self.top.X_ITEMS_PANE + self.W_MAIN_PANE - self.X_STATS_PANE + self.top.X_ITEMS_PANE
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE

		self.Y_REQUIRES = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE
		self.H_REQUIRES = 110

		self.Y_SPECIAL = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.H_SPECIAL = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_SPECIAL

		self.X_TEXT = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + 20
		self.Y_TEXT = self.top.Y_ITEMS_PANE - 20
		self.H_TEXT = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_TEXT

		szHeader = gc.getProjectInfo(self.iProject).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sProjectIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sProjectIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_PROJECT, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getProjectInfo(self.iProject).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.placeStats()
		self.placeRequires()
		self.placeSpecial()
		self.placeText()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_PROJECT and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_PROJECT

	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		projectInfo = gc.getProjectInfo(self.iProject)

		if isWorldProject(self.iProject):
			iMaxInstances = projectInfo.getMaxGlobalInstances()
			szProjectType = CyTranslator().getText("TXT_KEY_PEDIA_WORLD_PROJECT", ())
			if iMaxInstances > 1:
				szProjectType += "\n" + CyTranslator().getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
			screen.appendListBoxString(panelName, "<font=4>" + szProjectType + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		if isTeamProject(self.iProject):
			iMaxInstances = projectInfo.getMaxTeamInstances()
			szProjectType = CyTranslator().getText("TXT_KEY_PEDIA_TEAM_PROJECT", ())
			if iMaxInstances > 1:
				szProjectType += "\n" + CyTranslator().getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
			screen.appendListBoxString(panelName, "<font=4>" + szProjectType + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iCost = projectInfo.getProductionCost()
		if iCost:
			szCost = CyTranslator().getText("TXT_KEY_PEDIA_COST", (iCost * gc.getDefineINT("PROJECT_PRODUCTION_PERCENT")/100,))
			if self.top.iActivePlayer > -1:
				szCost = CyTranslator().getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getProjectProductionNeeded(self.iProject),))
			screen.appendListBoxString(panelName, "<font=4>" + szCost + u"%c</font>" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES, self.W_MAIN_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		iPrereq = gc.getProjectInfo(self.iProject).getTechPrereq()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )

	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_SPECIAL, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().getProjectHelp(self.iProject, True, None)[1:]
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_SPECIAL+30, self.W_MAIN_PANE-10, self.H_SPECIAL-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, true, self.X_TEXT, self.Y_TEXT, self.W_MAIN_PANE, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getProjectInfo(self.iProject).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getProjectInfo(self.iProject).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia	
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_TEXT + 10, self.Y_TEXT + 30, self.W_MAIN_PANE - 20, self.H_TEXT - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortProjects(self.top.iSortProjects)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sProjectIcon, ()), self.iProject, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, -1)

	def handleInput (self, inputClass):
		return 0