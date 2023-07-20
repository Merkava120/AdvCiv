//	FILE:	 CvMap.cpp
//	AUTHOR:  Soren Johnson
//	PURPOSE: Game map class
//	Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.


#include "CvGameCoreDLL.h"
#include "CvMap.h"
#include "PlotRange.h"
#include "CvArea.h"
#include "CvGame.h"
#include "CvPlayer.h"
#include "CvCity.h"
#include "CvUnit.h"
#include "CvSelectionGroup.h"
#include "CvPlotGroup.h"
#include "CvFractal.h"
#include "CvMapGenerator.h"
#include "DepthFirstPlotSearch.h" // advc.030
#include "GroupPathFinder.h"
#include "FAStarFunc.h"
#include "FAStarNode.h"
#include "CvInfo_Terrain.h" // advc.pf (for pathfinder initialization)
#include "CvInfo_GameOption.h"
#include "CvReplayInfo.h" // advc.106n
#include "BarbarianWeightMap.h" // advc.304
#include "CvDLLIniParserIFaceBase.h"
#include <boost/algorithm/string.hpp> // advc.108b


CvMap::CvMap()
{
	CvMapInitData defaultMapData;
	m_pMapPlots = NULL;
	reset(&defaultMapData);
}


CvMap::~CvMap()
{
	uninit();
}

/*	Initializes the map
	pInitInfo  - Optional init structure (used for WB load) */
void CvMap::init(CvMapInitData* pInitInfo)
{
	PROFILE("CvMap::init");
	gDLL->logMemState(CvString::format("CvMap::init begin - world size=%s, climate=%s, sealevel=%s, num custom options=%6",
			GC.getInfo(GC.getInitCore().getWorldSize()).getDescription(),
			GC.getInfo(GC.getInitCore().getClimate()).getDescription(),
			GC.getInfo(GC.getInitCore().getSeaLevel()).getDescription(),
			GC.getInitCore().getNumCustomMapOptions()).c_str());
	GC.getPythonCaller()->callMapFunction("beforeInit");

	reset(pInitInfo); // Init serialized data
	m_areas.init(); // Init containers
	setup();
	gDLL->logMemState("CvMap before init plots");
	FAssert(numPlots() <= integer_limits<PlotNumInt>::max); // advc.enum
	m_pMapPlots = new CvPlot[numPlots()];
	for (int iX = 0; iX < getGridWidth(); iX++)
	{
		gDLL->callUpdater();
		for (int iY = 0; iY < getGridHeight(); iY++)
		{
			getPlot(iX, iY).init(iX, iY);
		}
	}
	// <advc.003s>
	FOR_EACH_ENUM(PlotNum)
		getPlotByIndex(eLoopPlotNum).initAdjList(); // </advc.003s>
	calculateAreas();
	//calculateBiomes(); // merk.biome
	gDLL->logMemState("CvMap after init plots");
}


void CvMap::uninit()
{
	SAFE_DELETE_ARRAY(m_pMapPlots);
	m_replayTexture.clear(); // advc.106n
	m_areas.uninit();
	CvSelectionGroup::uninitPathFinder(); // advc.pf
}

// Initializes data members that are serialized.
void CvMap::reset(CvMapInitData const* pInitInfo,
	bool bResetPlotExtraData) // advc.enum (only needed for legacy saves)
{
	uninit();

	// set grid size
	// initially set in terrain cell units
	m_iGridWidth = (GC.getInitCore().getWorldSize() != NO_WORLDSIZE) ?
			GC.getInfo(GC.getInitCore().getWorldSize()).getGridWidth() : 0; //todotw:tcells wide
	m_iGridHeight = (GC.getInitCore().getWorldSize() != NO_WORLDSIZE) ?
			GC.getInfo(GC.getInitCore().getWorldSize()).getGridHeight() : 0;
	// advc.137: (Ignore CvLandscapeInfos::getPlotsPerCellX/Y)
	int iPlotsPerCell = 2;
	// allow grid size override
	if (pInitInfo != NULL)
	{
		m_iGridWidth	= pInitInfo->m_iGridW;
		m_iGridHeight	= pInitInfo->m_iGridH;
	}
	else
	{
		WorldSizeTypes eWorldSize = GC.getInitCore().getWorldSize();
		if (eWorldSize != NO_WORLDSIZE)
		{
			CvWorldInfo const& kWorldSz = GC.getInfo(eWorldSize);
			// <advc.165>
			int iPlotNumPercent;
			if (GC.getPythonCaller()->mapPlotsPercent(eWorldSize, iPlotNumPercent))
			{
				scaled rTargetAspectRatio(kWorldSz.getGridWidth(),
						kWorldSz.getGridHeight());
				// (The number of cells is proportional to the number of plots)
				scaled rTargetCells = m_iGridWidth * m_iGridHeight
						* per100(iPlotNumPercent);
				scaled rTargetHeight = (rTargetCells / rTargetAspectRatio).sqrt();
				scaled rTargetWidth = rTargetCells / rTargetHeight;
				m_iGridWidth = rTargetWidth.uround();
				m_iGridHeight = rTargetHeight.uround();
			}
			else // </advc.165>
			// check map script for grid size override
			if (GC.getPythonCaller()->mapGridDimensions(eWorldSize,
				m_iGridWidth, m_iGridHeight))
			{	// <advc.137>
				// If a map sets custom dimensions, then we can't change the scale.
				iPlotsPerCell = 4;
			}
			// Undo aspect ratio changes for Continents
			else if (!GC.getInitCore().getScenario() &&
				GC.getInitCore().getMapScriptName() == CvWString("Continents"))
			{
				scaled rModAspectRatio(kWorldSz.getGridWidth(),
						kWorldSz.getGridHeight());
				scaled rHStretch = fixp(1.6) / rModAspectRatio;
				m_iGridWidth = (m_iGridWidth * rHStretch).uround();
				m_iGridHeight = (m_iGridHeight / rHStretch).uround();
			} // </advc.137>
		}

		// convert to plot dimensions
	#if 0
		if (GC.getNumLandscapeInfos() > 0)
		{	/*  advc.003x: A bit of code moved into new CvGlobals functions
				in order to remove the dependency of CvMap on CvLandscapeInfos */
			m_iGridWidth *= GC.getLandscapePlotsPerCellX();
			m_iGridHeight *= GC.getLandscapePlotsPerCellY();
		}
	#endif
		/*	<advc.137> The landscape-based multipliers (4) are too coarse.
			I'm not seeing graphical artifacts; seems fine to use 2 instead. */
		m_iGridWidth *= iPlotsPerCell;
		m_iGridHeight *= iPlotsPerCell; // </advc.137>
	}
	updateNumPlots(); // advc.opt

	m_iLandPlots = 0;
	m_iOwnedPlots = 0;

	if (pInitInfo != NULL)
	{
		m_iTopLatitude = pInitInfo->m_iTopLatitude;
		m_iBottomLatitude = pInitInfo->m_iBottomLatitude;
	}
	else
	{
		// Check map script for latitude override (map script beats ini file)
		GC.getPythonCaller()->mapLatitudeExtremes(m_iTopLatitude, m_iBottomLatitude);
	}
	m_iTopLatitude = std::min(m_iTopLatitude, 90);
	m_iTopLatitude = std::max(m_iTopLatitude, -90);
	m_iBottomLatitude = std::min(m_iBottomLatitude, 90);
	m_iBottomLatitude = std::max(m_iBottomLatitude, -90);
	FAssert(m_iTopLatitude >= m_iBottomLatitude); // advc

	m_iNextRiverID = 0;
	//
	// set wrapping
	//
	m_bWrapX = true;
	m_bWrapY = false;
	if (pInitInfo)
	{
		m_bWrapX = pInitInfo->m_bWrapX;
		m_bWrapY = pInitInfo->m_bWrapY;
	}
	else
	{
		// Check map script for wrap override (map script beats ini file)
		GC.getPythonCaller()->mapWraps(m_bWrapX, m_bWrapY);
	}

	m_aiNumBonus.reset();
	m_aiNumBonusOnLand.reset();
	m_aebBalancedBonuses.reset(); // advc.108c
	// <advc.enum>
	if (bResetPlotExtraData)
		resetPlotExtraData(); // </advc.enum>
	m_areas.removeAll();
}

// Initializes all data that is not serialized but needs to be initialized after loading
void CvMap::setup()
{
	PROFILE_FUNC();

	CvDLLFAStarIFaceBase& kAStar = *gDLL->getFAStarIFace();
	kAStar.Initialize(&GC.getPathFinder(),
			getGridWidth(),	getGridHeight(),isWrapX(),	isWrapY(),
			pathDestValid,	pathHeuristic,	pathCost,	pathValid,
			pathAdd,		NULL,			NULL);
	kAStar.Initialize(&GC.getInterfacePathFinder(),
			getGridWidth(),	getGridHeight(),isWrapX(),	isWrapY(),
			pathDestValid,	pathHeuristic,	pathCost,	pathValid,
			pathAdd,		NULL,			NULL);
	kAStar.Initialize(&GC.getStepFinder(),
			getGridWidth(),	getGridHeight(),isWrapX(),	isWrapY(),
			stepDestValid,	stepHeuristic,	stepCost,	stepValid,
			stepAdd,		NULL,			NULL);
	kAStar.Initialize(&GC.getRouteFinder(),
			getGridWidth(), getGridHeight(), isWrapX(), isWrapY(),
			NULL,			NULL,			NULL,		routeValid,
			NULL,			NULL,			NULL);
	kAStar.Initialize(&GC.getBorderFinder(),
			getGridWidth(), getGridHeight(), isWrapX(), isWrapY(),
			NULL,			NULL,			NULL,		borderValid,
			NULL,			NULL,			NULL);
	kAStar.Initialize(&GC.getAreaFinder(),
			getGridWidth(), getGridHeight(), isWrapX(), isWrapY(),
			NULL,			NULL,			NULL,		areaValid,
			NULL,			joinArea,		NULL);
	/*	(PlotGroupFinder now probably unused, gets instantiated,
		if necessary, by CvGlobals::getPlotGroupFinder.) */
	// advc (note): IrrigatedFinder gets instantiated in updateIrrigated
	// <advc.pf>
	CvSelectionGroup::initPathFinder();
	// Moved this computation out of KmodPathFinder.h to avoid a header inclusion
	int iMinMovementCost = MAX_INT;
	int iMinFlatMovementCost = MAX_INT;
	FOR_EACH_ENUM(Route)
	{
		CvRouteInfo const& kLoopRoute = GC.getInfo(eLoopRoute);
		int iCost = kLoopRoute.getMovementCost();
		FOR_EACH_ENUM(Tech)
		{
			if (kLoopRoute.getTechMovementChange(eLoopTech) < 0)
				iCost += kLoopRoute.getTechMovementChange(eLoopTech);
		}
		iMinMovementCost = std::min(iMinMovementCost, iCost);
		iMinFlatMovementCost = std::min(iMinFlatMovementCost,
				kLoopRoute.getFlatMovementCost());
	}
	GroupPathFinder::initHeuristicWeights(
			iMinMovementCost, iMinFlatMovementCost); // </advc.pf>
}


void CvMap::setupGraphical() // graphical only setup
{
	if (!GC.IsGraphicsInitialized())
		return;

	CvPlot::setMaxVisibilityRangeCache(); // advc.003h
	if (m_pMapPlots != NULL)
	{
		for (int i = 0; i < numPlots(); i++)
		{
			gDLL->callUpdater(); // allow windows msgs to update
			getPlotByIndex(i).setupGraphical();
		}
	}
	// <advc.106n> For games starting in a later era
	if (getReplayTexture() == NULL &&
		GC.getGame().getHighestEra() >= GC.getDefineINT("REPLAY_TEXTURE_ERA"))
	{
		// The EXE isn't quite ready here to provide the texture
		GC.getGame().setUpdateTimer(CvGame::UPDATE_STORE_REPLAY_TEXTURE, 5);
	} // </advc.106n>
}


void CvMap::erasePlots()
{
	for (int i = 0; i < numPlots(); i++)
		plotByIndex(i)->erase();
	resetPlotExtraData(); // advc.004j
	m_replayTexture.clear(); // advc.106n
}


void CvMap::setRevealedPlots(TeamTypes eTeam, bool bNewValue, bool bTerrainOnly)
{
	PROFILE_FUNC();

	for (int i = 0; i < numPlots(); i++)
	{
		getPlotByIndex(i).setRevealed(eTeam, bNewValue, bTerrainOnly, NO_TEAM, false);
	}

	GC.getGame().updatePlotGroups();
}


