from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()
lForgetful = []

class Forgetful:
	def __init__(self):
		self.iForgetfulType = 0

	def interfaceScreen(self):
		global lForgetful
		lForgetful = [	[gc.getUnitInfo, gc.getNumUnitInfos()],
				[gc.getBuildingInfo, gc.getNumBuildingInfos()],
				[gc.getPromotionInfo, gc.getNumPromotionInfos()],
				[gc.getTechInfo, gc.getNumTechInfos()],
				[gc.getBonusInfo, gc.getNumBonusInfos()],
				[gc.getTerrainInfo, gc.getNumTerrainInfos()],
				[gc.getFeatureInfo, gc.getNumFeatureInfos()],
				[gc.getImprovementInfo, gc.getNumImprovementInfos()],
				[gc.getSpecialistInfo, gc.getNumSpecialistInfos()],
				[gc.getUnitCombatInfo, gc.getNumUnitCombatInfos()],
				[gc.getCivilizationInfo, gc.getNumCivilizationInfos()],
				[gc.getLeaderHeadInfo, gc.getNumLeaderHeadInfos()],
				[gc.getReligionInfo, gc.getNumReligionInfos()],
				[gc.getCorporationInfo, gc.getNumCorporationInfos()],
				[gc.getCivicInfo, gc.getNumCivicInfos()],
				[gc.getProjectInfo, gc.getNumProjectInfos()],
				[gc.getProcessInfo, gc.getNumProcessInfos()],
				[gc.getTraitInfo, gc.getNumTraitInfos()],
				[gc.getRouteInfo, gc.getNumRouteInfos()],
				[gc.getEraInfo, gc.getNumEraInfos()],
				[gc.getUpkeepInfo, gc.getNumUpkeepInfos()],
				[gc.getCultureLevelInfo, gc.getNumCultureLevelInfos()],
				[gc.getGameSpeedInfo, gc.getNumGameSpeedInfos()],
				[gc.getWorldInfo, gc.getNumWorldInfos()],
				[gc.getClimateInfo, gc.getNumClimateInfos()],
				[gc.getHandicapInfo, gc.getNumHandicapInfos()],
				[gc.getVoteSourceInfo, gc.getNumVoteSourceInfos()],
				[gc.getBuildInfo, gc.getNumBuildInfos()],
				[gc.getCalendarInfo, gc.getNumCalendarInfos()],
				[gc.getCivicOptionInfo, gc.getNumCivicOptionInfos()],
				[gc.getCommandInfo, gc.getNumCommandInfos()],
				[gc.getConceptInfo, gc.getNumConceptInfos()],
				[gc.getControlInfo, gc.getNumControlInfos()],
				[gc.getDenialInfo, gc.getNumDenialInfos()],
				[gc.getEffectInfo, gc.getNumEffectInfos()],
				[gc.getEmphasizeInfo, gc.getNumEmphasizeInfos()],
				[gc.getEspionageMissionInfo, gc.getNumEspionageMissionInfos()],
				[gc.getEventInfo, gc.getNumEventInfos()],
				[gc.getEventTriggerInfo, gc.getNumEventTriggerInfos()],
				[gc.getGameOptionInfo, gc.getNumGameOptionInfos()],
				[gc.getGoodyInfo, gc.getNumGoodyInfos()],
				[gc.getHurryInfo, gc.getNumHurryInfos()],
				[gc.getMPOptionInfo, gc.getNumMPOptionInfos()],
				[gc.getMissionInfo, gc.getNumMissionInfos()],
				[gc.getNewConceptInfo, gc.getNumNewConceptInfos()],
				[gc.getSeaLevelInfo, gc.getNumSeaLevelInfos()],
				[gc.getSeasonInfo, gc.getNumSeasonInfos()],
				[gc.getSpecialBuildingInfo, gc.getNumSpecialBuildingInfos()],
				[gc.getSpecialUnitInfo, gc.getNumSpecialUnitInfos()],
				[gc.getVictoryInfo, gc.getNumVictoryInfos()],
				[gc.getVoteInfo, gc.getNumVoteInfos()],
				[gc.getBuildingClassInfo, gc.getNumBuildingClassInfos()],
				[gc.getUnitClassInfo, gc.getNumUnitClassInfos()],
				[gc.getGraphicOptionsInfo, GraphicOptionTypes.NUM_GRAPHICOPTION_TYPES],
				[gc.getCommerceInfo, CommerceTypes.NUM_COMMERCE_TYPES],
				[gc.getYieldInfo, YieldTypes.NUM_YIELD_TYPES],
				[gc.getDomainInfo, DomainTypes.NUM_DOMAIN_TYPES],
				[gc.getMemoryInfo, MemoryTypes.NUM_MEMORY_TYPES],
				[gc.getUnitAIInfo, UnitAITypes.NUM_UNITAI_TYPES],
				]
		for i in xrange(len(lForgetful)):
			sName = str(lForgetful[i][0])
			sName = sName[sName.find("get") + 3:]
			sName = sName[:sName.find("Info")]
			lForgetful[i] = [sName] + lForgetful[i]
		lForgetful.sort()

		screen = CyGInterfaceScreen("ForgetfulScreen", CvScreenEnums.FORGETFUL_SCREEN)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setLabel("ForgetfulHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_XML_TAGS", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText("ForgetfulExit", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 25, screen.getYResolution() - 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		szDropdownName = "ForgetfulType"
		screen.addDropDownBoxGFC(szDropdownName, 20, 20, 180, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i in xrange(len(lForgetful)):
			screen.addPullDownString(szDropdownName, CyTranslator().getText(lForgetful[i][0], ()), i, i, i == self.iForgetfulType)
		self.drawTable("ForgetfulTable")

	def drawTable(self, Table):
		global lForgetful

		screen = CyGInterfaceScreen("ForgetfulScreen", CvScreenEnums.FORGETFUL_SCREEN)
		iWidth = screen.getXResolution() - 40
		iHeight = screen.getYResolution() - 100
		screen.addTableControlGFC(Table, 4, 20, 60, iWidth, iHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader(Table, 0, "ID", 50)
		screen.setTableColumnHeader(Table, 1, CyTranslator().getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()).upper(), 250)
		screen.setTableColumnHeader(Table, 2, "TYPE", (iWidth - 300)/2)
		screen.setTableColumnHeader(Table, 3, "TEXT", (iWidth - 300)/2)
		screen.enableSort("ForgetfulTable")
		for item in xrange(lForgetful[self.iForgetfulType][2]):
			ItemInfo = lForgetful[self.iForgetfulType][1](item)
			screen.appendTableRow(Table)
			screen.setTableInt(Table, 0, item, "<font=2>" + str(item) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(Table, 1, item, "<font=2>" + ItemInfo.getDescription() + "</font>", ItemInfo.getButton(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(Table, 2, item, "<font=1>" + ItemInfo.getType() + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText(Table, 3, item, "<font=1>" + ItemInfo.getTextKey() + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def handleInput (self, inputClass):
		if inputClass.getFunctionName() == "ForgetfulType":
			self.iForgetfulType = int(inputClass.getData())
			self.drawTable("ForgetfulTable")
		return 0

	def update(self, fDelta):
		return 1