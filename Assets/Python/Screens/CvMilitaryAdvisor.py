from CvPythonExtensions import *
import CvUtil
import ScreenInput
import time
import re
import PlatyOptions
gc = CyGlobalContext()

class CvMilitaryAdvisor:
	def __init__(self, screenId):
		self.screenId = screenId
		self.UNIT_PANEL_ID = "MilitaryAdvisorUnitPanel"
		self.UNIT_BUTTON_ID = "MilitaryAdvisorUnitButton"
		self.UNIT_BUTTON_LABEL_ID = "MilitaryAdvisorUnitButtonLabel"
		self.LEADER_PANEL_ID = "MilitaryAdvisorLeaderPanel"
		self.UNIT_LIST_ID = "MilitaryAdvisorUnitList"

		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.Y_TITLE = 8

		self.iActivePlayer = -1
		self.selectedPlayerList = []
		self.selectedGroupList = []
		self.selectedUnitList = []

		self.bUnitDetails = False
		self.iLeaderPerColumn = 3	
						
	def getScreen(self):
		return CyGInterfaceScreen("MilitaryAdvisor", self.screenId)
				
	def interfaceScreen(self):
		screen = self.getScreen()
		if screen.isActive(): return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
## Unique Background ##
		screen.addDDSGFC("ScreenBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground(False)
		screen.setText("MilitaryAdvisorExitWidget", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText("MilitaryHeader", "Background", "<font=4b>" + CyTranslator().getText("TXT_KEY_MILITARY_ADVISOR_TITLE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	
		self.W_TEXT = screen.getXResolution()/3
		self.X_TEXT = screen.getXResolution() - 30 - self.W_TEXT
		self.Y_TEXT = 80
		self.H_TEXT = screen.getYResolution() - 160

		self.X_MAP = 30
		self.W_MAP =  self.X_TEXT - 10 - self.X_MAP
		self.H_MAP_MAX = self.H_TEXT - 50 - 25 * 6
		self.MAP_MARGIN = 20
		self.W_LEADERS =  self.X_TEXT - 10 - self.X_MAP
		
		self.X_GREAT_GENERAL_BAR = self.X_MAP
		self.Y_GREAT_GENERAL_BAR = screen.getYResolution() - 38
		self.W_GREAT_GENERAL_BAR = screen.getXResolution()/3
		self.H_GREAT_GENERAL_BAR = 30
		
		# Minimap initialization
		self.H_MAP = (self.W_MAP * CyMap().getGridHeight()) / CyMap().getGridWidth()
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * CyMap().getGridWidth()) / CyMap().getGridHeight()
			self.H_MAP = self.H_MAP_MAX
		self.Y_MAP = screen.getYResolution() - 80 - self.H_MAP
## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
		screen.addPanel("", u"", "", False, False, self.X_MAP, self.Y_MAP, self.W_MAP, self.H_MAP, self.PanelStyle)
## Transparent Panels ##
		screen.initMinimap(self.X_MAP + self.MAP_MARGIN, self.X_MAP + self.W_MAP - self.MAP_MARGIN, self.Y_MAP + self.MAP_MARGIN, self.Y_MAP + self.H_MAP - self.MAP_MARGIN, self.Z_CONTROLS)
		screen.updateMinimapSection(False, False)

		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)

		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)
		
		iOldMode = CyInterface().getShowInterface()
		CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)
					
		self.iActivePlayer = CyGame().getActivePlayer()

		self.unitsList = [(0, 0, [], 0)] * gc.getNumUnitInfos()
		self.selectedUnitList = []
		self.selectedPlayerList.append(self.iActivePlayer)

		self.drawCombatExperience()

		self.refresh(true)
		
	def drawCombatExperience(self):
		if (gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true) > 0):
			iExperience = gc.getPlayer(self.iActivePlayer).getCombatExperience()
			screen = self.getScreen()
			screen.addStackedBarGFC("MilitaryAdvisorGreatGeneralBar", self.X_GREAT_GENERAL_BAR, self.Y_GREAT_GENERAL_BAR, self.W_GREAT_GENERAL_BAR, self.H_GREAT_GENERAL_BAR, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
			screen.setStackedBarColors("MilitaryAdvisorGreatGeneralBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
			screen.setStackedBarColors("MilitaryAdvisorGreatGeneralBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
			screen.setStackedBarColors("MilitaryAdvisorGreatGeneralBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setStackedBarColors("MilitaryAdvisorGreatGeneralBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
			screen.setBarPercentage("MilitaryAdvisorGreatGeneralBar", InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(true)))
			sText = u"%s (%d/%d)" %(CyTranslator().getText("TXT_KEY_MISC_COMBAT_EXPERIENCE", ()), gc.getPlayer(self.iActivePlayer).getCombatExperience(), gc.getPlayer(self.iActivePlayer).greatPeopleThreshold(True))
			screen.setLabel("MilitaryAdvisorGreatGeneralLabel", "", sText, CvUtil.FONT_CENTER_JUSTIFY, self.X_GREAT_GENERAL_BAR + self.W_GREAT_GENERAL_BAR/2, self.Y_GREAT_GENERAL_BAR + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1)
																					
	def resetMinimapColor(self):
		screen = self.getScreen()
		for iX in xrange(gc.getMap().getGridWidth()):
			for iY in xrange(gc.getMap().getGridHeight()):
				screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, iX, iY, -1, 0.6)
																				
	# handle the input for this screen...
	def handleInput (self, inputClass):
		if inputClass.getButtonType() == WidgetTypes.WIDGET_PYTHON:
			if inputClass.getData1() == 8202:
				self.refreshSelectedGroup(inputClass.getData2())
			elif inputClass.getData1() == 8203:
				self.refreshSelectedGroup(inputClass.getData2() + gc.getNumUnitInfos())
			elif inputClass.getData1() == 8204:
				self.refreshSelectedLeader(inputClass.getData2())
			elif inputClass.getData1() > 8299 and inputClass.getData1() < 8400:
				self.refreshSelectedUnit(inputClass.getData1() - 8300, inputClass.getData2())
			return
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == self.UNIT_BUTTON_ID) :
			self.bUnitDetails = not self.bUnitDetails
			self.refreshUnitSelection(True)
		return 0

	def update(self, fDelta):
		screen = self.getScreen()
		screen.updateMinimap(fDelta)

	def minimapClicked(self):
		screen = self.getScreen()
		screen.hideScreen()
			
	def isSelectedGroup(self, iGroup, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if iGroup == -1:
				return False
		return ((iGroup + gc.getNumUnitInfos()) in self.selectedGroupList)
				
	def isSelectedUnitType(self, iUnit, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			if self.isSelectedGroup(gc.getUnitInfo(iUnit).getUnitCombatType(), True):
				return True
		return (iUnit in self.selectedGroupList)
		
	def isSelectedUnit(self, iPlayer, iUnitId, bIndirect):
		if (bIndirect):
			if -1 in self.selectedGroupList:
				return True
			unit = gc.getPlayer(iPlayer).getUnit(iUnitId)
			if self.isSelectedGroup(gc.getUnitInfo(unit.getUnitType()).getUnitCombatType(), True):
				return True
			if self.isSelectedUnitType(unit.getUnitType(), True):
				return True
		return ((iPlayer, iUnitId) in self.selectedUnitList)
		
	def refreshSelectedLeader(self, iPlayer):
		if CyInterface().shiftKey():
			if iPlayer in self.selectedPlayerList:
				self.selectedPlayerList.remove(iPlayer)
			else:
				self.selectedPlayerList.append(iPlayer)
		else:
			self.selectedPlayerList = []
			self.selectedPlayerList.append(iPlayer)	
		self.refresh(True)

	def refreshSelectedGroup(self, iSelected):
		if CyInterface().shiftKey():
			if iSelected in self.selectedGroupList:
				self.selectedGroupList.remove(iSelected)
			else:
				self.selectedGroupList.append(iSelected)
		else:
			self.selectedGroupList = []
			self.selectedGroupList.append(iSelected)
		self.refreshUnitSelection(false)
			
	def refreshSelectedUnit(self, iPlayer, iUnitId):
		selectedUnit = (iPlayer, iUnitId)
		if CyInterface().shiftKey():
			if (selectedUnit in self.selectedUnitList):
				self.selectedUnitList.remove(selectedUnit)
			else:
				self.selectedUnitList.append(selectedUnit)
		else:
			self.selectedUnitList = []
			self.selectedGroupList = []
			self.selectedUnitList.append(selectedUnit)
		self.refreshUnitSelection(false)		
	
	def refreshUnitSelection(self, bReload):
		screen = self.getScreen()
		
		screen.minimapClearAllFlashingTiles()

		if (bReload):
			if (self.bUnitDetails):
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", self.X_TEXT + self.MAP_MARGIN, self.Y_TEXT + self.MAP_MARGIN/2, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", CyTranslator().getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_OFF", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_TEXT + self.MAP_MARGIN + 22, self.Y_TEXT + self.MAP_MARGIN/2 + 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", self.X_TEXT + self.MAP_MARGIN, self.Y_TEXT + self.MAP_MARGIN/2, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", CyTranslator().getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_ON", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_TEXT + self.MAP_MARGIN + 22, self.Y_TEXT + self.MAP_MARGIN/2 + 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# self.unitsList[iUnit][0] is the UnitCombatGroup (e.g. Melee)
		# self.unitsList[iUnit][1] is the unit type (e.g. Warrior)
		# self.unitsList[iUnit][2] is a list of the active player's actual units
		# self.unitsList[iUnit][3] is the total number of those units seen by the active player (not only his own)
		
		if bReload:
			for iUnit in xrange(gc.getNumUnitInfos()):
				self.unitsList[iUnit] = (gc.getUnitInfo(iUnit).getUnitCombatType(), iUnit, [], 0)

			for iPlayer in xrange(gc.getMAX_PLAYERS()):		
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					(loopUnit, iter) = pPlayer.firstUnit(False)
					while(loopUnit):
						unitType = loopUnit.getUnitType()
						bVisible = False
						plot = loopUnit.plot()
						if (not plot.isNone()):
							bVisible = plot.isVisible(gc.getPlayer(self.iActivePlayer).getTeam(), False) and not loopUnit.isInvisible(gc.getPlayer(self.iActivePlayer).getTeam(), False)

						if unitType > -1 and unitType < gc.getNumUnitInfos() and bVisible:
							iNumUnits = self.unitsList[unitType][3]
							if (iPlayer == self.iActivePlayer):
								iNumUnits += 1
							if loopUnit.getVisualOwner() in self.selectedPlayerList:
								self.unitsList[unitType][2].append(loopUnit)							
							
							self.unitsList[unitType] = (self.unitsList[unitType][0], self.unitsList[unitType][1], self.unitsList[unitType][2], iNumUnits)
						(loopUnit, iter) = pPlayer.nextUnit(iter, False)

			# sort by unit combat type
			self.unitsList.sort()

		iWidth = self.W_TEXT-2*self.MAP_MARGIN
		screen.addTableControlGFC(self.UNIT_LIST_ID, 2, self.X_TEXT+self.MAP_MARGIN, self.Y_TEXT+self.MAP_MARGIN+15, iWidth, self.H_TEXT-2*self.MAP_MARGIN-15, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader(self.UNIT_LIST_ID, 0, "", iWidth * 5/6)
		screen.setTableColumnHeader(self.UNIT_LIST_ID, 1, "", iWidth/6)
		screen.enableSelect(self.UNIT_LIST_ID, False)

		screen.appendTableRow(self.UNIT_LIST_ID)
		sColor = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ())
		if -1 in self.selectedGroupList:
			sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
		szText = sColor + CyTranslator().getText("TXT_KEY_PEDIA_ALL_UNITS", ()).upper() + "</color>"
		screen.setTableInt(self.UNIT_LIST_ID, 0, 0, szText, "", WidgetTypes.WIDGET_PYTHON, 8202, -1, CvUtil.FONT_LEFT_JUSTIFY)
							
		iPrevUnitCombat = -1
		iRow = 1
		iCount = 0
		iTotal = 0
		iPreviousRow = 0
		for iUnit in xrange(gc.getNumUnitInfos()):
			if (len(self.unitsList[iUnit][2]) > 0):
				if iPrevUnitCombat != self.unitsList[iUnit][0]:
					screen.setTableInt(self.UNIT_LIST_ID, 1, iPreviousRow, str(iCount), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					iCount = 0
					if not self.bUnitDetails:
						screen.appendTableRow(self.UNIT_LIST_ID)
						iRow += 1
					iPrevUnitCombat = self.unitsList[iUnit][0]
					szDescription = gc.getUnitCombatInfo(self.unitsList[iUnit][0]).getDescription().upper()
					sButton = gc.getUnitCombatInfo(self.unitsList[iUnit][0]).getButton()
					sColor = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ())
					if (self.isSelectedGroup(self.unitsList[iUnit][0], True)):
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
					if (self.isSelectedGroup(self.unitsList[iUnit][0], False)):
						sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
					iPreviousRow = iRow
					screen.appendTableRow(self.UNIT_LIST_ID)
					screen.setTableText(self.UNIT_LIST_ID, 0, iRow, sColor+ szDescription + "</color>", sButton, WidgetTypes.WIDGET_PYTHON, 8203, self.unitsList[iUnit][0], CvUtil.FONT_LEFT_JUSTIFY)
					iRow += 1
				
				szDescription = gc.getUnitInfo(self.unitsList[iUnit][1]).getDescription()
				sButton = gc.getUnitInfo(self.unitsList[iUnit][1]).getButton()
				iNumber = (len(self.unitsList[iUnit][2]))
				iCount += iNumber
				iTotal += iNumber
				sColor = ""
				if (self.isSelectedUnitType(self.unitsList[iUnit][1], True)):
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				if (self.isSelectedUnitType(self.unitsList[iUnit][1], False)):
					sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())

				screen.appendTableRow(self.UNIT_LIST_ID)
				screen.setTableText(self.UNIT_LIST_ID, 0, iRow, sColor+ szDescription + "</color>", sButton, WidgetTypes.WIDGET_PYTHON, 8202, self.unitsList[iUnit][1], CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt(self.UNIT_LIST_ID, 1, iRow, sColor+ str(iNumber) + "</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
				
				for i in xrange(len(self.unitsList[iUnit][2])):
					loopUnit = self.unitsList[iUnit][2][i]
					iPlayer = loopUnit.getVisualOwner()
					if self.bUnitDetails:
						szDescription = loopUnit.getName()
						
						if loopUnit.isWaiting():
							szDescription = '*' + szDescription

						sColor = ""
						if (self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True)):
							sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						if (self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), False)):
							sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())

						iCivilization = gc.getPlayer(iPlayer).getCivilizationType()
						screen.appendTableRow(self.UNIT_LIST_ID)
						screen.setTableText(self.UNIT_LIST_ID, 0, iRow, sColor+ szDescription + "</color>", gc.getCivilizationInfo(iCivilization).getButton(), WidgetTypes.WIDGET_PYTHON, 8300 + loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableInt(self.UNIT_LIST_ID, 1, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
						iRow += 1
						if i == len(self.unitsList[iUnit][2]) - 1:
							screen.appendTableRow(self.UNIT_LIST_ID)
							iRow += 1

					pPlayer = gc.getPlayer(iPlayer)
					iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, loopUnit.getX(), loopUnit.getY(), iColor, 0.6)
					if (self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID(), True) and (iPlayer in self.selectedPlayerList)):
						
						if (gc.getTeam(pPlayer.getTeam()).isAtWar(gc.getPlayer(self.iActivePlayer).getTeam())):
							iColor = gc.getInfoTypeForString("COLOR_RED")
						elif (pPlayer.getTeam() != gc.getPlayer(self.iActivePlayer).getTeam()):
							iColor = gc.getInfoTypeForString("COLOR_YELLOW")
						else:
							iColor = gc.getInfoTypeForString("COLOR_WHITE")
						screen.minimapFlashPlot(loopUnit.getX(), loopUnit.getY(), iColor, -1)
		screen.setTableInt(self.UNIT_LIST_ID, 1, iPreviousRow, str(iCount), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableInt(self.UNIT_LIST_ID, 1, 0, str(iTotal), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def refresh(self, bReload):
		if (self.iActivePlayer < 0):
			return
						
		screen = self.getScreen()
			
		listLeaders = []
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			player = gc.getPlayer(iLoopPlayer)
			if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or CyGame().isDebugMode())):
				listLeaders.append(iLoopPlayer)

		iNumRows = (len(listLeaders) + self.iLeaderPerColumn - 1) / self.iLeaderPerColumn
		self.H_LEADERS = min(iNumRows * 25 + 40, self.Y_MAP - 10 - self.Y_TEXT)
## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
		screen.addPanel(self.UNIT_PANEL_ID, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, self.PanelStyle)			
		screen.addPanel(self.LEADER_PANEL_ID, "", "", False, True, self.X_MAP, self.Y_TEXT, self.W_LEADERS, self.H_LEADERS, self.PanelStyle)
## Transparent Panels ##

		screen.addTableControlGFC("LeadersTable", self.iLeaderPerColumn * 2, self.X_MAP + 20, self.Y_TEXT + 20, self.W_LEADERS - 40, self.H_LEADERS - 40, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		iWidth = (self.W_LEADERS - 40 - 24 * self.iLeaderPerColumn) / self.iLeaderPerColumn
		for i in xrange(0, self.iLeaderPerColumn * 2, 2):
			screen.setTableColumnHeader("LeadersTable", i, "", 24)
			screen.setTableColumnHeader("LeadersTable", i + 1, "", iWidth)
		for i in xrange(iNumRows):
			screen.appendTableRow("LeadersTable")

		for iIndex in xrange(len(listLeaders)):
			iLoopPlayer = listLeaders[iIndex]
			pPlayer = gc.getPlayer(iLoopPlayer)

			if (bReload):
				iRow = iIndex / self.iLeaderPerColumn
				iColumn = iIndex % self.iLeaderPerColumn
				sColor = ""
				if pPlayer.isBarbarian():
					sLeaderButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
					sCivButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					sLeaderButton = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
					sCivButton = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton()
				if iLoopPlayer in self.selectedPlayerList:
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				screen.setTableText("LeadersTable", iColumn * 2, iRow, "", sCivButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("LeadersTable", iColumn * 2 + 1, iRow, sColor + pPlayer.getName() + "</color>", sLeaderButton, WidgetTypes.WIDGET_PYTHON, 8204, iLoopPlayer, CvUtil.FONT_LEFT_JUSTIFY)

		self.refreshUnitSelection(bReload)