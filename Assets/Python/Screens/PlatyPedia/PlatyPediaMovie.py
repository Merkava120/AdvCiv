from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()
bNoMovies = False

class CvPediaMovie:
	def __init__(self, main):
		self.iType = -1
		self.iEntry = -1
		self.top = main
		self.W_EXIT = 100
		self.H_EXIT = 30

	def interfaceScreen(self, iType, iEntry):
		screen = CyGInterfaceScreen( "MoviePlayer", CvScreenEnums.PLATYPEDIA_MOVIE)
		self.iType = iType
		self.iEntry = iEntry
		global bNoMovies
		bNoMovies = CyUserProfile().getGraphicOption(GraphicOptionTypes.GRAPHICOPTION_NO_MOVIES)
		CyUserProfile().setGraphicOption(GraphicOptionTypes.GRAPHICOPTION_NO_MOVIES, False)
		self.W_MOVIE = screen.getXResolution()
		self.H_MOVIE = screen.getXResolution() * 2 / 3
		if self.H_MOVIE > screen.getYResolution():
			self.H_MOVIE = screen.getYResolution()
			self.W_MOVIE = self.H_MOVIE * 3 / 2
		self.X_MOVIE = (screen.getXResolution() - self.W_MOVIE) / 2
		self.Y_MOVIE = (screen.getYResolution() - self.H_MOVIE) / 2
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.addPanel( "MoviePlayerBG", u"", u"", True, False, -10, -10, screen.getXResolution() +20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.enableWorldSounds(False)

		if self.iType == 8201:
			sDescription =gc.getCorporationInfo(iEntry).getDescription()
			self.szMovieFile = gc.getCorporationInfo(self.iEntry).getMovieFile()
		elif self.iType == 7869:
			sDescription =gc.getReligionInfo(iEntry).getDescription()
			self.szMovieFile = gc.getReligionInfo(self.iEntry).getMovieFile()
		elif self.iType == 7870:
			sDescription =gc.getBuildingInfo(iEntry).getDescription()
			self.szMovieFile = gc.getBuildingInfo(self.iEntry).getMovie()
		elif self.iType == 6785:
			sDescription =gc.getProjectInfo(iEntry).getDescription()
			self.szMovieFile = CyArtFileMgr().getMovieArtInfo(gc.getProjectInfo(self.iEntry).getMovieArtDef()).getPath()
		elif self.iType == 6786:
			sDescription =gc.getVictoryInfo(iEntry).getDescription()
			self.szMovieFile = CyArtFileMgr().getMovieArtInfo(gc.getVictoryInfo(self.iEntry).getMovie()).getPath()
		if self.szMovieFile.find(".nif") > -1:
			screen.addReligionMovieWidgetGFC("Movie", self.szMovieFile, self.X_MOVIE, self.Y_MOVIE, self.W_MOVIE, self.H_MOVIE, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.playMovie(self.szMovieFile, -1, -1, -1, -1, 0)
		screen.setLabel("MoviePlayerDescription", "Background", u"<font=4b>" + sDescription.upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, 8, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText("MoviePlayerExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_MOVIE, -1)
		screen.setButtonGFC("MoviePlayerExit", CyTranslator().getText("TXT_KEY_MAIN_MENU_OK", ()), "", screen.getXResolution()/2 - self.W_EXIT/2, screen.getYResolution() - self.H_EXIT - 8, self.W_EXIT , self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER and inputClass.getData() == int(InputTypes.KB_ESCAPE)) or inputClass.getFunctionName() == "MoviePlayerExit":
			CyUserProfile().setGraphicOption(GraphicOptionTypes.GRAPHICOPTION_NO_MOVIES, bNoMovies)
			screen = CyGInterfaceScreen( "MoviePlayer", CvScreenEnums.PLATYPEDIA_MOVIE)
			screen.hideScreen()
			self.top.showScreen(self.top.PLATYPEDIA_MOVIE)
		return 0

	def update(self, fDelta):
		return 1