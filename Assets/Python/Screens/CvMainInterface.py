from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import time

## Ultrapack ##
import WorldTracker
import OrderList
import PlatyOptions

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# END OF TURN BUTTON POSITIONS
######################
iEndOfTurnButtonSize = 32
iEndOfTurnPosY = 147 # distance from bottom

# MINIMAP BUTTON POSITIONS
######################
iMinimapButtonsY_Regular = 160
iMinimapButtonsY_Minimal = 32

# Globe button
iGlobeButtonX = 48
iGlobeButtonY_Regular = 168
iGlobeButtonY_Minimal = 40
iGlobeToggleWidth = 48
iGlobeToggleHeight = 48

# GLOBE LAYER OPTION POSITIONING
######################
iGlobeLayerOptionsY_Regular  = 170# distance from bottom edge
iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
iGlobeLayerOptionHeight = 24

# STACK BAR
#####################
iStackBarHeight = 27

# TOP CENTER TITLE
#####################
iCityCenterRow1Y = 78
iCityCenterRow2Y = 104

g_szTimeText = ""

## UltraPack Initialisation ##
lGreatPeople = []
lUnitCombat = []
iSpecialistY = 500	## PlaceHolder, no point editing

class CvMainInterface:
	def __init__ (self) :
		self.iSelectedSpecialist = 0
		self.iIconSize = 28		## Specialist Icon
		self.iSpecialistColumnWidth = 80
		self.iMaxSpecialistRows = 5
		self.iCityGPBarY = 180		## City Great People Bar = screen.getResolutionY() - 180
		self.iBonusClass = -1		## Resource Filter
		self.iScoreRows = 0		## Score Board
		self.iScoreWidth = 100
		self.bPrereq = False
		self.lAdvisors = [0,0,0,0,0,0]
		self.m_iNumPlotListButtons = 10
		self.iMaxBottomPanelWidth = 400
		self.iTopPanelWidth = 288
		self.iCenterPanelWidth = 258
		self.iBottomPanelWidth = 304
		self.iCityBarX = 140
## UltraPack Initialisation ##

	def numPlotListButtons(self):
		return self.m_iNumPlotListButtons

	def interfaceScreen (self):
		global lGreatPeople
		if len(lGreatPeople) == 0:
			for i in xrange(gc.getNumSpecialistInfos()):
				ItemInfo = gc.getSpecialistInfo(i)
				iGPClass = ItemInfo.getGreatPeopleUnitClass()
				if iGPClass == -1: continue
				if not iGPClass in lGreatPeople:
					lGreatPeople.append(iGPClass)
			for i in xrange(gc.getNumBuildingInfos()):
				ItemInfo = gc.getBuildingInfo(i)
				iGPClass = ItemInfo.getGreatPeopleUnitClass()
				if iGPClass == -1: continue
				if not iGPClass in lGreatPeople:
					lGreatPeople.append(iGPClass)
		if CyGame().isPitbossHost(): return

		# This is the main interface screen, create it as such
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.setForcedRedraw(True)

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		screen.setDimensions(0, 0, xResolution, yResolution)
		
		# Help Text Area
		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		self.iScoreWidth = xResolution/10

	## Bottom Panels ##
		self.iBottomPanelWidth = min(self.iMaxBottomPanelWidth, xResolution *3/10)

		# Bottom Left Panel
		screen.addPanel( "InterfaceLeftBackgroundWidget", u"", u"", True, False, 0, yResolution - 168, self.iBottomPanelWidth, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceLeftBackgroundWidget", "Panel_Game_HudBL_Style" )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		screen.addPanel( "InterfaceCenterBackgroundWidget", u"", u"", True, False, self.iBottomPanelWidth - 8, yResolution - 138, xResolution - (self.iBottomPanelWidth - 8) *2, 138, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceCenterBackgroundWidget", "Panel_Game_HudBC_Style" )
		screen.hide( "InterfaceCenterBackgroundWidget" )

		screen.addPanel( "InterfaceRightBackgroundWidget", u"", u"", True, False, xResolution - self.iBottomPanelWidth, yResolution - 168, self.iBottomPanelWidth, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceRightBackgroundWidget", "Panel_Game_HudBR_Style" )
		screen.hide( "InterfaceRightBackgroundWidget" )

	## City Center Panels ##
		self.iCenterPanelWidth = self.iBottomPanelWidth *5/6

		screen.addPanel( "CityScreenCenterTopWidget", u"", u"", True, False, self.iCenterPanelWidth, 0, xResolution - self.iCenterPanelWidth * 2, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityScreenCenterTopWidget", "Panel_City_Top_Style" )
		screen.hide( "CityScreenCenterTopWidget" )

		screen.addPanel( "InterfaceCenterLeftBackgroundWidget", u"", u"", True, False, 0, 0, self.iCenterPanelWidth, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterLeftBackgroundWidget", "Panel_City_Left_Style" )
		screen.hide( "InterfaceCenterLeftBackgroundWidget" )

		screen.addPanel( "InterfaceCenterRightBackgroundWidget", u"", u"", True, False, xResolution - self.iCenterPanelWidth, 0, self.iCenterPanelWidth, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterRightBackgroundWidget", "Panel_City_Right_Style" )
		screen.hide( "InterfaceCenterRightBackgroundWidget" )
		
		screen.addPanel( "CityScreenAdjustPanel", u"", u"", True, False, 10, 44, self.iCenterPanelWidth - 20, 105, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityScreenAdjustPanel", "Panel_City_Info_Style" )
		screen.hide( "CityScreenAdjustPanel" )

		screen.addPanel( "CityNameBackground", u"", u"", True, False, self.iCenterPanelWidth, 31, xResolution - self.iCenterPanelWidth *2, 38, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityNameBackground", "Panel_City_Title_Style" )
		screen.hide( "CityNameBackground" )
	
		screen.addPanel( "CityScreenTopWidget", u"", u"", True, False, 0, -2, xResolution, 41, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityScreenTopWidget", "Panel_TopBar_Style" )
		screen.hide( "CityScreenTopWidget" )
		
		screen.addPanel( "TopCityPanelLeft", u"", u"", True, False, self.iCenterPanelWidth, 70, xResolution/2 - self.iCenterPanelWidth, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelLeft", "Panel_City_TanTL_Style" )
		screen.hide( "TopCityPanelLeft" )
		
		screen.addPanel( "TopCityPanelRight", u"", u"", True, False, xResolution/2, 70, xResolution/2 - self.iCenterPanelWidth, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelRight", "Panel_City_TanTR_Style" )
		screen.hide( "TopCityPanelRight" )

	## Top Panels ##
		self.iTopPanelWidth = self.iCenterPanelWidth + 28

		screen.addPanel( "InterfaceTopLeft", u"", u"", True, False, 0, -2, self.iTopPanelWidth, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopLeft", "Panel_Game_HudTL_Style" )
		screen.hide( "InterfaceTopLeft" )

		screen.addPanel( "InterfaceTopRight", u"", u"", True, False, xResolution - self.iTopPanelWidth + 2, -2, self.iTopPanelWidth, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopRight", "Panel_Game_HudTR_Style" )
		screen.hide( "InterfaceTopRight" )

		iBtnWidth = 28
		iBtnX = 25

		# Turn log Button
		iX = 0
		screen.setImageButton( "TurnLogButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
		screen.setStyle( "TurnLogButton", "Button_HUDLog_Style" )
		screen.hide( "TurnLogButton" )

## Trackers ##
		iX += iBtnX
		screen.setImageButton("WorldTrackerButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_WORLD_TRACKER").getPath(), iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_PYTHON, 7100, -1)
		screen.hide("WorldTrackerButton")
		iX += iBtnX
		screen.setImageButton("PlatyOptionsButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_PLATY_OPTIONS").getPath(), iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_PYTHON, 7101, -1)
		screen.hide("PlatyOptionsButton")
## Trackers ##
		iX = xResolution - iBtnX - 2
		if not CyGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE):
			screen.setImageButton( "EspionageAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
			screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
			screen.hide( "EspionageAdvisorButton" )
			iX -= iBtnX

		screen.setImageButton( "InfoAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1 )
		screen.setStyle( "InfoAdvisorButton", "Button_HUDAdvisorRecord_Style" )
		screen.hide( "InfoAdvisorButton" )

		iX -= iBtnX
		screen.setImageButton( "VictoryAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "VictoryAdvisorButton", "Button_HUDAdvisorVictory_Style" )
		screen.hide( "VictoryAdvisorButton" )
		
		iX -= iBtnX
		screen.setImageButton( "CorporationAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CORPORATION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CorporationAdvisorButton", "Button_HUDAdvisorCorporation_Style" )
		screen.hide( "CorporationAdvisorButton" )

		iX -= iBtnX
		screen.setImageButton( "ReligiousAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RELIGION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ReligiousAdvisorButton", "Button_HUDAdvisorReligious_Style" )
		screen.hide( "ReligiousAdvisorButton" )
		
		iX -= iBtnX
		screen.setImageButton( "TechAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1 )
		screen.setStyle( "TechAdvisorButton", "Button_HUDAdvisorTechnology_Style" )
		screen.hide( "TechAdvisorButton" )
		
		iX -= iBtnX
		screen.setImageButton( "MilitaryAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "MilitaryAdvisorButton", "Button_HUDAdvisorMilitary_Style" )
		screen.hide( "MilitaryAdvisorButton" )
		
		iX -= iBtnX
		screen.setImageButton( "ForeignAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ForeignAdvisorButton", "Button_HUDAdvisorForeign_Style" )
		screen.hide( "ForeignAdvisorButton" )

		iX -= iBtnX
		screen.setImageButton( "CivicsAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVICS_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CivicsAdvisorButton", "Button_HUDAdvisorCivics_Style" )
		screen.hide( "CivicsAdvisorButton" )

		iX -= iBtnX
		screen.setImageButton( "FinanceAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FINANCIAL_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "FinanceAdvisorButton", "Button_HUDAdvisorFinance_Style" )
		screen.hide( "FinanceAdvisorButton" )

		iX -= iBtnX
		screen.setImageButton( "DomesticAdvisorButton", "", iX, iBtnX, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "DomesticAdvisorButton", "Button_HUDAdvisorDomestic_Style" )
		screen.hide( "DomesticAdvisorButton" )
		
		# Minimap initialization
		screen.setMainInterface(True)
		
		screen.addPanel( "MiniMapPanel", u"", u"", True, False, xResolution - self.iBottomPanelWidth + 90, yResolution - 151, self.iBottomPanelWidth - 86, 151, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "MiniMapPanel", "Panel_Game_HudMap_Style" )
		screen.hide( "MiniMapPanel" )

		screen.initMinimap(xResolution - self.iBottomPanelWidth + 94, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )
		CyMap().updateMinimapColor()

		self.createMinimapButtons()
	
		# Help button (always visible)
		screen.setImageButton( "InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), xResolution - 28, 2, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1 )
		screen.hide( "InterfaceHelpButton" )

		screen.setImageButton( "MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), xResolution - 54, 2, 24, 24, WidgetTypes.WIDGET_MENU_ICON, -1, -1 )
		screen.hide( "MainMenuButton" )

		# Globeview buttons
		self.createGlobeviewButtons( )

		# *********************************************************************************
		# PLOT LIST BUTTONS
		# *********************************************************************************
		self.m_iNumPlotListButtons = (xResolution - (self.iBottomPanelWidth * 2 + 64)) / 34

		for j in xrange(gc.getMAX_PLOT_LIST_ROWS()):
			yRow = (j - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34
			yPixel = yResolution - 169 + yRow - 3
			xPixel = self.iBottomPanelWidth + 8
			xWidth = self.numPlotListButtons() * 34 + 3
			yHeight = 32 + 3
		
			szStringPanel = "PlotListPanel" + str(j)
			screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight + 2, PanelStyles.PANEL_STYLE_EMPTY)

			for i in xrange(self.numPlotListButtons()):
				k = j*self.numPlotListButtons()+i
				
				xOffset = i * 34
				
				szString = "PlotListButton" + str(k)
				screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
				screen.hide( szString )
				szStringHealth = szString + "Health"
				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 27, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
				screen.hide( szStringHealth )
				
				szStringIcon = szString + "Icon"
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
				screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringIcon )
## Fortify Rounds ##
				szStringFortify = szString + "Fortify"
				screen.addStackedBarGFCAt( szStringFortify, szStringPanel, xOffset + 3, 23, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
				screen.hide( szStringFortify )
## Fortify Rounds ##
## Promotion Ready ##
				szStringPromotion = szString + "Promotion"
				screen.setLabelAt(szStringPromotion, szStringPanel, "<font=2>" + CyTranslator().getText("[ICON_SILVER_STAR]", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, xOffset, 20, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.hide( szStringPromotion)
## Promotion Ready ##

		
		screen.setButtonGFC( "PlotListMinus", u"", "", xResolution - self.iBottomPanelWidth - 56, yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "PlotListMinus" )

		screen.setButtonGFC( "PlotListPlus", u"", "", xResolution - self.iBottomPanelWidth - 40, yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "PlotListPlus" )

		# End Turn Text		
		screen.setLabel( "EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - 188, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "EndTurnText", HitTestTypes.HITTEST_NOHIT )

		# Three states for end turn button...
		iX = xResolution - (iEndOfTurnButtonSize/2) - self.iBottomPanelWidth + 8
		screen.setImageButton( "EndTurnButton", "", iX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_END_TURN, -1, -1 )
		screen.setStyle( "EndTurnButton", "Button_HUDEndTurn_Style" )
		screen.setEndTurnState( "EndTurnButton", "Red" )
		screen.hide( "EndTurnButton" )

		# *********************************************************************************
		# SELECTION DATA BUTTONS/STRINGS
		# *********************************************************************************

		iCityBarX = self.iCenterPanelWidth + self.iCityBarX
		screen.addStackedBarGFC( "PopulationBar", iCityBarX, iCityCenterRow1Y-4, xResolution - iCityBarX *2, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColorsAlpha( "PopulationBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), 0.8 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "PopulationBar" )
		
		screen.addStackedBarGFC( "ProductionBar", iCityBarX, iCityCenterRow2Y-4, xResolution - iCityBarX *2, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_PRODUCTION, -1, -1 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType() )
		screen.setStackedBarColorsAlpha( "ProductionBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), 0.8 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ProductionBar" )
		
		screen.addStackedBarGFC( "GreatPeopleBar", xResolution - self.iCenterPanelWidth + 16, yResolution - self.iCityGPBarY, self.iCenterPanelWidth - 32, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPeopleBar" )
## Culture Bar Position ##			
		screen.addStackedBarGFC( "CultureBar", 16 + 24, yResolution - 188, self.iCenterPanelWidth - 32 - 24, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_CULTURE, -1, -1 )
## Culture Bar Position ##	
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CULTURE_STORED") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "CultureBar" )

## Nationality Bar Position ##
		screen.addStackedBarGFC( "NationalityBar", 16 + 24, yResolution - 214, self.iCenterPanelWidth - 32 - 24, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_NATIONALITY, -1, -1 )
## Nationality Bar Position ##
		screen.hide( "NationalityBar" )
		screen.setButtonGFC( "CityScrollMinus", u"", "", self.iCenterPanelWidth + 16, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "CityScrollMinus" )

		screen.setButtonGFC( "CityScrollPlus", u"", "", self.iCenterPanelWidth + 32, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "CityScrollPlus" )
## Unit List Scroll ##
		iBtnWidth = 28
		iX = 10
		iY = yResolution - 166
		screen.setButtonGFC("UnitListScrollMinus", "", "", iX, iY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_PYTHON, -1, 1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
		screen.hide("UnitListScrollMinus")

		iX += iBtnWidth
		screen.setButtonGFC("UnitListScrollPlus", "", "", iX, iY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_PYTHON, -1, 0, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
		screen.hide("UnitListScrollPlus")
## Unit List Scroll ##
		screen.addPanel( "TradeRouteListBackground", u"", u"", True, False, 10, 157, self.iCenterPanelWidth - 20, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TradeRouteListBackground", "Panel_City_Header_Style" )
		screen.hide( "TradeRouteListBackground" )

		screen.addPanel( "BuildingListBackground", u"", u"", True, False, 10, 287, self.iCenterPanelWidth - 20, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "BuildingListBackground", "Panel_City_Header_Style" )
		screen.hide( "BuildingListBackground" )
		# *********************************************************************************
		# UNIT INFO ELEMENTS
		# *********************************************************************************
		
		# This should be a forced redraw screen
		screen.setForcedRedraw( True )
		
		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		return 0

	# Will update the screen (every 250 MS)
	def updateScreen(self):
		
		global g_szTimeText

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		self.m_iNumPlotListButtons = (xResolution - (self.iBottomPanelWidth * 2 + 64)) / 34
		
		# This should recreate the minimap on load games and returns if already exists -JW
		screen.initMinimap(xResolution - self.iBottomPanelWidth + 94, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )

		messageControl = CyMessageControl()
		
		bShow = False

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			if (gc.getGame().isPaused()):
				# Pause overrides other messages
				acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
				screen.setEndTurnState( "EndTurnText", acOutput )
				bShow = True
			elif (messageControl.GetFirstBadConnection() != -1):
				# Waiting on a bad connection to resolve
				if (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1):
					acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					if CyGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS):
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2):
					acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
			else:
				# Flash select messages if no popups are present
				if ( CyInterface().shouldDisplayReturn() ):
					acOutput = localText.getText("SYSTEM_RETURN", ())
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingOthers() ):
					acOutput = localText.getText("SYSTEM_WAITING", ())
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayEndTurn() ):
					acOutput = localText.getText("SYSTEM_END_TURN", ())
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingYou() ):
					acOutput = localText.getText("SYSTEM_WAITING_FOR_YOU", ())
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True

		if bShow:
			screen.showEndTurn( "EndTurnText" )
			if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isCityScreenUp():
				screen.moveItem( "EndTurnText", 0, yResolution - 194, -0.1 )
			else:
				screen.moveItem( "EndTurnText", 0, yResolution - 86, -0.1 )
		else:
			screen.hideEndTurn( "EndTurnText" )

		self.updateEndTurnButton()
		
		if (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			self.updateTimeText()
			sColor = u"<color=255,255,255,0>"
			if PlatyOptions.bCivColors:
				ePlayer = gc.getGame().getActivePlayer()
				sColor = u"<color=%d,%d,%d,%d>" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA())
			screen.setLabel( "TimeText", "Background", sColor + g_szTimeText + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( "TimeText" )
		else:
			screen.hide( "TimeText" )
## Era Text ##
			screen.hide( "EraText" )
## Era Text ##	
		return 0

	def redraw( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		if (CyInterface().isDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT) == True):
			self.updatePercentButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Flag_DIRTY_BIT) == True):
			self.updateFlag()
			CyInterface().setDirty(InterfaceDirtyBits.Flag_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT) == True ):
			self.updateMiscButtons()
			CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT) == True ):
			self.updateInfoPaneStrings()
			CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT) == True ):
			self.updatePlotListButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT) == True ):
			self.updateSelectionButtons()
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT) == True ):
			self.updateResearchButtons()
			CyInterface().setDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT) == True ):
			self.updateCitizenButtons()
			CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT) == True ):
			self.updateGameDataStrings()
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT) == True ):
			self.updateHelpStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT) == True ):
			self.updateCityScreen()
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) == True or CyInterface().checkFlashUpdate() ):
			self.updateScoreStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT) == True ):
			CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
			self.updateGlobeviewButtons()
		return 0

	def updatePercentButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
			szString = "IncreasePercent" + str(iI)
			screen.hide( szString )
			szString = "DecreasePercent" + str(iI)
			screen.hide( szString )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if ( not CyInterface().isCityScreenUp() or ( pHeadSelectedCity.getOwner() == CyGame().getActivePlayer() ) or CyGame().isDebugMode() ):
			iCount = 0

			if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
				for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
					# Intentional offset...
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
										
					if gc.getActivePlayer().isCommerceFlexible(eCommerce):
						szString1 = "IncreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString1, u"", "", 70, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
						screen.show( szString1 )
						szString2 = "DecreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString2, u"", "", 90, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )
						screen.show( szString2 )
						iCount += 1
		return 0

	# Will update the end Turn Button
	def updateEndTurnButton( self ):		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		if CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
			eState = CyInterface().getEndTurnState()
			bShow = False
			if eState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT:
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif eState == EndTurnButtonStates.END_TURN_OVER_DARK:
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif eState == EndTurnButtonStates.END_TURN_GO:
				screen.setEndTurnState( "EndTurnButton", u"Green" )
				bShow = True
			if bShow:
				screen.showEndTurn( "EndTurnButton" )
			else:
				screen.hideEndTurn( "EndTurnButton" )
		else:
			screen.hideEndTurn( "EndTurnButton" )
		return 0

	# Update the miscellaneous buttons
	def updateMiscButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide( "CivilizationFlag" )
		screen.hide( "InterfaceHelpButton" )
		screen.hide( "MainMenuButton" )
		screen.hide( "InterfaceLeftBackgroundWidget" )
		screen.hide( "InterfaceCenterBackgroundWidget" )
		screen.hide( "InterfaceRightBackgroundWidget" )
		screen.hide( "MiniMapPanel" )
		screen.hide( "InterfaceTopLeft" )
		screen.hide( "InterfaceTopCenter" )
		screen.hide( "InterfaceTopRight" )
		screen.hide( "TurnLogButton" )
		screen.hide( "EspionageAdvisorButton" )
		screen.hide( "DomesticAdvisorButton" )
		screen.hide( "ForeignAdvisorButton" )
		screen.hide( "TechAdvisorButton" )
		screen.hide( "CivicsAdvisorButton" )
		screen.hide( "ReligiousAdvisorButton" )
		screen.hide( "CorporationAdvisorButton" )
		screen.hide( "FinanceAdvisorButton" )
		screen.hide( "MilitaryAdvisorButton" )
		screen.hide( "VictoryAdvisorButton" )
		screen.hide( "InfoAdvisorButton" )
