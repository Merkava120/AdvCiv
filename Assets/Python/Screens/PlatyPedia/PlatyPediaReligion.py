from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaReligion:
	def __init__(self, main):
		self.iReligion = -1
		self.top = main
		self.bDisplaySpread = False
		for i in xrange(1, gc.getNumReligionInfos()):
			if gc.getReligionInfo(i).getSpreadFactor() != gc.getReligionInfo(i - 1).getSpreadFactor():
				self.bDisplaySpread = True
				break
		
	def interfaceScreen(self, iReligion):
		self.iReligion = iReligion
		self.top.deleteAllWidgets()			
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()
	
		self.H_ICON = 150
		self.H_MAIN_PANE = 210
		self.X_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.X_ITEMS_PANE
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
		
		self.X_REQUIRES = self.top.X_ITEMS_PANE + self.H_MAIN_PANE + self.top.W_BORDER
		self.Y_REQUIRES = self.top.Y_ITEMS_PANE - 20
		self.W_REQUIRES = 75
		self.H_REQUIRES = 110
		self.Y_ALLOWS = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_REQUIRES
		self.Y_SPECIAL = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.W_SPECIAL = self.top.W_ITEMS_PANE - self.top.W_BORDER - self.H_MAIN_PANE

		self.Y_TEXT = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_TEXT = self.Y_ALLOWS - self.Y_TEXT - 10

		self.X_LEADERS = self.X_REQUIRES + self.W_REQUIRES + self.top.W_BORDER
		self.W_LEADERS = self.W_SPECIAL - self.top.W_BORDER - self.W_REQUIRES

		szHeader = gc.getReligionInfo(self.iReligion).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sReligionIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sReligionIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_RELIGION, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.H_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getReligionInfo(self.iReligion).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeSpecial()
		self.placeRequires()
		self.placeText()
		self.placeAllows()
		self.placeLeaders()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_RELIGION and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_RELIGION

	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)
		
		iTech = gc.getReligionInfo(self.iReligion).getTechPrereq()
		if iTech > -1:
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			
	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.X_REQUIRES, self.Y_SPECIAL, self.W_SPECIAL, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().parseReligionInfo(self.iReligion, True)[1:]
## Spread Factor ##
		if self.bDisplaySpread:
			szSpecialText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_SPREAD", ()) + ": " + str(gc.getReligionInfo(self.iReligion).getSpreadFactor())
## Spread Factor ##
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_REQUIRES +5, self.Y_SPECIAL + 30, self.W_SPECIAL - 10, self.H_REQUIRES - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, true, self.top.X_ITEMS_PANE, self.Y_TEXT, self.top.W_ITEMS_PANE, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addMultilineText(self.top.getNextWidgetName(), gc.getReligionInfo(self.iReligion).getCivilopedia(), self.top.X_ITEMS_PANE + 10, self.Y_TEXT + 30, self.top.W_ITEMS_PANE - 20, self.H_TEXT - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeAllows(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_ALLOWS", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_ALLOWS, self.top.W_ITEMS_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		
		for i in xrange(gc.getNumUnitInfos()):
			if gc.getUnitInfo(i).getPrereqReligion() == self.iReligion:
				szButton = gc.getUnitInfo(i).getButton()
				if self.top.iActivePlayer > -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(i)
				screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, i, 1, False )

		for i in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(i).getPrereqReligion() == self.iReligion or gc.getBuildingInfo(i).getHolyCity() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(i).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, i, 1, False )
		for i in xrange(gc.getNumPromotionInfos()):
			if gc.getPromotionInfo(i).getStateReligionPrereq() == self.iReligion:
				screen.attachImageButton( panelName, "", gc.getPromotionInfo(i).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, i, 1, False )

	def placeLeaders(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()), "", false, true, self.X_LEADERS, self.Y_REQUIRES, self.W_LEADERS, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		
		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			LeaderInfo = gc.getLeaderHeadInfo(iLeader)
			if LeaderInfo.getFavoriteReligion() == self.iReligion:
				screen.attachImageButton( panelName, "", LeaderInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, 1, False )

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortReligions(self.top.iSortReligions)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sReligionIcon, ()), self.iReligion, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, -1)

	def handleInput (self, inputClass):
		return 0