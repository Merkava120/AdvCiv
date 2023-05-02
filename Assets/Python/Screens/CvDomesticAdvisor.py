from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

bWonder = False
iDomesticPage = 0
iMaxAirCapacity = 0 ## debug assert if global define is called too early
listSelectedCities = []
lCities = []
lSpecialists = []

class CvDomesticAdvisor:
	def interfaceScreen(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		global iPlayer
		global pPlayer
		global lSpecialists
		global listSelectedCities
		global lCities
		global iMaxAirCapacity

		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		listSelectedCities = []
		lSpecialists = []
		for i in xrange(gc.getNumSpecialistInfos()):
			if gc.getSpecialistInfo(i).isVisible():
				lSpecialists.append(i)

		self.nScreenWidth = screen.getXResolution()
		self.nScreenHeight = screen.getYResolution() - 200
		self.nTableWidth = self.nScreenWidth - 40
		self.nTableHeight = self.nScreenHeight - 125

		self.nFirstSpecialistX = 30
		self.nSpecialistY = self.nScreenHeight - 55
		self.nSpecialistWidth = 32
		self.nSpecialistLength = 32
		self.nSpecialistDistance = 100

		# Offset from Specialist Image/Size for the Specialist Plus/Minus buttons
		self.nPlusOffsetX = -4
		self.nMinusOffsetX = 16
		self.nPlusOffsetY = self.nMinusOffsetY = 30
		self.nPlusWidth = self.nPlusHeight = self.nMinusWidth = self.nMinusHeight = 20

		# Offset from Specialist Image for the Specialist Text
		self.nSpecTextOffsetX = 40
		self.nSpecTextOffsetY = 10

		screen.setRenderInterfaceOnly(True)
		screen.setDimensions(0, 60, self.nScreenWidth, self.nScreenHeight)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.addPanel("DomesticAdvisorBG", u"", u"", True, False, 0, 0, self.nScreenWidth, self.nScreenHeight, PanelStyles.PANEL_STYLE_MAIN)
		screen.setText("DomesticExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.nScreenWidth - 30, self.nScreenHeight - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText("DomesticHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_TITLE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.nScreenWidth/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)
		screen.addDropDownBoxGFC("DomesticPage", 20, 20, 184, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("DomesticPage", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL", ()), 0, 0, iDomesticPage == 0)
		screen.addPullDownString("DomesticPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ()), 1, 1, iDomesticPage == 1)
		screen.addPullDownString("DomesticPage", CyTranslator().getText("TXT_KEY_CONCEPT_CULTURE", ()), 2, 2, iDomesticPage == 2)
		screen.addPullDownString("DomesticPage", CyTranslator().getText("TXT_KEY_CONCEPT_AIR_UNITS", ()), 3, 3, iDomesticPage == 3)
		screen.addPullDownString("DomesticPage", CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ()), 4, 4, iDomesticPage == 4)
		screen.addPullDownString("DomesticPage", CyTranslator().getText("TXT_KEY_CONCEPT_COMBAT", ()), 5, 5, iDomesticPage == 5)

		bCanLiberate = False
		lCities = []
		(pCity, i) = pPlayer.firstCity(False)
		while(pCity):
			szName = pCity.getName()
			if pCity.isCapital():
				szName += CyTranslator().getText("[ICON_STAR]", ())
			elif pCity.isGovernmentCenter():
				szName += CyTranslator().getText("[ICON_SILVER_STAR]", ())
			for iReligion in xrange(gc.getNumReligionInfos()):
				if pCity.isHasReligion(iReligion):
					if pCity.isHolyCityByType(iReligion):
						szName += (u"%c" % gc.getReligionInfo(iReligion).getHolyCityChar())
					else:
						szName += (u"%c" % gc.getReligionInfo(iReligion).getChar())
			for iCorporation in xrange(gc.getNumCorporationInfos()):
				if pCity.isHeadquartersByType(iCorporation):
					szName += (u"%c" % gc.getCorporationInfo(iCorporation).getHeadquarterChar())
				elif pCity.isActiveCorporation(iCorporation):
					szName += (u"%c" % gc.getCorporationInfo(iCorporation).getChar())
			if pCity.getLiberationPlayer(false) > -1:
				if not gc.getTeam(gc.getPlayer(pCity.getLiberationPlayer(false)).getTeam()).isAtWar(CyGame().getActiveTeam()) :
					szName = CyTranslator().getText("[ICON_OCCUPATION]", ()) + szName 
					bCanLiberate = True
			lCities.append([szName, pCity.getID()])
			iMaxAirCapacity = max(gc.getDefineINT("CITY_AIR_UNIT_CAPACITY"), pCity.getAirUnitCapacity(pCity.getTeam()))
			(pCity, i) = pPlayer.nextCity(i, false)
		lCities.sort()

		if bCanLiberate or pPlayer.canSplitEmpire():
			screen.setImageButton("DomesticSplit", "", self.nScreenWidth - 110, self.nScreenHeight - 45, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FREE_COLONY).getActionInfoIndex(), -1)
			screen.setStyle("DomesticSplit", "Button_HUDAdvisorVictory_Style")

		self.drawContents()
		self.drawSpecialists()
		screen.updateAppropriateCitySelection("DomesticTable", pPlayer.getNumCities(), 1)

	def drawContents(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		screen.hide("AdvisorWonder")
		if iDomesticPage == 0:
			self.GeneralTable()
		elif iDomesticPage == 1:
			self.SpecialistTable()
		elif iDomesticPage == 2:
			self.CultureTable()
		elif iDomesticPage == 3:
			self.AirTable()
		elif iDomesticPage == 4:
			self.TradeTable()
		elif iDomesticPage == 5:
			self.MilitaryTable()

	def addColor(self, iValue, iType):
		sColor = ""
		sValue = str(iValue)
		if iType == 0:
			if iValue < 0:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			elif iValue > 0:
				sColor = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())
		elif iType == 1:
			if iValue > 0:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			elif iValue < 0:
				sColor = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ())
		elif iType == 2 or iType == 3:
			if iValue >= 75:
				sColor = CyTranslator().getText("[COLOR_GREEN]", ())
			elif iValue >= 50:
				sColor = CyTranslator().getText("[COLOR_CYAN]", ())
			elif iValue >= 25:
				sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
			sValue += "%"
			if iType == 3 and iValue > 0:
				sValue = "+" + sValue
		return sColor + sValue + "</color>"

	def MilitaryTable(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		screen.addTableControlGFC("DomesticTable", DomainTypes.NUM_DOMAIN_TYPES * 2 + 2, 20, 90, self.nTableWidth, self.nTableHeight - 30, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("DomesticTable", True)
		screen.enableSort("DomesticTable")
		
		iWidth = (self.nTableWidth - 174)/(DomainTypes.NUM_DOMAIN_TYPES * 2)
		screen.setTableColumnHeader("DomesticTable", 0, "", 24)
		screen.setTableColumnHeader("DomesticTable", 1, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 150)
		for i in xrange(DomainTypes.NUM_DOMAIN_TYPES):
			screen.setLabel("Domestic" + str(i), "Background", "<font=3b>" + gc.getDomainInfo(i).getDescription() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, 204 + iWidth * (i * 2 + 1), 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setTableColumnHeader("DomesticTable", i * 2 + 2, CyTranslator().getText("INTERFACE_PANE_EXPERIENCE", ()), iWidth)
			screen.setTableColumnHeader("DomesticTable", i * 2 + 3, CyTranslator().getText("TXT_KEY_CONCEPT_PRODUCTION", ()), iWidth)
		screen.enableSort( "DomesticTable" )
		screen.setStyle("DomesticTable", "Table_StandardCiv_Style")

		iCivilization = pPlayer.getCivilizationType()
		for i in xrange(len(lCities)):
			pCity = pPlayer.getCity(lCities[i][1])
			iRow = screen.appendTableRow("DomesticTable")
			screen.setTableText("DomesticTable", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, iPlayer, pCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("DomesticTable", 1, iRow, lCities[i][0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			for j in xrange(DomainTypes.NUM_DOMAIN_TYPES):
				iXP = pCity.getDomainFreeExperience(j) + pCity.getSpecialistFreeExperience() + pPlayer.getFreeExperience()
				screen.setTableInt("DomesticTable", j * 2 + 2, iRow, self.addColor(iXP, 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt("DomesticTable", j * 2 + 3, iRow, self.addColor(pCity. getDomainProductionModifier(j), 3), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			
	def TradeTable(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		screen.addTableControlGFC("DomesticTable", 9, 20, 60, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("DomesticTable", True)
		screen.enableSort("DomesticTable")
		
		iWidth = (self.nTableWidth - 174)/13
		screen.setTableColumnHeader("DomesticTable", 0, "", 24)
		screen.setTableColumnHeader("DomesticTable", 1, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 150)
		screen.setTableColumnHeader("DomesticTable", 2, CyTranslator().getText("[ICON_STAR]", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 3, CyTranslator().getText("[ICON_TRADE]", ()), iWidth * 2)
		screen.setTableColumnHeader("DomesticTable", 4, CyTranslator().getText("TXT_KEY_LOCAL", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth * 2)
		screen.setTableColumnHeader("DomesticTable", 5, CyTranslator().getText("TXT_KEY_FOREIGN", ()) + CyTranslator().getText("[ICON_TRADE]", ()), iWidth * 2)
		screen.setTableColumnHeader("DomesticTable", 6, CyTranslator().getText("TXT_KEY_LOCAL", ()) + CyTranslator().getText("[ICON_COMMERCE]", ()), iWidth * 2)
		screen.setTableColumnHeader("DomesticTable", 7, CyTranslator().getText("TXT_KEY_FOREIGN", ()) + CyTranslator().getText("[ICON_COMMERCE]", ()), iWidth * 2)
		screen.setTableColumnHeader("DomesticTable", 8, CyTranslator().getText("TXT_KEY_BONUS_TOTAL", ()) + CyTranslator().getText("[ICON_COMMERCE]", ()), iWidth * 2)
		screen.enableSort( "DomesticTable" )
		screen.setStyle("DomesticTable", "Table_StandardCiv_Style")

		iCivilization = pPlayer.getCivilizationType()
		for i in xrange(len(lCities)):
			pCity = pPlayer.getCity(lCities[i][1])
			iRow = screen.appendTableRow("DomesticTable")
			screen.setTableText("DomesticTable", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, iPlayer, pCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("DomesticTable", 1, iRow, lCities[i][0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if pCity.isConnectedToCapital(iPlayer):
				screen.setTableText("DomesticTable", 2, iRow, CyTranslator().getText("[ICON_TRADE]", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			iLocal = 0
			iForeign = 0
			iTradeRoutes = 0
			iMaxRoutes = pCity.getTradeRoutes()
			for i in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
				pLoopCity = pCity.getTradeCity(i)
				if pLoopCity and pLoopCity.getOwner() > -1:
					iTradeRoutes += 1
					iTradeProfit = pCity.calculateTradeYield(YieldTypes.YIELD_COMMERCE, pCity.calculateTradeProfit(pLoopCity))
					if pLoopCity.getOwner() == iPlayer:
						iLocal += iTradeProfit
					else:
						iForeign += iTradeProfit
				else:
					break
			sTradeRoutes = str(iTradeRoutes)
			if iTradeRoutes < iMaxRoutes:
				sTradeRoutes += "/" + str(iMaxRoutes)
			screen.setTableInt("DomesticTable", 3, iRow, sTradeRoutes, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			iModifier = pCity.getTradeRouteModifier()
			screen.setTableInt("DomesticTable", 4, iRow, self.addColor(iModifier, 3), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			iModifier = pCity.getTradeRouteModifier() + pCity.getForeignTradeRouteModifier()
			screen.setTableInt("DomesticTable", 5, iRow, self.addColor(iModifier, 3), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 6, iRow, self.addColor(iLocal, 1) + CyTranslator().getText("[ICON_COMMERCE]", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 7, iRow, self.addColor(iForeign, 1) + CyTranslator().getText("[ICON_COMMERCE]", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 8, iRow, self.addColor(iLocal + iForeign, 1) + CyTranslator().getText("[ICON_COMMERCE]", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

	def AirTable(self):
		iMaxAirCapacity = gc.getDefineINT("CITY_AIR_UNIT_CAPACITY")
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		screen.addTableControlGFC("DomesticTable", iMaxAirCapacity + 5, 20, 60, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("DomesticTable", True)
		screen.enableSort("DomesticTable")
		
		iWidth = (self.nTableWidth - 174 - 150)/(iMaxAirCapacity)
		screen.setTableColumnHeader("DomesticTable", 0, "", 24)
		screen.setTableColumnHeader("DomesticTable", 1, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 150)
		screen.setTableColumnHeader("DomesticTable", 2, CyTranslator().getText("[ICON_TRADE]", ()), 50)
		screen.setTableColumnHeader("DomesticTable", 3, CyTranslator().getText("[ICON_DEFENSE]", ()), 50)
		screen.setTableColumnHeader("DomesticTable", 4, CyTranslator().getText("[ICON_POWER]", ()), 50)
		for i in xrange(iMaxAirCapacity):
			screen.setTableColumnHeader("DomesticTable", i + 5, str(i + 1), iWidth)
		screen.enableSort( "DomesticTable" )
		screen.setStyle("DomesticTable", "Table_StandardCiv_Style")

		iCivilization = pPlayer.getCivilizationType()
		for i in xrange(len(lCities)):
			pCity = pPlayer.getCity(lCities[i][1])
			iRow = screen.appendTableRow("DomesticTable")
			screen.setTableText("DomesticTable", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, iPlayer, pCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("DomesticTable", 1, iRow, lCities[i][0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iMax = pCity.getMaxAirlift()
			iDiff = iMax - pCity.getCurrAirlift()
			sColor = ""
			sText = str(iDiff)
			if iMax > 0:
				if iDiff == iMax:
					sColor = CyTranslator().getText("[COLOR_GREEN]", ())
				else:
					sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
					if iDiff == 0:
						sColor = CyTranslator().getText("[COLOR_RED]", ())
					sText += "/" + str(iMax)
			screen.setTableInt("DomesticTable", 2, iRow, sColor + sText + "</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 3, iRow, self.addColor(-pCity.getAirModifier(), 2), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 4, iRow, str(pCity.getAirUnitCapacity(pCity.getTeam())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			iCount = 5
			for iUnit in xrange(pCity.plot().getNumUnits()):
				pUnit = pCity.plot().getUnit(iUnit)
				if pUnit.isNone(): continue
				if pUnit.getTeam() != pCity.getTeam(): continue
				if pUnit.getDomainType() != DomainTypes.DOMAIN_AIR: continue
				if pUnit.isCargo(): continue
				if gc.getUnitInfo(pUnit.getUnitType()).getAirUnitCap() == 0: continue
				sColor = u"<color=%d,%d,%d,%d>" %(gc.getPlayer(pUnit.getOwner()).getPlayerTextColorR(), gc.getPlayer(pUnit.getOwner()).getPlayerTextColorG(), gc.getPlayer(pUnit.getOwner()).getPlayerTextColorB(), gc.getPlayer(pUnit.getOwner()).getPlayerTextColorA())
				sText = sColor + pUnit.getName() + "</color>"
				screen.setTableText("DomesticTable", iCount, iRow, sText, pUnit.getButton(), WidgetTypes.WIDGET_PYTHON, 8202, pUnit.getUnitType(), CvUtil.FONT_LEFT_JUSTIFY)
				iCount += 1
			for i in xrange(iMaxAirCapacity - pCity.getAirUnitCapacity(pCity.getTeam())):
				screen.setTableText("DomesticTable", pCity.getAirUnitCapacity(pCity.getTeam()) + 5 + i, iRow, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
	def CultureTable(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		screen.addTableControlGFC("DomesticTable", 11, 20, 60, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("DomesticTable", True)
		screen.enableSort("DomesticTable")

		iWidth = (self.nTableWidth - 174)/9
		screen.setTableColumnHeader("DomesticTable", 0, "", 24)
		screen.setTableColumnHeader("DomesticTable", 1, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 150)
		screen.setTableColumnHeader("DomesticTable", 2, CyTranslator().getText("[ICON_CULTURE]", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 3, CyTranslator().getText("[ICON_CULTURE]", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 4, CyTranslator().getText("TXT_KEY_RATE", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 5, CyTranslator().getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 6, CyTranslator().getText("[ICON_DEFENSE]", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 7, CyTranslator().getText("TXT_KEY_NATIONALITY", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 8, CyTranslator().getText("[ICON_OCCUPATION]", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 9, CyTranslator().getText("[ICON_STAR]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 10, CyTranslator().getText("[ICON_SILVER_STAR]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()), iWidth)

		iCivilization = pPlayer.getCivilizationType()
		for i in xrange(len(lCities)):
			pCity = pPlayer.getCity(lCities[i][1])
			sTurns = ""
			iCultureTimes100 = pCity.getCultureTimes100(iPlayer)
			iCultureRateTimes100 = pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
			if iCultureRateTimes100 > 0:
				iCultureLeftTimes100 = 100 * pCity.getCultureThreshold() - iCultureTimes100
				if iCultureLeftTimes100 > 0:
					sTurns = str((iCultureLeftTimes100 + iCultureRateTimes100 - 1) / iCultureRateTimes100)

			iRow = screen.appendTableRow("DomesticTable")
			screen.setTableText("DomesticTable", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, iPlayer, pCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("DomesticTable", 1, iRow, lCities[i][0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("DomesticTable", 2, iRow, gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 3, iRow, str(pCity.getCulture(iPlayer)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 4, iRow, self.addColor(pCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 5, iRow, sTurns, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			iDefense = pCity.getDefenseModifier(False)
			sText = str(iDefense)
			sColor = CyTranslator().getText("[COLOR_GREEN]", ())
			iMax = pCity.getTotalDefense(False)
			if iDefense < iMax:
				sColor = CyTranslator().getText("[COLOR_RED]", ())
				sText += "/" + str(iMax)
			screen.setTableInt("DomesticTable", 6, iRow, sColor + sText + "</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 7, iRow, self.addColor(pCity.plot().calculateCulturePercent(iPlayer), 2), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 8, iRow, self.addColor(pCity.getOccupationTimer(), 0), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 9, iRow, self.addColor(pCity.getNumWorldWonders(), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 10, iRow, self.addColor(pCity.getNumNationalWonders(), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

	def SpecialistTable(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		screen.addTableControlGFC("DomesticTable", len(lSpecialists) + 4, 20, 60, self.nTableWidth, self.nTableHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("DomesticTable", True)
		screen.enableSort("DomesticTable")

		screen.setTableColumnHeader("DomesticTable", 0, "", 24)
		screen.setTableColumnHeader("DomesticTable", 1, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 150)
		iWidth = (self.nTableWidth - 174)/(len(lSpecialists) * 2 + 2)
		screen.setTableColumnHeader("DomesticTable", 2, CyTranslator().getText("TXT_KEY_RATE", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 3, CyTranslator().getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()), iWidth)
		for i in xrange(len(lSpecialists)):
			screen.setTableColumnHeader("DomesticTable", i + 4, gc.getSpecialistInfo(lSpecialists[i]).getDescription(), iWidth * 2)

		iCivilization = pPlayer.getCivilizationType()
		for i in xrange(len(lCities)):
			pCity = pPlayer.getCity(lCities[i][1])
			iRow = screen.appendTableRow("DomesticTable")
			screen.setTableText("DomesticTable", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, iPlayer, pCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("DomesticTable", 1, iRow, lCities[i][0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iProgress = pCity.getGreatPeopleProgress()
			iRate = pCity.getGreatPeopleRate()
			sTurns = ""
			if iRate > 0:
				iGPPLeft = pPlayer.greatPeopleThreshold(false) - iProgress
				if iGPPLeft > 0:
					sTurns = str((iGPPLeft + iRate - 1) / iRate)
			screen.setTableInt("DomesticTable", 2, iRow, self.addColor(iRate, 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableInt("DomesticTable", 3, iRow, sTurns, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
			for j in xrange(len(lSpecialists)):
				iSpecialist = lSpecialists[j]
				sMax = str(pCity.getMaxSpecialistCount(iSpecialist))
				if sMax == "0" and pCity.isSpecialistValid(iSpecialist, 1):
					sMax = "--"
				sText = u"%d/%s</font>" %(pCity.getSpecialistCount(iSpecialist), sMax)
				sButton = ""
				if iWidth * 2 >= 90:
					sButton = gc.getSpecialistInfo(iSpecialist).getButton()
				screen.setTableInt("DomesticTable", iSpecialist + 4, iRow, sText, sButton, WidgetTypes.WIDGET_PYTHON, 7879, iSpecialist, CvUtil.FONT_CENTER_JUSTIFY)

	def GeneralTable(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		bEspionage = not CyGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE)
		screen.addTableControlGFC("DomesticTable", 17 + bEspionage, 20, 60, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect("DomesticTable", True)
		screen.enableSort("DomesticTable")

		iWidth = (self.nTableWidth - 180 - 174)/(12 + bEspionage)
		screen.setTableColumnHeader("DomesticTable", 0, "", 24)
		screen.setTableColumnHeader("DomesticTable", 1, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()), 150)
		screen.setTableColumnHeader("DomesticTable", 2, u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR), iWidth)
		screen.setTableColumnHeader("DomesticTable", 3, u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR), iWidth)
		screen.setTableColumnHeader("DomesticTable", 4, u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR), iWidth)
		screen.setTableColumnHeader("DomesticTable", 5, u"%c" % gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iWidth)
		screen.setTableColumnHeader("DomesticTable", 6, u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar(), iWidth)
		screen.setTableColumnHeader("DomesticTable", 7, u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(), iWidth)
		screen.setTableColumnHeader("DomesticTable", 8, u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar(), iWidth)
		if bEspionage:
			screen.setTableColumnHeader("DomesticTable", 9, u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar(), iWidth)
		screen.setTableColumnHeader("DomesticTable", 9 + bEspionage, u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), iWidth)
		screen.setTableColumnHeader("DomesticTable", 10 + bEspionage, u"%c" % CyGame().getSymbolID(FontSymbols.TRADE_CHAR), iWidth)
		screen.setTableColumnHeader("DomesticTable", 11 + bEspionage, u"%c" % CyGame().getSymbolID(FontSymbols.BAD_GOLD_CHAR), iWidth)
		screen.setTableColumnHeader("DomesticTable", 12 + bEspionage, CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 13 + bEspionage, CyTranslator().getText("[ICON_DEFENSE]", ()), iWidth)
		screen.setTableColumnHeader("DomesticTable", 14 + bEspionage, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_PRODUCING", ()), 180)

		iCivilization = pPlayer.getCivilizationType()
		for i in xrange(len(lCities)):
			pCity = pPlayer.getCity(lCities[i][1])
			iRow = screen.appendTableRow("DomesticTable")
			screen.setTableText("DomesticTable", 0, iRow, "", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, iPlayer, pCity.getID(), CvUtil.FONT_CENTER_JUSTIFY)
			screen.setTableText("DomesticTable", 1, iRow, lCities[i][0], "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableInt("DomesticTable", 2, iRow, self.addColor(pCity.getPopulation(), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 3, iRow, self.addColor(pCity.happyLevel() - pCity.unhappyLevel(0), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 4, iRow, self.addColor(pCity.goodHealth() - pCity.badHealth(0), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 5, iRow, self.addColor(pCity.foodDifference(True), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 6, iRow, self.addColor(pCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 7, iRow, self.addColor(pCity.getCommerceRate(CommerceTypes.COMMERCE_GOLD), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 8, iRow, self.addColor(pCity.getCommerceRate(CommerceTypes.COMMERCE_RESEARCH), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			if bEspionage:
				screen.setTableInt("DomesticTable", 9, iRow, self.addColor(pCity.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 9 + bEspionage, iRow, self.addColor(pCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 10 + bEspionage, iRow, self.addColor(pCity.getTradeYield(YieldTypes.YIELD_COMMERCE), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 11 + bEspionage, iRow, self.addColor(pCity.getMaintenance(), 0), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 12 + bEspionage, iRow, self.addColor(pCity.getGreatPeopleRate(), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			screen.setTableInt("DomesticTable", 13 + bEspionage, iRow, self.addColor(pCity.plot().getNumDefenders(iPlayer), 1), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

			if pCity.isProduction():
				sButton = ""
				if pCity.getProductionBuilding() > -1:
					sButton = gc.getBuildingInfo(pCity.getProductionBuilding()).getButton()
				elif pCity.getProductionProject() > -1:
					sButton = gc.getProjectInfo(pCity.getProductionProject()).getButton()
				elif pCity.getProductionUnit() > -1:
					sButton = gc.getUnitInfo(pCity.getProductionUnit()).getButton()
				elif pCity.getProductionProcess() > -1:
					sButton = gc.getProcessInfo(pCity.getProductionProcess()).getButton()
				screen.setTableText("DomesticTable", 14 + bEspionage, iRow, pCity.getProductionName() + " (" + str(pCity.getGeneralProductionTurnsLeft()) + ")", sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

			if pCity.getName() in listSelectedCities:
				screen.selectRow("DomesticTable", iRow, True)

	def drawSpecialists(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		for i in xrange( gc.getNumSpecialistInfos() ):
			if gc.getSpecialistInfo(i).isVisible():			
				screen.setImageButton("SpecialistImage" + str(i), gc.getSpecialistInfo(i).getTexture(), self.nFirstSpecialistX + (self.nSpecialistDistance * i), self.nSpecialistY, self.nSpecialistWidth, self.nSpecialistLength, WidgetTypes.WIDGET_CITIZEN, i, -1)
				screen.setButtonGFC("SpecialistPlus" + str(i), u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nPlusOffsetX, self.nSpecialistY + self.nPlusOffsetY, self.nPlusWidth, self.nPlusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
				screen.setButtonGFC("SpecialistMinus" + str(i), u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nMinusOffsetX, self.nSpecialistY + self.nMinusOffsetY, self.nMinusWidth, self.nMinusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
				screen.setLabel("SpecialistText" + str(i), "Background", "", CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.updateSpecialists()

	def hideSpecialists(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		for i in xrange(gc.getNumSpecialistInfos()):
			if gc.getSpecialistInfo(i).isVisible():			
				screen.hide("SpecialistImage" + str(i))
				screen.hide("SpecialistPlus" + str(i))
				screen.hide("SpecialistMinus" + str(i))
				screen.hide("SpecialistText" + str(i))
				
	def updateSpecialists(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		if CyInterface().isOneCitySelected():
			city = CyInterface().getHeadSelectedCity()
			nPopulation = city.getPopulation()
			nFreeSpecial = city.totalFreeSpecialists()

			for i in xrange(gc.getNumSpecialistInfos()):
				if gc.getSpecialistInfo(i).isVisible():	
					szName = "SpecialistImage" + str(i)
					screen.show(szName)
					
					szName = "SpecialistText" + str(i)
					screen.setLabel(szName, "Background", str (city.getSpecialistCount(i)) + "/" + str(city.getMaxSpecialistCount(i)), CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.show(szName)

					szName = "SpecialistPlus" + str(i)
					screen.hide(szName)
					if city.isSpecialistValid(i, 1) and (city.getForceSpecialistCount(i) < (nPopulation + nFreeSpecial)):
						screen.show(szName)

					szName = "SpecialistMinus" + str(i)
					screen.hide(szName)
					if city.getSpecialistCount(i) > 0 or city.getForceSpecialistCount(i) > 0:
						screen.show(szName)
		else:
			self.hideSpecialists()
				
	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		global bWonder
		global iDomesticPage

		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			if inputClass.getFunctionName() == "DomesticPage":
				iDomesticPage = screen.getPullDownData("DomesticPage", screen.getSelectedPullDownID("DomesticPage"))
				self.drawContents()
			elif inputClass.getFunctionName() == "DomesticTable":
				if inputClass.getMouseX() == 0:
					screen.hideScreen()
					CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), True)
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setText(u"showDomesticAdvisor")
					popupInfo.addPopup(inputClass.getData1())		
				else:
					self.updateAppropriateCitySelection()
					self.updateSpecialists()

		elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if inputClass.getFunctionName() == "DomesticSplit":
				screen.hideScreen()

			elif inputClass.getFunctionName() == "AdvisorWonder":
				bWonder = not bWonder
				self.drawContents()
		return 0
	
	def updateAppropriateCitySelection(self):
		screen = CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)
		global listSelectedCities
		nCities = gc.getPlayer(gc.getGame().getActivePlayer()).getNumCities()
		self.listSelectedCities = []
		for i in xrange(nCities):
			if screen.isRowSelected("DomesticTable", i):
				listSelectedCities.append(screen.getTableText("DomesticTable", 2, i))
		screen.updateAppropriateCitySelection("DomesticTable", nCities, 1)
								
	def update(self, fDelta):
		if CyInterface().isDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT) == True:
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, False)
			self.drawContents()
			self.updateSpecialists()
		return