#pragma once

#ifndef CV_INFO_TERRAIN_H
#define CV_INFO_TERRAIN_H

/*  advc.003x: Cut from CvInfos.h. Info classes related to the natural terrain
	of individual non-city tiles and terrain improvements:
	CvTerrainInfo, CvFeatureInfo, CvBonusInfo, CvBonusClassInfo,
	CvRouteInfo, CvImprovementInfo, CvImprovementBonusInfo, CvGoodyInfo
	and CvBuildInfo (via include).
	(Infos related to the map options are handled by CvInfo_GameOption.h.
	Left in CvInfo_Misc.h: CvRouteModelInfo and CvRiverModelInfo - those are
	only used by the EXE.) */

#include "CvInfo_Build.h"

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvTerrainInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTerrainInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All the const functions are exposed to Python except for those related to sound
	CvTerrainInfo();
	~CvTerrainInfo();

	int getMovementCost() const { return m_iMovementCost; }
	int getSeeFromLevel() const { return m_iSeeFromLevel; }
	int getSeeThroughLevel() const { return m_iSeeThroughLevel; }
	int getBuildModifier() const { return m_iBuildModifier; }
	int getDefenseModifier() const { return m_iDefenseModifier; }
	int getTemp() const { return m_iTemp; } // merk.rasmore
	// merk.msm begin
	int getBaseTerrain() const { return m_iBaseTerrain; }
	int getBaseFeature() const { return m_iBaseFeature; }
	int getBaseFeatureWeight() const { return m_iUseBFWt; } // merk.msmfix
	int getBaseFeatureAdjWeight() const { return m_iAdjBFWt; } // merk.msmfix
	int getChanceInclude() const { return m_iChanceInclude; }
	int getChanceMap() const { return m_iChanceMap; }
	int getWtRiver() const { return m_iWtRiver; }
	int getWtHills() const { return m_iWtHills; }
	int getWtCoastal() const { return m_iWtCoastal; }
	int getWtCoast() const { return m_iWtCoast; }
	int getWtOcean() const { return m_iWtOcean; }
	int getMinLatitude() const { return m_iMinLatitude; }
	int getMaxLatitude() const { return m_iMaxLatitude; }
	int getMinAreaSize() const { return m_iMinAreaSize; }
	int getMaxAreaSize() const { return m_iMaxAreaSize; }
	int getMinAreaProportion() const { return m_iMinAreaProportion; }
	int getMaxAreaProportion() const { return m_iMaxAreaProportion; }
	int getAreaChannel() const { return m_iAreaChannel; }
	int getHillsAdjWeight() const { return m_iHillsAdjacentWeight; }
	int getCoastAdjWeight() const { return m_iCoastAdjacentWeight; }
	// merk.msm end

	bool isWater() const { return m_bWater; }
	bool isImpassable() const { return m_bImpassable; }
	bool isFound() const { return m_bFound; }
	bool isFoundCoast() const { return m_bFoundCoast; }
	bool isFoundFreshWater() const { return m_bFoundFreshWater; }
	// merk.msm begin
	bool isReqRiver() const { return m_bReqRiver; }
	bool isReqFlatlands() const { return m_bRequiresFlatlands; }
	bool isReqHills() const { return m_bReqHills; }
	bool isReqCoastal() const { return m_bReqCoastal; }
	bool isReqCoast() const { return m_bReqCoast; }
	bool isReqOcean() const { return m_bReqOcean; }
	bool isPlaceOnce() const { return m_bPlaceOnce; }
	bool isPlaceInGroup() const { return m_bPlaceInGroup; }
	bool isSurroundedByBase() const { return m_bSurroundedByBase; }
	// merk.msm end

	DllExport const TCHAR* getArtDefineTag() const;

	int getWorldSoundscapeScriptId() const;

	int getYield(int i) const;
	int getRiverYieldChange(int i) const;
	int getHillsYieldChange(int i) const;
	int get3DAudioScriptFootstepIndex(int i) const;
	// merk.msm begin
	int getTerrainWeight(int iTerrain) const;
	//int getFeatureWeight(int iFeature) const;
	int getTerrainAdjWeight(int iTerrain) const;
	//int getFeatureAdjWeight(int iFeature) const;
	// merk.msm end

	const CvArtInfoTerrain* getArtInfo() const;
	const TCHAR* getButton() const;

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML); // merk.msm
	bool readPass3(); // merk.msm


