from CvPythonExtensions import *
import CvUtil
import ScreenInput
gc = CyGlobalContext()

TEXTURE_SIZE = 24
X_START = 6
X_INCREMENT = TEXTURE_SIZE + X_START /2
Y_ROW = 32
PIXEL_INCREMENT = 7
BOX_WIDTH = 0
BOX_HEIGHT = TEXTURE_SIZE * 3
BOX_Y_SPACING = -10		## Min Vertical Panel Spacing
BOX_X_SPACING = X_INCREMENT * 3

class CvPediaTechTree:
	def __init__(self, main):
		self.top = main
		self.TechBenefits = {}
		self.Advisors = ["[ICON_STRENGTH]", "[ICON_RELIGION]", "[ICON_GOLD]", "[ICON_RESEARCH]", "[ICON_CULTURE]", "[ICON_FOOD]"]

	def updateBenefits(self, iCivilization):
		self.TechBenefits = {}

		for iTech in xrange(gc.getNumTechInfos()):
			self.TechBenefits[iTech] = []
			Info = gc.getTechInfo(iTech)
			for j in xrange(gc.getNumRouteInfos()):
				if gc.getRouteInfo(j).getTechMovementChange(iTech) != 0:
					self.TechBenefits[iTech].append(["RouteChange", j])
			if Info.getFirstFreeUnitClass() > -1:
				if iCivilization == -1:
					iItem = gc.getUnitClassInfo(Info.getFirstFreeUnitClass()).getDefaultUnitIndex()
				else:
					iItem = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(Info.getFirstFreeUnitClass())
				if iItem > -1:
					self.TechBenefits[iTech].append(["FreeUnit", iItem])
			if Info.getFeatureProductionModifier():
				self.TechBenefits[iTech].append(["FeatureProduction", -1])
			if Info.getWorkerSpeedModifier():
				self.TechBenefits[iTech].append(["WorkerSpeed", -1])
			if Info.getTradeRoutes():
				self.TechBenefits[iTech].append(["TradeRoute", -1])
			if Info.getHealth():
				self.TechBenefits[iTech].append(["Health", -1])
			if Info.getHappiness():
				self.TechBenefits[iTech].append(["Happiness", -1])
			if Info.getFirstFreeTechs():
				self.TechBenefits[iTech].append(["FreeTech", -1])
			if Info.isExtraWaterSeeFrom():
				self.TechBenefits[iTech].append(["WaterSight", -1])
			if Info.isMapCentering():
				self.TechBenefits[iTech].append(["MapCentering", -1])
			if Info.isMapVisible():
				self.TechBenefits[iTech].append(["MapVisible", -1])
			if Info.isMapTrading():
				self.TechBenefits[iTech].append(["MapTrading", -1])
			if Info.isTechTrading():
				self.TechBenefits[iTech].append(["TechTrading", -1])
			if Info.isGoldTrading():
				self.TechBenefits[iTech].append(["GoldTrading", -1])
			if Info.isOpenBordersTrading():
				self.TechBenefits[iTech].append(["OpenBorders", -1])
			if Info.isDefensivePactTrading():
				self.TechBenefits[iTech].append(["DefensivePact", -1])
			if Info.isPermanentAllianceTrading():
				self.TechBenefits[iTech].append(["PermanentAlliance", -1])
			if Info.isVassalStateTrading():
				self.TechBenefits[iTech].append(["VassalState", -1])
			if Info.isBridgeBuilding():
				self.TechBenefits[iTech].append(["BridgeBuilding", -1])
			if Info.isIrrigation():
				self.TechBenefits[iTech].append(["EnablesIrrigation", -1])
			if Info.isIgnoreIrrigation():
				self.TechBenefits[iTech].append(["IgnoreIrrigation", -1])
			if Info.isWaterWork():
				self.TechBenefits[iTech].append(["WaterWork", -1])
			for j in xrange(DomainTypes.NUM_DOMAIN_TYPES):
				if Info.getDomainExtraMoves(j):
					self.TechBenefits[iTech].append(["DomainMoves", j])
			for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				if Info.isCommerceFlexible(j):
					self.TechBenefits[iTech].append(["CommerceFlexible", j])
			for j in xrange(gc.getNumTerrainInfos()):
				if Info.isTerrainTrade(j):
					self.TechBenefits[iTech].append(["TerrainTrade", j])
			if Info.isRiverTrade():
				self.TechBenefits[iTech].append(["RiverTrade", -1])
			for j in xrange(gc.getNumImprovementInfos()):
				for k in xrange(YieldTypes.NUM_YIELD_TYPES):
					if gc.getImprovementInfo(j).getTechYieldChanges(iTech, k):
						self.TechBenefits[iTech].append(["ImprovementYield", j])
						break
			if Info.getHelp():
				self.TechBenefits[iTech].append(["TechHelp", -1])

		for j in xrange(gc.getNumUnitClassInfos()):
			if iCivilization == -1:
				iItem = gc.getUnitClassInfo(j).getDefaultUnitIndex()
			else:
				iItem = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(j)
			if iItem > -1:
				iTech = gc.getUnitInfo(iItem).getPrereqAndTech()
				if iTech > -1:
					self.TechBenefits[iTech].append(["UnlockUnit", iItem])

		for j in xrange(gc.getNumBuildingClassInfos()):
			if iCivilization == -1:
				iItem = gc.getBuildingClassInfo(j).getDefaultBuildingIndex()
			else:
				iItem = gc.getCivilizationInfo(iCivilization).getCivilizationBuildings(j)
			if iItem > -1:
				iTech = gc.getBuildingInfo(iItem).getPrereqAndTech()
				if iTech > -1:
					self.TechBenefits[iTech].append(["UnlockBuilding", iItem])
				iTech = gc.getBuildingInfo(iItem).getObsoleteTech()
				if iTech > -1:
					self.TechBenefits[iTech].append(["ObsoleteBuilding", iItem])

		for j in xrange(gc.getNumSpecialBuildingInfos()):
			iTech = gc.getSpecialBuildingInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockSpecialBuilding", j])
			iTech = gc.getSpecialBuildingInfo(j).getObsoleteTech()
			if iTech > -1:
				self.TechBenefits[iTech].append(["ObsoleteSpecialBuilding", j])

		for j in xrange(gc.getNumBonusInfos()):
			iTech = gc.getBonusInfo(j).getTechReveal()
			if iTech > -1:
				self.TechBenefits[iTech].append(["RevealBonus", j])
			iTech = gc.getBonusInfo(j).getTechObsolete()
			if iTech > -1:
				self.TechBenefits[iTech].append(["ObsoleteBonus", j])

		for j in xrange(gc.getNumPromotionInfos()):
			iTech = gc.getPromotionInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockPromotion", j])

		for j in xrange(gc.getNumBuildInfos()):
			bTechFound = False
			iTech = gc.getBuildInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockImprovement", j])
			else:
				for k in xrange(gc.getNumFeatureInfos()):
					iTech = gc.getBuildInfo(j).getFeatureTech(k)
					if iTech > -1:
						self.TechBenefits[iTech].append(["UnlockImprovement", j])
						break

		for j in xrange(gc.getNumCivicInfos()):
			iTech = gc.getCivicInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockCivic", j])

		for j in xrange(gc.getNumProjectInfos()):
			iTech = gc.getProjectInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockProject", j])

		for j in xrange(gc.getNumProcessInfos()):
			iTech = gc.getProcessInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockProcess", j])

		for j in xrange(gc.getNumReligionInfos()):
			iTech = gc.getReligionInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockReligion", j])
			
		for j in xrange(gc.getNumCorporationInfos()):
			iTech = gc.getCorporationInfo(j).getTechPrereq()
			if iTech > -1:
				self.TechBenefits[iTech].append(["UnlockCorporation", j])

		global BOX_WIDTH
		iMax = 0
		for iTech in xrange(gc.getNumTechInfos()):
			iMax = max(iMax, len(self.TechBenefits[iTech]))
		iMax += 2
		BOX_WIDTH = PIXEL_INCREMENT * 3 + (X_INCREMENT * iMax)

	def interfaceScreen(self):
		screen = self.top.getScreen()
		iCivilization = CyGame().getActiveCivilizationType()
		if not self.TechBenefits:
			self.updateBenefits(iCivilization)

		iMaxY = 1
		for i in xrange(gc.getNumTechInfos()):
			iMaxY = max(iMaxY, gc.getTechInfo(i).getGridY())

		global BOX_Y_SPACING
		iHeight = self.top.H_ITEMS_PANE + self.top.W_BORDER/2
		iEmptySpace = iHeight - 12 - int((iMaxY + 1) * BOX_HEIGHT * 0.5)
		iNumBoxSpace = (iMaxY + 1)/2 - 1
		BOX_Y_SPACING = max(BOX_Y_SPACING, iEmptySpace/iNumBoxSpace)

		ARROW_X = CyArtFileMgr().getInterfaceArtInfo("ARROW_X").getPath()
		ARROW_Y = CyArtFileMgr().getInterfaceArtInfo("ARROW_Y").getPath()
		ARROW_MXMY = CyArtFileMgr().getInterfaceArtInfo("ARROW_MXMY").getPath()
		ARROW_XY = CyArtFileMgr().getInterfaceArtInfo("ARROW_XY").getPath()
		ARROW_MXY = CyArtFileMgr().getInterfaceArtInfo("ARROW_MXY").getPath()
		ARROW_XMY = CyArtFileMgr().getInterfaceArtInfo("ARROW_XMY").getPath()
		ARROW_HEAD = CyArtFileMgr().getInterfaceArtInfo("ARROW_HEAD").getPath()
			
		for i in xrange(gc.getNumTechInfos()):
			Info = gc.getTechInfo(i)
			iX = (Info.getGridX() -1) * (BOX_X_SPACING + BOX_WIDTH)
			iY = (Info.getGridY() -1) * (BOX_HEIGHT + BOX_Y_SPACING)/2
			szTechRecord = "TechRecord" + str(i)
			screen.attachPanelAt(self.top.UPGRADES_GRAPH_ID, szTechRecord, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX,  iY, BOX_WIDTH, BOX_HEIGHT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, i, -1 )
			screen.setActivation(szTechRecord, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
			iColor = Info.getEra() * 255 / gc.getNumEraInfos()
			screen.setPanelColor(szTechRecord, iColor*5, (255 - iColor)/2, iColor)
			iX = 6
			iY = 6
			szTechID = "TechID" + str(i)
			szTechString = "<font=1>"
			iAdjustment = 6
			iAdvisor = Info.getAdvisorType()
			if iAdvisor > -1:
				szTechString += CyTranslator().getText(self.Advisors[iAdvisor], ())
				iAdjustment = 3
			szTechString += Info.getDescription() + "</font>"
			screen.setLabelAt(szTechID, szTechRecord, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + iAdjustment + (X_INCREMENT * 2), iY + 6, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, i, -1)
			screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
			szTechButtonID = "TechButtonID" + str(i)
			screen.addDDSGFCAt( szTechButtonID, szTechRecord, Info.getButton(), iX + 6, iY + 6, TEXTURE_SIZE + X_INCREMENT, TEXTURE_SIZE + X_INCREMENT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, i, -1, False )
			fX = X_START + (X_INCREMENT * 2)

			for j in xrange(len(self.TechBenefits[i])):
				sType = self.TechBenefits[i][j][0]
				iItem = self.TechBenefits[i][j][1]
				sButton = "Item" + str(i * 1000 + j)
				sObsolete = "Obsolete" + str(i * 1000 + j)
				if sType == "UnlockUnit":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getUnitInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iItem, 1, True)
				elif sType == "UnlockBuilding":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getBuildingInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iItem, 1, True )
				elif sType == "ObsoleteBuilding":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getBuildingInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, iItem, -1, False )
					screen.addDDSGFCAt(sObsolete, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, iItem, -1, False)
				elif sType == "UnlockSpecialBuilding":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getSpecialBuildingInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, i, iItem, False)
				elif sType == "ObsoleteSpecialBuilding":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getSpecialBuildingInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, i, iItem, False)
					screen.addDDSGFCAt(sObsolete, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, iItem, -1, False)
				elif sType == "RevealBonus":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getBonusInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, i, iItem, False)
				elif sType == "ObsoleteBonus":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getBonusInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, i, iItem, False)
					screen.addDDSGFCAt(sObsolete, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, iItem, -1, False)
				elif sType == "RouteChange":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MOVE_BONUS, i, -1, False)
				elif sType == "UnlockPromotion":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getPromotionInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iItem, -1, False)
				elif sType == "FreeUnit":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getUnitInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_UNIT, iItem, i, False)
				elif sType == "FeatureProduction":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, i, -1, False)
				elif sType == "WorkerSpeed":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WORKER_SPEED").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WORKER_RATE, i, -1, False)
				elif sType == "TradeRoute":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, i, -1, False)
				elif sType == "Health":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HEALTH_RATE, i, -1, False)
				elif sType == "Happiness":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, i, -1, False)
				elif sType == "FreeTech":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_TECH, i, -1, False)
				elif sType == "WaterSight":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_LOS_BONUS, i, -1, False)
				elif sType == "MapCentering":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_CENTER, i, -1, False)
				elif sType == "MapVisible":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_REVEAL, i, -1, False)
				elif sType == "MapTrading":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_TRADE, i, -1, False)
				elif sType == "TechTrading":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_TRADE, i, -1, False)
				elif sType == "GoldTrading":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_GOLD_TRADE, i, -1, False)
				elif sType == "OpenBorders":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, i, -1, False)
				elif sType == "DefensivePact":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, i, -1, False)
				elif sType == "PermanentAlliance":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, i, -1, False)
				elif sType == "VassalState":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_VASSAL_STATE, i, -1, False)
				elif sType == "BridgeBuilding":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, i, -1, False)
				elif sType == "EnablesIrrigation":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IRRIGATION, i, -1, False)
				elif sType == "IgnoreIrrigation":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, i, -1, False)
				elif sType == "WaterWork":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WATER_WORK, i, -1, False)
				elif sType == "UnlockImprovement":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getBuildInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, i, iItem, False)
				elif sType == "DomainMoves":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, i, iItem, False)
				elif sType == "CommerceFlexible":
					szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
					if iItem == CommerceTypes.COMMERCE_CULTURE:
						szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_CULTURE").getPath()
					elif iItem == CommerceTypes.COMMERCE_ESPIONAGE:
						szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_ESPIONAGE").getPath()
					#elif iItem == CommerceTypes.COMMERCE_RESEARCH:
					#	szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_RESEARCH").getPath()
					#elif iItem == CommerceTypes.COMMERCE_GOLD:
					#	szFileName = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_GOLD").getPath()
					screen.addDDSGFCAt(sButton, szTechRecord, szFileName, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_ADJUST, i, iItem, False)
				elif sType == "TerrainTrade":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, iItem, False)
				elif sType == "RiverTrade":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, gc.getNumTerrainInfos(), False)
				elif sType == "ImprovementYield":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getImprovementInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, i, iItem, False)
				elif sType == "UnlockCivic":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getCivicInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_CIVIC_REVEAL, i, iItem, False)
				elif sType == "UnlockProject":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getProjectInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, iItem, 1, False)
				elif sType == "UnlockProcess":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getProcessInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PROCESS_INFO, i, iItem, False)
				elif sType == "UnlockReligion":
					if CyGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
						szButton = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_POPUPBUTTON_RELIGION").getPath()
					else:
						szButton = gc.getReligionInfo(iItem).getButton()
					screen.addDDSGFCAt(sButton, szTechRecord, szButton, iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, i, iItem, False)
				elif sType == "UnlockCorporation":
					screen.addDDSGFCAt(sButton, szTechRecord, gc.getCorporationInfo(iItem).getButton(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, i, iItem, False)
				elif sType == "TechHelp":
					screen.addDDSGFCAt(sButton, szTechRecord, CyArtFileMgr().getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath(), iX + fX, iY + Y_ROW, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PYTHON, 7800, i, False)
				fX += X_INCREMENT
			fX = BOX_WIDTH - (PIXEL_INCREMENT * 2)

			for j in xrange(gc.getNUM_AND_TECH_PREREQS()):
				eTech = Info.getPrereqAndTechs(j)
				if eTech == -1: break
				fX -= X_INCREMENT
				szTechPrereqID = "TechPrereqID" + str((i * 1000) + j)
				screen.addDDSGFCAt( szTechPrereqID, szTechRecord, gc.getTechInfo(eTech).getButton(), iX + fX, iY + 6, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

			for j in xrange(gc.getNUM_OR_TECH_PREREQS()):
				eTech = Info.getPrereqOrTechs(j)
				if eTech == -1: break
				iX = (gc.getTechInfo(eTech).getGridX() -1) * (BOX_X_SPACING + BOX_WIDTH) + BOX_WIDTH - 6
				iY = (gc.getTechInfo(eTech).getGridY() -1) * (BOX_HEIGHT + BOX_Y_SPACING)/2 - 6
					
				xDiff = Info.getGridX() - gc.getTechInfo(eTech).getGridX()
				yDiff = Info.getGridY() - gc.getTechInfo(eTech).getGridY()

				if yDiff == 0:
					screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX, iY + self.getYStart(4), self.getWidth(xDiff), 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
				elif yDiff < 0:
					if yDiff < -3 and xDiff == 1:					
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX, iY + self.getYStart(2), self.getWidth(xDiff)/3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_XY, iX + self.getWidth(xDiff)/3, iY + self.getYStart(2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_Y, iX + self.getWidth(xDiff)/3, iY + self.getYStart(2) + 8 - self.getHeight(yDiff, -4), 8, self.getHeight(yDiff, -4) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_XMY, iX + self.getWidth(xDiff)/3, iY + self.getYStart(2) - self.getHeight(yDiff, -4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX + 8 + self.getWidth(xDiff)/3, iY + self.getYStart(2) - self.getHeight(yDiff, -4), self.getWidth(xDiff) * 2/3 - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(2) - self.getHeight(yDiff, -4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					else:
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX, iY + self.getYStart(3), self.getWidth(xDiff)/2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_XY, iX + self.getWidth(xDiff)/2, iY + self.getYStart(3), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_Y, iX + self.getWidth(xDiff)/2, iY + self.getYStart(3) + 8 - self.getHeight(yDiff, -2), 8, self.getHeight(yDiff, -2) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_XMY, iX + self.getWidth(xDiff)/2, iY + self.getYStart(3) - self.getHeight(yDiff, -2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX + 8 + self.getWidth(xDiff)/2, iY + self.getYStart(3) - self.getHeight(yDiff, -2), self.getWidth(xDiff)/2 - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(3) - self.getHeight(yDiff, -2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
				else:
					pass
					if yDiff > 3 and xDiff == 1:
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX, iY + self.getYStart(6), self.getWidth(xDiff)/3, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_MXMY, iX + self.getWidth(xDiff)/3, iY + self.getYStart(6), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_Y, iX + self.getWidth(xDiff)/3, iY + self.getYStart(6) + 8, 8, self.getHeight(yDiff, -4) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_MXY, iX + self.getWidth(xDiff)/3, iY + self.getYStart(6) + self.getHeight(yDiff, -4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX + 8 + self.getWidth(xDiff)/3, iY + self.getYStart(6) + self.getHeight(yDiff, -4), self.getWidth(xDiff) * 2/3 - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(6) + self.getHeight(yDiff, -4), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					else:
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX, iY + self.getYStart(5), self.getWidth(xDiff)/2, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_MXMY, iX + self.getWidth(xDiff)/2, iY + self.getYStart(5), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_Y, iX + self.getWidth(xDiff)/2, iY + self.getYStart(5) + 8, 8, self.getHeight(yDiff, -2) - 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_MXY, iX + self.getWidth(xDiff)/2, iY + self.getYStart(5) + self.getHeight(yDiff, -2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_X, iX + 8 + self.getWidth(xDiff)/2, iY + self.getYStart(5) + self.getHeight(yDiff, -2), self.getWidth(xDiff)/2 - 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt(self.top.getNextWidgetName(), self.top.UPGRADES_GRAPH_ID, ARROW_HEAD, iX + self.getWidth(xDiff), iY + self.getYStart(5) + self.getHeight(yDiff, -2), 8, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

	def getYStart(self, iY):
		return BOX_HEIGHT * iY / 8

	def getWidth(self, xDiff):
		return xDiff * BOX_X_SPACING + (xDiff - 1) * BOX_WIDTH
		
	def getHeight(self, yDiff, iAdjustment):
		return (abs(yDiff) * (BOX_Y_SPACING + BOX_HEIGHT)/2) + (iAdjustment * BOX_HEIGHT/8)

	def handleInput (self, inputClass):
		return 0