from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaUnitChart:
	def __init__(self, main):
		self.iGroup = -1
		self.top = main

	def interfaceScreen(self, iGroup):
		self.iGroup = iGroup
		self.top.deleteAllWidgets()				
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		if self.iGroup == -1:
			szHeader = CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ())
		elif self.iGroup == -2:
			szHeader = CyTranslator().getText("TXT_KEY_PEDIA_ALL_GROUPS", ())
		else:
			szHeader = gc.getUnitCombatInfo(self.iGroup).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sUnitCombatIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sUnitCombatIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_UNIT_GROUP, -1)
		self.placeUnitTable()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_UNIT_CHART and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_UNIT_CHART
		
	def placeUnitTable(self):
		screen = self.top.getScreen()

		szTable = self.top.getNextWidgetName()
		iNumColumns = 9
		screen.addTableControlGFC(szTable, iNumColumns, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE + 6, self.top.W_ITEMS_PANE, self.top.H_ITEMS_PANE, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSort(szTable)
		iNumColumns -= 2
		iWidth = self.top.W_ITEMS_PANE *3/4 - 10
		screen.setTableColumnHeader(szTable, 0, "", self.top.W_ITEMS_PANE /4)
		screen.setTableColumnHeader(szTable, 1, "<font=2>" + CyTranslator().getText("TXT_KEY_PEDIA_DOMAIN", ()) + "</font>", iWidth/iNumColumns)
		screen.setTableColumnHeader(szTable, 2, u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), iWidth/iNumColumns)
		screen.setTableColumnHeader(szTable, 3, u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR), iWidth/iNumColumns)
		screen.setTableColumnHeader(szTable, 4, u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR), iWidth/iNumColumns)
		screen.setTableColumnHeader(szTable, 5, "<font=2>" + CyTranslator().getText("TXT_KEY_PEDIA_AIR_RANGE", ()) + "</font>", iWidth/iNumColumns)
		screen.setTableColumnHeader(szTable, 6, "<font=2>" + CyTranslator().getText("TXT_KEY_PEDIA_WITHDRAWAL", ()) + "</font>", iWidth/iNumColumns)
		screen.setTableColumnHeader(szTable, 7, "<font=2>" + CyTranslator().getText("TXT_KEY_MISSION_BOMBARD", ()) + "</font>", iWidth/iNumColumns)
		screen.setTableColumnHeader(szTable, 8, "", 10)

		for j in xrange(gc.getNumUnitInfos()):
			if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and CyGame().isFinalInitialized():
				if not CyGame().isBuildingEverActive(j): continue
			UnitInfo = gc.getUnitInfo(j)
			if (self.iGroup == UnitInfo.getUnitCombatType() or self.iGroup == -2):
				if UnitInfo.getDomainType() == DomainTypes.DOMAIN_AIR:
					iStrength = UnitInfo.getAirCombat()
					iBomb = UnitInfo.getBombRate()
					iWithdrawal = UnitInfo.getEvasionProbability()
				else:
					iStrength = UnitInfo.getCombat()
					iBomb = UnitInfo.getBombardRate()
					iWithdrawal = UnitInfo.getWithdrawalProbability()

				szCost = CyTranslator().getText("TXT_KEY_NON_APPLICABLE", ())
				iCost = UnitInfo.getProductionCost()
				if iCost > -1:
					szCost = str(iCost)
				sDomain = gc.getDomainInfo(gc.getUnitInfo(j).getDomainType()).getDescription()
				sDomain = sDomain[:sDomain.find(" ")]
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, iRow, u"<font=3>" + gc.getUnitInfo(j).getDescription() + u"</font>", gc.getUnitInfo(j).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, j, 1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(szTable, 1, iRow, u"<font=3>" + sDomain + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable, 2, iRow, u"<font=3>" + szCost + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 3, iRow, u"<font=3>" + self.colorCode(iStrength) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 4, iRow, u"<font=3>" + self.colorCode(UnitInfo.getMoves()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 5, iRow, u"<font=3>" + self.colorCode(UnitInfo.getAirRange()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 6, iRow, u"<font=3>" + self.colorCode(iWithdrawal) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 7, iRow, u"<font=3>" + self.colorCode(iBomb) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

	def colorCode(self, iValue):
		sText = str(iValue)
		if iValue > 0:
			sText = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + sText + "</color>"
		elif iValue < 0:
			sText = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ()) + sText + "</color>"
		return sText

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)

		iRow = screen.appendTableRow("PlatyTable")
		if self.iGroup == -2:
			screen.selectRow("PlatyTable", iRow, True)
		sText = "<font=3>" + self.top.color3 + CyTranslator().getText("TXT_KEY_PEDIA_ALL_GROUPS", ()) + "</font></color>"
		screen.setTableText("PlatyTable", 0, iRow, sText, ",Art/Interface/Buttons/Promotions/Combat5.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,5,10", WidgetTypes.WIDGET_PYTHON, 6781, -2, CvUtil.FONT_LEFT_JUSTIFY )
		iRow = screen.appendTableRow("PlatyTable")
		if self.iGroup == -1:
			screen.selectRow("PlatyTable", iRow, True)
		sText = "<font=3>" + self.top.color3 + CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ()) + "</font></color>"
		screen.setTableText("PlatyTable", 0, iRow, sText, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), WidgetTypes.WIDGET_PYTHON, 6781, -1, CvUtil.FONT_LEFT_JUSTIFY )

		listSorted = self.top.sortUnitGroups(0)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sUnitCombatIcon, ()), self.iGroup, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, -1)

	def handleInput (self, inputClass):
		return 0