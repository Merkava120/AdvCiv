from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaLeader:
	def __init__(self, main):
		self.iLeader = -1
		self.top = main

	def interfaceScreen(self, iLeader):
		self.iLeader = iLeader
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()
                
		self.W_LEADERHEAD = screen.getXResolution() *3/10
		self.H_LEADERHEAD = self.W_LEADERHEAD * 6/5
		if self.H_LEADERHEAD > screen.getYResolution()/2:
			self.H_LEADERHEAD = screen.getYResolution()/2
			self.W_LEADERHEAD = self.H_LEADERHEAD * 5/6
		
		self.Y_TRAITS = self.top.Y_ITEMS_PANE + self.H_LEADERHEAD + 20
		self.H_TRAITS = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_TRAITS

		self.W_CIVIC = 150
		self.X_CIVIC = self.top.X_ITEMS_PANE + self.top.W_ITEMS_PANE - self.W_CIVIC
                
		self.X_CIV = self.top.X_ITEMS_PANE + self.W_LEADERHEAD + self.top.W_BORDER
		self.Y_CIV = self.top.Y_ITEMS_PANE - 20
		self.W_CIV = self.X_CIVIC - 20 - self.X_CIV
		self.H_CIV = 110
		
		self.Y_HISTORY = self.Y_CIV + self.H_CIV + 10
		self.W_HISTORY = self.top.W_ITEMS_PANE - self.W_LEADERHEAD - self.top.W_BORDER
		self.H_HISTORY = self.Y_TRAITS - self.Y_HISTORY - 10

		szHeader = gc.getLeaderHeadInfo(self.iLeader).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sLeaderIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sLeaderIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_LEADER, -1)
		self.LeaderWidget = self.top.getNextWidgetName()
		screen.addLeaderheadGFC(self.LeaderWidget, self.iLeader, AttitudeTypes.ATTITUDE_PLEASED, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE + 8, self.W_LEADERHEAD, self.H_LEADERHEAD, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.placeHistory()
		self.placeFavourites()
		self.placeCiv()
		self.placeTraits()
		self.placeStats()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_LEADER and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_LEADER

	def placeStats(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_STATS", ()), "", True, True, self.top.X_ITEMS_PANE, self.Y_TRAITS, self.W_LEADERHEAD, self.H_TRAITS, PanelStyles.PANEL_STYLE_BLUE50)
		Info = gc.getLeaderHeadInfo(self.iLeader)

		szStatsText = CyTranslator().getText("TXT_KEY_PEDIA_WONDER_CONSTRUCTION", (Info.getWonderConstructRand(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_ATTITUDE", (Info.getBaseAttitude(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_WARMONGER_RESPECT", (Info.getWarmongerRespect(),))
		szStatsText += "\n"
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_MAX_WAR", (Info.getMaxWarRand(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_NEARBY_POWER_RATIO", (Info.getMaxWarNearbyPowerRatio(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_DISTANCE_POWER_RATIO", (Info.getMaxWarDistantPowerRatio(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_MIN_ADJACENT_LAND", (Info.getMaxWarMinAdjacentLandPercent(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_LIMITED_WAR", (Info.getLimitedWarRand(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_POWER_RATIO", (Info.getLimitedWarPowerRatio(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_DOGPILE", (Info.getDogpileWarRand(),))
		szStatsText += "\n"
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_PEACE_WEIGHT", (Info.getBasePeaceWeight(), Info.getPeaceWeightRand(),))
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_MAKE_PEACE", (Info.getMakePeaceRand(),))
		szStatsText += "\n"
		szStatsText += CyTranslator().getText("TXT_KEY_PEDIA_ESPIONAGE_WEIGHT", (Info.getEspionageWeight(),))
		
		screen.addMultilineText(self.top.getNextWidgetName(), szStatsText, self.top.X_ITEMS_PANE+5, self.Y_TRAITS+30, self.W_LEADERHEAD-10, self.H_TRAITS-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
													
	def placeCiv(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()), "", False, true, self.X_CIV, self.Y_CIV, self.W_CIV, self.H_CIV, PanelStyles.PANEL_STYLE_BLUE50 )
		for iCiv in xrange(gc.getNumCivilizationInfos()):
			if gc.getCivilizationInfo(iCiv).isLeaders(self.iLeader):
				screen.attachImageButton( panelName, "", gc.getCivilizationInfo(iCiv).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1, False )
													
	def placeTraits(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_TRAITS", ()), "", true, false, self.X_CIV, self.Y_TRAITS, self.W_HISTORY, self.H_TRAITS, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().parseLeaderTraits(self.iLeader, -1, False, True)[1:]
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_CIV+5, self.Y_TRAITS+30, self.W_HISTORY-10, self.H_TRAITS-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
	def placeFavourites(self):		
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_FAVOURITES", ()), "", False, true, self.X_CIVIC, self.Y_CIV, self.W_CIVIC, self.H_CIV, PanelStyles.PANEL_STYLE_BLUE50 )
		iCivic = gc.getLeaderHeadInfo(self.iLeader).getFavoriteCivic()
		if iCivic > -1:
			screen.attachImageButton( panelName, "", gc.getCivicInfo(iCivic).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1, False )
		iReligion = gc.getLeaderHeadInfo(self.iLeader).getFavoriteReligion()
		if iReligion > -1:
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iReligion).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iReligion, 1, False )
	def placeHistory(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, true, self.X_CIV, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = ""
		sStrategy = gc.getLeaderHeadInfo(self.iLeader).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getLeaderHeadInfo(self.iLeader).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_CIV + 10, self.Y_HISTORY + 30, self.W_HISTORY - 20, self.H_HISTORY - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortLeaders(self.top.iSortLeaders)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sLeaderIcon, ()), self.iLeader, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, -1)

	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_0)):
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.LEADERANIM_GREETING)
			elif (inputClass.getData() == int(InputTypes.KB_6)):
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.LEADERANIM_DISAGREE)
			elif (inputClass.getData() == int(InputTypes.KB_7)):
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.LEADERANIM_AGREE)
			elif (inputClass.getData() == int(InputTypes.KB_1)):
				self.top.getScreen().setLeaderheadMood(self.LeaderWidget, AttitudeTypes.ATTITUDE_FRIENDLY)
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_2)):
				self.top.getScreen().setLeaderheadMood(self.LeaderWidget, AttitudeTypes.ATTITUDE_PLEASED)
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_3)):
				self.top.getScreen().setLeaderheadMood(self.LeaderWidget, AttitudeTypes.ATTITUDE_CAUTIOUS)
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_4)):
				self.top.getScreen().setLeaderheadMood(self.LeaderWidget, AttitudeTypes.ATTITUDE_ANNOYED)
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_5)):
				self.top.getScreen().setLeaderheadMood(self.LeaderWidget, AttitudeTypes.ATTITUDE_FURIOUS)
				self.top.getScreen().performLeaderheadAction(self.LeaderWidget, LeaderheadAction.NO_LEADERANIM)
			else:
				self.top.getScreen().leaderheadKeyInput(self.LeaderWidget, inputClass.getData())
		return 0