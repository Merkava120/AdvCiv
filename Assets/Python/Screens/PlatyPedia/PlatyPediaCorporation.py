from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaCorporation:
	def __init__(self, main):
		self.iCorporation = -1
		self.top = main
		self.bDisplaySpread = False
		self.bDisplayCost = False
		self.bDisplayMaintenance = False
		for i in xrange(1, gc.getNumCorporationInfos()):
			if gc.getCorporationInfo(i).getSpreadFactor() != gc.getCorporationInfo(i - 1).getSpreadFactor():
				self.bDisplaySpread = True
			if gc.getCorporationInfo(i).getSpreadCost() != gc.getCorporationInfo(i - 1).getSpreadCost():
				self.bDisplayCost = True
			if gc.getCorporationInfo(i).getMaintenance() != gc.getCorporationInfo(i - 1).getMaintenance():
				self.bDisplayMaintenance = True			
		
	def interfaceScreen(self, iCorporation):
		self.iCorporation = iCorporation
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_ICON = 150
		self.H_MAIN_PANE = 210
		self.X_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.X_ITEMS_PANE
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
		
		self.H_REQUIRES = 110
		self.X_REQUIRES = self.top.X_ITEMS_PANE + self.H_MAIN_PANE + 20
		self.Y_REQUIRES = self.top.Y_ITEMS_PANE - 20
		self.W_REQUIRES = self.top.W_ITEMS_PANE - self.top.W_BORDER - self.H_MAIN_PANE
		self.Y_ALLOWS = self.Y_REQUIRES + self.H_REQUIRES + 10

		self.W_TEXT = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.X_TEXT = self.top.X_ITEMS_PANE + self.W_TEXT + 20
		self.Y_TEXT = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_TEXT = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_TEXT

		szHeader = gc.getCorporationInfo(self.iCorporation).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sCorporationIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sCorporationIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_CORPORATION, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.H_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getCorporationInfo(self.iCorporation).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeSpecial()
		self.placeRequires()
		self.placeText()
		self.placeAllows()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_CORPORATION and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_CORPORATION

	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		Info = gc.getCorporationInfo(self.iCorporation)
		iTech = Info.getTechPrereq()
		if iTech > -1:
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(iBuilding).getFoundsCorporation() == self.iCorporation):
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )
				
		for iUnit in xrange(gc.getNumUnitInfos()):
			bRequired = false
			for iBuilding in xrange(gc.getNumBuildingInfos()):
				if (gc.getBuildingInfo(iBuilding).getFoundsCorporation() == self.iCorporation):
					if gc.getUnitInfo(iUnit).getBuildings(iBuilding) or gc.getUnitInfo(iUnit).getForceBuildings(iBuilding):
						bRequired = true
						break

			if bRequired:
				szButton = gc.getUnitInfo(iUnit).getButton()
				if self.top.iActivePlayer != -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(iUnit)
				screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False )

		for i in xrange(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
			iBonus = Info.getPrereqBonus(i)
			if iBonus > -1:
				screen.attachImageButton(panelName, "", gc.getBonusInfo(iBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, 1, False )
				
			
	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().parseCorporationInfo(self.iCorporation, True)[1:]
## Spread, Cost, Maintenance ##
		Info = gc.getCorporationInfo(self.iCorporation)
		if self.bDisplaySpread:
			szSpecialText += "\n\n" + CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_SPREAD", ()) + ": " + str(Info.getSpreadFactor())
		if self.bDisplayCost:
			szSpecialText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_COST", (Info.getSpreadCost(),))
		if self.bDisplayMaintenance:
			szSpecialText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + CyTranslator().getText("INTERFACE_CITY_MAINTENANCE", ()) + str(Info.getMaintenance())
## Spread, Cost, Maintenance ##
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE + 5, self.Y_TEXT+ 30, self.W_TEXT - 10, self.H_TEXT - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
				
	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, true, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getCorporationInfo(self.iCorporation).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getCorporationInfo(self.iCorporation).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_TEXT + 10, self.Y_TEXT + 30, self.W_TEXT - 20, self.H_TEXT - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
	def placeAllows(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_ALLOWS", ()), "", false, true, self.X_REQUIRES, self.Y_ALLOWS, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		
		for eLoopUnit in xrange(gc.getNumUnitInfos()):
			if (gc.getUnitInfo(eLoopUnit).getPrereqCorporation() == self.iCorporation):
				szButton = gc.getUnitInfo(eLoopUnit).getButton()
				if self.top.iActivePlayer != -1:
					szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(eLoopUnit)
				screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

		for eLoopBuilding in xrange(gc.getNumBuildingInfos()):
			if gc.getBuildingInfo(eLoopBuilding).getPrereqCorporation() == self.iCorporation:
				screen.attachImageButton( panelName, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )
				
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortCorporations(self.top.iSortCorporations)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sCorporationIcon, ()), self.iCorporation, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, -1)

	def handleInput (self, inputClass):
		return 0