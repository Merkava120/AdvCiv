from CvPythonExtensions import *
import CvScreenEnums
import CvUtil
import ScreenInput
import string
import time
import PlatyOptions
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()

class CvInfoScreen:
	def __init__(self, screenId):
		self.screenId = screenId

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2
		self.Z_HELP_AREA = self.Z_CONTROLS - 1
		self.Y_TITLE = 8
		self.W_HELP_AREA = 200

		self.X_TABS		= 60

		self.graphEnd		= CyGame().getGameTurn() - 1
		self.graphZoom		= self.graphEnd - CyGame().getStartTurn()
		self.nWidgetCount	= 0
		self.nLineCount		= -1

		# This is used to allow the wonders screen to refresh without redrawing everything
		self.iNumWondersPermanentWidgets = 0

		self.iGraphID		= 0
		self.iDemographicsID	= 1
		self.iTopCitiesID	= 2
		self.iStatsID		= 3

		self.iActiveTab = self.iGraphID

		self.TOTAL_SCORE	= 0
		self.ECONOMY_SCORE	= 1
		self.INDUSTRY_SCORE	= 2
		self.AGRICULTURE_SCORE	= 3
		self.POWER_SCORE	= 4
		self.CULTURE_SCORE	= 5
		self.ESPIONAGE_SCORE	= 6
		self.NUM_SCORES		= 7
		self.RANGE_SCORES	= range(self.NUM_SCORES)

		self.scoreCache	= []
		for t in self.RANGE_SCORES:
		    self.scoreCache.append(None)

		self.GRAPH_H_LINE = "GraphHLine"
		self.GRAPH_V_LINE = "GraphVLine"

		self.xSelPt = 0
		self.ySelPt = 0
		
		self.graphLeftButtonID = ""
		self.graphRightButtonID = ""

		self.szWonderDisplayMode = "World Wonders"
		self.iWonderID = -1

		self.iInfoTable = 0

		self.reset()

	def initText(self):

		###### TEXT ######
		self.SCREEN_TITLE = u"<font=4b>" + CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()).upper() + u"</font>"
		self.SCREEN_GRAPH_TITLE = u"<font=4b>" + CyTranslator().getText("TXT_KEY_INFO_GRAPH", ()).upper() + u"</font>"
		self.SCREEN_DEMOGRAPHICS_TITLE = u"<font=4b>" + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_TITLE", ()).upper() + u"</font>"
		self.SCREEN_TOP_CITIES_TITLE = u"<font=4b>" + CyTranslator().getText("TXT_KEY_WONDERS_SCREEN_TOP_CITIES_TEXT", ()).upper() + u"</font>"
		self.SCREEN_STATS_TITLE = u"<font=4b>" + CyTranslator().getText("TXT_KEY_INFO_SCREEN_STATISTICS_TITLE", ()).upper() + u"</font>"

		self.TEXT_GRAPH = u"<font=4>" + CyTranslator().getText("TXT_KEY_INFO_GRAPH", ()).upper() + u"</font>"
		self.TEXT_DEMOGRAPHICS = u"<font=4>" + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_TITLE", ()).upper() + u"</font>"
		self.TEXT_DEMOGRAPHICS_SMALL = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_TITLE", ())
		self.TEXT_TOP_CITIES = u"<font=4>" + CyTranslator().getText("TXT_KEY_WONDERS_SCREEN_TOP_CITIES_TEXT", ()).upper() + u"</font>"
		self.TEXT_STATS = u"<font=4>" + CyTranslator().getText("TXT_KEY_INFO_SCREEN_STATISTICS_TITLE", ()).upper() + u"</font>"
		self.TEXT_GRAPH_YELLOW = u"<font=4>" + CyTranslator().getColorText("TXT_KEY_INFO_GRAPH", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"
		self.TEXT_DEMOGRAPHICS_YELLOW = u"<font=4>" + CyTranslator().getColorText("TXT_KEY_DEMO_SCREEN_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"
		self.TEXT_TOP_CITIES_YELLOW = u"<font=4>" + CyTranslator().getColorText("TXT_KEY_WONDERS_SCREEN_TOP_CITIES_TEXT", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"
		self.TEXT_STATS_YELLOW = u"<font=4>" + CyTranslator().getColorText("TXT_KEY_INFO_SCREEN_STATISTICS_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + u"</font>"

		self.TEXT_ENTIRE_HISTORY = CyTranslator().getText("TXT_KEY_INFO_ENTIRE_HISTORY", ())
		
		self.TEXT_SCORE = CyTranslator().getText("TXT_KEY_GAME_SCORE", ())
		self.TEXT_POWER = CyTranslator().getText("TXT_KEY_POWER", ())
		self.TEXT_CULTURE = CyTranslator().getObjectText("TXT_KEY_COMMERCE_CULTURE", 0)
		self.TEXT_ESPIONAGE = CyTranslator().getObjectText("TXT_KEY_ESPIONAGE_CULTURE", 0)

		self.TEXT_VALUE = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_VALUE_TEXT", ())
		self.TEXT_RANK = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_RANK_TEXT", ())
		self.TEXT_AVERAGE = CyTranslator().getText("TXT_KEY_DEMOGRAPHICS_SCREEN_RIVAL_AVERAGE", ())
		self.TEXT_BEST = CyTranslator().getText("TXT_KEY_INFO_RIVAL_BEST", ())
		self.TEXT_WORST = CyTranslator().getText("TXT_KEY_INFO_RIVAL_WORST", ())

		self.TEXT_ECONOMY = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_ECONOMY_TEXT", ())
		self.TEXT_INDUSTRY = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_INDUSTRY_TEXT", ())
		self.TEXT_AGRICULTURE = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_AGRICULTURE_TEXT", ())
		self.TEXT_MILITARY = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_MILITARY_TEXT", ())
		self.TEXT_LAND_AREA = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_LAND_AREA_TEXT", ())
		self.TEXT_POPULATION = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_POPULATION_TEXT", ())
		self.TEXT_HAPPINESS = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_HAPPINESS_TEXT", ())
		self.TEXT_HEALTH = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_HEALTH_TEXT", ())
		self.TEXT_IMP_EXP = CyTranslator().getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()) + " - " + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_IMPORTS_TEXT", ())

		self.TEXT_ECONOMY_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_ECONOMY_MEASURE", ())
		self.TEXT_INDUSTRY_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_INDUSTRY_MEASURE", ())
		self.TEXT_AGRICULTURE_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_AGRICULTURE_MEASURE", ())
		self.TEXT_LAND_AREA_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_LAND_AREA_MEASURE", ())
		self.TEXT_HAPPINESS_MEASURE = "%"
		self.TEXT_HEALTH_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_POPULATION_MEASURE", ())
		self.TEXT_IMP_EXP_MEASURE = (u"  %c" % CyGame().getSymbolID(FontSymbols.BULLET_CHAR)) + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_ECONOMY_MEASURE", ())

	def reset(self):
		self.graphEnd	    = CyGame().getGameTurn() - 1
		self.graphZoom	    = self.graphEnd - CyGame().getStartTurn()
		for t in self.RANGE_SCORES:
		    self.scoreCache[t]	= None

	def getScreen(self):
		return CyGInterfaceScreen("DemographicsScreen", self.screenId)

	# Screen construction function
	def showScreen(self, iTurn, iTabID, iEndGame):
		self.initText()
		if iTurn > CyGame().getReplayMessageTurn(CyGame().getNumReplayMessages() -1):
			return

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.reset()
		self.deleteAllWidgets()
## Unique Background ##
		screen.addDDSGFC("ScreenBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		screen.setDimensions(0, 0, screen.getXResolution(), screen.getYResolution())
		self.szExitButtonName = self.getNextWidgetName()
		screen.setText(self.szExitButtonName, "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Header...
		self.szHeaderWidget = self.getNextWidgetName()
		screen.setText(self.szHeaderWidget, "Background", self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Help area for tooltips
		screen.setHelpTextArea(self.W_HELP_AREA, FontTypes.SMALL_FONT, 0, 0, self.Z_HELP_AREA, 1, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )

		if (CyGame().isDebugMode()):
			screen.addDropDownBoxGFC("InfoScreenDropdownWidget", 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_PLAYERS()):
				if gc.getPlayer(j).isAlive():
					screen.addPullDownString("InfoScreenDropdownWidget", gc.getPlayer(j).getName(), j, j, False )

		self.iActivePlayer = CyGame().getActivePlayer()
		self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
		self.iActiveTeam = CyGame().getActiveTeam()
		self.pActiveTeam = gc.getTeam(self.iActiveTeam)
		
		iDemographicsMission = -1
		# See if Espionage allows graph to be shown for each player
		if not CyGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE):
			for iMissionLoop in xrange(gc.getNumEspionageMissionInfos()):
				if gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics():
					iDemographicsMission = iMissionLoop
					break
				
		# Determine who this active player knows
		self.aiPlayersMet = []
		self.iNumPlayersMet = 0
		for iLoopPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			iLoopPlayerTeam = pLoopPlayer.getTeam()
			if gc.getTeam(iLoopPlayerTeam).isEverAlive():
				if self.pActiveTeam.isHasMet(iLoopPlayerTeam) or CyGame().isDebugMode() or iEndGame:
					if (	iDemographicsMission == -1 or
							self.pActivePlayer.canDoEspionageMission(iDemographicsMission, iLoopPlayer, None, -1) or
							iEndGame or
							iLoopPlayerTeam == self.iActiveTeam):
						self.aiPlayersMet.append(iLoopPlayer)
						self.iNumPlayersMet += 1

		# "Save" current widgets so they won't be deleted later when changing tabs
		self.iNumPermanentWidgets = self.nWidgetCount

		# Reset variables
		self.graphEnd	= CyGame().getGameTurn() - 1
		self.graphZoom	= self.graphEnd - CyGame().getStartTurn()
		self.iActiveTab = iTabID
		self.redrawContents()
		return

	def redrawContents(self):

		screen = self.getScreen()
		self.deleteAllWidgets(self.iNumPermanentWidgets)
		self.iNumWondersPermanentWidgets = 0

		self.szGraphTabWidget = self.getNextWidgetName()
		self.szDemographicsTabWidget = self.getNextWidgetName()
		self.szTopCitiesTabWidget = self.getNextWidgetName()
		self.szStatsTabWidget = self.getNextWidgetName()

		iX_Increment = (screen.getXResolution() - 25 - self.X_TABS) / 4

		screen.setText(self.szGraphTabWidget, "", self.TEXT_GRAPH, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.szDemographicsTabWidget, "", self.TEXT_DEMOGRAPHICS, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS + iX_Increment, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.szTopCitiesTabWidget, "", self.TEXT_TOP_CITIES, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS + iX_Increment * 2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.szStatsTabWidget, "", self.TEXT_STATS, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS + iX_Increment * 3, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if self.iActiveTab == self.iGraphID:
			screen.setText(self.szGraphTabWidget, "", self.TEXT_GRAPH_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawGraphTab()
		elif self.iActiveTab == self.iDemographicsID:
			screen.setText(self.szDemographicsTabWidget, "", self.TEXT_DEMOGRAPHICS_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS + iX_Increment, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawDemographicsTab()
		elif self.iActiveTab == self.iTopCitiesID:
			screen.setText(self.szTopCitiesTabWidget, "", self.TEXT_TOP_CITIES_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS + iX_Increment * 2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawTopCitiesTab()
		elif self.iActiveTab == self.iStatsID:
			screen.setText(self.szStatsTabWidget, "", self.TEXT_STATS_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS + iX_Increment * 3, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.drawStatsTab()

#############################################################################################################
#################################################### GRAPH ##################################################
#############################################################################################################

	def drawGraphTab(self):
		screen = self.getScreen()
		self.X_MARGIN	= 30
		self.Y_MARGIN	= 80
		self.H_DROPDOWN	= 35
		self.W_DEMO_DROPDOWN	= screen.getXResolution()/6
		self.Y_ZOOM_DROPDOWN	= self.Y_MARGIN + self.H_DROPDOWN
		self.Y_LEGEND		= self.Y_ZOOM_DROPDOWN + self.H_DROPDOWN + 3

		self.X_GRAPH = self.X_MARGIN + self.W_DEMO_DROPDOWN + 10
		self.W_GRAPH = screen.getXResolution() - self.X_GRAPH - self.X_MARGIN
		self.H_GRAPH = screen.getYResolution() - self.Y_MARGIN - 90

		self.iButtonWidth  = 20
		self.Y_LEFT_BUTTON  = self.Y_MARGIN + self.H_GRAPH
		self.X_RIGHT_BUTTON  = self.X_GRAPH + self.W_GRAPH - self.iButtonWidth

		self.X_LEFT_LABEL   = self.X_GRAPH + self.iButtonWidth + 10
		self.X_RIGHT_LABEL  = self.X_RIGHT_BUTTON - 10
		self.Y_LABEL	    = self.Y_MARGIN + self.H_GRAPH + 3

		self.X_MARGIN_MARGIN	= 10
		self.Y_LEGEND_MARGIN	= 5
		self.X_MARGIN_LINE	= self.X_MARGIN_MARGIN
		self.Y_LEGEND_LINE	= self.Y_LEGEND_MARGIN + 9  # to center it relative to the text
		self.W_DEMO_DROPDOWN_LINE	= 30
		self.X_MARGIN_TEXT	= self.X_MARGIN_LINE + self.W_DEMO_DROPDOWN_LINE + 10
		self.Y_LEGEND_TEXT	= self.Y_LEGEND_MARGIN
		self.H_LEGEND_TEXT	= 16

		self.TOTAL_SCORE		= 0
		self.ECONOMY_SCORE	= 1
		self.INDUSTRY_SCORE	= 2
		self.AGRICULTURE_SCORE	= 3
		self.POWER_SCORE		= 4
		self.CULTURE_SCORE	= 5
		self.ESPIONAGE_SCORE	= 6
		self.iGraphTabID = self.TOTAL_SCORE
		self.drawPermanentGraphWidgets()
		self.drawGraph()

	def drawPermanentGraphWidgets(self):

	    screen = self.getScreen()

	    self.H_LEGEND = 2 * self.Y_LEGEND_MARGIN + self.iNumPlayersMet * self.H_LEGEND_TEXT + 3
	    self.Y_LEGEND = self.Y_MARGIN + self.H_GRAPH - self.H_LEGEND

	    self.LEGEND_PANEL_ID = self.getNextWidgetName()
	    screen.addPanel( self.LEGEND_PANEL_ID, "", "", true, true
			   , self.X_MARGIN, self.Y_LEGEND, self.W_DEMO_DROPDOWN, self.H_LEGEND
			   , PanelStyles.PANEL_STYLE_IN
			   )
	    self.LEGEND_CANVAS_ID = self.getNextWidgetName()
	    screen.addDrawControl(self.LEGEND_CANVAS_ID, None, self.X_MARGIN, self.Y_LEGEND, self.W_DEMO_DROPDOWN, self.H_LEGEND, WidgetTypes.WIDGET_GENERAL, -1, -1)

	    self.drawLegend()

	    self.graphLeftButtonID = self.getNextWidgetName()
	    screen.setButtonGFC( self.graphLeftButtonID, u"", "", self.X_GRAPH, self.Y_LEFT_BUTTON, self.iButtonWidth, self.iButtonWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
	    self.graphRightButtonID = self.getNextWidgetName()
	    screen.setButtonGFC( self.graphRightButtonID, u"", "", self.X_RIGHT_BUTTON, self.Y_LEFT_BUTTON, self.iButtonWidth, self.iButtonWidth, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
	    screen.enable(self.graphLeftButtonID, False)
	    screen.enable(self.graphRightButtonID, False)

	    # Dropdown Box
	    self.szGraphDropdownWidget = self.getNextWidgetName()
	    screen.addDropDownBoxGFC(self.szGraphDropdownWidget, self.X_MARGIN, self.Y_MARGIN, self.W_DEMO_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_SCORE, 0, 0, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_ECONOMY, 1, 1, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_INDUSTRY, 2, 2, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_AGRICULTURE, 3, 3, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_POWER, 4, 4, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_CULTURE, 5, 5, False )
	    screen.addPullDownString(self.szGraphDropdownWidget, self.TEXT_ESPIONAGE, 6, 6, False )

	    self.dropDownTurns = []
	    self.szTurnsDropdownWidget = self.getNextWidgetName()
	    screen.addDropDownBoxGFC(self.szTurnsDropdownWidget, self.X_MARGIN, self.Y_ZOOM_DROPDOWN, self.W_DEMO_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
	    start = CyGame().getStartTurn()
	    now   = CyGame().getGameTurn()
	    nTurns = now - start - 1
	    screen.addPullDownString(self.szTurnsDropdownWidget, self.TEXT_ENTIRE_HISTORY, 0, 0, False)
	    self.dropDownTurns.append(nTurns)
	    iCounter = 1
	    last = 50
	    while (last < nTurns):
		screen.addPullDownString(self.szTurnsDropdownWidget, CyTranslator().getText("TXT_KEY_INFO_NUM_TURNS", (last,)), iCounter, iCounter, False)
		self.dropDownTurns.append(last)
		iCounter += 1
		last += 50

	    self.iNumPreDemoChartWidgets = self.nWidgetCount

	def updateGraphButtons(self):
	    screen = self.getScreen()
	    screen.enable(self.graphLeftButtonID, self.graphEnd - self.graphZoom > CyGame().getStartTurn())
	    screen.enable(self.graphRightButtonID, self.graphEnd < CyGame().getGameTurn() - 1)

	def checkGraphBounds(self):
	    start = CyGame().getStartTurn()
	    end   = CyGame().getGameTurn() - 1
	    if (self.graphEnd - self.graphZoom < start):
		self.graphEnd = start + self.graphZoom
	    if (self.graphEnd > end):
		self.graphEnd = end

	def zoomGraph(self, zoom):
	    self.graphZoom = zoom
	    self.checkGraphBounds()
	    self.updateGraphButtons()

	def slideGraph(self, right):
	    self.graphEnd += right
	    self.checkGraphBounds()
	    self.updateGraphButtons()

	def buildScoreCache(self, scoreType):

	    # Check if the scores have already been computed
	    if (self.scoreCache[scoreType]):
		return

	    print("Rebuilding score cache")

	    # Get the player with the highest ID
	    maxPlayer = 0
	    for p in self.aiPlayersMet:
		if (maxPlayer < p):
		    maxPlayer = p

	    # Compute the scores
	    self.scoreCache[scoreType] = []
	    for p in range(maxPlayer + 1):

		if (p not in self.aiPlayersMet):
		    # Don't compute score for people we haven't met
		    self.scoreCache[scoreType].append(None)

		else:

		    self.scoreCache[scoreType].append([])
		    firstTurn	= CyGame().getStartTurn()
		    thisTurn	= CyGame().getGameTurn()
		    turn	= firstTurn
		    while (turn <= thisTurn):
			self.scoreCache[scoreType][p].append(self.computeHistory(scoreType, p, turn))
			turn += 1

	    return

	def computeHistory(self, scoreType, iPlayer, iTurn):

	    iScore = gc.getPlayer(iPlayer).getScoreHistory(iTurn)

	    if (iScore == 0):	# for some reason only the score is 0 when you're dead..?
		return 0

	    if (scoreType == self.TOTAL_SCORE):
		return iScore
	    elif (scoreType == self.ECONOMY_SCORE):
		return gc.getPlayer(iPlayer).getEconomyHistory(iTurn)
	    elif (scoreType == self.INDUSTRY_SCORE):
		return gc.getPlayer(iPlayer).getIndustryHistory(iTurn)
	    elif (scoreType == self.AGRICULTURE_SCORE):
		return gc.getPlayer(iPlayer).getAgricultureHistory(iTurn)
	    elif (scoreType == self.POWER_SCORE):
		return gc.getPlayer(iPlayer).getPowerHistory(iTurn)
	    elif (scoreType == self.CULTURE_SCORE):
		return gc.getPlayer(iPlayer).getCultureHistory(iTurn)
	    elif (scoreType == self.ESPIONAGE_SCORE):
		return gc.getPlayer(iPlayer).getEspionageHistory(iTurn)

	# Requires the cache to be built
	def getHistory(self, scoreType, iPlayer, iRelTurn):
	    return self.scoreCache[scoreType][iPlayer][iRelTurn]

	def drawGraphLines(self):
	    screen = self.getScreen()

	    if (self.xSelPt != 0 or self.ySelPt != 0):
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_H_LINE, 0, self.ySelPt, self.W_GRAPH, self.ySelPt, gc.getInfoTypeForString("COLOR_GREY"))
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_V_LINE, self.xSelPt, 0, self.xSelPt, self.H_GRAPH, gc.getInfoTypeForString("COLOR_GREY"))
	    else:
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_H_LINE, -1, -1, -1, -1, gc.getInfoTypeForString("COLOR_GREY"))
		screen.addLineGFC(self.GRAPH_CANVAS_ID, self.GRAPH_V_LINE, -1, -1, -1, -1, gc.getInfoTypeForString("COLOR_GREY"))


	def drawXLabel(self, screen, turn, x, just = CvUtil.FONT_CENTER_JUSTIFY):
	    screen.setLabel( self.getNextWidgetName(), ""
			   , u"<font=2>" + self.getTurnDate(turn) + u"</font>"
			   , just , x , self.Y_LABEL
			   , 0, FontTypes.TITLE_FONT
			   , WidgetTypes.WIDGET_GENERAL, -1, -1
			   )

	def drawGraph(self):

	    screen = self.getScreen()

	    self.deleteAllLines()
	    self.deleteAllWidgets(self.iNumPreDemoChartWidgets)

	    # Draw the graph widget
	    self.GRAPH_CANVAS_ID = self.getNextWidgetName()
	    screen.addDrawControl(self.GRAPH_CANVAS_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG").getPath(), self.X_GRAPH, self.Y_MARGIN, self.W_GRAPH, self.H_GRAPH, WidgetTypes.WIDGET_GENERAL, -1, -1)

	    # Compute the scores
	    self.buildScoreCache(self.iGraphTabID)

	    # Compute max score
	    max = 0
	    thisTurn    = CyGame().getGameTurn()
	    startTurn   = CyGame().getStartTurn()

	    if (self.graphZoom == 0 or self.graphEnd == 0):
		firstTurn = startTurn
	    else:
		firstTurn = self.graphEnd - self.graphZoom

	    if (self.graphEnd == 0):
		lastTurn  = thisTurn - 1 # all civs haven't neccessarily got a score for the current turn
	    else:
		lastTurn  = self.graphEnd

	    self.drawGraphLines()

	    # Draw x-labels
	    self.drawXLabel( screen, firstTurn, self.X_LEFT_LABEL,  CvUtil.FONT_LEFT_JUSTIFY  )
	    self.drawXLabel( screen, lastTurn,  self.X_RIGHT_LABEL, CvUtil.FONT_RIGHT_JUSTIFY )

	    # Don't draw anything the first turn
	    if (firstTurn >= lastTurn):
		return

	    # Compute max and min
	    max = 1
	    min = 0
	    for p in self.aiPlayersMet:
		for turn in range(firstTurn,lastTurn + 1):
		    score = self.getHistory(self.iGraphTabID, p, turn - startTurn)
		    if (max < score):
			max = score
		    if (min > score):
			min = score

	    yFactor = (1.0 * self.H_GRAPH / (1.0 * (max - min)))
	    xFactor = (1.0 * self.W_GRAPH / (1.0 * (lastTurn - firstTurn)))

	    if (lastTurn - firstTurn > 10):
		turn = (firstTurn + lastTurn) / 2
		self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn)) )
		if (lastTurn - firstTurn > 20):
		    turn = firstTurn + (lastTurn - firstTurn) / 4
		    self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn)) )
		    turn = firstTurn + 3 * (lastTurn - firstTurn) / 4
		    self.drawXLabel ( screen, turn, self.X_GRAPH + int(xFactor * (turn - firstTurn)) )

	    # Draw the lines
	    for p in self.aiPlayersMet:

		color = gc.getPlayerColorInfo(gc.getPlayer(p).getPlayerColor()).getColorTypePrimary()
		oldX = -1
		oldY = self.H_GRAPH
		turn = lastTurn
		while (turn >= firstTurn):

		    score = self.getHistory(self.iGraphTabID, p, turn - startTurn)
		    y = self.H_GRAPH - int(yFactor * (score - min))
		    x = int(xFactor * (turn - firstTurn))

		    if (x < oldX):
			if (y != self.H_GRAPH or oldY != self.H_GRAPH): # don't draw if score is constant zero
			    self.drawLine(screen, self.GRAPH_CANVAS_ID, oldX, oldY, x, y, color)
			oldX = x
			oldY = y
		    elif (oldX == -1):
			oldX = x
			oldY = y

		    turn -= 1

	    return

	def drawLegend(self):
	    screen = self.getScreen()

	    yLine = self.Y_LEGEND_LINE
	    yText = self.Y_LEGEND + self.Y_LEGEND_TEXT

	    for p in self.aiPlayersMet:

		lineColor = gc.getPlayerColorInfo(gc.getPlayer(p).getPlayerColor()).getColorTypePrimary()
		textColorR = gc.getPlayer(p).getPlayerTextColorR()
		textColorG = gc.getPlayer(p).getPlayerTextColorG()
		textColorB = gc.getPlayer(p).getPlayerTextColorB()
		textColorA = gc.getPlayer(p).getPlayerTextColorA()

		str = u"<color=%d,%d,%d,%d>%s</color>" %(textColorR,textColorG,textColorB,textColorA,gc.getPlayer(p).getName())

		self.drawLine(screen, self.LEGEND_CANVAS_ID, self.X_MARGIN_LINE, yLine, self.X_MARGIN_LINE + self.W_DEMO_DROPDOWN_LINE, yLine, lineColor)
		screen.setLabel( self.getNextWidgetName(), ""
			       , u"<font=2>" + str + u"</font>"
			       , CvUtil.FONT_LEFT_JUSTIFY
			       , self.X_MARGIN + self.X_MARGIN_TEXT, yText
			       , 0, FontTypes.TITLE_FONT
			       , WidgetTypes.WIDGET_GENERAL, -1, -1)
		yLine += self.H_LEGEND_TEXT
		yText += self.H_LEGEND_TEXT

#############################################################################################################
################################################# DEMOGRAPHICS ##############################################
#############################################################################################################
	    
	def getHappyValue(self, pPlayer):
		iHappy = pPlayer.calculateTotalCityHappiness()
		iUnhappy = pPlayer.calculateTotalCityUnhappiness()
		return (iHappy * 100) / max(1, iHappy + iUnhappy)	 

	def getHealthValue(self, pPlayer):
		iGood = pPlayer.calculateTotalCityHealthiness()
		iBad = pPlayer.calculateTotalCityUnhealthiness()
		return (iGood * 100) / max(1, iGood + iBad)	 
		
	def getRank(self, aiGroup):
		aiGroup.sort()
		aiGroup.reverse()
		iRank = 1
		for (iLoopValue, iLoopPlayer) in aiGroup:
			if iLoopPlayer == self.iActivePlayer:
				return iRank
			iRank += 1
		return 0

	def getBest(self, aiGroup):
		aiGroup.sort()
		aiGroup.reverse()
		for (iLoopValue, iLoopPlayer) in aiGroup:
			if iLoopPlayer != self.iActivePlayer:
				return iLoopValue
		return 0

	def getWorst(self, aiGroup):
		aiGroup.sort()
		for (iLoopValue, iLoopPlayer) in aiGroup:
			if iLoopPlayer != self.iActivePlayer:
				return iLoopValue
		return 0

	def drawDemographicsTab(self):
		screen = self.getScreen()
		self.X_CHART = 45
		self.Y_CHART = 80
		self.W_CHART = screen.getXResolution() - self.X_CHART * 2
		self.H_CHART = 600

		######## DATA ########

		iNumPlayers = max(1, CyGame().countCivPlayersAlive() - 1)
		pPlayer = gc.getPlayer(self.iActivePlayer)

		iEconomyGameAverage = 0
		iIndustryGameAverage = 0
		iAgricultureGameAverage = 0
		iMilitaryGameAverage = 0
		iLandAreaGameAverage = 0
		iPopulationGameAverage = 0
		iHappinessGameAverage = 0
		iHealthGameAverage = 0
		iNetTradeGameAverage = 0

		# Lists of Player values - will be used to determine rank, strength and average per city
		aiGroupEconomy = []
		aiGroupIndustry = []
		aiGroupAgriculture = []
		aiGroupMilitary = []
		aiGroupLandArea = []
		aiGroupPopulation = []
		aiGroupHappiness = []
		aiGroupHealth = []
		aiGroupNetTrade = []

		# Loop through all players to determine Rank and relative Strength
		for iPlayerLoop in xrange(gc.getMAX_CIV_PLAYERS()):
			if gc.getPlayer(iPlayerLoop).isAlive():
				pCurrPlayer = gc.getPlayer(iPlayerLoop)
				
				iValue = pCurrPlayer.calculateTotalCommerce()
				if iPlayerLoop == self.iActivePlayer:
					iEconomy = iValue
				else:
					iEconomyGameAverage += iValue
				aiGroupEconomy.append((iValue, iPlayerLoop))
				
				iValue = pCurrPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
				if iPlayerLoop == self.iActivePlayer:
					iIndustry = iValue
				else:
					iIndustryGameAverage += iValue
				aiGroupIndustry.append((iValue, iPlayerLoop))

				iValue = pCurrPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
				if iPlayerLoop == self.iActivePlayer:
					iAgriculture = iValue
				else:
					iAgricultureGameAverage += iValue
				aiGroupAgriculture.append((iValue, iPlayerLoop))

				iValue = pCurrPlayer.getPower() * 1000
				if iPlayerLoop == self.iActivePlayer:
					iMilitary = iValue
				else:
					iMilitaryGameAverage += iValue
				aiGroupMilitary.append((iValue, iPlayerLoop))

				iValue = pCurrPlayer.getTotalLand() * 1000
				if iPlayerLoop == self.iActivePlayer:
					iLandArea = iValue
				else:
					iLandAreaGameAverage += iValue
				aiGroupLandArea.append((iValue, iPlayerLoop))
## Real Population ##
				iValue = long(0)
				(pCity, iter) = pCurrPlayer.firstCity(False)
				while(pCity):
					iValue += long((pCity.getPopulation() ** 2.8)) * 1000
					(pCity, iter) = pCurrPlayer.nextCity(iter, False)
				if iPlayerLoop == self.iActivePlayer:
					iPopulation = iValue
				else:
					iPopulationGameAverage += iValue
				aiGroupPopulation.append((iValue, iPlayerLoop))
## Real Population ##
				iValue = self.getHappyValue(pCurrPlayer)
				if iPlayerLoop == self.iActivePlayer:
					iHappiness = iValue
				else:
					iHappinessGameAverage += iValue
				aiGroupHappiness.append((iValue, iPlayerLoop))

				iValue = self.getHealthValue(pCurrPlayer)
				if iPlayerLoop == self.iActivePlayer:
					iHealth = iValue
				else:
					iHealthGameAverage += iValue
				aiGroupHealth.append((iValue, iPlayerLoop))
					
				iValue = pCurrPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE) - pCurrPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
				if iPlayerLoop == self.iActivePlayer:
					iNetTrade = iValue
				else:
					iNetTradeGameAverage += iValue
				aiGroupNetTrade.append((iValue, iPlayerLoop))
					
		iEconomyRank = self.getRank(aiGroupEconomy)
		iIndustryRank = self.getRank(aiGroupIndustry)
		iAgricultureRank = self.getRank(aiGroupAgriculture)
		iMilitaryRank = self.getRank(aiGroupMilitary)
		iLandAreaRank = self.getRank(aiGroupLandArea)
		iPopulationRank = self.getRank(aiGroupPopulation)
		iHappinessRank = self.getRank(aiGroupHappiness)
		iHealthRank = self.getRank(aiGroupHealth)
		iNetTradeRank = self.getRank(aiGroupNetTrade)

		iEconomyGameBest	= self.getBest(aiGroupEconomy)
		iIndustryGameBest	= self.getBest(aiGroupIndustry)
		iAgricultureGameBest	= self.getBest(aiGroupAgriculture)
		iMilitaryGameBest	= self.getBest(aiGroupMilitary)
		iLandAreaGameBest	= self.getBest(aiGroupLandArea)
		iPopulationGameBest	= self.getBest(aiGroupPopulation)
		iHappinessGameBest	= self.getBest(aiGroupHappiness)
		iHealthGameBest		= self.getBest(aiGroupHealth)
		iNetTradeGameBest	= self.getBest(aiGroupNetTrade)

		iEconomyGameWorst	= self.getWorst(aiGroupEconomy)
		iIndustryGameWorst	= self.getWorst(aiGroupIndustry)
		iAgricultureGameWorst	= self.getWorst(aiGroupAgriculture)
		iMilitaryGameWorst	= self.getWorst(aiGroupMilitary)
		iLandAreaGameWorst	= self.getWorst(aiGroupLandArea)
		iPopulationGameWorst	= self.getWorst(aiGroupPopulation)
		iHappinessGameWorst	= self.getWorst(aiGroupHappiness)
		iHealthGameWorst	= self.getWorst(aiGroupHealth)
		iNetTradeGameWorst	= self.getWorst(aiGroupNetTrade)

		iEconomyGameAverage /= iNumPlayers
		iIndustryGameAverage /= iNumPlayers
		iAgricultureGameAverage /= iNumPlayers
		iMilitaryGameAverage /= iNumPlayers
		iLandAreaGameAverage /= iNumPlayers
		iPopulationGameAverage /= iNumPlayers
		iHappinessGameAverage /= iNumPlayers
		iHealthGameAverage /= iNumPlayers
		iNetTradeGameAverage /= iNumPlayers


		######## TEXT ########

		# Create Table
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 6, self.X_CHART, self.Y_CHART, self.W_CHART, self.H_CHART, true, true, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szTable, 0, self.TEXT_DEMOGRAPHICS_SMALL, self.W_CHART * 2/9)
		screen.setTableColumnHeader(szTable, 1, self.TEXT_VALUE, self.W_CHART/6)
		screen.setTableColumnHeader(szTable, 2, self.TEXT_BEST, self.W_CHART/6)
		screen.setTableColumnHeader(szTable, 3, self.TEXT_AVERAGE, self.W_CHART/6)
		screen.setTableColumnHeader(szTable, 4, self.TEXT_WORST, self.W_CHART/6)
		screen.setTableColumnHeader(szTable, 5, self.TEXT_RANK, self.W_CHART/9)

		for i in range(18 + 5): # 18 normal items + 5 lines for spacing
			screen.appendTableRow(szTable)
		iNumRows = screen.getTableNumRows(szTable)
		iRow = iNumRows - 1
		iCol = 0
		screen.setTableText(szTable, iCol, 0, "<font=3>" + self.TEXT_ECONOMY + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 1, "<font=3>" + self.TEXT_ECONOMY_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, "<font=3>" + self.TEXT_INDUSTRY + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 4, "<font=3>" + self.TEXT_INDUSTRY_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, "<font=3>" + self.TEXT_AGRICULTURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 7, "<font=3>" + self.TEXT_AGRICULTURE_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, "<font=3>" + self.TEXT_MILITARY + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, "<font=3>" + self.TEXT_LAND_AREA + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 12, "<font=3>" + self.TEXT_LAND_AREA_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, "<font=3>" + self.TEXT_POPULATION + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, "<font=3>" + self.TEXT_HAPPINESS + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, "<font=3>" + self.TEXT_HEALTH + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 19, "<font=3>" + self.TEXT_HEALTH_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, "<font=3>" + self.TEXT_IMP_EXP + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, iCol, 22, "<font=3>" + self.TEXT_IMP_EXP_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		iCol = 1
		screen.setTableText(szTable, iCol, 0, "<font=3>" + self.addComma(iEconomy) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, "<font=3>" + self.addComma(iIndustry) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, "<font=3>" + self.addComma(iAgriculture) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, "<font=3>" + self.addComma(iMilitary) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, "<font=3>" + self.addComma(iLandArea) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, "<font=3>" + self.addComma(iPopulation) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, "<font=3>" + str(iHappiness) + self.TEXT_HAPPINESS_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, "<font=3>" + str(iHealth) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, "<font=3>" + self.addComma(iNetTrade) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		iCol = 2
		screen.setTableText(szTable, iCol, 0, "<font=3>" + self.addComma(iEconomyGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, "<font=3>" + self.addComma(iIndustryGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, "<font=3>" + self.addComma(iAgricultureGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, "<font=3>" + self.addComma(iMilitaryGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, "<font=3>" + self.addComma(iLandAreaGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, "<font=3>" + self.addComma(iPopulationGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, "<font=3>" + str(iHappinessGameBest) + self.TEXT_HAPPINESS_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, "<font=3>" + str(iHealthGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, "<font=3>" + self.addComma(iNetTradeGameBest) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		iCol = 3
		screen.setTableText(szTable, iCol, 0, "<font=3>" + self.addComma(iEconomyGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, "<font=3>" + self.addComma(iIndustryGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, "<font=3>" + self.addComma(iAgricultureGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, "<font=3>" + self.addComma(iMilitaryGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, "<font=3>" + self.addComma(iLandAreaGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, "<font=3>" + self.addComma(iPopulationGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, "<font=3>" + str(iHappinessGameAverage) + self.TEXT_HAPPINESS_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, "<font=3>" + str(iHealthGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, "<font=3>" + self.addComma(iNetTradeGameAverage) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		iCol = 4
		screen.setTableText(szTable, iCol, 0, "<font=3>" + self.addComma(iEconomyGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, "<font=3>" + self.addComma(iIndustryGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, "<font=3>" + self.addComma(iAgricultureGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, "<font=3>" + self.addComma(iMilitaryGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, "<font=3>" + self.addComma(iLandAreaGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, "<font=3>" + self.addComma(iPopulationGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, "<font=3>" + str(iHappinessGameWorst) + self.TEXT_HAPPINESS_MEASURE + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, "<font=3>" + str(iHealthGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, "<font=3>" + self.addComma(iNetTradeGameWorst) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		iCol = 5
		screen.setTableText(szTable, iCol, 0, "<font=3>" + self.addComma(iEconomyRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 3, "<font=3>" + self.addComma(iIndustryRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 6, "<font=3>" + self.addComma(iAgricultureRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 9, "<font=3>" + self.addComma(iMilitaryRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 11, "<font=3>" + self.addComma(iLandAreaRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 14, "<font=3>" + self.addComma(iPopulationRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 16, "<font=3>" + str(iHappinessRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 18, "<font=3>" + str(iHealthRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTable, iCol, 21, "<font=3>" + self.addComma(iNetTradeRank) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

		return

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
			

#############################################################################################################
################################################## TOP CITIES ###############################################
#############################################################################################################

	def drawTopCitiesTab(self):
		screen = self.getScreen()
		self.szLeftPaneWidget = self.getNextWidgetName()
		self.X_LEFT_PANE = 30
		self.Y_LEFT_PANE = 70
		self.W_LEFT_PANE = screen.getXResolution()/2 - self.X_LEFT_PANE - 5
		self.H_LEFT_PANE = 620

		# Animated City thingies

		self.X_CITY_ANIMATION = self.X_LEFT_PANE + 20
		self.W_CITY_ANIMATION = 160
		self.H_CITY_ANIMATION = 110
		self.Y_CITY_ANIMATION_BUFFER = self.H_CITY_ANIMATION / 2

		# Placement of Cities

		self.Y_ROWS_CITIES = []
		for i in range(5):
			self.Y_ROWS_CITIES.append(self.Y_LEFT_PANE + 20 + i * 118)

		self.X_CITIES_DESC = self.X_CITY_ANIMATION + self.W_CITY_ANIMATION + 10
		self.Y_CITIES_DESC_BUFFER = -4
		self.W_CITIES_DESC = screen.getXResolution()/2 - self.X_CITIES_DESC - 25
		self.H_CITIES_DESC = 60
		self.Y_CITIES_WONDER_BUFFER = 57
## Transparent Panels ##
		PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			PanelStyle = PanelStyles.PANEL_STYLE_IN
		screen.addPanel( self.szLeftPaneWidget, "", "", true, true, self.X_LEFT_PANE, self.Y_LEFT_PANE, self.W_LEFT_PANE, self.H_LEFT_PANE, PanelStyle)
## Transparent Panels ##
		self.drawTopCities()
		self.drawWondersTab()

	def drawTopCities(self):
		screen = self.getScreen()
		self.lTopCities = []
		self.calculateTopCities()
		self.lTopCities.reverse()
		for i in xrange(len(self.lTopCities)):
			pCity = self.lTopCities[i][1]
			pPlayer = gc.getPlayer(pCity.getOwner())

## Transparent Panels ##
			PanelStyle = PanelStyles.PANEL_STYLE_DAWNTOP
			iX = 8
			if PlatyOptions.bTransparent:
				PanelStyle = PanelStyles.PANEL_STYLE_IN
				iX = 14
			screen.addPanel(self.getNextWidgetName(), "", "", false, true, self.X_CITIES_DESC, self.Y_ROWS_CITIES[i] + self.Y_CITIES_DESC_BUFFER, self.W_CITIES_DESC, self.H_CITIES_DESC, PanelStyle)
## Transparent Panels ##
			if pCity.isRevealed(CyGame().getActiveTeam(), False) or gc.getTeam(pPlayer.getTeam()).isHasMet(CyGame().getActiveTeam()):
				sName = pCity.getName()
				screen.addDDSGFC(self.getNextWidgetName(), gc.getCivilizationInfo(pCity.getCivilizationType()).getButton(), self.X_CITIES_DESC + iX, self.Y_ROWS_CITIES[i] + self.Y_CITIES_DESC_BUFFER + 8 , 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, pCity.getCivilizationType(), 1)
			else:
				sName = CyTranslator().getText("TXT_KEY_UNKNOWN", ())
				screen.addDDSGFC(self.getNextWidgetName(), CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), self.X_CITIES_DESC + iX, self.Y_ROWS_CITIES[i] + self.Y_CITIES_DESC_BUFFER + 8 , 46, 46, WidgetTypes.WIDGET_GENERAL, -1, -1)
			szCityDesc = u"<font=4b>" + str(pCity.getPopulation()) + u"</font>-<font=3b>" + sName.upper() + u"</font>\n"

			iTurnYear = CyGame().getTurnYear(pCity.getGameTurnFounded())
			szTurnFounded = CyTranslator().getText("TXT_KEY_TIME_AD", (iTurnYear,))
			if iTurnYear < 0:
				szTurnFounded = CyTranslator().getText("TXT_KEY_TIME_BC", (-iTurnYear,))
			szCityDesc += CyTranslator().getText("TXT_KEY_MISC_FOUNDED_IN", (szTurnFounded,))
			screen.addMultilineText(self.getNextWidgetName(), szCityDesc, self.X_CITIES_DESC + iX + 46, self.Y_ROWS_CITIES[i] + self.Y_CITIES_DESC_BUFFER + 3, self.W_CITIES_DESC - 6, self.H_CITIES_DESC - 6, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iCityX = pCity.getX()
			iCityY = pCity.getY()
			pPlot = CyMap().plot(iCityX, iCityY)

			iDistance = min(350, 200 + (pCity.getPopulation() * 5))			
			if pCity.isRevealed(CyGame().getActiveTeam(), False):			
				screen.addPlotGraphicGFC(self.getNextWidgetName(), self.X_CITY_ANIMATION, self.Y_ROWS_CITIES[i] + self.Y_CITY_ANIMATION_BUFFER - self.H_CITY_ANIMATION / 2, self.W_CITY_ANIMATION, self.H_CITY_ANIMATION, pPlot, iDistance, false, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.drawCityWonderIcons()
		return

	def drawCityWonderIcons(self):
		screen = self.getScreen()
		for i in xrange(len(self.lTopCities)):
			pCity = self.lTopCities[i][1]
			szIconPanel = self.getNextWidgetName()
## Transparent Panels ##
			PanelStyle = PanelStyles.PANEL_STYLE_DAWNTOP
			if PlatyOptions.bTransparent:
				PanelStyle = PanelStyles.PANEL_STYLE_IN
			screen.addPanel( szIconPanel, "", "", false, true, self.X_CITIES_DESC, self.Y_ROWS_CITIES[i] + self.Y_CITIES_WONDER_BUFFER + self.Y_CITIES_DESC_BUFFER, self.W_CITIES_DESC, self.H_CITIES_DESC, PanelStyle)
## Transparent Panels ##
			for iBuilding in xrange(gc.getNumBuildingInfos()):
				BuildingInfo = gc.getBuildingInfo(iBuilding)
				if (isWorldWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
					if pCity.getNumBuilding(iBuilding):
						screen.attachImageButton( szIconPanel, "", BuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, -1, False )

	def calculateTopCities(self):
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			(pCity, iter) = pPlayer.firstCity(False)
			while(pCity):
				iTotalCityValue = (pCity.getCulture(iPlayer) /5 + pCity.getYieldRate(YieldTypes.YIELD_FOOD) + pCity.getYieldRate(YieldTypes.YIELD_PRODUCTION) + pCity.getYieldRate(YieldTypes.YIELD_COMMERCE)) * pCity.getPopulation()
				if len(self.lTopCities) < 5:
					self.lTopCities.append([iTotalCityValue, pCity])
					self.lTopCities.sort()
				elif self.lTopCities[0][0] < iTotalCityValue:
					self.lTopCities[0] = [iTotalCityValue, pCity]
					self.lTopCities.sort()
				(pCity, iter) = pPlayer.nextCity(iter, False)

#############################################################################################################
################################################### WONDERS #################################################
#############################################################################################################

	def drawWondersTab(self):

		screen = self.getScreen()
		self.X_RIGHT_PANE = screen.getXResolution()/2 + 5
		self.Y_RIGHT_PANE = 70
		self.W_RIGHT_PANE = screen.getXResolution() - self.X_RIGHT_PANE - 30
		self.H_RIGHT_PANE = 620
		self.iWonderID = -1
		self.szRightPaneWidget = self.getNextWidgetName()
## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
		screen.addPanel( self.szRightPaneWidget, "", "", true, true, self.X_RIGHT_PANE, self.Y_RIGHT_PANE, self.W_RIGHT_PANE, self.H_RIGHT_PANE, self.PanelStyle)
## Transparent Panels ##

		# Info about this wonder, e.g. name, cost so on

		self.X_STATS_PANE = self.X_RIGHT_PANE + 20
		self.Y_STATS_PANE = self.Y_RIGHT_PANE + 20
		self.W_STATS_PANE = 210
		self.H_STATS_PANE = 220

		# Wonder mode dropdown Box

		self.X_DROPDOWN = self.X_STATS_PANE + self.W_STATS_PANE + 20
		self.Y_DROPDOWN = self.Y_RIGHT_PANE + 20
		self.W_DROPDOWN = screen.getXResolution() - self.X_DROPDOWN - 50

		# List Box that displays all wonders built
		self.Y_WONDER_LIST = self.Y_RIGHT_PANE + 60
		self.H_WONDER_LIST = 180

		# Animated Wonder thingies
		self.Y_WONDER_GRAPHIC = self.Y_STATS_PANE + self.H_STATS_PANE + 15
		self.W_WONDER_GRAPHIC = self.W_RIGHT_PANE - 40
		self.H_WONDER_GRAPHIC = 150

		self.X_ROTATION_WONDER_ANIMATION = -20
		self.Z_ROTATION_WONDER_ANIMATION = 30
		self.SCALE_ANIMATION = 1

		# Icons used for Projects instead because no on-map art exists
		self.X_PROJECT_ICON = self.X_STATS_PANE + self.W_WONDER_GRAPHIC / 2
		self.Y_PROJECT_ICON = self.Y_WONDER_GRAPHIC + self.H_WONDER_GRAPHIC / 2
		self.W_PROJECT_ICON = 128

		# Special Stats about this wonder
		self.Y_SPECIAL_TITLE = self.Y_WONDER_GRAPHIC + self.H_WONDER_GRAPHIC
		self.Y_SPECIAL_PANE = self.Y_SPECIAL_TITLE + 25
		self.H_SPECIAL_PANE = self.Y_RIGHT_PANE + self.H_RIGHT_PANE - self.Y_SPECIAL_PANE - 20

		self.drawWondersDropdownBox()
		self.calculateWondersList()
		self.drawWondersList()

	def drawWondersDropdownBox(self):
		screen = self.getScreen()
		self.szWondersDropdownWidget = self.getNextWidgetName()
		screen.addDropDownBoxGFC(self.szWondersDropdownWidget, self.X_DROPDOWN, self.Y_DROPDOWN, self.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString(self.szWondersDropdownWidget, CyTranslator().getText("TXT_KEY_TOP_CITIES_SCREEN_WORLD_WONDERS", ()), 0, 0, self.szWonderDisplayMode == "World Wonders")
		screen.addPullDownString(self.szWondersDropdownWidget, CyTranslator().getText("TXT_KEY_TOP_CITIES_SCREEN_NATIONAL_WONDERS", ()), 1, 1, self.szWonderDisplayMode == "National Wonders")
		screen.addPullDownString(self.szWondersDropdownWidget, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, self.szWonderDisplayMode == "Projects")
		return

	def determineListBoxContents(self):

		screen = self.getScreen()
		self.aiWonderListBoxIDs = []
		self.aiTurnYearBuilt = []
		self.aiWonderBuiltBy = []
		self.aszWonderCity = []
		iRow = 0

		if self.szWonderDisplayMode == "Projects":
			for iWonderLoop in self.aaWondersBeingBuilt:
				screen.appendTableRow(self.szWondersListBox)
				iProjectType = iWonderLoop[0]
				pProjectInfo = gc.getProjectInfo(iProjectType)

				self.aiWonderListBoxIDs.append(iProjectType)
				self.aiTurnYearBuilt.append(-6666)
				self.aiWonderBuiltBy.append(iWonderLoop[1])

				iTeam = iWonderLoop[1]
				iLeader = gc.getTeam(iTeam).getLeaderID()
				pPlayer = gc.getPlayer(iLeader)
				sButton = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton()
				screen.setTableText(self.szWondersListBox, 0, iRow, "", sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(self.szWondersListBox, 1, iRow, "<font=3>" + "*" + pProjectInfo.getDescription() + "</font>", pProjectInfo.getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1

			for iWonderLoop in self.aaWondersBuilt:
				screen.appendTableRow(self.szWondersListBox)
				iProjectType = iWonderLoop[1]
				pProjectInfo = gc.getProjectInfo(iProjectType)

				self.aiWonderListBoxIDs.append(iProjectType)
				self.aiTurnYearBuilt.append(-9999)
				self.aiWonderBuiltBy.append(iWonderLoop[2])

				sButton = ""
				iTeam = iWonderLoop[2]
				sColor = ""
				if iTeam == -1:
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
				else:
					iLeader = gc.getTeam(iTeam).getLeaderID()
					pPlayer = gc.getPlayer(iLeader)
					sButton = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton()
				screen.setTableText(self.szWondersListBox, 0, iRow, "", sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(self.szWondersListBox, 1, iRow, "<font=3>" + pProjectInfo.getDescription() + "</font>", pProjectInfo.getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
		else:
			for iWonderLoop in self.aaWondersBeingBuilt:
				screen.appendTableRow(self.szWondersListBox)
				iWonderType = iWonderLoop[0]
				pWonderInfo = gc.getBuildingInfo(iWonderType)

				self.aiWonderListBoxIDs.append(iWonderType)
				self.aiTurnYearBuilt.append(-9999)
				self.aiWonderBuiltBy.append(iWonderLoop[1])
				self.aszWonderCity.append("")

				iPlayer = iWonderLoop[1]
				pPlayer = gc.getPlayer(iPlayer)
				sButton = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton()
				screen.setTableText(self.szWondersListBox, 0, iRow, "", sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(self.szWondersListBox, 1, iRow, "<font=3>" + "*" + pWonderInfo.getDescription() + "</font>", pWonderInfo.getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1

			for iWonderLoop in self.aaWondersBuilt:
				screen.appendTableRow(self.szWondersListBox)
				iWonderType = iWonderLoop[1]
				pWonderInfo = gc.getBuildingInfo(iWonderType)

				self.aiWonderListBoxIDs.append(iWonderType)
				self.aiTurnYearBuilt.append(iWonderLoop[0])
				self.aiWonderBuiltBy.append(iWonderLoop[2])
				self.aszWonderCity.append(iWonderLoop[3])

				sButton = ""
				iPlayer = iWonderLoop[2]
				if iPlayer == -1:
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
				else:
					pPlayer = gc.getPlayer(iPlayer)
					sButton = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton()
				screen.setTableText(self.szWondersListBox, 0, iRow, "", sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(self.szWondersListBox, 1, iRow, "<font=3>" + pWonderInfo.getDescription() + "</font>", pWonderInfo.getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1

	def drawWondersList(self):

		screen = self.getScreen()

		if (self.iNumWondersPermanentWidgets == 0):
			self.szWondersListBox = self.getNextWidgetName()
			screen.addTableControlGFC(self.szWondersListBox, 2, self.X_DROPDOWN, self.Y_WONDER_LIST, self.W_DROPDOWN, self.H_WONDER_LIST, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
			screen.setTableColumnHeader(self.szWondersListBox, 0, "", 24)
			screen.setTableColumnHeader(self.szWondersListBox, 1, "", self.W_DROPDOWN - 24)
			self.determineListBoxContents()
			self.iNumWondersPermanentWidgets = self.nWidgetCount

		# Stats Panel
		panelName = self.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true, self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, PanelStyles.PANEL_STYLE_IN)

		# Set default wonder if any exist in this list
		if len(self.aaWondersBuilt) + len(self.aaWondersBeingBuilt) > 0 and self.iWonderID == -1:
			self.iWonderID = 0

		# Only display/do the following if a wonder is actively being displayed
		if self.iWonderID > -1:

############################################### DISPLAY PROJECT MODE ###############################################

			if self.szWonderDisplayMode == "Projects":

				pProjectInfo = gc.getProjectInfo(self.aiWonderListBoxIDs[self.iWonderID])

				# Stats panel (cont'd) - Name
				szStatsText = u"<font=3b>" + pProjectInfo.getDescription().upper() + u"</font>\n\n"

				iTurnYear = self.aiTurnYearBuilt[self.iWonderID]
				if (iTurnYear == -6666):	# -6666 used for wonders in progress
					szTempText = CyTranslator().getText("TXT_KEY_BEING_BUILT", ())
				else:
					szTempText = CyTranslator().getText("TXT_KEY_INFO_SCREEN_BUILT", ())

				iTeam = self.aiWonderBuiltBy[self.iWonderID]
				if iTeam == -1:
					sName = CyTranslator().getText("TXT_KEY_UNKNOWN", ())
				else:
					sName = gc.getTeam(iTeam).getName()
				szStatsText += "%s, %s\n\n" %(sName, szTempText)

				if pProjectInfo.getProductionCost() > 0:
					szCost = CyTranslator().getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getProjectProductionNeeded(self.iWonderID),))
					szStatsText += szCost.upper() + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) + "\n"

				if isWorldProject(self.aiWonderListBoxIDs[self.iWonderID]):
					iMaxInstances = gc.getProjectInfo(self.aiWonderListBoxIDs[self.iWonderID]).getMaxGlobalInstances()
					szProjectType = CyTranslator().getText("TXT_KEY_PEDIA_WORLD_PROJECT", ())
					if iMaxInstances > 1:
						szProjectType += " " + CyTranslator().getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
					szStatsText += szProjectType.upper() + "\n"

				if isTeamProject(self.aiWonderListBoxIDs[self.iWonderID]):
					iMaxInstances = gc.getProjectInfo(self.iWonderID).getMaxTeamInstances()
					szProjectType = CyTranslator().getText("TXT_KEY_PEDIA_TEAM_PROJECT", ())
					if iMaxInstances > 1:
						szProjectType += " " + CyTranslator().getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
					szStatsText += szProjectType.upper()

				screen.addMultilineText(self.getNextWidgetName(), szStatsText, self.X_STATS_PANE + 5, self.Y_STATS_PANE + 15, self.W_STATS_PANE - 10, self.H_STATS_PANE - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Add Graphic
				iIconX = self.X_PROJECT_ICON - self.W_PROJECT_ICON / 2
				iIconY = self.Y_PROJECT_ICON - self.W_PROJECT_ICON / 2

				screen.addDDSGFC(self.getNextWidgetName(), gc.getProjectInfo(self.aiWonderListBoxIDs[self.iWonderID]).getButton(), iIconX, iIconY, self.W_PROJECT_ICON, self.W_PROJECT_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )

				# Special Abilities ListBox

				szSpecialTitle = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u"</font>"
				self.szSpecialTitleWidget = self.getNextWidgetName()
				screen.setText(self.szSpecialTitleWidget, "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE, self.Y_SPECIAL_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				panelName = self.getNextWidgetName()
				screen.addPanel( panelName, "", "", true, true, self.X_STATS_PANE, self.Y_SPECIAL_PANE, self.W_WONDER_GRAPHIC, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_IN)

				listName = self.getNextWidgetName()
				screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
				screen.enableSelect(listName, False)

				szSpecialText = CyGameTextMgr().getProjectHelp(self.aiWonderListBoxIDs[self.iWonderID], True, None)
				splitText = string.split( szSpecialText, "\n" )
				for special in splitText:
					if len( special ) != 0:
						screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

			else:

	############################################### DISPLAY WONDER MODE ###############################################

				pWonderInfo = gc.getBuildingInfo(self.aiWonderListBoxIDs[self.iWonderID])

				# Stats panel (cont'd) - Name
				szStatsText = u"<font=3b>" + pWonderInfo.getDescription().upper() + u"</font>\n\n"

				# Wonder built-in year
				iTurnYear = self.aiTurnYearBuilt[self.iWonderID]

				szDateBuilt = ""

				if (iTurnYear != -9999):	# -9999 used for wonders in progress
					if (iTurnYear < 0):
						szTurnFounded = CyTranslator().getText("TXT_KEY_TIME_BC", (-iTurnYear,))
					else:
						szTurnFounded = CyTranslator().getText("TXT_KEY_TIME_AD", (iTurnYear,))

					szDateBuilt = (", %s" %(szTurnFounded))

				else:
					szDateBuilt = (", %s" %(CyTranslator().getText("TXT_KEY_BEING_BUILT", ())))

				iPlayer = self.aiWonderBuiltBy[self.iWonderID]
				if iPlayer == -1:
					sName = CyTranslator().getText("TXT_KEY_UNKNOWN", ())
				else:
					sName = gc.getPlayer(iPlayer).getName()
				szStatsText += "%s%s\n" %(sName, szDateBuilt)
				
				if (self.aszWonderCity[self.iWonderID] != ""):
					szStatsText += self.aszWonderCity[self.iWonderID] + "\n\n"
				else:
					szStatsText += "\n"

				# Building attributes

				if (pWonderInfo.getProductionCost() > 0):
					szCost = CyTranslator().getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getBuildingProductionNeeded(self.aiWonderListBoxIDs[self.iWonderID]),))
					szStatsText += szCost.upper() + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) + "\n"

				for k in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
					if (pWonderInfo.getObsoleteSafeCommerceChange(k) != 0):
						szSign = ""
						if (pWonderInfo.getObsoleteSafeCommerceChange(k) > 0):
							szSign = "+"
						szCommerce = gc.getCommerceInfo(k).getDescription() + ": "

						szStatsText += szCommerce.upper() + szSign + str(pWonderInfo.getObsoleteSafeCommerceChange(k)) + (u"%c" % (gc.getCommerceInfo(k).getChar())) + "\n"

				if pWonderInfo.getHappiness() > 0:
					szStatsText += (u"%s%c\n" % (CyTranslator().getText("TXT_KEY_PEDIA_HAPPY", (pWonderInfo.getHappiness(),)), CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)))

				elif pWonderInfo.getHappiness() < 0:
					szStatsText += (u"%s%c\n" % (CyTranslator().getText("TXT_KEY_PEDIA_UNHAPPY", (-pWonderInfo.getHappiness(),)), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR)))

				if pWonderInfo.getHealth() > 0:
					szStatsText += (u"%s%c\n" % (CyTranslator().getText("TXT_KEY_PEDIA_HEALTHY", (pWonderInfo.getHealth(),)), CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)))

				elif pWonderInfo.getHealth() < 0:
					szStatsText += (u"%s%c\n" % (CyTranslator().getText("TXT_KEY_PEDIA_UNHEALTHY", (-pWonderInfo.getHealth(),)), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR)))
					
				if pWonderInfo.getGreatPeopleRateChange() != 0:
					szStatsText += (u"%s%c\n" % (CyTranslator().getText("TXT_KEY_PEDIA_GREAT_PEOPLE", (pWonderInfo.getGreatPeopleRateChange(),)).upper(), CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)))

				screen.addMultilineText(self.getNextWidgetName(), szStatsText, self.X_STATS_PANE + 5, self.Y_STATS_PANE + 15, self.W_STATS_PANE - 10, self.H_STATS_PANE - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

				# Add Graphic
				screen.addBuildingGraphicGFC(self.getNextWidgetName(), self.aiWonderListBoxIDs[self.iWonderID], self.X_STATS_PANE, self.Y_WONDER_GRAPHIC, self.W_WONDER_GRAPHIC, self.H_WONDER_GRAPHIC,
				    WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_WONDER_ANIMATION, self.Z_ROTATION_WONDER_ANIMATION, self.SCALE_ANIMATION, True)

				# Special Abilities ListBox

				szSpecialTitle = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u"</font>"
				self.szSpecialTitleWidget = self.getNextWidgetName()
				screen.setText(self.szSpecialTitleWidget, "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE, self.Y_SPECIAL_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				panelName = self.getNextWidgetName()
				screen.addPanel( panelName, "", "", true, true, self.X_STATS_PANE, self.Y_SPECIAL_PANE, self.W_WONDER_GRAPHIC, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_IN)

				listName = self.getNextWidgetName()
				screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
				screen.enableSelect(listName, False)

				szSpecialText = CyGameTextMgr().getBuildingHelp(self.aiWonderListBoxIDs[self.iWonderID], True, False, False, None)
				splitText = string.split( szSpecialText, "\n" )
				for special in splitText:
					if len( special ) != 0:
						screen.appendListBoxString( listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

	def calculateWondersList(self):
		self.aaWondersBeingBuilt = []
		self.aaWondersBuilt = []

		self.pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
		iActiveTeam = self.pActivePlayer.getTeam()

		# Loop through players to determine Wonders
		for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):

			pPlayer = gc.getPlayer(iPlayerLoop)
			iPlayerTeam = pPlayer.getTeam()

			# Only display national wonders for the active player's team
 			if self.szWonderDisplayMode != "National Wonders" or iPlayerTeam == iActiveTeam:

				(pCity, iter) = pPlayer.firstCity(False)
				while(pCity):

					pCityPlot = CyMap().plot(pCity.getX(), pCity.getY())
					
					# Check to see if active player can see this city
					szCityName = ""
					if pCityPlot.isActiveVisible(false):
						szCityName = pCity.getName()
					
					# Loop through projects to find any under construction
					if self.szWonderDisplayMode == "Projects" and iPlayerTeam == iActiveTeam:
						for iProjectLoop in xrange(gc.getNumProjectInfos()):
							if pCity.getProductionProject() == iProjectLoop:
								pProject = gc.getProjectInfo(iProjectLoop)
								self.aaWondersBeingBuilt.append([iProjectLoop, iPlayerTeam])

					# Loop through buildings
					else:
						for iBuildingLoop in xrange(gc.getNumBuildingInfos()):
							if (self.szWonderDisplayMode == "World Wonders" and isWorldWonderClass(gc.getBuildingInfo(iBuildingLoop).getBuildingClassType())):
								if pCity.getProductionBuilding() == iBuildingLoop and iPlayerTeam == iActiveTeam:
									self.aaWondersBeingBuilt.append([iBuildingLoop, iPlayerLoop])

								if pCity.getNumBuilding(iBuildingLoop):
									if (iPlayerTeam == iActiveTeam or gc.getTeam(iActiveTeam).isHasMet(iPlayerTeam)):								
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,iPlayerLoop,szCityName])
									else:
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,-1,CyTranslator().getText("TXT_KEY_UNKNOWN", ())])

							# National/Team Wonder Mode
							elif (self.szWonderDisplayMode == "National Wonders" and (isNationalWonderClass(gc.getBuildingInfo(iBuildingLoop).getBuildingClassType()) or isTeamWonderClass(gc.getBuildingInfo(iBuildingLoop).getBuildingClassType()))):
								if pCity.getProductionBuilding() == iBuildingLoop and iPlayerTeam == iActiveTeam:
									self.aaWondersBeingBuilt.append([iBuildingLoop, iPlayerLoop])

								if pCity.getNumBuilding(iBuildingLoop):
									if (iPlayerTeam == iActiveTeam or gc.getTeam(iActiveTeam).isHasMet(iPlayerTeam)):								
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,iPlayerLoop, szCityName])
									else:
										self.aaWondersBuilt.append([pCity.getBuildingOriginalTime(iBuildingLoop),iBuildingLoop,-1, CyTranslator().getText("TXT_KEY_UNKNOWN", ())])
					(pCity, iter) = pPlayer.nextCity(iter, False)
		# Project Mode
		if self.szWonderDisplayMode == "Projects":
			for iTeamLoop in xrange(gc.getMAX_TEAMS()):
				pTeam = gc.getTeam(iTeamLoop)
				if pTeam.isAlive():
					for iProjectLoop in xrange(gc.getNumProjectInfos()):
						for iI in xrange(pTeam.getProjectCount(iProjectLoop)):
							if iTeamLoop == iActiveTeam or pTeam.isHasMet(iActiveTeam):								
								self.aaWondersBuilt.append([-9999,iProjectLoop,iTeamLoop,szCityName])
							else:
								self.aaWondersBuilt.append([-9999,iProjectLoop,-1,CyTranslator().getText("TXT_KEY_UNKNOWN", ())])

		# Sort wonders in order of date built
		self.aaWondersBuilt.sort()
		self.aaWondersBuilt.reverse()

#############################################################################################################
################################################## STATISTICS ###############################################
#############################################################################################################

	def drawStatsTab(self):

		screen = self.getScreen()

		self.Y_STATS_TOP_CHART = 130
		self.W_STATS_TOP_CHART = screen.getXResolution() * 2/5
		self.X_STATS_TOP_CHART = screen.getXResolution()/2 - self.W_STATS_TOP_CHART/2
		self.H_STATS_TOP_CHART = 100
		self.Y_LEADER_ICON = 95
		self.H_LEADER_ICON = 140
		self.W_LEADER_ICON = 110
		self.X_LEADER_ICON = self.X_STATS_TOP_CHART - self.W_LEADER_ICON - 20
		self.Y_LEADER_NAME = self.Y_STATS_TOP_CHART - 40

		player = gc.getPlayer(self.iActivePlayer)
		iMinutesPlayed = CyGame().getMinutesPlayed()
		iHoursPlayed = iMinutesPlayed / 60
		iMinutesPlayed = iMinutesPlayed % 60

		szMinutesString = str(iMinutesPlayed)
		if (iMinutesPlayed < 10):
			szMinutesString = "0" + szMinutesString
		szHoursString = str(iHoursPlayed)
		if (iHoursPlayed < 10):
			szHoursString = "0" + szHoursString

		szTimeString = szHoursString + ":" + szMinutesString

		iNumCitiesBuilt = CyStatistics().getPlayerNumCitiesBuilt(self.iActivePlayer)
		iNumCitiesRazed = CyStatistics().getPlayerNumCitiesRazed(self.iActivePlayer)

		iNumReligionsFounded = 0
		for i in xrange(gc.getNumReligionInfos()):
			if CyStatistics().getPlayerReligionFounded(self.iActivePlayer, i):
				iNumReligionsFounded += 1

################################################### TOP PANEL ###################################################

		# Leaderhead graphic
		szLeaderWidget = self.getNextWidgetName()
		screen.addLeaderheadGFC(szLeaderWidget, player.getLeaderType(), AttitudeTypes.ATTITUDE_PLEASED, self.X_LEADER_ICON, self.Y_LEADER_ICON, self.W_LEADER_ICON, self.H_LEADER_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Leader Name
		self.szLeaderNameWidget = self.getNextWidgetName()
		szText = u"<font=4b>" + player.getName() + u"</font>"
		screen.setText(self.szLeaderNameWidget, "", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_TOP_CHART, self.Y_LEADER_NAME, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Create Table
		szTopChart = self.getNextWidgetName()
		screen.addTableControlGFC(szTopChart, 2, self.X_STATS_TOP_CHART, self.Y_STATS_TOP_CHART, self.W_STATS_TOP_CHART, self.H_STATS_TOP_CHART, False, True, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szTopChart, 0, "", self.W_STATS_TOP_CHART *3/4)
		screen.setTableColumnHeader(szTopChart, 1, "", self.W_STATS_TOP_CHART/4)
		for i in xrange(4):
			screen.appendTableRow(szTopChart)

		screen.setTableText(szTopChart, 0, 0, "<font=3>" + CyTranslator().getText("TXT_KEY_INFO_SCREEN_TIME_PLAYED", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTopChart, 1, 0, "<font=3>" + szTimeString + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTopChart, 0, 1, "<font=3>" + CyTranslator().getText("TXT_KEY_INFO_SCREEN_CITIES_BUILT", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTopChart, 1, 1, "<font=3>" + str(iNumCitiesBuilt) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTopChart, 0, 2, "<font=3>" + CyTranslator().getText("TXT_KEY_INFO_SCREEN_CITIES_RAZED", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTopChart, 1, 2, "<font=3>" + str(iNumCitiesRazed) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
		screen.setTableText(szTopChart, 0, 3, "<font=3>" + CyTranslator().getText("TXT_KEY_INFO_SCREEN_RELIGIONS_FOUNDED", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTopChart, 1, 3, "<font=3>" + str(iNumReligionsFounded) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)

################################################### BOTTOM PANEL ###################################################

		self.X_STATS_BOTTOM_CHART = 30
		self.Y_STATS_BOTTOM_CHART = 280
		iWidth = screen.getXResolution() - (self.X_STATS_BOTTOM_CHART * 2)
		self.H_STATS_BOTTOM_CHART = (screen.getYResolution() - self.Y_STATS_BOTTOM_CHART - 65)/24 * 24 + 2	
		self.szInfoTable = self.getNextWidgetName()
		screen.addDropDownBoxGFC(self.szInfoTable, self.X_STATS_BOTTOM_CHART, self.Y_STATS_BOTTOM_CHART - 40, screen.getXResolution()/6, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString(self.szInfoTable, CyTranslator().getText("TXT_KEY_CONCEPT_UNITS",()), 0, 0, self.iInfoTable == 0)
		screen.addPullDownString(self.szInfoTable, CyTranslator().getText("TXT_KEY_CONCEPT_BUILDINGS",()), 1, 1, self.iInfoTable == 1)
		screen.addPullDownString(self.szInfoTable, CyTranslator().getText("TXT_KEY_CONCEPT_RESOURCES",()), 2, 2, self.iInfoTable == 2)
		szTable1 = self.getNextWidgetName()
		szTable2 = self.getNextWidgetName()
		szTable3 = self.getNextWidgetName()
		lList1 = []
		lList2 = []

		if self.iInfoTable == 0:
			iColWidth = iWidth / 11
			screen.addTableControlGFC(szTable1, 5, self.X_STATS_BOTTOM_CHART, self.Y_STATS_BOTTOM_CHART, iColWidth * 7, self.H_STATS_BOTTOM_CHART,
					  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(szTable1)

			screen.addTableControlGFC(szTable2, 2, self.X_STATS_BOTTOM_CHART + iColWidth * 7, self.Y_STATS_BOTTOM_CHART, iColWidth * 4, self.H_STATS_BOTTOM_CHART,
					  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(szTable2)

			screen.setTableColumnHeader(szTable1, 0, CyTranslator().getText("TXT_KEY_CONCEPT_UNITS", ()), iColWidth * 3)
			screen.setTableColumnHeader(szTable1, 1, CyTranslator().getText("TXT_KEY_CURRENT", ()), iColWidth)
			screen.setTableColumnHeader(szTable1, 2, CyTranslator().getText("TXT_KEY_INFO_SCREEN_BUILT", ()), iColWidth)
			screen.setTableColumnHeader(szTable1, 3, CyTranslator().getText("TXT_KEY_INFO_SCREEN_KILLED", ()), iColWidth)
			screen.setTableColumnHeader(szTable1, 4, CyTranslator().getText("TXT_KEY_INFO_SCREEN_LOST", ()), iColWidth)
			screen.setTableColumnHeader(szTable2, 0, CyTranslator().getText("TXT_KEY_CONCEPT_PROMOTIONS", ()), iColWidth * 3)
			screen.setTableColumnHeader(szTable2, 1, CyTranslator().getText("TXT_KEY_CURRENT", ()), iColWidth)
				
	
			for i in xrange(gc.getNumUnitInfos()):
				lList1.append(0)
			for i in xrange(gc.getNumPromotionInfos()):
				lList2.append(0)

			(pUnit, iter) = player.firstUnit(False)
			while(pUnit):
				lList1[pUnit.getUnitType()] += 1
				for i in xrange(gc.getNumPromotionInfos()):
					if pUnit.isHasPromotion(i):
						lList2[i] += 1
				(pUnit, iter) = player.nextUnit(iter, False)

			for i in xrange(gc.getNumUnitInfos()):
				if not CyGame().isUnitEverActive(i): continue
				iRow = screen.appendTableRow(szTable1)
				screen.setTableText(szTable1, 0, iRow, "<font=3>" + gc.getUnitInfo(i).getDescription() + "</font>", gc.getUnitInfo(i).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt(szTable1, 1, iRow, "<font=3>" + self.getColorText(lList1[i]) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable1, 2, iRow, "<font=3>" + self.getColorText(CyStatistics().getPlayerNumUnitsBuilt(self.iActivePlayer, i)) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable1, 3, iRow, "<font=3>" + self.getColorText(CyStatistics().getPlayerNumUnitsKilled(self.iActivePlayer, i)) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable1, 4, iRow, "<font=3>" + self.getColorText(CyStatistics().getPlayerNumUnitsLost(self.iActivePlayer, i)) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

			for i in xrange(gc.getNumPromotionInfos()):
				iRow = screen.appendTableRow(szTable2)
				screen.setTableText(szTable2, 0, iRow, "<font=3>" + gc.getPromotionInfo(i).getDescription() + "</font>", gc.getPromotionInfo(i).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt(szTable2, 1, iRow, "<font=3>" + self.getColorText(lList2[i]) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		elif self.iInfoTable == 1:
			iColWidth = iWidth / 14
			screen.addTableControlGFC(szTable1, 3, self.X_STATS_BOTTOM_CHART, self.Y_STATS_BOTTOM_CHART, iColWidth * 5, self.H_STATS_BOTTOM_CHART,
					  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(szTable1)

			screen.addTableControlGFC(szTable2, 3, self.X_STATS_BOTTOM_CHART + iColWidth * 5, self.Y_STATS_BOTTOM_CHART, iColWidth * 5, self.H_STATS_BOTTOM_CHART,
					  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(szTable2)

			screen.addTableControlGFC(szTable3, 2, self.X_STATS_BOTTOM_CHART + iColWidth * 10, self.Y_STATS_BOTTOM_CHART, iColWidth * 4, self.H_STATS_BOTTOM_CHART,
					  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(szTable3)

			screen.setTableColumnHeader(szTable1, 0, CyTranslator().getText("TXT_KEY_CONCEPT_BUILDINGS", ()), iColWidth * 3)
			screen.setTableColumnHeader(szTable1, 1, CyTranslator().getText("TXT_KEY_INFO_SCREEN_BUILT", ()), iColWidth)
			screen.setTableColumnHeader(szTable1, 2, CyTranslator().getText("TXT_KEY_CURRENT", ()), iColWidth)

			screen.setTableColumnHeader(szTable2, 0, CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()), iColWidth * 3)
			screen.setTableColumnHeader(szTable2, 1, CyTranslator().getText("TXT_KEY_INFO_SCREEN_BUILT", ()), iColWidth)
			screen.setTableColumnHeader(szTable2, 2, CyTranslator().getText("TXT_KEY_CURRENT", ()), iColWidth)

			screen.setTableColumnHeader(szTable3, 0, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), iColWidth * 3)
			screen.setTableColumnHeader(szTable3, 1, CyTranslator().getText("TXT_KEY_CURRENT", ()), iColWidth)

			for i in xrange(gc.getNumBuildingInfos()):
				lList1.append(0)

			(pCity, iter) = player.firstCity(False)
			while(pCity):
				for i in xrange(gc.getNumBuildingInfos()):
					if pCity.isHasBuilding(i):
						lList1[i] += 1
				(pCity, iter) = player.nextCity(iter, False)

			for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
				i = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationBuildings(iBuildingClass)
				if i == -1: continue
				szTable = szTable1
				if isLimitedWonderClass(iBuildingClass):
					szTable = szTable2
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, iRow, "<font=3>" + gc.getBuildingInfo(i).getDescription() + "</font>", gc.getBuildingInfo(i).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt(szTable, 1, iRow, "<font=3>" + self.getColorText(CyStatistics().getPlayerNumBuildingsBuilt(self.iActivePlayer, i)) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable, 2, iRow, "<font=3>" + self.getColorText(lList1[i]) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

			for i in xrange(gc.getNumProjectInfos()):
				iRow = screen.appendTableRow(szTable3)
				screen.setTableText(szTable3, 0, iRow, "<font=3>" + gc.getProjectInfo(i).getDescription() + "</font>", gc.getProjectInfo(i).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt(szTable3, 1, iRow, "<font=3>" + self.getColorText(gc.getTeam(player.getTeam()).getProjectCount(i)) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		elif self.iInfoTable == 2:
			iColWidth = iWidth / 11
			screen.addTableControlGFC(szTable1, 5, self.X_STATS_BOTTOM_CHART, self.Y_STATS_BOTTOM_CHART, iColWidth * 7, self.H_STATS_BOTTOM_CHART,
					  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(szTable1)

			screen.addTableControlGFC(szTable2, 2, self.X_STATS_BOTTOM_CHART + iColWidth * 7, self.Y_STATS_BOTTOM_CHART, iColWidth * 4, self.H_STATS_BOTTOM_CHART,
					  True, True, 24,24, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSort(szTable2)

			screen.setTableColumnHeader(szTable1, 0, CyTranslator().getText("TXT_KEY_CONCEPT_RESOURCES", ()), iColWidth * 3)
			screen.setTableColumnHeader(szTable1, 1, "<font=3>" + CyTranslator().getText("TXT_KEY_LOCAL", ()) + "</font>", iColWidth)
			screen.setTableColumnHeader(szTable1, 2, "<font=3>" + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()) + "</font>", iColWidth)
			screen.setTableColumnHeader(szTable1, 3, "<font=3>" + CyTranslator().getText("TXT_KEY_DEMO_SCREEN_IMPORTS_TEXT", ()) + "</font>", iColWidth)
			screen.setTableColumnHeader(szTable1, 4, "<font=3>" + CyTranslator().getText("TXT_KEY_BONUS_TOTAL", ()) + "</font>", iColWidth)

			screen.setTableColumnHeader(szTable2, 0, CyTranslator().getText("TXT_KEY_CONCEPT_IMPROVEMENTS", ()), iColWidth * 3)
			screen.setTableColumnHeader(szTable2, 1, CyTranslator().getText("TXT_KEY_CURRENT", ()), iColWidth)

			for i in xrange(gc.getNumImprovementInfos()):
				lList1.append(0)

			for i in xrange(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.getOwner() != self.iActivePlayer: continue
				iImprovement = pPlot.getImprovementType()
				if iImprovement > -1:
					lList1[iImprovement] += 1

			for i in xrange(gc.getNumBonusInfos()):
				iRow = screen.appendTableRow(szTable1)
				screen.setTableText(szTable1, 0, iRow, "<font=3>" + gc.getBonusInfo(i).getDescription() + "</font>", gc.getBonusInfo(i).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt(szTable1, 1, iRow, self.getColorText(player.countOwnedBonuses(i)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable1, 2, iRow, self.getColorText(player.getBonusExport(i)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable1, 3, iRow, self.getColorText(player.getBonusImport(i)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableInt(szTable1, 4, iRow, self.getColorText(player.getNumAvailableBonuses(i)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

			for i in xrange(gc.getNumImprovementInfos()):
				Info = gc.getImprovementInfo(i)
				if Info.isGraphicalOnly(): continue
				iRow = screen.appendTableRow(szTable2)
				screen.setTableText(szTable2, 0, iRow, "<font=3>" + Info.getDescription() + "</font>", Info.getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableInt(szTable2, 1, iRow, "<font=3>" + self.getColorText(lList1[i]) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

	def getColorText(self, iCount):
		sText = str(iCount)
		if iCount > 0:
			sText = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ()) + sText + "</color>"
		return sText

#############################################################################################################
##################################################### OTHER #################################################
#############################################################################################################

	def drawLine (self, screen, canvas, x0, y0, x1, y1, color):
		screen.addLineGFC(canvas, self.getNextLineName(), x0, y0 + 1, x1, y1 + 1, color)
		screen.addLineGFC(canvas, self.getNextLineName(), x0 + 1, y0, x1 + 1, y1, color)
		screen.addLineGFC(canvas, self.getNextLineName(), x0, y0, x1, y1, color)

	def getTurnDate(self,turn):
		year = CyGame().getTurnYear(turn)
		if year < 0:
			return CyTranslator().getText("TXT_KEY_TIME_BC", (-year,))
		return CyTranslator().getText("TXT_KEY_TIME_AD", (year,))

	def getNextLineName(self):
		self.nLineCount += 1
		return "DemoLine" + str(self.nLineCount)

	def getNextWidgetName(self):
		szName = "DemoScreenWidget" + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllLines(self):
		screen = self.getScreen()
		while self.nLineCount > -1:
			screen.deleteWidget("DemoLine" + str(self.nLineCount))
			self.nLineCount -= 1

	def deleteAllWidgets(self, iNumPermanentWidgets = 0):
		self.deleteAllLines()
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= iNumPermanentWidgets):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1
		self.nWidgetCount = iNumPermanentWidgets

	def handleInput (self, inputClass):

		screen = self.getScreen()

		szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())
		code = inputClass.getNotifyCode()

		if szWidgetName == self.szExitButtonName and code == NotifyCode.NOTIFY_CLICKED or inputClass.getData() == int(InputTypes.KB_RETURN):
			screen.hideScreen()

		# Slide graph
		if (szWidgetName == self.graphLeftButtonID and code == NotifyCode.NOTIFY_CLICKED):
		    self.slideGraph(- 2 * self.graphZoom / 5)
		    self.drawGraph()
		    
		elif (szWidgetName == self.graphRightButtonID and code == NotifyCode.NOTIFY_CLICKED):
		    self.slideGraph(2 * self.graphZoom / 5)
		    self.drawGraph()

		# Dropdown Box/ ListBox
		if code == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:

			# Debug dropdown
			if (inputClass.getFunctionName() == "InfoScreenDropdownWidget"):
				iIndex = screen.getSelectedPullDownID("InfoScreenDropdownWidget")
				self.iActivePlayer = screen.getPullDownData("InfoScreenDropdownWidget", iIndex)
				self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
				self.iActiveTeam = self.pActivePlayer.getTeam()
				self.pActiveTeam = gc.getTeam(self.iActiveTeam)

				# Determine who this active player knows
				self.aiPlayersMet = []
				self.iNumPlayersMet = 0
				for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					iLoopPlayerTeam = pLoopPlayer.getTeam()
					if (self.pActiveTeam.isHasMet(iLoopPlayerTeam)):
						self.aiPlayersMet.append(iLoopPlayer)
						self.iNumPlayersMet += 1
				# Force recache of all scores
				self.scoreCache = []
				for t in self.RANGE_SCORES:
					self.scoreCache.append(None)
				self.redrawContents()

			iSelected = inputClass.getData()

			if self.iActiveTab == self.iTopCitiesID:

				if szWidgetName == self.szWondersDropdownWidget:
					self.iWonderID = -1

					if iSelected == 0:
						self.szWonderDisplayMode = "World Wonders"
					elif iSelected == 1:
						self.szWonderDisplayMode = "National Wonders"
					elif iSelected == 2:
						self.szWonderDisplayMode = "Projects"

					self.calculateWondersList()
					self.determineListBoxContents()
					if len(self.aaWondersBuilt) + len(self.aaWondersBeingBuilt) > 0:
						self.iWonderID = 0
					self.redrawContents()

				elif szWidgetName == self.szWondersListBox:
					self.reset()
					self.iWonderID = iSelected
					self.deleteAllWidgets(self.iNumWondersPermanentWidgets)
					self.drawWondersList()

			elif self.iActiveTab == self.iGraphID:
				if szWidgetName == self.szGraphDropdownWidget:
					self.iGraphTabID = iSelected
					self.drawGraph()
				elif szWidgetName == self.szTurnsDropdownWidget:
					self.zoomGraph(self.dropDownTurns[iSelected])
					self.drawGraph()

			elif self.iActiveTab == self.iStatsID:
				if szWidgetName == self.szInfoTable:
					self.iInfoTable = iSelected
					self.redrawContents()

		elif code == NotifyCode.NOTIFY_CLICKED:
			if szWidgetName == self.szGraphTabWidget:
				self.iActiveTab = self.iGraphID
				self.reset()
				self.redrawContents()
			elif szWidgetName == self.szDemographicsTabWidget:
				self.iActiveTab = self.iDemographicsID
				self.reset()
				self.redrawContents()
			elif szWidgetName == self.szTopCitiesTabWidget:
				self.iActiveTab = self.iTopCitiesID
				self.reset()
				self.redrawContents()
			elif szWidgetName == self.szStatsTabWidget:
				self.iActiveTab = self.iStatsID
				self.reset()
				self.redrawContents()
		return 0

	def update(self, fDelta):
		return