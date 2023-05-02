from CvPythonExtensions import *

gc = CyGlobalContext()
g_iAdvisorNags = 0
g_listNoLiberateCities = []
lPopulation = [	[2000000000, FeatTypes.FEAT_POPULATION_2_BILLION, "TXT_KEY_FEAT_2_BILLION"],
		[1000000000, FeatTypes.FEAT_POPULATION_1_BILLION, "TXT_KEY_FEAT_1_BILLION"],
		[500000000, FeatTypes.FEAT_POPULATION_500_MILLION, "TXT_KEY_FEAT_500_MILLION"],
		[200000000, FeatTypes.FEAT_POPULATION_200_MILLION, "TXT_KEY_FEAT_200_MILLION"],
		[100000000, FeatTypes.FEAT_POPULATION_100_MILLION, "TXT_KEY_FEAT_100_MILLION"],
		[50000000, FeatTypes.FEAT_POPULATION_50_MILLION, "TXT_KEY_FEAT_50_MILLION"],
		[20000000, FeatTypes.FEAT_POPULATION_20_MILLION, "TXT_KEY_FEAT_20_MILLION"],
		[10000000, FeatTypes.FEAT_POPULATION_10_MILLION, "TXT_KEY_FEAT_10_MILLION"],
		[5000000, FeatTypes.FEAT_POPULATION_5_MILLION, "TXT_KEY_FEAT_5_MILLION"],
		[2000000, FeatTypes.FEAT_POPULATION_2_MILLION, "TXT_KEY_FEAT_2_MILLION"],
		[1000000, FeatTypes.FEAT_POPULATION_1_MILLION, "TXT_KEY_FEAT_1_MILLION"],
		[500000, FeatTypes.FEAT_POPULATION_HALF_MILLION, "TXT_KEY_FEAT_HALF_MILLION"]]
lUnitCombat = {	"UNITCOMBAT_MOUNTED":	[FeatTypes.FEAT_UNITCOMBAT_MOUNTED, "TXT_KEY_FEAT_UNITCOMBAT_MOUNTED"],
		"UNITCOMBAT_ARCHER":	[FeatTypes.FEAT_UNITCOMBAT_ARCHER, "TXT_KEY_FEAT_UNITCOMBAT_ARCHER"],
		"UNITCOMBAT_MELEE":	[FeatTypes.FEAT_UNITCOMBAT_MELEE, "TXT_KEY_FEAT_UNITCOMBAT_MELEE"],
		"UNITCOMBAT_GUN":	[FeatTypes.FEAT_UNITCOMBAT_GUN, "TXT_KEY_FEAT_UNITCOMBAT_GUN"],
		"UNITCOMBAT_SIEGE":	[FeatTypes.FEAT_UNITCOMBAT_SIEGE, "TXT_KEY_FEAT_UNITCOMBAT_SIEGE"],
		"UNITCOMBAT_ARMOR":	[FeatTypes.FEAT_UNITCOMBAT_ARMOR, "TXT_KEY_FEAT_UNITCOMBAT_ARMOR"],
		"UNITCOMBAT_NAVAL":	[FeatTypes.FEAT_UNITCOMBAT_NAVAL, "TXT_KEY_FEAT_UNITCOMBAT_NAVAL"],
		"UNITCOMBAT_HELICOPTER":	[FeatTypes.FEAT_UNITCOMBAT_HELICOPTER, "TXT_KEY_FEAT_UNITCOMBAT_HELICOPTER"]}

lCorporations = []
lBonus = []

lUnits = {	"Settlers":	[],
		"Workers":	[],
		"Defenders":	[],
		"Missionaries":	[]}

lBuildings = {	"Research":	[],
		"Gold":		[],
		"Culture":	[],
		"Maintenance":	[],
		"SeaFood":	[],
		"Defense":	[],
		"Happy":	[],
		"Health":	[]}
		

def featPopup(iPlayer):
	if not gc.getPlayer(iPlayer).isOption(PlayerOptionTypes.PLAYEROPTION_ADVISOR_POPUPS):
		return False
	if not gc.getPlayer(iPlayer).isHuman():
		return False
	if CyGame().isNetworkMultiPlayer():
		return False
	if CyGame().getElapsedGameTurns() == 0:
		return False
	if CyGame().getStartYear() != gc.getDefineINT("START_YEAR"):
		return False
	return True

def resetAdvisorNags():
	global g_iAdvisorNags
	g_iAdvisorNags = 0
	
