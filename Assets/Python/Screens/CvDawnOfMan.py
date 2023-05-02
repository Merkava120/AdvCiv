import CvUtil
from CvPythonExtensions import *
gc = CyGlobalContext()

class CvDawnOfMan:
	def __init__(self, iScreenID):
		self.iScreenID = iScreenID				
				
	def interfaceScreen(self):
		if CyGame().isPitbossHost(): return
		
		self.calculateSizesAndPositions()
		
		pPlayer = gc.getPlayer(CyGame().getActivePlayer())
		iLeader = pPlayer.getLeaderType()
		iCivilization = pPlayer.getCivilizationType()
		
		screen = CyGInterfaceScreen( "CvDawnOfMan", self.iScreenID )		
		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground( False )
		screen.enableWorldSounds( false )
		
		# Create panels
		
		# Main
		szMainPanel = "DawnOfManMainPanel"
		screen.addPanel( szMainPanel, "", "", true, true, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		
		# Top
		szHeaderPanel = "DawnOfManHeaderPanel"
		screen.addPanel( szHeaderPanel, "", "", true, false, self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNTOP )
		
		# Bottom
		szTextPanel = "DawnOfManTextPanel"
		screen.addPanel( szTextPanel, "", "", true, true, self.X_HEADER_PANEL, self.Y_TEXT_PANEL, self.W_HEADER_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		
		# Add contents
		
		# Leaderhead graphic
		szLeaderPanel = "DawnOfManLeaderPanel"
		screen.addPanel( szLeaderPanel, "", "", true, false, self.X_LEADER_ICON - 3, self.Y_LEADER_ICON - 5, self.W_LEADER_ICON + 6, self.H_LEADER_ICON + 8, PanelStyles.PANEL_STYLE_DAWNTOP )
		screen.addLeaderheadGFC("LeaderHead", iLeader, AttitudeTypes.ATTITUDE_PLEASED, self.X_LEADER_ICON + 5, self.Y_LEADER_ICON + 5, self.W_LEADER_ICON - 10, self.H_LEADER_ICON - 10, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Info/"Stats" text
		
		szNameText = "<color=255,255,0,255>" + u"<font=4b>" + CyTranslator().getText("[ICON_STAR]", ()) + gc.getLeaderHeadInfo(iLeader).getDescription().upper() + CyTranslator().getText("[ICON_STAR]", ()) + u"</font>"
		szNameText += "\n<font=3b>- " + pPlayer.getCivilizationDescription(0) + " -</font>"
		screen.addMultilineText( "NameText", szNameText, self.X_LEADER_TITLE_TEXT, self.Y_FANCY_ICON, self.W_LEADER_TITLE_TEXT, self.H_LEADER_TITLE_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
## Ultrapack ##		
		screen.addMultilineText( "HeaderText2", CyTranslator().getText("TXT_KEY_FREE_TECHS", ()) + ":", self.X_FANCY_ICON1, self.Y_STATS, self.W_STATS, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addPanel( "HeaderText3", "", "", false, true, self.X_FANCY_ICON1, self.Y_STATS+15, self.W_STATS, self.H_STATS, PanelStyles.PANEL_STYLE_EMPTY )
		
		for iTech in xrange(gc.getNumTechInfos()):
			if gc.getCivilizationInfo(iCivilization).isCivilizationFreeTechs(iTech):
				screen.attachImageButton("HeaderText3", "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
		
		screen.addMultilineText( "HeaderText4", CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + ":", self.X_FANCY_ICON1, self.Y_STATS+25 + 64, self.W_STATS, 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addPanel( "HeaderText5", "", "", false, true, self.X_FANCY_ICON1, self.Y_STATS+40 + 64, self.W_STATS, self.H_STATS, PanelStyles.PANEL_STYLE_EMPTY )
		
		for iBuildingClass in xrange(gc.getNumBuildingClassInfos()):
			iUnique = gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(iBuildingClass)
			if iUnique == -1: continue
			iDefault = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex()
			if iDefault != iUnique:
				screen.attachImageButton( "HeaderText5", "", gc.getBuildingInfo(iUnique).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iUnique, 1, False )
		for iUnitClass in xrange(gc.getNumUnitClassInfos()):
			iUnique = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iUnitClass)
			if iUnique == -1: continue
			iDefault = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex()
			if iDefault != iUnique:
				screen.attachImageButton( "HeaderText5", "", gc.getUnitInfo(iUnique).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnique, 1, False )
## Ultrapack ##						
		# Fancy icon things
		screen.addDDSGFC( "IconLeft", gc.getLeaderHeadInfo(iLeader).getButton(), self.X_FANCY_ICON1 , self.Y_FANCY_ICON , self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, 1)
		screen.addDDSGFC( "IconRight", gc.getCivilizationInfo(iCivilization).getButton(), self.X_FANCY_ICON2 , self.Y_FANCY_ICON , self.WH_FANCY_ICON, self.WH_FANCY_ICON, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCivilization, -1 )
		
		# Main Body text
		szDawnTitle = u"<font=3>" + CyTranslator().getText("TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE", ()).upper() + u"</font>"
		screen.setLabel("DawnTitle", "Background", szDawnTitle, CvUtil.FONT_CENTER_JUSTIFY, self.X_HEADER_PANEL + (self.W_HEADER_PANEL / 2), self.Y_TEXT_PANEL + 15, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		bodyString = CyTranslator().getText("TXT_KEY_DAWN_OF_MAN_TEXT", (CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), false), pPlayer.getCivilizationAdjectiveKey(), pPlayer.getNameKey()))
## Specific DOM Text ##
		sCivilization = gc.getCivilizationInfo(iCivilization).getType()
		sDOM = CyTranslator().getText("TXT_KEY_DOM_" + sCivilization, ())
		if sDOM.find("TXT_") == -1:
			bodyString = sDOM
		sLeader = gc.getLeaderHeadInfo(iLeader).getType()
		sDOM = CyTranslator().getText("TXT_DOM_" + sLeader, ())
		if sDOM.find("TXT_") == -1:
			bodyString = sDOM
## Specific DOM Text ##
		screen.addMultilineText( "BodyText", bodyString, self.X_HEADER_PANEL + self.iMarginSpace, self.Y_TEXT_PANEL + self.iMarginSpace + self.iTEXT_PANEL_MARGIN, self.W_HEADER_PANEL - (self.iMarginSpace * 2), self.H_TEXT_PANEL - (self.iMarginSpace * 2) - 75, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setButtonGFC("Exit", CyTranslator().getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setSoundId(CyAudioGame().Play2DSoundWithId(gc.getLeaderHeadInfo(iLeader).getDiploPeaceMusicScriptIds(0)))
## Pedia ##
		screen.addMultilineText("PediaText", gc.getCivilizationInfo(iCivilization).getCivilopedia(), self.X_PEDIA, self.Y_PEDIA, self.W_PEDIA, self.H_PEDIA, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def handleInput( self, inputClass ):
		return 0
	
	def update(self, fDelta):
		return
		
	def onClose(self):
		CyInterface().setSoundSelectionReady(true)		
		return 0
			
	def calculateSizesAndPositions(self):		
		screen = CyGInterfaceScreen( "CvDawnOfMan", self.iScreenID )	
		
		self.W_MAIN_PANEL = screen.getXResolution() * 3/4
		self.H_MAIN_PANEL = screen.getYResolution() * 7/10
		self.X_MAIN_PANEL = (screen.getXResolution()/2) - (self.W_MAIN_PANEL/2)
		self.Y_MAIN_PANEL = 70
		
		self.iMarginSpace = 15
		
		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - self.iMarginSpace * 2
		self.H_HEADER_PANEL = 280
		
		self.X_LEADER_ICON = self.X_HEADER_PANEL + self.iMarginSpace
		self.Y_LEADER_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
		self.H_LEADER_ICON = self.H_HEADER_PANEL - self.iMarginSpace * 2
		self.W_LEADER_ICON = self.H_LEADER_ICON *11/14

		self.WH_FANCY_ICON = 64
		self.X_FANCY_ICON1 = self.X_LEADER_ICON + self.W_LEADER_ICON + self.iMarginSpace
		self.X_FANCY_ICON2 = self.X_MAIN_PANEL + self.W_MAIN_PANEL - self.iMarginSpace * 2 - self.WH_FANCY_ICON
		self.Y_FANCY_ICON = self.Y_HEADER_PANEL + self.iMarginSpace
		
		self.X_LEADER_TITLE_TEXT = self.X_FANCY_ICON1 + self.WH_FANCY_ICON
		self.W_LEADER_TITLE_TEXT = self.X_FANCY_ICON2 - self.X_LEADER_TITLE_TEXT
		self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 2
		
		self.Y_STATS = self.Y_FANCY_ICON + self.WH_FANCY_ICON + 6
		self.H_STATS = 80
		self.W_STATS = 68 * 3

		self.X_PEDIA = self.X_FANCY_ICON1 + self.W_STATS + self.iMarginSpace
		self.Y_PEDIA = self.Y_STATS + self.iMarginSpace
		self.W_PEDIA = self.W_HEADER_PANEL - self.W_LEADER_ICON - self.W_STATS - self.iMarginSpace * 4
		self.H_PEDIA = self.H_LEADER_ICON - self.WH_FANCY_ICON - self.iMarginSpace * 2
		
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.iMarginSpace
		self.H_TEXT_PANEL = self.H_MAIN_PANEL - self.H_HEADER_PANEL - self.iMarginSpace * 2
		self.iTEXT_PANEL_MARGIN = 35
		
		self.W_EXIT = 120
		self.H_EXIT = 30
		self.X_EXIT = (screen.getXResolution()/2) - (self.W_EXIT/2)
		self.Y_EXIT = self.Y_TEXT_PANEL + self.H_TEXT_PANEL - (self.iMarginSpace * 3)
