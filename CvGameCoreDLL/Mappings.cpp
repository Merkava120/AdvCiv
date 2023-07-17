#include "CvGameCoreDLL.h"
#include "Mappings.h"
#include "CvMap.h"
#include "CvGame.h"
#include "CvArea.h"
#include "CvInfo_Terrain.h"


Mappings::Mappings()
{
	// Init mapping values from global defines
	m_iOverrideMode = GC.getDefineINT("MAPPING_OVERRIDE_MODE");
	m_iWaterMode = GC.getDefineINT("FLIP_WATER");
	m_iNumMappings = getRandBetween(GC.getDefineINT("MIN_MAPPINGS"), GC.getDefineINT("MAX_MAPPINGS"), true);
	m_iMinPercentABM = GC.getDefineINT("MIN_PERCENT_OF_AREA_BIOMES_MAPPED");
	m_iMaxPercentABM = GC.getDefineINT("MAX_PERCENT_OF_AREA_BIOMES_MAPPED");
	m_iMinMappingsPerArea = GC.getDefineINT("MIN_MAPPINGS_PER_AREA");
	m_iMaxMappingsPerArea = GC.getDefineINT("MAX_MAPPINGS_PER_AREA");
	m_iMinBiomesPerMapping = GC.getDefineINT("MIN_BIOMES_PER_MAPPING");
	m_iMaxBiomesPerMapping = GC.getDefineINT("MAX_BIOMES_PER_MAPPING");
	m_iUnmappableDoWhat = GC.getDefineINT("UNMAPPABLE_BIOMES_DO_WHAT");
	m_iUnmappableSwaps = GC.getDefineINT("UNMAPPABLE_BIOMES_TRY_SWAPS");
	m_iMinAreaSize = GC.getDefineINT("MIN_MAPPING_AREA_SIZE");
	m_iMaxAreaSize = GC.getDefineINT("MAX_MAPPING_AREA_SIZE");
	m_iRepeatMode = GC.getDefineINT("MAPPING_REPEAT_MODE");
	m_iMaxMapInfos = GC.getDefineINT("MAX_MAPINFOS");
	std::vector<int> aiBannedTypes;
	collectNums(aiBannedTypes, GC.getDefineINT("BAN_TYPES"), 10);
	std::vector<int> aiForcedTypes;
	collectNums(aiForcedTypes, GC.getDefineINT("FORCE_TYPES"), 10);
	collectNums(m_aiForceIncludeTypes, GC.getDefineINT("FORCE_INCLUDE_TYPES"), 10);
	for (int i = 0; i < GC.getNumMappingInfos(); i++)
	{
		CvMappingInfo const& kMapping = GC.getMappingInfo((MappingTypes)i);
		if (!contains(m_aiAllowedTypes, kMapping.get(CvMappingInfo::iMappingType)))
			m_aiAllowedTypes.push_back(kMapping.get(CvMappingInfo::iMappingType));
	}
	if ((int)aiBannedTypes.size() > 0)
	{
		for (int h = 0; h < (int)m_aiAllowedTypes.size(); h++)
		{
			if (contains(aiBannedTypes, m_aiAllowedTypes[h]))
				m_aiAllowedTypes.erase(m_aiAllowedTypes.begin() + h);
		}
	}
	if ((int)aiForcedTypes.size() > 0)
	{
		for (int h = 0; h < (int)m_aiAllowedTypes.size(); h++)
		{
			if (!contains(aiForcedTypes, m_aiAllowedTypes[h]))
				m_aiAllowedTypes.erase(m_aiAllowedTypes.begin() + h);
		}
	}
}

void Mappings::collectNums(std::vector<int>& aiCollectNums, int iCollectInt, int power)
{
	bool bDone = false;
	int iTypes = iCollectInt;
	if (iTypes < 0)
		return;
	if (iTypes < power)
	{
		bDone = true;
		aiCollectNums.push_back(iTypes);
	}
	while (!bDone)
	{
		if (iTypes == 0)
			bDone = true;
		aiCollectNums.push_back(iTypes % power);
		iTypes = (iTypes - (iTypes % power)) / power;
	}
}

int Mappings::getRandBetween(int iMin, int iMax, bool bNoNegative) const
{
	int iRand = SyncRandNum(iMax - iMin) + iMin;
	if (bNoNegative && iRand < 0)
		return 0;
	else
		return iRand;
}

