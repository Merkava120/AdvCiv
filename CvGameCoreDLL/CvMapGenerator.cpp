#include "CvGameCoreDLL.h"
#include "CvMapGenerator.h"
#include "CvGame.h"
#include "PlotRange.h"
#include "CvArea.h" // advc.003s
#include "CvFractal.h"
#include "CvInfo_Terrain.h"
#include "CvInfo_GameOption.h"


CvMapGenerator* CvMapGenerator::m_pInst = NULL; // static


CvMapGenerator& CvMapGenerator::GetInstance() // singleton accessor
{
	if (m_pInst == NULL)
		m_pInst = new CvMapGenerator;
	return *m_pInst;
}


bool CvMapGenerator::canPlaceBonusAt(BonusTypes eBonus, int iX, int iY,  // refactored
	bool bIgnoreLatitude, /* advc.129: */ bool bCheckRange) const
{
	PROFILE_FUNC();

	CvMap const& kMap = GC.getMap();
	CvPlot const* pPlot = kMap.plot(iX, iY);
	if(pPlot == NULL)
		return false;
	CvPlot const& p = *pPlot;
	CvArea const& kArea = p.getArea();

	if (!p.canHaveBonus(eBonus, bIgnoreLatitude))
		return false;

	{
		bool bOverride=false;
		bool r = GC.getPythonCaller()->canPlaceBonusAt(p, bOverride);
		if (bOverride)
			return r;
	}

	CvBonusInfo const& kBonus = GC.getInfo(eBonus);

	if (p.isWater())
	{
		if (((kMap.getNumBonusesOnLand(eBonus) * 100) /
			(kMap.getNumBonuses(eBonus) + 1)) <
			kBonus.getMinLandPercent())
		{
			return false;
		}
	}
	// <advc.129>
	if (!bCheckRange)
		return true; // </advc.129>

	FOR_EACH_ADJ_PLOT(p)
	{
		BonusTypes eLoopBonus = pAdj->getBonusType();
		if (eLoopBonus != NO_BONUS && eLoopBonus != eBonus)
			return false;
	}

	int const iBonusClassRange = GC.getInfo(kBonus.getBonusClassType()).
			getUniqueRange();
	int const iBonusRange = kBonus.getUniqueRange();
	for (PlotCircleIter it(p, std::max(iBonusClassRange, iBonusRange));
		it.hasNext(); ++it)
	{
		CvPlot const& kLoopPlot = *it;
		if (!kLoopPlot.isArea(kArea))
			continue;
		BonusTypes eOtherBonus = kLoopPlot.getBonusType();
		if (eOtherBonus == NO_BONUS)
			continue;
		int iDist = it.currPlotDist();
		// Make sure there are none of the same bonus nearby:
		if (eBonus == eOtherBonus && iDist <= iBonusRange)
			return false;
		// Make sure there are no bonuses of the same class nearby:
		if (GC.getInfo(eOtherBonus).getBonusClassType() ==
			kBonus.getBonusClassType() && iDist <= iBonusClassRange)
		{
			return false;
		}
	}

	// <advc.129> Prevent more than one adjacent copy regardless of range.
	int iFound = 0;
	FOR_EACH_ADJ_PLOT(p)
	{
		if (!pAdj->isArea(kArea))
			continue;
		if (pAdj->getBonusType() == eBonus)
		{
			iFound++;
			if (iFound >= 2)
				return false;
			/*  A single adjacent copy could already have another adjacent copy.
				However, if that's prohibited, clusters of more than 2 resources
				won't be placed at all. (They're only placed around one central
				tile, which also gets the resource.) Better to change the placement
				pattern then (addUniqueBonusType). */
			/*FOR_EACH_ADJ_PLOT2(pAdjAdj, *pAdj) {
				if(pAdjAdj->isArea(kArea) && pAdjAdj->getBonusType() == eBonus)
					return false;
			}*/
		}
	} // </advc.129>

	return true;
}

// advc: param renamed from 'eImprovement'; const
bool CvMapGenerator::canPlaceGoodyAt(ImprovementTypes eGoody, int iX, int iY) const
{
	PROFILE_FUNC();

	FAssert(eGoody != NO_IMPROVEMENT);
	FAssert(GC.getInfo(eGoody).isGoody());

	if (GC.getGame().isOption(GAMEOPTION_NO_GOODY_HUTS))
		return false;

	CvPlot const* p = GC.getMap().plot(iX, iY);
	// <advc> May get called from Python; better check p.
	if (p == NULL)
		return false; // </advc>
	if (!p->canHaveImprovement(eGoody, NO_TEAM))
		return false;
	{
		bool bOverride=false;
		bool r = GC.getPythonCaller()->canPlaceGoodyAt(*p, bOverride);
		if (bOverride)
			return r;
	}
	if (p->isImproved() || p->getBonusType() != NO_BONUS || p->isImpassable())
		return false;

	int iUniqueRange = GC.getInfo(eGoody).getGoodyUniqueRange();
	// advc.314: Adjust to map size
	iUniqueRange += GC.getWorldInfo(GC.getMap().getWorldSize()).getFeatureGrainChange();
	for (SquareIter it(*p, iUniqueRange); it.hasNext(); ++it)
	{
		if (it->getImprovementType() == eGoody)
			return false;
	}

	return true;
}


void CvMapGenerator::addGameElements()
{
	// merkava.mb0 putting this before the rest of the game elements, so that those functions can use biomes. 
	addBiomes(); 
	gDLL->logMemState("CvMapGen after add biomes");
	// merkava.mb0 end

	addRivers();
	gDLL->logMemState("CvMapGen after add rivers");

	addLakes();
	gDLL->logMemState("CvMapGen after add lakes");

	addFeatures();
	gDLL->logMemState("CvMapGen after add features");

	addBonuses();
	gDLL->logMemState("CvMapGen after add bonuses");

	addGoodies();
	gDLL->logMemState("CvMapGen after add goodies");

	// Call for Python to make map modifications after it's been generated
	afterGeneration();
}

