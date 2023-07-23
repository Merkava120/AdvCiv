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

	void setPlotTypes(const int* paiPlotTypes);						// Exposed to Python
	// merk.msm
	void applyMappings();
	void applyFeatureMappings(int iTile);
	void handleUnmappedArea(int iNewMapping, CvPlot& kPlot);
	void applyTerrainMappings(int iTile);
	void applyImprovementMappings(int iTile);
	bool isMappingValid(CvPlot const& kPlot, FeatureTypes eFeatureMapping) const;
	bool isMappingValid(CvPlot const& kPlot, TerrainTypes eTerrainMapping) const;
	bool isMappingValid(CvPlot const& kPlot, ImprovementTypes eImprovementMapping) const;
	int getMappingWeight(CvPlot const& kPlot, FeatureTypes eFeatureMapping) const;
	int getMappingWeight(CvPlot const& kPlot, TerrainTypes eTerrainMapping) const;
	int getMappingWeight(CvPlot const& kPlot, ImprovementTypes eImprovementMapping) const;
	// merk.msm end

protected:

	int getRiverValueAtPlot(CvPlot const& kPlot) const;
	int calculateNumBonusesToAdd(BonusTypes eBonus);
	// advc.129: To avoid duplicate code in addUniqueBonus and addNonUniqueBonus
	int placeGroup(BonusTypes eBonus, CvPlot const& kCenter,
			bool bIgnoreLatitude, int iLimit = 100);
	// merk.msm
	std::vector< FeatureTypes > m_aiIncludeFeatures;
	std::vector< TerrainTypes > m_aiIncludeTerrains;
	std::vector< ImprovementTypes > m_aiIncludeImprovements;
	std::vector< int > m_aiPlacedChannels;
	// merk.msm end
private:
	static CvMapGenerator* m_pInst;

};
#endif
