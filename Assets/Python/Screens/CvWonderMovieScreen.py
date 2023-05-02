from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import PlatyOptions
gc = CyGlobalContext()

MOVIE_SCREEN_WONDER = 0
MOVIE_SCREEN_RELIGION = 1
MOVIE_SCREEN_PROJECT = 2
MOVIE_SCREEN_CORPORATION = 3
MOVIE_SCREEN_HERO = 4
MOVIE_SCREEN_INTRO = 5

class CvWonderMovieScreen:
	def interfaceScreen (self, iMovieItem, iCityId, iMovieType):
		if CyUserProfile().getGraphicOption(GraphicOptionTypes.GRAPHICOPTION_NO_MOVIES): return
		szMovieFile = None
		self.szHelp = ""

		if iMovieType == MOVIE_SCREEN_PROJECT:
			szArtDef = gc.getProjectInfo(iMovieItem).getMovieArtDef()
			if len(szArtDef):
				szMovieFile = CyArtFileMgr().getMovieArtInfo(szArtDef).getPath()
			szHeader = gc.getProjectInfo(iMovieItem).getDescription()
			self.szHelp = CyGameTextMgr().getProjectHelp(iMovieItem, False, None)
		elif iMovieType == MOVIE_SCREEN_WONDER:
			szMovieFile = gc.getBuildingInfo(iMovieItem).getMovie()
			szHeader = gc.getBuildingInfo(iMovieItem).getDescription()
			self.szHelp = CyGameTextMgr().getBuildingHelp(iMovieItem, False, False, False, None)
		elif iMovieType == MOVIE_SCREEN_RELIGION:
			szMovieFile = gc.getReligionInfo(iMovieItem).getMovieFile()
			szHeader = CyTranslator().getText("TXT_KEY_MISC_REL_FOUNDED_MOVIE", (gc.getReligionInfo(iMovieItem).getTextKey(), ))
			self.szHelp = gc.getReligionInfo(iMovieItem).getCivilopedia()
		elif iMovieType == MOVIE_SCREEN_CORPORATION:
			szMovieFile = gc.getCorporationInfo(iMovieItem).getMovieFile()
			szHeader = CyTranslator().getText("TXT_KEY_MISC_REL_FOUNDED_MOVIE", (gc.getCorporationInfo(iMovieItem).getTextKey(), ))
			self.szHelp = gc.getCorporationInfo(iMovieItem).getCivilopedia()
		elif iMovieType == MOVIE_SCREEN_HERO:
			sType = gc.getUnitInfo(iMovieItem).getType()
			szArtDef = CyArtFileMgr().getMovieArtInfo("ART_DEF_MOVIE_" + sType)
			if szArtDef:
				szMovieFile = szArtDef.getPath()
			szHeader = gc.getUnitInfo(iMovieItem).getDescription()
			self.szHelp = CyGameTextMgr().getUnitHelp(iMovieItem, False, False, False, None)
		elif iMovieType == MOVIE_SCREEN_INTRO:
			sType = gc.getCivilizationInfo(iMovieItem).getType()
			szArtDefSpecific = CyArtFileMgr().getMovieArtInfo("ART_DEF_MOVIE_INTRO_" + sType)
			if szArtDefSpecific:
				szMovieFile = szArtDefSpecific.getPath()
			else:
				szArtDef = CyArtFileMgr().getMovieArtInfo("ART_DEF_MOVIE_INTRO_DEFAULT")
				if szArtDef:
					szMovieFile = szArtDef.getPath()
			szHeader = ""

		if szMovieFile == None: return
		if szMovieFile.find(".") == -1: return
		
		CyInterface().lookAtCityBuilding(iCityId, -1)
		CyInterface().setDirty(InterfaceDirtyBits.SelectionCamera_DIRTY_BIT, True)
		
		screen = CyGInterfaceScreen("WonderMovieScreen", CvScreenEnums.WONDER_MOVIE_SCREEN)
		screen.showWindowBackground(True)
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.enableWorldSounds(False)

		self.W_EXIT = 100
		self.H_EXIT = 30
		self.W_MOVIE = screen.getXResolution()
		self.H_MOVIE = screen.getXResolution() * 2 / 3
		if self.H_MOVIE > screen.getYResolution():
			self.H_MOVIE = screen.getYResolution()
			self.W_MOVIE = self.H_MOVIE * 3 / 2
		if not PlatyOptions.bFullScreenMovie:
			self.H_MOVIE = self.H_MOVIE * 3/4
			self.W_MOVIE = self.W_MOVIE * 3/4
		self.X_MOVIE = (screen.getXResolution() - self.W_MOVIE) / 2
		self.Y_MOVIE = (screen.getYResolution() - self.H_MOVIE) / 2

		screen.addPanel("EraMoviePanel", "", "", True, False, self.X_MOVIE - 20, self.Y_MOVIE - 50, self.W_MOVIE +40, self.H_MOVIE + 100, PanelStyles.PANEL_STYLE_MAIN)

		if szMovieFile.find(".nif") > -1:
			screen.addReligionMovieWidgetGFC("ReligionMovie", szMovieFile, self.X_MOVIE, self.Y_MOVIE, self.W_MOVIE, self.H_MOVIE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			CyInterface().playGeneralSound(gc.getReligionInfo(iMovieItem).getMovieSound())	
		else:
			if iMovieType == MOVIE_SCREEN_INTRO:
				screen.playMovie(szMovieFile, -1, -1, -1, -1, 0)
			else:
				screen.playMovie(szMovieFile, self.X_MOVIE, self.Y_MOVIE, self.W_MOVIE, self.H_MOVIE, 0)
		screen.setLabel("WonderTitleHeader", "Background", u"<font=4b>" + szHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, self.Y_MOVIE - 36, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setButtonGFC("EraExit", CyTranslator().getText("TXT_KEY_MAIN_MENU_OK", ()), "", screen.getXResolution()/2 - self.W_EXIT/2, self.Y_MOVIE + self.H_MOVIE + 8, self.W_EXIT , self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen("WonderMovieScreen", CvScreenEnums.WONDER_MOVIE_SCREEN)
		if len(self.szHelp):
			screen.addPanel("MonkeyPanel", "", "", True, True, self.X_MOVIE + self.W_MOVIE/8 - 10, self.Y_MOVIE + self.W_MOVIE/8, self.W_MOVIE *3 /4 + 20, self.H_MOVIE - self.W_MOVIE/4, PanelStyles.PANEL_STYLE_MAIN_BLACK50)	
			screen.addMultilineText("MonkeyText", self.szHelp, self.X_MOVIE + self.W_MOVIE/8, self.Y_MOVIE + self.W_MOVIE/8 + 10, self.W_MOVIE * 3 /4, self.H_MOVIE - self.W_MOVIE/4 - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		return 0

	def update(self, fDelta):
		return