// merkava.mb
void CvMapGenerator::addBiomes()
{
	GC.getGame().resetPlotBiomeMap();
	// First pass: record biomes for all tiles based on their most common adjacent terrain. 
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		TerrainTypes eMostAdjacent = getMostAdjacentTerrain(i);
		if (eMostAdjacent != NO_TERRAIN)
			GC.getGame().setPlotBiome(i, eMostAdjacent); 
		else
			GC.getGame().setPlotBiome(i, NO_TERRAIN); 
	}
	// Second pass: check adjacent biomes, if none similar, flip to most common adjacent. 
	// Simultaneously, split ocean by latitude groups, as defined in global defines. 
	int iLatitudeGroups = GC.getDefineINT("NUM_LATITUDE_GROUPS");
	int iLatitudeDivision = (GC.getMap().getTopLatitude() - GC.getMap().getBottomLatitude()) / iLatitudeGroups;
	for (int n = 0; n < GC.getDefineINT("NUM_SECOND_PASSES"); n++) 
	{
		for (int i = 0; i < GC.getMap().numPlots(); i++)
		{
			if (GC.getMap().plotByIndex(i)->isWater() && !GC.getMap().plotByIndex(i)->isAdjacentToLand()) // ocean: set latitude biome - negative for now
			{
				int iLatBiome = (GC.getMap().plotByIndex(i)->getLatitude() - GC.getMap().getBottomLatitude()) / iLatitudeDivision;
				GC.getGame().setPlotBiome(i, (-1 * iLatBiome) - 2); // -1 is still reserved for "no biome"
				continue; // being adjacent to itself doesn't matter for ocean - yet. 
			}
			if (!isAdjacentToOwnBiome(i, GC.getDefineINT("SECOND_PASS_MINIMUM_ADJACENT"))) // note "own" means own biome, not biome matching own terrain
			{
				int adjBiome = getMostAdjacentBiome(i, false, true); // note that this might flip it right back if min > 1; that's okay for now
				if (adjBiome != -1) // don't spread -1 biomes around, do multiple passes here
					GC.getGame().setPlotBiome(i, adjBiome); 
			}
		}
	}
	// Third pass! Adjacency. 
	std::vector<std::vector<int> > aiBiomeSizeArray;
	int* aiAdjacencyMap = new int[GC.getMap().numPlots()];
	// initialize list
	for (int i = 0; i < GC.getMap().numPlots(); i++)
		aiAdjacencyMap[i] = -1;
	if (GC.getDefineINT("DO_THIRD_PASS") > 0)
	{
		int iBiome = 0;
		for (int i = 0; i < GC.getMap().numPlots(); i++)
		{
			CvPlot* pPlot = GC.getMap().plotByIndex(i); 
			// check adjacent plots, take their adjacency if they share our biome
			FOR_EACH_ADJ_PLOT2(pLoopPlot, *pPlot)
			{
				if (GC.getGame().getPlotBiome(pLoopPlot->plotNum()) == GC.getGame().getPlotBiome(i) && aiAdjacencyMap[pLoopPlot->plotNum()] != -1)
					aiAdjacencyMap[i] = aiAdjacencyMap[pLoopPlot->plotNum()];
			}
			// if we still have no adjacency, this is a new biome
			if (aiAdjacencyMap[i] == -1) 
			{
				aiAdjacencyMap[i] = iBiome;
				iBiome++;
			}
			// post-check: if adjacent tiles share our biome but not our adjacency, flip them to ours. 
			FOR_EACH_ADJ_PLOT2(pLoopPlot, *pPlot)
			{
				if (GC.getGame().getPlotBiome(pLoopPlot->plotNum()) == GC.getGame().getPlotBiome(i) && aiAdjacencyMap[pLoopPlot->plotNum()] != aiAdjacencyMap[i])
				{
					int iOriginalAdjacency = aiAdjacencyMap[pLoopPlot->plotNum()];
					aiAdjacencyMap[pLoopPlot->plotNum()] = aiAdjacencyMap[i];
					if (iOriginalAdjacency != -1)
					{
						int iNew = -1;
						int iOld = -1;
						// This means two biomes actually touch each other and are one biome. 
						// so whichever is less, flip the other to that. 
						if (iOriginalAdjacency < aiAdjacencyMap[i])
						{
							iOld = aiAdjacencyMap[i];
							iNew = iOriginalAdjacency;
						}
						else if (iOriginalAdjacency > aiAdjacencyMap[i])
						{
							iOld = iOriginalAdjacency;
							iNew = aiAdjacencyMap[i];
						}
						for (int ii = 0; ii < i; ii++)
							if (aiAdjacencyMap[ii] == iOld)
								aiAdjacencyMap[ii] = iNew;
					}
				}
			}
		}	
		// Now set biomes to match adjacency. 
		for (int i = 0; i < GC.getMap().numPlots(); i++)
		{
			// but skip -1 biomes; mb2c
			if (GC.getGame().getPlotBiome(i) == -1)
				continue;
			//if (!GC.getMap().plotByIndex(i)->isWater() || GC.getMap().plotByIndex(i)->isAdjacentToLand()) // mb2c ocean plot biomes set above, but not coasts
			GC.getGame().setPlotBiome(i, aiAdjacencyMap[i]); //mb3a adjacency for oceans
			// size array here
			std::vector<int> newVec;
			while ((int)aiBiomeSizeArray.size() <= GC.getGame().getPlotBiome(i))
				aiBiomeSizeArray.push_back(newVec);
			aiBiomeSizeArray[GC.getGame().getPlotBiome(i)].push_back(i); // the way this is set up this SHOULD not have any empty arrays but I'm not positive
		}
	}
	// mb6 I think having a separate size-flipping pass would be good. but need to make sure the size array is set up even if third passes aren't done. 
	else if (GC.getDefineINT("MIN_BIOME_SIZE") > 1)
	{
		for (int i = 0; i < GC.getMap().numPlots(); i++)
		{
			if (GC.getGame().getPlotBiome(i) == -1)
				continue;
			if (GC.getGame().getPlotBiome(i) < 0) // means water in this case, so let's tack those biomes on top
				GC.getGame().setPlotBiome(i, GC.getNumTerrainInfos() + (-1 * GC.getGame().getPlotBiome(i)));
			std::vector<int> newVec;
			while ((int)aiBiomeSizeArray.size() <= GC.getGame().getPlotBiome(i))
				aiBiomeSizeArray.push_back(newVec);
			aiBiomeSizeArray[GC.getGame().getPlotBiome(i)].push_back(i); // in this case these will be TerrainTypes. Might have a couple blank rows but that's no big deal. 
		}
	}
	// Size pass
	if (GC.getDefineINT("MIN_BIOME_SIZE") > 1)
	{
		int iSize = (int)aiBiomeSizeArray.size();
		for (int s = 0; s < (int)aiBiomeSizeArray.size(); s++)
		{
			if ((int)aiBiomeSizeArray[s].size() < GC.getDefineINT("MIN_BIOME_SIZE"))
			{
				// need to do this until all are flipped or a certain cap is reached. 
				int iCap = 100;
				int iNumFlipped = 0;
				// remove biome's tiles from list
				int iSize = (int)aiBiomeSizeArray[s].size();
				std::vector<int> biomeTiles = aiBiomeSizeArray[s];
				aiBiomeSizeArray[s].clear();
				while (iNumFlipped < iSize && iCap > 0)
				{
					iCap--;
					// flip all of this biome's tiles to adjacent biomes. 
					for (int i = 0; i < (int)biomeTiles.size(); i++)
					{
						int iAdjBiome = getMostAdjacentBiome(biomeTiles[i], true); //exclude own biome from this
						if (iAdjBiome >= 0) // shouldn't be anything but -1 and positive at this point, but, who knows
						{
							GC.getGame().setPlotBiome(biomeTiles[i], iAdjBiome);
							iNumFlipped++;
							// add to new biome array
							aiBiomeSizeArray[iAdjBiome].push_back(biomeTiles[i]);
						}
					}
				}
			}
		}
	}
	// And finally, set up the biomes in CvGame. 
	int iBiomeCount = 0;
	for (int j = 0; j < (int)aiBiomeSizeArray.size(); j++)
	{
		if ((int)aiBiomeSizeArray[j].size() == 0)
			continue;
		TerrainTypes eTerrain = NO_TERRAIN;
		int iBottomLatitude = 1000;
		int iTopLatitude = -1000;
		std::vector<int> adjBiomes;
		std::vector<int> landAreas;
		int iMax = 0;
		ArrayEnumMap<TerrainTypes, int> aiTerrains;
		for (int i = 0; i < (int)aiBiomeSizeArray[j].size(); i++)
		{
			TerrainTypes iIndex = GC.getMap().plotByIndex(aiBiomeSizeArray[j][i])->getTerrainType();
			int iLatitude = GC.getMap().plotByIndex(aiBiomeSizeArray[j][i])->getLatitude();
			aiTerrains[iIndex]++;
			if (aiTerrains[iIndex] > iMax)
			{
				iMax = aiTerrains[iIndex];
				eTerrain = iIndex;
			}
			if (iLatitude < iBottomLatitude)
				iBottomLatitude = iLatitude;
			if (iLatitude > iTopLatitude)
				iTopLatitude = iLatitude;
			FOR_EACH_ADJ_PLOT(*GC.getMap().plotByIndex(aiBiomeSizeArray[j][i]))
			{
				int iAdjBiome = GC.getGame().getPlotBiome(pAdj->plotNum());
				bool bFound = false;
				if ((int)adjBiomes.size() > 0)
				{
					for (int k = 0; k < (int)adjBiomes.size(); k++)
					{
						if (adjBiomes[k] == iAdjBiome)
						{
							bFound = true;
							break;
						}
					}
				}
				if (bFound)
					continue;
				else
					adjBiomes.push_back(iAdjBiome);
			}
			CvArea *pArea = GC.getMap().plotByIndex(aiBiomeSizeArray[j][i])->area();
			if (GC.getMap().plotByIndex(aiBiomeSizeArray[j][i])->isWater())
				continue; 
			int iAreaID = pArea->getID();
			bool bFound = false;
			if ((int)landAreas.size() > 0)
			{
				for (int k = 0; k < (int)landAreas.size(); k++)
				{
					if (landAreas[k] == iAreaID)
					{
						bFound = true;
						break;
					}
				}
			}
			if (bFound)
				continue;
			else
				landAreas.push_back(iAreaID);
		}
		if (eTerrain != NO_TERRAIN && iBottomLatitude < 1000 && iTopLatitude > -1000) // i.e., we found stuff for the biome
		{
			GC.getGame().addBiome(eTerrain, iBottomLatitude, iTopLatitude);
			for (int l = 0; l < (int)landAreas.size(); l++)
				GC.getGame().addBiomeLandArea(iBiomeCount, landAreas[l]);
			for (int l = 0; l < (int)adjBiomes.size(); l++)
				GC.getGame().addAdjacentBiome(iBiomeCount, l);
			iBiomeCount++;
		}
		else
			FAssertMsg(false, "Probably some non-plot indices added to biome size array");

	}
	// That should be it! 
}
// counts terrains bordering this tile and returns the numerically highest present
TerrainTypes CvMapGenerator::getMostAdjacentTerrain(int iPlotIndex)
{
	CvPlot* pPlot = GC.getMap().plotByIndex(iPlotIndex);
	ArrayEnumMap<TerrainTypes, int> adjTerrainNums;
	FOR_EACH_ADJ_PLOT2(pLoopPlot, *pPlot)
	{
		// Ignore coasts; coasts are non-biomes and just attached to whatever biome is nearby. 
		if (pLoopPlot->isAdjacentToLand() && pLoopPlot->isWater())
			continue;
		// Also, if the center plot is a coast, ignore oceans. 
		if (pPlot->isAdjacentToLand() && pPlot->isWater() && pLoopPlot->isWater())
			continue;
		TerrainTypes eAdjTerrain = pLoopPlot->getTerrainType();
		adjTerrainNums[pLoopPlot->getTerrainType()] += 1;
	}
	// Now find numerically most adjacent. 
	int iMax = 0;
	TerrainTypes eMaxTerrain = NO_TERRAIN;
	// If there is a tie, will consider the center tile, and if that can't break ties, just leave at -1 for now. 
	std::vector<int> tiedTerrains; 
	// Loop through terrains in list
	FOR_EACH_ENUM2(Terrain, eTerrain)
	{
		// If current greater than max, update max
		if (adjTerrainNums[eTerrain] > iMax)
		{
			iMax = adjTerrainNums[eTerrain];
			eMaxTerrain = eTerrain;
			// Previous ties no longer relevant, but current max is part of future ties. 
			tiedTerrains.clear(); 
			tiedTerrains.push_back(eMaxTerrain);
		}
		else if (adjTerrainNums[eTerrain] == iMax && iMax > 0) // don't consider zero lol
			tiedTerrains.push_back(eTerrain);
	}
	// check tied terrains; if the center matches the terrain, that's the max. otherwise, no terrain is max. 
	if ((int)tiedTerrains.size() > 1)
	{
		for (int i = 0; i < (int)tiedTerrains.size(); i++)
		{
			if (tiedTerrains[i] == pPlot->getTerrainType())
				return pPlot->getTerrainType();
		}
		return NO_TERRAIN;
	}
	return eMaxTerrain;
}
//mb1.3
// returns false if biome is -1 or if no adjacent terrains share same biome
bool CvMapGenerator::isAdjacentToOwnBiome(int iPlotIndex, int iMinAdj)
{
	int iAdj = 0;
	if (GC.getGame().getPlotBiome(iPlotIndex) == -1) 
		return false;
	CvPlot* pPlot = GC.getMap().plotByIndex(iPlotIndex);
	FOR_EACH_ADJ_PLOT2(pLoopPlot, *pPlot)
	{
		if (pLoopPlot->isWater() && !pLoopPlot->isAdjacentToLand()) // skip ocean tiles, but coast is fine
			continue;
		if (GC.getGame().getPlotBiome(iPlotIndex) == GC.getGame().getPlotBiome(pLoopPlot->plotNum()))
			iAdj++;
	}
	return (iAdj >= iMinAdj);
}
// returns the most common adjacent biome. This one only works before same-terrain biomes are separated. 
// Basically the same as the terrain one, but it uses biomes. 
int CvMapGenerator::getMostAdjacentBiome(int iPlotIndex, bool bExcludeOwn, bool bProbabilistic)
{
	CvPlot* pPlot = GC.getMap().plotByIndex(iPlotIndex);
	std::vector<std::pair<int, int> > adjBiomeNums;
	FOR_EACH_ADJ_PLOT2(pLoopPlot, *pPlot)
	{
		int iAdjBiome = GC.getGame().getPlotBiome(pLoopPlot->plotNum());
		if (iAdjBiome == -1)
			continue;
		if (bExcludeOwn && iAdjBiome == GC.getGame().getPlotBiome(iPlotIndex)) 
			continue;
		if (!(pPlot->isWater() && !pPlot->isAdjacentToLand()) && pLoopPlot->isWater() && !pLoopPlot->isAdjacentToLand()) // if center is not deep ocean and adjacent is, skip it
			continue;
		bool bFound = false;
		for (int k = 0; k < (int)adjBiomeNums.size(); k++)
		{
			if (adjBiomeNums[k].first == iAdjBiome)
			{
				bFound = true;
				adjBiomeNums[k].second += 1;
				break;
			}
		}
		if (!bFound)
		{
			std::pair<int, int> biome = std::pair<int, int>(iAdjBiome, 1);
			adjBiomeNums.push_back(biome);
		}
	}
	int iMax = 0;
	int iMaxBiome = -1;
	if ((int)adjBiomeNums.size() == 0) // found no adjacent biomes that aren't -1 or coasts
		return GC.getGame().getPlotBiome(iPlotIndex); // so just leave it as its own
	std::vector<int> tiedBiomes; 
	// Loop through terrains in list
	for (int k = 0; k < (int)adjBiomeNums.size(); k++)
	{
		// If current greater than max, update max
		if (adjBiomeNums[k].second > iMax)
		{
			iMax = adjBiomeNums[k].second;
			iMaxBiome = adjBiomeNums[k].first; 
			tiedBiomes.clear();
			tiedBiomes.push_back(iMaxBiome);
		}
		else if (adjBiomeNums[k].second == iMax && iMax > 0) // don't consider zero lol
		{
			tiedBiomes.push_back(adjBiomeNums[k].first);
		}
	}
	// now check the tied biomes. 
	if ((int)tiedBiomes.size() > 0)
	{
		for (int i = 0; i < (int)tiedBiomes.size(); i++)
		{
			if (tiedBiomes[i] == GC.getGame().getPlotBiome(pPlot->plotNum()))
				return tiedBiomes[i];
		}
		// If got to here that means center does not match tied biomes. 
		if (bProbabilistic)
			return tiedBiomes[SyncRandNum((int)tiedBiomes.size())];
		return -1;
	}
	return iMaxBiome;
}
// merkava.mb END

