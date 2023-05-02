from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import PlatyOptions
gc = CyGlobalContext()

class CvReligionScreen:
	def __init__(self):
		self.CONVERT_NAME = "ReligionConvertButton"
		self.CANCEL_NAME = "ReligionCancelButton"
		self.DEBUG_DROPDOWN_ID =  "ReligionDropdownWidget"
		self.RELIGION_ANARCHY_WIDGET = "ReligionAnarchyWidget"

		self.Z_SCREEN = -6.1
		self.Y_TITLE = 8		
		self.Z_TEXT = self.Z_SCREEN - 0.2
		self.X_ANARCHY = 21

		self.iMaxReligions = 8		## Includes No State Religions
		self.X_RELIGION_AREA = 30
		self.Y_RELIGION_AREA = 80
		self.H_RELIGION_AREA = (self.iMaxReligions + 1) * 25 + 40
		self.Y_INFO_AREA = self.Y_RELIGION_AREA + self.H_RELIGION_AREA + 10

		self.iReligionSelected = -1
		self.iActivePlayer = -1

	def interfaceScreen (self):
		screen = CyGInterfaceScreen("ReligionScreen", CvScreenEnums.RELIGION_SCREEN)
		self.NO_STATE_BUTTON_ART = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
		self.CONVERT_TEXT = u"<font=4>" + CyTranslator().getText("TXT_KEY_RELIGION_CONVERT", ()).upper() + "</font>"
		self.CANCEL_TEXT = u"<font=4>" + CyTranslator().getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + "</font>"
		self.W_RELIGION_AREA = screen.getXResolution() /2 - self.X_RELIGION_AREA - 5
		
		self.iActivePlayer = gc.getGame().getActivePlayer()
		self.iReligionSelected = gc.getPlayer(self.iActivePlayer).getStateReligion()

		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)