## Trackers Start ##
		screen.hide( "WorldTrackerButton" )
		screen.hide( "PlatyOptionsButton" )

		if ( CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.show( "CivilizationFlag" )
			screen.show( "InterfaceHelpButton" )
			screen.show( "MainMenuButton" )
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			pass
		elif ( CyInterface().isCityScreenUp() ):
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )		
		elif ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE):
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
			screen.show( "WorldTrackerButton" )
			screen.show( "PlatyOptionsButton" )
		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START):
			screen.show( "MiniMapPanel" )	
		elif ( CyEngine().isGlobeviewUp() ):
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
			screen.show( "WorldTrackerButton" )
			screen.show( "PlatyOptionsButton" )
		else:
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )
			screen.show( "EspionageAdvisorButton" )
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
			screen.show( "WorldTrackerButton" )
			screen.show( "PlatyOptionsButton" )
## Trackers End ##			
		screen.updateMinimapVisibility()
		return 0

	# Update plot List Buttons
	def updatePlotListButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide( "InterfaceUnitModel" )
		iWidth = 124
		iX = self.iBottomPanelWidth - iWidth - 6
		yResolution = screen.getYResolution()

		if ( CyInterface().shouldDisplayUnitModel() and CyEngine().isGlobeviewUp() == false and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
			if CyInterface().isCitySelection():
				eOrderNodeType = CyInterface().getOrderNodeType(0)
				if eOrderNodeType  == OrderTypes.ORDER_TRAIN:
					screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(0), iX, yResolution - 138, iWidth, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 1, False )
				elif eOrderNodeType == OrderTypes.ORDER_CONSTRUCT:
					screen.addBuildingGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(0), iX, yResolution - 148, iWidth, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.8, False )
				elif eOrderNodeType == OrderTypes.ORDER_CREATE:
					if gc.getProjectInfo(CyInterface().getOrderNodeData1(0)).isSpaceship():
						screen.addSpaceShipWidgetGFC("InterfaceUnitModel", iX, yResolution - 148, iWidth, 132, CyInterface().getOrderNodeData1(0), 0, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
				screen.moveToFront("SelectedCityText")

			elif CyInterface().getHeadSelectedUnit():
				screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), iX, yResolution - 138, iWidth, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
				screen.moveToFront("SelectedUnitText")
			
		pPlot = CyInterface().getSelectionPlot()
## Hidden Promotions ##
		screen.moveToFront("UnitPromotions")
## Hidden Promotions ##		
		screen.hide( "PlotListMinus" )
		screen.hide( "PlotListPlus" )
		
		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
			
			for i in range(self.numPlotListButtons()):
				szString = "PlotListButton" + str(j * self.numPlotListButtons() + i)
				screen.hide( szString )
				
				szStringHealth = szString + "Health"
				screen.hide( szStringHealth )

				szStringIcon = szString + "Icon"
				screen.hide( szStringIcon )
## Fortify Rounds ##
				szStringFortify = szString + "Fortify"
				screen.hide( szStringFortify )
				szStringPromotion = szString + "Promotion"
				screen.hide( szStringPromotion)
