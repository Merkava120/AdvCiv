from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaImprovement:
	def __init__(self, main):
		self.iImprovement = -1
		self.top = main
		self.iSize = 48
		
	def interfaceScreen(self, iImprovement):
		self.iImprovement = iImprovement
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()
		
		self.H_ICON = 150
		self.H_MAIN_PANE = 210
		self.W_MAIN_PANE = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.X_ICON = self.top.X_ITEMS_PANE + 30
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
                
		self.X_STATS_PANE = self.X_ICON + self.H_ICON
		self.Y_STATS_PANE = self.Y_ICON + self.H_ICON /4
		self.W_STATS_PANE = self.W_MAIN_PANE - self.H_ICON - self.top.W_BORDER * 2
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE

		self.H_HISTORY = 110
		self.Y_HISTORY = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_HISTORY
		self.Y_IMPROVEMENTS = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_IMPROVEMENTS = self.Y_HISTORY - self.Y_IMPROVEMENTS - 10
		self.W_IMPROVEMENTS = (self.top.W_ITEMS_PANE - self.top.W_BORDER * 2)/3
		self.X_IMPROVEMENTS = self.top.X_ITEMS_PANE + self.W_IMPROVEMENTS + self.top.W_BORDER
		self.X_BONUS = self.X_IMPROVEMENTS + self.W_IMPROVEMENTS + self.top.W_BORDER

		self.X_ANIMATION = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_ANIMATION = self.top.Y_ITEMS_PANE + 8
		self.H_ANIMATION = self.H_MAIN_PANE - 10
		self.X_ROTATION_ANIMATION = -20
		self.Z_ROTATION_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7

		szHeader = gc.getImprovementInfo(self.iImprovement).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sImprovementIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sImprovementIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_IMPROVEMENT, -1)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getImprovementInfo(self.iImprovement).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addImprovementGraphicGFC(self.top.getNextWidgetName(), self.iImprovement, self.X_ANIMATION, self.Y_ANIMATION, self.W_MAIN_PANE, self.H_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_ANIMATION, self.Z_ROTATION_ANIMATION, self.SCALE_ANIMATION, True)
				
		self.placeStats()				
		self.placeSpecial()
		self.placeBonusYield()
		self.placeImprovements()
		self.placeRequires()
		self.placeHistory()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_IMPROVEMENT and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_IMPROVEMENT

	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		sText = ""
		Info = gc.getImprovementInfo(self.iImprovement)
		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = Info.getYieldChange(k)
			if iYieldChange != 0:				
				sText += (u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar()))
		if len(sText):
			sText = "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_YIELDS", ()) + ": " + sText + "</font>"
			screen.appendListBoxString(panelName, sText, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		
		for iBuild in xrange(gc.getNumBuildInfos()):
			BuildInfo = gc.getBuildInfo(iBuild)
			if BuildInfo.getImprovement() == self.iImprovement:
				iTime = BuildInfo.getTime()
				if iTime > 0:
					sText = u"%s: %d" % (CyTranslator().getText("TXT_KEY_VICTORY_TIME", ()), iTime)
					screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				iCost = BuildInfo.getCost()
				if iCost > 0:
					sText = u"%s%c" % (CyTranslator().getText("TXT_KEY_PEDIA_COST", (iCost,)), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
					screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				break

	def placeBonusYield(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_BONUS_YIELDS", ()), "", true, true, self.X_BONUS, self.Y_IMPROVEMENTS, self.W_IMPROVEMENTS, self.H_IMPROVEMENTS, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.X_BONUS - 2, self.Y_IMPROVEMENTS + 20, self.W_IMPROVEMENTS + 4, self.H_IMPROVEMENTS - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		Info = gc.getImprovementInfo(self.iImprovement)
		for item in xrange(gc.getNumBonusInfos()):
			sText = ""
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = Info.getImprovementBonusYield(item, k)
				if iYieldChange != 0:
					sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
			if len(sText):
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getBonusInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getBonusInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)

	def placeHistory(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_ANIMATION, self.Y_HISTORY, self.W_MAIN_PANE, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50)
		szText = ""
		sStrategy = gc.getImprovementInfo(self.iImprovement).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getImprovementInfo(self.iImprovement).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_ANIMATION + 10, self.Y_HISTORY + 30, self.W_MAIN_PANE - 20, self.H_HISTORY - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeImprovements(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", True, True, self.X_IMPROVEMENTS, self.Y_IMPROVEMENTS, self.W_IMPROVEMENTS, self.H_IMPROVEMENTS, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.X_IMPROVEMENTS - 2, self.Y_IMPROVEMENTS + 20, self.W_IMPROVEMENTS + 4, self.H_IMPROVEMENTS - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		Info = gc.getImprovementInfo(self.iImprovement)

		sText = ""
		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = Info.getIrrigatedYieldChange(k)
			if iYieldChange != 0:
				sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
		if len(sText) > 0:
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_IRRIGATION"))
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + CyTranslator().getText("TXT_KEY_CONCEPT_IRRIGATION", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iY += (self.iSize + 4)

		sText = ""
		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = Info.getHillsYieldChange(k)
			if iYieldChange != 0:
				sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
		if len(sText) > 0:
			iHill = gc.getInfoTypeForString("TERRAIN_HILL")
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getTerrainInfo(iHill).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, iHill, 1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getTerrainInfo(iHill).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iY += (self.iSize + 4)

		sText = ""
		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = Info.getRiverSideYieldChange(k)
			if iYieldChange != 0:
				sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
		if len(sText) > 0:
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_RIVER_PLACEMENT").getPath(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PYTHON, 6783, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + CyTranslator().getText("TXT_KEY_MISC_RIVERS", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iY += (self.iSize + 4)

		for item in xrange(gc.getNumTechInfos()):
			sText = ""
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = Info.getTechYieldChanges(item, k)
				if iYieldChange != 0:
					sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
			if len(sText):
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getTechInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getTechInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)

		for item in xrange(gc.getNumCivicInfos()):
			sText = ""
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getCivicInfo(item).getImprovementYieldChanges(self.iImprovement, k)
				if iYieldChange != 0:
					sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
			if len(sText):
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getCivicInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getCivicInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)
	
		for item in xrange(gc.getNumRouteInfos()):
			sText = ""
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = Info.getRouteYieldChanges(item, k)
				if iYieldChange != 0:
					sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
			if len(sText):
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getRouteInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PYTHON, 6788, item)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getRouteInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)
			
	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_HISTORY, self.W_MAIN_PANE, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )

		Info = gc.getImprovementInfo(self.iImprovement)		
		for iBuild in xrange(gc.getNumBuildInfos()):
			if gc.getBuildInfo(iBuild).getImprovement() == self.iImprovement:	 
				iTech = gc.getBuildInfo(iBuild).getTechPrereq()
				if iTech > -1:
					screen.attachImageButton(panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
		for item in xrange(gc.getNumTerrainInfos()):
			if Info.getTerrainMakesValid(item):
				screen.attachImageButton(panelName, "", gc.getTerrainInfo(item).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, item, 1, False )
		if Info.isHillsMakesValid() and not Info.isRequiresFlatlands():
			item = gc.getInfoTypeForString("TERRAIN_HILL")
			screen.attachImageButton(panelName, "", gc.getTerrainInfo(item).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, item, 1, False )
		if Info.isRequiresIrrigation():
			screen.attachImageButton(panelName, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_IRRIGATION"), CvUtil.FONT_LEFT_JUSTIFY)
		if Info.isRiverSideMakesValid() and not Info.isRequiresRiverSide():
			screen.attachImageButton(panelName, "", CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_RIVER_PLACEMENT").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		for item in xrange(gc.getNumFeatureInfos()):
			if Info.getFeatureMakesValid(item):
				screen.attachImageButton(panelName, "", gc.getFeatureInfo(item).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, item, 1, False )
			
	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_IMPROVEMENTS, self.W_IMPROVEMENTS, self.H_IMPROVEMENTS, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().getImprovementHelp(self.iImprovement, True)[1:]
		Info = gc.getImprovementInfo(self.iImprovement)
		if Info.isFreshWaterMakesValid():
			if len(szSpecialText) > 0:
				szSpecialText += "\n"
			szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_IMPROVEMENT_FRESHWATER_VALID", ())
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_IMPROVEMENTS+30, self.W_IMPROVEMENTS-10, self.H_IMPROVEMENTS-55, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortImprovements(self.top.iSortImprovements)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sImprovementIcon, ()), self.iImprovement, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, -1)

	def handleInput (self, inputClass):
		return 0