protected:
	int m_iMovementCost;
	int m_iSeeFromLevel;
	int m_iSeeThroughLevel;
	int m_iBuildModifier;
	int m_iDefenseModifier;
	int m_iTemp; // merk.rasmore
	// merk.msm begin
	int m_iBaseTerrain;
	int m_iBaseFeature;
	int m_iChanceInclude;
	int m_iUseBFWt; // merk.msmfix
	int m_iAdjBFWt; // merk.msmfix
	int m_iChanceMap;
	int m_iWtRiver;
	int m_iWtHills;
	int m_iWtCoastal;
	int m_iWtCoast;
	int m_iWtOcean;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iMinAreaSize;
	int m_iMaxAreaSize;
	int m_iMinAreaProportion;
	int m_iMaxAreaProportion;
	int m_iAreaChannel;
	int m_iHillsAdjacentWeight;
	int m_iCoastAdjacentWeight;
	// merk.msm end


	bool m_bWater;
	bool m_bImpassable;
	bool m_bFound;
	bool m_bFoundCoast;
	bool m_bFoundFreshWater;
	// merk.msm begin
	bool m_bReqRiver;
	bool m_bRequiresFlatlands;
	bool m_bReqHills;
	bool m_bReqCoastal;
	bool m_bReqCoast;
	bool m_bReqOcean;
	bool m_bPlaceOnce;
	bool m_bPlaceInGroup;
	bool m_bSurroundedByBase;
	// merk.msm end
	

	int m_iWorldSoundscapeScriptId;

	int* m_piYields;
	int* m_piRiverYieldChange;
	int* m_piHillsYieldChange;
	int* m_pi3DAudioScriptFootstepIndex;
	// merk.msm begin
	int* m_piTerrainWeights;
	//std::vector< int > m_piFeatureWeights;
	int* m_piAdjTerrainWeights;
	//std::vector< int > m_piAdjFeatureWeights;
	// merk.msm end