void CvMapGenerator::addLakes()
{
	PROFILE_FUNC();

	if (GC.getPythonCaller()->addLakes())
		return;

	gDLL->NiTextOut("Adding Lakes...");
	int const iLAKE_PLOT_RAND = GC.getDefineINT("LAKE_PLOT_RAND"); // advc.opt
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		//gDLL->callUpdater(); // advc.opt: Not needed I reckon
		CvPlot& p = GC.getMap().getPlotByIndex(i);
		if (!p.isWater() && !p.isCoastalLand() && !p.isRiver())
		{
			if (MapRandNum(iLAKE_PLOT_RAND) == 0)
				p.setPlotType(PLOT_OCEAN);
		}
	}
}

void CvMapGenerator::addRivers()  // advc: refactored
{
	PROFILE_FUNC();

	if (GC.getPythonCaller()->addRivers())
		return;

	gDLL->NiTextOut("Adding Rivers...");

	int const iRiverSourceRange = GC.getDefineINT("RIVER_SOURCE_MIN_RIVER_RANGE");
	int const iSeaWaterRange = GC.getDefineINT("RIVER_SOURCE_MIN_SEAWATER_RANGE");
	int const iPlotsPerRiverEdge =  GC.getDefineINT("PLOTS_PER_RIVER_EDGE");
	// advc.129: Randomize the traversal
	int* aiShuffledIndices = mapRand().shuffle(GC.getMap().numPlots());
	for (int iPass = 0; iPass < 4; iPass++)
	{
		int iRiverSourceRangeLoop = (iPass <= 1 ? iRiverSourceRange : iRiverSourceRange / 2);
		int iSeaWaterRangeLoop =  (iPass <= 1 ? iSeaWaterRange : iSeaWaterRange / 2);

		for (int i = 0; i < GC.getMap().numPlots(); i++)
		{
			CvPlot const& p = GC.getMap().getPlotByIndex(
					aiShuffledIndices[i]); // advc.129
			if (p.isWater())
				continue;

			bool bValid = false;
			switch(iPass)
			{
			case 0:
				bValid = (p.isHills() || p.isPeak());
				break;
			case 1:
				bValid = (!p.isCoastalLand() && MapRandSuccess(fixp(1/8.)));
				break;
			case 2:
				bValid = ((p.isHills() || p.isPeak()) &&
						p.getArea().getNumRiverEdges() <
						1 + p.getArea().getNumTiles() / iPlotsPerRiverEdge);
				break;
			case 3:
				bValid = (p.getArea().getNumRiverEdges() <
						1 + p.getArea().getNumTiles() / iPlotsPerRiverEdge);
				break;
			default: FErrorMsg("Invalid iPass");
			}
			if (!bValid)
				continue;

			gDLL->callUpdater(); // advc.opt: Moved down; shouldn't need to update the UI in every iteration.
			if (!GC.getMap().findWater(&p, iRiverSourceRangeLoop, true) &&
				!GC.getMap().findWater(&p, iSeaWaterRangeLoop, false))
			{
				CvPlot* pStartPlot = p.getInlandCorner();
				if (pStartPlot != NULL)
					doRiver(pStartPlot);
			}
		}
	}
	SAFE_DELETE_ARRAY(aiShuffledIndices); // advc.129
}

