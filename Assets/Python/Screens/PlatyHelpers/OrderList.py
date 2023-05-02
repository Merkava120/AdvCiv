from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class OrderList:
	def __init__(self):
		self.bUpdateOrder = False
		self.iOrderType = 0
		self.iCombatType = -2
		self.iWonderType = 0

	def interfaceScreen(self):
		screen = CyGInterfaceScreen("OrderList", CvScreenEnums.ORDER_LIST)
		global pCity
		global iOrderWidth
		pCity = CyInterface().getHeadSelectedCity()
		iOrderWidth = screen.getXResolution()/4 - 20

		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setLabel("OrderHeader", "Background", u"<font=4b>" + pCity.getName().upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText("OrderExit", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 25, screen.getYResolution() - 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		screen.addDropDownBoxGFC("OrderType", 20, 20, iOrderWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("OrderType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()), 0, 0, 0 == self.iOrderType)
		screen.addPullDownString("OrderType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), 1, 1, 1 == self.iOrderType)
		screen.addPullDownString("OrderType", CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()), 2, 2, 2 == self.iOrderType)
		screen.addPullDownString("OrderType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 3, 3, 3 == self.iOrderType)
		screen.addPullDownString("OrderType", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROCESS", ()), 4, 4, 4 == self.iOrderType)

		screen.addDropDownBoxGFC("CombatType", screen.getXResolution() - 20 - iOrderWidth, 20, iOrderWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("CombatType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), -2, -2, -2 == self.iCombatType)
		screen.addPullDownString("CombatType", CyTranslator().getText("TXT_PEDIA_NON_COMBAT",()), -1, -1, -1 == self.iCombatType)
		for i in xrange(gc.getNumUnitCombatInfos()):
			screen.addPullDownString("CombatType", gc.getUnitCombatInfo(i).getDescription(), i, i, i == self.iCombatType)

		screen.addDropDownBoxGFC("WonderType", screen.getXResolution() - 20 - iOrderWidth, 20, iOrderWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("WonderType", CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), 0, 0, 0 == self.iWonderType)
		screen.addPullDownString("WonderType", CyTranslator().getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ()), 1, 1, 1 == self.iWonderType)
		screen.addPullDownString("WonderType", CyTranslator().getText("TXT_KEY_PEDIA_TEAM_WONDER", ()), 2, 2, 2 == self.iWonderType)
		screen.addPullDownString("WonderType", CyTranslator().getText("TXT_KEY_PEDIA_WORLD_WONDER", ()), 3, 3, 3 == self.iWonderType)

		self.drawOrderTable()
		self.drawSelectionTable()

	def drawSelectionTable(self):
		screen = CyGInterfaceScreen("OrderList", CvScreenEnums.ORDER_LIST)
		iWidth = screen.getXResolution() * 3/4 - 40
		iHeight = screen.getYResolution() - 100
		screen.hide("CombatType")
		screen.hide("WonderType")

		if self.iOrderType == 0:
			screen.show("CombatType")
			screen.addTableControlGFC("SelectionTable", 8, iOrderWidth + 40, 60, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
			screen.setTableColumnHeader("SelectionTable", 0, "", 24)
			screen.setTableColumnHeader("SelectionTable", 1, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()), (iWidth - 24)/4)
			screen.setTableColumnHeader("SelectionTable", 2, u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR), (iWidth - 24)/8)
			screen.setTableColumnHeader("SelectionTable", 3, u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR), (iWidth - 24)/8)
			screen.setTableColumnHeader("SelectionTable", 4, u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), (iWidth - 24)/8)
			screen.setTableColumnHeader("SelectionTable", 5, "<font=2>" + CyTranslator().getText("TXT_KEY_PEDIA_AIR_RANGE", ()) + "</font>", (iWidth - 24)/8)
			screen.setTableColumnHeader("SelectionTable", 6, "<font=2>" + CyTranslator().getText("TXT_KEY_PEDIA_WITHDRAWAL", ()) + "</font>", (iWidth - 24)/8)
			screen.setTableColumnHeader("SelectionTable", 7, "<font=2>" + CyTranslator().getText("TXT_KEY_MISSION_BOMBARD", ()) + "</font>", (iWidth - 24)/8)
			screen.enableSort("SelectionTable")

			for i in xrange (gc.getNumUnitClassInfos()):
				item = gc.getCivilizationInfo(pCity.getCivilizationType()).getCivilizationUnits(i)
				if item == -1: continue
				if pCity.canTrain(item, False, True):
					Info = gc.getUnitInfo(item)
					iCombat = Info.getUnitCombatType()
					if self.iCombatType != iCombat and self.iCombatType > -2: continue
					
					iRow = screen.appendTableRow("SelectionTable")
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					sText = ""
					if iCombat > -1:
						sButton = gc.getUnitCombatInfo(iCombat).getButton()
						sText = gc.getUnitCombatInfo(iCombat).getDescription()
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					if not pCity.canTrain(item, False, False):
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
					screen.setTableText("SelectionTable", 0, iRow, sText, sButton, WidgetTypes.WIDGET_PYTHON, 6781, iCombat, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText("SelectionTable", 1, iRow, sColor + Info.getDescription() + "</color>", Info.getButton(), WidgetTypes.WIDGET_TRAIN, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if Info.getDomainType() == DomainTypes.DOMAIN_AIR:
						iStrength = Info.getAirCombat()
						iBomb = Info.getBombRate()
						iWithdrawal = Info.getEvasionProbability()
					else:
						iStrength = Info.getCombat()
						iBomb = Info.getBombardRate()
						iWithdrawal = Info.getWithdrawalProbability()
					screen.setTableInt("SelectionTable", 2, iRow, str(iStrength), "", WidgetTypes.WIDGET_TRAIN, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 3, iRow, str(Info.getMoves()), "", WidgetTypes.WIDGET_TRAIN, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 4, iRow, str(Info.getProductionCost()), "", WidgetTypes.WIDGET_TRAIN, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 5, iRow, str(Info.getAirRange()), "", WidgetTypes.WIDGET_TRAIN, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 6, iRow, str(iWithdrawal), "", WidgetTypes.WIDGET_TRAIN, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 7, iRow, str(iBomb), "", WidgetTypes.WIDGET_TRAIN, i, -1, CvUtil.FONT_LEFT_JUSTIFY)

		elif self.iOrderType == 3:
			screen.addTableControlGFC("SelectionTable", 3, iOrderWidth + 40, 60, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
			screen.setTableColumnHeader("SelectionTable", 0, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), iWidth/2)
			screen.setTableColumnHeader("SelectionTable", 1, CyTranslator().getText("TXT_KEY_SPACE_SHIP_SCREEN_TYPE_BUTTON", ()), iWidth/3)
			screen.setTableColumnHeader("SelectionTable", 2, CyTranslator().getText("[ICON_PRODUCTION]", ()), iWidth/6)
			screen.enableSort("SelectionTable")

			for item in xrange (gc.getNumProjectInfos()):
				if pCity.canCreate(item, False, True):
					iRow = screen.appendTableRow("SelectionTable")
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					if not pCity.canCreate(item, False, False):
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
					Info = gc.getProjectInfo(item)
					screen.setTableText("SelectionTable", 0, iRow, sColor + Info.getDescription() + "</color>", Info.getButton(), WidgetTypes.WIDGET_CREATE, item, -1, CvUtil.FONT_LEFT_JUSTIFY)
					sText = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
					if isWorldProject(item):
						sText = CyTranslator().getText("TXT_KEY_PEDIA_WORLD_PROJECT", ())
					elif isTeamProject(item):
						sText = CyTranslator().getText("TXT_KEY_PEDIA_TEAM_PROJECT", ())
					screen.setTableText("SelectionTable", 1, iRow, sText, "", WidgetTypes.WIDGET_CREATE, item, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 2, iRow, str(Info.getProductionCost()), "", WidgetTypes.WIDGET_CREATE, item, -1, CvUtil.FONT_LEFT_JUSTIFY)

		elif self.iOrderType == 4:
			screen.addTableControlGFC("SelectionTable", CommerceTypes.NUM_COMMERCE_TYPES + 1, iOrderWidth + 40, 60, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
			screen.setTableColumnHeader("SelectionTable", 0, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROCESS", ()), iWidth/2)
			screen.enableSort("SelectionTable")
			for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				screen.setTableColumnHeader("SelectionTable", i + 1, u"%c" %(gc.getCommerceInfo(i).getChar()), iWidth/2 /CommerceTypes.NUM_COMMERCE_TYPES)

			for item in xrange (gc.getNumProcessInfos()):
				if pCity.canMaintain(item, False):
					iRow = screen.appendTableRow("SelectionTable")
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					Info = gc.getProcessInfo(item)
					screen.setTableText("SelectionTable", 0, iRow, sColor + Info.getDescription() + "</color>", Info.getButton(), WidgetTypes.WIDGET_MAINTAIN, item, -1, CvUtil.FONT_LEFT_JUSTIFY)
					for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
						screen.setTableInt("SelectionTable", i + 1, iRow, str(Info.getProductionToCommerceModifier(i)), "", WidgetTypes.WIDGET_MAINTAIN, item, -1, CvUtil.FONT_LEFT_JUSTIFY)

		else:
			if self.iOrderType == 2:
				screen.show("WonderType")
			iNumColumns = YieldTypes.NUM_YIELD_TYPES + CommerceTypes.NUM_COMMERCE_TYPES + 4
			screen.addTableControlGFC("SelectionTable", iNumColumns, iOrderWidth + 40, 60, iWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
			iColumnWidth = iWidth/(iNumColumns + 2)
			screen.setTableColumnHeader("SelectionTable", 0, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), iColumnWidth * 3)
			screen.setTableColumnHeader("SelectionTable", 1, CyTranslator().getText("[ICON_PRODUCTION]", ()), iColumnWidth)
			screen.setTableColumnHeader("SelectionTable", 2, CyTranslator().getText("[ICON_HAPPY]", ()), iColumnWidth)
			screen.setTableColumnHeader("SelectionTable", 3, CyTranslator().getText("[ICON_HEALTHY]", ()), iColumnWidth)
			for j in xrange(YieldTypes.NUM_YIELD_TYPES):
				screen.setTableColumnHeader("SelectionTable", 4 + j, u"%c" % gc.getYieldInfo(j).getChar(), iColumnWidth)
			for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				screen.setTableColumnHeader("SelectionTable", 4 + j + YieldTypes.NUM_YIELD_TYPES, u"%c" % gc.getCommerceInfo(j).getChar(), iColumnWidth)
			screen.enableSort("SelectionTable")

			for i in xrange (gc.getNumBuildingClassInfos()):
				if self.iOrderType == 1:
					if isLimitedWonderClass(i): continue
				else:
					if not isLimitedWonderClass(i): continue
					if self.iWonderType == 1 and not isNationalWonderClass(i): continue
					if self.iWonderType == 2 and not isTeamWonderClass(i): continue
					if self.iWonderType == 3 and not isWorldWonderClass(i): continue
				item = gc.getCivilizationInfo(pCity.getCivilizationType()).getCivilizationBuildings(i)
				if item == -1: continue
				if pCity.canConstruct(item, False, True, False):
					iRow = screen.appendTableRow("SelectionTable")
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					if not pCity.canConstruct(item, False, False, False):
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
					Info = gc.getBuildingInfo(item)
					screen.setTableText("SelectionTable", 0, iRow, sColor + Info.getDescription() + "</color>", Info.getButton(), WidgetTypes.WIDGET_CONSTRUCT, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 1, iRow, str(Info.getProductionCost()), "", WidgetTypes.WIDGET_CONSTRUCT, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 2, iRow, str(pCity.getBuildingHappiness(item)), "", WidgetTypes.WIDGET_CONSTRUCT, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableInt("SelectionTable", 3, iRow, str(pCity.getBuildingHealth(item)), "", WidgetTypes.WIDGET_CONSTRUCT, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					for j in xrange(YieldTypes.NUM_YIELD_TYPES):
						screen.setTableInt("SelectionTable", 4 + j, iRow, str(Info.getYieldChange(j) + pCity.getBuildingYieldChange(i, j)), "", WidgetTypes.WIDGET_CONSTRUCT, i, -1, CvUtil.FONT_LEFT_JUSTIFY)
					for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
						screen.setTableInt("SelectionTable", 4 + YieldTypes.NUM_YIELD_TYPES + j, iRow, str(pCity.getBuildingCommerceByBuilding(j, item)), "", WidgetTypes.WIDGET_CONSTRUCT, i, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def drawOrderTable(self):
		screen = CyGInterfaceScreen("OrderList", CvScreenEnums.ORDER_LIST)
		iHeight = screen.getYResolution() - 100
		screen.addTableControlGFC("OrderTable", 2, 20, 60, iOrderWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("OrderTable", 0, "", iOrderWidth)

		for i in xrange(CyInterface().getNumOrdersQueued()):
			szLeftBuffer = ""
			szRightBuffer = ""
				
			if CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN:
				szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
				szButton = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getButton()
				szRightBuffer = " (" + str(pCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

				if CyInterface().getOrderNodeSave(i):
					szLeftBuffer = "*" + szLeftBuffer

			elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT:
				szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
				szButton = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getButton()
				szRightBuffer = " (" + str(pCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i))+ ")"

			elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CREATE:
				szLeftBuffer = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getDescription()
				szButton = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getButton()
				szRightBuffer = " (" + str(pCity.getProjectProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i))+ ")"

			elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_MAINTAIN:
				szLeftBuffer = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getDescription()
				szButton = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getButton()
			iRow = screen.appendTableRow("OrderTable")
			szLeftBuffer += szRightBuffer
			screen.setTableText("OrderTable", 0, iRow, szLeftBuffer, szButton, WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
		
	def handleInput (self, inputClass):
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			screen = CyGInterfaceScreen("OrderList", CvScreenEnums.ORDER_LIST)
			if inputClass.getFunctionName() == "OrderType":
				self.iOrderType = inputClass.getData()
				self.drawSelectionTable()
			elif inputClass.getFunctionName() == "CombatType":
				iIndex = screen.getSelectedPullDownID("CombatType")
				self.iCombatType = screen.getPullDownData("CombatType", iIndex)
				self.drawSelectionTable()
			elif inputClass.getFunctionName() == "WonderType":
				iIndex = screen.getSelectedPullDownID("WonderType")
				self.iWonderType = screen.getPullDownData("WonderType", iIndex)
				self.drawSelectionTable()
			elif inputClass.getFunctionName() == "OrderTable" or inputClass.getFunctionName() == "SelectionTable":
				self.bUpdateOrder = True
		return 0

	def update(self, fDelta):
		if self.bUpdateOrder:
			self.drawOrderTable()
			self.bUpdateOrder = False
		return 1