private:
	CvString m_szArtDefineTag;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvFeatureInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvFeatureInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: /*  All the const functions are exposed to Python except for those dealing with art
			and those added by mods */
	CvFeatureInfo();
	~CvFeatureInfo();

	int getMovementCost() const { return m_iMovementCost; }
	int getSeeThroughChange() const { return m_iSeeThroughChange; }
	int getHealthPercent() const { return m_iHealthPercent; }
	int getAppearanceProbability() const;
	int getDisappearanceProbability() const;
	int getGrowthProbability() const;
	int getDefenseModifier() const { return m_iDefenseModifier; }
	// advc.012:
	int getRivalDefenseModifier() const { return m_iRivalDefenseModifier; }
	int getAdvancedStartRemoveCost() const;
	int getTurnDamage() const;
	int getWarmingDefense() const; //GWmod new xml field M.A. // Exposed to Python
	int getTempAdd() const { return m_iTempAdd; } // merk.rasmore
	// merk.msm begin
	int getBaseTerrain() const { return m_iBaseTerrain; }
	int getBaseFeature() const { return m_iBaseFeature; }
	int getChanceInclude() const { return m_iChanceInclude; }
	int getChanceMap() const { return m_iChanceMap; }
	int getWtRiver() const { return m_iWtRiver; }
	int getWtHills() const { return m_iWtHills; }
	int getWtCoastal() const { return m_iWtCoastal; }
	int getWtCoast() const { return m_iWtCoast; }
	int getWtOcean() const { return m_iWtOcean; }
	int getMinLatitude() const { return m_iMinLatitude; }
	int getMaxLatitude() const { return m_iMaxLatitude; }
	int getMinAreaSize() const { return m_iMinAreaSize; }
	int getMaxAreaSize() const { return m_iMaxAreaSize; }
	int getMinAreaProportion() const { return m_iMinAreaProportion; }
	int getMaxAreaProportion() const { return m_iMaxAreaProportion; }
	int getAreaChannel() const { return m_iAreaChannel; }
	int getHillsAdjWeight() const { return m_iHillsAdjacentWeight; }
	int getCoastAdjWeight() const { return m_iCoastAdjacentWeight; }
	TerrainTypes getPlaceTerrain() const { return m_ePlaceTerrain; } // merk.msmadd
	// merk.msm end

	bool isNoCoast() const;
	bool isNoRiver() const;
	bool isNoRiverSide() const; // advc.129b
	bool isNoAdjacent() const;
	bool isRequiresFlatlands() const;
	bool isRequiresRiver() const;
	bool isRequiresRiverSide() const; // advc.129b
	bool isAddsFreshWater() const;
	bool isImpassable() const { return m_bImpassable; }
	bool isNoCity() const;
	bool isNoImprovement() const { return m_bNoImprovement; }
	bool isVisibleAlways() const;
	bool isNukeImmune() const;
	const TCHAR* getOnUnitChangeTo() const;
	// merk.msm begin
	bool isReqHills() const { return m_bReqHills; }
	bool isReqCoastal() const { return m_bReqCoastal; }
	bool isReqCoast() const { return m_bReqCoast; }
	bool isReqOcean() const { return m_bReqOcean; }
	bool isPlaceOnce() const { return m_bPlaceOnce; }
	bool isPlaceInGroup() const { return m_bPlaceInGroup; }
	bool isSurroundedByBase() const { return m_bSurroundedByBase; }
	// merk.msm end

	const TCHAR* getArtDefineTag() const;

	int getWorldSoundscapeScriptId() const;

	const TCHAR* getEffectType() const;
	int getEffectProbability() const;

	// merk.msm begin
	int getTerrainWeight(int iTerrain) const;
	int getFeatureWeight(int iFeature) const;
	int getTerrainAdjWeight(int iTerrain) const;
	int getFeatureAdjWeight(int iFeature) const;
	// merk.msm end

	int getYieldChange(int i) const
	{
		FAssertBounds(0, NUM_YIELD_TYPES, i);
		return m_piYieldChange[i]; // advc: Don't branch to check for NULL
	}
	int getRiverYieldChange(int i) const
	{
		FAssertBounds(0, NUM_YIELD_TYPES, i);
		return m_piRiverYieldChange[i]; // advc: see above
	}
	int getHillsYieldChange(int i) const
	{
		FAssertBounds(0, NUM_YIELD_TYPES, i);
		return m_piHillsYieldChange[i]; // advc: see above
	}
	int get3DAudioScriptFootstepIndex(int i) const;

	bool isTerrain(int i) const;
	int getNumVarieties() const;

	DllExport const CvArtInfoFeature* getArtInfo() const;
	const TCHAR* getButton() const;

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML); // merk.msm

protected:
	int m_iMovementCost;
	int m_iSeeThroughChange;
	int m_iHealthPercent;
	int m_iAppearanceProbability;
	int m_iDisappearanceProbability;
	int m_iGrowthProbability;
	int m_iDefenseModifier;
	int m_iRivalDefenseModifier; // advc.012
	int m_iAdvancedStartRemoveCost;
	int m_iTurnDamage;
	int m_iWarmingDefense; //GWMod
	int m_iTempAdd; // merk.rasmore
	// merk.msm begin
	int m_iBaseTerrain;
	int m_iBaseFeature;
	int m_iChanceInclude;
	int m_iChanceMap;
	int m_iWtRiver;
	int m_iWtHills;
	int m_iWtCoastal;
	int m_iWtCoast;
	int m_iWtOcean;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iMinAreaSize;
	int m_iMaxAreaSize;
	int m_iMinAreaProportion;
	int m_iMaxAreaProportion;
	int m_iAreaChannel;
	int m_iHillsAdjacentWeight;
	int m_iCoastAdjacentWeight;
	TerrainTypes m_ePlaceTerrain;
	// merk.msm end

	bool m_bNoCoast;
	bool m_bNoRiver;
	bool m_bNoRiverSide; // advc.129b
	bool m_bNoAdjacent;
	bool m_bRequiresFlatlands;
	bool m_bRequiresRiver;
	bool m_bRequiresRiverSide; // advc.129b
	bool m_bAddsFreshWater;
	bool m_bImpassable;
	bool m_bNoCity;
	bool m_bNoImprovement;
	bool m_bVisibleAlways;
	bool m_bNukeImmune;
	CvString m_szOnUnitChangeTo;
	// merk.msm begin
	bool m_bReqHills;
	bool m_bReqCoastal;
	bool m_bReqCoast;
	bool m_bReqOcean;
	bool m_bPlaceOnce;
	bool m_bPlaceInGroup;
	bool m_bSurroundedByBase;
	// merk.msm end

	int m_iWorldSoundscapeScriptId;

	CvString m_szEffectType;
	int m_iEffectProbability;

	int* m_piYieldChange;
	int* m_piRiverYieldChange;
	int* m_piHillsYieldChange;
	int* m_pi3DAudioScriptFootstepIndex;
	// merk.msm begin
	int* m_piTerrainWeights;
	int* m_piFeatureWeights;
	int* m_piAdjTerrainWeights;
	int* m_piAdjFeatureWeights;
	// merk.msm end

	bool* m_pbTerrain;

