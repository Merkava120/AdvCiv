from CvPythonExtensions import *
gc = CyGlobalContext()

def checkAlerts(pCity, iPlayer):
	if pCity.isDisorder(): return
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman(): return
	if not pPlayer.isOption(PlayerOptionTypes.PLAYEROPTION_ADVISOR_POPUPS): return

	if pCity.getFoodTurnsLeft() == 1:
		CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_GROW_SOON", (pCity.getName(), pCity.getPopulation() + 1,)),"",0, "",gc.getInfoTypeForString("COLOR_YIELD_FOOD"), -1, -1, True,True)
		if pCity.goodHealth() == pCity.badHealth(False):
			CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_UNHEALTHY_SOON", (pCity.getName(),)),"",0, "",gc.getInfoTypeForString("COLOR_PLAYER_LIGHT_GREEN"), -1, -1, True,True)
		if pCity.happyLevel() == pCity.unhappyLevel(0):
			CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_UNHAPPY_SOON", (pCity.getName(),)),"",0, "",gc.getInfoTypeForString("COLOR_RED"), -1, -1, True,True)

	else:
		iFoodDiff = pCity.foodDifference(True)
		if iFoodDiff < 0 and pCity.getFood() < -iFoodDiff:
			CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_STARVE_SOON", (pCity.getName(),)),"",0, "",gc.getInfoTypeForString("COLOR_RED"), -1, -1, True,True)

	iCultureThreshold100 = pCity.getCultureThreshold() * 100
	if iCultureThreshold100 > pCity.getCultureTimes100(iPlayer):
		if iCultureThreshold100 - pCity.getCultureTimes100(iPlayer) <= pCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE):
			CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_CULTURE_SOON", (pCity.getName(),)),"",0, "",gc.getInfoTypeForString("COLOR_CULTURE_STORED"), -1, -1, True,True)

	bWorldHurry = False
	item = pCity.getProductionBuilding()
	if item > -1:
		itemInfo = gc.getBuildingInfo(item)
		bWorldHurry = isWorldWonderClass(itemInfo.getBuildingClassType())
	if not bWorldHurry:
		item = pCity.getProductionUnit()
		if item > -1:
			itemInfo = gc.getUnitInfo(item)
			bWorldHurry = not isWorldUnitClass(itemInfo.getUnitClassType())
	if bWorldHurry:
		for iHurry in xrange(gc.getNumHurryInfos()):
			if pCity.canHurry(iHurry, True):
				HurryInfo = gc.getHurryInfo(iHurry)
				if HurryInfo.getGoldPerProduction() > 0 and pCity.hurryGold(iHurry) <= pPlayer.getGold():
					CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_CAN_HURRY", (pCity.getName(), itemInfo.getDescription(), pCity.hurryGold(iHurry), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getDescription())),"",0, "",gc.getInfoTypeForString("COLOR_CYAN"), -1, -1, True,True)
				if HurryInfo.getProductionPerPopulation() > 0 and pCity.hurryPopulation(iHurry) <= pCity.maxHurryPopulation():
					CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_CAN_HURRY", (pCity.getName(), itemInfo.getDescription(), pCity.hurryPopulation(iHurry), CyTranslator().getText("TXT_KEY_SPECIALIST_CITIZEN", ()))),"",0, "",gc.getInfoTypeForString("COLOR_CYAN"), -1, -1, True,True)

def cityGrown(pCity, iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman(): return
	if not pPlayer.isOption(PlayerOptionTypes.PLAYEROPTION_ADVISOR_POPUPS): return

	CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_GROW_NOW", (pCity.getName(), pCity.getPopulation(),)),"",0, "",gc.getInfoTypeForString("COLOR_YIELD_FOOD"), -1, -1, True,True)

	if pCity.badHealth(False) - pCity.goodHealth() == 1:
		CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_UNHEALTHY_NOW", (pCity.getName(),)),"",0, "",gc.getInfoTypeForString("COLOR_PLAYER_LIGHT_GREEN"), -1, -1, True,True)
	if pCity.unhappyLevel(0) - pCity.happyLevel() == 1:
		CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_ALERT_UNHAPPY_NOW", (pCity.getName(),)),"",0, "",gc.getInfoTypeForString("COLOR_RED"), -1, -1, True,True)