def resetNoLiberateCities():
	global g_listNoLiberateCities
	g_listNoLiberateCities = []

	global lCorporations
	lCorporations = []

	for iI in xrange(gc.getNumBuildingInfos()):
		Info = gc.getBuildingInfo(iI)
		eCorporation = Info.getFoundsCorporation()
		if eCorporation > -1 and not CyGame().isCorporationFounded(eCorporation):
			lTechs = []
			iTech = Info.getPrereqAndTech()
			if iTech > -1:
				lTechs.append(iTech)
			for iPrereq in xrange(gc.getDefineINT("NUM_BUILDING_AND_TECH_PREREQS")):
				iTech = Info.getPrereqAndTechs(iPrereq)
				if iTech > -1:
					lTechs.append(iTech)

			iUnit = -1
			for i in xrange(gc.getNumUnitInfos()):
				if gc.getUnitInfo(i).getBuildings(iI) or gc.getUnitInfo(i).getForceBuildings(iI):
					iUnit = i
					break
			if iUnit == -1: continue

			lTemp = []
			for iPrereq in xrange(gc.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES")):
				eBonus = gc.getCorporationInfo(eCorporation).getPrereqBonus(iPrereq)
				if eBonus > -1:
					lTemp.append(eBonus)
			if len(lTemp) == 0: continue

			lCorporations.append([eCorporation, lTechs, iUnit, lTemp])
	global lBonus
	lBonus = []
	lLuxury = []
	lFood = []

	for i in xrange(gc.getNumBonusInfos()):
		if gc.getBonusInfo(i).getHappiness() > 0:
			lLuxury.append(i)
		if gc.getBonusInfo(i).getHealth() > 0:
			lFood.append(i)
	iBonus = gc.getInfoTypeForString("BONUS_COPPER")
	if iBonus > -1:
		lBonus.append([FeatTypes.FEAT_COPPER_CONNECTED, [iBonus], "TXT_KEY_FEAT_COPPER_CONNECTED"])
	iBonus = gc.getInfoTypeForString("BONUS_HORSE")
	if iBonus > -1:
		lBonus.append([FeatTypes.FEAT_HORSE_CONNECTED, [iBonus], "TXT_KEY_FEAT_HORSE_CONNECTED"])
	iBonus = gc.getInfoTypeForString("BONUS_IRON")
	if iBonus > -1:
		lBonus.append([FeatTypes.FEAT_IRON_CONNECTED, [iBonus], "TXT_KEY_FEAT_IRON_CONNECTED"])
	if len(lLuxury) > 0:
		lBonus.append([FeatTypes.FEAT_LUXURY_CONNECTED, lLuxury, "TXT_KEY_FEAT_LUXURY_CONNECTED"])
	if len(lFood) > 0:
		lBonus.append([FeatTypes.FEAT_FOOD_CONNECTED, lFood, "TXT_KEY_FEAT_FOOD_CONNECTED"])

	global lUnits
	lUnits = {	"Settlers":	[],
			"Workers":	[],
			"Defenders":	[],
			"Missionaries":	[]}

	for i in xrange(gc.getNumUnitInfos()):
		Info = gc.getUnitInfo(i)
		if Info.getProductionCost == -1: continue
		if Info.getDomainType() != DomainTypes.DOMAIN_LAND: continue
		if Info.isFound():
			lUnits["Settlers"].append(i)
		if Info.getWorkRate() > 0:
			lUnits["Workers"].append(i)
		if Info.getCombat() > 0:
			lUnits["Defenders"].append(i)
		if Info.getDefaultUnitAIType() == UnitAITypes.UNITAI_MISSIONARY:
			lUnits["Missionaries"].append(i)

	global lBuildings
	lBuildings = {	"Research":	[],
			"Gold":		[],
			"Culture":	[],
			"Maintenance":	[],
			"SeaFood":	[],
			"Defense":	[],
			"Happy":	[],
			"Health":	[]}

	for i in xrange(gc.getNumBuildingInfos()):
		Info = gc.getBuildingInfo(i)
		if Info.getProductionCost == -1: continue
		if isLimitedWonderClass(Info.getBuildingClassType()): continue
		if Info.getCommerceModifier(CommerceTypes.COMMERCE_RESEARCH) > 0:
			lBuildings["Research"].append(i)
		if Info.getCommerceModifier(CommerceTypes.COMMERCE_GOLD) > 0:
			lBuildings["Gold"].append(i)
		if Info.getObsoleteSafeCommerceChange(CommerceTypes.COMMERCE_CULTURE) > 0:
			lBuildings["Culture"].append(i)
		if Info.getMaintenanceModifier() < 0:
			lBuildings["Maintenance"].append(i)
		if Info.getSeaPlotYieldChange(YieldTypes.YIELD_FOOD) > 0:
			lBuildings["SeaFood"].append(i)
		if Info.getDefenseModifier() > 0:
			lBuildings["Defense"].append(i)
		if Info.getHappiness() > 0:
			lBuildings["Happy"].append(i)
		if Info.getHealth() > 0:
			lBuildings["Health"].append(i)

def unitBuiltFeats(pCity, pUnit):
	iPlayer = pCity.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iCombat = pUnit.getUnitCombatType()
	if iCombat > -1:
		sCombat = gc.getUnitCombatInfo(iCombat).getType()
		if sCombat in lUnitCombat:
			iFeat = lUnitCombat[sCombat][0]
			if not pPlayer.isFeatAccomplished(iFeat):
				updateFeat(iPlayer, iFeat, CyTranslator().getText(lUnitCombat[sCombat][1], (pUnit.getNameKey(), pCity.getNameKey(), )), pCity.getID())

		if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_UNIT_PRIVATEER):
			if gc.getUnitInfo(pUnit.getUnitType()).isHiddenNationality() and pUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
				updateFeat(iPlayer, FeatTypes.FEAT_UNIT_PRIVATEER, CyTranslator().getText("TXT_KEY_FEAT_UNIT_PRIVATEER", (pUnit.getNameKey(), pCity.getNameKey(), )), pCity.getID())

	if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_UNIT_SPY):
		if gc.getUnitInfo(pUnit.getUnitType()).isSpy():
			updateFeat(iPlayer, FeatTypes.FEAT_UNIT_SPY, CyTranslator().getText("TXT_KEY_FEAT_UNIT_SPY", (pUnit.getNameKey(), pCity.getNameKey(), )), pCity.getID())