bool Mappings::contains(std::vector<int> ThisVector, int iThisInt) const
{
	for (int x = 0; x < (int)ThisVector.size(); x++)
	{
		if (ThisVector[x] == iThisInt)
			return true;
	}
	return false;
}

int Mappings::index(std::vector<int> inThisVector, int iFindThisInt) const
{
	for (int i = 0; i < (int)inThisVector.size(); i++)
	{
		if (inThisVector[i] == iFindThisInt)
			return i;
	}
	return -1;
}

bool Mappings::isEligibleArea(int iAreaID) const
{
	CvArea *pArea = GC.getMap().getArea(iAreaID);
	if (pArea->isWater())
		return false; // ocean areas are handled separately if mapped at all
	int iSize = pArea->getNumTiles();
	return (iSize >= m_iMinAreaSize && iSize <= m_iMaxAreaSize);
}

bool Mappings::isEligibleMapping(MappingTypes eMapping) const
{
	CvMappingInfo const& kMappingInfo = GC.getMappingInfo(eMapping);
	if ((int)m_aiForceIncludeTypes.size() > 0)
		return (contains(m_aiForceIncludeTypes, kMappingInfo.get(CvMappingInfo::iMappingType)));
	bool bInclude = kMappingInfo.isInclude();
	return (bInclude && contains(m_aiAllowedTypes, kMappingInfo.get(CvMappingInfo::iMappingType)));
}

// used for initial placement of mappings, so already have mapping or is not prereq makes false
bool Mappings::isBiomeCanMapping(int iBiome, MappingTypes eMapping) const
{
	if (GC.getGame().getBiomeMapping(iBiome) != NO_MAPPING)
		return false; // can't have another mapping
	CvMappingInfo const& kMappingInfo = GC.getMappingInfo(eMapping);
	if (!GC.getGame().isBiomeWithinLatitudes(iBiome, kMappingInfo.get(CvMappingInfo::iMaxLatitude), kMappingInfo.get(CvMappingInfo::iMinLatitude)))
		return false;
	if (kMappingInfo.isBannedBiomeTerrain(GC.getGame().getBiomeTerrain(iBiome)))
		return false;
	return (kMappingInfo.isPrereqBiomeTerrain(GC.getGame().getBiomeTerrain(iBiome)));
}


bool Mappings::isAdjacentToMapping(int iCenterBiome, MappingTypes eMapping) const
{
	CvGame::BiomeData biome = GC.getGame().getBiomeData(iCenterBiome);
	for (int i = 0; i < (int)biome.aiAdjBiomes.size(); i++)
	{
		if (GC.getGame().getBiomeMapping(biome.aiAdjBiomes[i]) == eMapping)
			return true;
	}
	return false;
}

void Mappings::trimRandomly(std::vector<int>& aiThisVector, int iFinalSize)
{
	while ((int)aiThisVector.size() > iFinalSize)
	{
		aiThisVector.erase(aiThisVector.begin() + SyncRandNum((int)aiThisVector.size()));
	}
}

int Mappings::countAreaBiomes(int iAreaID) const
{
	int iNum = 0;
	if (GC.getMap().getArea(iAreaID)->isWater())
		return 0;
	for (int i = 0; i < GC.getGame().getNumBiomes(); i++)
	{
		if (GC.getGame().isBiomeInLandArea(i, iAreaID))
			iNum++;
	}
	return iNum;
}

int Mappings::getNumBiomesToMap(int iAvailable, int iPercentage) const
{
	return (iPercentage * iAvailable) / 100;
}

int Mappings::getNumMappingsToMap(int iBiomes)
{
	// biomes / max biomes per mapping: minimum possible mappings. If min mappings per area greater, that's the real minimum. 
	int iMin = std::max(iBiomes / m_iMaxBiomesPerMapping, m_iMinMappingsPerArea);
	// biomes / min biomes per mapping: maximum possible mappings. If max mappings per area less, that's the real max. 
	int iMax = std::min(iBiomes / m_iMinBiomesPerMapping, m_iMaxMappingsPerArea);
	return getRandBetween(iMin, iMax, true);
}