// pStartPlot = the plot at whose SE corner the river is starting
void CvMapGenerator::doRiver(CvPlot* pStartPlot,
	CardinalDirectionTypes eLastCardinalDirection,
	CardinalDirectionTypes eOriginalCardinalDirection, short iThisRiverID)
{
	if (iThisRiverID == -1)
	{
		iThisRiverID = GC.getMap().getNextRiverID();
		GC.getMap().incrementNextRiverID();
	}
	/*	advc (note): Could probably just pass river ids through the call stack
		instead of storing them for the entire game at CvPlot. However,
		CyPlot::setRiverID/ getRiverID are also used by some map scripts. */
	short iOtherRiverID = pStartPlot->getRiverID();
	if (iOtherRiverID != -1 && iOtherRiverID != iThisRiverID)
		return; // Another river already exists here; can't branch off of an existing river!

	CvPlot *pRiverPlot = NULL;
	CvPlot *pAdjacentPlot = NULL;

	CardinalDirectionTypes eBestCardinalDirection = NO_CARDINALDIRECTION;
	if (eLastCardinalDirection == CARDINALDIRECTION_NORTH)
	{
		pRiverPlot = pStartPlot;
		if (pRiverPlot == NULL)
			return;
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX(), pRiverPlot->getY(),
				CARDINALDIRECTION_EAST);
		if (pAdjacentPlot == NULL || pRiverPlot->isWOfRiver() ||
			pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}

		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setWOfRiver(true, eLastCardinalDirection);
		pRiverPlot = plotCardinalDirection(pRiverPlot->getX(), pRiverPlot->getY(),
				CARDINALDIRECTION_NORTH);
	}
	else if (eLastCardinalDirection == CARDINALDIRECTION_EAST)
	{
		pRiverPlot = plotCardinalDirection(pStartPlot->getX(), pStartPlot->getY(),
				CARDINALDIRECTION_EAST);
		if (pRiverPlot == NULL)
			return;
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX(), pRiverPlot->getY(),
				CARDINALDIRECTION_SOUTH);
		if (pAdjacentPlot == NULL || pRiverPlot->isNOfRiver() ||
			pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}
		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setNOfRiver(true, eLastCardinalDirection);
	}
	else if (eLastCardinalDirection == CARDINALDIRECTION_SOUTH)
	{
		pRiverPlot = plotCardinalDirection(pStartPlot->getX(), pStartPlot->getY(),
				CARDINALDIRECTION_SOUTH);
		if (pRiverPlot == NULL)
			return;
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX(), pRiverPlot->getY(),
				CARDINALDIRECTION_EAST);
		if (pAdjacentPlot == NULL || pRiverPlot->isWOfRiver() ||
			pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}
		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setWOfRiver(true, eLastCardinalDirection);
	}
	else if (eLastCardinalDirection == CARDINALDIRECTION_WEST)
	{
		pRiverPlot = pStartPlot;
		if (pRiverPlot == NULL)
			return;
		pAdjacentPlot = plotCardinalDirection(pRiverPlot->getX(), pRiverPlot->getY(),
				CARDINALDIRECTION_SOUTH);
		if (pAdjacentPlot == NULL || pRiverPlot->isNOfRiver() ||
			pRiverPlot->isWater() || pAdjacentPlot->isWater())
		{
			return;
		}
		pStartPlot->setRiverID(iThisRiverID);
		pRiverPlot->setNOfRiver(true, eLastCardinalDirection);
		pRiverPlot = plotCardinalDirection(pRiverPlot->getX(), pRiverPlot->getY(),
				CARDINALDIRECTION_WEST);
	}
	else
	{
		//FErrorMsg("Illegal direction type");
		// River is starting here, set the direction in the next step
		pRiverPlot = pStartPlot;

		GC.getPythonCaller()->riverStartCardinalDirection(*pRiverPlot, eBestCardinalDirection);
	}

	if (pRiverPlot == NULL)
		return; // The river has flowed off the edge of the map. All is well.
	if (pRiverPlot->hasCoastAtSECorner())
		return; // The river has flowed into the ocean. All is well.

	if (eBestCardinalDirection == NO_CARDINALDIRECTION)
	{
		int iBestValue = MAX_INT;
		FOR_EACH_ENUM(CardinalDirection)
		{
			CardinalDirectionTypes eOppositeDir = getOppositeCardinalDirection(
					eLoopCardinalDirection);
			if (eOppositeDir != eOriginalCardinalDirection &&
				eOppositeDir != eLastCardinalDirection)
			{
				CvPlot* pLoopPlot = plotCardinalDirection(pRiverPlot->getX(), pRiverPlot->getY(),
						eLoopCardinalDirection);
				if (pLoopPlot != NULL)
				{
					int iValue = getRiverValueAtPlot(*pLoopPlot);
					if (iValue < iBestValue)
					{
						iBestValue = iValue;
						eBestCardinalDirection = eLoopCardinalDirection;
					}
				}
			}
		}
	}

	if (eBestCardinalDirection != NO_CARDINALDIRECTION)
	{
		if (eOriginalCardinalDirection == NO_CARDINALDIRECTION)
			eOriginalCardinalDirection = eBestCardinalDirection;
		doRiver(pRiverPlot, eBestCardinalDirection, eOriginalCardinalDirection, iThisRiverID);
	}
}

