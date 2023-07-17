#pragma once
#ifndef MAPPINGS_H
#define MAPPINGS_H

class Mappings
{
public:
	Mappings();
	void collectNums(std::vector<int>& aiCollectNums, int iCollectInt, int power);
	int getRandBetween(int iMin, int iMax, bool bNoNegative = false) const;
	bool contains(std::vector<int> ThisVector, int iThisInt) const;
	int index(std::vector<int> inThisVector, int iFindThisInt) const;
	bool isEligibleArea(int iAreaID) const;
	bool isEligibleMapping(MappingTypes eMapping) const;
	bool isBiomeCanMapping(int iBiome, MappingTypes eMapping) const;
	bool isAdjacentToMapping(int iCenterBiome, MappingTypes eMapping) const;
	void trimRandomly(std::vector<int>& aiThisVector, int iFinalSize);
	int countAreaBiomes(int iAreaID) const;
	int getNumBiomesToMap(int iAvailable, int iPercentage) const;
	int getNumMappingsToMap(int iBiomes);
	int getUnmappedBiomeFromArea(int iAreaID) const;
	/*int getMappingIndexFromAdjacentBiomes(int iCenterBiome, std::vector<int> aiCenterBiomes, MappingTypes eOnlyThisMapping = NO_MAPPING) const;*/
	MappingTypes chooseMappingForBiome(int iBiome, int iAreaID) const; // take into account repeating mode
	//MappingTypes chooseMappingFromAdjacent(int iCenterBiome) const;
	//int getAnotherBiomeForMappedBiome(int iBiome, MappingTypes eMapping) const;
	std::vector<int> getAllUnmappedAreaBiomes(int iAreaID, bool bReverse = false) const;
	//void swapMappings(int iBiome);
	int getAdjacentEligibleBiome(int iCenterBiome, MappingTypes eMapping) const;
	void mapUnmappableBiomes(std::vector<int> aiUnmappableBiomes);
	void placeMapping(int iBiome);
	void doPlanetsMode();
	void doChaosMode();
	void doWTFMode();
	void doAllBiomesMode(int iProbability);
	void doAllAreasMode(int iProbability);
	void placeMappings();
	void handleForceIncludes();
private:
	int m_iOverrideMode;
	int m_iWaterMode;
	int m_iRepeatMode;
	int m_iMaxMapInfos;
	int m_iNumMappings;
	int m_iMinPercentABM;
	int m_iMaxPercentABM;
	int m_iMinMappingsPerArea;
	int m_iMaxMappingsPerArea;
	int m_iMinBiomesPerMapping;
	int m_iMaxBiomesPerMapping;
	int m_iMinAreaSize;
	int m_iMaxAreaSize;
	int m_iUnmappableSwaps;
	int m_iUnmappableDoWhat;
	std::vector<int> m_aiAllowedTypes;
	std::vector<int> m_aiForceIncludeTypes;
	std::vector<int> m_aiMappedTypes;
};

#endif