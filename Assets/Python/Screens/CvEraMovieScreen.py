from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvEraMovieScreen:
	"Wonder Movie Screen"
	def interfaceScreen (self, iEra):
		if CyUserProfile().getGraphicOption(GraphicOptionTypes.GRAPHICOPTION_NO_MOVIES): return
		screen = CyGInterfaceScreen( "EraMovieScreen" + str(iEra), CvScreenEnums.ERA_MOVIE_SCREEN)
		screen.addPanel("EraMoviePanel", "", "", True, False, -10, -10, screen.getXResolution() +20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN)
		screen.setSound("AS2D_NEW_ERA")
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.W_EXIT = 120
		self.H_EXIT = 30
		szHeader = CyTranslator().getText("TXT_KEY_ERA_SPLASH_SCREEN", (gc.getEraInfo(iEra).getTextKey(), ))
		screen.setLabel("EraTitleHeader", "Background", u"<font=4b>" + szHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() /2, 8, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setButtonGFC("EraExit", CyTranslator().getText("TXT_KEY_MAIN_MENU_OK", ()), "", screen.getXResolution()/2 - self.W_EXIT/2, screen.getYResolution() - self.H_EXIT - 8, self.W_EXIT , self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

		self.W_MOVIE = screen.getXResolution()
		self.H_MOVIE = screen.getXResolution() * 2 / 3
		if self.H_MOVIE > (screen.getYResolution() - (self.H_EXIT + 16)*2):
			self.H_MOVIE = screen.getYResolution() - (self.H_EXIT + 16)*2
			self.W_MOVIE = self.H_MOVIE * 3 / 2
		self.X_MOVIE = (screen.getXResolution() - self.W_MOVIE) / 2
		self.Y_MOVIE = (screen.getYResolution() - self.H_MOVIE) / 2
		sType = gc.getEraInfo(iEra).getType()
		szArtDef = CyArtFileMgr().getMovieArtInfo("ART_DEF_MOVIE_" + sType)
		if szArtDef:
			szMovieFile = szArtDef.getPath()
			if szMovieFile.find(".nif") > -1:
				screen.addReligionMovieWidgetGFC("EraMovie", szMovieFile, self.X_MOVIE, self.Y_MOVIE, self.W_MOVIE, self.H_MOVIE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.playMovie(szMovieFile, self.X_MOVIE, self.Y_MOVIE, self.W_MOVIE, self.H_MOVIE, -2.3)

	def handleInput (self, inputClass):
		return 0

	def update(self, fDelta):
		return