private:
	CvString m_szArtDefineTag;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvBonusInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBonusInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All the const functions are exposed to Python
	CvBonusInfo();
	virtual ~CvBonusInfo();

	BonusClassTypes getBonusClassType() const { return m_eBonusClassType; }
	wchar getChar() const; // advc: return wchar (not int)
	void setChar(/* advc: */ wchar wc);
	TechTypes getTechReveal() const { return m_eTechReveal; }
	TechTypes getTechCityTrade() const { return m_eTechCityTrade; }
	TechTypes getTechObsolete() const { return m_eTechObsolete; }
	TechTypes getTechImprove(bool bWater) const; // advc.003w
	int getAITradeModifier() const;
	int getAIObjective() const;
	int getHealth() const { return m_iHealth; }
	int getHappiness() const { return m_iHappiness; }
	int getMinAreaSize() const;
	int getMinLatitude() const;
	int getMaxLatitude() const;
	int getPlacementOrder() const;
	int getConstAppearance() const;
	int getRandAppearance1() const;
	int getRandAppearance2() const;
	int getRandAppearance3() const;
	int getRandAppearance4() const;
	int getPercentPerPlayer() const;
	int getTilesPer() const;
	int getMinLandPercent() const;
	int getUniqueRange() const;
	int getGroupRange() const;
	int getGroupRand() const;

	bool isOneArea() const;
	bool isHills() const;
	bool isFlatlands() const;
	bool isNoRiverSide() const;
	bool isNormalize() const;

	const TCHAR* getArtDefineTag() const;

	int getYieldChange(int i) const;
	int* getYieldChangeArray();
	// advc.003j: Unused in DLL and XML; wasn't even read from XML.
	//int getImprovementChange(int i) const;

	bool isTerrain(int i) const;
	bool isFeature(int i) const;
	bool isFeatureTerrain(int i) const;

	const TCHAR* getButton() const;
	DllExport const CvArtInfoBonus* getArtInfo() const;
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
	bool read(CvXMLLoadUtility* pXML);
	void updateCache(BonusTypes eBonus); // advc.003w

protected:
	BonusClassTypes m_eBonusClassType;
	wchar m_wcSymbol; // advc
	TechTypes m_eTechReveal;
	TechTypes m_eTechCityTrade;
	TechTypes m_eTechObsolete;
	std::pair<TechTypes,TechTypes> m_eeTechImprove; // advc.003w
	int m_iAITradeModifier;
	int m_iAIObjective;
	int m_iHealth;
	int m_iHappiness;
	int m_iMinAreaSize;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iPlacementOrder;
	int m_iConstAppearance;
	int m_iRandAppearance1;
	int m_iRandAppearance2;
	int m_iRandAppearance3;
	int m_iRandAppearance4;
	int m_iPercentPerPlayer;
	int m_iTilesPer;
	int m_iMinLandPercent;
	int m_iUniqueRange;
	int m_iGroupRange;
	int m_iGroupRand;

	bool m_bOneArea;
	bool m_bHills;
	bool m_bFlatlands;
	bool m_bNoRiverSide;
	bool m_bNormalize;

	CvString m_szArtDefineTag;

	int* m_piYieldChange;

	bool* m_pbTerrain;
	bool* m_pbFeature;
	bool* m_pbFeatureTerrain;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvBonusClassInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBonusClassInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public:
	CvBonusClassInfo();

	int getUniqueRange() const; // Exposed to Python
	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iUniqueRange;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvRouteInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRouteInfo : /* <advc.tag> */ public CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addInt(AirBombDefense, "AirBombDefense"); // advc.255
	}
public:
	enum IntElementTypes
	{
		AirBombDefense = base_t::NUM_INT_ELEMENT_TYPES, // advc.255
		NUM_INT_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	}
	// </advc.tag>