//Note from Blake:
//Iustus wrote this function, it ensures that a new river actually
//creates fresh water on the passed plot. Quite useful really
//Although I veto'd its use since I like that you don't always
//get fresh water starts.
/*	advc (note): This function isn't unused though. It's a fallback
	in case that no lake can be placed. Though I'm not sure if it can
	succeed where CvGame::normalizeFindLakePlot fails. */
// pFreshWaterPlot = the plot we want to give a fresh water river
bool CvMapGenerator::addRiver(CvPlot* pFreshWaterPlot)
{
	FAssert(pFreshWaterPlot != NULL);

	// cannot have a river flow next to water
	if (pFreshWaterPlot->isWater())
		return false;

	// if it already has a fresh water river, then success! we done
	if (pFreshWaterPlot->isRiver())
		return true;

	int const iFreshWX = pFreshWaterPlot->getX(); // advc
	int const iFreshWY = pFreshWaterPlot->getY(); // advc

	// make two passes, once for each flow direction of the river
	int iNWFlowPass = MapRandNum(2);
	for (int iPass = 0; iPass <= 1; iPass++)
	{
		// try placing a river edge in each direction, in random order
		FOR_EACH_ENUM_RAND(CardinalDirection, mapRand())
		{
			CardinalDirectionTypes eRiverDirection = NO_CARDINALDIRECTION;
			CvPlot *pRiverPlot = NULL;

			switch (eLoopCardinalDirection)
			{
			case CARDINALDIRECTION_NORTH:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = plotDirection(iFreshWX, iFreshWY, DIRECTION_NORTH);
					eRiverDirection = CARDINALDIRECTION_WEST;
				}
				else
				{
					pRiverPlot = plotDirection(iFreshWX, iFreshWY, DIRECTION_NORTHWEST);
					eRiverDirection = CARDINALDIRECTION_EAST;
				}
				break;

			case CARDINALDIRECTION_EAST:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = pFreshWaterPlot;
					eRiverDirection = CARDINALDIRECTION_NORTH;
				}
				else
				{
					pRiverPlot = plotDirection(iFreshWX, iFreshWY, DIRECTION_NORTH);
					eRiverDirection = CARDINALDIRECTION_SOUTH;
				}
				break;

			case CARDINALDIRECTION_SOUTH:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = pFreshWaterPlot;
					eRiverDirection = CARDINALDIRECTION_WEST;
				}
				else
				{
					pRiverPlot = plotDirection(iFreshWX, iFreshWY, DIRECTION_WEST);
					eRiverDirection = CARDINALDIRECTION_EAST;
				}
				break;

			case CARDINALDIRECTION_WEST:
				if (iPass == iNWFlowPass)
				{
					pRiverPlot = plotDirection(iFreshWX, iFreshWY, DIRECTION_WEST);
					eRiverDirection = CARDINALDIRECTION_NORTH;
				}
				else
				{
					pRiverPlot = plotDirection(iFreshWX, iFreshWY, DIRECTION_NORTHWEST);
					eRiverDirection = CARDINALDIRECTION_SOUTH;
				}
				break;

			default:
				FErrorMsg("invalid cardinal direction");
			}

			if (pRiverPlot != NULL && !pRiverPlot->hasCoastAtSECorner())
			{
				// try to make the river
				doRiver(pRiverPlot, eRiverDirection, eRiverDirection);

				// if it succeeded, then we will be a river now!
				if (pFreshWaterPlot->isRiver())
					return true;
			}
		}
	}
	return false;
}


void CvMapGenerator::addFeatures()
{
	PROFILE_FUNC();

	if (GC.getPythonCaller()->addFeatures())
		return;

	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot& kPlot = GC.getMap().getPlotByIndex(i);
		FOR_EACH_ENUM(Feature)
		{
			if (kPlot.canHaveFeature(eLoopFeature))
			{
				if (MapRandSuccess(per10000(GC.getInfo(eLoopFeature).
					getAppearanceProbability())))
				{
					kPlot.setFeatureType(eLoopFeature);
				}
			}
		}
	}
}

void CvMapGenerator::addBonuses()
{
	PROFILE_FUNC();
	gDLL->NiTextOut("Adding Bonuses...");

	CvPythonCaller const& py = *GC.getPythonCaller();
	if (py.addBonuses())
		return;
	/*  <advc.129> Only do an iteration for those PlacementOrder numbers that are
		actually used in the BonusInfos. */
	std::vector<int> aiOrdinals;
	FOR_EACH_ENUM(Bonus)
	{
		int iOrder = GC.getInfo(eLoopBonus).getPlacementOrder();
		if (iOrder >= 0) // The negative ones aren't supposed to be placed at all
			aiOrdinals.push_back(iOrder);
	}
	::removeDuplicates(aiOrdinals);
	FAssertMsg(aiOrdinals.size() <= (uint)12, "Shuffling the bonus indices this often might be slow(?)");
	std::sort(aiOrdinals.begin(), aiOrdinals.end());
	//for (int iOrder = 0; iOrder < GC.getNumBonusInfos(); iOrder++)
	for (size_t i = 0; i < aiOrdinals.size(); i++)
	{
		int iOrder = aiOrdinals[i];	
		/*  advc.129: Break ties in the order randomly (perhaps better
			not to do this though if the assertion above fails) */
		FOR_EACH_ENUM_RAND(Bonus, GC.getGame().getMapRand())
		{
			//gDLL->callUpdater();
			if (GC.getInfo(eLoopBonus).getPlacementOrder() != iOrder)
				continue;

			gDLL->callUpdater(); // advc.opt: Moved down; don't need to update the UI quite so frequently.
			if (!py.addBonusType(eLoopBonus))
			{
				if (GC.getInfo(eLoopBonus).isOneArea())
					addUniqueBonusType(eLoopBonus);
				else addNonUniqueBonusType(eLoopBonus);
			}
		}
	}
}