int Mappings::getUnmappedBiomeFromArea(int iAreaID) const
{
	std::vector<int> unmappedBiomes = getAllUnmappedAreaBiomes(iAreaID);
	if ((int)unmappedBiomes.size() > 0)
		return (unmappedBiomes[SyncRandNum((int)unmappedBiomes.size())]);
	else
		return -1;
}

//// Loops through adjacent biomes, looks for them in aiCenterBiomes, and returns the index if found
//int Mappings::getMappingIndexFromAdjacentBiomes(int iCenterBiome, std::vector<int> aiCenterBiomes, MappingTypes eOnlyThisMapping) const
//{
//
//}

// This method takes into account repeating modes and prereqs but not adjacency
MappingTypes Mappings::chooseMappingForBiome(int iBiome, int iAreaID) const
{
	std::vector<int> mappedBiomes = getAllUnmappedAreaBiomes(iAreaID, true);
	std::vector<MappingTypes> alreadyMappings;
	for (int i = 0; i < (int)mappedBiomes.size(); i++)
	{
		alreadyMappings.push_back(GC.getGame().getBiomeMapping(mappedBiomes[i]));
	}
	std::vector<MappingTypes> canMappings;
	int iRepeats = 0;
	for (int i = 0; i < GC.getNumMappingInfos(); i++)
	{
		if (!contains(m_aiAllowedTypes, GC.getMappingInfo((MappingTypes)i).get(CvMappingInfo::iMappingType)))
			continue;
		if (!isBiomeCanMapping(iBiome, (MappingTypes)i))
			continue;
		bool bContinue = false;
		for (int j = 0; j < (int)alreadyMappings.size(); j++)
		{
			if (alreadyMappings[j] == (MappingTypes)i)
			{
				if (m_iRepeatMode == 1)
				{
					bContinue = true;
					break;
				}
				else if (m_iRepeatMode == 2)
					iRepeats++;
			}
		}
		if (bContinue)
			continue;
	}
}

