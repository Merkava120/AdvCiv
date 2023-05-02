from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

gc = CyGlobalContext()

class WorldTracker:
		
	def __init__(self):
		self.iWorldClass = 0
		
	def interfaceScreen(self):
		screen = CyGInterfaceScreen( "WorldTracker", CvScreenEnums.WORLD_TRACKER)

		self.nTableWidth = 600
		self.nScreenWidth = self.nTableWidth + 40
		self.nScreenHeight = screen.getYResolution() - 250
		self.nTableHeight = self.nScreenHeight - 125
		screen.setRenderInterfaceOnly(True)
		screen.setDimensions(screen.getXResolution()/2 - self.nScreenWidth/2, 100, self.nScreenWidth, self.nScreenHeight)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		# Here we set the background widget and exit button, and we show the screen
		screen.addPanel( "WorldTrackerBG", u"", u"", True, False, 0, 0, self.nScreenWidth, self.nScreenHeight, PanelStyles.PANEL_STYLE_MAIN )
		screen.setText("WorldExit", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.nScreenWidth - 25, self.nScreenHeight - 45, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		
		# Header...
		screen.setText("WorldHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_WORLD_TRACKER_HEADER", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.nScreenWidth/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szDropdownName = str("WorldClass")
		screen.addDropDownBoxGFC(szDropdownName, 20, 20, 180, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString(szDropdownName, CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), 0, 0, 0 == self.iWorldClass)
		screen.addPullDownString(szDropdownName, CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS",()), 1, 1, 1 == self.iWorldClass)
		screen.addPullDownString(szDropdownName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT",()), 2, 2, 2 == self.iWorldClass)

		# Build the table	
		screen.addTableControlGFC( "WorldTracker", 4, 20, 60, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader( "WorldTracker", 0, "<font=2>" + CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", 200)
		screen.setTableColumnHeader( "WorldTracker", 1, "<font=2>" + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()) + "</font>", 200)
		screen.setTableColumnHeader( "WorldTracker", 2, "<font=2>" + CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_PRODUCING", ()) + "</font>", 100)
		screen.setTableColumnHeader( "WorldTracker", 3, "<font=2>" + CyTranslator().getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()) + "</font>", 100)
		screen.enableSort( "WorldTracker" )
		screen.setStyle("WorldTracker", "Table_StandardCiv_Style")

		iRow = 0
		for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
			pPlayerX = gc.getPlayer(iPlayerX)
			(loopCity, iter) = pPlayerX.firstCity(False)
			while(loopCity):
				if loopCity.getEspionageVisibility(CyGame().getActiveTeam()) or pPlayerX.getTeam() == CyGame().getActiveTeam():
					if self.iWorldClass != 2:
						iBuilding = loopCity.getProductionBuilding()
						if iBuilding > -1:
							BuildingInfo = gc.getBuildingInfo(iBuilding)
							if isWorldWonderClass(BuildingInfo.getBuildingClassType()):
								screen.appendTableRow("WorldTracker")
								screen.setTableText("WorldTracker", 1, iRow, BuildingInfo.getDescription(), BuildingInfo.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText("WorldTracker", 0, iRow, loopCity.getName(), gc.getCivilizationInfo(pPlayerX.getCivilizationType()).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, loopCity.getOwner(), loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
								sText = str(loopCity.getProduction()) + " / " + str(loopCity.getProductionNeeded())
								screen.setTableText("WorldTracker", 2, iRow, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								screen.setTableText("WorldTracker", 3, iRow, str(loopCity.getBuildingProductionTurnsLeft(iBuilding, 0)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								iRow += 1
					if self.iWorldClass != 1:
						iProject = loopCity.getProductionProject()
						if iProject > -1:
							ProjectInfo = gc.getProjectInfo(iProject)
							if ProjectInfo.getMaxGlobalInstances() > 0:
								screen.appendTableRow("WorldTracker")
								screen.setTableText("WorldTracker", 1, iRow, ProjectInfo.getDescription(), ProjectInfo.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iProject, 1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText("WorldTracker", 0, iRow, loopCity.getName(), gc.getCivilizationInfo(pPlayerX.getCivilizationType()).getButton(), WidgetTypes.WIDGET_ZOOM_CITY, loopCity.getOwner(), loopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)
								sText = str(loopCity.getProduction()) + " / " + str(loopCity.getProductionNeeded())
								screen.setTableText("WorldTracker", 2, iRow, sText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								screen.setTableText("WorldTracker", 3, iRow, str(loopCity.getProjectProductionTurnsLeft(iProject, 0)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								iRow += 1
				(loopCity, iter) = pPlayerX.nextCity(iter, False)
				
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			if (inputClass.getFunctionName() == "WorldClass"):
				self.handlePlatyWorldClassCB(inputClass.getData())
				return
			if (inputClass.getMouseX() == 0):
				screen = CyGInterfaceScreen( "WorldTracker", CvScreenEnums.WORLD_TRACKER)
				screen.hideScreen()				
				CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), true);
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setText(u"showWorldTracker")
				popupInfo.addPopup(inputClass.getData1())
		return 0

	def handlePlatyWorldClassCB ( self, argsList ) :
		self.iWorldClass = int(argsList)
		self.interfaceScreen()
		return 1

	def update(self, fDelta):
		return 1