void CvMapGenerator::addUniqueBonusType(BonusTypes eBonus)
{
	CvBonusInfo const& kBonus = GC.getInfo(eBonus);
	int const iTarget = calculateNumBonusesToAdd(eBonus);
	bool const bIgnoreLatitude = GC.getPythonCaller()->isBonusIgnoreLatitude();
	// advc.opt: Don't waste time trying to place land resources in the ocean
	bool const bWater = (kBonus.isTerrain(GC.getWATER_TERRAIN(true)) ||
			kBonus.isTerrain(GC.getWATER_TERRAIN(false)));
	FAssertMsg(kBonus.isOneArea(), "addUniqueBonusType called with non-unique bonus type");
	CvMap& kMap = GC.getMap();

	/*	K-Mod note: the areas tried stuff was originally done using an array.
		I've rewritten it to use std::set, for no good reason. The functionality is unchanged.
		(But it is now slightly more efficient and easier to read.) */
	std::set<int> areas_tried;
	// <advc.129>
	// Sort areas in order to save time below
	std::vector<std::pair<int,int> > areasBySize;
	FOR_EACH_AREA(pLoopArea)
		areasBySize.push_back(std::make_pair(pLoopArea->getNumTiles(), pLoopArea->getID()));
	std::sort(areasBySize.rbegin(), areasBySize.rend());

	for (int iPass = 0; iPass < 2; iPass++)
	{	/*  Two passes - just to make sure that the new per-area limit doesn't
			lead to fewer resources overall. */
		bool const bIgnoreAreaLimit = (iPass == 1); // </advc.129>
		while (/* advc.129: */kMap.getNumBonuses(eBonus) < iTarget)
		{
			int iBestValue = 0;
			CvArea* pBestArea = NULL;
			for (size_t i = 0; i < areasBySize.size(); i++)
			{
				CvArea& kLoopArea = *kMap.getArea(areasBySize[i].second);
				// <advc.opt>
				if (kLoopArea.isWater() && !bWater)
					continue; // </advc.opt>
				if (areas_tried.count(kLoopArea.getID()) > 0)
					continue;
				int iNumTiles = kLoopArea.getNumTiles();
				// <advc> Who knows what a map script might do ...
				if (iNumTiles <= 0)
				{
					FAssert(iNumTiles > 0);
					continue;
				} // </advc>
				int iAddedTotal = kMap.getNumBonuses(eBonus);
				if (iAddedTotal * 3 < 2 * iTarget &&
					iNumTiles < 4 * NUM_CITY_PLOTS) // K-Mod
				{
					continue;
				}
				// number of unique bonuses starting on the area, plus this one
				int iNumUniqueBonusesOnArea = 1 + kLoopArea.countNumUniqueBonusTypes();
				//int iValue = iNumTiles / iNumUniqueBonusesOnArea;
				int iValue = ((iNumTiles *
						// advc.129: Decrease the impact of iNumTiles when approaching the target resource count
						(iTarget - iAddedTotal)) / iTarget +
						MapRandNum(3 * NUM_CITY_PLOTS)) / iNumUniqueBonusesOnArea;
				// <advc.129>
				if (iValue <= iBestValue) // To save time
					continue;
				int iEligible = 0;
				for (int j = 0; j < kMap.numPlots(); j++)
				{
					CvPlot const& kTestPlot = kMap.getPlotByIndex(j);
					if (kTestPlot.isArea(kLoopArea) &&
						canPlaceBonusAt(eBonus, kTestPlot.getX(), kTestPlot.getY(),
						false, false)) // Save some time by skipping range checks
					{
						iEligible++;
					}
				}
				scaled rSuitability(iEligible, iNumTiles);
				rSuitability = (rSuitability + 2) / 3; // dilute
				iValue = (rSuitability * iValue).round(); // </advc.129>
				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestArea = &kLoopArea;
				}
			}

			if (pBestArea == NULL)
				break; // can't place bonus on any area

			areas_tried.insert(pBestArea->getID());
			// <advc.129>
			int iAdded = 0;
			int const iAreaLimit = std::min(2, 3 * pBestArea->getNumTiles()) +
					pBestArea->getNumTiles() / 25; // </advc.129>

			// Place the bonuses ...
			int* aiShuffledIndices = mapRand().shuffle(kMap.numPlots());
			for (int i = 0; i < kMap.numPlots() &&
				(bIgnoreAreaLimit || iAdded < iAreaLimit) && // advc.129
				kMap.getNumBonuses(eBonus) < iTarget; i++)
			{
				CvPlot& kRandPlot = kMap.getPlotByIndex(aiShuffledIndices[i]);
				if (pBestArea != kRandPlot.area())
					continue;
				if (!canPlaceBonusAt(eBonus, kRandPlot.getX(), kRandPlot.getY(),
					bIgnoreLatitude))
				{
					continue;
				}
				/*	<advc.129> About to place a cluster of eBonus. Don't place that
					cluster near an earlier cluster (or any instance) of the same bonus class
					- that's what can lead to e.g. starts with 5 Gold. canPlaceBonusAt
					can't enforce this well b/c it doesn't know whether a cluster starts
					(distance needs to be heeded) or continues (distance mustn't be heeded). */
				BonusClassTypes eClassToAvoid = kBonus.getBonusClassType();
				/*	In BtS, all resources that occur in clusters are of the
					"general" class, id 0. Don't want to eliminate all overlapping clusters
					b/c that may get in the way of (early) resource trades too much and
					make the map less exciting than it could be. So I've moved the
					problematic resources into a new class "precious" (id greater than 0). */
				if (kBonus.getGroupRand() > 0 && eClassToAvoid > 0)
				{
					bool bSkip = false;
					/*	Check a range that makes it difficult to cover more than
						one group with a single city. */
					int const iRange = CITY_PLOTS_DIAMETER + kBonus.getGroupRange() - 1;
					for (PlotCircleIter it(kRandPlot, iRange);
						it.hasNext(); ++it)
					{
						CvPlot const& p = *it;
						if (!p.sameArea(kRandPlot))
							continue;
						BonusTypes eOtherBonus = p.getBonusType();
						if(eOtherBonus != NO_BONUS && GC.getInfo(eOtherBonus).
							getBonusClassType() == eClassToAvoid &&
							GC.getInfo(eOtherBonus).getGroupRand() > 0)
						{
							bSkip = true;
							break;
						}
					}
					if(bSkip)
						continue;
				} // </advc.129>
				kRandPlot.setBonusType(eBonus);
				// <advc.129>
				iAdded++;
				iAdded += placeGroup(eBonus, kRandPlot, bIgnoreLatitude); // Replacing the code below
				/*for (int iDX = -(kBonus.getGroupRange()); iDX <= kBonus.getGroupRange(); iDX++) {
					for (int iDY = -(kBonus.getGroupRange()); iDY <= kBonus.getGroupRange(); iDY++) {
						if (GC.getMap().getNumBonuses(eBonus) < iBonusCount) {
							CvPlot* pLoopPlot	= plotXY(pPlot->getX(), pPlot->getY(), iDX, iDY);
							if (pLoopPlot != NULL && (pLoopPlot->area() == pBestArea)) {
								if (canPlaceBonusAt(eBonus, pLoopPlot->getX(), pLoopPlot->getY(), bIgnoreLatitude)) {
									if (MapRandNum(100) < kBonus.getGroupRand())
										pLoopPlot->setBonusType(eBonus);
				} } } } }*/

			}
			SAFE_DELETE_ARRAY(aiShuffledIndices);
		}
	}
}

