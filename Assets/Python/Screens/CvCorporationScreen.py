from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import PlatyOptions
gc = CyGlobalContext()

class CvCorporationScreen:
	def __init__(self):
		self.CANCEL_NAME = "CorporationCancelButton"
		self.DEBUG_DROPDOWN_ID =  "CorporationDropdownWidget"
		self.AREA_ID =  "CorporationAreaWidget"
		self.Y_TITLE = 8

		self.X_CORPORATION_AREA = 30
		self.Y_CORPORATION_AREA = 80
		self.iMinBonusRow = 6

		self.iCorporationSelected = -1
		self.iActivePlayer = -1
		self.bScreenUp = False
			
	def getScreen(self):
		return CyGInterfaceScreen("CorporationScreen", CvScreenEnums.CORPORATION_SCREEN)

	def interfaceScreen (self):

		self.SCREEN_ART = CyArtFileMgr().getInterfaceArtInfo("TECH_BG").getPath()
		self.CANCEL_TEXT = u"<font=4>" + CyTranslator().getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + "</font>"
		
		self.iActivePlayer = gc.getGame().getActivePlayer()
		self.iCorporationSelected = -1

		self.bScreenUp = True

		screen = self.getScreen()
		if screen.isActive(): return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)
## Unique Background ##
		screen.addDDSGFC("ScreenBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
## Transparent Panels ##
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText(self.CANCEL_NAME, "Background", self.CANCEL_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 35, -6.3, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)

		screen.showWindowBackground(False)

		# Make the scrollable areas for the city list...

		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		self.drawCorporationInfo()
		self.drawCityInfo(self.iCorporationSelected)

	# Draws the Corporation buttons and information		
	def drawCorporationInfo(self):
		screen = self.getScreen()
		self.W_CORPORATION_AREA = screen.getXResolution()/2 - self.X_CORPORATION_AREA - 5
		self.H_CORPORATION_AREA = min((gc.getNumCorporationInfos() + 1) * 25 + 40, screen.getYResolution() - 190 - self.iMinBonusRow * 25)
		screen.hide("BonusRequired")
		screen.addTableControlGFC("Corporations", 5, self.X_CORPORATION_AREA, self.Y_CORPORATION_AREA, self.W_CORPORATION_AREA, self.H_CORPORATION_AREA, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("Corporations", 0, "<font=3>" + CyTranslator().getText("[ICON_GOLD]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ()) + "</font>", self.W_CORPORATION_AREA/3)
		screen.setTableColumnHeader("Corporations", 1, "<font=3>" + CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_FOUNDED", ()) + "</font>", self.W_CORPORATION_AREA/3)
		screen.setTableColumnHeader("Corporations", 2, "<font=3>" + CyTranslator().getText("TXT_KEY_CORPORATION_HEADQUARTERS", ()) + "</font>", self.W_CORPORATION_AREA/3)
		screen.enableSort("Corporations")
		
		for i in xrange(gc.getNumCorporationInfos()):
			screen.appendTableRow("Corporations")
			sGreatPerson = ""
			sGreatButton = ""
			for iBuilding in xrange(gc.getNumBuildingInfos()):
				if (gc.getBuildingInfo(iBuilding).getFoundsCorporation() == i):
					for iUnit in xrange(gc.getNumUnitInfos()):
						if gc.getUnitInfo(iUnit).getBuildings(iBuilding) or gc.getUnitInfo(iUnit).getForceBuildings(iBuilding):
							sGreatButton = gc.getUnitInfo(iUnit).getButton()
							sGreatPerson = gc.getUnitInfo(iUnit).getDescription()
							break
					break
			if CyGame().isCorporationFounded(i):
				sFounded = CyGameTextMgr().getTimeStr(gc.getGame().getCorporationGameTurnFounded(i), false)
				sButton = ""
				sColor = CyTranslator().getText("[COLOR_WHITE]", ())
				Font = CvUtil.FONT_CENTER_JUSTIFY
			else:
				sFounded = sGreatPerson
				sButton = sGreatButton
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				Font = CvUtil.FONT_LEFT_JUSTIFY
			if gc.getTeam(gc.getPlayer(self.iActivePlayer).getTeam()).hasHeadquarters(i):
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			if i == self.iCorporationSelected:
				sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())

			screen.setTableText("Corporations", 0, i, sColor + gc.getCorporationInfo(i).getDescription() + "</color>", gc.getCorporationInfo(i).getButton(), WidgetTypes.WIDGET_PYTHON, 8201, i, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("Corporations", 1, i, sFounded, sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, Font)

			pHeadquarters = CyGame().getHeadquarters(i)
			if pHeadquarters.isNone():
				szFounded = ""
				sButton = ""
			elif not pHeadquarters.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam(), False):
				szFounded = CyTranslator().getText("TXT_KEY_UNKNOWN", ())
				sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
			else:
				szFounded = pHeadquarters.getName()
				sButton = gc.getCivilizationInfo(pHeadquarters.getCivilizationType()).getButton()
			screen.setTableText("Corporations", 2, i, szFounded, sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.deleteWidget("AllowsArea")
		if self.iCorporationSelected == -1: return
		self.Y_BONUS_AREA = self.Y_CORPORATION_AREA + self.H_CORPORATION_AREA + 10
		self.H_BONUS_AREA = screen.getYResolution() - self.Y_BONUS_AREA - 80
		screen.addPanel("AllowsArea", "", "", False, True, self.X_CORPORATION_AREA, self.Y_BONUS_AREA, self.W_CORPORATION_AREA, self.H_BONUS_AREA, self.PanelStyle)

		screen.addTableControlGFC("BonusRequired", 5, self.X_CORPORATION_AREA, self.Y_BONUS_AREA, self.W_CORPORATION_AREA, self.H_BONUS_AREA, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		iWidth = (self.W_CORPORATION_AREA - 150) /4
		screen.setTableColumnHeader("BonusRequired", 0, "<font=3>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()) + "</font>", 150)
		screen.setTableColumnHeader("BonusRequired", 1, "<font=3>" + CyTranslator().getText("TXT_KEY_LOCAL", ()) + "</font>", iWidth)
		screen.setTableColumnHeader("BonusRequired", 2, "<font=3>" + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()) + "</font>", iWidth)
		screen.setTableColumnHeader("BonusRequired", 3, "<font=3>" + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_IMPORTS_TEXT", ()) + "</font>", iWidth)
		screen.setTableColumnHeader("BonusRequired", 4, "<font=3>" + CyTranslator().getText("TXT_KEY_BONUS_TOTAL", ()) + "</font>", iWidth)
		screen.enableSort("BonusRequired")
		
		for i in xrange(gc.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES")):
			eBonus = gc.getCorporationInfo(self.iCorporationSelected).getPrereqBonus(i)
			if eBonus > -1:
				iRow = screen.appendTableRow("BonusRequired")
				screen.setTableText("BonusRequired", 0, iRow, gc.getBonusInfo(eBonus).getDescription(), gc.getBonusInfo(eBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, 1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt("BonusRequired", 1, iRow, str(gc.getPlayer(self.iActivePlayer).countOwnedBonuses(eBonus)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt("BonusRequired", 2, iRow, str(gc.getPlayer(self.iActivePlayer).getBonusExport(eBonus)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt("BonusRequired", 3, iRow, str(gc.getPlayer(self.iActivePlayer).getBonusImport(eBonus)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt("BonusRequired", 4, iRow, str(gc.getPlayer(self.iActivePlayer).getNumAvailableBonuses(eBonus)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

	def drawCityInfo(self, iCorporation):
	
		if (not self.bScreenUp):
			return
			
		screen = self.getScreen()
		screen.addPanel(self.AREA_ID, "", "", True, True, screen.getXResolution()/2 + 5, self.Y_CORPORATION_AREA, self.W_CORPORATION_AREA, screen.getYResolution() - 160, self.PanelStyle)
		sButton = ""
		sCorporation = ""
		if iCorporation > -1:
			sButton = gc.getCorporationInfo(iCorporation).getButton()
			sCorporation = gc.getCorporationInfo(iCorporation).getDescription()
		screen.setLabel("CorporationName", "Background",  u"<font=3>" + sCorporation.upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2 + 5 + self.W_CORPORATION_AREA/2, self.Y_CORPORATION_AREA+ 84, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setImageButton("CorporationButton", sButton, screen.getXResolution()/2 + 5 + self.W_CORPORATION_AREA/2 - 32, self.Y_CORPORATION_AREA + 20, 64, 64, WidgetTypes.WIDGET_PYTHON, 8201, iCorporation)
					
		pPlayer = gc.getPlayer(self.iActivePlayer)
		
		szCities = u"<font=3>"
		(pLoopCity, iter) = pPlayer.firstCity(False)
		while(pLoopCity):
			if iter > 1:
				szCities += "\n"

			for j in xrange(gc.getNumCorporationInfos()):
				if pLoopCity.isHeadquartersByType(j):
					szCities += u"%c" %(gc.getCorporationInfo(j).getHeadquarterChar())
				elif pLoopCity.isHasCorporation(j):
					szCities += u"%c" %(gc.getCorporationInfo(j).getChar())

			if pLoopCity.isCapital():
				szCities += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
	
			sColor = ""
			if iCorporation > -1:
				if pLoopCity.isHeadquartersByType(iCorporation):
					sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
				elif pLoopCity.isHasCorporation(iCorporation):
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			szCities += sColor + pLoopCity.getName() + "</color>" + " "

			for k in xrange(YieldTypes.NUM_YIELD_TYPES):
				if iCorporation == -1:
					iYieldChange = pLoopCity.getCorporationYield(k)
				else:
					iYieldChange = pLoopCity.getCorporationYieldByCorporation(k, iCorporation)
				if iYieldChange != 0:
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())									
					if iYieldChange > 0:
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					szCities += sColor + (u"%d%c" % (iYieldChange, gc.getYieldInfo(k).getChar())) + "</color>"
	
			for k in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				if iCorporation == -1:
					iCommerceChange = pLoopCity.getCorporationCommerce(k)
				else:
					iCommerceChange = pLoopCity.getCorporationCommerceByCorporation(k, iCorporation)
				if iCommerceChange != 0:
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())									
					if iCommerceChange > 0:
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					szCities += sColor + (u"%d%c" % (iCommerceChange, gc.getCommerceInfo(k).getChar())) + "</color>"
			if iCorporation == -1:
				iMaintenance = pLoopCity.calculateCorporationMaintenance()
				if iMaintenance > 0:
					szCities += CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + "-" + str(iMaintenance) + CyTranslator().getText("[ICON_GOLD]", ()) + "</color>"
			else:
				sText = CyGameTextMgr().getCorporationHelpCity(iCorporation, pLoopCity, False, False)
				while sText.find("-") > -1:
					sText = sText[sText.find("-")+1:]
				if sText:
					szCities += CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + "-" + sText + "</color>"
			szCities += u"</font>"
			(pLoopCity, iter) = pPlayer.nextCity(iter, False)
		
		screen.addMultilineText("Child" + self.AREA_ID, szCities, screen.getXResolution()/2 + 5+5, self.Y_CORPORATION_AREA+110, self.W_CORPORATION_AREA-10, screen.getYResolution() - 280, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
													
		# Header...
		screen.setLabel("CorporationScreenHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_CORPORATION_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE, -2.3, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("CorporationExitButton", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -2.3, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
		screen.show(self.CANCEL_NAME)
		if self.iCorporationSelected == -1:
			screen.hide(self.CANCEL_NAME)

	def handleInput (self, inputClass):
		screen = self.getScreen()
		if inputClass.getFunctionName() == "Corporations":
			self.iCorporationSelected = inputClass.getData2()
		elif inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID:
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
			self.iCorporationSelected = -1
		elif inputClass.getFunctionName() == self.CANCEL_NAME:	
			self.iCorporationSelected = -1
		self.drawCorporationInfo()
		self.drawCityInfo(self.iCorporationSelected)
		return

	def update(self, fDelta):
		return	