## Unique Background ##
		screen.addDDSGFC("ScreenBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText(self.CANCEL_NAME, "Background", self.CANCEL_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)
		screen.showWindowBackground(False)

		# Header...
		screen.setLabel("ReligionScreenHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Make the scrollable areas for the city list...

		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		self.drawReligionInfo()
		self.drawCityInfo(self.iReligionSelected)
		self.placeInfo()

	def placeInfo(self):
		screen = CyGInterfaceScreen("ReligionScreen", CvScreenEnums.RELIGION_SCREEN)
		self.H_INFO_AREA = screen.getYResolution() - 180 - self.H_RELIGION_AREA - 84
		self.Y_ALLOW_AREA = self.Y_INFO_AREA + self.H_INFO_AREA + 10
		screen.deleteWidget("ReligionMovie")
		screen.deleteWidget("AllowsArea")
		if self.iReligionSelected == -1: return
		screen.addPanel("AllowsArea", "", "", False, True, self.X_RELIGION_AREA, self.Y_ALLOW_AREA, self.W_RELIGION_AREA, 84, PanelStyles.PANEL_STYLE_EMPTY)
		for eLoopUnit in xrange(gc.getNumUnitInfos()):
			if (gc.getUnitInfo(eLoopUnit).getPrereqReligion() == self.iReligionSelected):
				szButton = gc.getUnitInfo(eLoopUnit).getButton()
				if self.iActivePlayer > -1:
					szButton = gc.getPlayer(self.iActivePlayer).getUnitButton(eLoopUnit)
				screen.attachImageButton("AllowsArea", "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

		for eLoopBuilding in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(eLoopBuilding).getPrereqReligion() == self.iReligionSelected or gc.getBuildingInfo(eLoopBuilding).getHolyCity() == self.iReligionSelected:
				screen.attachImageButton("AllowsArea", "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )
		for iItem in xrange(gc.getNumPromotionInfos()):
			if gc.getPromotionInfo(iItem).getStateReligionPrereq() == self.iReligionSelected:
				screen.attachImageButton("AllowsArea", "", gc.getPromotionInfo(iItem).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iItem, 1, False )
		if CyUserProfile().getGraphicOption(GraphicOptionTypes.GRAPHICOPTION_NO_MOVIES):
			return
		self.szMovieFile = gc.getReligionInfo(self.iReligionSelected).getMovieFile()
		if self.szMovieFile:
			screen.addReligionMovieWidgetGFC("ReligionMovie", self.szMovieFile, self.X_RELIGION_AREA + 2, self.Y_INFO_AREA, self.W_RELIGION_AREA - 4, self.H_INFO_AREA, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
	# Draws the religion buttons and information		
	def drawReligionInfo(self):
		screen = CyGInterfaceScreen("ReligionScreen", CvScreenEnums.RELIGION_SCREEN)
		screen.addTableControlGFC("Religions", 3, self.X_RELIGION_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA, self.H_RELIGION_AREA, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		iWidth = self.W_RELIGION_AREA / 3
		screen.setTableColumnHeader("Religions", 0, "<font=3>" + CyTranslator().getText("[ICON_RELIGION]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ()) + "</font>", iWidth)
		sText = CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_FOUNDED", ())
		screen.setTableColumnHeader("Religions", 1, "<font=3>" + sText + "</font>", iWidth)
		sText = CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_HOLY_CITY", ())[:-1]
		screen.setTableColumnHeader("Religions", 2, "<font=3>" + sText + "</font>", iWidth)
		for i in xrange(gc.getNumReligionInfos() + 1):
			screen.appendTableRow("Religions")
		screen.enableSort("Religions")
		
		for i in xrange(gc.getNumReligionInfos()):			
			if CyGame().isReligionFounded(i):
				sButton = gc.getReligionInfo(i).getButton()
				sFounded = u"%s: %d%%" %(CyGameTextMgr().getTimeStr(gc.getGame().getReligionGameTurnFounded(i), false), CyGame().calculateReligionPercent(i))
				sFButton = ""
				FontType = CvUtil.FONT_CENTER_JUSTIFY
				sColor = ""
			else:
				sButton = gc.getReligionInfo(i).getButtonDisabled()
				sFounded = ""
				sFButton = ""
				iPrereq = gc.getReligionInfo(i).getTechPrereq()
				if iPrereq > -1:
					sFounded = gc.getTechInfo(iPrereq).getDescription()
					sFButton = gc.getReligionInfo(i).getTechButton()
				FontType = CvUtil.FONT_LEFT_JUSTIFY
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
			if i == self.iReligionSelected:
				sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
			if gc.getPlayer(self.iActivePlayer).getStateReligion() == i:
				sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setTableText("Religions", 0, i, sColor + "<font=3>" + gc.getReligionInfo(i).getDescription() + "</font></color>", sButton, WidgetTypes.WIDGET_HELP_RELIGION, i, 1, CvUtil.FONT_LEFT_JUSTIFY )
			screen.setTableText("Religions", 1, i, "<font=3>" + sFounded + "</font>", sFButton, WidgetTypes.WIDGET_GENERAL, -1, -1, FontType)

			pHolyCity = CyGame().getHolyCity(i)
			if pHolyCity.isNone():
				szFounded = ""
				sButton = ""
			elif not pHolyCity.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam(), False):
				szFounded = CyTranslator().getText("TXT_KEY_UNKNOWN", ())
				sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
			else:
				szFounded = pHolyCity.getName()
				sButton = gc.getCivilizationInfo(pHolyCity.getCivilizationType()).getButton()
			screen.setTableText("Religions", 2, i, "<font=3>" + szFounded + "</font>", sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		sColor = CyTranslator().getText("[COLOR_WHITE]", ())
		if self.iReligionSelected == -1 or self.iReligionSelected == gc.getNumReligionInfos():
			sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
		if gc.getPlayer(self.iActivePlayer).getStateReligion() == -1:
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
		screen.setTableText("Religions", 0, i + 1, sColor + "<font=3>" + CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_NO_STATE", ()) + "</font></color>",  self.NO_STATE_BUTTON_ART, WidgetTypes.WIDGET_HELP_RELIGION, -1, 1, CvUtil.FONT_LEFT_JUSTIFY )

	# Draws the city list
	def drawCityInfo(self, iReligion):
		screen = CyGInterfaceScreen("ReligionScreen", CvScreenEnums.RELIGION_SCREEN)
		self.X_CITY_AREA = screen.getXResolution() /2 + 5
		self.H_CITY_AREA = screen.getYResolution() - 160
## Transparent Panels ##
		PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			PanelStyle = PanelStyles.PANEL_STYLE_IN
## Transparent Panels ##
		screen.addPanel("ReligionAreaWidget", "", "", True, True, self.X_CITY_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA , self.H_CITY_AREA, PanelStyle)
		sButton = self.NO_STATE_BUTTON_ART
		sReligion = CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_NO_STATE", ())
		if iReligion > -1:
			sButton = gc.getReligionInfo(iReligion).getButton()
			sReligion = gc.getReligionInfo(iReligion).getDescription()
		screen.setLabel("ReligionName", "Background",  u"<font=3>" + sReligion.upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_CITY_AREA + self.W_RELIGION_AREA /2, self.Y_RELIGION_AREA+ 84, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setImageButton("ReligionButton", sButton, self.X_CITY_AREA + self.W_RELIGION_AREA /2 - 32, self.Y_RELIGION_AREA + 20, 64, 64, WidgetTypes.WIDGET_HELP_RELIGION, iReligion, 1)
			
		pPlayer = gc.getPlayer(self.iActivePlayer)
		szCities = u"<font=3>"
		(pLoopCity, iter) = pPlayer.firstCity(False)
		while(pLoopCity):
			if iter > 1:
				szCities += "\n"
			for i in xrange(gc.getNumReligionInfos()):
				if pLoopCity.isHolyCityByType(i):
					szCities += u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
				elif pLoopCity.isHasReligion(i):
					szCities += u"%c" %(gc.getReligionInfo(i).getChar())	
			if pLoopCity.isCapital():
				szCities += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)

			sColor = ""
			if iReligion > -1:
				if pLoopCity.isHolyCityByType(iReligion):
					sColor = CyTranslator().getText("[COLOR_YELLOW]", ())
				elif pLoopCity.isHasReligion(iReligion):
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			szCities += sColor + pLoopCity.getName() + "</color>" + "  "
		
			if iReligion == -1:
				bFirst = True
				for i in xrange(gc.getNumReligionInfos()):
					if pLoopCity.isHasReligion(i):
						szTempBuffer = CyGameTextMgr().getReligionHelpCity(i, pLoopCity, False, False, False, True)
						if szTempBuffer:
							if not bFirst:
								szCities += u", "
							szCities += szTempBuffer
							bFirst = False
			else:
				szCities += CyGameTextMgr().getReligionHelpCity(iReligion, pLoopCity, False, False, True, False)
			szCities += u"</font>"
			(pLoopCity, iter) = pPlayer.nextCity(iter, False)
		
		screen.addMultilineText("Child" + "ReligionAreaWidget", szCities, self.X_CITY_AREA+5, self.Y_RELIGION_AREA + 110, self.W_RELIGION_AREA  -10, self.H_CITY_AREA-120, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
		# Convert Button....
		iLink = 0
		if (gc.getPlayer(self.iActivePlayer).canChangeReligion()):
			iLink = 1
				
		if (not self.canConvert(iReligion) or iReligion == gc.getPlayer(self.iActivePlayer).getStateReligion()):			
			screen.setText(self.CONVERT_NAME, "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)
			screen.hide(self.CANCEL_NAME)
			szAnarchyTime = CyGameTextMgr().setConvertHelp(self.iActivePlayer, iReligion)
		else:
			screen.setText(self.CONVERT_NAME, "Background", self.CONVERT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CONVERT, iReligion, 1)
			screen.show(self.CANCEL_NAME)
			szAnarchyTime = CyTranslator().getText("TXT_KEY_ANARCHY_TURNS", (gc.getPlayer(self.iActivePlayer).getReligionAnarchyLength(), ))

		# Turns of Anarchy Text...
		screen.setLabel(self.RELIGION_ANARCHY_WIDGET, "Background", u"<font=3>" + szAnarchyTime + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ANARCHY, screen.getYResolution() - 42, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
															
	def canConvert(self, iReligion):
		iCurrentReligion = gc.getPlayer(self.iActivePlayer).getStateReligion()
		iConvertReligion = iReligion
		if iReligion == gc.getNumReligionInfos():
			iConvertReligion = -1						
		return (iConvertReligion != iCurrentReligion and gc.getPlayer(self.iActivePlayer).canConvert(iConvertReligion))		
		
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen("ReligionScreen", CvScreenEnums.RELIGION_SCREEN)
		if inputClass.getButtonType() == WidgetTypes.WIDGET_HELP_RELIGION:
			self.iReligionSelected = inputClass.getData1()
			self.drawReligionInfo()
			self.drawCityInfo(self.iReligionSelected)
			self.placeInfo()
			return 1
		if inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID:
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
			self.iReligionSelected = gc.getPlayer(self.iActivePlayer).getStateReligion()
			self.drawReligionInfo()
			self.drawCityInfo(self.iReligionSelected)
			self.placeInfo()
			return 1
		if inputClass.getFunctionName() == self.CONVERT_NAME:
			screen.hideScreen()
			return 1
		if inputClass.getFunctionName() == self.CANCEL_NAME:
			self.iReligionSelected = gc.getPlayer(self.iActivePlayer).getStateReligion()
			self.drawReligionInfo()
			self.drawCityInfo(self.iReligionSelected)
			self.placeInfo()
			return 1
		return 0
		
	def update(self, fDelta):
		return	