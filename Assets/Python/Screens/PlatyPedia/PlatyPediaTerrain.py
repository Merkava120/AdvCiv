from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaTerrain:
	def __init__(self, main):
		self.iTerrain = -1
		self.top = main

	def interfaceScreen(self, iTerrain):
		self.iTerrain = iTerrain
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
		
		self.X_SPECIAL = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_SPECIAL = self.top.Y_ITEMS_PANE - 20
		self.H_SPECIAL = self.H_MAIN_PANE + 20
		self.Y_IMPROVEMENT = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.X_FEATURE = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.H_FEATURE = 110
		self.Y_BONUS = self.Y_IMPROVEMENT + self.H_FEATURE + 10
		self.Y_HISTORY_PANE = self.Y_BONUS + self.H_FEATURE + 10
		self.H_HISTORY_PANE = screen.getYResolution() - self.Y_HISTORY_PANE - self.top.Y_ITEMS_PANE

		szHeader = gc.getTerrainInfo(self.iTerrain).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sTerrainIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sTerrainIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_TERRAIN, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTerrainInfo(self.iTerrain).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeStats()
		self.placeSpecial()
		self.placeFeatures()
		self.placeBonus()
		self.placeImprovements()
		self.placeHistory()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_UNIT and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_TERRAIN

	def placeHistory(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.top.X_ITEMS_PANE, self.Y_HISTORY_PANE, self.top.W_ITEMS_PANE, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getTerrainInfo(self.iTerrain).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getTerrainInfo(self.iTerrain).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.top.X_ITEMS_PANE + 10, self.Y_HISTORY_PANE + 30, self.top.W_ITEMS_PANE - 20, self.H_HISTORY_PANE - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)

		sText = ""
		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getTerrainInfo(self.iTerrain).getYield(k)
			if iYieldChange != 0:
				sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
		if len(sText):
			screen.appendListBoxString(panelName, "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_YIELDS", ()) + ": </font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
			screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false, self.X_SPECIAL, self.Y_SPECIAL, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().getTerrainHelp(self.iTerrain, True)[1:]
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_SPECIAL +5, self.Y_SPECIAL + 30, self.W_MAIN_PANE - 10, self.H_SPECIAL - 55, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeFeatures(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ()), "", false, true, self.X_FEATURE, self.Y_IMPROVEMENT, self.W_MAIN_PANE, self.H_FEATURE, PanelStyles.PANEL_STYLE_BLUE50 )
		for iFeature in xrange(gc.getNumFeatureInfos()):
			FeatureInfo = gc.getFeatureInfo(iFeature)
			if FeatureInfo.isTerrain(self.iTerrain):
				screen.attachImageButton( panelName, "", FeatureInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, iFeature, 1, False )
		
	def placeBonus(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_BONUS, self.top.W_ITEMS_PANE, self.H_FEATURE, PanelStyles.PANEL_STYLE_BLUE50 )
		for iBonus in xrange(gc.getNumBonusInfos()):
			BonusInfo = gc.getBonusInfo(iBonus)
			if BonusInfo.isTerrain(self.iTerrain):
				screen.attachImageButton( panelName, "", BonusInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, 1, False )

	def placeImprovements(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_IMPROVEMENT, self.W_MAIN_PANE, self.H_FEATURE, PanelStyles.PANEL_STYLE_BLUE50 )
		for iImprovement in xrange(gc.getNumImprovementInfos()):
			ImprovementInfo = gc.getImprovementInfo(iImprovement)
			if ImprovementInfo.getTerrainMakesValid(self.iTerrain):
				screen.attachImageButton( panelName, "", ImprovementInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImprovement, 1, False )

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortTerrains(self.top.iSortTerrains)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sTerrainIcon, ()), self.iTerrain, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, -1)

	def handleInput (self, inputClass):
		return 0