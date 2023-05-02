from CvPythonExtensions import *
import CvUtil
import ScreenInput
gc = CyGlobalContext()

class CvPediaBuildingChart:
	def __init__(self, main):
		self.top = main

	def interfaceScreen(self):		
		screen = self.top.getScreen()
		szTable = self.top.getNextWidgetName()
		iNumColumns = 8
		if self.top.iSortBChartType == 1:
			iNumColumns = YieldTypes.NUM_YIELD_TYPES * 2 + 2
		elif self.top.iSortBChartType == 2:
			iNumColumns = CommerceTypes.NUM_COMMERCE_TYPES * 2 + 2
		elif self.top.iSortBChartType == 3:
			iNumColumns = 7
		screen.addTableControlGFC(szTable, iNumColumns, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE + 6, self.top.W_ITEMS_PANE, self.top.H_ITEMS_PANE, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSort(szTable)
		screen.setTableColumnHeader(szTable, 0, "", self.top.W_ITEMS_PANE *3/10)
		iWidth = self.top.W_ITEMS_PANE *7/10 - 10
		iNumColumns -= 2
		if self.top.iSortBChartType == 0:
			screen.setTableColumnHeader(szTable, 1, CyTranslator().getText("[ICON_PRODUCTION]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 2, CyTranslator().getText("[ICON_HAPPY]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 3, CyTranslator().getText("[ICON_HEALTHY]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 4, CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 5, CyTranslator().getText("[ICON_DEFENSE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 6, CyTranslator().getText("[ICON_BAD_GOLD]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 7, "", 10)
		elif self.top.iSortBChartType == 1:
			for j in xrange(YieldTypes.NUM_YIELD_TYPES):
				screen.setTableColumnHeader(szTable, 1 + j * 2, u"%c" % gc.getYieldInfo(j).getChar(), iWidth/iNumColumns)
				screen.setTableColumnHeader(szTable, 2 + j * 2, u"%c%%" % gc.getYieldInfo(j).getChar(), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, YieldTypes.NUM_YIELD_TYPES * 2 + 1, "", 10)
		elif self.top.iSortBChartType == 2:
			for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				screen.setTableColumnHeader(szTable, 1 + j * 2, u"%c" % gc.getCommerceInfo(j).getChar(), iWidth/iNumColumns)
				screen.setTableColumnHeader(szTable, 2 + j * 2, u"%c%%" % gc.getCommerceInfo(j).getChar(), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, CommerceTypes.NUM_COMMERCE_TYPES * 2 + 1, "", 10)
		elif self.top.iSortBChartType == 3:
			screen.setTableColumnHeader(szTable, 1, CyTranslator().getText("TXT_KEY_LOCAL", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 2, CyTranslator().getText("TXT_KEY_TERRAIN_COAST", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 3, CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 4, CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ()) + CyTranslator().getText("[ICON_COMMERCE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 5, CyTranslator().getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()) + CyTranslator().getText("[ICON_COMMERCE]", ()), iWidth/iNumColumns)
			screen.setTableColumnHeader(szTable, 6, "", 10)

		for i in xrange(gc.getNumBuildingInfos()):
			if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and CyGame().isFinalInitialized():
				if not CyGame().isBuildingEverActive(i): continue
			Info = gc.getBuildingInfo(i)
			if self.top.iSortBChart == 0:
				if not isNationalWonderClass(Info.getBuildingClassType()): continue
			elif self.top.iSortBChart == 1:
				if not isTeamWonderClass(Info.getBuildingClassType()): continue
			elif self.top.iSortBChart == 2:
				if not isWorldWonderClass(Info.getBuildingClassType()): continue
			bDisplay = False
			if self.top.iSortBChartType == 0:
				bDisplay = True
				iRow = screen.appendTableRow(szTable)
				szCost = CyTranslator().getText("TXT_KEY_NON_APPLICABLE", ())
				iCost = Info.getProductionCost()
				if iCost > -1:
					szCost = str(iCost)
				screen.setTableInt(szTable, 1, iRow, u"<font=3>" + szCost + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 2, iRow, u"<font=3>" + self.colorCode(Info.getHappiness()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 3, iRow, u"<font=3>" + self.colorCode(Info.getHealth()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 4, iRow, u"<font=3>" + self.colorCode(Info.getGreatPeopleRateChange()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 5, iRow, u"<font=3>" + self.colorCode(Info.getDefenseModifier()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
				screen.setTableInt(szTable, 6, iRow, u"<font=3>" + self.colorCode(Info.getMaintenanceModifier()) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			elif self.top.iSortBChartType == 1:
				lTemp = []
				for j in xrange(YieldTypes.NUM_YIELD_TYPES):
					iData1 = Info.getYieldChange(j)
					lTemp.append(iData1)
					iData2 = Info.getYieldModifier(j)
					lTemp.append(iData2)
					if iData1 != 0 or iData2 != 0:
						bDisplay = True
				if bDisplay:
					iRow = screen.appendTableRow(szTable)
					for i in xrange(len(lTemp)):
						screen.setTableInt(szTable, 1 + i, iRow, u"<font=3>" + self.colorCode(lTemp[i]) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			elif self.top.iSortBChartType == 2:
				lTemp = []
				for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
					iData1 = Info.getObsoleteSafeCommerceChange(j)
					lTemp.append(iData1)
					iData2 = Info.getCommerceModifier(j)
					lTemp.append(iData2)
					if iData1 != 0 or iData2 != 0:
						bDisplay = True
				if bDisplay:
					iRow = screen.appendTableRow(szTable)
					for i in xrange(len(lTemp)):
						screen.setTableInt(szTable, 1 + i, iRow, u"<font=3>" + self.colorCode(lTemp[i]) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			elif self.top.iSortBChartType == 3:
				iData1 = Info.getTradeRoutes()
				iData2 = Info.getCoastalTradeRoutes()
				iData3 = Info.getGlobalTradeRoutes()
				iData4 = Info.getTradeRouteModifier()
				iData5 = Info.getForeignTradeRouteModifier()
				lTemp = [iData1, iData2, iData3, iData4, iData5]
				for iData in lTemp:
					if iData != 0:
						bDisplay = True
						break
				if bDisplay:
					iRow = screen.appendTableRow(szTable)
					for i in xrange(len(lTemp)):
						screen.setTableInt(szTable, 1 + i, iRow, u"<font=3>" + self.colorCode(lTemp[i]) + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			if bDisplay:
				screen.setTableText(szTable, 0, iRow, u"<font=3>" + Info.getDescription() + u"</font>", Info.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, i, 1, CvUtil.FONT_LEFT_JUSTIFY)

	def colorCode(self, iValue):
		sText = str(iValue)
		if iValue > 0:
			sText = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + sText + "</color>"
		elif iValue < 0:
			sText = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ()) + sText + "</color>"
		return sText

	def handleInput (self, inputClass):
		return 0