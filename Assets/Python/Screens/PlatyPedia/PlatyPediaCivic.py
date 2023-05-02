from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaCivic:

	def __init__(self, main):
		self.iCivic = -1
		self.top = main
		self.bDisplayAnarchy = False
		for i in xrange(1, gc.getNumCivicInfos()):
			if gc.getCivicInfo(i).getAnarchyLength() != gc.getCivicInfo(i - 1).getAnarchyLength():
				self.bDisplayAnarchy = True
				break
	
	def interfaceScreen(self, iCivic):
		self.iCivic = iCivic
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
		self.W_STATS_PANE = self.top.X_ITEMS_PANE + self.W_MAIN_PANE - self.X_STATS_PANE + self.top.X_ITEMS_PANE
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE

		self.Y_REQUIRES = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.W_REQUIRES = 75
		self.H_REQUIRES = 110

		self.X_SPECIAL = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_SPECIAL = self.top.Y_ITEMS_PANE - 20
		self.W_SPECIAL = self.top.W_ITEMS_PANE - self.W_MAIN_PANE - self.top.W_BORDER
		self.H_SPECIAL = self.H_MAIN_PANE + 20

		self.Y_TEXT = self.Y_REQUIRES+ self.H_REQUIRES + 10
		self.H_TEXT = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_TEXT

		self.X_LEADERS = self.top.X_ITEMS_PANE + self.W_REQUIRES + self.top.W_BORDER
		self.W_LEADERS = self.top.W_ITEMS_PANE - self.top.W_BORDER - self.W_REQUIRES

		szHeader = gc.getCivicInfo(self.iCivic).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sCivicIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sCivicIcon, ()) + "</color></font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_CIVIC, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getCivicInfo(self.iCivic).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.placeStats()
		self.placeSpecial()
		self.placeRequires()
		self.placeText()
		self.placeLeaders()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_CIVIC and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_CIVIC
		
	def placeLeaders(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()), "", false, true, self.X_LEADERS, self.Y_REQUIRES, self.W_LEADERS, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			LeaderInfo = gc.getLeaderHeadInfo(iLeader)
			if LeaderInfo.getFavoriteCivic() == self.iCivic:
				screen.attachImageButton( panelName, "", LeaderInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, 1, False )
				
	def placeStats(self):				
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		iCivicOptionType = gc.getCivicInfo(self.iCivic).getCivicOptionType()
		if iCivicOptionType > -1:
			screen.appendListBoxStringNoUpdate(panelName,  "<font=4>" + gc.getCivicOptionInfo(iCivicOptionType).getDescription().upper() + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		pUpkeepInfo = gc.getUpkeepInfo(gc.getCivicInfo(self.iCivic).getUpkeep())
		sText = CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
		if pUpkeepInfo:
			sText = pUpkeepInfo.getDescription()
		screen.appendListBoxStringNoUpdate(panelName,  "<font=4>" + sText.upper() + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		screen.updateListBox(panelName)

	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		iTech = gc.getCivicInfo(self.iCivic).getTechPrereq()
		if (iTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			

	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().parseCivicInfo(self.iCivic, True, False, True)[1:]
## Anarchy Length ##
		if self.bDisplayAnarchy:
			szSpecialText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_WB_ANARCHY", (gc.getCivicInfo(self.iCivic).getAnarchyLength(),))
## Anarchy Length ##
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_SPECIAL +5, self.Y_SPECIAL + 30, self.W_SPECIAL - 10, self.H_SPECIAL - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, true, self.top.X_ITEMS_PANE, self.Y_TEXT, self.top.W_ITEMS_PANE, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getCivicInfo(self.iCivic).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getCivicInfo(self.iCivic).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.top.X_ITEMS_PANE + 10, self.Y_TEXT + 30, self.top.W_ITEMS_PANE - 20, self.H_TEXT - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortCivics(self.top.iSortCivics)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sCivicIcon, ()), self.iCivic, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, -1)

	def handleInput (self, inputClass):
		return 0