void CvMapGenerator::addNonUniqueBonusType(BonusTypes eBonus)
{
	int iBonusCount = calculateNumBonusesToAdd(eBonus);
	if (iBonusCount == 0)
		return;

	int *aiShuffledIndices = mapRand().shuffle(GC.getMap().numPlots());
	bool const bIgnoreLatitude = GC.getPythonCaller()->isBonusIgnoreLatitude();
	for (int i = 0; i < GC.getMap().numPlots(); i++)
	{
		CvPlot& p = GC.getMap().getPlotByIndex(aiShuffledIndices[i]);
		if (!canPlaceBonusAt(eBonus, p.getX(), p.getY(), bIgnoreLatitude))
			continue;

		p.setBonusType(eBonus);
		iBonusCount--;
		// advc.129: Replacing the loop below
		iBonusCount -= placeGroup(eBonus, p, bIgnoreLatitude, iBonusCount);
		/*for (int iDX = -(kBonus.getGroupRange()); iDX <= kBonus.getGroupRange(); iDX++) {
			for (int iDY = -(kBonus.getGroupRange()); iDY <= kBonus.getGroupRange(); iDY++) {
				if (iBonusCount > 0) {
					CvPlot* pLoopPlot	= plotXY(p.getX(), p.getY(), iDX, iDY);
					if (pLoopPlot != NULL) {
						if (canPlaceBonusAt(eBonus, pLoopPlot->getX(), pLoopPlot->getY(), bIgnoreLatitude)) {
							if (MapRandNum(100) < kBonus.getGroupRand()) {
								pLoopPlot->setBonusType(eBonus);
								iBonusCount--;
		} } } } } }
		FAssertMsg(iBonusCount >= 0, "iBonusCount must be >= 0");*/
		if (iBonusCount == 0)
			break;
	}
	SAFE_DELETE_ARRAY(aiShuffledIndices);
}

// advc.129:
int CvMapGenerator::placeGroup(BonusTypes eBonus, CvPlot const& kCenter,
	bool bIgnoreLatitude, int iLimit)
{
	CvBonusInfo const& kBonus = GC.getInfo(eBonus);
	// The one in the center is already placed, but that doesn't count here.
	int iPlaced = 0;
	std::vector<CvPlot*> apGroupRange;
	// BtS used a square here (but also only used GroupRange 1)
	for (PlotCircleIter it(kCenter, kBonus.getGroupRange()); it.hasNext(); ++it)
		apGroupRange.push_back(&*it);
	int const iSize = (int)apGroupRange.size();
	if (iSize <= 0)
		return 0;
	std::vector<int> aiShuffled(iSize);
	mapRand().shuffle(aiShuffled);
	for (int j = 0; j < iSize &&
		iLimit > 0; j++)
	{
		CvPlot& kPlot = *apGroupRange[aiShuffled[j]];
		if (!canPlaceBonusAt(eBonus, kPlot.getX(), kPlot.getY(), bIgnoreLatitude))
			continue;
		scaled rAddBonusProb = per100(kBonus.getGroupRand());
		// Make large clusters exponentially unlikely
		rAddBonusProb *= fixp(2/3.).pow(iPlaced);
		if (MapRandSuccess(rAddBonusProb))
		{
			kPlot.setBonusType(eBonus);
			iLimit--;
			iPlaced++;
		}
	}
	FAssert(iLimit >= 0);
	return iPlaced;
}


void CvMapGenerator::addGoodies()
{
	PROFILE_FUNC();

	if (GC.getPythonCaller()->addGoodies())
		return;

	gDLL->NiTextOut("Adding Goodies...");

	if (GC.getInfo(GC.getGame().getStartEra()).isNoGoodies())
		return;

	CvMap const& kMap = GC.getMap();
	int* aiShuffledIndices = mapRand().shuffle(kMap.numPlots());
	FOR_EACH_ENUM(Improvement)
	{
		ImprovementTypes const eGoody = eLoopImprovement;
		if (!GC.getInfo(eGoody).isGoody())
			continue;
		int const iTilesPerGoody = GC.getInfo(eGoody).getTilesPerGoody();
		if (iTilesPerGoody <= 0)
			continue;
		// advc.opt: Count the goodies here instead of storing the counts at CvArea
		std::map<int,short> goodiesPerArea;
		for (int i = 0; i < kMap.numPlots(); i++)
		{
			CvPlot& kPlot = kMap.getPlotByIndex(aiShuffledIndices[i]);
			if (kPlot.isWater())
				continue;

			CvArea const& kArea = kPlot.getArea();
			if (goodiesPerArea[kArea.getID()] < // advc.opt: was kArea.getNumImprovements(eImprov)
				intdiv::uround(kArea.getNumTiles(), iTilesPerGoody))
			{
				if (canPlaceGoodyAt(eGoody, kPlot.getX(), kPlot.getY()))
				{
					kPlot.setImprovementType(eGoody);
					goodiesPerArea[kArea.getID()]++; // advc.opt
				}
			}
		}
		gDLL->callUpdater(); // advc.opt: Moved out of the loop
	}
	SAFE_DELETE_ARRAY(aiShuffledIndices);
}


void CvMapGenerator::eraseRivers()
{
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
	{
		CvPlot& kPlot = kMap.getPlotByIndex(i);
		if (kPlot.isNOfRiver())
			kPlot.setNOfRiver(false, NO_CARDINALDIRECTION);
		if (kPlot.isWOfRiver())
			kPlot.setWOfRiver(false, NO_CARDINALDIRECTION);
	}
}

void CvMapGenerator::eraseFeatures()
{
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
		kMap.getPlotByIndex(i).setFeatureType(NO_FEATURE);
}

void CvMapGenerator::eraseBonuses()
{
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
		kMap.getPlotByIndex(i).setBonusType(NO_BONUS);
}

void CvMapGenerator::eraseGoodies()
{
	CvMap const& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
		kMap.getPlotByIndex(i).removeGoody();
	// (advc: isGoody check moved into removeGoody)
}


void CvMapGenerator::generateRandomMap()
{
	PROFILE_FUNC();

	CvPythonCaller const& py = *GC.getPythonCaller();
	py.callMapFunction("beforeGeneration");
	if (py.generateRandomMap()) // will call applyMapData when done
		return;

	char buf[256];

	sprintf(buf, "Generating Random Map %S, %S...", gDLL->getMapScriptName().GetCString(), GC.getInfo(GC.getMap().getWorldSize()).getDescription());
	gDLL->NiTextOut(buf);

	generatePlotTypes();
	generateTerrain();
	/* advc.300: Already done in CvMap::calculateAreas, but when calculateAreas
	   is called during map generation, tile yields aren't yet set. */
	GC.getMap().computeShelves();
	// <advc.108>
	if (py.isAnyCustomMapOptionSetTo(gDLL->getText("TXT_KEY_MAP_BALANCED")))
		GC.getGame().setStartingPlotNormalizationLevel(CvGame::NORMALIZE_HIGH);
	// </advc.108>
}

