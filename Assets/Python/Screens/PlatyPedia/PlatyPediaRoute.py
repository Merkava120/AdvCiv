from CvPythonExtensions import *
import CvUtil
import ScreenInput
gc = CyGlobalContext()

class CvPediaRoute:
	def __init__(self, main):
		self.iRoute = -1
		self.top = main
		self.iSize = 48

	def interfaceScreen(self, iRoute):	
		self.iRoute = iRoute
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
		self.Y_STATS_PANE = self.Y_ICON + self.H_ICON/5
		self.W_STATS_PANE = self.W_MAIN_PANE - self.H_ICON - self.top.W_BORDER
		self.H_STATS_PANE = self.H_MAIN_PANE - self.Y_STATS_PANE + self.top.Y_ITEMS_PANE

		self.H_REQUIRES = 110
		self.Y_REQUIRES = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_REQUIRES
		
		self.Y_EFFECTS = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_EFFECTS = self.Y_REQUIRES - self.Y_EFFECTS - 10

		self.X_UNITS = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + 20
		self.Y_CONCEPT = self.top.Y_ITEMS_PANE - 20
		self.Y_UNITS = self.Y_EFFECTS + self.H_EFFECTS + 10

		szHeader = gc.getRouteInfo(self.iRoute).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sRouteIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sRouteIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_ROUTE, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getRouteInfo(iRoute).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeStats()
		self.placeMovement()
		self.placeYields()
		self.placeRequires()
		self.placeText()
		self.placeLinks(self.top.iLastScreen == self.top.PLATYPEDIA_ROUTE and screen.isActive())
		self.top.iLastScreen = self.top.PLATYPEDIA_ROUTE

	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		RouteInfo = gc.getRouteInfo(self.iRoute)		
		sText = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_VALUE_TEXT",()) + ": " + str(RouteInfo.getValue())
		screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		for iBuild in xrange(gc.getNumBuildInfos()):
			BuildInfo = gc.getBuildInfo(iBuild)
			if gc.getBuildInfo(iBuild).getRoute() == self.iRoute:
				iTime = BuildInfo.getTime()
				if iTime > 0:
					sText = u"%s: %d" % (CyTranslator().getText("TXT_KEY_VICTORY_TIME", ()), iTime)
					screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				iCost = BuildInfo.getCost()
				if iCost > 0:
					sText = u"%s%c" % (CyTranslator().getText("TXT_KEY_PEDIA_COST", (iCost,)), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
					screen.appendListBoxString(panelName, "<font=4>" + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				break
		
	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		panelName2 = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES, self.W_MAIN_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.addPanel(panelName2, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()), "", false, true, self.X_UNITS, self.Y_UNITS, self.W_MAIN_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )

		for iBuild in xrange(gc.getNumBuildInfos()):
			if (gc.getBuildInfo(iBuild).getRoute() == self.iRoute):	 
				iTech = gc.getBuildInfo(iBuild).getTechPrereq()
				if (iTech > -1):
					screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

				for i in xrange(gc.getNumUnitClassInfos()):
					item = gc.getUnitClassInfo(i).getDefaultUnitIndex()
					if CyGame().getActiveCivilizationType() > -1:
						item = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(i)
					if item == -1: continue
					if gc.getUnitInfo(item).getBuilds(iBuild):
						screen.attachImageButton(panelName2, "", gc.getUnitInfo(item).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item, 1, False )

		bFirst = True
		iPrereq = gc.getRouteInfo(self.iRoute).getPrereqBonus()
		if iPrereq > -1:
			bFirst = False
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		nOr = 0
		for j in xrange(gc.getNUM_ROUTE_PREREQ_OR_BONUSES()):
			if gc.getRouteInfo(self.iRoute).getPrereqOrBonus(j) > -1:
				nOr += 1

		szRightDelimeter = ""
		if not bFirst:
			if (nOr > 1):
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()) + "( ")
				szRightDelimeter = " ) "
			elif (nOr > 0):
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()))

		bFirst = True
		for j in xrange(gc.getNUM_ROUTE_PREREQ_OR_BONUSES()):
			eBonus = gc.getRouteInfo(self.iRoute).getPrereqOrBonus(j)
			if eBonus > -1:
				if (not bFirst):
					screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getBonusInfo(eBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False )					

		if len(szRightDelimeter):
			screen.attachLabel(panelName, "", szRightDelimeter)

	def placeMovement(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CONCEPT_MOVEMENT", ()), "", False, True, self.top.X_ITEMS_PANE, self.Y_EFFECTS, self.W_MAIN_PANE, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.top.X_ITEMS_PANE - 2, self.Y_EFFECTS + 20, self.W_MAIN_PANE + 4, self.H_EFFECTS - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		Info = gc.getRouteInfo(self.iRoute)
		sText = u"%s: %.2f%s" % (CyTranslator().getText("TXT_KEY_PEDIA_FLAT_COST",()), float(Info.getFlatMovementCost()) / gc.getMOVE_DENOMINATOR(), CyTranslator().getText("[ICON_MOVES]", ()))
		screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		sText = u"%s: %.2f%s" % (CyTranslator().getText("TXT_KEY_PEDIA_MOVE_COST",()), float(Info.getMovementCost()) / gc.getMOVE_DENOMINATOR(), CyTranslator().getText("[ICON_MOVES]", ()))
		screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		iY += (self.iSize + 4)

		for item in xrange(gc.getNumTechInfos()):
			iRouteChange = Info.getTechMovementChange(item)
			if iRouteChange != 0:
				sText = u"%s: %+.2f%s" % (CyTranslator().getText("TXT_KEY_PEDIA_MOVE_COST",()), float(iRouteChange) / gc.getMOVE_DENOMINATOR(), CyTranslator().getText("[ICON_MOVES]", ()))
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getTechInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getTechInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)


	def placeYields(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_YIELDS", ()), "", False, True, self.X_UNITS, self.Y_EFFECTS, self.W_MAIN_PANE, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.X_UNITS - 2, self.Y_EFFECTS + 20, self.W_MAIN_PANE + 4, self.H_EFFECTS - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		Info = gc.getRouteInfo(self.iRoute)
		sText = ""
		for k in xrange(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = Info.getYieldChange(k)
			if iYieldChange != 0:
				sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
		if len(sText) > 0:
			screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iY += (self.iSize + 4)

		for item in xrange(gc.getNumImprovementInfos()):
			sText = ""
			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getImprovementInfo(item).getRouteYieldChanges(self.iRoute, k)
				if iYieldChange != 0:
					sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())
			if len(sText) > 0:
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getImprovementInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getImprovementInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)

	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()), "", true, false, self.X_UNITS, self.Y_CONCEPT, self.W_MAIN_PANE, self.H_MAIN_PANE + 20, PanelStyles.PANEL_STYLE_BLUE50 )	
		screen.addMultilineText(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CONCEPT_MOVEMENT_PEDIA", ()), self.X_UNITS+10, self.Y_CONCEPT + 30, self.W_MAIN_PANE -20, self.H_MAIN_PANE - 35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortRoutes(self.top.iSortRoutes)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sRouteIcon, ()), self.iRoute, WidgetTypes.WIDGET_PYTHON, 6788)

	def handleInput (self, inputClass):
		return 0