def buildingBuiltFeats(pCity, iBuildingType):
	if gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_NATIONAL_WONDER): return
	if isNationalWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType()):
		updateFeat(pCity.getOwner(), FeatTypes.FEAT_NATIONAL_WONDER, CyTranslator().getText("TXT_KEY_FEAT_NATIONAL_WONDER", (gc.getBuildingInfo(iBuildingType).getTextKey(), pCity.getNameKey(),)), pCity.getID())

def updateFeat(iPlayer, eFeat, szText, iCityID):
	gc.getPlayer(iPlayer).setFeatAccomplished(eFeat, True)
	if featPopup(iPlayer):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setData1(eFeat)
		popupInfo.setData2(iCityID)
		popupInfo.setText(szText)
		popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
		popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
		popupInfo.addPopup(iPlayer)

def endTurnFeats(iPlayer):
	global g_listPopulationFeats
	pPlayer = gc.getPlayer(iPlayer)
	pCapitalCity = pPlayer.getCapitalCity()
	if pCapitalCity.isNone(): return

	lRealPopulation = pPlayer.getRealPopulation()
	for item in lPopulation:
		if pPlayer.isFeatAccomplished(item[1]): break
		if lRealPopulation > item[0]:
			updateFeat(iPlayer, item[1], CyTranslator().getText(item[2], (pPlayer.getCivilizationDescriptionKey(), )), pCapitalCity.getID())

	if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_TRADE_ROUTE):
		(pCity, iter) = pPlayer.firstCity(False)
		while(pCity):
			if not pCity.isCapital():
				if pCity.isConnectedToCapital(iPlayer):
					updateFeat(iPlayer, FeatTypes.FEAT_TRADE_ROUTE, CyTranslator().getText("TXT_KEY_FEAT_TRADE_ROUTE", (pCity.getNameKey(), )), pCity.getID())
					break
			(pCity, iter) = pPlayer.nextCity(iter, False)

	for item in lBonus:
		if pPlayer.isFeatAccomplished(item[0]): continue
		for iBonus in item[1]:
			if pCapitalCity.hasBonus(iBonus):
				updateFeat(iPlayer, item[0], CyTranslator().getText(item[2], (gc.getBonusInfo(iBonus).getTextKey(),)), pCapitalCity.getID())
				break

	if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_CORPORATION_ENABLED):
		global lCorporations
		eTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(eTeam)
		i = 0
		while i < len(lCorporations):
			item = lCorporations[i]
			if CyGame().isCorporationFounded(item[0]):
				del lCorporations[i]
			else:
				bValid = True
				for iTech in item[1]:
					if not pTeam.isHasTech(iTech):
						bValid = False
						break
				if bValid:
					szBonusList = u""
					for j in xrange(len(item[3])):
						eBonus = item[3][j]
						szBonusList += gc.getBonusInfo(eBonus).getDescription()
						if j != len(item[3]) - 1:
							szBonusList += CyTranslator().getText("TXT_KEY_OR", ())
					
					szFounder = gc.getUnitInfo(item[2]).getTextKey()
					updateFeat(iPlayer, FeatTypes.FEAT_CORPORATION_ENABLED, CyTranslator().getText("TXT_KEY_FEAT_CORPORATION_ENABLED", (gc.getCorporationInfo(item[0]).getTextKey(), szFounder, szBonusList)), pCapitalCity.getID())
					break
				i += 1

