from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import PlatyOptions
gc = CyGlobalContext()

class CvEspionageAdvisor:

	def __init__(self):
		self.WIDGET_ID = "EspionageAdvisorWidget"
		self.Y_TITLE = 12		
		self.nWidgetCount = 0
		self.iTargetPlayer = -1
		self.iActiveCityID = -1
		self.iChange = 1
		self.iMission = 1
		self.iButtonSize = 28
		self.iIconSize = 48

	def getScreen(self):
		return CyGInterfaceScreen("EspionageAdvisor", CvScreenEnums.ESPIONAGE_ADVISOR)

	def interfaceScreen (self):
		self.iTargetPlayer = -1		
		self.iActiveCityID = -1
		self.iActivePlayer = CyGame().getActivePlayer()
	
		screen = self.getScreen()
		if screen.isActive(): return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)
## Unique Background ##
		screen.addDDSGFC("ScreenBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
		screen.addPanel("EspionageTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel("EspionageBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.setText("EspionageAdvisorExitWidget", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setLabel("EspionageAdvisorWidgetHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iX = 20
		iY = screen.getYResolution() - 40
		iWidth = 100
		screen.addDropDownBoxGFC("ChangeBy", iX, iY, iWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		i = 1
		while i < 101:
			screen.addPullDownString("ChangeBy", "(+/-) " + str(i), i, i, self.iChange == i)
			if str(i)[0] == "1":
				i *= 5
			else:
				i *= 2
		iX += iWidth
		iY += (30 - self.iButtonSize) /2
		screen.setButtonGFC("WeightPlus", "", "", iX, iY, self.iButtonSize, self.iButtonSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
		iX += self.iButtonSize
		screen.setButtonGFC("WeightMinus", "", "", iX, iY, self.iButtonSize, self.iButtonSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
		iX += self.iButtonSize
		screen.setLabel("WeightTarget", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
		if CyGame().isDebugMode():
			screen.addDropDownBoxGFC("EspionageAdvisorDropdownWidget", screen.getXResolution() - 220, 12, 200, WidgetTypes.WIDGET_GENERAL, 554, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_CIV_PLAYERS()):
				if gc.getPlayer(j).isAlive():
					screen.addPullDownString("EspionageAdvisorDropdownWidget", gc.getPlayer(j).getName(), j, j, False )

		self.drawContents()
		self.drawTable()
		self.refreshScreen()

## Add "," ##
	def addComma(self, iValue):
		sTemp = str(iValue)
		sStart = ""
		while len(sTemp) > 0:
			if sTemp[0].isdigit(): break
			sStart += sTemp[0]
			sTemp = sTemp[1:]
		sEnd = sTemp[-3:]
		while len(sTemp) > 3:
			sTemp = sTemp[:-3]
			sEnd = sTemp[-3:] + "," + sEnd
		return (sStart + sEnd)
## Add "," ##
	def drawContents(self):
		self.deleteAllWidgets()
		screen = self.getScreen()

		self.X_LEFT_PANE = 15
		self.Y_LEFT_PANE = 70
		self.W_LEFT_PANE = screen.getXResolution() * 2/5 - 20
		self.iPanelWidth = self.W_LEFT_PANE - 40
		self.H_LEFT_PANE = screen.getYResolution() - 140
		
## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
## Transparent Panels ##
		self.X_RIGHT_PANE = self.X_LEFT_PANE + self.W_LEFT_PANE + 10
		self.W_RIGHT_PANE = screen.getXResolution() - self.X_RIGHT_PANE - 20
					
		self.X_CITY_LIST = self.X_RIGHT_PANE + 20
		self.Y_CITY_LIST = self.Y_LEFT_PANE + 100
		self.W_CITY_LIST = (self.W_RIGHT_PANE - 60) *2/5
		self.H_CITY_LIST = self.H_LEFT_PANE - 130
		
		self.X_EFFECTS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
		self.H_EFFECTS_LIST = (self.H_CITY_LIST / 3) - 50
		
		self.X_MISSIONS_LIST = self.X_CITY_LIST + self.W_CITY_LIST + 20
		self.Y_MISSIONS_LIST = self.Y_CITY_LIST + self.H_EFFECTS_LIST + 50
		self.H_MISSIONS_LIST = (self.H_CITY_LIST * 2 / 3)
		self.W_MISSIONS_LIST = self.W_RIGHT_PANE - 60 - self.W_CITY_LIST

## Unique Background ##
		screen.addPanel("RightPane", "", "", True, True, self.X_RIGHT_PANE, self.Y_LEFT_PANE, self.W_RIGHT_PANE, self.H_LEFT_PANE, self.PanelStyle)
## Unique Background ##
		szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()) + "</font>"
		screen.setLabel("CitiesTitle", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, self.X_CITY_LIST + self.W_CITY_LIST/2, self.Y_CITY_LIST - 40, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_PASSIVE_EFFECTS", ()) + "</font>"
		screen.setLabel("EffectsTitle", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_EFFECTS_LIST, self.Y_CITY_LIST - 40, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
		szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_MISSIONS", ()) + "</font>"
		screen.setLabel("MissionsTitle", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST - 40, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
		szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
		screen.setLabel("EffectsCostTitle", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANE + self.W_RIGHT_PANE - 30, self.Y_CITY_LIST - 40, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
		szText = u"<font=4>" + CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_COST", ()) + "</font>"
		screen.setLabel("MissionsCostTitle", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, self.X_RIGHT_PANE + self.W_RIGHT_PANE - 30, self.Y_MISSIONS_LIST - 40, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def updateWeight(self):
		screen = self.getScreen()
		for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			iTeamX = pPlayerX.getTeam()
			if iTeamX == self.iActiveTeam: continue
			if pPlayerX.isAlive() and self.pActiveTeam.isHasMet(iTeamX):
				playerPanelName = "PlayerPanel" + str(iPlayerX)
				iX = 8
				iY = 8
				if PlatyOptions.bTransparent:
					iX -= 5
					iY -= 5

				iX += self.iIconSize
				iX += self.iIconSize/2
				iWeight = self.pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTeamX)
				sText = u"<font=3>%s: %d</font>" %(CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()), iWeight)
				WeightText = "EspionageWeight" + str(iPlayerX)
				screen.setLabelAt(WeightText, playerPanelName, sText, CvUtil.FONT_LEFT_JUSTIFY, iX, iY + self.iIconSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
				iRate = self.pActivePlayer.getEspionageSpending(iTeamX)
				sText = u"<font=3>%s%s</color></font>" %(CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()), CyTranslator().getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (iRate,)))
				RateText = "EspionageRate" + str(iPlayerX)
				screen.setLabelAt(RateText, playerPanelName, sText, CvUtil.FONT_RIGHT_JUSTIFY, self.iPanelWidth - 20, iY + self.iIconSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def drawTable(self):
		screen = self.getScreen()
		screen.addScrollPanel("EspionageTable", "", self.X_LEFT_PANE, self.Y_LEFT_PANE - 10, self.W_LEFT_PANE, self.H_LEFT_PANE, PanelStyles.PANEL_STYLE_EXTERNAL)
				
		self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
		self.iActiveTeam = self.pActivePlayer.getTeam()
		self.pActiveTeam = gc.getTeam(self.iActiveTeam)
		szText = u"<font=4>%c: %d%%</font>" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar(), self.pActivePlayer.getCommercePercent(CommerceTypes.COMMERCE_ESPIONAGE))
		szText += u"<font=4>%s</font>" %(CyTranslator().getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (self.pActivePlayer.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE), )))
		screen.setLabel("MakingText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 20, self.Y_TITLE, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		iCount = 0
		iPanelHeight = self.iIconSize + 16
		for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			iTeamX = pPlayerX.getTeam()
			if iTeamX == self.iActiveTeam: continue
			if pPlayerX.isAlive() and self.pActiveTeam.isHasMet(iTeamX):
				playerPanelName = "PlayerPanel" + str(iPlayerX)
				screen.attachPanelAt("EspionageTable", playerPanelName, "", "", False, True, self.PanelStyle, 0, iCount * iPanelHeight, self.iPanelWidth, iPanelHeight, WidgetTypes.WIDGET_GENERAL, -1, -1)
				pTeamX = gc.getTeam(iTeamX)
				if self.iTargetPlayer == -1:
					self.iTargetPlayer = iPlayerX

				iX = 8
				iY = 8
				if PlatyOptions.bTransparent:
					iX -= 5
					iY -= 5
				iLeader = pPlayerX.getLeaderType()
				LeaderIcon = "LeaderIcon" + str(iPlayerX)
				screen.addCheckBoxGFCAt(playerPanelName, LeaderIcon, gc.getLeaderHeadInfo(iLeader).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
					iX, iY, self.iIconSize, self.iIconSize, WidgetTypes.WIDGET_PYTHON, 7876, iLeader + iPlayerX * 10000, ButtonStyles.BUTTON_STYLE_LABEL, False)
				screen.setState(LeaderIcon, self.iTargetPlayer == iPlayerX)

				iX += self.iIconSize
				iCivilization = pPlayerX.getCivilizationType()
				CivilizationIcon = "CivilizationIcon" + str(iPlayerX)
				screen.addDDSGFCAt(CivilizationIcon, playerPanelName, gc.getCivilizationInfo(iCivilization).getButton(), iX, iY, self.iIconSize/2, self.iIconSize/2, WidgetTypes.WIDGET_PYTHON, 7872, iCivilization, False)
				
				iAttitude = pPlayerX.AI_getAttitude(self.iActivePlayer)
				AttitudeIcon = "AttitudeIcon" + str(iPlayerX)
				screen.addDDSGFCAt(AttitudeIcon, playerPanelName, self.getAttitudeButton(iAttitude), iX, iY + self.iIconSize/2, self.iIconSize/2, self.iIconSize/2, WidgetTypes.WIDGET_GENERAL, -1, -1, False)

				sTemp = ""
				if self.pActiveTeam.getCounterespionageTurnsLeftAgainstTeam(iTeamX):
					sTemp = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + "(+)" + "</color>"
				if pTeamX.getCounterespionageTurnsLeftAgainstTeam(self.iActiveTeam):
					sTemp = CyTranslator().getText("[COLOR_NEGATIVE_TEXT]", ()) + "(-)" + "</color>"

				iX += self.iIconSize/2
				iMultiplier = getEspionageModifier(self.pActivePlayer.getTeam(), iTeamX)
				sText = u"<font=3>%s%% %s</font>" %(CyTranslator().getText("TXT_KEY_PEDIA_COST", (iMultiplier,)), sTemp)
				MultiplierText = "EspionageMultiplier" + str(iPlayerX)
				screen.setLabelAt(MultiplierText, playerPanelName, sText, CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				iWeight = self.pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTeamX)
				sText = u"<font=3>%s: %d</font>" %(CyTranslator().getText("TXT_KEY_ESPIONAGE_SCREEN_SPENDING_WEIGHT", ()), iWeight)
				WeightText = "EspionageWeight" + str(iPlayerX)
				screen.setLabelAt(WeightText, playerPanelName, sText, CvUtil.FONT_LEFT_JUSTIFY, iX, iY + self.iIconSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
				iAmount = self.pActiveTeam.getEspionagePointsAgainstTeam(iTeamX)
				sText = u"<font=3>%s %s</font>" %(self.addComma(iAmount), CyTranslator().getText("[ICON_ESPIONAGE]", ()))
				AmountText = "EspionagePoints" + str(iPlayerX)
				screen.setLabelAt(AmountText, playerPanelName, sText, CvUtil.FONT_RIGHT_JUSTIFY, self.iPanelWidth - 20, iY, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				iRate = self.pActivePlayer.getEspionageSpending(iTeamX)
				sText = u"<font=3>%s%s</color></font>" %(CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()), CyTranslator().getText("TXT_KEY_ESPIONAGE_NUM_EPS_PER_TURN", (iRate,)))
				RateText = "EspionageRate" + str(iPlayerX)
				screen.setLabelAt(RateText, playerPanelName, sText, CvUtil.FONT_RIGHT_JUSTIFY, self.iPanelWidth - 20, iY + self.iIconSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iCount += 1

	def refreshScreen(self):
		self.deleteAllWidgets()
		screen = self.getScreen()
		if self.iTargetPlayer > -1:
			pTargetPlayer = gc.getPlayer(self.iTargetPlayer)
			iTargetTeam = pTargetPlayer.getTeam()
			iEspionage = self.pActiveTeam.getEspionagePointsAgainstTeam(pTargetPlayer.getTeam())
			sText = u"<color=%d,%d,%d,%d>%s (%s%c)</color>" %(pTargetPlayer.getPlayerTextColorR(), pTargetPlayer.getPlayerTextColorG(), pTargetPlayer.getPlayerTextColorB(), pTargetPlayer.getPlayerTextColorA(), pTargetPlayer.getName(), self.addComma(self.pActiveTeam.getEspionagePointsAgainstTeam(iTargetTeam)), gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
			screen.setLabel(self.getNextWidgetName(), "Background", "<font=4>" + sText + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_RIGHT_PANE + self.W_RIGHT_PANE/2, self.Y_LEFT_PANE + 20, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			
			self.szCityListBox = self.getNextWidgetName()
			screen.addListBoxGFC(self.szCityListBox, "", self.X_CITY_LIST, self.Y_CITY_LIST, self.W_CITY_LIST, self.H_CITY_LIST, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSelect(self.szCityListBox, True)
			screen.setStyle(self.szCityListBox, "Table_StandardCiv_Style")

			iLoop = 0
			(loopCity, iter) = pTargetPlayer.firstCity(False)
			while(loopCity):
				if (loopCity.isRevealed(self.pActivePlayer.getTeam(), False)):
					sText = loopCity.getName()
					if self.iMission > -1:
						iCost = self.pActivePlayer.getEspionageMissionCost(self.iMission, self.iTargetPlayer, loopCity.plot(), -1)
						if iCost > -1:
							sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
							if iEspionage < iCost:
								sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
							sText += " (" + sColor + str(iCost) + "</color>)"
					if self.iActiveCityID == -1 or pTargetPlayer.getCity(self.iActiveCityID).isNone():
						self.iActiveCityID = loopCity.getID()
					if self.iActiveCityID == loopCity.getID():
						sText = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + sText + "</color>"
					screen.appendListBoxString(self.szCityListBox, sText, WidgetTypes.WIDGET_GENERAL, loopCity.getID(), 0, CvUtil.FONT_LEFT_JUSTIFY)
					if self.iActiveCityID == loopCity.getID():
						screen.setSelectedListBoxStringGFC(self.szCityListBox, iLoop)
					iLoop += 1
				(loopCity, iter) = pTargetPlayer.nextCity(iter, False)

			if self.iActiveCityID > -1:
				if gc.getPlayer(self.iTargetPlayer).getCity(self.iActiveCityID).getEspionageVisibility(CyGame().getActiveTeam()):
					screen.setImageButton(self.getNextWidgetName(), CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath(),self.X_CITY_LIST, self.Y_CITY_LIST - 40, 32, 32, WidgetTypes.WIDGET_ZOOM_CITY, self.iTargetPlayer, self.iActiveCityID)
				
			screen.addTableControlGFC("PassiveTable", 3, self.X_EFFECTS_LIST, self.Y_CITY_LIST, self.W_MISSIONS_LIST, self.H_EFFECTS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("PassiveTable", 0, "", self.W_MISSIONS_LIST *2/3 - 10)
			screen.setTableColumnHeader("PassiveTable", 1, "", self.W_MISSIONS_LIST /3)
			screen.setTableColumnHeader("PassiveTable", 2, "", 10)
				
			screen.addTableControlGFC("ActiveTable", 3, self.X_MISSIONS_LIST, self.Y_MISSIONS_LIST, self.W_MISSIONS_LIST, self.H_MISSIONS_LIST, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
			screen.setTableColumnHeader("ActiveTable", 0, "", self.W_MISSIONS_LIST *2/3 - 10)
			screen.setTableColumnHeader("ActiveTable", 1, "", self.W_MISSIONS_LIST /3)
			screen.setTableColumnHeader("ActiveTable", 2, "", 10)

			for iMissionLoop in xrange(gc.getNumEspionageMissionInfos()):
				pMission = gc.getEspionageMissionInfo(iMissionLoop)
				if pMission.getCost() > -1:
					pPlot = None
					if self.iActiveCityID > -1:
						pActiveCity = gc.getPlayer(self.iTargetPlayer).getCity(self.iActiveCityID)
						pPlot = pActiveCity.plot()
					iCost = self.pActivePlayer.getEspionageMissionCost(iMissionLoop, self.iTargetPlayer, pPlot, -1)
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					if iEspionage < iCost:
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
					sText = pMission.getDescription()
					if iMissionLoop == self.iMission:
						sText = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + sText + "</color>"
					if pMission.getTechPrereq() > -1:
						sText += " (%s)" %(gc.getTechInfo(pMission.getTechPrereq()).getDescription())
						pTeam = gc.getTeam(self.pActivePlayer.getTeam())
						if not pTeam.isHasTech(pMission.getTechPrereq()):
							sText = u"<color=255,0,0,0>%s</color>" %(sText)
					if pMission.isPassive():					
						iRow = screen.appendTableRow("PassiveTable")
						screen.setTableText("PassiveTable", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8207, iMissionLoop, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText("PassiveTable", 1, iRow, "<font=3>" + sColor + str(iCost) + "</font></color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
					else:								
						iRow = screen.appendTableRow("ActiveTable")
						screen.setTableText("ActiveTable", 0, iRow, "<font=3>" + sText + "</font>", "", WidgetTypes.WIDGET_PYTHON, 8208, iMissionLoop, CvUtil.FONT_LEFT_JUSTIFY)
						if iCost > 0:
							screen.setTableText("ActiveTable", 1, iRow, "<font=3>" + sColor + str(iCost) + "</font></color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		return 0

	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while i > -1:
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1
		self.nWidgetCount = 0
			
	def handleInput (self, inputClass):
		screen = self.getScreen()
		if inputClass.getButtonType() == WidgetTypes.WIDGET_ZOOM_CITY:	
			screen.hideScreen()		
			CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), True)
		if inputClass.getFunctionName() == "ChangeBy":
			iIndex = screen.getSelectedPullDownID("ChangeBy")
			self.iChange = screen.getPullDownData("ChangeBy", iIndex)
		elif inputClass.getFunctionName() == "PassiveTable" or inputClass.getFunctionName() == "ActiveTable":
			iMission = inputClass.getData2()
			if self.iMission == iMission:
				self.iMission = -1
			else:
				self.iMission = iMission
			self.refreshScreen()
		elif inputClass.getFunctionName() == "EspionageAdvisorDropdownWidget":
			iIndex = screen.getSelectedPullDownID("EspionageAdvisorDropdownWidget")
			self.iActivePlayer = screen.getPullDownData("EspionageAdvisorDropdownWidget", iIndex)
			self.iTargetPlayer = -1
			self.iActiveCityID = -1
			self.drawTable()
			self.refreshScreen()
		if self.iTargetPlayer > -1:
			if ("%s%d" %(inputClass.getFunctionName(), inputClass.getID()) == self.szCityListBox):
				self.iActiveCityID = inputClass.getData1()
				self.refreshScreen()
			elif inputClass.getData1() == 7876:
				screen.setState("LeaderIcon" + str(self.iTargetPlayer), False)
				self.iTargetPlayer = inputClass.getData2()/10000
				screen.setState("LeaderIcon" + str(self.iTargetPlayer), True)
				self.iActiveCityID = -1
				self.refreshScreen()
			elif inputClass.getFunctionName() == "WeightPlus":
					self.changeEspionageWeight(self.iChange)
			elif inputClass.getFunctionName() == "WeightMinus":
				self.changeEspionageWeight(-self.iChange)		
		return 0

	def changeEspionageWeight(self, iChange):
		pTargetPlayer = gc.getPlayer(self.iTargetPlayer)
		iTargetTeam = pTargetPlayer.getTeam()
		if iChange < 0:
			if self.pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam) == 0: return
			iChange = min(iChange, self.pActivePlayer.getEspionageSpendingWeightAgainstTeam(iTargetTeam))
		CyMessageControl().sendEspionageSpendingWeightChange(iTargetTeam, iChange)
		CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, True)

	def update(self, fDelta):
		if CyInterface().isDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT):
			self.updateWeight()
			CyInterface().setDirty(InterfaceDirtyBits.Espionage_Advisor_DIRTY_BIT, False)
		return

	def getAttitudeButton(self, iAttitude):
		lAttitude = ["INTERFACE_ATTITUDE_0", "INTERFACE_ATTITUDE_1", "INTERFACE_ATTITUDE_2", "INTERFACE_ATTITUDE_3", "INTERFACE_ATTITUDE_4"]
		if iAttitude < len(lAttitude):
			sButton = CyArtFileMgr().getInterfaceArtInfo(lAttitude[iAttitude])
			if sButton:
				return sButton.getPath()
		return ""