public: // All the const functions are exposed to Python except those added by mods
	CvRouteInfo();
	~CvRouteInfo();

	int getAdvancedStartCost() const;
	int getAdvancedStartCostIncrease() const;

	int getValue() const;
	int getMovementCost() const { return m_iMovementCost; }
	int getFlatMovementCost() const { return m_iFlatMovementCost; }
	RouteTypes getRoutePillage() const { return m_eRoutePillage; } // advc.255
	BonusTypes getPrereqBonus() const { return m_ePrereqBonus; }

	int getYieldChange(int i) const;
	int getTechMovementChange(int i) const;
	// <advc.003t>
	int getNumPrereqOrBonuses() const { return m_aePrereqOrBonuses.size(); }
	BonusTypes getPrereqOrBonus(int i) const
	{
		FAssertBounds(0, getNumPrereqOrBonuses(), i);
		return m_aePrereqOrBonuses[i];
	}
	int py_getPrereqOrBonus(int i) const;
	// </advc.003t>
	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML); // advc.255

protected:
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;

	int m_iValue;
	int m_iMovementCost;
	int m_iFlatMovementCost;
	RouteTypes m_eRoutePillage; // advc.255
	BonusTypes m_ePrereqBonus;

	int* m_piYieldChange;
	int* m_piTechMovementChange;
	std::vector<BonusTypes> m_aePrereqOrBonuses; // advc.003t: was int*
};

class CvImprovementBonusInfo;
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvImprovementInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvImprovementInfo : /* <advc.tag> */ public CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addInt(HealthPercent, "HealthPercent"); // advc.901
		kElements.addInt(GWFeatureProtection, "GWFeatureProtection"); // advc.055
	}
