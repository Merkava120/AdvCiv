from CvPythonExtensions import *
import PyHelpers
import CvUtil
import ScreenInput
import CvScreenEnums
import PlatyOptions
gc = CyGlobalContext()

class CvFinanceAdvisor:

	def __init__(self):
		self.DEBUG_DROPDOWN_ID =  "FinanceAdvisorDropdownWidget"
		self.WIDGET_ID = "FinanceAdvisorWidget"
		self.Y_TITLE = 12
		self.TEXT_MARGIN = 15
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2
		
		self.nWidgetCount = 0

	def interfaceScreen (self):
		screen = CyGInterfaceScreen("FinanceAdvisor", CvScreenEnums.FINANCE_ADVISOR)
		self.iActiveLeader = CyGame().getActivePlayer()
		player = gc.getPlayer(self.iActiveLeader)
		self.X_TRADE = 30
		self.Y_TRADE = 80
		self.W_TRADE = screen.getXResolution() * 2/5
		self.Y_SPACING = 30
	
		if screen.isActive(): return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)
## Unique Background ##
		screen.addDDSGFC("ScreenBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.showWindowBackground(False)
		screen.setText("FinanceAdvisorExitWidget", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setLabel("FinanceAdvisorWidgetHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
		if CyGame().isDebugMode():
			screen.addDropDownBoxGFC(self.DEBUG_DROPDOWN_ID, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_PLAYERS()):
				if gc.getPlayer(j).isAlive():
					screen.addPullDownString(self.DEBUG_DROPDOWN_ID, gc.getPlayer(j).getName(), j, j, False )
		self.drawContents()

	def drawContents(self):
		screen = CyGInterfaceScreen("FinanceAdvisor", CvScreenEnums.FINANCE_ADVISOR)
		self.deleteAllWidgets()
		self.H_TRADE = screen.getYResolution() - 160
		self.X_INCOME = self.X_TRADE + self.W_TRADE + 10
		self.PANE_WIDTH = (screen.getXResolution() - 40 - self.X_INCOME) /2
		self.X_EXPENSES = self.X_INCOME + self.PANE_WIDTH + 10
		self.H_TREASURY = 100
		self.Y_LOCATION = self.Y_TRADE + self.H_TREASURY + 20
		self.PANE_HEIGHT = screen.getYResolution() - 80 - self.Y_LOCATION
		player = gc.getPlayer(self.iActiveLeader)
					
		totalUnitCost = player.calculateUnitCost()
		totalUnitSupply = player.calculateUnitSupply()
		totalMaintenance = player.getTotalMaintenance()
		totalCivicUpkeep = player.getCivicUpkeep([], False)
		totalPreInflatedCosts = player.calculatePreInflatedCosts()
		totalInflatedCosts = player.calculateInflatedCosts()
		goldCommerce = player.getCommerceRate(CommerceTypes.COMMERCE_GOLD)
		if not player.isCommerceFlexible(CommerceTypes.COMMERCE_RESEARCH):
			goldCommerce += player.calculateBaseNetResearch()
		goldFromCivs = player.getGoldPerTurn()

## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
		screen.addPanel(self.getNextWidgetName(), u"", "", True, True, self.X_INCOME, self.Y_TRADE, self.X_EXPENSES + self.PANE_WIDTH - self.X_INCOME, self.H_TREASURY, self.PanelStyle)
		screen.addPanel(self.getNextWidgetName(), u"", "", True, True, self.X_TRADE, self.Y_TRADE, self.W_TRADE, self.H_TRADE, self.PanelStyle)
		screen.addPanel(self.getNextWidgetName(), u"", "", True, True, self.X_INCOME, self.Y_LOCATION, self.PANE_WIDTH, self.PANE_HEIGHT, self.PanelStyle)
		screen.addPanel(self.getNextWidgetName(), u"", "", True, True, self.X_EXPENSES, self.Y_LOCATION, self.PANE_WIDTH, self.PANE_HEIGHT, self.PanelStyle)
## Transparent Panels ##
		iWidth = (self.W_TRADE - 40 - 24)/2
		screen.addTableControlGFC("TradeTable", 3, self.X_TRADE + 20, self.Y_TRADE + 20, self.W_TRADE - 40, self.H_TRADE - 40, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("TradeTable", 0, CyTranslator().getText("[ICON_TRADE]", ()), 24)
		screen.setTableColumnHeader("TradeTable", 1, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()), iWidth)
		screen.setTableColumnHeader("TradeTable", 2, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), iWidth)
		screen.enableSort("TradeTable")

		iCivilization = player.getCivilizationType()
		for i in xrange(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getOwner() != self.iActiveLeader: continue
			iBonus = pPlot.getBonusType(-1)
			if iBonus == -1: continue
			BonusInfo = gc.getBonusInfo(iBonus)
			if not gc.getTeam(player.getTeam()).isHasTech(gc.getBonusInfo(iBonus).getTechReveal()): continue
			iRow = screen.appendTableRow("TradeTable")
			pCity = CyMap().findCity(pPlot.getX(), pPlot.getY(), self.iActiveLeader, -1, False, False, -1, -1, CyCity())
			if pPlot.isPlotGroupConnectedBonus(self.iActiveLeader, iBonus):
				screen.setTableText("TradeTable", 0, iRow, CyTranslator().getText("[ICON_TRADE]", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("TradeTable", 1, iRow, "<font=3>" + BonusInfo.getDescription() + "</font>", BonusInfo.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, 1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("TradeTable", 2, iRow, "<font=3>" + pCity.getName() + "</font>", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, pCity.getOwner(), pCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
			
		yLocation  = self.Y_LOCATION + self.TEXT_MARGIN
		screen.setLabel(self.getNextWidgetName(), "Background",  "<font=4>" + CyTranslator().getText("TXT_KEY_CONCEPT_COMMERCE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_INCOME + self.PANE_WIDTH/2, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		xLocation = self.X_INCOME + self.TEXT_MARGIN
		
		yLocation += self.Y_SPACING /2
		for eCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			if eCommerce == CommerceTypes.COMMERCE_GOLD: continue
			if (player.isCommerceFlexible(eCommerce)):
				yLocation += self.Y_SPACING
				screen.setButtonGFC("IncreasePercent" + str(eCommerce), "", "", xLocation, yLocation, 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.setButtonGFC("DecreasePercent" + str(eCommerce), "", "", xLocation + 24, yLocation, 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )

				szText = u"<font=3>%c: %d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), player.getCommercePercent(eCommerce))
				screen.setLabel(self.getNextWidgetName(), "Background",  szText, CvUtil.FONT_LEFT_JUSTIFY, xLocation + 50, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				szRate = u"<font=3>" + unicode(player.getCommerceRate(CommerceTypes(eCommerce))) + u"</font>"
				screen.setLabel(self.getNextWidgetName(), "Background", szRate, CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Income
		yLocation += 2 * self.Y_SPACING
		screen.setLabel(self.getNextWidgetName(), "Background",  u"<font=4>" + CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_INCOME_HEADER", ()).upper() + u"</color></font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_INCOME + self.PANE_WIDTH/2, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )	
		iIncome = 0
		yLocation += self.Y_SPACING * 3/2

		xLocation = self.X_INCOME + self.TEXT_MARGIN
		if player.isCommerceFlexible(CommerceTypes.COMMERCE_GOLD):
			screen.setButtonGFC("IncreasePercent" + str(CommerceTypes.COMMERCE_GOLD), u"", "", xLocation, yLocation, 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, CommerceTypes.COMMERCE_GOLD, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
			screen.setButtonGFC("DecreasePercent" + str(CommerceTypes.COMMERCE_GOLD), u"", "", xLocation + 24, yLocation, 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, CommerceTypes.COMMERCE_GOLD, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )
			xLocation = self.X_INCOME + self.TEXT_MARGIN + 50

		szText = u"<font=3>%c: %d%%</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(), player.getCommercePercent(CommerceTypes.COMMERCE_GOLD))
		screen.setLabel(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, xLocation, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_GROSS_INCOME, -1, -1 )
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(goldCommerce) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_GROSS_INCOME, -1, -1 )
		iIncome += goldCommerce

		if goldFromCivs > 0:
			yLocation += self.Y_SPACING
			szText = unicode(goldFromCivs) + " : " + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_PER_TURN", ())
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_PER_TURN", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(goldFromCivs) + "</color></font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
			iIncome += goldFromCivs

		yLocation += 1.5 * self.Y_SPACING
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_INCOME", ()) + "</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_INCOME + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + str(iIncome) + "</color></font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_INCOME + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Expenses
		yLocation = self.Y_LOCATION + self.TEXT_MARGIN
		screen.setLabel(self.getNextWidgetName(), "Background",  u"<font=4>" + CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ()) + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_EXPENSES_HEADER", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH/2, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		iExpenses = 0

		yLocation += self.Y_SPACING * 3/2
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_UNITCOST", ()) + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_EXPENSES + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_UNIT_COST, self.iActiveLeader, 1)
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(totalUnitCost) + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_UNIT_COST, self.iActiveLeader, 1)
		iExpenses += totalUnitCost

		yLocation += self.Y_SPACING
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_UNITSUPPLY", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_EXPENSES + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_AWAY_SUPPLY, self.iActiveLeader, 1)
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(totalUnitSupply) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_AWAY_SUPPLY, self.iActiveLeader, 1)
		iExpenses += totalUnitSupply

		yLocation += self.Y_SPACING
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_MAINTENANCE", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_EXPENSES + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CITY_MAINT, self.iActiveLeader, 1)
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(totalMaintenance) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CITY_MAINT, self.iActiveLeader, 1)
		iExpenses += totalMaintenance

		yLocation += self.Y_SPACING
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_CIVICS", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_EXPENSES + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CIVIC_UPKEEP, self.iActiveLeader, 1)
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(totalCivicUpkeep) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_CIVIC_UPKEEP, self.iActiveLeader, 1)
		iExpenses += totalCivicUpkeep

		if (goldFromCivs < 0):
			yLocation += self.Y_SPACING
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_COST_PER_TURN", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_EXPENSES + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
			screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(-goldFromCivs) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_FOREIGN_INCOME, self.iActiveLeader, 1)
			iExpenses -= goldFromCivs

		yLocation += self.Y_SPACING
		iInflation = totalInflatedCosts - totalPreInflatedCosts
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_INFLATION", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_EXPENSES + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_INFLATED_COSTS, self.iActiveLeader, 1)
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + str(iInflation) + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_FINANCE_INFLATED_COSTS, self.iActiveLeader, 1)
		iExpenses += iInflation

		yLocation += self.Y_SPACING * 3/2
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ()) + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_EXPENSES", ()) + "</color></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_EXPENSES + self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ()) + str(iExpenses) + "</color></font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXPENSES + self.PANE_WIDTH - self.TEXT_MARGIN, yLocation, self.Z_CONTROLS + self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		yLocation += self.Y_SPACING * 3/2
		iCashflow = iIncome - iExpenses
		sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		if iCashflow < 0:
			sColor = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_TREASURY", (player.getGold(), )).upper(), CvUtil.FONT_CENTER_JUSTIFY, (self.X_INCOME + self.PANE_WIDTH + self.X_EXPENSES)/2, self.Y_TRADE + self.H_TREASURY/2 - self.Y_SPACING, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_HELP_FINANCE_GOLD_RESERVE, -1, -1 )
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + sColor + CyTranslator().getText("TXT_KEY_FINANCIAL_ADVISOR_NET_INCOME", (iCashflow,)) + "</color></font>", CvUtil.FONT_CENTER_JUSTIFY, (self.X_INCOME + self.PANE_WIDTH + self.X_EXPENSES)/2, self.Y_TRADE + self.H_TREASURY/2, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = CyGInterfaceScreen("FinanceAdvisor", CvScreenEnums.FINANCE_ADVISOR)
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1
		self.nWidgetCount = 0
			
	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen("FinanceAdvisor", CvScreenEnums.FINANCE_ADVISOR)
		if inputClass.getButtonType() == WidgetTypes.WIDGET_ZOOM_CITY:
			screen.hideScreen()			
			CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), true)
## Commerce Flexibles ##
		elif inputClass.getFunctionName().find("IncreasePercent") > -1:
			if CyInterface().shiftKey():
				CyMessageControl().sendModNetMessage(5678, inputClass.getData1(), 100, -1, -1)
		elif inputClass.getFunctionName().find("DecreasePercent") > -1:
			if CyInterface().shiftKey():
				CyMessageControl().sendModNetMessage(5678, inputClass.getData1(), 0, -1, -1)
## Commerce Flexibles ##
		elif inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID:
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.iActiveLeader = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
			self.drawContents()
		return

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Financial_Screen_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Financial_Screen_DIRTY_BIT, False)
			self.drawContents()
		return