void CvMap::setAllPlotTypes(PlotTypes ePlotType)
{
	//float startTime = (float) timeGetTime();

	for(int i = 0; i < numPlots(); i++)
	{
		getPlotByIndex(i).setPlotType(ePlotType, false, false);
	}

	recalculateAreas();

	//rebuild landscape
	gDLL->getEngineIFace()->RebuildAllPlots();

	//mark minimap as dirty
	gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);

	//float endTime = (float) timeGetTime();
	//printToConsole(CvString::format("[Jason] setAllPlotTypes: %f\n", endTime - startTime).c_str());
}

// XXX generalize these funcs? (macro?)
void CvMap::doTurn()
{
	//PROFILE("CvMap::doTurn()"); // advc.003o
	for(int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).doTurn();
}


void CvMap::updateFlagSymbols()
{
	PROFILE_FUNC();

	for (int i = 0; i < numPlots(); i++)
	{
		CvPlot& kPlot = getPlotByIndex(i);
		if (kPlot.isFlagDirty())
		{
			kPlot.updateFlagSymbol();
			kPlot.setFlagDirty(false);
		}
	}
}

// K-Mod:
void CvMap::setFlagsDirty()
{
	for (int i = 0; i < numPlots(); i++)
		plotByIndex(i)->setFlagDirty(true);
}


