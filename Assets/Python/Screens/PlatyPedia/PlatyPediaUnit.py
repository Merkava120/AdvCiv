from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaUnit:
	def __init__(self, main):
		self.iUnit = -1
		self.top = main

	def interfaceScreen(self, iUnit):	
		self.iUnit = iUnit
		self.top.deleteAllWidgets()										
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_ICON = 150
		self.W_MAIN_PANE = screen.getXResolution() * 2/5
		self.H_MAIN_PANE = 210
		self.X_ICON = self.top.X_ITEMS_PANE + 30
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE

		self.X_ANIMATION = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_ANIMATION = self.top.Y_ITEMS_PANE + 8
		self.W_ANIMATION = self.top.W_ITEMS_PANE - self.top.W_BORDER - self.W_MAIN_PANE
		self.H_ANIMATION = self.H_MAIN_PANE - 10
		self.X_ROTATION_ANIMATION = -20
		self.Z_ROTATION_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0

		self.H_PREREQ_PANE = 110
		self.Y_UPGRADES_TO_PANE = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE
		self.Y_HISTORY_PANE = self.Y_UPGRADES_TO_PANE + self.H_PREREQ_PANE
		self.H_HISTORY_PANE = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_HISTORY_PANE

		self.PROMOTION_ICON_SIZE = 32

		self.X_STATS_PANE = self.X_ICON + self.H_ICON
		self.Y_STATS_PANE = self.Y_ICON + self.H_ICON /4
		self.W_STATS_PANE = self.W_MAIN_PANE - self.H_ICON - self.top.W_BORDER * 2
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE

		self.H_SPECIAL_PANE = self.H_HISTORY_PANE /2
		self.Y_PROMO_PANE = self.Y_HISTORY_PANE + self.H_SPECIAL_PANE

		szHeader = gc.getUnitInfo(self.iUnit).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sUnitIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sUnitIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT, iUnit)

		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_UNIT, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		szButton = gc.getUnitInfo(self.iUnit).getButton()
		if self.top.iActivePlayer > -1:
			szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(self.iUnit)
		screen.addDDSGFC(self.top.getNextWidgetName(), szButton, self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addUnitGraphicGFC(self.top.getNextWidgetName(), self.iUnit, self.X_ANIMATION, self.Y_ANIMATION, self.W_ANIMATION, self.H_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_ANIMATION, self.Z_ROTATION_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()
		self.placeUpgradesTo()
		self.placeRequires()
		self.placeSpecial()
		self.placePromotions()						
		self.placeHistory()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_UNIT and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_UNIT
		
	def placeStats(self):
		screen = self.top.getScreen()
		
		iCombatType = gc.getUnitInfo(self.iUnit).getUnitCombatType()
		if iCombatType > -1:
			screen.setImageButton(self.top.getNextWidgetName(), gc.getUnitCombatInfo(iCombatType).getButton(), self.X_STATS_PANE + 5, self.Y_STATS_PANE - 34, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)
			screen.setText(self.top.getNextWidgetName(), "", u"<font=4>" + gc.getUnitCombatInfo(iCombatType).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 42, self.Y_STATS_PANE - 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)

		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		
		iStrength = gc.getUnitInfo(self.iUnit).getCombat()
		if iStrength:
			szStrength = u"<font=4>%s %d%c</font>" %(CyTranslator().getText("INTERFACE_PANE_STRENGTH", ()), iStrength, CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
			screen.appendListBoxString(panelName, szStrength, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		iStrength = gc.getUnitInfo(self.iUnit).getAirCombat()
		if iStrength:
			szStrength = u"<font=4>%s %d%c</font>" %(CyTranslator().getText("INTERFACE_PANE_AIR_STRENGTH", ()), iStrength, CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
			screen.appendListBoxString(panelName, szStrength, WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		szMovement = CyTranslator().getText("TXT_KEY_PEDIA_MOVEMENT", ( gc.getUnitInfo(self.iUnit).getMoves(), ) )
		screen.appendListBoxString(panelName, u"<font=4>" + szMovement + u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iRange = gc.getUnitInfo(self.iUnit).getAirRange()
		if iRange:
			szRange = CyTranslator().getText("TXT_KEY_PEDIA_AIR_RANGE", ()) + ": " + str(iRange) + CyTranslator().getText("[ICON_TRADE]", ())
			screen.appendListBoxString(panelName, u"<font=4>" + szRange + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iCost = gc.getUnitInfo(self.iUnit).getProductionCost()
		if iCost > -1 and not gc.getUnitInfo(self.iUnit).isFound():
			if self.top.iActivePlayer == -1:
				szCost = CyTranslator().getText("TXT_KEY_PEDIA_COST", (iCost * gc.getDefineINT("UNIT_PRODUCTION_PERCENT") /100,))
			else:
				szCost = CyTranslator().getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getUnitProductionNeeded(self.iUnit),))
			screen.appendListBoxString(panelName, u"<font=4>" + szCost + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_UPGRADES_TO_PANE, self.W_MAIN_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTech()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )
				
		for j in xrange(gc.getDefineINT("NUM_UNIT_AND_TECH_PREREQS")):
			iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndTechs(j)
			if iPrereq > -1:
				screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, -1, False )

		bFirst = True
		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqAndBonus()
		if iPrereq > -1:
			bFirst = False
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		nOr = 0
		for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			if gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j) > -1:
				nOr += 1

		szRightDelimeter = ""
		if not bFirst:
			if nOr > 1:
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()) + "( ")
				szRightDelimeter = " ) "
			elif nOr == 1:
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()))

		bFirst = True
		for j in xrange(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			eBonus = gc.getUnitInfo(self.iUnit).getPrereqOrBonuses(j)
			if eBonus > -1:
				if not bFirst:
					screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getBonusInfo(eBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False )					

		if len(szRightDelimeter):
			screen.attachLabel(panelName, "", szRightDelimeter)

		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqReligion()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, -1, False )

		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqCorporation()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getCorporationInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, iPrereq, -1, False )

		iPrereq = gc.getUnitInfo(self.iUnit).getPrereqBuilding()
		if iPrereq > -1:
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPrereq, -1, False )		
		
	def placeUpgradesTo(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_UPGRADES_TO", ()), "", false, true, self.X_ANIMATION, self.Y_UPGRADES_TO_PANE, self.W_ANIMATION, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		for k in xrange(gc.getNumUnitClassInfos()):
			eLoopUnit = gc.getUnitClassInfo(k).getDefaultUnitIndex()
			if self.top.iActivePlayer > -1:
				eLoopUnit = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(k)
				
			if eLoopUnit > -1 and gc.getUnitInfo(self.iUnit).getUpgradeUnitClass(k):
				szButton = gc.getUnitInfo(eLoopUnit).getButton()
				if self.top.iActivePlayer > -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(eLoopUnit)
				screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_HISTORY_PANE, self.W_MAIN_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().getUnitHelp( self.iUnit, True, False, False, None )[1:]
## Work Rate ##
		iWorkRate = gc.getUnitInfo(self.iUnit).getWorkRate()
		if iWorkRate > 0:
			szSpecialText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_WORK_RATE", ()) + ": " + str(iWorkRate) + CyTranslator().getText("[ICON_PRODUCTION]", ())
## State Religion Requirement ##
		iStateReligion = gc.getUnitInfo(self.iUnit).getStateReligion()
		if iStateReligion > -1:
			szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_UNIT_STATE_RELIGION", (gc.getReligionInfo(iStateReligion).getDescription(),))
## State Religion Requirement ##
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_HISTORY_PANE+30, self.W_MAIN_PANE-10, self.H_SPECIAL_PANE-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
					
	def placeHistory(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_ANIMATION, self.Y_HISTORY_PANE, self.W_ANIMATION, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getUnitInfo(self.iUnit).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getUnitInfo(self.iUnit).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_ANIMATION + 10, self.Y_HISTORY_PANE + 30, self.W_ANIMATION - 20, self.H_HISTORY_PANE - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placePromotions(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", true, true, self.top.X_ITEMS_PANE, self.Y_PROMO_PANE, self.W_MAIN_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.top.X_ITEMS_PANE + 15, self.Y_PROMO_PANE + 40, self.W_MAIN_PANE - 20, self.H_SPECIAL_PANE - 40, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
		for k in xrange(gc.getNumPromotionInfos()):
			if isPromotionValid(k, self.iUnit, True) and not gc.getPromotionInfo(k).isGraphicalOnly():
				screen.appendMultiListButton(rowListName, gc.getPromotionInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, k, -1, false )

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortUnits(self.top.iSortUnits)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sUnitIcon, ()), self.iUnit, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, -1)

	def handleInput (self, inputClass):
		return 0