## Fortify Rounds ##
		if pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False:

			iVisibleUnits = CyInterface().getNumVisibleUnits()
			iCount = -(CyInterface().getPlotListColumn())
				

			bLeftArrow = False
			bRightArrow = False
			
			if CyInterface().isCityScreenUp():
				iMaxRows = 1
				iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
				iCount += iSkipped
			else:
				iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
				iCount += CyInterface().getPlotListOffset()
				iSkipped = 0

			CyInterface().cacheInterfacePlotUnits(pPlot)
			for i in xrange(CyInterface().getNumCachedInterfacePlotUnits()):
				pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
				if pLoopUnit:

					if iCount == 0 and CyInterface().getPlotListColumn() > 0:
						bLeftArrow = True
					elif ((iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
						bRightArrow = True
						
					if (iCount >= 0 and (iCount <  self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS())):
						szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()
						if pLoopUnit.getTeam() != CyGame().getActiveTeam() or pLoopUnit.isWaiting():
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
							
						elif pLoopUnit.canMove():
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
							if pLoopUnit.hasMoved():
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()

						szString = "PlotListButton" + str(iCount)
						screen.changeImageButton( szString, gc.getPlayer(pLoopUnit.getOwner()).getUnitButton(pLoopUnit.getUnitType()))
						screen.enable(szString, pLoopUnit.getOwner() == CyGame().getActivePlayer())
						screen.setState(szString, pLoopUnit.IsSelected())
						screen.show( szString )
						
						# place the health bar
						bShowHealth = pLoopUnit.canAirAttack() or pLoopUnit.canFight()
						if pLoopUnit.isFighting():
							bShowHealth = False
						else:
							szStringIcon = szString + "Icon"
							screen.changeDDSGFC( szStringIcon, szFileName )
							screen.show( szStringIcon )
						
						if bShowHealth:
							szStringHealth = szString + "Health"
							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
							if pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
							elif pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
							else:
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
							screen.show( szStringHealth )
## Fortify Rounds ##
						if pLoopUnit.isFortifyable():
							szStringFortify = szString + "Fortify"
							screen.setBarPercentage( szStringFortify, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.getFortifyTurns() ) / gc.getDefineINT("MAX_FORTIFY_TURNS") )
							screen.setStackedBarColors(szStringFortify, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CYAN"))
							if pLoopUnit.getFortifyTurns() == gc.getDefineINT("MAX_FORTIFY_TURNS"):
								screen.setStackedBarColors(szStringFortify, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_BLUE"))
							screen.show( szStringFortify )
## Fortify Rounds ##
## Promotion Ready ##
						if pLoopUnit.isPromotionReady():
							szStringPromotion = szString + "Promotion"
							screen.show( szStringPromotion)
## Promotion Ready ##

					iCount += 1

			if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
				screen.enable("PlotListMinus", bLeftArrow)
				screen.show( "PlotListMinus" )
				screen.enable("PlotListPlus", bRightArrow)
				screen.show( "PlotListPlus" )
		return 0
		
	# This will update the flag widget for SP hotseat and dbeugging
	def updateFlag( self ):
		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			iX = screen.getXResolution() - self.iBottomPanelWidth + 16
			iY = screen.getYResolution() - 138
			screen.addFlagWidgetGFC( "CivilizationFlag", iX, iY, 68, 250, CyGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, CyGame().getActivePlayer(), -1)
		
	# Will hide and show the selection buttons and their associated buttons
	def updateSelectionButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
				
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		iX = self.iBottomPanelWidth + 14
		iWidth = xResolution - (iX *2) - 14

		iIconSize = 20
		iHeight = iIconSize + 2
		iY = yResolution - iHeight
		screen.addMultiListControlGFC("UnitCombatFilter", u"", iX, iY, iWidth, iHeight, 2, iIconSize, iIconSize, TableStyles.TABLE_STYLE_STANDARD )
		screen.clearMultiList("UnitCombatFilter")
		screen.hide("UnitCombatFilter")

		iIconSize = 48
		iHeight = 2 * (iIconSize + 2)
		iY -= iHeight
		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iX, iY, iWidth, iHeight, 2, iIconSize, iIconSize, TableStyles.TABLE_STYLE_STANDARD )
		screen.clearMultiList( "BottomButtonContainer" )
		screen.hide( "BottomButtonContainer" )
				
		# All of the hides...	
		self.setMinimapButtonVisibility(False)

		for i in xrange (gc.getNumEmphasizeInfos()):
			screen.hide("Emphasize" + str(i))

		# Hurry button show...
		for i in xrange(gc.getNumHurryInfos()):
			screen.hide("Hurry" + str(i))

		# Conscript Button Show
		screen.hide( "Conscript" )
		screen.hide( "AutomateProduction" )
		screen.hide( "AutomateCitizens" )
## Full Order List ##
		screen.hide("FullOrderList")
		# City Tabs
		for i in xrange(CityTabTypes.NUM_CITYTAB_TYPES):
			szButtonID = "CityTab" + str(i)
			screen.hide(szButtonID)
## Advisor Filter ##
		for i in xrange(6):
			screen.hide("AdvisorFilter" + str(i))
		screen.hide("PrereqFilter")
		global lUnitCombat
		if len(lUnitCombat) == 0:
			for i in xrange(gc.getNumUnitCombatInfos() + 1):
				lUnitCombat.append(0)
## Advisor Filter ##

		if (not CyEngine().isGlobeviewUp() and pHeadSelectedCity):
		
			self.setMinimapButtonVisibility(True)

			if ((pHeadSelectedCity.getOwner() == CyGame().getActivePlayer()) or CyGame().isDebugMode()):
			
				iBtnSX = xResolution - self.iBottomPanelWidth + 20
				
				iBtnX = iBtnSX
				iBtnY = yResolution - 140
				iBtnW = 64
				iBtnH = 30

				# Conscript button
				szText = "<font=1>" + localText.getText("TXT_KEY_DRAFT", ()) + "</font>"
				screen.setButtonGFC( "Conscript", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_CONSCRIPT, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Conscript", "Button_CityT1_Style" )
				screen.hide( "Conscript" )

				iBtnY += iBtnH
				iBtnW = 32
				iBtnH = 28
				
				# Hurry Buttons		
				screen.setButtonGFC( "Hurry0", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry0", "Button_CityC1_Style" )
				screen.hide( "Hurry0" )

				iBtnX += iBtnW

				screen.setButtonGFC( "Hurry1", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry1", "Button_CityC2_Style" )
				screen.hide( "Hurry1" )
			
				iBtnX = iBtnSX
				iBtnY += iBtnH
			
				# Automate Production Button
				screen.addCheckBoxGFC( "AutomateProduction", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateProduction", "Button_CityC3_Style" )

				iBtnX += iBtnW

				# Automate Citizens Button
				screen.addCheckBoxGFC( "AutomateCitizens", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateCitizens", "Button_CityC4_Style" )

				iBtnY += iBtnH
				iBtnX = iBtnSX

				iBtnW	= 22
				iBtnWa	= 20
				iBtnH	= 24
				iBtnHa	= 27
			
				# Set Emphasize buttons
				i = 0
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i += 1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i += 1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				iBtnY += iBtnH
				
				i += 1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i += 1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i += 1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )
				
				screen.setState( "AutomateCitizens", pHeadSelectedCity.isCitizensAutomated() )
				screen.setState( "AutomateProduction", pHeadSelectedCity.isProductionAutomated() )
				
				for i in xrange (gc.getNumEmphasizeInfos()):
					szButtonID = "Emphasize" + str(i)
					screen.show( szButtonID )
					screen.setState( szButtonID, pHeadSelectedCity.AI_isEmphasize(i))

				# Hurry button show...
				for i in xrange(gc.getNumHurryInfos()):
					szButtonID = "Hurry" + str(i)
					screen.show( szButtonID )
					screen.enable( szButtonID, pHeadSelectedCity.canHurry(i, False) )

				# Conscript Button Show
				screen.show( "Conscript" )
				screen.enable( "Conscript", pHeadSelectedCity.canConscript())
## Full Order List ##

				# City Tabs
				iBtnX = xResolution - self.iBottomPanelWidth - 20
				iBtnY = yResolution - 116
				iBtnWidth = 24
				screen.setImageButton("FullOrderList", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_PYTHON, 7002, -1 )
				screen.setStyle("FullOrderList", "Button_HUDAdvisorDomestic_Style" )

				iBtnY += iBtnWidth
				screen.setImageButton("CityTab0", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_UNIT").getPath(), iBtnX - 2, iBtnY, iBtnWidth + 4, iBtnWidth + 4, WidgetTypes.WIDGET_CITY_TAB, 0, -1)
				iBtnY += iBtnWidth + 4
				screen.setImageButton("CityTab1", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_BUILDING").getPath(), iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 1, -1)
				iBtnY += iBtnWidth
				screen.setImageButton("CityTab2", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_WONDER").getPath(), iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 2, -1)
## Built List Filters ##
				lAdvisorIcons = ["[ICON_STRENGTH]", "[ICON_RELIGION]", "[ICON_GOLD]", "[ICON_RESEARCH]", "[ICON_CULTURE]", "[ICON_FOOD]"]
				iBtnWidth = 18
				iX = self.iBottomPanelWidth - 4
				iY = yResolution - iBtnWidth * (len(lAdvisorIcons) + 1) - 4
				sText = CyTranslator().getText("[ICON_STAR]", ())
				if self.bPrereq:
					sText = CyTranslator().getText("[COLOR_RED]", ()) + " X" + "</color>"
				screen.setText("PrereqFilter", "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PYTHON, 7001, -1)
				iY += iBtnWidth
				for i in xrange(len(lAdvisorIcons)):
					sText = CyTranslator().getText(lAdvisorIcons[i], ())
					if self.lAdvisors[i]:
						sText = CyTranslator().getText("[COLOR_RED]", ()) + " X" + "</color>"
					screen.setText("AdvisorFilter" + str(i), "Background", "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX, iY, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PYTHON, 7001, i)
					iY += iBtnWidth
				
				for i in xrange(-1, gc.getNumUnitCombatInfos()):
					sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
					if lUnitCombat[i + 1]:
						sButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath()
					elif i > -1:
						sButton = gc.getUnitCombatInfo(i).getButton()
					screen.appendMultiListButton("UnitCombatFilter", sButton, 0, WidgetTypes.WIDGET_PYTHON, 6781, i, False)
				screen.show("UnitCombatFilter")

				iCount = 0
				iRow = 0
				if PlatyOptions.bBuildList:
					screen.appendMultiListButton("BottomButtonContainer", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_UNIT").getPath(), iRow, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_UNIT").getPath())
					iCount += 1
				for i in xrange (gc.getNumUnitClassInfos()):
					eLoopUnit = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationUnits(i)
					if pHeadSelectedCity.canTrain(eLoopUnit, False, True):
	## Combat Filter ##
						iCombat = gc.getUnitInfo(eLoopUnit).getUnitCombatType()
						if lUnitCombat[iCombat + 1]: continue
	## Combat Filter ##
						szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
	## Prereq Filter ##
						if self.bPrereq and not pHeadSelectedCity.canTrain(eLoopUnit, False, False): continue
	## Prereq Filter ##
						screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
						if not pHeadSelectedCity.canTrain(eLoopUnit, False, False):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, szButton)
						iCount += 1
				if PlatyOptions.bBuildList:
					screen.appendMultiListButton("BottomButtonContainer", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_BUILDING").getPath(), iRow, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_BUILDING").getPath())
					iCount += 1
				else:
					if iCount > 0:
						iRow += 1
						iCount = 0
				for i in xrange (gc.getNumBuildingClassInfos()):
					if not isLimitedWonderClass(i):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
						if pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False):
	## Advisor Filter ##
							Info = gc.getBuildingInfo(eLoopBuilding)
							iAdvisor = Info.getAdvisorType()
							if iAdvisor > -1 and iAdvisor < len(self.lAdvisors):
								if self.lAdvisors[iAdvisor]: continue
	## Advisor Filter ##
	## Prereq Filter ##
							if self.bPrereq and not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False): continue
	## Prereq Filter ##
							screen.appendMultiListButton( "BottomButtonContainer", Info.getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							if not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, Info.getButton() )
							iCount += 1
				if PlatyOptions.bBuildList:
					screen.appendMultiListButton("BottomButtonContainer", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_WONDER").getPath(), iRow, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_WONDER").getPath())
					iCount += 1
				else:
					if iCount > 0:
						iRow += 1
						iCount = 0
				for i in xrange(gc.getNumBuildingClassInfos()):
					if isLimitedWonderClass(i):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
						if pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False):
	## Advisor Filter ##
							Info = gc.getBuildingInfo(eLoopBuilding)
							iAdvisor = Info.getAdvisorType()
							if iAdvisor > -1 and iAdvisor < len(self.lAdvisors):
								if self.lAdvisors[iAdvisor]: continue
	## Advisor Filter ##
	## Prereq Filter ##
							if self.bPrereq and not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False): continue
	## Prereq Filter ##
							screen.appendMultiListButton( "BottomButtonContainer", Info.getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							if not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, Info.getButton() )
							iCount += 1
				if PlatyOptions.bBuildList:
					screen.appendMultiListButton("BottomButtonContainer", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_PROJECT").getPath(), iRow, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_PROJECT").getPath())
					iCount += 1
				else:
					if iCount > 0:
						iRow += 1
						iCount = 0
				for i in xrange(gc.getNumProjectInfos()):
					if (pHeadSelectedCity.canCreate(i, False, True)):
	## Prereq Filter ##
						if self.bPrereq and not pHeadSelectedCity.canCreate(i, False, False): continue
	## Prereq Filter ##
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProjectInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CREATE, i, -1, False )
						if not pHeadSelectedCity.canCreate(i, False, False):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getProjectInfo(i).getButton() )
						iCount += 1
				if PlatyOptions.bBuildList:
					screen.appendMultiListButton("BottomButtonContainer", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_PROCESS").getPath(), iRow, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					screen.disableMultiListButton("BottomButtonContainer", iRow, iCount, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUILD_PROCESS").getPath())
					iCount += 1
				else:
					if iCount > 0:
						iRow += 1
				for i in xrange(gc.getNumProcessInfos()):
					if pHeadSelectedCity.canMaintain(i, False):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProcessInfo(i).getButton(), iRow, WidgetTypes.WIDGET_MAINTAIN, i, -1, False )
				screen.show( "BottomButtonContainer" )
				screen.selectMultiList( "BottomButtonContainer", CyInterface().getCityTabSelectionRow() )
							
		elif (not CyEngine().isGlobeviewUp() and pHeadSelectedUnit and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
			self.setMinimapButtonVisibility(True)
			if CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION:
				if pHeadSelectedUnit.getOwner() == CyGame().getActivePlayer():					
					iCount = 0
					for i in CyInterface().getActionsToShow():
						screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
						if not CyInterface().canHandleAction(i, False):
							screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )
						screen.enableMultiListPulse( "BottomButtonContainer", pHeadSelectedUnit.isActionRecommended(i), 0, iCount )
						iCount += 1

					if CyInterface().canCreateGroup():
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), 0, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1, False )
						iCount += 1

					if CyInterface().canDeleteGroup():
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), 0, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1, False )
						iCount += 1
					screen.show( "BottomButtonContainer" )
		elif (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
			self.setMinimapButtonVisibility(True)
		return 0
		
## Research Buttons ##
	def updateResearchButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide("ResearchPanel")
		screen.hide("ResearchButton")
		if not ( CyInterface().shouldShowResearchButtons() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ): return 0
		xResolution = screen.getXResolution()
		iBarWidth = xResolution - self.iTopPanelWidth * 2
		iX = xResolution/2 - iBarWidth/2 + 4
		iY = 0
		screen.addPanel("ResearchPanel", "", "", True, True, iX - 15, iY - 40, iBarWidth + 32, 30 + 40, PanelStyles.PANEL_STYLE_EMPTY)
		screen.addMultiListControlGFC("ResearchButton", "", iX, iY, iBarWidth, 30, 1, 28, 28, TableStyles.TABLE_STYLE_EMPTY)
		for i in xrange(gc.getNumTechInfos()):
			if (gc.getActivePlayer().canResearch(i, False)):
				sButton = gc.getTechInfo(i).getButton()
				for j in xrange(gc.getNumReligionInfos()):
					if gc.getReligionInfo(j).getTechPrereq() == i:
						if CyGame().isReligionSlotTaken(j): continue
						sButton = gc.getReligionInfo(j).getTechButton()
						if CyGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
							sButton = gc.getReligionInfo(j).getGenericTechButton()
				screen.appendMultiListButton("ResearchButton", sButton, 0, WidgetTypes.WIDGET_RESEARCH, i, -1, false )
## Research Buttons ##		

	def updateCitizenButtons( self ):	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global iSpecialistY
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		screen.hide("AngryCitizen")
		screen.hide("SpecialistTable")			
		screen.hide("IncreaseSpecialist")
		screen.hide("DecreaseSpecialist")
		screen.hide("SelectedSpecialist")
		for i in xrange(gc.getNumSpecialistInfos()):
			screen.hide("FreeSpecialist" + str(i))
			screen.hide("FreeSpecialistCount" + str(i))

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if CyInterface().isCityScreenUp():
			if pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
				iPlayer = pHeadSelectedCity.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				sColor = u"<color=255,255,255,0>"
				if PlatyOptions.bCivColors:
					sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
				lFreeSpecialist = []
				lVisibleSpecialist = []
				for i in xrange(gc.getNumSpecialistInfos()):
					if pHeadSelectedCity.getFreeSpecialistCount(i) > 0:
						lFreeSpecialist.append(i)
					if gc.getSpecialistInfo(i).isVisible():
						lVisibleSpecialist.append(i)
				if not gc.getSpecialistInfo(self.iSelectedSpecialist).isVisible():
					self.iSelectedSpecialist = lVisibleSpecialist[0]
				iSpecialistY = yResolution - self.iCityGPBarY
				iMaxNumber = (self.iCenterPanelWidth - 24) / (self.iIconSize + 6)
				for i in xrange(len(lFreeSpecialist)):
					iResidue = i % iMaxNumber
					if iResidue == 0:
						iSpecialistY -= (self.iIconSize + 2)
					iSpecialist = lFreeSpecialist[i]
					szBuffer = u"<font=2>" + sColor + str(pHeadSelectedCity.getFreeSpecialistCount(iSpecialist)) + u"</color></font>"
					iX = xResolution - self.iCenterPanelWidth + 16  + (self.iIconSize + 6) * iResidue
					screen.setImageButton("FreeSpecialist" + str(i), gc.getSpecialistInfo(iSpecialist).getTexture(), iX, iSpecialistY, self.iIconSize, self.iIconSize, WidgetTypes.WIDGET_FREE_CITIZEN, iSpecialist, 1 )
					screen.setText("FreeSpecialistCount" + str(i), "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, iX , iSpecialistY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
				iSpecialistY -= 32
				sText = u"<font=2>" + sColor + str(pHeadSelectedCity.angryPopulation(0)) + u"</color></font>"
				iTableWidth = self.iCenterPanelWidth - 8
				iNumColumns = iTableWidth / self.iSpecialistColumnWidth
				iWidth = iTableWidth / iNumColumns
				screen.addTableControlGFC("AngryCitizen", 1, xResolution - iWidth, iSpecialistY, iWidth, self.iIconSize + 2, False, False, self.iIconSize, self.iIconSize, TableStyles.TABLE_STYLE_EMPTY)
				screen.setTableColumnHeader("AngryCitizen", 0, "", iWidth)
				screen.appendTableRow("AngryCitizen")
				screen.setTableText("AngryCitizen", 0, 0, sText,ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				if iPlayer == CyGame().getActivePlayer() or CyGame().isDebugMode():
					if (pHeadSelectedCity.isSpecialistValid(self.iSelectedSpecialist, 1) and (pHeadSelectedCity.isCitizensAutomated() or pHeadSelectedCity.getSpecialistCount(self.iSelectedSpecialist) < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
						screen.setButtonGFC("IncreaseSpecialist", u"", "", xResolution - iTableWidth + 4, iSpecialistY, self.iIconSize - 4, self.iIconSize - 4, WidgetTypes.WIDGET_CHANGE_SPECIALIST, self.iSelectedSpecialist, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
					if pHeadSelectedCity.getSpecialistCount(self.iSelectedSpecialist) > 0:
						screen.setButtonGFC("DecreaseSpecialist", u"", "", xResolution - iTableWidth + self.iIconSize, iSpecialistY, self.iIconSize - 4, self.iIconSize - 4, WidgetTypes.WIDGET_CHANGE_SPECIALIST, self.iSelectedSpecialist, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				sText = u"<font=2>" + sColor + gc.getSpecialistInfo(self.iSelectedSpecialist).getDescription() + u"</color></font>"
				screen.setLabel("SelectedSpecialist", "Background", sText, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iTableWidth + self.iIconSize *2 - 4, iSpecialistY + 4, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				
				iNumRows = (len(lVisibleSpecialist) + iNumColumns - 1)/ iNumColumns
				iTableHeight = min(self.iMaxSpecialistRows, iNumRows) * self.iIconSize + 2
				iSpecialistY -= iTableHeight
				screen.addTableControlGFC("SpecialistTable", iNumColumns, xResolution - iTableWidth, iSpecialistY, iTableWidth, iTableHeight, False, False, self.iIconSize, self.iIconSize, TableStyles.TABLE_STYLE_EMPTY)
				for i in xrange(iNumColumns):
					screen.setTableColumnHeader("SpecialistTable", i, "", iWidth)
				for i in xrange(iNumRows):
					screen.appendTableRow("SpecialistTable")

				for i in xrange(len(lVisibleSpecialist)):
					iSpecialist = lVisibleSpecialist[i]
					Info = gc.getSpecialistInfo(iSpecialist)
					sMax = str(pHeadSelectedCity.getMaxSpecialistCount(iSpecialist))
					if pPlayer.isSpecialistValid(iSpecialist) or (sMax == "0" and pHeadSelectedCity.isSpecialistValid(iSpecialist, 1)):
						sMax = "--"
					iCount = pHeadSelectedCity.getSpecialistCount(iSpecialist)
					sText = "<font=2>"
					if iCount > 0:
						sText = "<font=2b>"
					sText += u"%s%d/%s</color></font>" %(sColor, iCount, sMax)
					iColumn = i % iNumColumns
					iRow = i / iNumColumns
					screen.setTableText("SpecialistTable", iColumn, iRow, sText,Info.getButton(), WidgetTypes.WIDGET_CITIZEN, iSpecialist, 1, CvUtil.FONT_LEFT_JUSTIFY)
		return 0
			
	# Will update the game data strings
	def updateGameDataStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "ResearchText" )
		screen.hide( "GoldText" )
		screen.hide( "TimeText" )
		screen.hide( "ResearchBar" )
## Great People Bar ##
		screen.hide( "MainGPText" )
		screen.hide( "MainGPBar" )
## Field of View ##
		screen.hide("IncreaseFOV")
		screen.hide("DecreaseFOV")
		screen.hide("FOVText")
## Era Text ##
		screen.hide( "EraText" )
##
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		ePlayer = gc.getGame().getActivePlayer()
		if pHeadSelectedCity:
			ePlayer = pHeadSelectedCity.getOwner()

		if ( ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS() ):
			return 0

		for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			szString = "PercentText" + str(iI)
			screen.hide(szString)
			szString = "RateText" + str(iI)
			screen.hide(szString)
## Platy Color Text Main ##
		pPlayer = gc.getPlayer(ePlayer)
		sColor = u"<color=255,255,255,0>"
		if PlatyOptions.bCivColors:
			sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):

			self.updateTimeText()
			screen.setLabel( "TimeText", "Background", sColor + g_szTimeText + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( "TimeText" )

			# Percent of commerce
			if pPlayer.isAlive():
				iCount = 0
				for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
					if pPlayer.isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and eCommerce == CommerceTypes.COMMERCE_GOLD):
						szOutText = u"<font=2>%c:%d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), pPlayer.getCommercePercent(eCommerce))
						szString = "PercentText" + str(iI)
						screen.setLabel( szString, "Background", sColor + szOutText + u"</color>", CvUtil.FONT_LEFT_JUSTIFY, 14, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( szString )

						if not CyInterface().isCityScreenUp():
							szOutText = u"<font=2>" + localText.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (pPlayer.getCommerceRate(CommerceTypes(eCommerce)), )) + u"</font>"
							szString = "RateText" + str(iI)
							screen.setLabel( szString, "Background", sColor + szOutText + u"</color>", CvUtil.FONT_LEFT_JUSTIFY, 112, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							screen.show( szString )
						iCount += 1

				szText = CyGameTextMgr().getGoldStr(ePlayer)
				screen.setLabel( "GoldText", "Background", sColor + szText + u"</color>", CvUtil.FONT_LEFT_JUSTIFY, 12, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "GoldText" )

## Research Bar ##
				iBarWidth = xResolution - self.iTopPanelWidth * 2
				if gc.getPlayer(ePlayer).getCurrentResearch() > -1:
					screen.addStackedBarGFC("ResearchBar", xResolution /2 - iBarWidth /2 + 32, 1, iBarWidth - 36, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1)
					screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED"))
					screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"))
					screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
					screen.setStackedBarColors("ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
					if gc.getPlayer(ePlayer).isAnarchy():
						szText = localText.getText("INTERFACE_ANARCHY", (pPlayer.getAnarchyTurns(),))
						screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xResolution /2, 2, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					else:
						szText = "<font=3>" + CyGameTextMgr().getResearchStr(ePlayer) + "</font>"
						screen.addTableControlGFC("ResearchText", 1, xResolution /2 - iBarWidth /2, 2, iBarWidth, iStackBarHeight, False, False, 28, 28, TableStyles.TABLE_STYLE_EMPTY )
						screen.setTableColumnHeader("ResearchText", 0, u"", iBarWidth)
						screen.appendTableRow("ResearchText" )
						screen.setTableText("ResearchText", 0, 0, szText, gc.getTechInfo(gc.getPlayer(ePlayer).getCurrentResearch()).getButton(), WidgetTypes.WIDGET_RESEARCH, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
## Research Bar ##

					researchProgress = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchProgress(gc.getPlayer(ePlayer).getCurrentResearch())
					overflowResearch = (gc.getPlayer(ePlayer).getOverflowResearch() * gc.getPlayer(ePlayer).calculateResearchModifier(gc.getPlayer(ePlayer).getCurrentResearch()))/100
					researchCost = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchCost(gc.getPlayer(ePlayer).getCurrentResearch())
					researchRate = gc.getPlayer(ePlayer).calculateResearchRate(-1)
					
					screen.setBarPercentage("ResearchBar", InfoBarTypes.INFOBAR_STORED, float(researchProgress + overflowResearch) / researchCost )
					screen.setBarPercentage("ResearchBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if (researchCost >  researchProgress + overflowResearch):
						screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_RATE, float(researchRate) / (researchCost - researchProgress - overflowResearch))
## Era Text ##
				szText = gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentEra()).getDescription()
				screen.setLabel( "EraText", "Background", sColor + szText + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, self.iTopPanelWidth - 18, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "EraText" )
## Field of View ##
				if not CyInterface().isCityScreenUp():
					screen.setButtonGFC("IncreaseFOV", u"", "", xResolution - 58, 58, 20, 20, WidgetTypes.WIDGET_PYTHON, 7000, 1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
					screen.addDDSGFC("FOVText", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), xResolution - 38, 59, 18, 18, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.setButtonGFC("DecreaseFOV", u"", "", xResolution - 20, 58, 20, 20, WidgetTypes.WIDGET_PYTHON, 7000, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)				
## Great People Bar ##
					if PlatyOptions.bGreatPeopleBar:
						iMinTurns = 99999
						iCityID = -1
						(loopCity, iter) = pPlayer.firstCity(False)
						while(loopCity):
							iRate = loopCity.getGreatPeopleRate()
							if iRate > 0:
								iTurns = (pPlayer.greatPeopleThreshold(false) - loopCity.getGreatPeopleProgress() + iRate - 1) / iRate
								if iTurns < iMinTurns:
									iMinTurns = iTurns
									iCityID = loopCity.getID()
							(loopCity, iter) = pPlayer.nextCity(iter, False)
						if iCityID > -1:
							pCity = pPlayer.getCity(iCityID)
							screen.addStackedBarGFC( "MainGPBar", xResolution /2 - iBarWidth /2 + 32, 3 + 24, iBarWidth - 36, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_PYTHON, 7200 + ePlayer, iCityID)
							screen.setStackedBarColors( "MainGPBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
							screen.setStackedBarColors( "MainGPBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
							screen.setStackedBarColors( "MainGPBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
							screen.setStackedBarColors( "MainGPBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )

							fGreatProgress = float(pCity.getGreatPeopleProgress()) / pPlayer.greatPeopleThreshold(false)
							screen.setBarPercentage( "MainGPBar", InfoBarTypes.INFOBAR_STORED, fGreatProgress)
							screen.setBarPercentage( "MainGPBar", InfoBarTypes.INFOBAR_RATE, 0.0)
							if fGreatProgress < 1:
								screen.setBarPercentage( "MainGPBar", InfoBarTypes.INFOBAR_RATE, ( float(pCity.getGreatPeopleRate()) / (pPlayer.greatPeopleThreshold(false) - pCity.getGreatPeopleProgress())))
							
							iGreatUnit = -1
							iMaxProgress = 0
							for i in xrange(len(lGreatPeople)):
								iUnitClass = lGreatPeople[i]
								iUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)
								if iUnit == -1: continue
								iProgress = pCity.getGreatPeopleUnitProgress(iUnit)
								if iProgress > iMaxProgress:
									iMaxProgress = iProgress
									iGreatUnit = iUnit
							screen.addTableControlGFC( "MainGPText", 1, xResolution /2 - iBarWidth /2, 4 + 24, iBarWidth, iStackBarHeight, False, False, 28, 28, TableStyles.TABLE_STYLE_EMPTY )
							screen.setTableColumnHeader( "MainGPText", 0, u"", iBarWidth)
							screen.appendTableRow( "MainGPText" )
							sUnit = ""
							sButton = ""
							if iGreatUnit > -1:
								sUnit = gc.getUnitInfo(iGreatUnit).getDescription()
								sButton = gc.getUnitInfo(iGreatUnit).getButton()
							sText = u"<font=3>%s: %s (%d)</font>" %(pCity.getName(), sUnit, iMinTurns)
							screen.setTableText( "MainGPText", 0, 0, sText, sButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
							screen.setHitTest( "MainGPText", HitTestTypes.HITTEST_NOHIT )
## Great People Bar ##					
		return 0
		
	def updateTimeText( self ):
		global g_szTimeText
		g_szTimeText = localText.getText("TXT_KEY_TIME_TURN", (CyGame().getGameTurn(), )) + u" - " + unicode(CyGameTextMgr().getInterfaceTimeStr(CyGame().getActivePlayer()))
		if CyUserProfile().isClockOn():
			g_szTimeText = getClockText() + u" - " + g_szTimeText
		
	# Will update the selection Data Strings
	def updateCityScreen( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.hide( "PopulationBar" )
		screen.hide( "ProductionBar" )
		screen.hide( "GreatPeopleBar" )
		screen.hide( "CultureBar" )
		screen.hide( "MaintenanceText" )
		screen.hide( "MaintenanceAmountText" )
		screen.hide( "NationalityText" )
		screen.hide( "NationalityBar" )
		screen.hide( "DefenseText" )
		screen.hide( "CityScrollMinus" )
		screen.hide( "CityScrollPlus" )
		screen.hide( "CityNameText" )
		screen.hide( "PopulationText" )
		screen.hide( "PopulationInputText" )
		screen.hide( "HealthText" )
		screen.hide( "ProductionText" )
		screen.hide( "ProductionInputText" )
		screen.hide( "HappinessText" )
		screen.hide( "CultureText" )
		screen.hide( "GreatPeopleText" )
			
		for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			szName = "CityPercentText" + str(i)
			screen.hide( szName )

		screen.hide( "TradeRouteTable" )
		screen.hide( "BuildingListTable" )
		screen.hide( "BuildingListBackground" )
		screen.hide( "TradeRouteListBackground" )
		screen.hide( "BuildingListLabel" )
		screen.hide( "TradeRouteListLabel" )
## Bonus Table ##
		screen.hide("BonusTable")
		screen.hide("ResourceFilter")
## Religions and Corporations ##
		screen.hide("ReligionsCorps")
## Camera City Zoom In Distance ##
		screen.hide("CityFOVPlus")
		screen.hide("CityFOVMinus")
		screen.hide("CityFOVText")

		if CyInterface().isCityScreenUp():
			if pHeadSelectedCity:
				sColor = u"<color=255,255,255,0>"	
				if PlatyOptions.bCivColors:
					sColor = u"<color=%d,%d,%d,%d>" %(gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorR(), gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorG(), gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorB(), gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorA())
				screen.show( "CityScreenCenterTopWidget" )
				screen.show( "InterfaceCenterLeftBackgroundWidget" )
				screen.show( "CityScreenTopWidget" )
				screen.show( "CityNameBackground" )
				screen.show( "TopCityPanelLeft" )
				screen.show( "TopCityPanelRight" )
				screen.show( "CityScreenAdjustPanel" )
				screen.show( "InterfaceCenterRightBackgroundWidget" )
				
				if pHeadSelectedCity.getTeam() == CyGame().getActiveTeam():
					if gc.getActivePlayer().getNumCities() > 1:
						screen.show( "CityScrollMinus" )
						screen.show( "CityScrollPlus" )
				
				screen.setHelpTextArea( 390, FontTypes.SMALL_FONT, 0, 0, -2.2, True, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )
## Camera City Zoom In Distance ##
				screen.setButtonGFC("CityFOVPlus", u"", "", xResolution -  self.iCenterPanelWidth - 62, 138, 20, 20, WidgetTypes.WIDGET_PYTHON, 6999, 10, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
				screen.addDDSGFC("CityFOVText", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), xResolution -  self.iCenterPanelWidth - 40, 139, 18, 18, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setButtonGFC("CityFOVMinus", u"", "", xResolution - self.iCenterPanelWidth - 22, 138, 20, 20, WidgetTypes.WIDGET_PYTHON, 6999, -10, ButtonStyles.BUTTON_STYLE_CITY_PLUS)				
## Camera City Zoom In Distance ##
## Defense Text ##
				szBuffer = ""
				iDefenseModifier = pHeadSelectedCity.getDefenseModifier(False)
				if iDefenseModifier != 0:
					szBuffer = localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))
					if (pHeadSelectedCity.getDefenseDamage() > 0):
						szBuffer += u" (%d%%)" %( ( ( gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage() ) * 100 ) / gc.getMAX_CITY_DEFENSE_DAMAGE() )
					screen.setLabel( "DefenseText", "Background", "<font=3>" + sColor + szBuffer + u"</color>" + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, xResolution - self.iCenterPanelWidth - 12, 38, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1 )
				iDefenseX = xResolution - 270 - CyInterface().determineWidth(szBuffer)
## Defense Text ##
## City Name ##
				szBuffer = sColor
				if pHeadSelectedCity.isCapital():
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
				elif pHeadSelectedCity.isGovernmentCenter():
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))

				if pHeadSelectedCity.isPower():
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))
					
				szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())

				if pHeadSelectedCity.isOccupation():
					szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())
				szBuffer +=  "</font></color>"
				sTemp = "<font=4>" + szBuffer
				iWidth = CyInterface().determineWidth(sTemp)
				if iWidth/2 > iDefenseX - xResolution/2:
					if iWidth > iDefenseX - self.iCenterPanelWidth - 62:
						sTemp = "<font=3>" + szBuffer
						iWidth = CyInterface().determineWidth(sTemp)
						if iWidth/2 > iDefenseX - xResolution/2:
							screen.setText("CityNameText", "Background", sTemp, CvUtil.FONT_RIGHT_JUSTIFY, iDefenseX, 36, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
						else:
							screen.setText("CityNameText", "Background", sTemp, CvUtil.FONT_CENTER_JUSTIFY, xResolution/2, 36, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
					else:
						screen.setText("CityNameText", "Background", sTemp, CvUtil.FONT_RIGHT_JUSTIFY, iDefenseX, 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
				else:
					screen.setText("CityNameText", "Background", sTemp, CvUtil.FONT_CENTER_JUSTIFY, xResolution/2, 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
				screen.setStyle( "CityNameText", "Button_Stone_Style" )
## City Name ##
				iFoodDifference = pHeadSelectedCity.foodDifference(True)
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True, True)
				iProductionDiffJustFood = (pHeadSelectedCity.getCurrentProductionDifference(False, True) - iProductionDiffNoFood)

				if iFoodDifference != 0 or not pHeadSelectedCity.isFoodProduction():
					if iFoodDifference > 0:
						szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))	
					elif iFoodDifference < 0:
						szBuffer = localText.getText("INTERFACE_CITY_STARVING", ())	
					else:
						szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())	

					screen.setLabel( "PopulationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow1Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "PopulationText", HitTestTypes.HITTEST_NOHIT )

				if not pHeadSelectedCity.isDisorder() and not pHeadSelectedCity.isFoodProduction():		
					szBuffer = u"%d%c - %d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD), gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), pHeadSelectedCity.foodConsumption(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
					screen.setLabel( "PopulationInputText", "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, self.iCenterPanelWidth + self.iCityBarX - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					
				else:
					szBuffer = u"%d%c" %(iFoodDifference, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
					screen.setLabel( "PopulationInputText", "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, self.iCenterPanelWidth + self.iCityBarX - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				if iFoodDifference < 0:
					iDeltaFood = 0
					if pHeadSelectedCity.getFood() + iFoodDifference > 0:
						iDeltaFood = pHeadSelectedCity.getFood() + iFoodDifference
					iExtraFood = pHeadSelectedCity.getFood()
					if -iFoodDifference < pHeadSelectedCity.getFood():
						iExtraFood = -iFoodDifference
					iFirst = float(iDeltaFood) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(iDeltaFood) / pHeadSelectedCity.growthThreshold() )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)
					if pHeadSelectedCity.growthThreshold() > iDeltaFood:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iExtraFood) / (pHeadSelectedCity.growthThreshold() - iDeltaFood) )
				else:
					iFirst = float(pHeadSelectedCity.getFood()) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(pHeadSelectedCity.getFood()) / pHeadSelectedCity.growthThreshold() )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if pHeadSelectedCity.growthThreshold() >  pHeadSelectedCity.getFood():
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, float(iFoodDifference) / (pHeadSelectedCity.growthThreshold() - pHeadSelectedCity.getFood()) )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0 )
				screen.show( "PopulationBar" )

				if pHeadSelectedCity.getOrderQueueLength() > 0:
					if pHeadSelectedCity.isProductionProcess():
						szBuffer = pHeadSelectedCity.getProductionName()
					else:
						szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))

					screen.setLabel( "ProductionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow2Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "ProductionText", HitTestTypes.HITTEST_NOHIT )
				
				if pHeadSelectedCity.isProductionProcess():
					szBuffer = u"%d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				elif pHeadSelectedCity.isFoodProduction() and iProductionDiffJustFood > 0:
					szBuffer = u"%d%c + %d%c" %(iProductionDiffJustFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				else:
					szBuffer = u"%d%c" %(iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				screen.setLabel( "ProductionInputText", "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, self.iCenterPanelWidth + self.iCityBarX - 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1 )
## Health Text ##
				szBuffer = ""
				if pHeadSelectedCity.goodHealth() > 0:
					szBuffer += u"%d%c" %(pHeadSelectedCity.goodHealth(), CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR))
				if pHeadSelectedCity.badHealth(False) > 0:
					szBuffer += u"%d%c" %(pHeadSelectedCity.badHealth(False), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))
				if pHeadSelectedCity.healthRate(False, 0) < 0:
					szBuffer += u"%d%c" %(- pHeadSelectedCity.healthRate(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))		
				screen.setLabel( "HealthText", "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_LEFT_JUSTIFY, xResolution - self.iCenterPanelWidth - self.iCityBarX + 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HEALTH, -1, -1 )
## Health Text ##
## Happiness Text ##
				if pHeadSelectedCity.isDisorder():
					szBuffer = u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
				else:
					szBuffer = ""
					if pHeadSelectedCity.happyLevel() > 0:
						szBuffer += u"%d%c" %(pHeadSelectedCity.happyLevel(), CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
					if pHeadSelectedCity.unhappyLevel(0) > 0:
						szBuffer += u"%d%c" %(pHeadSelectedCity.unhappyLevel(0), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
					if pHeadSelectedCity.angryPopulation(0) != 0:
						szBuffer += u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))		
				screen.setLabel( "HappinessText", "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_LEFT_JUSTIFY, xResolution - self.iCenterPanelWidth - self.iCityBarX + 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HAPPINESS, -1, -1 )
## Happiness Text ##
				if not pHeadSelectedCity.isProductionProcess():
					iNeeded = pHeadSelectedCity.getProductionNeeded()
					iStored = pHeadSelectedCity.getProduction()
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_STORED, float(iStored) / iNeeded )
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if iNeeded > iStored:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, float(iProductionDiffNoFood) / (iNeeded - iStored) )
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)
					if iNeeded > iStored + iProductionDiffNoFood:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iProductionDiffJustFood) / (iNeeded - iStored - iProductionDiffNoFood) )
					screen.show( "ProductionBar" )

				iCount = 0
				for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
					if gc.getPlayer(pHeadSelectedCity.getOwner()).isCommerceFlexible(eCommerce) or eCommerce == CommerceTypes.COMMERCE_GOLD:
						szBuffer = u"%d.%02d %c" %(pHeadSelectedCity.getCommerceRate(eCommerce), pHeadSelectedCity.getCommerceRateTimes100(eCommerce)%100, gc.getCommerceInfo(eCommerce).getChar())
						iHappiness = pHeadSelectedCity.getCommerceHappinessByType(eCommerce)
						if iHappiness != 0:
							if iHappiness > 0:
								szBuffer += u", %d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
							else:
								szBuffer += u", %d%c" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
						szName = "CityPercentText" + str(iCount)
						screen.setLabel( szName, "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, self.iCenterPanelWidth - 15, 45 + (19 * iCount) + 4, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_COMMERCE_MOD_HELP, eCommerce, -1 )
						screen.show( szName )
						iCount += 1

## Trade Routes ##
				screen.show( "TradeRouteListBackground" )
				iTableWidth = self.iCenterPanelWidth - 20
				screen.addTableControlGFC( "TradeRouteTable", 2, 10, 187, self.iCenterPanelWidth - 20, 4 * 24, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "TradeRouteTable", "Table_City_Style" )
				screen.setTableColumnHeader( "TradeRouteTable", 0, u"", iTableWidth/2)
				screen.setTableColumnHeader( "TradeRouteTable", 1, u"", iTableWidth/2 - 8)

				sText = u"%d%c" %(pHeadSelectedCity.getTradeRoutes(), CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
				for j in xrange( YieldTypes.NUM_YIELD_TYPES ):
					iTradeProfit = pHeadSelectedCity.getTradeYield(j)
					if iTradeProfit != 0:
						sText += u"%d%c" %(iTradeProfit, gc.getYieldInfo(j).getChar() )
				sText += CyTranslator().getText("TXT_KEY_TRADE_ROUTE_LABEL", (pHeadSelectedCity.plot().getLatitude(),))
				screen.setLabel( "TradeRouteListLabel", "Background", sColor + sText + u"</color>", CvUtil.FONT_CENTER_JUSTIFY, self.iCenterPanelWidth/2, 165, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

				for i in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
					pLoopCity = pHeadSelectedCity.getTradeCity(i)
					if pLoopCity and pLoopCity.getOwner() > -1:
						player = gc.getPlayer(pLoopCity.getOwner())
						szLeftBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), pLoopCity.getName() )
						szRightBuffer = u""

						for j in xrange( YieldTypes.NUM_YIELD_TYPES ):
							iTradeProfit = pHeadSelectedCity.calculateTradeYield(j, pHeadSelectedCity.calculateTradeProfit(pLoopCity))
							if iTradeProfit != 0:
								szRightBuffer += u"%d%c" %(iTradeProfit, gc.getYieldInfo(j).getChar() )
						szRightBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), szRightBuffer )
						iRow = screen.appendTableRow( "TradeRouteTable" )
						iCiv = player.getCivilizationType()
						screen.setTableText( "TradeRouteTable", 0, iRow, "<font=1>" + szLeftBuffer + "</font>", gc.getCivilizationInfo(iCiv).getButton(), WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "TradeRouteTable", 1, iRow, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
## Trade Routes ##
## Building List ##
				screen.show( "BuildingListBackground" )
				screen.addTableControlGFC( "BuildingListTable", 2, 10, 317, iTableWidth, (yResolution - 541)/24*24, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "BuildingListTable", "Table_City_Style" )
				screen.setTableColumnHeader( "BuildingListTable", 0, "", iTableWidth/2)
				screen.setTableColumnHeader( "BuildingListTable", 1, "", iTableWidth/2 - 8)

				sText = localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ())
				sText += " (" + str(pHeadSelectedCity.getNumNationalWonders() + pHeadSelectedCity.getNumTeamWonders()) + CyTranslator().getText("[ICON_SILVER_STAR]", ()) + str(pHeadSelectedCity.getNumWorldWonders()) + CyTranslator().getText("[ICON_STAR]", ()) + ")"
				screen.setLabel( "BuildingListLabel", "Background", sColor + sText + u"</color>", CvUtil.FONT_CENTER_JUSTIFY, self.iCenterPanelWidth/2, 295, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				for i in xrange( gc.getNumBuildingInfos() ):
	## Graphical Only ##
					BuildingInfo = gc.getBuildingInfo(i)
					if BuildingInfo.isGraphicalOnly(): continue
	## Graphical Only ##
					iNumBuilding = pHeadSelectedCity.getNumBuilding(i)
					if iNumBuilding > 0:
						szLeftBuffer = BuildingInfo.getDescription()
						szRightBuffer = ""
							
						if pHeadSelectedCity.getNumActiveBuilding(i) > 0:
							iTradeRoute = BuildingInfo.getTradeRoutes() * iNumBuilding
							if iTradeRoute != 0:
								szRightBuffer +=  u"%d%c" %(iTradeRoute, CyGame().getSymbolID(FontSymbols.TRADE_CHAR) )
							iHealth = pHeadSelectedCity.getBuildingHealth(i)
							if iHealth != 0:										
								if iHealth > 0:
									szRightBuffer +=  u"%d%c" %( iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) )
								else:
									szRightBuffer += u"%d%c" %( -(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )

							iHappiness = pHeadSelectedCity.getBuildingHappiness(i)
							if iHappiness != 0:									
								if iHappiness > 0:
									szRightBuffer += u"%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
								else:
									szRightBuffer += u"%d%c" %( -(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
							for j in xrange( YieldTypes.NUM_YIELD_TYPES):
								iYield = iNumBuilding * (BuildingInfo.getYieldChange(j) + pHeadSelectedCity.getBuildingYieldChange(BuildingInfo.getBuildingClassType(), j))
								if iYield != 0:										
									szRightBuffer += u"%d%c" %(iYield, gc.getYieldInfo(j).getChar() )
								iYieldModifier = BuildingInfo.getYieldModifier(j) * iNumBuilding
								if iYieldModifier != 0:
									szRightBuffer += str(iYieldModifier) + "%" + u"%c" %(gc.getYieldInfo(j).getChar())
						for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getBuildingCommerceByBuilding(j, i)
							if iCommerce != 0:										
								szRightBuffer += u"%d%c" %(iCommerce, gc.getCommerceInfo(j).getChar() )
							if pHeadSelectedCity.getNumActiveBuilding(i) > 0:
								iCommerceModifier = BuildingInfo.getCommerceModifier(j) * iNumBuilding
								if iCommerceModifier != 0:
									szRightBuffer += str(iCommerceModifier) + "%" + u"%c" %(gc.getCommerceInfo(j).getChar())
	## Building GP Rate ##
						if pHeadSelectedCity.getNumActiveBuilding(i) > 0:
							iGPRate = gc.getBuildingInfo(i).getGreatPeopleRateChange() * iNumBuilding
							if iGPRate != 0:
								szRightBuffer += str(iGPRate) + CyTranslator().getText("[ICON_GREATPEOPLE]", ())
						iRow = screen.appendTableRow( "BuildingListTable" )
						screen.setTableText( "BuildingListTable", 0, iRow, "<font=1>" + sColor + szLeftBuffer + "</color></font>", gc.getBuildingInfo(i).getButton(), WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "BuildingListTable", 1, iRow, "<font=1>" + sColor + szRightBuffer + "</color></font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
## Building List ##
## Bonus Table ##
				iY = 90
	## Resource Filter ##
				iResourceWidth = self.iCenterPanelWidth - 8
				screen.addDropDownBoxGFC("ResourceFilter", xResolution - iResourceWidth, iY, 120, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("ResourceFilter", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_EVERYTHING",()), 0, 0, 0 == self.iBonusClass)
				screen.addPullDownString("ResourceFilter", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL",()), 1, 1, 1 == self.iBonusClass)
				screen.addPullDownString("ResourceFilter", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_FOOD",()), 2, 2, 2 == self.iBonusClass)
				screen.addPullDownString("ResourceFilter", CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_LUXURIES",()), 3, 3, 3 == self.iBonusClass)
	## Resource Filter ##
				iY += 30
				iHeight = iSpecialistY - iY
				iHeight = (iHeight - 2) /24 * 24 - 1
				screen.addTableControlGFC( "BonusTable", 4, xResolution - iResourceWidth, iY, iResourceWidth, iHeight, True, True, 24, 24, TableStyles.TABLE_STYLE_CITY )				
				screen.setTableColumnHeader("BonusTable", 0, "", 30)
				screen.setTableColumnHeader("BonusTable", 1, "<font=2>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ()) + "</font>", iResourceWidth - 90 - 12)
				screen.setTableColumnHeader("BonusTable", 2, "<font=2>" + CyTranslator().getText("[ICON_HAPPY]" + "</font>", ()), 30)
				screen.setTableColumnHeader("BonusTable", 3, "<font=2>" + CyTranslator().getText("[ICON_HEALTHY]" + "</font>", ()), 30)
				screen.enableSort("BonusTable")

				for iBonus in xrange(gc.getNumBonusInfos()):
					if pHeadSelectedCity.hasBonus(iBonus):
						Info = gc.getBonusInfo(iBonus)
						iHealth = pHeadSelectedCity.getBonusHealth(iBonus)
						iHappiness = pHeadSelectedCity.getBonusHappiness(iBonus)
						if self.iBonusClass == 1:
							if iHealth > 0 or iHappiness > 0: continue
						elif self.iBonusClass == 2:
							if iHealth < 1: continue
						elif self.iBonusClass == 3:
							if iHappiness < 1: continue
						iNumBonus = pHeadSelectedCity.getNumBonuses(iBonus)
						iRow = screen.appendTableRow("BonusTable")
						screen.setTableInt("BonusTable", 0, iRow, sColor + str(iNumBonus) + u"</color>","", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
						screen.setTableText("BonusTable", 1, iRow, sColor + Info.getDescription() + "</color>",Info.getButton(), WidgetTypes.WIDGET_PYTHON, 7878, iBonus, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableInt("BonusTable", 2, iRow, sColor + str(iHappiness) + u"</color>","", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
						screen.setTableInt("BonusTable", 3, iRow, sColor + str(iHealth) + u"</color>","", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
## Bonus Table ##		
				iMaintenance = pHeadSelectedCity.getMaintenanceTimes100()
				szBuffer = localText.getText("INTERFACE_CITY_MAINTENANCE", ())
				screen.setLabel( "MaintenanceText", "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_LEFT_JUSTIFY, 15, 126, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				szBuffer = u"-%d.%02d %c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
				screen.setLabel( "MaintenanceAmountText", "Background", sColor + szBuffer + u"</color>", CvUtil.FONT_RIGHT_JUSTIFY, self.iCenterPanelWidth - 15, 125, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
## Religions and Corporations ##
				nColumns = min(10, max(1, gc.getNumReligionInfos(), gc.getNumCorporationInfos()))
				screen.addTableControlGFC("ReligionsCorps", nColumns, xResolution - iResourceWidth , 42, iResourceWidth, 50, False, False, 0, 0, TableStyles.TABLE_STYLE_EMPTY)
				for i in xrange(nColumns):				
					screen.setTableColumnHeader("ReligionsCorps", i, "", iResourceWidth/nColumns)

				iCount = 0
				for i in xrange(gc.getNumReligionInfos()):
					if pHeadSelectedCity.isHasReligion(i):
						iColumn = iCount % nColumns
						if iColumn == 0:
							iRow = screen.appendTableRow("ReligionsCorps")
						sText = u"%c" %(gc.getReligionInfo(i).getChar())
						if pHeadSelectedCity.isHolyCityByType(i):
							sText = u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
						screen.setTableText("ReligionsCorps", iColumn, iRow, "<font=4>" + sText + "</font>","", WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1, CvUtil.FONT_CENTER_JUSTIFY)
						iCount += 1

				iCount = 0
				for i in xrange(gc.getNumCorporationInfos()):
					if pHeadSelectedCity.isHasCorporation(i):
						iColumn = iCount % nColumns
						if iColumn == 0:
							iRow = screen.appendTableRow("ReligionsCorps")
						sText = u"%c" %(gc.getCorporationInfo(i).getChar())
						if pHeadSelectedCity.isHeadquartersByType(i):
							sText = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
						screen.setTableText("ReligionsCorps", iColumn, iRow, "<font=4>" + sText + "</font>","", WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1, CvUtil.FONT_CENTER_JUSTIFY)
						iCount += 1
## Religions and Corporations ##
## Great People Bar ##
				iRate = pHeadSelectedCity.getGreatPeopleRate()
				iCurrent = pHeadSelectedCity.getGreatPeopleProgress()
				if iCurrent > 0 or iRate >0:
					iThreshold = gc.getPlayer(pHeadSelectedCity.getOwner()).greatPeopleThreshold(false)
					szBuffer = CyTranslator().getText("[ICON_GREATPEOPLE]: ", ()) + str(iCurrent) + CyTranslator().getText("[COLOR_POSITIVE_TEXT] +", ())+ str(iRate) + CyTranslator().getText("[COLOR_REVERT] / ", ()) + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + str(iThreshold) + CyTranslator().getText("[COLOR_REVERT]", ())
					screen.setLabel( "GreatPeopleText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution - self.iCenterPanelWidth/2, yResolution - self.iCityGPBarY + 4, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
					screen.setHitTest( "GreatPeopleText", HitTestTypes.HITTEST_NOHIT )
					screen.setBarPercentage("GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, float(iCurrent) / iThreshold)
					screen.setBarPercentage("GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, 0.0)
					if iCurrent < iThreshold:
						screen.setBarPercentage("GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) )
					screen.show( "GreatPeopleBar" )
## Great People Bar ##
## Nationality Bar ##
				iBarWidth = self.iCenterPanelWidth - 24
				szBuffer = u"%d%% %s" %(pHeadSelectedCity.plot().calculateCulturePercent(pHeadSelectedCity.getOwner()), gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationAdjective(0) )
				screen.addTableControlGFC( "NationalityText", 1, 12, yResolution - 213, iBarWidth, iStackBarHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY )
				screen.setTableColumnHeader( "NationalityText", 0, u"", iBarWidth)
				screen.appendTableRow( "NationalityText" )
				screen.setTableText( "NationalityText", 0, 0, szBuffer, gc.getCivilizationInfo(gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationType()).getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setHitTest( "NationalityText", HitTestTypes.HITTEST_NOHIT )
				iRemainder = 100
				iWhichBar = 0
				for h in xrange( gc.getMAX_PLAYERS() ):
					if gc.getPlayer(h).isAlive():
						iPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
						if iPercent > 0:
							screen.setStackedBarColorsRGB( "NationalityBar", iWhichBar, gc.getPlayer(h).getPlayerTextColorR(), gc.getPlayer(h).getPlayerTextColorG(), gc.getPlayer(h).getPlayerTextColorB(), gc.getPlayer(h).getPlayerTextColorA() )
							if iRemainder <= 0:
								screen.setBarPercentage( "NationalityBar", iWhichBar, 0.0 )
							else:
								screen.setBarPercentage( "NationalityBar", iWhichBar, float(iPercent) / iRemainder)
							iRemainder -= iPercent
							iWhichBar += 1
				screen.show( "NationalityBar" )
## Nationality Bar ##
## Culture Bar ##
				if pHeadSelectedCity.getCultureLevel != CultureLevelTypes.NO_CULTURELEVEL:
					iRate = pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)
					szBuffer = "<font=1>" + gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getDescription() + ": "
					szBuffer +=  str(pHeadSelectedCity.getCulture(pHeadSelectedCity.getOwner())) + CyTranslator().getText("[COLOR_POSITIVE_TEXT] +", ()) + str(iRate) + CyTranslator().getText("[COLOR_REVERT] / ", ()) + CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ()) + str(pHeadSelectedCity.getCultureThreshold()) + CyTranslator().getText("[COLOR_REVERT]", ()) + "</font>"

					screen.addTableControlGFC( "CultureText", 1, 12, yResolution - 187, iBarWidth, iStackBarHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY )
					screen.setTableColumnHeader( "CultureText", 0, u"", iBarWidth)
					screen.appendTableRow( "CultureText" )
					screen.setTableText( "CultureText", 0, 0, szBuffer, "Art/Interface/Buttons/Process/ProcessCulture.dds", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
					screen.setHitTest( "CultureText", HitTestTypes.HITTEST_NOHIT )
				iCurrent = pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())
				iThreshold = 100 * pHeadSelectedCity.getCultureThreshold()
				screen.setBarPercentage("CultureBar", InfoBarTypes.INFOBAR_STORED, float(iCurrent) / iThreshold)
				screen.setBarPercentage("CultureBar", InfoBarTypes.INFOBAR_RATE, 0.0)
				if iCurrent < iThreshold:
					screen.setBarPercentage("CultureBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) )
				screen.show( "CultureBar" )
## Culture Bar ##				
		else:
		
			# Help Text Area
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
				self.setMinimapButtonVisibility(True)
			screen.hide( "CityScreenCenterTopWidget" )
			screen.hide( "InterfaceCenterLeftBackgroundWidget" )
			screen.hide( "CityScreenTopWidget" )
			screen.hide( "CityNameBackground" )
			screen.hide( "TopCityPanelLeft" )
			screen.hide( "TopCityPanelRight" )
			screen.hide( "CityScreenAdjustPanel" )
			screen.hide( "InterfaceCenterRightBackgroundWidget" )

		return 0
		
	def updateInfoPaneStrings( self ):
## Ultrapack ##	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		iPanelWidth = self.iBottomPanelWidth - 24
		screen.addPanel( "SelectedUnitPanel", u"", u"", True, False, 8, yResolution - 140, iPanelWidth, 130, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitPanel", "Panel_Game_HudStat_Style" )
		iTableWidth = iPanelWidth *5/8
		screen.addTableControlGFC( "SelectedUnitText", 2, 10, yResolution - 109, iTableWidth, 96, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitText", "Table_EmptyScroll_Style" )
		screen.addTableControlGFC( "SelectedCityText", 1, 10, yResolution - 138, iTableWidth, 120, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedCityText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedUnitText" )
		screen.hide( "SelectedUnitCombat" )
		screen.hide( "SelectedUnitLabel" )
		screen.hide("SelectedUnitPanel")
		screen.hide( "SelectedCityText" )
## Hidden Promotions ##
		screen.hide("UnitPromotions")
## Hidden Promotions ##
## Experience Bar ##
		screen.hide("ExperienceBar")
		screen.hide("ExperienceText")
## Experience Bar ##
## Unit List Scroll ##
		screen.hide("UnitListScrollPlus")
		screen.hide("UnitListScrollMinus")
## Unit List Scroll ##
			
		if CyEngine().isGlobeviewUp():
			return

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

		if pHeadSelectedCity:
			screen.show("SelectedUnitPanel")
			iOrders = CyInterface().getNumOrdersQueued()
			sColor = u"<color=255,255,255,0>"
			if PlatyOptions.bCivColors:
				sColor = u"<color=%d,%d,%d,%d>" %(gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorR(), gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorG(), gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorB(), gc.getPlayer(pHeadSelectedCity.getOwner()).getPlayerTextColorA())		
			for i in xrange( iOrders ):
				szLeftBuffer = u""
				szRightBuffer = u""
				
				if CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN:
					szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(CyInterface().getOrderNodeData1(i))
					szRightBuffer = " (" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

					if (CyInterface().getOrderNodeSave(i)):
						szLeftBuffer = u"*" + szLeftBuffer

				elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT:
					szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szButton = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getButton()
					szRightBuffer = " (" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

				elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CREATE:
					szLeftBuffer = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szButton = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getButton()
					szRightBuffer = " (" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

				elif CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_MAINTAIN:
					szLeftBuffer = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szButton = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getButton()
				szLeftBuffer += szRightBuffer
				iRow = screen.appendTableRow( "SelectedCityText" )
				screen.setTableText( "SelectedCityText", 0, iRow, sColor + szLeftBuffer + u"</color>", szButton, WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.show( "SelectedCityText" )

		elif (pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			screen.show("SelectedUnitPanel")
## Unit List Scroll ##
			iPlayer = pHeadSelectedUnit.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.getNumUnits() > 1:
				screen.show("UnitListScrollPlus")
				screen.show("UnitListScrollMinus")
## Unit List Scroll ##
			sColor = u"<color=255,255,255,0>"
			if PlatyOptions.bCivColors:
				sColor = u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
			pSelectedGroup = 0	
			if CyInterface().mirrorsSelectionGroup():
				pSelectedGroup = pHeadSelectedUnit.getGroup()

			if CyInterface().getLengthSelectionList() > 1:
				screen.setText( "SelectedUnitLabel", "Background", localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), )), CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
				if pSelectedGroup == 0 or pSelectedGroup.getLengthMissionQueue() < 2:
					if pHeadSelectedUnit:
						for i in xrange(gc.getNumUnitInfos()):
							iCount = CyInterface().countEntities(i)
							if iCount > 0:
								szLeftBuffer = gc.getUnitInfo(i).getDescription()
								if iCount > 1:
									szLeftBuffer += u" (" + str(iCount) + u")"
								iRow = screen.appendTableRow( "SelectedUnitText" )
								screen.setTableText( "SelectedUnitText", 0, iRow, sColor + szLeftBuffer + u"</color>", gc.getUnitInfo(i).getButton(), WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
## Platy Unit Display ##
								screen.show( "SelectedUnitText" )
			else:
	## Hides Unit Type for Named Units ##
				sName = pHeadSelectedUnit.getNameNoDesc()
				if len(sName) == 0:
					sName = pHeadSelectedUnit.getName()
	## Hides Unit Type for Named Units ##
				if pHeadSelectedUnit.getHotKeyNumber() == -1:
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (sName, ))
				else:
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), sName))
				iCombatType = pHeadSelectedUnit.getUnitCombatType()
				if iCombatType == -1:
					if len(szBuffer) > 60:
						szBuffer = "<font=2>" + szBuffer + "</font>"
					screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
				else:
					if len(szBuffer) > 50:
						szBuffer = "<font=2>" + szBuffer + "</font>"
					sButton = gc.getUnitCombatInfo(iCombatType).getButton()
					screen.addDDSGFC("SelectedUnitCombat", sButton, 18, yResolution - 136, 21, 21, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 1 )
					screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18 + 21, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
			
				if pSelectedGroup == 0 or pSelectedGroup.getLengthMissionQueue() < 2:
					screen.setTableColumnHeader( "SelectedUnitText", 0, "", iTableWidth * 55/100)
					screen.setTableColumnHeader( "SelectedUnitText", 1, "", iTableWidth * 45/100)
					screen.show( "SelectedUnitText" )
					szLeftBuffer = ""
## Promotions ##
					iNumRow = 6
					iNumColumn = (iPanelWidth * 3/8) /24
					iWidth = iNumColumn * 24
					screen.addTableControlGFC("UnitPromotions", iNumColumn, iPanelWidth - iWidth + 10, yResolution - 144, iWidth + 20, 24*iNumRow + 2, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
					for i in xrange(iNumColumn):
						screen.setTableColumnHeader("UnitPromotions", i, "", 24)
					iPromotionCount = 0
					iMaxRow = -1
					for i in xrange(gc.getNumPromotionInfos()):
						if pHeadSelectedUnit.isHasPromotion(i):
							sPromotion = gc.getPromotionInfo(i).getType()
							sLast = sPromotion[-1]
							if sLast.isdigit():
								sPromotion = sPromotion[:-1] + str(int(sLast) +1)
								if gc.getInfoTypeForString(sPromotion) > -1:
									pass
									#if pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString(sPromotion)): continue
							if iPromotionCount < iNumColumn * iNumRow:
								iPRow = iPromotionCount % iNumRow
								iColumn = iNumColumn - iPromotionCount/iNumRow - 1
							else:
								iPRow = iPromotionCount/iNumColumn
								iColumn = iNumColumn - iPromotionCount % iNumColumn - 1
							if iMaxRow < iPRow:
								iMaxRow = iPRow
								screen.appendTableRow("UnitPromotions")
							screen.setTableText("UnitPromotions", iColumn, iPRow, "", gc.getPromotionInfo(i).getButton(), WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(i).getActionInfoIndex(), -1, CvUtil.FONT_CENTER_JUSTIFY )
							iPromotionCount += 1
## Promotions ##
					
					if pHeadSelectedUnit.canFight():
						szLeftBuffer = localText.getText("INTERFACE_PANE_STRENGTH", ())
						if pHeadSelectedUnit.isFighting():
							szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
						elif pHeadSelectedUnit.isHurt():
							szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
						else:
							szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					if szLeftBuffer:
						iRow = screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, sColor + szLeftBuffer + u"</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, sColor + szRightBuffer + u"</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						
					szLeftBuffer = ""
					if pHeadSelectedUnit.airBaseCombatStr() > 0:
						szLeftBuffer = localText.getText("INTERFACE_PANE_AIR_STRENGTH", ())
						if pHeadSelectedUnit.isFighting():
							szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
						elif pHeadSelectedUnit.isHurt():
							szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.airBaseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
						else:
							szRightBuffer = u"%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					if szLeftBuffer:
						iRow = screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, sColor + szLeftBuffer + u"</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, sColor + szRightBuffer + u"</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						
					iDenom = pHeadSelectedUnit.movesLeft() % gc.getMOVE_DENOMINATOR() > 0
					iCurrMoves = ((pHeadSelectedUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
					szLeftBuffer = localText.getText("INTERFACE_PANE_MOVEMENT", ())
					if pHeadSelectedUnit.baseMoves() == iCurrMoves:
						szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
					else:
						szRightBuffer = u"%d/%d%c" %(iCurrMoves, pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
					iRow = screen.appendTableRow( "SelectedUnitText" )
					screen.setTableText( "SelectedUnitText", 0, iRow, sColor + szLeftBuffer + u"</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText( "SelectedUnitText", 1, iRow, sColor + szRightBuffer + u"</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
## Air Range ##
					iRange = pHeadSelectedUnit.airRange()
					if iRange:
						if iRow < 2 or pHeadSelectedUnit.getUnitCombatType() == -1:
							iRow = screen.appendTableRow("SelectedUnitText")
							screen.setTableText("SelectedUnitText", 0, iRow, sColor + CyTranslator().getText("TXT_KEY_PEDIA_AIR_RANGE", ()) + u":</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
							screen.setTableText("SelectedUnitText", 1, iRow, sColor + str(iRange) + CyTranslator().getText("[ICON_TRADE]", ()) + u"</color>", "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
## Experience Bar ##
					if pHeadSelectedUnit.getUnitCombatType() > -1 and not pHeadSelectedUnit.isFighting():
						iX = 16
						iY = yResolution - 40
						iWidth = iTableWidth - iX
						screen.addStackedBarGFC("ExperienceBar", iX, iY, iWidth, 30, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
						iExperience = pHeadSelectedUnit.getExperience()
						iThreshold = pHeadSelectedUnit.experienceNeeded()
						screen.setBarPercentage("ExperienceBar", InfoBarTypes.INFOBAR_STORED, float(iExperience) / float(iThreshold))
						screen.setStackedBarColors("ExperienceBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
						if iExperience < iThreshold:
							screen.setStackedBarColors("ExperienceBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CYAN"))
						screen.setStackedBarColors("ExperienceBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
						sText = u"%s %d (%d/%d)" %(CyTranslator().getText("INTERFACE_PANE_LEVEL", ()), pHeadSelectedUnit.getLevel(), iExperience, iThreshold)
						screen.setLabel("ExperienceText", "", sText, CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth/2, iY + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
## Experience Bar ##

			if pSelectedGroup:
				iNodeCount = pSelectedGroup.getLengthMissionQueue()
				if iNodeCount > 1:
					screen.setTableColumnHeader( "SelectedUnitText", 0, u"", iTableWidth)
					for i in xrange( iNodeCount ):
## Platy Mission Display ##
						szLeftBuffer = gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription()
						sButton = gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getButton()
						if gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild():
							szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
							if i == 0:
								szLeftBuffer += " (" + str(pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0)) + ")"
							sButton = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getButton()
						iRow = screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, sColor + szLeftBuffer + u"</color>", sButton, WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
## Platy Mission Display ##
		return 0
		
	def updateScoreStrings( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		screen.hide("ScoreBackground")
		screen.hide("ScoreRowPlus")
		screen.hide("ScoreRowMinus")
		screen.hide("ScoreWidthPlus")
		screen.hide("ScoreWidthMinus")
		if CyEngine().isGlobeviewUp(): return
		if CyInterface().isCityScreenUp(): return
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL: return
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY: return
		if not CyInterface().isScoresVisible(): return

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		lMasters = []
		lVassals = []
		lPlayers = []
		if CyInterface().isScoresMinimized():
			lPlayers.append(CyGame().getActivePlayer())
		else:
			for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive():
					iTeamX = pPlayerX.getTeam()
					pTeamX = gc.getTeam(iTeamX)
					if pTeamX.isHasMet(CyGame().getActiveTeam()) or CyGame().isDebugMode():
						if pTeamX.isAVassal():
							for iTeamY in xrange(gc.getMAX_CIV_TEAMS()):
								if pTeamX.isVassal(iTeamY):
									lVassals.append([CyGame().getTeamRank(iTeamY), CyGame().getTeamRank(iTeamX), CyGame().getPlayerRank(iPlayerX), iPlayerX])
									break
						else:
							lMasters.append([CyGame().getTeamRank(iTeamX), CyGame().getPlayerRank(iPlayerX), iPlayerX])
		lMasters.sort()
		lVassals.sort()
		for i in xrange(len(lMasters)):
			lPlayers.append(lMasters[i][2])
			if i < len(lMasters) - 1 and lMasters[i][0] == lMasters[i + 1][0]: continue
			for j in lVassals:
				if j[0] == lMasters[i][0]:
					lPlayers.append(j[3])
				elif j[0] > lMasters[i][0]:
					break
				
		nRows = len(lPlayers)
		self.iScoreRows = max(0, min(self.iScoreRows, nRows - 1))
		iHeight = min(yResolution - 300, max(1, (nRows - self.iScoreRows)) * 24 + 2)
		screen.addTableControlGFC("ScoreBackground", 5, xResolution - self.iScoreWidth - 150, yResolution - iHeight - 180, self.iScoreWidth + 150, iHeight, False, False, 23, 23, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect("ScoreBackground", False)
		screen.setTableColumnHeader("ScoreBackground", 0, "", self.iScoreWidth)
		screen.setTableColumnHeader("ScoreBackground", 1, "", 23)
		screen.setTableColumnHeader("ScoreBackground", 2, "", 23)
		screen.setTableColumnHeader("ScoreBackground", 3, "", 23)
		screen.setTableColumnHeader("ScoreBackground", 4, "", 73)
		screen.setButtonGFC("ScoreWidthMinus", "", "", xResolution - 50, yResolution - 180, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
		screen.setButtonGFC("ScoreRowMinus", "", "", xResolution - 70, yResolution - 180, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
		screen.setButtonGFC("ScoreRowPlus", "", "", xResolution - 90, yResolution - 180, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
		screen.setButtonGFC("ScoreWidthPlus", "", "", xResolution - 110, yResolution - 180, 20, 20, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT)
		for iPlayer in lPlayers:
			iRow = screen.appendTableRow("ScoreBackground")
			pPlayer = gc.getPlayer(iPlayer)
			iTeam = pPlayer.getTeam()
			pTeam = gc.getTeam(iTeam)

			sText1 = u"<font=2>"
			if CyGame().isGameMultiPlayer() and not pPlayer.isTurnActive():
				sText1 += "*"
			if CyGame().isNetworkMultiPlayer():
				sText1 += CyGameTextMgr().getNetStats(iPlayer)				
			if pPlayer.isHuman() and CyInterface().isOOSVisible():
				sText1 += u" <color=255,0,0>* %s *</color>" %(CyGameTextMgr().getOOSSeeds(iPlayer))
			if not pTeam.isHasMet(CyGame().getActiveTeam()):
				sText1 += " ?"

			iReligion = pPlayer.getStateReligion()
			if iReligion > -1:
				if pPlayer.hasHolyCity(iReligion):
					sText1 += u"%c" %(gc.getReligionInfo(iReligion).getHolyCityChar())
				else:
					sText1 += u"%c" %(gc.getReligionInfo(iReligion).getChar())
			
			sButton = "INTERFACE_ATTITUDE_BOY"
			if not pPlayer.isHuman():
				lVincent = ["INTERFACE_ATTITUDE_0", "INTERFACE_ATTITUDE_1", "INTERFACE_ATTITUDE_2", "INTERFACE_ATTITUDE_3", "INTERFACE_ATTITUDE_4"]
				sButton = lVincent[pPlayer.AI_getAttitude(CyGame().getActivePlayer())]
			screen.setTableText("ScoreBackground", 1, iRow, "", ArtFileMgr.getInterfaceArtInfo(sButton).getPath(), WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("ScoreBackground", 2, iRow, "", gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("ScoreBackground", 3, iRow, "", gc.getCivilizationInfo(pPlayer.getCivilizationType()).getButton(), WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iPlayer == CyGame().getActivePlayer():
				sText1 += CyTranslator().getText("[ICON_POWER]", ())
			else:
				if pTeam.isAtWar(CyGame().getActiveTeam()):
					sText1 += CyTranslator().getText("[ICON_OCCUPATION]", ())
				elif pPlayer.canTradeNetworkWith(CyGame().getActivePlayer()):
					sText1 += CyTranslator().getText("[ICON_TRADE]", ())
				if pTeam.isOpenBorders(CyGame().getActiveTeam()):
					sText1 += CyTranslator().getText("[ICON_OPENBORDERS]", ())
				if pTeam.isDefensivePact(CyGame().getActiveTeam()):
					sText1 += CyTranslator().getText("[ICON_DEFENSIVEPACT]", ())
				if pTeam.getEspionagePointsAgainstTeam(CyGame().getActiveTeam()) < gc.getTeam(CyGame().getActiveTeam()).getEspionagePointsAgainstTeam(iTeam):
					sText1 += CyTranslator().getText("[ICON_ESPIONAGE]", ())
			if pTeam.isAVassal():
				sText1 += CyTranslator().getText("[ICON_SILVER_STAR]", ())
			sText1 += u"<color=%d,%d,%d,%d>%d</color>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), CyGame().getPlayerScore(iPlayer)) + u"</font>"
			screen.setTableText("ScoreBackground", 0, iRow, sText1, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY)
			bEspionageCanSeeResearch = false
			for iMissionLoop in xrange(gc.getNumEspionageMissionInfos()):
				if (gc.getEspionageMissionInfo(iMissionLoop).isSeeResearch()):
					bEspionageCanSeeResearch = gc.getPlayer(CyGame().getActivePlayer()).canDoEspionageMission(iMissionLoop, iPlayer, None, -1)
					break
				
			if iTeam == CyGame().getActiveTeam() or pTeam.isVassal(CyGame().getActiveTeam()) or CyGame().isDebugMode() or bEspionageCanSeeResearch:
				iTech = pPlayer.getCurrentResearch()
				if iTech > -1:
					sTech = u"<color=%d,%d,%d,%d>%d</color>" %( pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA(), pPlayer.getResearchTurnsLeft(pPlayer.getCurrentResearch(), True))
					screen.setTableText("ScoreBackground", 4, iRow, sTech, gc.getTechInfo(iTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, CvUtil.FONT_LEFT_JUSTIFY)

	def updateHelpStrings( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.setHelpTextString( CyInterface().getHelpString() )
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL:
			screen.setHelpTextString( "" )		
		return 0

	# Will build the globeview UI
	def updateGlobeviewButtons( self ):
		kInterface = CyInterface()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()
		iCurrentLayerID = kGLM.getCurrentLayerID()
		
		# Positioning things based on the visibility of the globe
		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		if kEngine.isGlobeviewUp():
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		elif CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW:
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )

		
		# Set base Y position for the LayerOptions, if we find them	
		iY = yResolution - iGlobeLayerOptionsY_Regular
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iGlobeLayerOptionsY_Minimal

		# Hide the layer options ... all of them
		for i in xrange (20):
			szName = "GlobeLayerOption" + str(i)
			screen.hide(szName)

		# Setup the GlobeLayer panel
		iNumLayers = kGLM.getNumLayers()
		if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
			screen.setState("GlobeToggle", True)
			for i in xrange(kGLM.getNumLayers()):
				szButtonID = "GlobeLayer" + str(i)
				screen.setState( szButtonID, iCurrentLayerID == i )
				
			# Set up options pane
			if iCurrentLayerID > -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() > 0:
				kLayer = kGLM.getLayer(iCurrentLayerID)

				iCurY = iY
				iNumOptions = kLayer.getNumOptions()
				iCurOption = kLayer.getCurrentOption()
				for iOption in xrange(iNumOptions):
					szName = "GlobeLayerOption" + str(iOption)
					szCaption = kLayer.getOptionName(iOption)
					szBuffer = "  %s  " % (szCaption)		
					if(iOption == iCurOption):
						szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
					iTextWidth = CyInterface().determineWidth( szBuffer )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1 )
					screen.show( szName )

					iCurY -= iGlobeLayerOptionHeight
			self.updateScoreStrings()

		else:
			screen.setState("ResourceIcons", False)
			screen.setState("UnitIcons", False)
			if iCurrentLayerID > -1:
				kLayer = kGLM.getLayer(iCurrentLayerID)
				screen.setState("ResourceIcons", kLayer.getName() == "RESOURCES")
				screen.setState("UnitIcons", kLayer.getName() == "UNITS")
				
			screen.setState("Grid", CyUserProfile().getGrid())
			screen.setState("BareMap", CyUserProfile().getMap())
			screen.setState("Yields", CyUserProfile().getYields())
			screen.setState("ScoresVisible", CyUserProfile().getScores())

			screen.hide( "InterfaceGlobeLayerPanel" )
			screen.setState("GlobeToggle", False )

	# Update minimap buttons
	def setMinimapButtonVisibility( self, bVisible):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		kInterface = CyInterface()
		kGLM = CyGlobeLayerManager()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( CyInterface().isCityScreenUp() ):
			bVisible = False
		
		kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
		kGlobeButtons = []
		for i in range(kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)
			kGlobeButtons.append(szButtonID)
		
		if bVisible:
			if CyEngine().isGlobeviewUp():
				kHide = kMainButtons
				kShow = kGlobeButtons
			else:
				kHide = kGlobeButtons
				kShow = kMainButtons
			screen.show( "GlobeToggle" )
			
		else:
			kHide = kMainButtons + kGlobeButtons
			kShow = []
			screen.hide( "GlobeToggle" )
		
		for szButton in kHide:
			screen.hide(szButton)
		
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iMinimapButtonsY_Minimal
			iGlobeY = yResolution - iGlobeButtonY_Minimal 
		else:
			iY = yResolution - iMinimapButtonsY_Regular
			iGlobeY = yResolution - iGlobeButtonY_Regular
			
		iBtnX = xResolution - 39
		screen.moveItem("GlobeToggle", iBtnX, iGlobeY, 0.0)
		
		iBtnAdvance = 28
		iBtnX = iBtnX - len(kShow)*iBtnAdvance - 10
		if len(kShow) > 0:		
			i = 0
			for szButton in kShow:
				screen.moveItem(szButton, iBtnX, iY, 0.0)
				screen.moveToFront(szButton)
				screen.show(szButton)
				iBtnX += iBtnAdvance
				i += 1
				
	
	def createGlobeviewButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()

		for i in range (kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)

			kLayer = kGLM.getLayer(i)
			szStyle = kLayer.getButtonStyle()
			
			if szStyle == 0 or szStyle == "":
				szStyle = "Button_HUDSmall_Style"
			
			screen.addCheckBoxGFC( szButtonID, "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_GLOBELAYER, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.setStyle( szButtonID, szStyle )
			screen.hide( szButtonID )
				
			
	def createMinimapButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.addCheckBoxGFC( "UnitIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_UNIT_ICONS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "UnitIcons", "Button_HUDGlobeUnit_Style" )
		screen.setState( "UnitIcons", False )
		screen.hide( "UnitIcons" )

		screen.addCheckBoxGFC( "Grid", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GRID).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Grid", "Button_HUDBtnGrid_Style" )
		screen.setState( "Grid", False )
		screen.hide( "Grid" )

		screen.addCheckBoxGFC( "BareMap", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_BARE_MAP).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "BareMap", "Button_HUDBtnClearMap_Style" )
		screen.setState( "BareMap", False )
		screen.hide( "BareMap" )

		screen.addCheckBoxGFC( "Yields", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_YIELDS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Yields", "Button_HUDBtnTileAssets_Style" )
		screen.setState( "Yields", False )
		screen.hide( "Yields" )

		screen.addCheckBoxGFC( "ScoresVisible", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_SCORES).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ScoresVisible", "Button_HUDBtnRank_Style" )
		screen.setState( "ScoresVisible", True )
		screen.hide( "ScoresVisible" )

		screen.addCheckBoxGFC( "ResourceIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RESOURCE_ALL).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ResourceIcons", "Button_HUDBtnResources_Style" )
		screen.setState( "ResourceIcons", False )
		screen.hide( "ResourceIcons" )
		
		screen.addCheckBoxGFC( "GlobeToggle", "", "", -1, -1, 36, 36, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GLOBELAYER).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "GlobeToggle", "Button_HUDZoom_Style" )
		screen.setState( "GlobeToggle", False )
		screen.hide( "GlobeToggle" )

	def update(self, fDelta):
		return
	
	def forward(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_NEXTCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_NEXTUNIT)
		
	def back(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_PREVCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_PREVUNIT)

	def handleInput(self, inputClass):
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
## Commerce Flexibles ##
			if inputClass.getFunctionName().find("IncreasePercent") > -1:
				if CyInterface().shiftKey():
					CyMessageControl().sendModNetMessage(5678, inputClass.getData1(), 100, -1, -1)
			elif inputClass.getFunctionName().find("DecreasePercent") > -1:
				if CyInterface().shiftKey():
					CyMessageControl().sendModNetMessage(5678, inputClass.getData1(), 0, -1, -1)
## Advisor Filter ##
			elif inputClass.getFunctionName().find("AdvisorFilter") > -1:
				self.lAdvisors[inputClass.getData2()] = not self.lAdvisors[inputClass.getData2()]
				self.updateSelectionButtons()
			elif inputClass.getFunctionName() == "PrereqFilter":
				self.bPrereq = not self.bPrereq
				self.updateSelectionButtons()
## Full Order List ##
			elif inputClass.getFunctionName() == "FullOrderList":
				OrderList.OrderList().interfaceScreen()
## Field of View ##
			elif inputClass.getFunctionName().find("FOV") > -1:
				iAdjustment = inputClass.getData2()
				if CyInterface().shiftKey():
					iAdjustment *= 10
				if inputClass.getData1() == 7000:
					gc.setDefineFLOAT("FIELD_OF_VIEW", max(1.0, min(125.0, gc.getDefineFLOAT("FIELD_OF_VIEW") + iAdjustment)))
					self.updateGameDataStrings()
				elif inputClass.getData1() == 6999:
					gc.setDefineFLOAT("CAMERA_CITY_ZOOM_IN_DISTANCE", max(1.0, gc.getDefineFLOAT("CAMERA_CITY_ZOOM_IN_DISTANCE") + iAdjustment))
## Score Board ##
			elif inputClass.getFunctionName() == "ScoreRowPlus":
				self.iScoreRows -= 1
				self.updateScoreStrings()
			elif inputClass.getFunctionName() == "ScoreRowMinus":
				self.iScoreRows += 1
				self.updateScoreStrings()
			elif inputClass.getFunctionName() == "ScoreWidthPlus":
				self.iScoreWidth += 10
				self.updateScoreStrings()
			elif inputClass.getFunctionName() == "ScoreWidthMinus":
				self.iScoreWidth = max(0, self.iScoreWidth - 10)
				self.updateScoreStrings()
## Trackers ##
			elif inputClass.getFunctionName() == "WorldTrackerButton":
				WorldTracker.WorldTracker().interfaceScreen()
## Platy Options ##
			elif inputClass.getFunctionName() == "PlatyOptionsButton":
				PlatyOptions.PlatyOptions().interfaceScreen()
## Unit List Scroll ##
			elif inputClass.getFunctionName().find("UnitListScroll") > -1:
				bReverse = inputClass.getData2()
				pUnit = CyInterface().getHeadSelectedUnit()
				if pUnit:
					bFound = False
					pPlayer = gc.getPlayer(pUnit.getOwner())
					pNewGroup = None
					(pGroup, iter) = pPlayer.firstSelectionGroup(bReverse)
					while(pGroup):
						if bFound:
							if pGroup.readyToMove(False):
								pNewGroup = pGroup
								break
						if pGroup.getID() == pUnit.getGroupID():
							bFound = True
						(pGroup, iter) = pPlayer.nextSelectionGroup(iter, bReverse)
					if not pNewGroup:
						(pGroup, iter) = pPlayer.firstSelectionGroup(bReverse)
						while(pGroup):
							if pGroup.readyToMove(False):
								pNewGroup = pGroup
								break
							if pGroup.getID() == pUnit.getGroupID():
								break
							(pGroup, iter) = pPlayer.nextSelectionGroup(iter, bReverse)
					if pNewGroup:
						pNewUnit = pNewGroup.getHeadUnit()
					else:
						pNewUnit = CyInterface().getHeadSelectedUnit()
					CyInterface().selectGroup(pNewUnit, False, False, False)
					pNewUnit.centerCamera()
## Specialist Count ##
		elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			if inputClass.getFunctionName() == "SpecialistTable":
				self.iSelectedSpecialist = inputClass.getData1()
				self.updateCityScreen()
				self.updateCitizenButtons()
## Resource Filter ##
			elif inputClass.getFunctionName() == "ResourceFilter":
				self.iBonusClass = inputClass.getData()
				self.updateCityScreen()
## Combat Filter ##
			elif inputClass.getFunctionName() == "UnitCombatFilter":
				iType = inputClass.getData2() + 1
				lUnitCombat[iType] = not lUnitCombat[iType]
				self.updateSelectionButtons()
		return 0