def cityAdvise(pCity, iPlayer):

	global g_iAdvisorNags
	if g_iAdvisorNags > 1: return
	if pCity.isDisorder(): return
	pPlayer = gc.getPlayer(iPlayer)

	if (pPlayer.isOption(PlayerOptionTypes.PLAYEROPTION_ADVISOR_POPUPS) and pPlayer.isHuman() and not CyGame().isNetworkMultiPlayer()):
		iTurnDiff = (CyGame().getGameTurn() - pCity.getGameTurnFounded())% 40
		if iTurnDiff == 0:
			if pCity.getID() in g_listNoLiberateCities: return
			eLiberationPlayer = pCity.getLiberationPlayer(false)
			if eLiberationPlayer > -1:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(pCity.getID())
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_LIBERATION_DEMAND", (pCity.getNameKey(), gc.getPlayer(eLiberationPlayer).getCivilizationDescriptionKey(), gc.getPlayer(eLiberationPlayer).getNameKey())))
				popupInfo.setOnClickedPythonCallback("liberateOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
				popupInfo.addPopup(iPlayer)
				g_listNoLiberateCities.append(pCity.getID())
				g_iAdvisorNags += 1

			elif (pPlayer.canSplitEmpire() and pPlayer.canSplitArea(pCity.area().getID()) and pCity.AI_cityValue() < 0):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(pCity.getID())
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_COLONY_DEMAND", (pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("colonyOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
				popupInfo.addPopup(iPlayer)
				g_listNoLiberateCities.append(pCity.getID())
				g_iAdvisorNags += 1

		elif pCity.isProduction() and pCity.getOrderQueueLength() < 2:
			lBest = []
			if not pCity.isProductionUnit():
				if iTurnDiff == 3:
					if ((CyGame().getElapsedGameTurns() < 200) and pCity.getPopulation() > 2 and (pPlayer.AI_totalAreaUnitAIs(pCity.area(), UnitAITypes.UNITAI_SETTLE) == 0) and not pPlayer.AI_isFinancialTrouble() and (pCity.area().getBestFoundValue(iPlayer) > 0)):
						for eLoopUnit in lUnits["Settlers"]:
							if pCity.canTrain(eLoopUnit, False, False):
								iValue = pPlayer.AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_SETTLE, pCity.area())
								lBest.append([iValue,eLoopUnit, CyTranslator().getText("TXT_KEY_POPUP_UNIT_SETTLE_DEMAND", (gc.getUnitInfo(eLoopUnit).getTextKey(),))])
					
				elif iTurnDiff == 15:
					if (pCity.getPopulation() > 1 and pCity.countNumImprovedPlots() == 0 and (pCity.AI_countBestBuilds(pCity.area()) > 3)):
						for eLoopUnit in lUnits["Workers"]:
							if pCity.canTrain(eLoopUnit, False, False):
								iValue = gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_WORKER, pCity.area())
								lBest.append([iValue,eLoopUnit, CyTranslator().getText("TXT_KEY_POPUP_UNIT_WORKER_DEMAND", (pCity.getNameKey(), gc.getUnitInfo(eLoopUnit).getTextKey()))])

				elif iTurnDiff == 27:
					if pCity.plot().getNumDefenders(iPlayer) == 0:
						for eLoopUnit in lUnits["Defenders"]:
							if pCity.canTrain(eLoopUnit, False, False):
								iValue = (gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_CITY_DEFENSE, pCity.area()) * 2)
								iValue += gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_ATTACK, pCity.area())
								lBest.append([iValue,eLoopUnit, CyTranslator().getText("TXT_KEY_POPUP_UNIT_DEFENSE_DEMAND", (pCity.getNameKey(), gc.getUnitInfo(eLoopUnit).getTextKey()))])

				elif iTurnDiff == 36:
					if ((pPlayer.AI_totalAreaUnitAIs(pCity.area(), UnitAITypes.UNITAI_MISSIONARY) == 0) and (gc.getTeam(pPlayer.getTeam()).getAtWarCount(True) == 0)):
						eStateReligion = pPlayer.getStateReligion()
						if eStateReligion != ReligionTypes.NO_RELIGION:
							if pPlayer.getHasReligionCount(eStateReligion) < (pPlayer.getNumCities() / 2):
								for eLoopUnit in lUnits["Missionaries"]:
									if gc.getUnitInfo(eLoopUnit).getReligionSpreads(eStateReligion):
										if pCity.canTrain(eLoopUnit, False, False):
											iValue = pPlayer.AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_MISSIONARY, pCity.area())
											lBest.append([iValue,eLoopUnit, CyTranslator().getText("TXT_KEY_POPUP_MISSIONARY_DEMAND", (gc.getReligionInfo(eStateReligion).getTextKey(), gc.getUnitInfo(eLoopUnit).getTextKey(), pCity.getNameKey()))])

				if len(lBest) > 0:
					lBest.sort()
					lBest.reverse()
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setData1(pCity.getID())
					popupInfo.setData2(OrderTypes.ORDER_TRAIN)
					popupInfo.setData3(lBest[0][1])
					popupInfo.setText(lBest[0][2])
					popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
					popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
					popupInfo.addPopup(iPlayer)
					g_iAdvisorNags += 1

			elif not pCity.isProductionBuilding():
				if iTurnDiff == 6:
					if pCity.healthRate(False, 0) < 0:
						for eLoopBuilding in lBuildings["Health"]:
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getHealth()
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_UNHEALTHY_CITIZENS_DEMAND"])

				elif iTurnDiff == 9:
					if pCity.angryPopulation(0) > 0:
						for eLoopBuilding in lBuildings["Happy"]:
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getHappiness()
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_UNHAPPY_CITIZENS_DEMAND"])

				elif iTurnDiff == 12:
					if (CyGame().getGameTurn < 100 and gc.getTeam(pPlayer.getTeam()).getHasMetCivCount(True) > 0 and pCity.getBuildingDefense() == 0):
						for eLoopBuilding in lBuildings["Defense"]:
							if gc.getBuildingInfo(eLoopBuilding).getDefenseModifier() < pCity.getNaturalDefense(): continue
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getDefenseModifier()
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_BUILDING_DEFENSE_DEMAND"])

				elif iTurnDiff == 18:
					if pCity.getMaintenance() >= 8:
						for eLoopBuilding in lBuildings["Maintenance"]:
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getMaintenanceModifier()
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_MAINTENANCE_DEMAND"])

				elif iTurnDiff == 21:
					if pCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE) < 0:
						for eLoopBuilding in lBuildings["Culture"]:
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getObsoleteSafeCommerceChange(CommerceTypes.COMMERCE_CULTURE)
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_CULTURE_DEMAND"])

				elif iTurnDiff == 24:
					if pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_GOLD) > 10:
						for eLoopBuilding in lBuildings["Gold"]:
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getCommerceModifier(CommerceTypes.COMMERCE_GOLD)
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_GOLD_DEMAND"])

				elif iTurnDiff == 30:
					if pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_RESEARCH) > 10:
						for eLoopBuilding in lBuildings["Research"]:
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getCommerceModifier(CommerceTypes.COMMERCE_RESEARCH)
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_RESEARCH_DEMAND"])

				elif iTurnDiff == 33:
					if pCity.countNumWaterPlots() > 10:
						for eLoopBuilding in lBuildings["SeaFood"]:
							if pCity.canConstruct(eLoopBuilding, False, False, False):
								iValue = gc.getBuildingInfo(eLoopBuilding).getSeaPlotYieldChange(YieldTypes.YIELD_FOOD)
								lBest.append([iValue,eLoopBuilding, "TXT_KEY_POPUP_WATER_FOOD_DEMAND"])

				if len(lBest) > 0:
					lBest.sort()
					lBest.reverse()
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setData1(pCity.getID())
					popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
					popupInfo.setData3(lBest[0][1])
					popupInfo.setText(CyTranslator().getText(lBest[0][2], (pCity.getNameKey(), gc.getBuildingInfo(lBest[0][1]).getTextKey())))
					popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
					popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
					popupInfo.addPopup(iPlayer)
					g_iAdvisorNags += 1