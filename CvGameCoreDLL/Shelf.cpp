// advc.300: New class; see Shelf.h for description

#include "CvGameCoreDLL.h"
#include "Shelf.h"
#include "CvGame.h"
#include "CvPlot.h"
#include "CvUnit.h"
#include "CvPlayer.h"


void Shelf::add(CvPlot* pPlot)
{
	m_apPlots.push_back(pPlot);
}


CvPlot* Shelf::randomPlot(RandPlotFlags eRestrictions, int iUnitDistance,
	int* piLegalCount) const
{
	int iLegal_local=0;
	int& iLegal = (piLegalCount == NULL ? iLegal_local : *piLegalCount);
	/*	Based on CvMap::syncRandPlot, but shelves are (normally) so small
		that random sampling isn't efficient. Instead, compute the legal
		plots first, then return one of those at random (NULL if none). */
	std::vector<CvPlot*> apLegal;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CvPlot& p = *m_apPlots[i];
		bool isLegal = (
				!(RANDPLOT_LAND & eRestrictions) &&
				(!(RANDPLOT_UNOWNED & eRestrictions) || !p.isOwned()) &&
				(!(RANDPLOT_ADJACENT_UNOWNED & eRestrictions) || !p.isAdjacentOwned()) &&
				(!(RANDPLOT_NOT_VISIBLE_TO_CIV & eRestrictions) || !p.isVisibleToCivTeam()) &&
				// In case that a mod enables sea cities:
				(!(RANDPLOT_NOT_CITY & eRestrictions) || !p.isCity()) &&
				(!p.isCivUnitNearby(iUnitDistance)) &&
				!p.isUnit());
		/*	RANDPLOT_PASSIBLE, RANDPLOT_ADJACENT_LAND, RANDPLOT_HABITABLE:
			Ensured by CvMap::computeShelves. */
		if (isLegal)
			apLegal.push_back(&p);
	}
	iLegal = (int)apLegal.size();
	if (iLegal == 0)
		return NULL;
	return apLegal[GC.getGame().getSorenRandNum(iLegal, "random shelf plot")];
}


int Shelf::countUnownedPlots() const
{
	int iR = 0;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		if (!m_apPlots[i]->isOwned())
			iR++;
	}
	return iR;
}


int Shelf::countBarbarians() const
{
	int iR = 0;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CvPlot const& p = *m_apPlots[i];
		// Take advantage of Barbarians being unable to coexist with visible units
		CLLNode<IDInfo> const* pUnitNode = p.headUnitNode();
		if (pUnitNode == NULL)
			continue;
		CvUnit const* pAnyUnit = CvUnit::fromIDInfo(pUnitNode->m_data);
		if (pAnyUnit != NULL && pAnyUnit->isBarbarian())
			iR += p.plotCount(PUF_isVisible, BARBARIAN_PLAYER);
	}
	return iR;
}


bool Shelf::killBarbarian()
{
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CLLNode<IDInfo>* pUnitNode = m_apPlots[i]->headUnitNode();
		if (pUnitNode == NULL)
			continue;
		CvUnit* pAnyUnit = CvUnit::fromIDInfo(pUnitNode->m_data);
		if (pAnyUnit != NULL && pAnyUnit->isBarbarian() &&
			pAnyUnit->getUnitCombatType() != NO_UNITCOMBAT)
		{
			pAnyUnit->kill(false);
			return true;
		}
	}
	return false;
}

// advc.306:
CvUnit* Shelf::randomBarbarianTransport() const
{
	std::vector<CvUnit*> apValid;
	for (size_t i = 0; i < m_apPlots.size(); i++)
	{
		CvPlot const& p = *m_apPlots[i];
		if (p.isVisibleToCivTeam())
			continue;
		FOR_EACH_UNIT_VAR_IN(pTransport, p)
		{
			if (pTransport->getOwner() != BARBARIAN_PLAYER)
				break;
			// Load at most 2
			int iCargo = std::min(2, GC.getInfo(pTransport->getUnitType()).getCargoSpace());
			iCargo -= std::max(0, pTransport->getCargo());
			if (iCargo > 0)
				apValid.push_back(pTransport);
		}
	}
	if (apValid.empty())
		return NULL;
	int iValid = apValid.size();
	scaled rNoneProb = fixp(0.2) + scaled(iValid, 10);
	if(!rNoneProb.bernoulliSuccess(GC.getGame().getSRand(), "no Barbarian transport"))
		return NULL;
	return apValid[GC.getGame().getSorenRandNum(iValid, "choose Barbarian transport")];
}