public:
	enum IntElementTypes
	{
		HealthPercent = base_t::NUM_INT_ELEMENT_TYPES, // advc.901
		GWFeatureProtection, // advc.055
		NUM_INT_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	}
	// </advc.tag>
	/*  All the const functions are exposed to Python except those dealing with sound,
		Advanced Start and those added by mods */
	CvImprovementInfo();
	~CvImprovementInfo();

	int getAdvancedStartCost() const;
	int getAdvancedStartCostIncrease() const;

	int getTilesPerGoody() const;
	int getGoodyUniqueRange() const;
	int getFeatureGrowthProbability() const;
	int getUpgradeTime() const { return m_iUpgradeTime; }
	int getAirBombDefense() const { return m_iAirBombDefense; }
	int getDefenseModifier() const { return m_iDefenseModifier; }
	int getHappiness() const { return m_iHappiness; }
	int getPillageGold() const;
	ImprovementTypes getImprovementPillage() const { return m_eImprovementPillage; }
	ImprovementTypes getImprovementUpgrade() const { return m_eImprovementUpgrade; }

	// merk.msm begin
	int getBaseTerrain() const { return m_iBaseTerrain; }
	int getBaseFeature() const { return m_iBaseFeature; }
	int getChanceInclude() const { return m_iChanceInclude; }
	int getChanceMap() const { return m_iChanceMap; }
	int getWtRiver() const { return m_iWtRiver; }
	int getWtHills() const { return m_iWtHills; }
	int getWtCoastal() const { return m_iWtCoastal; }
	int getWtCoast() const { return m_iWtCoast; }
	int getWtOcean() const { return m_iWtOcean; }
	int getMinLatitude() const { return m_iMinLatitude; }
	int getMaxLatitude() const { return m_iMaxLatitude; }
	int getMinAreaSize() const { return m_iMinAreaSize; }
	int getMaxAreaSize() const { return m_iMaxAreaSize; }
	int getMinAreaProportion() const { return m_iMinAreaProportion; }
	int getMaxAreaProportion() const { return m_iMaxAreaProportion; }
	int getAreaChannel() const { return m_iAreaChannel; }
	int getHillsAdjWeight() const { return m_iHillsAdjacentWeight; }
	int getCoastAdjWeight() const { return m_iCoastAdjacentWeight; }
	// merk.msm end

	// Super Forts begin *XML*
	int getCulture() const;
	int getCultureRange() const;
	int getVisibilityChange() const;
	int getSeeFrom() const;
	int getUniqueRange() const;
	bool isBombardable() const;
	bool isUpgradeRequiresFortify() const;
	// Super Forts end
	bool isActsAsCity() const { return m_bActsAsCity; }
	bool isHillsMakesValid() const { return m_bHillsMakesValid; }
	bool isFreshWaterMakesValid() const { return m_bFreshWaterMakesValid; }
	bool isRiverSideMakesValid() const { return m_bRiverSideMakesValid; }
	bool isNoFreshWater() const { return m_bNoFreshWater; }
	bool isRequiresFlatlands() const { return m_bRequiresFlatlands; }
	DllExport bool isRequiresRiverSide() const { return m_bRequiresRiverSide; }
	bool isRequiresIrrigation() const { return m_bRequiresIrrigation; }
	bool isCarriesIrrigation() const { return m_bCarriesIrrigation; }
	bool isRequiresFeature() const { return m_bRequiresFeature; }
	bool isWater() const { return m_bWater; }
	DllExport bool isGoody() const { return m_bGoody; }
	bool isPermanent() const { return m_bPermanent; }
	bool isOutsideBorders() const { return m_bOutsideBorders; }
	// merk.msm begin
	bool isReqCoastal() const { return m_bReqCoastal; }
	bool isReqCoast() const { return m_bReqCoast; }
	bool isReqOcean() const { return m_bReqOcean; }
	bool isPlaceOnce() const { return m_bPlaceOnce; }
	bool isPlaceInGroup() const { return m_bPlaceInGroup; }
	bool isSurroundedByBase() const { return m_bSurroundedByBase; }
	// merk.msm end

	const TCHAR* getArtDefineTag() const;

	int getWorldSoundscapeScriptId() const;

	// Array access:

	int getPrereqNatureYield(int i) const;
	int const* getPrereqNatureYieldArray() const { return m_piPrereqNatureYield; }
	int getYieldChange(int i) const;
	int const* getYieldChangeArray() const { return m_piYieldChange; }
	int getRiverSideYieldChange(int i) const;
	int const* getRiverSideYieldChangeArray() const { return m_piRiverSideYieldChange; }
	int getHillsYieldChange(int i) const;
	int const* getHillsYieldChangeArray() const { return m_piHillsYieldChange; }
	int getIrrigatedYieldChange(int i) const;
	int const* getIrrigatedYieldChangeArray() const // For Moose - CvWidgetData XXX
	{
		return m_piIrrigatedChange;
	}

	bool getTerrainMakesValid(int i) const;
	bool isAnyTerrainMakesValid() const { return (m_pbTerrainMakesValid != NULL); } // advc.003t
	bool getFeatureMakesValid(int i) const;
	bool isAnyFeatureMakesValid() const { return (m_pbFeatureMakesValid != NULL); } // advc.003t

	int getTechYieldChanges(int i, int j) const;
	int const* getTechYieldChangesArray(int i) const;

	int getRouteYieldChanges(int i, int j) const;
	int const* getRouteYieldChangesArray(int i) const; // For Moose - CvWidgetData XXX

	int getImprovementBonusYield(int iBonus, int iYield) const;
	bool isImprovementBonusMakesValid(int i) const;
	bool isImprovementBonusTrade(int i) const;
	int getImprovementBonusDiscoverRand(int i) const;

	// merk.msm begin
	int getTerrainWeight(int iTerrain) const;
	int getFeatureWeight(int iFeature) const;
	int getTerrainAdjWeight(int iTerrain) const;
	int getFeatureAdjWeight(int iFeature) const;
	// merk.msm end

	// merk.fac3.1
	std::vector < CvString > factionAdjectives;
	std::vector < CvString > factionNouns;
	// merk.fac3 end

	/*	advc.003w: Moved from CvGameCoreUtils; still exposed to Python through CyGameCoreUtils.
		Renamed from "finalImprovementUpgrade".
		Can't turn it into a non-static function b/c a CvImprovementInfo object
		doesn't know its own ImprovementTypes id. */
	static ImprovementTypes finalUpgrade(ImprovementTypes eImprov);

	const TCHAR* getButton() const;
	DllExport const CvArtInfoImprovement* getArtInfo() const;
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

	