void CvMap::updateFog()
{
	for(int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateFog();
}


void CvMap::updateVisibility()
{
	for (int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateVisibility();
}


void CvMap::updateSymbolVisibility()
{
	for(int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateSymbolVisibility();
}


void CvMap::updateSymbols()
{
	for(int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateSymbols();
}


void CvMap::updateMinimapColor()
{
	for(int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateMinimapColor();
}


void CvMap::updateSight(bool bIncrement)
{
	for (int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateSight(bIncrement, false);

	GC.getGame().updatePlotGroups();
}


void CvMap::updateIrrigated()
{
	for(int i = 0; i < numPlots(); i++)
		updateIrrigated(getPlotByIndex(i));
}

/*	K-Mod. This function is called when the unit selection is changed
	or when a selected unit is promoted. (Or when UnitInfo_DIRTY_BIT is set.)
	The purpose is to update which unit is displayed in the center of each plot.
	The original implementation simply updated every plot on the map. This is
	a bad idea because it scales badly for big maps, and the update function
	on each plot can be expensive. The new functionality attempts to only
	update plots that are in movement range of the selected group;
	with a very generous approximation for what might be in range. */
void CvMap::updateCenterUnit()
{
	/*for (int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateCenterUnit();*/ // BtS
	PROFILE_FUNC();
	int iRange = -1;

	for (CLLNode<IDInfo> const* pNode = gDLL->UI().headSelectionListNode();
		pNode != NULL; pNode = gDLL->UI().nextSelectionListNode(pNode))
	{
		CvUnit const& kLoopUnit = *::getUnit(pNode->m_data);
		//if (kLoopUnit.getDomainType() == DOMAIN_AIR)
		if (kLoopUnit.airRange() > 0) // advc.rstr
			iRange = std::max(iRange, kLoopUnit.airRange());
		DomainTypes eLoopDomain = kLoopUnit.getDomainType();
		if (eLoopDomain == DOMAIN_LAND || eLoopDomain == DOMAIN_SEA) // advc.rstr
		{
			int iStepCost = (eLoopDomain == DOMAIN_LAND ?
					GroupPathFinder::minimumStepCost(kLoopUnit.baseMoves()) :
					GC.getMOVE_DENOMINATOR());
			int iMoveRange = kLoopUnit.maxMoves() / iStepCost +
					(kLoopUnit.canParadrop(kLoopUnit.plot()) ?
					kLoopUnit.getDropRange() : 0);
			iRange = std::max(iRange, iMoveRange);
		}
		/*  Note: technically we only really need the minimum range; but I'm using the maximum range
			because I think it will produce more intuitive and useful information for the player. */
	}

	if (iRange < 0 || iRange*iRange > numPlots() / 2)
	{
		// update the whole map
		for (int i = 0; i < numPlots(); i++)
			getPlotByIndex(i).updateCenterUnit();
	}
	else
	{
		// only update within the range
		CvPlot* pCenterPlot = gDLL->UI().getHeadSelectedUnit()->plot();
		for (SquareIter it(*pCenterPlot, iRange); it.hasNext(); ++it)
		{
			it->updateCenterUnit();
		}
	}
} // K-Mod end


void CvMap::updateWorkingCity()
{
	for (int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateWorkingCity();
}


void CvMap::updateMinOriginalStartDist(CvArea const& kArea)
{
	PROFILE_FUNC();

	for (int i = 0; i < numPlots(); i++)
	{
		CvPlot& kPlot = getPlotByIndex(i);
		if (kPlot.isArea(kArea))
			kPlot.setMinOriginalStartDist(-1);
	}

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlot* pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();
		if (pStartingPlot == NULL || !pStartingPlot->isArea(kArea))
			continue;
		for (int iJ = 0; iJ < numPlots(); iJ++)
		{
			CvPlot& kPlot = getPlotByIndex(iJ);
			if (kPlot.isArea(kArea) && /* K-Mod: */ &kPlot != pStartingPlot)
			{
				//iDist = calculatePathDistance(pStartingPlot, pLoopPlot);
				int iDist = stepDistance(pStartingPlot, &kPlot);
				if (iDist != -1)
				{
					//int iCrowDistance = plotDistance(pStartingPlot, pLoopPlot);
					//iDist = std::min(iDist,  iCrowDistance * 2);
					if (kPlot.getMinOriginalStartDist() == -1 ||
						iDist < kPlot.getMinOriginalStartDist())
					{
						kPlot.setMinOriginalStartDist(iDist);
					}
				}
			}
		}
	}
}


void CvMap::updateYield()
{
	for (int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).updateYield();
}

// <advc.enum> Moved from CvGame
void CvMap::setPlotExtraYield(CvPlot& kPlot, YieldTypes eYield, int iChange)
{
	m_aeiPlotExtraYield.set(kPlot.plotNum(), eYield, iChange);
	kPlot.updateYield();
}


void CvMap::changePlotExtraCost(CvPlot& kPlot, int iChange)
{
	m_aiPlotExtraCost.add(kPlot.plotNum(), iChange);
}


void CvMap::setPlotExtraYield(PlotNumTypes ePlot, YieldTypes eYield, int iChange)
{
	m_aeiPlotExtraYield.set(ePlot, eYield, iChange);
}


void CvMap::changePlotExtraCost(PlotNumTypes ePlot, int iChange)
{
	m_aiPlotExtraCost.add(ePlot, iChange);
}


void CvMap::resetPlotExtraData()
{
	m_aeiPlotExtraYield.reset();
	m_aiPlotExtraCost.reset();
} // </advc.enum>


void CvMap::verifyUnitValidPlot()
{
	for (int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).verifyUnitValidPlot();
}


void CvMap::combinePlotGroups(PlayerTypes ePlayer, CvPlotGroup* pPlotGroup1, CvPlotGroup* pPlotGroup2,
	bool bVerifyProduction) // advc.064d
{
	FAssert(pPlotGroup1 != NULL);
	FAssert(pPlotGroup2 != NULL);

	if(pPlotGroup1 == pPlotGroup2)
		return;

	CvPlotGroup* pNewPlotGroup;
	CvPlotGroup* pOldPlotGroup;

	if (pPlotGroup1->getLengthPlots() > pPlotGroup2->getLengthPlots())
	{
		pNewPlotGroup = pPlotGroup1;
		pOldPlotGroup = pPlotGroup2;
	}
	else
	{
		pNewPlotGroup = pPlotGroup2;
		pOldPlotGroup = pPlotGroup1;
	}

	CLLNode<XYCoords>* pPlotNode = pOldPlotGroup->headPlotsNode();
	while (pPlotNode != NULL)
	{
		CvPlot& kPlot = getPlot(pPlotNode->m_data.iX, pPlotNode->m_data.iY);
		pNewPlotGroup->addPlot(&kPlot, /* advc.064d: */ bVerifyProduction);
		pPlotNode = pOldPlotGroup->deletePlotsNode(pPlotNode);
	}
}


CvPlot* CvMap::syncRandPlot(RandPlotFlags eFlags, CvArea const* pArea,
	int iMinCivUnitDistance, // advc.300: Renamed from iMinUnitDistance
	int iTimeout,
	/* <advc.304> */ int* piValidCount, // Number of valid tiles
	RandPlotWeightMap const* pWeights)
{
	LOCAL_REF(int, iValid, piValidCount, 0);
	/*  Look exhaustively for a valid plot by default. Rationale:
		The biggest maps have about 10000 plots. If there is only one valid plot,
		then the BtS default of considering 100 plots drawn at random has only a
		(ca.) 1% chance of success. 10000 trials - slower than exhaustive search! -
		still have only a 63% chance of success. Also bear in mind that the
		1 plot in 10000 could be 1 of just 3 plots in the given pArea (or the only
		plot there), so not exactly a needle in a haystack from the caller's pov. */
	if (iTimeout < 0)
	{
		std::vector<CvPlot*> apValidPlots;
		std::vector<int> aiWeights;
		for (int i = 0; i < numPlots(); i++)
		{
			CvPlot& kPlot = getPlotByIndex(i);
			if (isValidRandPlot(kPlot, eFlags, pArea, iMinCivUnitDistance))
			{
				apValidPlots.push_back(&kPlot);
				if (pWeights != NULL)
					aiWeights.push_back(pWeights->getProbWeight(kPlot));
			}
		}
		iValid = (int)apValidPlots.size();
		return syncRand().weightedChoice(apValidPlots,
				pWeights == NULL ? NULL : &aiWeights);
	}
	FAssert(iTimeout != 0);
	FAssert(pWeights == NULL); // Not compatible with limited trials
	/*  BtS code (refactored): Limited number of trials
		(can be faster or slower than the above; that's not really the point) */
	// </advc.304>
	for (int i = 0; i < iTimeout; i++)
	{
		CvPlot& kTestPlot = getPlot(
				SyncRandNum(getGridWidth()), SyncRandNum(getGridHeight()));
		if (isValidRandPlot(kTestPlot, eFlags, pArea, iMinCivUnitDistance))
		{	/*  <advc.304> Not going to be useful ...
				Use 1 to indicate that we found one valid plot. */
			iValid = 1; // </advc.304>
			return &kTestPlot;
		}
	}
	return NULL;
}

// advc: Body cut from syncRandPlot
bool CvMap::isValidRandPlot(CvPlot const& kPlot, RandPlotFlags eFlags,
	CvArea const* pArea, int iMinCivUnitDistance) const
{
	if (pArea != NULL && !kPlot.isArea(*pArea))
		return false;
	/*  advc.300: Code moved into new function isCivUnitNearby;
		Barbarians in surrounding plots are now ignored. */
	if(iMinCivUnitDistance >= 0 && (kPlot.isUnit() ||
		kPlot.isCivUnitNearby(iMinCivUnitDistance)))
	{
		return false;
	}
	if ((eFlags & RANDPLOT_LAND) && kPlot.isWater())
		return false;
	if ((eFlags & RANDPLOT_UNOWNED) && kPlot.isOwned())
		return false;
	if ((eFlags & RANDPLOT_ADJACENT_UNOWNED) && kPlot.isAdjacentOwned())
		return false;
	if ((eFlags & RANDPLOT_ADJACENT_LAND) && !kPlot.isAdjacentToLand())
		return false;
	if ((eFlags & RANDPLOT_PASSABLE) && kPlot.isImpassable())
		return false;
	if ((eFlags & RANDPLOT_NOT_VISIBLE_TO_CIV) && kPlot.isVisibleToCivTeam())
		return false;
	if ((eFlags & RANDPLOT_NOT_CITY) && kPlot.isCity())
		return false;
	// <advc.300>
	if((eFlags & RANDPLOT_HABITABLE) && kPlot.getYield(YIELD_FOOD) <= 0)
		return false;
	if((eFlags & RANDPLOT_WATERSOURCE) && !kPlot.isFreshWater() &&
		kPlot.getYield(YIELD_FOOD) <= 0)
	{
		return false;
	} // </advc.300>
	return true;
}


CvCity* CvMap::findCity(int iX, int iY, PlayerTypes eOwner, TeamTypes eTeam,
		bool bSameArea, bool bCoastalOnly, TeamTypes eTeamAtWarWith,
		DirectionTypes eDirection, CvCity const* pSkipCity, // advc: const city
		TeamTypes eObserver) const // advc.004r
{
	PROFILE_FUNC();

	int iBestValue = MAX_INT;
	CvCity* pBestCity = NULL;
	for (int i = // <advc.opt> Don't go through all players if eOwner is given
		(eOwner != NO_PLAYER ? eOwner : 0);
		i < (eOwner != NO_PLAYER ? eOwner + 1 : // </advc.opt>
		MAX_PLAYERS); i++) // XXX look for barbarian cities???
	{
		/*if (eOwner != NO_PLAYER && i != eOwner)
			continue;*/
		CvPlayer const& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
		if (!kLoopPlayer.isAlive())
			continue;
		if (eTeam != NO_TEAM && kLoopPlayer.getTeam() != eTeam)
			continue;

		FOR_EACH_CITY_VAR(pLoopCity, kLoopPlayer)
		{	// <advc.004r>
			if(eObserver != NO_TEAM && !pLoopCity->isRevealed(eObserver))
				continue; // </advc.004r>
			if (!bSameArea || pLoopCity->isArea(getPlot(iX, iY).getArea())  ||
				(bCoastalOnly && pLoopCity->waterArea() == getPlot(iX, iY).area()))
			{
				if ((!bCoastalOnly || pLoopCity->isCoastal()) &&
					(eTeamAtWarWith == NO_TEAM || ::atWar(kLoopPlayer.getTeam(), eTeamAtWarWith)) &&
					(eDirection == NO_DIRECTION || estimateDirection(
					dxWrap(pLoopCity->getX() - iX), dyWrap(pLoopCity->getY() - iY)) == eDirection) &&
					(pSkipCity == NULL || pLoopCity != pSkipCity))
				{
					int iValue = plotDistance(iX, iY, pLoopCity->getX(), pLoopCity->getY());
					if (iValue < iBestValue)
					{
						iBestValue = iValue;
						pBestCity = pLoopCity;
					}
				}
			}
		}
	}
	return pBestCity;
}


CvSelectionGroup* CvMap::findSelectionGroup(int iX, int iY, PlayerTypes eOwner,
	bool bReadyToSelect, bool bWorkers) const
{
	int iBestValue = MAX_INT;
	CvSelectionGroup* pBestSelectionGroup = NULL;
	for (int i =  // <advc.opt> Don't go through all players if eOwner is given
		(eOwner != NO_PLAYER ? eOwner : 0);
		i < (eOwner != NO_PLAYER ? eOwner + 1 : // </advc.opt>
		MAX_PLAYERS); i++) // XXX look for barbarian groups???
	{
		/*if (eOwner != NO_PLAYER && i != eOwner)
			continue;*/
		CvPlayer const& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
		if (!kLoopPlayer.isAlive())
			continue;

		FOR_EACH_GROUP_VAR(pLoopSelectionGroup, kLoopPlayer)
		{
			bool const bAIControl = pLoopSelectionGroup->AI_isControlled(); // advc.153
			if (bReadyToSelect && !pLoopSelectionGroup->readyToSelect(
				!bAIControl)) // advc.153: was false
			{
				continue;
			}
			if (bWorkers &&
				// advc.153: with moves
				!pLoopSelectionGroup->hasWorkerWithMoves())
			{
				continue;
			}
			int iValue = plotDistance(iX, iY,
					pLoopSelectionGroup->getX(), pLoopSelectionGroup->getY());
			/*	<advc.153> Select groups where only some units are ready last
				(unless plotDistance is 0) */
			if (!bAIControl && pLoopSelectionGroup->readyToSelect())
				iValue *= 100; // </advc.153>
			if (iValue < iBestValue)
			{
				iBestValue = iValue;
				pBestSelectionGroup = pLoopSelectionGroup;
			}
		}
	}
	return pBestSelectionGroup;
}


CvArea* CvMap::findBiggestArea(bool bWater)
{
	int iBestValue = 0;
	CvArea* pBestArea = NULL;
	FOR_EACH_AREA_VAR(pLoopArea)
	{
		if (pLoopArea->isWater() == bWater)
		{
			int iValue = pLoopArea->getNumTiles();
			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestArea = pLoopArea;
			}
		}
	}
	return pBestArea;
}


int CvMap::getMapFractalFlags() const
{
	CvFractal::Flags eWrapX = CvFractal::NO_FLAGS;
	if (isWrapX())
		eWrapX = CvFractal::FRAC_WRAP_X;

	CvFractal::Flags eWrapY = CvFractal::NO_FLAGS;
	if (isWrapY())
		eWrapY = CvFractal::FRAC_WRAP_Y;
	/*	(advc.enum: Convert to int. It's only used in Python anyway, and
		don't want to include CvFractal.h in CvMap.h.) */
	return (eWrapX | eWrapY);
}

// Check plots for wetlands or seaWater. Returns true if found
bool CvMap::findWater(CvPlot const* pPlot, int iRange, bool bFreshWater) // advc: const CvPlot*
{
	PROFILE_FUNC();

	for (SquareIter it(*pPlot, iRange); it.hasNext(); ++it)
	{
		CvPlot const& kLoopPlot = *it;
		if (bFreshWater)
		{
			if (kLoopPlot.isFreshWater())
				return true;
		}
		else if (kLoopPlot.isWater())
			return true;
	}
	return false;
}


int CvMap::numPlotsExternal() const // advc.inl
{
	return numPlots();
}


int CvMap::pointXToPlotX(float fX) const
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return (int)(((fX + fWidth/2) / fWidth) * getGridWidth());
}


float CvMap::plotXToPointX(int iX) const
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return ((iX * fWidth) / getGridWidth()) - fWidth/2 + GC.getPLOT_SIZE()/2;
}


int CvMap::pointYToPlotY(float fY) const
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return (int)(((fY + fHeight/2) / fHeight) * getGridHeight());
}


float CvMap::plotYToPointY(int iY) const
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return ((iY * fHeight) / getGridHeight()) - fHeight/2 + GC.getPLOT_SIZE()/2;
}


float CvMap::getWidthCoords() const
{
	return GC.getPLOT_SIZE() * getGridWidth();
}


float CvMap::getHeightCoords() const
{
	return GC.getPLOT_SIZE() * getGridHeight();
}

// advc.tsl: Cut from maxPlotDistance
int CvMap::maxPlotDistance(int iGridWidth, int iGridHeight) const
{
	return std::max(1, plotDistance(0, 0,
			isWrapX() ? iGridWidth / 2 : iGridWidth - 1,
			isWrapY() ? iGridHeight / 2 : iGridHeight - 1));
}


int CvMap::maxStepDistance() const
{
	return std::max(1, stepDistance(0, 0,
			isWrapX() ? getGridWidth() / 2 : getGridWidth() - 1,
			isWrapY() ? getGridHeight() / 2 : getGridHeight() - 1));
}

/*	advc.140: Not sure what distance this measures exactly; I'm using it as a
	replacement (everywhere) for maxPlotDistance, with reduced impact of world wraps. */
int CvMap::maxTypicalDistance() const
{
	CvGame const& kGame = GC.getGame();
	scaled rCivRatio(kGame.getRecommendedPlayers(), kGame.getCivPlayersEverAlive());
	// Already factored into getRecommendedPlayers, but I want to give it a little extra weight.
	scaled rSeaLvlModifier = (100 - fixp(2.5) * kGame.getSeaLevelChange()) / 100;
	int iWraps = -1; // 0 if cylindrical (1 wrap), -1 flat, +1 toroidical
	if(isWrapX())
		iWraps++;
	if(isWrapY())
		iWraps++;
	CvWorldInfo const& kWorld = GC.getInfo(getWorldSize());
	scaled r = (kWorld.getGridWidth() * kWorld.getGridHeight() * rCivRatio.sqrt() *
			rSeaLvlModifier).sqrt() * fixp(3.5) - 5 * iWraps;
	return std::max(1, r.round());
}


void CvMap::changeLandPlots(int iChange)
{
	m_iLandPlots += iChange;
	FAssert(getLandPlots() >= 0);
}


void CvMap::changeOwnedPlots(int iChange)
{
	m_iOwnedPlots = (m_iOwnedPlots + iChange);
	FAssert(getOwnedPlots() >= 0);
}


// advc.tsl:
void CvMap::setLatitudeLimits(int iTop, int iBottom)
{
	if (iBottom > iTop)
	{
		FErrorMsg("Invalid latitude limits");
		return;
	}
	if (iTop == getTopLatitude() && iBottom == getBottomLatitude())
		return;
	m_iTopLatitude = iTop;
	m_iBottomLatitude = iBottom;
	FOR_EACH_ENUM(PlotNum)
		getPlotByIndex(eLoopPlotNum).updateLatitude();
}


short CvMap::getNextRiverID() const
{
	return m_iNextRiverID;
}


void CvMap::incrementNextRiverID()
{
	m_iNextRiverID++;
}


bool CvMap::isWrapXExternal() // advc.inl
{
	return isWrapX();
}


bool CvMap::isWrapYExternal() // advc.inl
{
	return isWrapY();
}

bool CvMap::isWrapExternal() // advc.inl
{
	return isWrap();
}


int CvMap::getNumCustomMapOptions() const
{
	return GC.getInitCore().getNumCustomMapOptions();
}


CustomMapOptionTypes CvMap::getCustomMapOption(int iOption) /* advc: */ const
{
	return GC.getInitCore().getCustomMapOption(iOption);
}

// advc.190b: Returns an empty string if the option is set to its default value
CvWString CvMap::getNonDefaultCustomMapOptionDesc(int iOption) const
{
	CvPythonCaller const& py = *GC.getPythonCaller();
	CvString szMapScriptNameNarrow(GC.getInitCore().getMapScriptName());
	CustomMapOptionTypes eOptionValue = getCustomMapOption(iOption);
	int iDefaultValue = py.customMapOptionDefault(szMapScriptNameNarrow.c_str(), iOption);
	// Negative value means that default couldn't be loaded (script may have been removed)
	if (iDefaultValue < 0 || eOptionValue == iDefaultValue)
		return L"";
	return py.customMapOptionDescription(szMapScriptNameNarrow.c_str(), iOption, eOptionValue);
}

/*	advc.108b: Does any custom map option have the value szOptionsValue?
	Checks for an exact match ignoring case unless bCheckContains is set to true
	or bIgnoreCase to false.
	So that the DLL can implement special treatment for particular custom map options
	(that may or may not be present in only one particular map script).
	Translations will have to be handled by the caller (by generating szOptionsValue
	through gDLL->getText). */
bool CvMap::isCustomMapOption(char const* szOptionsValue, bool bCheckContains,
	bool bIgnoreCase) const
{
	CvWString wsOptionsValue(szOptionsValue);
	if (bIgnoreCase)
	{
		// A pain to implement with the (2003) standard library
		boost::algorithm::to_lower(wsOptionsValue);
	}
	CvString szMapScriptNameNarrow(GC.getInitCore().getMapScriptName());
	for (int iOption = 0; iOption < getNumCustomMapOptions(); iOption++)
	{
		CvWString wsOptionDescr = GC.getPythonCaller()->customMapOptionDescription(
				szMapScriptNameNarrow.c_str(), iOption, getCustomMapOption(iOption));
		if (bIgnoreCase)
			boost::algorithm::to_lower(wsOptionDescr);
		if (bCheckContains ? (wsOptionDescr.find(wsOptionsValue) != CvWString::npos) :
			(wsOptionDescr == wsOptionsValue))
		{
			return true;
		}
	}
	return false;
}

/*	For convenience, especially when working with translated strings
	(which use wide characters). */
bool CvMap::isCustomMapOption(CvWString szOptionsValue, bool bCheckContains,
	bool bIgnoreCase) const
{
	CvString szNarrow(szOptionsValue);
	return isCustomMapOption(szNarrow.c_str());
}


int CvMap::getNumBonuses(BonusTypes eIndex) const
{
	return m_aiNumBonus.get(eIndex);
}


void CvMap::changeNumBonuses(BonusTypes eIndex, int iChange)
{
	m_aiNumBonus.add(eIndex, iChange);
	FAssert(getNumBonuses(eIndex) >= 0);
}


int CvMap::getNumBonusesOnLand(BonusTypes eIndex) const
{
	return m_aiNumBonusOnLand.get(eIndex);
}


void CvMap::changeNumBonusesOnLand(BonusTypes eIndex, int iChange)
{
	m_aiNumBonusOnLand.add(eIndex, iChange);
	FAssert(getNumBonusesOnLand(eIndex) >= 0);
}


CvPlot* CvMap::plotByIndexExternal(int iIndex) const // advc.inl
{
	return plotByIndex(iIndex);
}


CvPlot* CvMap::pointToPlot(float fX, float fY)
{
	return plot(pointXToPlotX(fX), pointYToPlotY(fY));
}


int CvMap::getIndexAfterLastArea() const
{
	return m_areas.getIndexAfterLast();
}


int CvMap::getNumLandAreas() const
{
	int iNumLandAreas = 0;
	FOR_EACH_AREA(pLoopArea)
	{
		if (!pLoopArea->isWater())
			iNumLandAreas++;
	}
	return iNumLandAreas;
}


CvArea* CvMap::addArea()
{
	return m_areas.add();
}


void CvMap::deleteArea(int iID)
{
	m_areas.removeAt(iID);
}


void CvMap::recalculateAreas(/* advc.opt: */bool bUpdateIsthmuses)
{
	PROFILE_FUNC();
	// <advc.opt>
	if (bUpdateIsthmuses)
	{
		for (int i = 0; i < numPlots(); i++)
			getPlotByIndex(i).updateAnyIsthmus();
	} // </advc.opt>
	for (int i = 0; i < numPlots(); i++)
	{	// advc.opt: Don't update the old areas, we're about to delete them.
		getPlotByIndex(i).setArea(NULL, false);
	}
	m_areas.removeAll();
	calculateAreas();
	calculateBiomes(); // merk.biome
}


void CvMap::resetPathDistance()
{
	gDLL->getFAStarIFace()->ForceReset(&GC.getStepFinder());
}


int CvMap::calculatePathDistance(CvPlot const* pSource, CvPlot const* pDest) const
{
	if(pSource == NULL || pDest == NULL)
		return -1;
	if (gDLL->getFAStarIFace()->GeneratePath(&GC.getStepFinder(),
		pSource->getX(), pSource->getY(), pDest->getX(), pDest->getY(), false, 0, true))
	{
		FAStarNode* pNode = gDLL->getFAStarIFace()->GetLastNode(&GC.getStepFinder());
		if (pNode != NULL)
			return pNode->m_iData1;
	}
	return -1; // no passable path exists
}

/*	advc.pf: Cut from CvPlot::updateIrrigated
	so that all the non-unit FAStar stuff is in one place */
void CvMap::updateIrrigated(CvPlot& kPlot)
{
	PROFILE_FUNC();

	if (!GC.getGame().isFinalInitialized())
		return;

	/*	advc.opt (note): Perhaps better to use singleton (at CvGlobals) for this?
		Might avoid repeated memory allocation that way. */
	FAStar* pIrrigatedFinder = gDLL->getFAStarIFace()->create();
	if (kPlot.isIrrigated())
	{
		if (!kPlot.isPotentialIrrigation())
		{
			kPlot.setIrrigated(false);
			FOR_EACH_ADJ_PLOT(kPlot)
			{
				bool bFoundFreshWater = false;
				gDLL->getFAStarIFace()->Initialize(pIrrigatedFinder,
						getGridWidth(), getGridHeight(),
						isWrapX(), isWrapY(), NULL, NULL, NULL,
						potentialIrrigation, NULL, checkFreshWater,
						&bFoundFreshWater);
				gDLL->getFAStarIFace()->GeneratePath(pIrrigatedFinder,
						pAdj->getX(), pAdj->getY(), -1, -1);
				if (!bFoundFreshWater)
				{
					bool bIrrigated = false;
					gDLL->getFAStarIFace()->Initialize(pIrrigatedFinder,
							getGridWidth(), getGridHeight(),
							isWrapX(), isWrapY(), NULL, NULL, NULL,
							/*	advc (note): GeneratePath will cause the
								changeIrrigated function to perform the
								updates by calling CvPlot::setIrrigated */
							potentialIrrigation, NULL, changeIrrigated, &bIrrigated);
					gDLL->getFAStarIFace()->GeneratePath(pIrrigatedFinder,
							pAdj->getX(), pAdj->getY(), -1, -1);
				}
			}
		}
	}
	else if (kPlot.isPotentialIrrigation() && kPlot.isIrrigationAvailable(true))
	{
		bool bIrrigated = true;
		gDLL->getFAStarIFace()->Initialize(pIrrigatedFinder,
				getGridWidth(), getGridHeight(),
				isWrapX(), isWrapY(), NULL, NULL, NULL,
				potentialIrrigation, NULL, changeIrrigated, &bIrrigated);
		gDLL->getFAStarIFace()->GeneratePath(pIrrigatedFinder,
				kPlot.getX(), kPlot.getY(), -1, -1);
	}

	gDLL->getFAStarIFace()->destroy(pIrrigatedFinder);
}


// BETTER_BTS_AI_MOD, Efficiency (plot danger cache), 08/21/09, jdog5000: START
void CvMap::invalidateActivePlayerSafeRangeCache()
{
	PROFILE_FUNC();

	for (int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).setActivePlayerSafeRangeCache(-1);
}


void CvMap::invalidateBorderDangerCache(TeamTypes eTeam)
{
	PROFILE_FUNC();

	for(int i = 0; i < numPlots(); i++)
		getPlotByIndex(i).setBorderDangerCache(eTeam, false);
} // BETTER_BTS_AI_MOD: END

// read object from a stream. used during load
void CvMap::read(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Read(&uiFlag);

	CvMapInitData defaultMapData;
	reset(&defaultMapData, /* advc.enum: */ uiFlag >= 7);

	pStream->Read(&m_iGridWidth);
	pStream->Read(&m_iGridHeight);
	// <advc.opt>
	if (uiFlag >= 3)
		pStream->Read((int*)&m_ePlots);
	else updateNumPlots(); // </advc.opt>
	pStream->Read(&m_iLandPlots);
	pStream->Read(&m_iOwnedPlots);
	pStream->Read(&m_iTopLatitude);
	pStream->Read(&m_iBottomLatitude);
	// <advc.opt>
	int iRiver;
	pStream->Read(&iRiver);
	if (iRiver < MIN_SHORT || iRiver > MAX_SHORT)
		m_iNextRiverID = -1;
	else m_iNextRiverID = static_cast<short>(iRiver);
	// </advc.opt>
	pStream->Read(&m_bWrapX);
	pStream->Read(&m_bWrapY);
	if (uiFlag >= 4)
	{
		m_aiNumBonus.read(pStream);
		m_aiNumBonusOnLand.read(pStream);
	}
	else
	{
		m_aiNumBonus.readArray<int>(pStream);
		m_aiNumBonusOnLand.readArray<int>(pStream);
	}
	// <advc.108c>
	if (uiFlag >= 6)
		m_aebBalancedBonuses.read(pStream); // </advc.108c>
	// <advc.enum>
	if (uiFlag >= 7)
	{
		m_aeiPlotExtraYield.read(pStream);
		m_aiPlotExtraCost.read(pStream);
	} // </advc.enum>
	// <advc.304>
	if (uiFlag >= 5)
		GC.getGame().getBarbarianWeightMap().getActivityMap().read(pStream);
	// </advc.304>
	if (numPlots() > 0)
	{
		m_pMapPlots = new CvPlot[numPlots()];
		for (int i = 0; i < numPlots(); i++)
			m_pMapPlots[i].read(pStream);
		// <advc.003s>
		for (int i = 0; i < numPlots(); i++)
			m_pMapPlots[i].initAdjList(); // </advc.003s>
		// <advc.opt>
		if (uiFlag < 2)
		{
			for (int i = 0; i < numPlots(); i++)
				m_pMapPlots[i].updateAnyIsthmus();
		} // </advc.opt>
	}

	ReadStreamableFFreeListTrashArray(m_areas, pStream);
	// <advc> Let the plots know that the areas have been loaded
	for (int i = 0; i < numPlots(); i++)
	{
		plotByIndex(i)->initArea();
	} // </advc>
	setup();
	computeShelves(); // advc.300
	/*  advc.004z: Not sure if this is the ideal place for this, but it works.
		(The problem was that goody huts weren't always highlighted by the
		Resource layer after loading a game.) */
	gDLL->UI().setDirty(GlobeLayer_DIRTY_BIT, true);
	// <advc.106n>
	if (uiFlag > 0)
	{
		size_t iPixels;
		pStream->Read(&iPixels);
		m_replayTexture.reserve(iPixels);
		for (size_t i = 0; i < iPixels; i++)
		{
			byte ucPixel;
			pStream->Read(&ucPixel);
			m_replayTexture.push_back(ucPixel);
		}
	} // </advc.106n>
}


void CvMap::write(FDataStreamBase* pStream)
{
	REPRO_TEST_BEGIN_WRITE("Map");
	uint uiFlag;
	//uiFlag = 1; // advc.106n
	//uiFlag = 2; // advc.opt: CvPlot::m_bAnyIsthmus
	//uiFlag = 3; // advc.opt: m_ePlots
	//uiFlag = 4; // advc.enum: new enum map save behavior
	//uiFlag = 5; // advc.304: Barbarian weight map
	//uiFlag = 6; // advc.108c
	uiFlag = 7; // advc.enum: Extra plot yields, costs moved from CvGame
	pStream->Write(uiFlag);

	pStream->Write(m_iGridWidth);
	pStream->Write(m_iGridHeight);
	pStream->Write(m_ePlots);
	pStream->Write(m_iLandPlots);
	pStream->Write(m_iOwnedPlots);
	pStream->Write(m_iTopLatitude);
	pStream->Write(m_iBottomLatitude);
	pStream->Write((int)m_iNextRiverID); // advc.opt (cast)

	pStream->Write(m_bWrapX);
	pStream->Write(m_bWrapY);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated");
	m_aiNumBonus.write(pStream);
	m_aiNumBonusOnLand.write(pStream);
	/*	advc.108c (Player might save on turn 0, then reload and regenerate the map.
		Therefore this info needs to be saved.) */
	m_aebBalancedBonuses.write(pStream);
	// <advc.enum>
	m_aeiPlotExtraYield.write(pStream);
	m_aiPlotExtraCost.write(pStream); // </advc.enum>
	/*	advc.304: Serialize this for CvGame b/c the map size isn't known
		when CvGame gets deserialized. (kludge) */
	GC.getGame().getBarbarianWeightMap().getActivityMap().write(pStream);
	REPRO_TEST_END_WRITE();
	for (int i = 0; i < numPlots(); i++)
		m_pMapPlots[i].write(pStream);

	WriteStreamableFFreeListTrashArray(m_areas, pStream);
	// <advc.106n>
	pStream->Write(m_replayTexture.size());
	pStream->Write(m_replayTexture.size(), &m_replayTexture[0]);
	// </advc.106n>
}

// used for loading WB maps
void CvMap::rebuild(int iGridW, int iGridH, int iTopLatitude, int iBottomLatitude, bool bWrapX, bool bWrapY, WorldSizeTypes eWorldSize, ClimateTypes eClimate, SeaLevelTypes eSeaLevel, int iNumCustomMapOptions, CustomMapOptionTypes * aeCustomMapOptions)
{
	CvMapInitData initData(iGridW, iGridH, iTopLatitude, iBottomLatitude, bWrapX, bWrapY);

	// Set init core data
	CvInitCore& kInitCore = GC.getInitCore();
	kInitCore.setWorldSize(eWorldSize);
	kInitCore.setClimate(eClimate);
	kInitCore.setSeaLevel(eSeaLevel);
	kInitCore.setCustomMapOptions(iNumCustomMapOptions, aeCustomMapOptions);

	init(&initData); // Init map
}

// advc.opt:
void CvMap::updateNumPlots()
{
	m_ePlots = (PlotNumTypes)(getGridWidth() * getGridHeight());
}

// merk.biome: this maps tiles to biomes based on terrains / features / etc. 
void CvMap::calculateBiomes()
{
	if (getPlotByIndex(0).getTerrainType() == NO_TERRAIN)
		return; // haven't actually placed terrains yet
	resetBiomes(); // just in case
	initBiomes();
	// Gather some settings
	bool bSkipPeaks = (GC.getDefineINT("PEAKS_NO_BIOME") > 0);
	int iPlacementBiome = GC.getDefineINT("INITIAL_PLACEMENT_RULESET_BIOME");
	int iPlacementTile = GC.getDefineINT("INITIAL_PLACEMENT_RULESET_TILE");
	int iFeatureCutoff = GC.getDefineINT("FEATURELEVEL_CUTOFF");
	int iHillCutoff = GC.getDefineINT("HILLLEVEL_CUTOFF");
	int iNonSingleBiomes = 0;
	int iNewBiomes = 0;
	// First pass: add a basic biome to each plot. But first check adjacent plots and add to their biome if same terrain. 
	for (int i = 0; i < numPlots(); i++)
	{
		CvPlot& kPlot = getPlotByIndex(i);
		if (kPlot.isPeak() && bSkipPeaks)
			continue;
		// Right now only the previous tiles will have biomes. So there are several ways we could do this. 
		// Option 1: Just place a new biome on each tile and let the checks sort things out. 
		if (iPlacementBiome == -1)
		{
			addBiomeFromPlot(i);
			iNewBiomes++;
			continue; 
		}
		// Option 2: do an adjacency check just like in biomesAdjCheck, then place new biome if none placed yet. 
		else if (iPlacementBiome == -2)
		{
			int iNewBiome = maxAdjacentBiomeIndex(i, false, GC.getDefineINT("PRIORITIZE_MATCHING_BIOMES"));
			if (isBiomeInRange(iNewBiome))
				setPlotBiome(i, iNewBiome);
			else
				addBiomeFromPlot(i);
			continue;
		}
		// Otherwise, placement will use an adjacency loop and apply certain rules. 
		bool bFound = false;
		FOR_EACH_ADJ_PLOT(kPlot)
		{
			if (pAdj->isPeak() && bSkipPeaks)
				continue;
			int iBiome = getPlotBiomeIndex(pAdj->plotNum());
			if (!isBiomeInRange(iBiome))
				continue;
			// coast / ocean biomes need to be separate, and beaches / rivers are a separate setting anyway, so
			if (!isNewBiomeValid(iBiome, -1, false, i))
				continue;
			// check other placement options via separate method
			if (!isAdjacentRulesetValid(kPlot, pAdj, iBiome, iPlacementBiome, iPlacementTile))
				continue;
			// if we made it to here, then the adjacent plot has a biome we can switch to
			bFound = true;
			setPlotBiome(i, iBiome);
			break;
		}
		if (!bFound) // didn't find any valid biomes, so add a new one
			addBiomeFromPlot(i);
	}
	// debug line
	int fart = (int)(m_Biomes.size());
	// CHECKS
	// First gotta decode the check list
	int iChecklist = GC.getDefineINT("BIOME_CHECK_LIST");
	std::vector< int > aiChecks;
	while (iChecklist > 0)
	{
		int iNextCheck = iChecklist % 10;
		aiChecks.push_back(iNextCheck);
		iChecklist = iChecklist - iNextCheck; // makes sure int division doesn't round up
		iChecklist /= 10;
	}
	for (int c = 0; c < (int)(aiChecks.size()); c++)
	{
		if (aiChecks[c] == 1)
			biomesAdjCheck(GC.getDefineINT("ADJACENCY_RULESET_BIOME"), GC.getDefineINT("ADJACENCY_RULESET_TILE"));
		else if (aiChecks[c] == 2)
			biomesNeighborsCheck();
		else if (aiChecks[c] == 3)
			biomesSizeCheck(GC.getDefineINT("CARVE_UP_RULESET_BIOME"), GC.getDefineINT("CARVE_UP_RULESET_TILE"));
		else if (aiChecks[c] == 4) // backwards standard check
			biomesAdjCheck(GC.getDefineINT("ADJACENCY_RULESET_BIOME"), GC.getDefineINT("ADJACENCY_RULESET_TILE"), true);
		else if (aiChecks[c] == 5) // second ruleset check
			biomesAdjCheck(GC.getDefineINT("SECOND_ADJACENCY_RULESET_BIOME"), GC.getDefineINT("SECOND_ADJACENCY_RULESET_TILE"));
		else if (aiChecks[c] == 6) // backwards second ruleset check
			biomesAdjCheck(GC.getDefineINT("SECOND_ADJACENCY_RULESET_BIOME"), GC.getDefineINT("SECOND_ADJACENCY_RULESET_TILE"), true);
		else if (aiChecks[c] == 7) // flip empty, use first ruleset
			flipEmptyTiles(GC.getDefineINT("ADJACENCY_RULESET_BIOME"), GC.getDefineINT("ADJACENCY_RULESET_TILE"));
		else if (aiChecks[c] == 8) // flip empty, use second ruleset
			flipEmptyTiles(GC.getDefineINT("SECOND_ADJACENCY_RULESET_BIOME"), GC.getDefineINT("SECOND_ADJACENCY_RULESET_TILE"));
		else if (aiChecks[c] == 9) // check biomes to make sure they internally touch, if not, split them up
			biomesFortifyCheck2();

	}
	
	// Debug mode: set plot bonus type equal to the biome. 
	if (GC.getDefineINT("DEBUG_MODE") > 0)
	{
		for (int i = 0; i < (int)(m_aiBiomesMap.size()); i++)
		{
			if (getPlotByIndex(i).getFeatureType() == (FeatureTypes)GC.getInfoTypeForString("FEATURE_ICE"))
				getPlotByIndex(i).setFeatureType(NO_FEATURE);
			getPlotByIndex(i).setBonusType(NO_BONUS);
			if (getPlotByIndex(i).getTerrainType() == NO_TERRAIN)
				continue;
			if (m_aiBiomesMap[i] == -1)
				getPlotByIndex(i).setFeatureType((FeatureTypes)GC.getInfoTypeForString("FEATURE_ICE"));
			if (!isBiomeInRange(m_aiBiomesMap[i]))
				continue;
			if (m_aiBiomesMap[i] <= GC.getNumBonusInfos() - 1)
				getPlotByIndex(i).setBonusType((BonusTypes)m_aiBiomesMap[i]);
			
		}
		// debug line
		int fart = (int)(m_Biomes.size());
	}
}
// uses rulesets defined as encoded prime numbers to determine if adjacent tile / biome should be considered a 'match'. 
// oceans and shallow water are handled elsewhere. Rivers and beaches can also be handled elsewhere optionally, or here. 
bool CvMap::isAdjacentRulesetValid(CvPlot& kPlot, CvPlot_const_t* pAdj, int iBiome, int iPlacementBiome, int iPlacementTile)
{
	if (iPlacementBiome == 1 && iPlacementTile == 1) // 'skip' button
		return true; 
	int iFeatureCutoff = GC.getDefineINT("FEATURELEVEL_CUTOFF");
	int iHillCutoff = GC.getDefineINT("HILLLEVEL_CUTOFF");
	// Gather some info
	bool bMatchTerrain = (kPlot.getTerrainType() == pAdj->getTerrainType());
	bool bMatchFeature = (kPlot.getFeatureType() == pAdj->getFeatureType());
	bool bMatchBiomeTerrain = (kPlot.getTerrainType() == getBiomeTerrain(iBiome));
	bool bMatchBiomeFeature = (kPlot.getFeatureType() == getBiomeFeature(iBiome));
	bool bMatchBiomeFeatureLevelRegard = (bMatchBiomeFeature ? getBiomeFeatureLevel(iBiome) >= iFeatureCutoff : kPlot.getFeatureType() == NO_FEATURE ? getBiomeFeatureLevel(iBiome) <= iFeatureCutoff : false);
	bool bMatchBiomeFeatureLevelDisregardDifferent = (bMatchBiomeFeature ? getBiomeFeatureLevel(iBiome) >= iFeatureCutoff : getBiomeFeatureLevel(iBiome) <= iFeatureCutoff);
	bool bMatchBiomeFeatureLevel = GC.getDefineINT("DISREGARD_NONMATCHING_FEATURES") ? bMatchBiomeFeatureLevelDisregardDifferent : bMatchBiomeFeatureLevelRegard;
	bool bMatchHill = (kPlot.isHills() && pAdj->isHills());
	bool bMatchHillLevel = (kPlot.isHills() ? getBiomeHillLevel(iBiome) >= iHillCutoff : getBiomeHillLevel(iBiome) <= iHillCutoff);
	bool bMatchPeaks = (kPlot.isPeak() && pAdj->isPeak()); // only matters if !bSkipPeaks
	// can apply to rivers / beaches separately from their specific GlobalDefine options
	bool bMatchRivers = (kPlot.isRiver() == pAdj->isRiver());
	bool bMatchBiomeRivers = (kPlot.isRiver() == isBiomeRiver(iBiome));
	bool bMatchBeaches = (kPlot.isCoastalLand() == pAdj->isCoastalLand());
	bool bMatchBiomeBeaches = (kPlot.isCoastalLand() == isBiomeCoast(iBiome));
	// not doing sea stuff because that always makes biome invalid. 

	// The rest of the options are coded into iPlacement, decoded via modulus division.  
	if (iPlacementBiome % 2 == 0 && !bMatchBiomeTerrain)
	{
		return false;
	}
	if (iPlacementBiome % 3 == 0 && !bMatchBiomeFeature)
	{
		return false;
	}
	if (iPlacementBiome % 5 == 0 && !bMatchBiomeFeatureLevel)
	{
		return false;
	}
	if (iPlacementBiome % 7 == 0 && !bMatchHillLevel)
	{
		return false;
	}
	if (iPlacementBiome % 11 == 0 && !bMatchBiomeRivers)
	{
		return false;
	}
	if (iPlacementBiome % 13 == 0 && !bMatchBiomeBeaches)
	{
		return false;
	}
	if (iPlacementTile % 2 == 0 && !bMatchTerrain)
	{
		return false;
	}
	if (iPlacementTile % 3 == 0 && !bMatchFeature)
	{
		return false;
	}
	if (iPlacementTile % 5 == 0 && !bMatchPeaks)
	{
		return false;
	}
	if (iPlacementTile % 7 == 0 && !bMatchHill)
	{
		return false;
	}
	if (iPlacementTile % 11 == 0 && !bMatchRivers)
	{
		return false;
	}
	if (iPlacementTile % 13 == 0 && !bMatchBeaches)
	{
		return false;
	}
	// if made it here, none of the checks failed
	return true;
}
// merk.biome end


// <advc.106n>
void CvMap::updateReplayTexture()
{
	byte* pTexture = gDLL->UI().getMinimapBaseTexture();
	FAssert(pTexture != NULL);
	if (pTexture == NULL)
		return;
	int const iPixels = CvReplayInfo::minimapPixels(GC.getDefineINT(CvGlobals::MINIMAP_RENDER_SIZE));
	m_replayTexture.clear();
	m_replayTexture.reserve(iPixels);
	for (int i = 0; i < iPixels; i++)
		m_replayTexture.push_back(pTexture[i]);
}


byte const* CvMap::getReplayTexture() const
{
	// When in HoF or updateReplayTexture was never called or MINIMAP_RENDER_SIZE has changed
	if (m_replayTexture.size() != CvReplayInfo::minimapPixels(
		GC.getDefineINT(CvGlobals::MINIMAP_RENDER_SIZE)))
	{
		return NULL;
	}
	return &m_replayTexture[0];
} // </advc.106n>


void CvMap::calculateAreas()
{
	PROFILE("CvMap::calculateAreas"); // <advc.030>
	if (GC.getDefineBOOL(CvGlobals::PASSABLE_AREAS))
	{
		/*  Will recalculate from CvGame::setinitialItems once normalization is
			through. But need preliminary areas because normalization is done
			based on areas. Also, some scenarios don't call CvGame::
			setInitialItems; these only get the initial calculation based on
			land, sea and peaks (not ice). */
		calculateAreas_dfs();
		calculateReprAreas();
		return;
	} // </advc.030>
	for (int i = 0; i < numPlots(); i++)
	{
		CvPlot& kLoopPlot = getPlotByIndex(i);
		gDLL->callUpdater();
		if (kLoopPlot.area() == NULL)
		{
			CvArea* pArea = addArea();
			pArea->init(kLoopPlot.isWater());
			kLoopPlot.setArea(pArea);
			gDLL->getFAStarIFace()->GeneratePath(&GC.getAreaFinder(),
					kLoopPlot.getX(), kLoopPlot.getY(), -1, -1,
					kLoopPlot.isWater(), pArea->getID());
		}
	}
	updateLakes(); // advc.030
}

// <advc.030>
class CvAreaAggregator : public PlotVisitor<>
{
protected:
	CvMap& m_kMap;
	CvArea& m_kArea;
public:
	CvAreaAggregator(CvMap& kMap, CvArea& kArea) : m_kMap(kMap), m_kArea(kArea) {}
	bool isVisited(CvPlot const& kPlot) const
	{
		return (kPlot.area() != NULL);
	}
	bool canVisit(CvPlot const& kFrom, CvPlot const& kPlot) const
	{
		return (kFrom.isWater() == kPlot.isWater() &&
				!m_kMap.isSeparatedByIsthmus(kFrom, kPlot) &&
				/*	At an impassable plot, continue only to other impassables
					so that mountain ranges and ice packs end up in one area. */
				(!kFrom.isImpassable() || kPlot.isImpassable()));
	}
	bool visit(CvPlot& kPlot)
	{
		kPlot.setArea(&m_kArea);
		return true;
	}
};

void CvMap::calculateAreas_dfs()
{
	for (int iPass = 0; iPass <= 1; iPass++)
	{
		FOR_EACH_ENUM(PlotNum)
		{
			CvPlot& kPlot = getPlotByIndex(eLoopPlotNum);
			if (kPlot.area() != NULL)
				continue;
			/*	Second pass for impassables; can't handle
				all-peak/ice areas otherwise. */
			if (iPass == 0 && kPlot.isImpassable())
				continue;
			FAssert(iPass == 0 || kPlot.isImpassable());
			CvArea& kArea = *addArea();
			kArea.init(kPlot.isWater());
			CvAreaAggregator aggr(*this, kArea);
			DepthFirstPlotSearch<CvAreaAggregator> dfs(kPlot, aggr);
			gDLL->callUpdater(); // Allow UI to update
		}
	}
}


void CvMap::updateLakes()
{
	// CvArea::getNumTiles no longer sufficient for identifying lakes
	FOR_EACH_AREA_VAR(a)
		a->updateLake();
	for (int i = 0; i < numPlots(); i++)
	{
		CvPlot& kPlot = getPlotByIndex(i);
		if (kPlot.isLake())
			kPlot.updateYield();
	}
	computeShelves(); // advc.300
}


void CvMap::calculateReprAreas()
{
	/*  Still need areas as in BtS for submarine movement. Store at each CvArea
		an area id representing all areas that would be encompassed by the same
		BtS area. To decide if a submarine move is possible, only need to
		check if the representative id of the submarine's current area equals
		that of its target area. That's done in CvArea::canBeEntered. */
	int iLoop = 0;
	int iReprChanged = 0; // For debugging; otherwise a bool would suffice.
	do
	{
		iReprChanged = 0;
		for(int i = 0; i < numPlots(); i++)
		{
			CvPlot& p = getPlotByIndex(i);
			int const x = p.getX();
			int const y = p.getY();
			FOR_EACH_ADJ_PLOT_VAR2(pAdjacent, p)
			{
				CvPlot& q = *pAdjacent;
				// Only orthogonal adjacency for water tiles
				if(p.isWater() && x != q.getX() && y != q.getY())
					continue;
				int const pReprArea = p.getArea().getRepresentativeArea();
				int const qReprArea = q.getArea().getRepresentativeArea();
				if(pReprArea != qReprArea && p.isWater() == q.isWater())
				{
					if(qReprArea < pReprArea)
						p.getArea().setRepresentativeArea(qReprArea);
					else q.getArea().setRepresentativeArea(pReprArea);
					iReprChanged++;
				}
			}
		}
		if(++iLoop > 10)
		{
			FAssert(iLoop <= 10);
			/*  Will have to write a faster algorithm then, based on the BtS code at
				the beginning of this function. That would also make it easier to
				set the lakes. */
			break;
		}
	} while(iReprChanged > 0);
	updateLakes();
} // </advc.030>

// <advc.300>
// All shelves adjacent to a continent
void CvMap::getShelves(CvArea const& kArea, std::vector<Shelf*>& kShelves) const
{
	int const iArea = kArea.getID();
	for(std::map<Shelf::Id,Shelf*>::const_iterator it = m_shelves.begin();
		it != m_shelves.end(); ++it)
	{
		if(it->first.first == iArea)
			kShelves.push_back(it->second);
	}
}


void CvMap::computeShelves()
{
	if (m_shelves.empty() && getLandPlots() <= 0)
		return; // Map still being generated, no need to waste time.
	/*	NB: First call that gets here normally still has no shallow water.
		But that's not guaranteed, so we have to see for ourselves. */
	for (std::map<Shelf::Id,Shelf*>::iterator it = m_shelves.begin();
		it != m_shelves.end(); ++it)
	{
		SAFE_DELETE(it->second);
	}
	m_shelves.clear();
	FOR_EACH_ENUM(PlotNum)
	{
		CvPlot& p = getPlotByIndex(eLoopPlotNum);
		if (p.getTerrainType() != GC.getWATER_TERRAIN(true) ||
			p.isImpassable() || p.isLake() || !p.isHabitable())
		{
			continue;
		}
		// Add plot to shelves of all adjacent land areas
		std::set<int> adjLands;
		FOR_EACH_ADJ_PLOT(p)
		{
			if (!pAdj->isWater())
				adjLands.insert(pAdj->getArea().getID());
		}
		for (std::set<int>::iterator it = adjLands.begin(); it != adjLands.end(); ++it)
		{
			Shelf::Id shelfID(*it, p.getArea().getID());
			std::map<Shelf::Id,Shelf*>::iterator shelfPos = m_shelves.find(shelfID);
			Shelf* pShelf;
			if (shelfPos == m_shelves.end())
			{
				pShelf = new Shelf();
				m_shelves.insert(std::make_pair(shelfID, pShelf));
			}
			else pShelf = shelfPos->second;
			pShelf->add(&p);
		}
	}
} // </advc.300>
// merk.biome begin

// return biome plot index in main list from its tile list
int CvMap::getBiomePlot(int iBiome, int iIndex)
{
	if (iIndex > (int)(m_Biomes[iBiome].tiles.size()) - 1)
		return -1;
	return m_Biomes[iBiome].tiles[iIndex];
}
bool CvMap::isBiomeInRange(int iBiome)
{
	if (iBiome < 0)
		return false;
	if (iBiome > (int)(m_Biomes.size() - 1))
		return false;
	return true;
}
// remove a tile from a biome in the list
void CvMap::removeTile(int iPlot, int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return;
	if (getBiomeSize(iBiome) <= 0)
	{
		if (isPlotInRange(iPlot))
			unBiomePlot(iPlot);
	}
	if (isPlotInRange(iPlot))
	{
		for (int i = 0; i < getBiomeSize(iBiome); i++)
		{
			if (iPlot == getBiomePlot(iBiome, i))
			{
				m_Biomes[iBiome].tiles.erase(m_Biomes[iBiome].tiles.begin() + i);
				unBiomePlot(iPlot);
				return; // all done
			}
		}
	}
}
// add a tile to a biome's list
void CvMap::addTile(int iPlot, int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return;
	if (isPlotInRange(iPlot))
	{
		m_Biomes[iBiome].tiles.push_back(iPlot);
	}
}
// find most common adjacent biome and flip to that
void CvMap::flipToAdjacentBiome(int iPlot, int iBiomeRuleset, int iTileRuleset, bool bExcludeSame)
{
	if (!isPlotInRange(iPlot))
		return;
	// find adjacent biome with all relevant checks
	int iMaxAdjBiomeIndex = maxAdjacentBiomeIndex(iPlot, iBiomeRuleset, iTileRuleset, bExcludeSame, GC.getDefineINT("PRIORITIZE_MATCHING_BIOMES") > 0);
	// make DANG sure it's valid
	if (!isNewBiomeValid(iMaxAdjBiomeIndex, -1, bExcludeSame, iPlot))
		return;
	// if found one: 
	if (isBiomeInRange(iMaxAdjBiomeIndex))
	{
		// if had a previous one
		if (isBiomeInRange(getPlotBiomeIndex(iPlot)))
		{
			if (getBiomeSize(getPlotBiomeIndex(iPlot)) <= 1) // we are all that is left, or it's a weird biome anyway, so kill the whole biome
				removeBiome(getPlotBiomeIndex(iPlot));
			else
			// just remove us from it
				removeTile(iPlot, getPlotBiomeIndex(iPlot));
			
		}
		// set new biome (this method also updates new biome levels but does not change isRiver, isCoast, feature, etc.)
		setPlotBiome(iPlot, iMaxAdjBiomeIndex);
	}
}
void CvMap::addBiome(TerrainTypes eTerrain, FeatureTypes eFeature, int iFeatureLevel, int iHillLevel, bool bRiver, bool bCoast, bool bCoastalSea, bool bOcean)
{
	Biome biome1; 
	biome1.eBiomeTerrain = eTerrain;
	biome1.eBiomeFeature = eFeature;
	biome1.iFeatureLevel = iFeatureLevel;
	biome1.iHillLevel = iHillLevel;
	biome1.bRiver = bRiver;
	biome1.bCoast = bCoast;
	biome1.bCoastalSea = bCoastalSea;
	biome1.bOcean = bOcean;
	m_Biomes.push_back(biome1);
}
void CvMap::addBiomeFromPlot(int iPlot)
{
	if (!isPlotInRange(iPlot))
		return;
	CvPlot& kPlot = getPlotByIndex(iPlot);
	if (kPlot.isPeak() && GC.getDefineINT("PEAKS_NO_BIOME"))
		return;
	addBiome(kPlot.getTerrainType(), kPlot.getFeatureType(), 0, 0, kPlot.isRiver(), kPlot.isCoastalLand(), kPlot.getTerrainType() == GC.getDefineINT("SHALLOW_WATER_TERRAIN"), kPlot.getTerrainType() == GC.getDefineINT("DEEP_WATER_TERRAIN"));
	setPlotBiome(iPlot, (int)m_Biomes.size() - 1);
}
void CvMap::removeBiome(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return;
	m_Biomes.erase(m_Biomes.begin() + iBiome);
	// Have to delete it from tiles referencing it too! 
	// And update everything greater than iBiome to move one down
	for (int i = 0; i < (int)(m_aiBiomesMap.size()); i++)
	{
		if (m_aiBiomesMap[i] == iBiome)
			m_aiBiomesMap[i] = -1;
		else if (m_aiBiomesMap[i] > iBiome)
			m_aiBiomesMap[i] -= 1;
	}
}
int CvMap::getMostSimilarBiome(int iBiome)
{
	// Create list of nearby biomes
	std::vector< int > adjBiomes;
	for (int j = 0; j < getBiomeSize(iBiome); j++)
	{
		int iTileBiome = getPlotBiomeIndex(getBiomePlot(iBiome, j));
		FOR_EACH_ADJ_PLOT(getPlotByIndex(getPlotBiomeIndex(getBiomePlot(iBiome, j))))
		{
			if (getPlotBiomeIndex(pAdj->plotNum()) != iTileBiome && isBiomeInRange(getPlotBiomeIndex(pAdj->plotNum())))
				adjBiomes.push_back(getPlotBiomeIndex(pAdj->plotNum()));
		}
	}
	if ((int)adjBiomes.size() > 0)
	{
		TerrainTypes eCompareTerrain = getBiomeTerrain(iBiome);
		FeatureTypes eCompareFeature = getBiomeFeature(iBiome);
		bool bRiver = isBiomeRiver(iBiome);
		bool bCoast = isBiomeCoast(iBiome);
		bool bCoastalSea = isBiomeCoastalSea(iBiome);
		int iHillLevel = getBiomeHillLevel(iBiome);
		int iFeatureLevel = getBiomeFeatureLevel(iBiome);
		bool bOcean = isBiomeOcean(iBiome);
		int iMaxScore = 0;
		int iBestBiome = -1;
		int iDist = GC.getDefineINT("LEVEL_SIMILARITY");
		for (int i = 0; i < (int)(adjBiomes.size()); i++)
		{
			int iNewBiome = adjBiomes[i];
			if (!isBiomeInRange(iNewBiome))
				continue;
			// non-negotiables
			if (isBiomeOcean(iNewBiome) != bOcean)
				continue;
			if (isBiomeCoastalSea(iNewBiome) != bCoastalSea)
				continue;
			if (isBiomeRiver(iNewBiome) != bRiver && GC.getDefineINT("KEEP_RIVER_BIOMES_SEPARATE"))
				continue;
			if (isBiomeCoast(iNewBiome) != bCoast && GC.getDefineINT("KEEP_COASTAL_BIOMES_SEPARATE"))
				continue;
			int iScore = 0;
			if (getBiomeTerrain(iNewBiome) == eCompareTerrain)
				iScore++;
			if (getBiomeFeature(iNewBiome) == eCompareFeature)
				iScore++;
			if (getBiomeFeatureLevel(iNewBiome) - iFeatureLevel <= iDist && (GC.getDefineINT("DISREGARD_NONMATCHING_FEATURES") || getBiomeFeature(iNewBiome) == eCompareFeature))
				iScore++;
			if (isBiomeCoast(iNewBiome) == bCoast)
				iScore++;
			if (isBiomeRiver(iNewBiome) == bRiver)
				iScore++;
			if (getBiomeHillLevel(iNewBiome) - iHillLevel <= iDist)
				iScore++;

			if (iScore > iMaxScore)
			{
				iMaxScore = iScore;
				iBestBiome = iNewBiome;
			}
		}
		if (isBiomeInRange(iBestBiome))
			return iBestBiome;
		else // just return the first one, gotta have one
			return adjBiomes[0];
	}
	// if got to here, that means there are no adjacent biomes. 
	// soooo
	return iBiome;
}
// count tiles of the given biome adjacent to this plot
int CvMap::countAdjacentBiomeTiles(int iPlot, int iCountBiome)
{
	if (!isPlotInRange(iPlot))
		return -1;
	if (!isBiomeInRange(iCountBiome))
		return 0;
	int iCount = 0;
	FOR_EACH_ADJ_PLOT(getPlotByIndex(iPlot))
	{
		if (pAdj->isPeak() && GC.getDefineINT("PEAKS_NO_BIOME"))
			continue;
		int iAdj = pAdj->plotNum();
		if (getPlotBiomeIndex(iAdj) == iCountBiome)
			iCount++;
	}
	return iCount;
}
// returns the most common adjacent biome
int CvMap::maxAdjacentBiomeIndex(int iPlot, int iBiomeRuleset, int iTileRuleset, bool bExcludeSame, bool bSharedWinsTies)
{
	if (!isPlotInRange(iPlot))
		return -1;
	int iMax = 0;
	int iMaxBiome = -1;
	std::vector< int > iTiedBiomes;
	std::vector < std::pair< int, int > > adjBiomes;
	int iOriginalBiome = getPlotBiomeIndex(iPlot);
	FOR_EACH_ADJ_PLOT(getPlotByIndex(iPlot))
	{
		int iAdjBiome = getPlotBiomeIndex(pAdj->plotNum());
		if (!isNewBiomeValid(iAdjBiome, iOriginalBiome, bExcludeSame, iPlot))
			continue;
		// check using rulesets
		if (!isAdjacentRulesetValid(getPlotByIndex(iPlot), pAdj, iAdjBiome, iBiomeRuleset, iTileRuleset))
			continue;
		bool bFound = false;
		for (int i = 0; i < (int)(adjBiomes.size()); i++)
		{
			if (adjBiomes[i].first == iAdjBiome)
			{
				adjBiomes[i].second++;
				if (adjBiomes[i].second > iMax)
				{
					iTiedBiomes.clear();
					iMax = adjBiomes[i].second;
					iMaxBiome = adjBiomes[i].first;
				}
				else if (adjBiomes[i].second == iMax)
					iTiedBiomes.push_back(adjBiomes[i].first);
				bFound = true;
				break;
			}
		}
		if (!bFound)
		{
			std::pair< int, int > newBiome;
			newBiome.first = iAdjBiome;
			newBiome.second = 1;
			adjBiomes.push_back(newBiome);
			if (iMax < 1)
			{
				iMaxBiome = iAdjBiome;
				iTiedBiomes.clear();
				iMax = 1;
			}
		}
	}
	if ((int)(iTiedBiomes.size()) > 0 && bSharedWinsTies)
	{
		// I changed the most similar method and that sort of broke the tie functionality but I think it's better anyway
		return getMostSimilarBiome(iOriginalBiome);
	}
	else
		return iMaxBiome; // ignore ties unless we are prioritizing similar biomes
}
bool CvMap::isNewBiomeValid(int iAdjBiome, int iOriginalBiome, bool bExcludeSame, int iPlot)
{
	if (!isBiomeInRange(iAdjBiome))
	{
		return false;
	}
	if (isBiomeInRange(iOriginalBiome))
	{
		if (iAdjBiome == iOriginalBiome && bExcludeSame)
		{
			return false;
		}
		// If the biomes don't match on certain things we can't count the new one:
		if (!(isBiomeCoastalSea(iOriginalBiome) == isBiomeCoastalSea(iAdjBiome)))
		{
			return false;
		}
		if (!(isBiomeOcean(iOriginalBiome) == isBiomeOcean(iAdjBiome)))
		{
			return false;
		}
		if (!(isBiomeRiver(iOriginalBiome) == isBiomeRiver(iAdjBiome)) && GC.getDefineINT("KEEP_RIVER_BIOMES_SEPARATE"))
		{
			return false;
		}
		if (!(isBiomeCoast(iOriginalBiome) == isBiomeCoast(iAdjBiome)) && GC.getDefineINT("KEEP_COASTAL_BIOMES_SEPARATE"))
		{
			return false;
		}
		return true;
	}
	else
	{
		// focus tile has no biome, but still should not flip it to certain biomes
		CvPlot& kp = getPlotByIndex(iPlot);
		if (isBiomeOcean(iAdjBiome) && !(kp.getTerrainType() == GC.getDefineINT("DEEP_WATER_TERRAIN")))
		{
			return false;
		}
		if (isBiomeCoastalSea(iAdjBiome) && !(kp.isAdjacentToLand()))
		{
			return false;
		}
		if (isBiomeCoast(iAdjBiome) && !(kp.isCoastalLand()) && GC.getDefineINT("KEEP_COASTAL_BIOMES_SEPARATE"))
		{
			return false;
		}
		if (isBiomeRiver(iAdjBiome) && !(kp.isRiver()) && GC.getDefineINT("KEEP_RIVER_BIOMES_SEPARATE"))
		{
			return false;
		}
		return true;
	}
}
// sends all tiles from a biome to another biome
void CvMap::mergeBiome(int iBiome, int iNewBiome)
{
	if (iBiome == iNewBiome)
		return;
	if (!isBiomeInRange(iBiome) || !isBiomeInRange(iNewBiome))
		return;
	for (int i = 0; i < (getBiomeSize(iBiome)); i++)
	{
		setPlotBiome(m_Biomes[iBiome].tiles[i], iNewBiome);
	}
	removeBiome(iBiome);
}



void CvMap::setBiomeTerrain(int iBiome, TerrainTypes eTerrain)
{
	if (!isBiomeInRange(iBiome))
		return;
	m_Biomes[iBiome].eBiomeTerrain = eTerrain;
}

void CvMap::setBiomeFeature(int iBiome, FeatureTypes eFeature)
{
	if (!isBiomeInRange(iBiome))
		return;
	m_Biomes[iBiome].eBiomeFeature = eFeature;
}

void CvMap::setBiomeFeatureLevel(int iBiome, int iFeatureLevel)
{
	if (!isBiomeInRange(iBiome))
		return;
	m_Biomes[iBiome].iFeatureLevel = iFeatureLevel;
}

void CvMap::setBiomeHillLevel(int iBiome, int iHillLevel)
{
	if (!isBiomeInRange(iBiome))
		return;
	m_Biomes[iBiome].iHillLevel = iHillLevel;
}

void CvMap::setBiomeTypes(int iBiome, bool bRiver, bool bCoast, bool bCoastalSea, bool bOcean)
{
	if (!isBiomeInRange(iBiome))
		return;
	m_Biomes[iBiome].bRiver = bRiver;
	m_Biomes[iBiome].bCoast = bCoast;
	m_Biomes[iBiome].bCoastalSea = bCoastalSea;
	m_Biomes[iBiome].bOcean = bOcean;
}

TerrainTypes CvMap::getBiomeTerrain(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return NO_TERRAIN;
	return m_Biomes[iBiome].eBiomeTerrain;
}

FeatureTypes CvMap::getBiomeFeature(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return NO_FEATURE;
	return m_Biomes[iBiome].eBiomeFeature;
}

int CvMap::getBiomeFeatureLevel(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return -1;
	return m_Biomes[iBiome].iFeatureLevel;
}

int CvMap::getBiomeHillLevel(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return -1;
	return m_Biomes[iBiome].iHillLevel;
}

bool CvMap::isBiomeRiver(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return false;
	return m_Biomes[iBiome].bRiver;
}

bool CvMap::isBiomeCoast(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return false;
	return m_Biomes[iBiome].bCoast;
}

bool CvMap::isBiomeCoastalSea(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return false;
	return m_Biomes[iBiome].bCoastalSea;
}

bool CvMap::isBiomeOcean(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return false;
	return m_Biomes[iBiome].bOcean;
}

int CvMap::getBiomeSize(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return -1;
	return (int)(m_Biomes[iBiome].tiles.size());
}
// changes plot's tracked biome and updates biome lists 
void CvMap::setPlotBiome(int iPlot, int iNewBiome)
{
	if (!isPlotInRange(iPlot))
		return;
	if (!isBiomeInRange(iNewBiome))
		return;
	m_aiBiomesMap[iPlot] = iNewBiome;
	addTile(iPlot, iNewBiome);
	updateBiomeCharacteristics(iNewBiome);
}

// splits up a biome and divides tiles among adjacent ones
void CvMap::carveUpBiome(int iBiome, int iBiomeRuleset, int iTileRuleset)
{
	if (!isBiomeInRange(iBiome))
		return;
	for (int i = 0; i < getBiomeSize(iBiome); i++)
	{
		flipToAdjacentBiome(getBiomePlot(iBiome, i), iBiomeRuleset, iTileRuleset, true);
	}
	removeBiome(iBiome);
}
// resets biome of a plot
void CvMap::unBiomePlot(int iPlot)
{
	if (!isPlotInRange(iPlot))
		return;
	m_aiBiomesMap[iPlot] = -1;
}

// adjusts iFeatureLevel and iHillLevel for the biome
void CvMap::updateBiomeCharacteristics(int iBiome)
{
	if (!isBiomeInRange(iBiome))
		return;
	if (getBiomeSize(iBiome) <= 0)
		return;
	int iFeatures = 0;
	int iHills = 0;
	// if no feature, let's set to the most common feature if any
	if (getBiomeFeature(iBiome) == NO_FEATURE)
	{
		bool bAny = false;
		ListEnumMap<FeatureTypes,int> featurelist;
		for (int t = 0; t < (int)(m_Biomes[iBiome].tiles.size()); t++)
		{
			CvPlot& kPlot = getPlotByIndex(getBiomePlot(iBiome, t));
			if (kPlot.getFeatureType() != NO_FEATURE)
			{
				bAny = true;
				featurelist.add(kPlot.getFeatureType(), 1);
			}
		}
		if (bAny)
		{
			int iMax = 0;
			FeatureTypes eWinner = NO_FEATURE;
			FOR_EACH_ENUM(Feature)
			{
				if (featurelist.get(eLoopFeature) > iMax)
				{
					eWinner = eLoopFeature;
					iMax = featurelist.get(eLoopFeature);
				}
			}
			setBiomeFeature(iBiome, eWinner);
		}
	}
	// same with terrain
	if (getBiomeTerrain(iBiome) == NO_TERRAIN)
	{
		bool bCoastal = false;
		bool bCoastalSea = false;
		bool bOcean = false; 
		bool bRiver = false;
		int iRivers = 0;
		int iBeaches = 0;
		bool bAny = false;
		ListEnumMap<TerrainTypes, int> Terrainlist;
		for (int t = 0; t < (int)(m_Biomes[iBiome].tiles.size()); t++)
		{
			CvPlot& kPlot = getPlotByIndex(getBiomePlot(iBiome, t));
			if (kPlot.getTerrainType() != NO_TERRAIN)
			{
				bAny = true;
				Terrainlist.add(kPlot.getTerrainType(), 1);
			}
			if (kPlot.isRiver())
				iRivers++;
			if (kPlot.isCoastalLand())
				iBeaches++;
		}
		if (bAny)
		{
			int iMax = 0;
			TerrainTypes eWinner = NO_TERRAIN;
			FOR_EACH_ENUM(Terrain)
			{
				if (Terrainlist.get(eLoopTerrain) > iMax)
				{
					eWinner = eLoopTerrain;
					iMax = Terrainlist.get(eLoopTerrain);
				}
			}
			setBiomeTerrain(iBiome, eWinner);
			if (eWinner == GC.getDefineINT("SHALLOW_WATER_TERRAIN"))
				bCoastalSea = true;
			if (eWinner == GC.getDefineINT("DEEP_WATER_TERRAIN"))
				bOcean = true;
			if ((iRivers * 100) / getBiomeSize(iBiome) >= GC.getDefineINT("PERCENT_RIVERS"))
				bRiver = true;
			if ((iBeaches * 100) / getBiomeSize(iBiome) >= GC.getDefineINT("PERCENT_BEACHES"))
				bCoastal = true;
			setBiomeTypes(iBiome, bRiver, bCoastal, bCoastalSea, bOcean);
		}
		
	}
	for (int i = 0; i < getBiomeSize(iBiome); i++)
	{
		if (!isPlotInRange(getBiomePlot(iBiome, i)))
			continue;
		if (getPlotByIndex(getBiomePlot(iBiome, i)).getFeatureType() == getBiomeFeature(iBiome))
			iFeatures++;
		if (getPlotByIndex(getBiomePlot(iBiome, i)).isHills())
			iHills++;
	}
	int iFeaturePercent = 100 * iFeatures / getBiomeSize(iBiome);
	int iHillsPercent = 100 * iFeatures / getBiomeSize(iBiome);
	if (getBiomeFeature(iBiome) == NO_FEATURE)
		setBiomeFeatureLevel(iBiome, 0);
	else if (iFeaturePercent < GC.getDefineINT("FEATURE_LEVEL_2_PERCENT"))
		setBiomeFeatureLevel(iBiome, 0);
	else if (iFeaturePercent < GC.getDefineINT("FEATURE_LEVEL_3_PERCENT"))
		setBiomeFeatureLevel(iBiome, 1);
	else if (iFeaturePercent < GC.getDefineINT("FEATURE_LEVEL_4_PERCENT"))
		setBiomeFeatureLevel(iBiome, 2);
	else if (iFeaturePercent < GC.getDefineINT("FEATURE_LEVEL_5_PERCENT"))
		setBiomeFeatureLevel(iBiome, 3);
	else
		setBiomeFeatureLevel(iBiome, 4);
	if (iHillsPercent < GC.getDefineINT("HILL_LEVEL_2_PERCENT"))
		setBiomeHillLevel(iBiome, 0);
	else if (iHillsPercent < GC.getDefineINT("HILL_LEVEL_3_PERCENT"))
		setBiomeHillLevel(iBiome, 1);
	else if (iHillsPercent < GC.getDefineINT("HILL_LEVEL_4_PERCENT"))
		setBiomeHillLevel(iBiome, 2);
	else if (iHillsPercent < GC.getDefineINT("HILL_LEVEL_5_PERCENT"))
		setBiomeHillLevel(iBiome, 3);
	else
		setBiomeHillLevel(iBiome, 4);
}

void CvMap::resetBiomes()
{
	m_aiBiomesMap.clear();
	m_Biomes.clear();
}

void CvMap::initBiomes()
{
	for (int i = 0; i < numPlots(); i++)
	{
		m_aiBiomesMap.push_back(-1);
	}
}

// go through all tiles and flip to adjacent if there are not enough
void CvMap::biomesAdjCheck(int iBiomeRuleset, int iTileRuleset, bool bBackwards)
{
	int flips = 0;
	int shouldflip = 0;
	if (bBackwards)
	{
		for (int i = numPlots() - 1; i >= 0; i--)
		{
			if (getPlotByIndex(i).isPeak() && GC.getDefineINT("PEAKS_NO_BIOME"))
				continue;
			int iNumAdj = countAdjacentBiomeTiles(i, getPlotBiomeIndex(i));
			if (iNumAdj < GC.getDefineINT("MIN_ADJ_SHARE"))
			{
				int iOriginalBiome = getPlotBiomeIndex(i);
				shouldflip++;
				flipToAdjacentBiome(i, iBiomeRuleset, iTileRuleset, true);
				if (iOriginalBiome != getPlotBiomeIndex(i))
					flips++;
			}
		}
	}
	else
	{
		for (int i = 0; i < numPlots(); i++)
		{
			if (getPlotByIndex(i).isPeak() && GC.getDefineINT("PEAKS_NO_BIOME"))
				continue;
			int iNumAdj = countAdjacentBiomeTiles(i, getPlotBiomeIndex(i));
			if (iNumAdj < GC.getDefineINT("MIN_ADJ_SHARE"))
			{
				int iOriginalBiome = getPlotBiomeIndex(i);
				shouldflip++;
				flipToAdjacentBiome(i, iBiomeRuleset, iTileRuleset, true);
				if (iOriginalBiome != getPlotBiomeIndex(i))
					flips++;
			}
		}
	}
	// debug line
	int fart = (int)(m_Biomes.size());
}

void CvMap::biomesSizeCheck(int iBiomeRuleset, int iTileRuleset)
{
	int kills = 0;
	int merges = 0;
	for (int i = 0; i < (int)(m_Biomes.size()); i++)
	{
		if (getBiomeSize(i) < GC.getDefineINT("MIN_BIOME_SIZE"))
		{
			if (getBiomeSize(i) <= GC.getDefineINT("MERGE_INSTEAD_OF_CARVE_CUTOFF"))
			{
				int iNewBiome = getMostSimilarBiome(i);
				if (iNewBiome == i)
				{
					// just carve it up
					carveUpBiome(i, iBiomeRuleset, iTileRuleset);
					kills++;
					i--;
					continue;
				}
				mergeBiome(i, iNewBiome);
				merges++;
			}
			else
			{
				carveUpBiome(i, iBiomeRuleset, iTileRuleset);
				kills++;
			}
			// Either way, old biome is gone, so need to go back 1 
			i--;
		}
	}
	// debug line
	int fart = (int)(m_Biomes.size());
}
// loop through biomes and merge with neighbors who are identical
void CvMap::biomesNeighborsCheck()
{
	int iDist = GC.getDefineINT("LEVEL_SIMILARITY");
	int iNumMerges = 0;
	for (int a = 0; a < (int)(m_Biomes.size()); a++)
	{
		for (int i = 0; i < getBiomeSize(a); i++)
		{
			FOR_EACH_ADJ_PLOT(getPlotByIndex(getBiomePlot(a, i)))
			{
				int b = getPlotBiomeIndex(pAdj->plotNum());
				if (!isBiomeInRange(b) || b == a)
					continue;
				if (getBiomeTerrain(a) == getBiomeTerrain(b) && getBiomeFeature(a) == getBiomeFeature(b) && (getBiomeFeatureLevel(a) - getBiomeFeatureLevel(b)) <= iDist && (getBiomeHillLevel(a) - getBiomeHillLevel(b)) <= iDist && isBiomeRiver(a) == isBiomeRiver(b) && isBiomeCoast(a) == isBiomeCoast(b) && isBiomeOcean(a) == isBiomeOcean(b) && isBiomeCoastalSea(a) == isBiomeCoastalSea(b))
				{
					// these biomes are the same
					mergeBiome(b, a);
					// go back to beginning of list
					a = -1;
					iNumMerges++;
					break;
				}
			}
			if (a == -1)
				break;
		}
	}
	// debug line
	int fart = (int)(m_Biomes.size());
}
// simply finds empty tiles and flips them to a near one. 
void CvMap::flipEmptyTiles(int iBiomeRuleset, int iTileRuleset)
{
	int flips = 0;
	int shouldflip = 0;
	for (int i = 0; i < numPlots(); i++)
	{
		if (getPlotByIndex(i).isPeak() && GC.getDefineINT("PEAKS_NO_BIOME"))
			continue;
		if (getPlotBiomeIndex(i) != -1)
			continue;
		shouldflip++;
		// It's empty. Flip it:
		flipToAdjacentBiome(i, iBiomeRuleset, iTileRuleset, true);
		if (getPlotBiomeIndex(i) != -1)
			flips++;
	}
	// debug line
	int fart = (int)(m_Biomes.size());
}

// check each biome to make sure all its tiles are connected
void CvMap::biomesFortifyCheck() // named after Risk fortify move
{
	int inewbiomes = 0;
	int iflips = 0;
	int shouldflips = 0;
	// Loop through each biome,
	for (int biome = 0; biome < (int)(m_Biomes.size()); biome++)
	{
		// And each tile in each biome
		std::vector< std::vector< int > > sortedTiles;
		for (int tile = 0; tile < getBiomeSize(biome); tile++)
		{
			int iTile = getBiomePlot(biome, tile);
			int iSorted = 0;
			std::vector< int > mergeLists;
			// check against our list we have made so far:
			for (int tlist = 0; tlist < (int)(sortedTiles.size()); tlist++)
			{
				for (int checktile = 0; checktile < (int)(sortedTiles[tlist].size()); checktile++)
				{
					int iCheckTile = sortedTiles[tlist][checktile];
					if (iTile == iCheckTile)
						continue;
					if (adjacentOrSame(getPlotByIndex(iTile), getPlotByIndex(iCheckTile)))
					{
						// sort it into the list.
						sortedTiles[tlist].push_back(iTile);
						iSorted++;
					}
				}
				if (iSorted > 0)
					mergeLists.push_back(tlist);
			}
			if (iSorted == 0)
			{
				// This means we made it all the way through our current list without finding something it is adjacent to. 
				// So, add a new list. 
				std::vector< int > newlist;
				newlist.push_back(iTile);
				sortedTiles.push_back(newlist);
			}
			else if ((int)(mergeLists.size()) > 1)
			{
				// This means the tile was adjacent to multiple different groups of tiles, which is good. Combine those lists. 
				for (int merg = 1; merg < (int)(mergeLists.size()); merg++)
				{
					for (int listtile = 0; listtile < (int)(sortedTiles[mergeLists[merg]].size()); listtile++)
					{
						sortedTiles[mergeLists[0]].push_back(sortedTiles[mergeLists[merg]][listtile]); // wow that's a fun line
						// mergeLists itself will just disappear into oblivion so we don't need to pop or erase or nothin
					}
					sortedTiles.erase(sortedTiles.begin() + mergeLists[merg]);
					// That decreases the index of all further lists by 1, so update mergeLists:
					for (int next = merg; next < (int)(mergeLists.size()); next++)
					{
						mergeLists[next]--;
					}
				}
				
			}
		}
		// Now we've sorted tiles out by what they are adjacent to. Good golly gee. 
		if ((int)(sortedTiles.size()) > 1)
		{
			// That means there are two groups of tiles that are not interconnected. 
			// Time to split the biome up. Skip the first group in the list. 
			for (int newbi = 1; newbi < (int)(sortedTiles.size()); newbi++)
			{
				int iPreviousIndex = (int)(m_Biomes.size() - 1);
				addBiomeFromPlot(sortedTiles[newbi][0]);
				int iNewBiome = (int)(m_Biomes.size()) - 1;
				if (iPreviousIndex != iNewBiome)
				{
					// Something went wrong with adding a new biome. 
					int IdkWhatToDo = true;
				}
				else
				{
					inewbiomes++;
					for (int newti = 1; newti < (int)(sortedTiles[newbi].size()); newti++)
					{
						shouldflips++;
						setPlotBiome(sortedTiles[newbi][newti], iNewBiome);
						if (getPlotBiomeIndex(sortedTiles[newbi][newti]) != biome) // yeah we're still in that loop btw
							iflips++;
					}
				}
			}
		}
	}
	// debug line
	int fart = (int)(m_Biomes.size());
}

// simply clears biomes, then runs through tiles and adds them to biomes
void CvMap::biomesFortifyCheck2()
{
	m_Biomes.clear();
	int iBiomes = 0;
	std::vector< int > newBiomesMap;
	for (int i = 0; i < numPlots(); i++)
		newBiomesMap.push_back(-1);
	for (int i = 0; i < numPlots(); i++)
	{
		if (getPlotByIndex(i).isPeak() && GC.getDefineINT("PEAKS_NO_BIOME"))
			continue;
		int iBiome = m_aiBiomesMap[i];
		bool bFoundAdj = false;
		FOR_EACH_ADJ_PLOT(getPlotByIndex(i))
		{
			int iAdjBiome = m_aiBiomesMap[pAdj->plotNum()];
			if (iBiome == iAdjBiome && newBiomesMap[pAdj->plotNum()] > -1)
			{
				newBiomesMap[i] = newBiomesMap[pAdj->plotNum()];
				bFoundAdj = true;
				break;
			}
		}
		if (!bFoundAdj)
		{
			// couldn't find adjacent tile with a newBiomesMap > -1
			// so, start one
			newBiomesMap[i] = iBiomes;
			// also add the biome to m_biomes
			Biome biomey;
			m_Biomes.push_back(biomey);
			iBiomes++;
		}
	}
	// Now run through the list again and setPlotBiome to make it official
	for (int i = 0; i < numPlots(); i++)
	{
		if (getPlotByIndex(i).isPeak() && GC.getDefineINT("PEAKS_NO_BIOME"))
			continue;
		setPlotBiome(i, newBiomesMap[i]); // this takes care of all the biome characteristics and everything. neet. 
	}
	// debug line
	int fart = (int)(m_Biomes.size());
}


// merk.biome end
