import CvUtil
import CvScreenEnums
from CvPythonExtensions import *
gc = CyGlobalContext()

class CvTopCivs:
	def turnChecker(self, iTurnNum):
		if CyGame().isNetworkMultiPlayer(): return
		if CyGame().getActivePlayer() < 0: return
		if CyGame().isPitbossHost(): return
		if iTurnNum % 50 == 0 and iTurnNum > 0 and gc.getPlayer(CyGame().getActivePlayer()).isAlive():
			self.showScreen()

	def showScreen(self):
		screen = CyGInterfaceScreen( "CvTopCivs", CvScreenEnums.TOP_CIVS )
		self.iMarginSpace = 15
		self.W_EXIT = 120
		self.H_EXIT = 30

		self.Y_MAIN_PANEL = 70
		self.H_MAIN_PANEL = screen.getYResolution() * 7/10

		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.H_HEADER_PANEL = 110
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.iMarginSpace
		self.H_TEXT_PANEL = self.H_MAIN_PANEL - self.H_HEADER_PANEL - self.iMarginSpace * 4 - self.H_EXIT

		self.W_TEXT_PANEL = self.H_TEXT_PANEL *4/3
		self.W_MAIN_PANEL = self.W_TEXT_PANEL + 40
		if self.W_MAIN_PANEL > screen.getXResolution():
			self.W_MAIN_PANEL = screen.getXResolution()
			self.W_TEXT_PANEL = self.W_MAIN_PANEL - 40
			self.H_TEXT_PANEL = self.W_TEXT_PANEL * 3/4

		self.X_MAIN_PANEL = (screen.getXResolution() - self.W_MAIN_PANEL)/2
		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - self.iMarginSpace * 2
		
		self.X_EXIT = (screen.getXResolution()/2) - (self.W_EXIT/2)
		self.Y_EXIT = self.Y_TEXT_PANEL + self.H_TEXT_PANEL + self.iMarginSpace

		self.TITLE_TEXT = u"<font=3>" + CyTranslator().getText("TXT_KEY_TOPCIVS_TITLE", ()).upper() + u"</font>"
		self.EXIT_TEXT = CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper()
		
		self.HistorianList = [	CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN1", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN2", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN3", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN4", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN5", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN6", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN7", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN8", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN9", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN10", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_HISTORIAN11", ())
				    ]
					
		self.RankList =     [	CyTranslator().getText("TXT_KEY_TOPCIVS_RANK1", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_RANK2", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_RANK3", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_RANK4", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_RANK5", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_RANK6", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_RANK7", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_RANK8", ())
				    ]

		self.TypeList =    [	CyTranslator().getText("TXT_KEY_TOPCIVS_WEALTH", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_POWER", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_TECH", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_CULTURE", ()),
					CyTranslator().getText("TXT_KEY_TOPCIVS_SIZE", ()),
				    ]

		self.SymbolList =    [	CyTranslator().getText("[ICON_GOLD]", ()),
					CyTranslator().getText("[ICON_STRENGTH]", ()),
					CyTranslator().getText("[ICON_RESEARCH]", ()),
					CyTranslator().getText("[ICON_CULTURE]", ()),
					CyTranslator().getText("[ICON_MAP]", ()),
				    ]

		iType = CyGame().getSorenRandNum(len(self.TypeList), "Select Type")
		sType = self.TypeList[iType]
		szHistorianRand = self.HistorianList[CyGame().getSorenRandNum(len(self.HistorianList), "Select Historian")]
		
		# Create screen
		screen.setSound("AS2D_TOP_CIVS")
		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground( False )
		
		# Create panels
		szMainPanel = "TopCivsMainPanel"
		screen.addPanel( szMainPanel, "", "", true, true, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		szHeaderPanel = "TopCivsHeaderPanel"
		screen.addPanel( szHeaderPanel, "", "", true, true, self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		
		screen.setButtonGFC("Exit", self.EXIT_TEXT, "", self.X_EXIT,self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		self.X_TITLE_TEXT = self.X_HEADER_PANEL + (self.W_HEADER_PANEL / 2)
		self.Y_TITLE_TEXT = self.Y_HEADER_PANEL + 15
		screen.setLabel("DawnTitle", "Background", self.TITLE_TEXT, CvUtil.FONT_CENTER_JUSTIFY,	self.X_TITLE_TEXT, self.Y_TITLE_TEXT, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		szText = "<font=3>" + CyTranslator().getText("TXT_KEY_TOPCIVS_TEXT1", (szHistorianRand, )) + "</font>"
		screen.setLabel("InfoTextA", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE_TEXT + 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		szText = "<font=3>" + self.SymbolList[iType] + CyTranslator().getText("TXT_KEY_TOPCIVS_TEXT2", (sType,)) + self.SymbolList[iType] + "</font>"
		screen.setLabel("InfoTextB", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE_TEXT + 60, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.aiTopCivsValues = []
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isBarbarian(): continue
			if pPlayer.isAlive():
				if (sType == CyTranslator().getText("TXT_KEY_TOPCIVS_WEALTH", ())):
					self.aiTopCivsValues.append([pPlayer.getGold(), iPlayer])
					
				if (sType == CyTranslator().getText("TXT_KEY_TOPCIVS_POWER", ())):
					self.aiTopCivsValues.append([pPlayer.getPower(), iPlayer])

				if (sType == CyTranslator().getText("TXT_KEY_TOPCIVS_TECH", ())):
					iNumTechs = 0
					for iTechLoop in xrange(gc.getNumTechInfos()):
						if gc.getTeam(pPlayer.getTeam()).isHasTech(iTechLoop):
							iNumTechs += 1
					self.aiTopCivsValues.append([iNumTechs, iPlayer])

				if (sType == CyTranslator().getText("TXT_KEY_TOPCIVS_CULTURE", ())):
					self.aiTopCivsValues.append([pPlayer.countTotalCulture(), iPlayer])

				if (sType == CyTranslator().getText("TXT_KEY_TOPCIVS_SIZE", ())):
					self.aiTopCivsValues.append([pPlayer.getTotalLand(), iPlayer])
		self.aiTopCivsValues.sort()
		self.aiTopCivsValues.reverse()

		sBackGround = CyArtFileMgr().getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath()
		pFirstPlayer = gc.getPlayer(self.aiTopCivsValues[0][1])
		if gc.getTeam(pFirstPlayer.getTeam()).isHasMet(CyGame().getActiveTeam()):
			sType = gc.getCivilizationInfo(pFirstPlayer.getCivilizationType()).getType()
			sNewArt = CyArtFileMgr().getInterfaceArtInfo("ART_DEF_BACKGROUND_" + sType)
			if sNewArt:
				sBackGround = sNewArt.getPath()
		screen.addDDSGFC("ScreenBackground", sBackGround, (screen.getXResolution() - self.W_TEXT_PANEL)/2, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		screen.addScrollPanel("RankTable", "", self.X_HEADER_PANEL + 20, self.Y_TEXT_PANEL, self.W_HEADER_PANEL - 40, self.H_TEXT_PANEL - 25, PanelStyles.PANEL_STYLE_EXTERNAL)
		iY = 0
		iSize = 30
		for iRank in xrange(len(self.RankList)):
			if iRank > len(self.aiTopCivsValues) -1: return
			iPlayerX = self.aiTopCivsValues[iRank][1]
			pPlayerX = gc.getPlayer(iPlayerX)
			pTeamX = gc.getTeam(pPlayerX.getTeam())
			sColor = ""
			sText = CyTranslator().getText("TXT_KEY_TOPCIVS_UNKNOWN", ())
			sCiv = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
			sLeader = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
			if pTeamX.isHasMet(CyGame().getActiveTeam()):
				sColor = u"<color=%d,%d,%d,%d>" %(pPlayerX.getPlayerTextColorR(), pPlayerX.getPlayerTextColorG(), pPlayerX.getPlayerTextColorB(), pPlayerX.getPlayerTextColorA())
				sText = CyTranslator().getText("TXT_KEY_TOPCIVS_TEXT3", (pPlayerX.getName(), self.RankList[iRank]))
				sCiv = gc.getCivilizationInfo(pPlayerX.getCivilizationType()).getButton()
				sLeader = gc.getLeaderHeadInfo(pPlayerX.getLeaderType()).getButton()
			screen.setLabelAt("RankText" + str(iRank), "RankTable", "<font=3>" + sColor + str(iRank + 1) + ")</color></font>", CvUtil.FONT_RIGHT_JUSTIFY, 20, iY + 2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addDDSGFCAt("CivButton" + str(iRank), "RankTable", sCiv, 30, iY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			screen.addDDSGFCAt("LeaderButton" + str(iRank), "RankTable", sLeader, 30 + iSize, iY, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
			screen.setLabelAt("NameText" + str(iRank), "RankTable", "<font=3>" + sColor + sText + "</color></font>", CvUtil.FONT_LEFT_JUSTIFY, 30 + iSize * 2, iY + 2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iY += iSize

	#####################################################################################################################################
	      
	def handleInput( self, inputClass ):
		screen = CyGInterfaceScreen( "CvTopCivs", CvScreenEnums.TOP_CIVS )		
		if inputClass.getData() == int(InputTypes.KB_RETURN):
			screen.hideScreen()
			return 1
		return 0

	def update(self, fDelta):
		return
