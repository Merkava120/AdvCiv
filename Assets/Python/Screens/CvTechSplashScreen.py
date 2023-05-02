from CvPythonExtensions import *
import CvUtil
import ScreenInput
import string
gc = CyGlobalContext()

class CvTechSplashScreen:
	def __init__(self, iScreenID):
		self.nScreenId = iScreenID
		self.iTech = -1
		self.SCREEN_NAME = "TechSplashScreen"
		self.Z_BACKGROUND = -1.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2		
		self.Z_HELP_AREA = self.Z_CONTROLS - 2
		
		self.iMarginSpace = 15
		
	def interfaceScreen(self, iTech):
		self.iTech = iTech		
		screen = self.getScreen()
		techInfo = gc.getTechInfo(self.iTech)
		
		self.W_MAIN_PANEL = screen.getXResolution() * 3/4
		self.X_MAIN_PANEL = (screen.getXResolution() - self.W_MAIN_PANEL) /2
		self.H_MAIN_PANEL = 500
		self.Y_MAIN_PANEL = (screen.getYResolution() - self.H_MAIN_PANEL)/2
		
		self.X_UPPER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_UPPER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_UPPER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_UPPER_PANEL = 200
		
		self.X_TITLE = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2)
		self.Y_TITLE = self.Y_UPPER_PANEL + 12
		
		self.iButtonWidth = 64
		self.X_ICON = self.X_UPPER_PANEL + 56
		self.Y_ICON = self.Y_UPPER_PANEL + (self.H_UPPER_PANEL / 2) - (self.iButtonWidth / 2) + 17
		
		self.X_ICON_PANEL = self.X_UPPER_PANEL + self.iMarginSpace + 2
		self.Y_ICON_PANEL = self.Y_UPPER_PANEL + self.iMarginSpace + 33
		self.W_ICON_PANEL = 140
		self.H_ICON_PANEL = 135
		
		self.X_QUOTE = self.X_ICON_PANEL + self.W_ICON_PANEL
		self.Y_QUOTE = self.Y_UPPER_PANEL + self.iMarginSpace + 36
		self.W_QUOTE = self.W_UPPER_PANEL - self.X_QUOTE
		self.H_QUOTE = self.H_UPPER_PANEL - (self.iMarginSpace * 2) - 38
		
		self.X_EXIT = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2) - 55
		self.Y_EXIT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL - 45
		self.W_EXIT = 120
		self.H_EXIT = 30
		
		self.X_LOWER_PANEL = self.X_UPPER_PANEL
		self.Y_LOWER_PANEL = self.Y_UPPER_PANEL + self.H_UPPER_PANEL
		self.W_LOWER_PANEL = self.W_UPPER_PANEL
		self.H_LOWER_PANEL = self.Y_EXIT - self.Y_LOWER_PANEL - self.iMarginSpace

		self.H_ALLOWS_PANEL = 80
		self.X_LEADTO_PANEL = self.X_LOWER_PANEL + self.iMarginSpace * 2
		self.Y_LEADTO_PANEL = self.Y_LOWER_PANEL + self.iMarginSpace * 2
		self.W_LEADTO_PANEL = self.W_LOWER_PANEL/3 - self.iMarginSpace * 2
		self.X_OBSOLETE_PANEL = self.X_LEADTO_PANEL + self.W_LEADTO_PANEL + self.iMarginSpace
		self.X_SPECIAL_PANEL = self.X_OBSOLETE_PANEL + self.W_LEADTO_PANEL + self.iMarginSpace
		self.Y_ALLOWS_PANEL = self.Y_LEADTO_PANEL + self.H_ALLOWS_PANEL + 20
		self.W_ALLOWS_PANEL = self.W_LOWER_PANEL - self.iMarginSpace * 4
		
		screen.setSound(techInfo.getSound())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.enableWorldSounds( false )
	
		screen.showWindowBackground( False )
		
		# Create panels
		
		# Main Panel
		szMainPanel = "TechSplashMainPanel"
		screen.addPanel( szMainPanel, "", "", true, true, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		
		# Top Panel
		szHeaderPanel = "TechSplashHeaderPanel"
		screen.addPanel( szHeaderPanel, "", "", true, true, self.X_UPPER_PANEL, self.Y_UPPER_PANEL, self.W_UPPER_PANEL, self.H_UPPER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		screen.setStyle(szHeaderPanel, "Panel_DawnBottom_Style")
		
		# Icon Panel
		szIconPanel = "IconPanel"
		screen.addPanel( szIconPanel, "", "", true, true, self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_UPPER_PANEL-(self.iMarginSpace * 2), self.H_UPPER_PANEL-(self.iMarginSpace * 4), PanelStyles.PANEL_STYLE_MAIN_TAN15 )
		screen.setStyle(szIconPanel, "Panel_TechDiscover_Style")
		
		# Icon Panel
		szIconPanel = "IconPanelGlow"
		screen.addPanel( szIconPanel, "", "", true, true, self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_ICON_PANEL, self.H_ICON_PANEL, PanelStyles.PANEL_STYLE_MAIN_TAN15 )
		screen.setStyle(szIconPanel, "Panel_TechDiscoverGlow_Style")
		
		# Bottom Panel
		szTextPanel = "TechSplashTextPanel"
		screen.addPanel( szTextPanel, "", "", true, true, self.X_LOWER_PANEL+self.iMarginSpace, self.Y_LOWER_PANEL, self.W_LOWER_PANEL-(self.iMarginSpace * 2), self.H_LOWER_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		screen.setStyle(szTextPanel, "Panel_TanT_Style")
		
		# Exit Button
		screen.setButtonGFC("Exit", CyTranslator().getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT , self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
		szLeadsToPanel = "LeadsToPanel"
		screen.addPanel( szLeadsToPanel, "", "", False, True, self.X_LEADTO_PANEL, self.Y_LEADTO_PANEL, self.W_LEADTO_PANEL, self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(szLeadsToPanel, "Panel_Black25_Style")
		szText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_LEADS_TO", ()) + u"</font>"
		screen.setText("LeadsToTitle", "", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_LEADTO_PANEL, self.Y_LEADTO_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		szObsoletePanel = "ObsoletePanel"
		screen.addPanel(szObsoletePanel, "", "", false, true, self.X_OBSOLETE_PANEL, self.Y_LEADTO_PANEL, self.W_LEADTO_PANEL, self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(szObsoletePanel, "Panel_Black25_Style")
		sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_OBSOLETE", ()) + u"</font>"
		screen.setText("ObsoleteTitle", "", sText, CvUtil.FONT_LEFT_JUSTIFY, self.X_OBSOLETE_PANEL, self.Y_LEADTO_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Special Panel
		szSpecialPanel = "TechSplashSpecialPanel"
		screen.addPanel( szSpecialPanel, "", "", False, True, self.X_SPECIAL_PANEL, self.Y_LEADTO_PANEL, self.W_LEADTO_PANEL, self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(szSpecialPanel, "Panel_Black25_Style")
		szSpecialTitle = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u"</font>"
		screen.setText("SpecialTitle", "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY, self.X_SPECIAL_PANEL, self.Y_LEADTO_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Allows Panel
		szAllowsPanel = "TechSplashAllowsPanel"
		screen.addPanel(szAllowsPanel, "", "", false, true, self.X_LEADTO_PANEL, self.Y_ALLOWS_PANEL, self.W_ALLOWS_PANEL, self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(szAllowsPanel, "Panel_Black25_Style")
		szAllowsTitleDesc = u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_ALLOWS", ()) + u"</font>"
		screen.setText("AllowsTitle", "", szAllowsTitleDesc, CvUtil.FONT_LEFT_JUSTIFY, self.X_LEADTO_PANEL, self.Y_ALLOWS_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
		# Title
		screen.setLabel("TechSplashTitle", "Background", u"<font=4>" + techInfo.getDescription().upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Tech Icon
		screen.addDDSGFC("TechSplashIcon", techInfo.getButton(), self.X_ICON, self.Y_ICON, self.iButtonWidth, self.iButtonWidth, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, self.iTech, -1 )
		
		# Tech Quote
		if techInfo.getQuote():
			szQuotePanel = "TechSplashQuotePanel"		
			screen.addMultilineText( "Text", techInfo.getQuote(), self.X_QUOTE, self.Y_QUOTE + self.iMarginSpace*2, self.W_QUOTE - (self.iMarginSpace * 2), self.H_QUOTE - (self.iMarginSpace * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		for j in xrange(gc.getNumTechInfos()):
			for k in xrange(gc.getNUM_OR_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqOrTechs(k)
				if iPrereq == self.iTech:
        					screen.attachImageButton(szLeadsToPanel, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )
			for k in xrange(gc.getNUM_AND_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqAndTechs(k)
				if iPrereq == self.iTech:
        					screen.attachImageButton(szLeadsToPanel, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )
		
		for j in xrange( gc.getNumUnitClassInfos() ):
			eLoopUnit = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(j)
			if eLoopUnit > -1:
				if isTechRequiredForUnit(self.iTech, eLoopUnit):
	        			screen.attachImageButton(szAllowsPanel, "", gc.getActivePlayer().getUnitButton(eLoopUnit), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )
		
		for j in xrange(gc.getNumBuildingClassInfos()):
			eLoopBuilding = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationBuildings(j)
			if eLoopBuilding > -1:
				if isTechRequiredForBuilding(self.iTech, eLoopBuilding):
	        				screen.attachImageButton(szAllowsPanel, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )
				elif gc.getBuildingInfo(eLoopBuilding).getObsoleteTech() == self.iTech:
					screen.attachImageButton(szObsoletePanel, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, 1, False)
				eSpecial = gc.getBuildingInfo(eLoopBuilding).getSpecialBuildingType()
				if eSpecial > -1:
					if gc.getSpecialBuildingInfo(eSpecial).getObsoleteTech() == self.iTech:
						screen.attachImageButton(szObsoletePanel, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, 1, False)

		for j in xrange(gc.getNumProjectInfos()):
			if isTechRequiredForProject(self.iTech, j):
				screen.attachImageButton(szAllowsPanel, "", gc.getProjectInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )

		for j in xrange( gc.getNumCivicInfos() ):
			if gc.getCivicInfo(j).getTechPrereq() == self.iTech:
				screen.attachImageButton(szAllowsPanel, "", gc.getCivicInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, j, 1, False )

		for j in xrange(gc.getNumBonusInfos()):
			if gc.getBonusInfo(j).getTechReveal() == self.iTech:
				screen.attachImageButton(szSpecialPanel, "", gc.getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, self.iTech, j, False )
			elif gc.getBonusInfo(j).getTechObsolete() == self.iTech:
				screen.attachImageButton(szObsoletePanel, "", gc.getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, 1, False )

		for j in xrange(gc.getNumPromotionInfos()):
			if gc.getPromotionInfo(j).getTechPrereq() == self.iTech:
				screen.attachImageButton(szAllowsPanel, "", gc.getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, -1, False )

		for j in xrange( gc.getNumProcessInfos() ):
			if gc.getProcessInfo(j).getTechPrereq() == self.iTech:
				screen.attachImageButton(szAllowsPanel, "", gc.getProcessInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_PROCESS_INFO, self.iTech, j, False )

		for j in xrange(gc.getNumBuildInfos()):
			bTechFound = False
			if gc.getBuildInfo(j).getTechPrereq() == self.iTech:
				bTechFound = True
			elif gc.getBuildInfo(j).getTechPrereq() == -1:
				for k in xrange(gc.getNumFeatureInfos()):
					if gc.getBuildInfo(j).getFeatureTech(k) == self.iTech:
						bTechFound = True
						break
			if bTechFound:
				screen.attachImageButton(szSpecialPanel, "", gc.getBuildInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IMPROVEMENT, self.iTech, j, False )

		if gc.getTechInfo(self.iTech).getFirstFreeUnitClass() != UnitClassTypes.NO_UNITCLASS:
			eLoopUnit = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(gc.getTechInfo(self.iTech).getFirstFreeUnitClass())
			if eLoopUnit > -1:
				screen.attachImageButton(szSpecialPanel, "", gc.getPlayer(CyGame().getActivePlayer()).getUnitButton(eLoopUnit), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FREE_UNIT, eLoopUnit, self.iTech, False )

		if gc.getTechInfo(self.iTech).getFeatureProductionModifier() != 0:
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, self.iTech, -1, False )

		for j in xrange(gc.getNumRouteInfos()):
			if ( gc.getRouteInfo(j).getTechMovementChange(self.iTech) != 0 ):
				screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MOVE_BONUS, self.iTech, -1, False )
			
		if gc.getTechInfo(self.iTech).getWorkerSpeedModifier() != 0:
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_WORKER_RATE, self.iTech, -1, False )
			
		if gc.getTechInfo(self.iTech).getTradeRoutes() != 0:
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, self.iTech, -1, False )
			
		if gc.getTechInfo(self.iTech).getHealth() != 0:
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_HEALTH_RATE, self.iTech, -1, False )
	
		if gc.getTechInfo(self.iTech).getHappiness() != 0:
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, self.iTech, -1, False )
		
		if gc.getTechInfo(self.iTech).getFirstFreeTechs() > 0:
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FREE_TECH, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isExtraWaterSeeFrom():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_LOS_BONUS, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isMapCentering():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MAP_CENTER, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isMapVisible():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MAP_REVEAL, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isMapTrading():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_MAP_TRADE, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isTechTrading():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TECH_TRADE, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isGoldTrading():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_GOLD_TRADE, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isOpenBordersTrading():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isDefensivePactTrading():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isPermanentAllianceTrading():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isVassalStateTrading():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_VASSAL_STATE, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isBridgeBuilding():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isIrrigation():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IRRIGATION, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isIgnoreIrrigation():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, self.iTech, -1, False )

		if gc.getTechInfo(self.iTech).isWaterWork():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_WATER_WORK, self.iTech, -1, False )

		for j in xrange( DomainTypes.NUM_DOMAIN_TYPES ):
			if gc.getTechInfo(self.iTech).getDomainExtraMoves(j) != 0:
				screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, self.iTech, j, False )

		for j in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
			if gc.getTechInfo(self.iTech).isCommerceFlexible(j):
				if ( j == CommerceTypes.COMMERCE_CULTURE ):
					szFileName = "Art/Interface/Buttons/Process/ProcessCulture.dds"
				elif ( j == CommerceTypes.COMMERCE_ESPIONAGE ):
					szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath()
				else:
					szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
				screen.attachImageButton(szSpecialPanel, "", szFileName, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_ADJUST, self.iTech, j, False )

		for j in xrange( gc.getNumTerrainInfos() ):
			if gc.getTechInfo(self.iTech).isTerrainTrade(j):
				screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, self.iTech, j, False )

		if gc.getTechInfo(self.iTech).isRiverTrade():
			screen.attachImageButton(szSpecialPanel, "", CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, self.iTech, gc.getNumTerrainInfos(), False )

		for j in xrange( gc.getNumImprovementInfos() ):
			for k in xrange( YieldTypes.NUM_YIELD_TYPES ):
				if (gc.getImprovementInfo(j).getTechYieldChanges(self.iTech, k)):
					screen.attachImageButton(szSpecialPanel, "", gc.getImprovementInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, self.iTech, j, False )

		for j in xrange( gc.getNumReligionInfos() ):
			if gc.getReligionInfo(j).getTechPrereq() == self.iTech:
				screen.attachImageButton(szSpecialPanel, "", gc.getReligionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, self.iTech, j, False )
			
		for j in xrange( gc.getNumCorporationInfos() ):
			if gc.getCorporationInfo(j).getTechPrereq() == self.iTech:
				screen.attachImageButton(szSpecialPanel, "", gc.getCorporationInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, self.iTech, j, False )
		
	def getScreen(self):
		screen = CyGInterfaceScreen(self.SCREEN_NAME + str(self.iTech), self.nScreenId)
		return screen

	def handleInput( self, inputClass ):
		if inputClass.getData() == int(InputTypes.KB_RETURN):
			self.getScreen().hideScreen()
			return 1
		return 0
		
	def update(self, fDelta):
		return