protected:
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;

	int m_iTilesPerGoody;
	int m_iGoodyUniqueRange;
	int m_iFeatureGrowthProbability;
	int m_iUpgradeTime;
	int m_iAirBombDefense;
	int m_iDefenseModifier;
	int m_iHappiness;
	int m_iPillageGold;
	ImprovementTypes m_eImprovementPillage;
	ImprovementTypes m_eImprovementUpgrade;
	// Super Forts begin *XML*
	int m_iCulture;
	int m_iCultureRange;
	int m_iVisibilityChange;
	int m_iSeeFrom;
	int m_iUniqueRange;
	bool m_bBombardable;
	bool m_bUpgradeRequiresFortify;
	// Super Forts end
	int m_iWorldSoundscapeScriptId;
	// merk.msm begin
	int m_iBaseTerrain;
	int m_iBaseFeature;
	int m_iChanceInclude;
	int m_iChanceMap;
	int m_iWtRiver;
	int m_iWtHills;
	int m_iWtCoastal;
	int m_iWtCoast;
	int m_iWtOcean;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iMinAreaSize;
	int m_iMaxAreaSize;
	int m_iMinAreaProportion;
	int m_iMaxAreaProportion;
	int m_iAreaChannel;
	int m_iHillsAdjacentWeight;
	int m_iCoastAdjacentWeight;
	// merk.msm end

	CvString m_szArtDefineTag;

	bool m_bActsAsCity;
	bool m_bHillsMakesValid;
	bool m_bFreshWaterMakesValid;
	bool m_bRiverSideMakesValid;
	bool m_bNoFreshWater;
	bool m_bRequiresFlatlands;
	bool m_bRequiresRiverSide;
	bool m_bRequiresIrrigation;
	bool m_bCarriesIrrigation;
	bool m_bRequiresFeature;
	bool m_bWater;
	bool m_bGoody;
	bool m_bPermanent;
	bool m_bOutsideBorders;
	// merk.msm begin
	bool m_bReqCoastal;
	bool m_bReqCoast;
	bool m_bReqOcean;
	bool m_bPlaceOnce;
	bool m_bPlaceInGroup;
	bool m_bSurroundedByBase;
	// merk.msm end

	int* m_piPrereqNatureYield;
	int* m_piYieldChange;
	int* m_piRiverSideYieldChange;
	int* m_piHillsYieldChange;
	int* m_piIrrigatedChange;
	// merk.msm begin
	int* m_piTerrainWeights;
	int* m_piFeatureWeights;
	int* m_piAdjTerrainWeights;
	int* m_piAdjFeatureWeights;
	// merk.msm end

	bool* m_pbTerrainMakesValid;
	bool* m_pbFeatureMakesValid;

	int** m_ppiTechYieldChanges;
	int** m_ppiRouteYieldChanges;

	CvImprovementBonusInfo* m_paImprovementBonus;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvImprovementBonusInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvImprovementBonusInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
	friend class CvImprovementInfo;
	friend class CvXMLLoadUtility;
public: // The const functions are exposed to Python
	CvImprovementBonusInfo();
	~CvImprovementBonusInfo();

	int getDiscoverRand() const;
	bool isBonusMakesValid() const;
	bool isBonusTrade() const;
	int getYieldChange(int i) const;

	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	#endif
protected:
	int m_iDiscoverRand;
	bool m_bBonusMakesValid;
	bool m_bBonusTrade;
	int* m_piYieldChange;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvGoodyInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGoodyInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // The const functions are exposed to Python
	CvGoodyInfo();

	int getGold() const;
	int getGoldRand1() const;
	int getGoldRand2() const;
	int getMapOffset() const;
	int getMapRange() const;
	int getMapProb() const;
	int getExperience() const;
	int getHealing() const;
	int getDamagePrereq() const;
	int getBarbarianUnitProb() const;
	int getMinBarbarians() const;
	int getUnitClassType() const;
	int getBarbarianUnitClass() const;

	bool isTech() const;
	bool isBad() const;

	const TCHAR* getSound() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iGold;
	int m_iGoldRand1;
	int m_iGoldRand2;
	int m_iMapOffset;
	int m_iMapRange;
	int m_iMapProb;
	int m_iExperience;
	int m_iHealing;
	int m_iDamagePrereq;
	int m_iBarbarianUnitProb;
	int m_iMinBarbarians;
	int m_iUnitClassType;
	int m_iBarbarianUnitClass;

	bool m_bTech;
	bool m_bBad;

	CvString m_szSound;
};

#endif