// Central function for placing all the mappings. 
void Mappings::placeMappings()
{
	// handle special modes
	if (m_iOverrideMode != 0)
	{
		if (m_iOverrideMode > 0 && m_iOverrideMode < 4)
		{
			switch (m_iOverrideMode)
			{
			case 1:
				doPlanetsMode();
			case 2:
				doChaosMode();
			case 3:
				doWTFMode();
			}
		}
		else if (m_iOverrideMode >= 4)
			doAllBiomesMode(m_iOverrideMode);
		else if (m_iOverrideMode < 0)
			doAllAreasMode(m_iOverrideMode * -1);
		return;
	}
	// Place areas in vector - only available ones using area sizes
	std::vector<int> aiAreaIDs;
	FOR_EACH_AREA(pArea)
	{
		if (isEligibleArea(pArea->getID()))
			aiAreaIDs.push_back(pArea->getID());
	}
	// Place mappings in a vector accounting for Max_MapInfos
	std::vector<int> aiAvailableMappings;
	FOR_EACH_ENUM(Mapping)
	{
		if (isEligibleMapping(eLoopMapping))
			aiAvailableMappings.push_back((int)eLoopMapping);
	}
	trimRandomly(aiAvailableMappings, m_iMaxMapInfos);
	// Loop through areas now
	std::vector<int> aiBiomeNums;
	int iTotalMappingsMapped = 0;
	for (int i = 0; i < (int)aiAreaIDs.size(); i++)
	{
		// Count biomes in the area
		int iNumBiomes = (countAreaBiomes(aiAreaIDs[i]));
		// Assign a percentage
		int iPercentage = 100;
		if (m_iMinPercentABM == m_iMaxPercentABM)
			iPercentage = m_iMinPercentABM;
		else
			iPercentage = getRandBetween(m_iMinPercentABM, m_iMaxPercentABM);
		// Make vector of the number of biomes to map
		std::vector<int> aiCenterBiomes;
		int iMappings = getNumMappingsToMap((getNumBiomesToMap(iNumBiomes, iPercentage)));
		int* aiMappingBiomeTotals = new int[iMappings];
		MappingTypes* aeMappings = new MappingTypes[iMappings];
		int iTotalBiomes = 0;
		for (int j = 0; j < iMappings && iTotalBiomes < iNumBiomes; j++)
		{
			// This getBiome method should only consider biomes that do not have mappings
			int iCenterBiome = getUnmappedBiomeFromArea(aiAreaIDs[i]);
			aiCenterBiomes.push_back(iCenterBiome);
			GC.getGame().setBiomeMapping(iCenterBiome, chooseMappingForBiome(iCenterBiome, aiAreaIDs[i]));
			iTotalBiomes++; // This makes sure we don't try to search for biomes when none are left
			aeMappings[j] = GC.getGame().getBiomeMapping(iCenterBiome);
			m_aiMappedTypes.push_back(GC.getMappingInfo(aeMappings[j]).get(CvMappingInfo::iMappingType));
			aiMappingBiomeTotals[j] = getRandBetween(m_iMinBiomesPerMapping, m_iMaxBiomesPerMapping);
		}
		// So now we have a list of center biomes, a list of mappings, and a list of totals. Let's look at all the other biomes and give them adjacent mapping types. 
		std::vector<int>* aiMappingBiomes = new std::vector<int>[iMappings];
		bool bFinished = false;
		bool bReallyFinished = false;
		while (!bFinished)
		{
			int iNumZeros = 0;
			int iNegatives = 0;
			for (int j = 0; j < iMappings; j++)
			{
				if (aiMappingBiomeTotals[j] == 0)
				{
					iNumZeros++;
					if (iNumZeros == iMappings)
					{
						bFinished = true;
						bReallyFinished = true;
						break;
					}
					else
						continue;
				}
				int iNextBiome = getAdjacentEligibleBiome(aiCenterBiomes[j], aeMappings[j]);
				if (iNextBiome != -1)
				{
					aiMappingBiomes[j].push_back(iNextBiome);
					aiMappingBiomeTotals[j]--;
					GC.getGame().setBiomeMapping(iNextBiome, aeMappings[j]);
				}
				else
				{
					iNegatives++;
					if (iNegatives == (iMappings - iNumZeros))
					{
						bFinished = true;
						break;
					}
				}
			}
		}
		// Okay now a bunch more biomes should have been placed into mappings. 
		std::vector<int> aiUnmappableBiomes;
		if (!bReallyFinished) // this means some of the mappings still need more
		{
			std::vector<int> aiUnmappedBiomes = getAllUnmappedAreaBiomes(aiAreaIDs[i]);
			// If there are biomes left
			if ((int)aiUnmappedBiomes.size() != 0)
			{
				// Go through each biome
				for (int j = 0; j < (int)aiUnmappedBiomes.size(); j++)
				{
					int iNumZeros = 0;
					bool bFound = false;
					// And check each mapping placed in this area
					for (int k = 0; k < iMappings; k++)
					{
						if (aiMappingBiomeTotals[k] == 0)
						{
							iNumZeros++;
							if (iNumZeros == iMappings)
							{
								bReallyFinished = true;
								break;
							}
							else
								continue;
						}
						if (isAdjacentToMapping(aiUnmappedBiomes[j], aeMappings[k]) && isBiomeCanMapping(aiUnmappedBiomes[j], aeMappings[k]))
						{
							// This biome can have this mapping. 
							aiMappingBiomes[k].push_back(aiUnmappedBiomes[j]);
							aiMappingBiomeTotals[k]--;
							GC.getGame().setBiomeMapping(aiUnmappedBiomes[j], aeMappings[k]);
							bFound = true;
							break; //from mappings loop
						}
					}
					if (bReallyFinished)
						break; // from biomes loop
					else if (bFound)
						continue; // to next biome; that one's good
					else // if didn't find mapping and didn't fill up list, this is 'unmappable'
						aiUnmappableBiomes.push_back(aiUnmappedBiomes[j]);
				}
			}
			else
			{
				// We didn't fill up all the mappings but we ran out of biomes. So, done. 
				bReallyFinished = true;
			}
		}
		// If we made it through that whole loop and bReallyFinished never set to True,
		// That means we have unmappable biomes and space left to fill. 
		if (!bReallyFinished)
		{
			mapUnmappableBiomes(aiUnmappableBiomes);
		}
	}
	// Now all areas should be filled up with mappings. 
	// So, loop through all the biomes and flip their terrains. 
	// But first:
	handleForceIncludes();
	for (int i = 0; i < GC.getGame().getNumBiomes(); i++)
	{
		placeMapping(i);
	}
}