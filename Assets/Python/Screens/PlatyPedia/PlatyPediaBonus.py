from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaBonus:
	def __init__(self, main):
		self.iBonus = -1
		self.top = main
		self.iSize = 48
		
	def interfaceScreen(self, iBonus):
		self.iBonus = iBonus
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()
		
		self.H_ICON = 150
		self.H_MAIN_PANE = 210
		self.W_MAIN_PANE = (self.top.W_ITEMS_PANE - self.top.W_BORDER * 2)/3
		self.X_ICON = self.top.X_ITEMS_PANE + 30
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
		
		self.X_STATS_PANE = self.X_ICON + self.H_ICON
		self.Y_STATS_PANE = self.Y_ICON + self.H_ICON /4
		self.W_STATS_PANE = self.top.X_ITEMS_PANE + self.W_MAIN_PANE - self.X_STATS_PANE + self.top.X_ITEMS_PANE
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE
		
		self.H_ALLOWS = 110
		self.W_ALLOWS = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.X_PRODUCTION = self.top.X_ITEMS_PANE + self.W_ALLOWS + self.top.W_BORDER
		self.X_TECH = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_ALLOWS = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_ALLOWS
		self.Y_SPECIAL = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_SPECIAL = self.Y_ALLOWS - self.Y_SPECIAL - 10
		
		self.X_ANIMATION = self.X_TECH + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_ANIMATION = self.top.Y_ITEMS_PANE + 8
		self.H_ANIMATION = self.H_MAIN_PANE - 10
		self.X_ROTATION_ANIMATION = -20
		self.Z_ROTATION_ANIMATION = 30
		self.SCALE_ANIMATION = 0.6

		szHeader = gc.getBonusInfo(self.iBonus).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sBonusIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sBonusIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT,  CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_BONUS, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBonusInfo(self.iBonus).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addBonusGraphicGFC(self.top.getNextWidgetName(), self.iBonus, self.X_ANIMATION, self.Y_ANIMATION, self.W_MAIN_PANE, self.H_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_ANIMATION, self.Z_ROTATION_ANIMATION, self.SCALE_ANIMATION, True)
		
		self.placeStats()
		self.placeSpecial()
		self.placeTechs()
		self.placeAllows()
		self.placeCorporations()
		self.placeHistory()
		self.placeFasterProduction()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_BONUS and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_BONUS

	def placeFasterProduction(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_FASTER_PRODUCTION", ()), "", False, True, self.X_PRODUCTION, self.Y_ALLOWS, self.W_ALLOWS, self.H_ALLOWS, PanelStyles.PANEL_STYLE_BLUE50 )

		for i in xrange(gc.getNumUnitClassInfos()):
			item = gc.getUnitClassInfo(i).getDefaultUnitIndex()
			if CyGame().getActiveCivilizationType() > -1:
				item = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(i)
			if item == -1: continue
			Info = gc.getUnitInfo(item)
			if Info.getBonusProductionModifier(self.iBonus) > 0:
				szButton = Info.getButton()
				if self.top.iActivePlayer > -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(item)
				screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item, 1, False )

		for i in xrange(gc.getNumBuildingClassInfos()):
			item = gc.getBuildingClassInfo(i).getDefaultBuildingIndex()
			if CyGame().getActiveCivilizationType() > -1:
				item = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationBuildings(i)
			if item == -1: continue
			Info = gc.getBuildingInfo(item)
			if Info.getBonusProductionModifier(self.iBonus) > 0:
				screen.attachImageButton(panelName, "", Info.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, 1, False )

		for item in xrange(gc.getNumProjectInfos()):
			Info = gc.getProjectInfo(item)
			if Info.getBonusProductionModifier(self.iBonus) > 0:
				screen.attachImageButton(panelName, "", Info.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, item, 1, False )

	def placeTechs(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, True, self.X_TECH, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.X_TECH - 2, self.top.Y_ITEMS_PANE + 20, self.W_MAIN_PANE + 4, self.H_MAIN_PANE - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		iAdjustment = (self.iSize - 16) /2 - iY

		item = gc.getBonusInfo(self.iBonus).getTechReveal()
		if item > -1:
			sText = CyTranslator().getText("TXT_KEY_PEDIA_BONUS_APPEARANCE", ())
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getTechInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item, 1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getTechInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += (self.iSize + 4)
		item = gc.getBonusInfo(self.iBonus).getTechCityTrade()
		if item > -1:
			sText = CyTranslator().getText("TXT_KEY_PEDIA_BONUS_TRADE", ())
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getTechInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item, 1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getTechInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += (self.iSize + 4)
		item = gc.getBonusInfo(self.iBonus).getTechObsolete()
		if item > -1:
			sText = CyTranslator().getText("TXT_KEY_PEDIA_OBSOLETE", ())
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getTechInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item, 1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getTechInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getBonusInfo(self.iBonus).getYieldChange(k)
			if iYieldChange != 0:
				sText = u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
				screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
						
	def getDecimal(self, iAmount):
		sText = str(iAmount / 10000)
		if iAmount > 0:
			sText = "+" + sText
		iEnd = abs(iAmount) % 10000
		if iEnd != 0:
			sEnd = str(iEnd)
			while len(sEnd) < 4:
				sEnd = "0" + sEnd
			while sEnd[-1] == "0":
				sEnd = sEnd[:-1]
			sText += "." + sEnd
		return sText

	def placeCorporations(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()), "", False, True, self.top.X_ITEMS_PANE, self.Y_SPECIAL, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.top.X_ITEMS_PANE - 2, self.Y_SPECIAL + 20, self.W_MAIN_PANE + 4, self.H_SPECIAL - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		iWorldSize = WorldSizeTypes.WORLDSIZE_STANDARD
		if CyGame().isFinalInitialized():
			iWorldSize = CyMap().getWorldSize()
		iModifier = gc.getWorldInfo(iWorldSize).getCorporationMaintenancePercent()

		for item in xrange(gc.getNumCorporationInfos()):
			Info = gc.getCorporationInfo(item)
			for i in xrange(gc.getNUM_CORPORATION_PREREQ_BONUSES ()):
				if self.iBonus == Info.getPrereqBonus(i):
					sText = ""
					for k in range(YieldTypes.NUM_YIELD_TYPES):
						iYieldChange = Info.getYieldProduced(k)
						if iYieldChange != 0:
							sText += u"%s%c" % (self.getDecimal(iYieldChange * iModifier), gc.getYieldInfo(k).getChar())
					for k in range(CommerceTypes.NUM_COMMERCE_TYPES):
						iCommerceChange = Info.getCommerceProduced(k)
						if iCommerceChange != 0:
							sText += u"%s%c" % (self.getDecimal(iCommerceChange * iModifier), gc.getCommerceInfo(k).getChar())
					if len(sText):
						screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getCorporationInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, item, 1)
						screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + Info.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						iY += (self.iSize + 4)

	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, True, self.X_TECH, self.Y_SPECIAL, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.X_TECH, self.Y_SPECIAL + 20, self.W_MAIN_PANE, self.H_SPECIAL - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		iAdjustment = (self.iSize - 16) /2 - iY
		iWorldSize = WorldSizeTypes.WORLDSIZE_STANDARD
		if CyGame().isFinalInitialized():
			iWorldSize = CyMap().getWorldSize()
		Info = gc.getBonusInfo(self.iBonus)

		lGroup = []
		lGroup2 = []
		lGroup3 = []
		for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
			iBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()
			if CyGame().getActiveCivilizationType() > -1:
				iBuilding = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationBuildings(iBuildingClass)
			if iBuilding == -1: continue
			BuildingInfo = gc.getBuildingInfo(iBuilding)
			sText = ""
			bFree = False
			bAccess = False
			if BuildingInfo.getFreeBonus() == self.iBonus:
				iNumFree = BuildingInfo.getNumFreeBonuses()
				if iNumFree == -1:
					iNumFree = gc.getWorldInfo(iWorldSize).getNumFreeBuildingBonuses()
				if iNumFree != 0:
					sText = u"%+d%c" % (iNumFree, Info.getChar()) + sText
					bFree = True
			if BuildingInfo.getNoBonus() == self.iBonus:
				sText = CyTranslator().getText("TXT_KEY_PEDIA_REMOVES_ACCESS", ())
				bAccess = True
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = BuildingInfo.getBonusYieldModifier(self.iBonus, k)
				if iYieldChange != 0:
					sText += u"%+d%%%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
			iHappy = BuildingInfo.getBonusHappinessChanges(self.iBonus)
			if iHappy != 0:
				if iHappy > 0:
					sText += u"%+d%s" % (iHappy, CyTranslator().getText("[ICON_HAPPY]", ()))
				else:
					sText += u"%+d%s" % (-iHappy, CyTranslator().getText("[ICON_UNHAPPY]", ()))
			iHealth = BuildingInfo.getBonusHealthChanges(self.iBonus)
			if iHealth != 0:
				if iHealth > 0:
					sText += u"%+d%s" % (iHealth, CyTranslator().getText("[ICON_HEALTHY]", ()))
				else:
					sText += u"%+d%s" % (-iHealth, CyTranslator().getText("[ICON_UNHEALTHY]", ()))
			if len(sText):
				if bFree:
					lGroup.append([iBuilding, sText])
				elif bAccess:
					lGroup2.append([iBuilding, sText])
				else:
					lGroup3.append([iBuilding, sText])
		lGroup += lGroup2 + lGroup3

		for i in xrange(len(lGroup)):
			item = lGroup[i][0]
			sText = lGroup[i][1]
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getBuildingInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, 1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getBuildingInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iY += (self.iSize + 4)

		sText = ""
		iHappy = Info.getHappiness()
		if iHappy != 0:
			if iHappy > 0:
				sText += u"%+d%s" % (iHappy, CyTranslator().getText("[ICON_HAPPY]", ()))
			else:
				sText += u"%+d%s" % (-iHappy, CyTranslator().getText("[ICON_UNHAPPY]", ()))
		iHealth = Info.getHealth()
		if iHealth != 0:
			if iHealth > 0:
				sText += u"%+d%s" % (iHealth, CyTranslator().getText("[ICON_HEALTHY]", ()))
			else:
				sText += u"%+d%s" % (-iHealth, CyTranslator().getText("[ICON_UNHEALTHY]", ()))
	
		for item in xrange(gc.getNumImprovementInfos()):
			szYield = ""
			ItemInfo = gc.getImprovementInfo(item)
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = ItemInfo.getImprovementBonusYield(self.iBonus, k)
				if iYieldChange != 0:
					iYieldChange += ItemInfo.getYieldChange(k)
					szYield += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
			if len(szYield):
				szYield += sText
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, ItemInfo.getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + ItemInfo.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + szYield + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)

		sHelp = Info.getHelp()
		if len(sHelp) > 0:
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), 0, iY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setTextAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sHelp + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
	def placeHistory(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_ANIMATION, self.Y_SPECIAL, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50)
		szText = ""
		sStrategy = gc.getBonusInfo(self.iBonus).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getBonusInfo(self.iBonus).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_ANIMATION + 10, self.Y_SPECIAL + 30, self.W_MAIN_PANE - 20, self.H_SPECIAL - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeAllows(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_ALLOWS", ()), "", False, True, self.top.X_ITEMS_PANE, self.Y_ALLOWS, self.W_ALLOWS, self.H_ALLOWS, PanelStyles.PANEL_STYLE_BLUE50 )

		for i in xrange(gc.getNumUnitClassInfos()):
			item = gc.getUnitClassInfo(i).getDefaultUnitIndex()
			if CyGame().getActiveCivilizationType() > -1:
				item = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(i)
			if item == -1: continue
			bFound = False
			Info = gc.getUnitInfo(item)
			if Info.getPrereqAndBonus() == self.iBonus:
				bFound = True	
			else:
				for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
					if Info.getPrereqOrBonuses(j) == self.iBonus:
						bFound = True
						break
			if bFound:
				szButton = Info.getButton()
				if self.top.iActivePlayer > -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(item)
				screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item, 1, False )

		for i in xrange(gc.getNumBuildingClassInfos()):
			item = gc.getBuildingClassInfo(i).getDefaultBuildingIndex()
			if CyGame().getActiveCivilizationType() > -1:
				item = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationBuildings(i)
			if item == -1: continue
			bFound = False
			Info = gc.getBuildingInfo(item)
			if Info.getPrereqAndBonus() == self.iBonus:
				bFound = True	
			else:
				for j in xrange(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
					if Info.getPrereqOrBonuses(j) == self.iBonus:
						bFound = True
						break
			if bFound:
				screen.attachImageButton(panelName, "", Info.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, 1, False )

		for item in xrange(gc.getNumRouteInfos()):
			bFound = False
			Info = gc.getRouteInfo(item)
			if Info.getPrereqBonus() == self.iBonus:
				bFound = True	
			else:
				for j in xrange(gc.getNUM_ROUTE_PREREQ_OR_BONUSES()):
					if Info.getPrereqOrBonus(j) == self.iBonus:
						bFound = True
						break
			if bFound:
				screen.attachImageButton(panelName, "", Info.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PYTHON, 6788, item, False)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortBonus(self.top.iSortBonus)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sBonusIcon, ()), self.iBonus, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, -1)

	def handleInput (self, inputClass):
		return 0