void CvMapGenerator::generatePlotTypes()
{
	int const iNumPlots = GC.getMap().numPlots();
	int* paiPlotTypes = new int[iNumPlots];
	if (!GC.getPythonCaller()->generatePlotTypes(paiPlotTypes, iNumPlots))
	{
		for (int iI = 0; iI < iNumPlots; iI++)
			paiPlotTypes[iI] = PLOT_LAND;
	}
	setPlotTypes(paiPlotTypes);
	SAFE_DELETE_ARRAY(paiPlotTypes);
}

void CvMapGenerator::generateTerrain()
{
	PROFILE_FUNC();

	std::vector<int> pyTerrain;
	CvMap const& kMap = GC.getMap();
	if (GC.getPythonCaller()->generateTerrainTypes(pyTerrain, kMap.numPlots()))
	{
		for (int i = 0; i < kMap.numPlots(); i++)
		{
			//gDLL->callUpdater(); // addvc.003b
			kMap.plotByIndex(i)->setTerrainType((TerrainTypes)pyTerrain[i], false, false);
		}
	}
}


void CvMapGenerator::afterGeneration()
{
	PROFILE_FUNC();
	// Allows for user-defined Python Actions for map generation after it's already been created
	GC.getPythonCaller()->callMapFunction("afterGeneration");
	GC.getLogger().logMapStats(); // advc.mapstat
}

void CvMapGenerator::setPlotTypes(const int* paiPlotTypes)
{
	CvMap& kMap = GC.getMap();
	for (int i = 0; i < kMap.numPlots(); i++)
	{
		//gDLL->callUpdater(); // advc.opt: Not needed I reckon
		kMap.getPlotByIndex(i).setPlotType((PlotTypes)paiPlotTypes[i], false, false);
	}

	kMap.recalculateAreas();

	for (int i = 0; i < kMap.numPlots(); i++)
	{
		//gDLL->callUpdater(); // advc.opt
		CvPlot& p = kMap.getPlotByIndex(i);
		if (p.isWater())
		{
			if (p.isAdjacentToLand())
				p.setTerrainType(GC.getWATER_TERRAIN(true), false, false);
			else p.setTerrainType(GC.getWATER_TERRAIN(false), false, false);
		}
	}
}


int CvMapGenerator::getRiverValueAtPlot(CvPlot const& kPlot) const // advc: const x2
{
	bool bOverride=false;
	int pyValue = GC.getPythonCaller()->riverValue(kPlot, bOverride);
	if (bOverride)
		return pyValue;
	int iSum = pyValue; // Add to value from Python

	/*iSum += (NUM_PLOT_TYPES - kPlot.getPlotType()) * 20;
	FOR_EACH_ENUM(Direction) {
		CvPlot* pAdj = plotDirection(kPlot.getX(), kPlot.getY(), eLoopDirection);
		if (pAdj != NULL)
			iSum += (NUM_PLOT_TYPES - pAdj->getPlotType());
		else iSum += (NUM_PLOT_TYPES * 10);
	}*/
	/*	<advc.129> kPlot is the plot at whose southeastern corner the river will arrive.
		That corner also touches 3 other plots, which are no less important.
		In addition to those 4, I'm going to count the 8 plots orthogonally adjacent
		to them, resulting in a 4x4 square without its 4 corners.
		(This range is awkward to traverse b/c it doesn't have a center plot.) */
	CvMap const& kMap = GC.getMap();
	for (int iDX = 0; iDX < 4; iDX++)
	{
		int const iX = kPlot.getX() - 1 + iDX; // west to east
		for (int iDY = 0; iDY < 4; iDY++)
		{
			int const iY = kPlot.getY() + 1 - iDY; // north to south
			// Skip corners
			if ((iDX == 0 || iDX == 3) && (iDY == 0 || iDY == 3))
				continue;
			CvPlot const* p = kMap.plotValidXY(iX, iY);
			int iPlotVal = NUM_PLOT_TYPES * 3; // p == NULL
			if (p != NULL)
			{
				if (p->isWater() && !p->isLake())
				{	/*	The term in the else branch (as in BtS) counts 1 more
						for hills than for flat and would count 1 less
						for water than for flat. I'm making (non-lake) water
						symmetrical with peak instead. */
					iPlotVal = 0;
				}
				else iPlotVal = NUM_PLOT_TYPES - p->getPlotType();
			}
			// Inner plots have much higher weight
			if ((iDX == 1 || iDX == 2) && (iDY == 1 || iDY == 2))
				iPlotVal *= 6;
			iSum += iPlotVal;
		}
	} // <advc.129>
	CvRandom riverRand;
	riverRand.init(kPlot.getX() * 43251267 + kPlot.getY() * 8273903);
	// advc.129: Was 10. The scale hasn't really changed; I just want more randomness.
	iSum += riverRand.get(20, "River Rand");

	return iSum;
}

// Calculates and returns the number of resources of eBonus to be placed
int CvMapGenerator::calculateNumBonusesToAdd(BonusTypes eBonus)
{
	CvBonusInfo const& kBonus = GC.getInfo(eBonus);
	CvMap const& kMap = GC.getMap();

	int iBaseCount = kBonus.getConstAppearance();
	{
		int iRand1 = MapRandNum(kBonus.getRandAppearance1());
		int iRand2 = MapRandNum(kBonus.getRandAppearance2());
		int iRand3 = MapRandNum(kBonus.getRandAppearance3());
		int iRand4 = MapRandNum(kBonus.getRandAppearance4());
		iBaseCount += iRand1 + iRand2 + iRand3 + iRand4;
	}
	bool const bIgnoreLatitude = GC.getPythonCaller()->isBonusIgnoreLatitude();

	//int iLandTiles = 0; // advc: misleadingly named
	int iFromTiles = 0;
	if (kBonus.getTilesPer() > 0)
	{
		int iNumPossible = 0; // Number of plots eligible to have this bonus
		for (int i = 0; i < kMap.numPlots(); i++)
		{
			CvPlot const& kPlot = kMap.getPlotByIndex(i);
			if (kPlot.canHaveBonus(eBonus, bIgnoreLatitude))
				iNumPossible++;
		}
		// <advc.129>
		if (GC.getDefineBOOL("SUBLINEAR_BONUS_QUANTITIES"))
		{
			int iSubtrahend = kBonus.getTilesPer(); // Typically 16 or 32
			// For normalization; don't want to place fewer resources in general.
			iSubtrahend = (fixp(0.83) * iSubtrahend).ceil();
			int iRemainder = iNumPossible;
			int iResult = 0;
			/* Place one for the first, say, 14 tiles, the next after 15, then 16 ...
			   i.e. number of resources placed grows sublinearly with the number of
			   eligible plots. */
			while(true)
			{
				iRemainder -= iSubtrahend;
				if(iRemainder < 0)
					break;
				iResult++;
				iSubtrahend++;
			}
			iFromTiles += iResult;
		}
		else // </advc.129>
			iFromTiles += (iNumPossible / kBonus.getTilesPer());
	}

	scaled rFromPlayers = GC.getGame().countCivPlayersAlive() *
			per100(kBonus.getPercentPerPlayer());
	/*	<advc.129> Same as in BtS for 8 players, a bit less for high player counts,
		a bit more for small player counts. */
	rFromPlayers.exponentiate(fixp(0.8));
	rFromPlayers *= fixp(1.5); // </advc.129>
	int iBonusCount = (iBaseCount * (iFromTiles + rFromPlayers.round())) / 100;
	return std::max(1, iBonusCount);
}
