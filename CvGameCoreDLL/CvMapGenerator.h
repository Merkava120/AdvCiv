#pragma once

#ifndef CIV4_MAPGENERATOR_H
#define CIV4_MAPGENERATOR_H

class CvFractal;
class CvPlot;
class CvArea;

class CvMapGenerator
{
public:
	DllExport static CvMapGenerator& GetInstance();
	DllExport static void FreeInstance() { SAFE_DELETE(m_pInst); }

	bool canPlaceBonusAt(BonusTypes eBonus, int iX, int iY,						// Exposed to Python
			bool bIgnoreLatitude, bool bCheckRange = true) const; // advc.129
	bool canPlaceGoodyAt(ImprovementTypes eGoody, int iX, int iY) const;		// Exposed to Python

	// does all of the below "add..." functions:
	DllExport void addGameElements();											// Exposed to Python

	void addLakes();																			// Exposed to Python
	DllExport void addRivers();														// Exposed to Python
	void doRiver(CvPlot* pStartPlot,												// Exposed to Python
			CardinalDirectionTypes eLastCardinalDirection = NO_CARDINALDIRECTION,
			CardinalDirectionTypes eOriginalCardinalDirection = NO_CARDINALDIRECTION,
			short iThisRiverID = -1); // advc.opt: was int
	bool addRiver(CvPlot *pFreshWaterPlot);
	DllExport void addFeatures();													// Exposed to Python
	DllExport void addBonuses();													// Exposed to Python
	void addUniqueBonusType(BonusTypes eBonus);					// Exposed to Python
	void addNonUniqueBonusType(BonusTypes eBonus);			// Exposed to Python
	DllExport void addGoodies();													// Exposed to Python

	DllExport void eraseRivers();													// Exposed to Python
	DllExport void eraseFeatures();												// Exposed to Python
	DllExport void eraseBonuses();												// Exposed to Python
	DllExport void eraseGoodies();												// Exposed to Python

	DllExport void generateRandomMap();										// Exposed to Python

	void generatePlotTypes();															// Exposed to Python
	void generateTerrain();																// Exposed to Python

	void afterGeneration();																// Exposed to Python
	void applyMappings(); // Merkava120 1.1.1 terrain adjuster
	void setPlotVariation(CvTerrainInfo const& kTerrain, int p, CvMap& kMap, int iMapping, int iType = -1);
	void applyNewMappingChanges(int iNewVar, CvMap& kMap, int p, CvTerrainInfo const& kTerrain, bool bFeature = true, bool bBonus = true);
	int getMappingProbability(CvPlot* pPlot, CvTerrainInfo const& kTerrain, int iVariation);
	void CvMapGenerator::collectNums(std::vector<int>& aiCollectNums, int iCollectInt, int power = 10);
	bool isMappingHasType(int iMapping, int iType) const;
	bool CvMapGenerator::contains(std::vector<int> ThisVector, int iThisInt) const;
	bool CvMapGenerator::isHomogeneityEligible(CvPlot* pPlot, CvTerrainInfo const& kTerrain, int iVariation) const;
	int getRandVariationFromMapping(TerrainTypes eTerrain, int iMapping);
	void setPlotTypes(const int* paiPlotTypes);						// Exposed to Python

protected:

	int getRiverValueAtPlot(CvPlot const& kPlot) const;
	int calculateNumBonusesToAdd(BonusTypes eBonus);
	// advc.129: To avoid duplicate code in addUniqueBonus and addNonUniqueBonus
	int placeGroup(BonusTypes eBonus, CvPlot const& kCenter,
			bool bIgnoreLatitude, int iLimit = 100);

private:
	static CvMapGenerator* m_pInst;

};
#endif
