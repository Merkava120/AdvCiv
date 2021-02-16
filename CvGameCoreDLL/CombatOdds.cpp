#include "CvGameCoreDLL.h"
#include "CombatOdds.h"
#include "CvUnit.h"

// advc: Cut from CvGameCoreUtils.cpp

using std::vector;
using namespace combat_odds; // advc

#ifdef FASSERT_ENABLE
	/*	advc.test: Will verify all results of calculateCombatOdds through a
		Monte Carlo simulation of the resolveCombat procedure. Slow. */
	#define MONTE_CARLO_ODDS_TEST 0
#else
	#define MONTE_CARLO_ODDS_TEST 0
#endif

/*	Returns the number of combinations of k draws out of a population of n
	Written by DeepO
	Modified by Jason Winokur to keep the intermediate factorials small */
__int64 getBinomialCoefficient(int iN, int iK)
{
	__int64 iTemp = 1;
	//take advantage of symmetry in combination, eg. 15C12 = 15C3
	iK = std::min(iK, iN - iK);
	//eg. 15C3 = (15 * 14 * 13) / (1 * 2 * 3) = 15 / 1 * 14 / 2 * 13 / 3 = 455
	for(int i = 1; i <= iK; i++)
		iTemp = (iTemp * (iN - i + 1)) / i;
	FAssert(iTemp <= MAX_INT); // advc: was <
	return iTemp;
}

namespace
{
/*	advc: Cut from getCombatOdds. See wrapper setupCombatants about the return value.
	For bFORCE_INIT=true, there is no meaningful return value.
	(The template param instead of a call param is just for performance.
	Probably shouldn't have concerned myself with that ...) */
template<bool bFORCE_INIT>
int setupCombatantsImpl(CvUnit const& kAttacker, CvUnit const& kDefender,
	Combatant& att, Combatant& def)
{
	// Needs to match CvUnit::getDefenderCombatValues, getCombatFirstStrikes.
	{
		att.setStrength(kAttacker.currCombatStr());
		def.setStrength(kDefender.currCombatStr(kDefender.plot(), &kAttacker));
		FAssert(att.strength() > 0 || def.strength() > 0);
		def.setOdds((GC.getCOMBAT_DIE_SIDES() * def.strength()) /
				(att.strength() + def.strength()));
	}
	att.setOdds(GC.getCOMBAT_DIE_SIDES() - def.odds());
	if (!bFORCE_INIT)
	{
		if (att.odds() == 0)
			return 0;
		if (def.odds() == 0)
			return 1000;
	}
	{
		int iAttFirepower = kAttacker.currFirepower();
		int iDefFirepower = kDefender.currFirepower(kDefender.plot(), &kAttacker);
		FAssert(iAttFirepower > 0 && iDefFirepower > 0);
		int iMeanFirepower = (iAttFirepower + iDefFirepower + 1) / 2;
		// Damage inflicted per hit
		att.setDamagePerRound(std::max(1,
				((GC.getCOMBAT_DAMAGE() * (iAttFirepower + iMeanFirepower)) /
				(iDefFirepower + iMeanFirepower))));
		def.setDamagePerRound(std::max(1,
				((GC.getCOMBAT_DAMAGE() * (iDefFirepower + iMeanFirepower)) /
				(iAttFirepower + iMeanFirepower))));
		// Needed rounds = round_up(health/damage)
		int iDefHitLimit = kDefender.maxHitPoints() - kAttacker.combatLimit();
		/*	advc.001l: Cut from CvGameTextMgr::setACOPlotHelp,
			replaced with code that I think is equivalent (iDefLimit),
			then commented that out too b/c I'm addressing this bug
			through CvUnit::resolveCombat instead. */
		/*int const iNeededRoundsAttacker = 1 + (pDefender->currHitPoints() -
				pDefender->maxHitPoints() + pAttacker->combatLimit() -
				(pAttacker->combatLimit() == pDefender->maxHitPoints() ? 1 : 0)) /
				iDamageToDefender;*/
		/*if (iDefHitLimit > 0)
			iDefHitLimit--;*/
		att.setHitsToWin(intdiv::uceil(std::max(0,
				kDefender.currHitPoints() - iDefHitLimit), att.damagePerRound()));
		def.setHitsToWin(intdiv::uceil(
				kAttacker.currHitPoints(), def.damagePerRound()));
		// <advc>
		if (!bFORCE_INIT)
		{
			// (moved -incl. comments- from LFBgetCombatOdds)
			/*	Essentially, this means we're attacking with a siege engine
				and the defender is already at or below the max combat limit
				We're not allowed to attack regardless, since we can't do any damage -
				just return 100% */
			if (att.hitsToWin() == 0)
				return 1000;
			/*	Because the best defender code calls us from the defender's perspective,
				we also need to check 'defender' rounds zero */
			/*if (def.hitsToWin() == 0)
				return 0;*/
		}
		FAssert(def.hitsToWin() > 0); // Not doing that perspective thing anymore
		// </advc>
	}
	if (!kDefender.immuneToFirstStrikes())
		att.setFirstStrikes(kAttacker.firstStrikes(), kAttacker.chanceFirstStrikes());
	if (!kAttacker.immuneToFirstStrikes())
		def.setFirstStrikes(kDefender.firstStrikes(), kDefender.chanceFirstStrikes());

	return (bFORCE_INIT ? 0 : -1); // No valid combat odds computed yet
}

/*	Returns combat odds of 0 or 1000 permille if those odds are immediately implied
	by the per-round odds; -1 otherwise. Not guaranteed to fully initialize
	the combatants (it's assumed that the caller won't need them when the
	odds are trivial). */
int setupCombatants(CvUnit const& kAttacker, CvUnit const& kDefender,
	Combatant& att, Combatant& def)
{
	return setupCombatantsImpl<false>(kAttacker, kDefender, att, def);
}

float fBinomial(int iN, int iK) // advc: for convenience
{
	return static_cast<float>(getBinomialCoefficient(iN, iK));
}
/*	advc.003g: Fixme -- Lead From Behind uses calculateCombatOdds in (synchronized)
	AI code, therefore, iBinomial should be used instead of fBinomial. Comments say
	that "this needs to be in floating point math", but it's only a matter of
	rounding errors. ScaledNum should handle that well enough at least for the AI.
	(Could continue using float for UI output.) */
int iBinomial(int iN, int iK)
{
	return static_cast<int>(getBinomialCoefficient(iN, iK));
}

// Lead From Behind by UncutDragon (start)
typedef vector<int> LFBoddsAttOdds;
typedef vector<LFBoddsAttOdds> LFBoddsDefRounds;
typedef vector<LFBoddsDefRounds> LFBoddsAttRounds;
typedef vector<LFBoddsAttRounds> LFBoddsFirstStrike;
LFBoddsFirstStrike pOddsCacheFSPos;
LFBoddsFirstStrike pOddsCacheFSNeg;
int const LFB_ODDS_INTERVAL_SIZE = 16;
int const LFB_ODDS_EXTRA_ACCURACY = 32;

/*	Perform the actual odds calculation (basically identical to the default algorithm
	except that we retain a little more accuracy) */
int LFBcalculateCombatOdds(int iFirstStrikes, int iNeededRoundsAttacker,
	int iNeededRoundsDefender, int iAttackerOdds)
{
	int iMaxRounds = iNeededRoundsAttacker + iNeededRoundsDefender - 1;
	int iOdds = 0;
	// <advc.opt>
	float const fAttHitProb = iAttackerOdds / (float)GC.getCOMBAT_DIE_SIDES();
	float const fDefHitProb = 1 - fAttHitProb; // </advc.opt>
	/*	This part is basically the inside of the outer two loops
		at the end of the standard getCombatOdds */
	if (iFirstStrikes > 0)
	{
		int const iAttFS = iFirstStrikes; // advc
		// Attacker gets more or equal first strikes than defender
		/*	For every possible first strike getting hit, calculate both
			the chance of that event happening, as well as the rest of
			the chance assuming the event has happened. Multiply these
			together to get the total chance (Bayes rule).
			iI3 counts the number of successful first strikes */
		for (int iI3 = 0; iI3 < iAttFS + 1; iI3++)
		{
			// event: iI3 first strikes hit the defender
			/*	calculate chance of iI3 first strikes hitting: fOddsEvent
				f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
				this needs to be in floating point math */
			float fOddsEvent = fBinomial(iAttFS, iI3) *
					std::pow(fAttHitProb, iI3) *
					std::pow(fDefHitProb, iAttFS - iI3);
			// calculate chance assuming iI3 first strike hits: fOddsAfterEvent
			float fOddsAfterEvent = 0;
			if (iI3 >= iNeededRoundsAttacker)
				fOddsAfterEvent = 1;
			else
			{
				/*	odds for _at_least_ (iNeededRoundsAttacker - iI3) (the remaining hits
					the attacker needs to make) out of (iMaxRounds - iI3) (the left over
					rounds) is the sum of each _exact_ draw */
				for (int iI4 = iNeededRoundsAttacker - iI3; iI4 < iMaxRounds - iI3 + 1; iI4++)
				{
					/*	odds of exactly iI4 out of (iMaxRounds - iI3) draws.
						f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
						this needs to be in floating point math */
					fOddsAfterEvent += fBinomial((iMaxRounds - iI3), iI4) *
							std::pow(fAttHitProb, iI4) *
							std::pow(fDefHitProb, (iMaxRounds - iI3) - iI4);
				}
			}
			/*	Multiply these together, round them properly, and add
				the result to the total iOdds */
			iOdds += (int)((1000 * fOddsEvent * fOddsAfterEvent *
					LFB_ODDS_EXTRA_ACCURACY) + 0.5f);
		}
	}
	else
	{
		// Attacker gets fewer first strikes than defender
		int const iDefFS = -iFirstStrikes; // advc
		/*	For every possible first strike getting hit, calculate both
			the chance of that event happening, as well as the rest of
			the chance assuming the event has happened. Multiply these
			together to get the total chance (Bayes rule).
			iI3 counts the number of successful first strikes */
		for (int iI3 = 0; iI3 < iDefFS + 1; iI3++)
		{
			// event: iI3 first strikes hit the defender
			/*	First of all, check if the attacker is still alive.
				Otherwise, no further calculations need to occur */
			if (iI3 < iNeededRoundsDefender)
			{
				/*	calculate chance of iI3 first strikes hitting: fOddsEvent
					f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
					this needs to be in floating point math */
				float fOddsEvent = fBinomial(iDefFS, iI3) *
						std::pow(fDefHitProb, iI3) *
						std::pow(fAttHitProb, iDefFS - iI3);
				// calculate chance assuming iI3 first strike hits: fOddsAfterEvent
				float fOddsAfterEvent = 0;
				/*	odds for _at_least_ iNeededRoundsAttacker (the remaining hits
					the attacker needs to make) out of (iMaxRounds - iI3) (the left over
					rounds) is the sum of each _exact_ draw */
				for (int iI4 = iNeededRoundsAttacker; iI4 < iMaxRounds - iI3 + 1; iI4++)
				{
					/*	odds of exactly iI4 out of (iMaxRounds - iI3) draws.
						f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
						this needs to be in floating point math */
					fOddsAfterEvent += fBinomial(iMaxRounds - iI3, iI4) *
							std::pow(fAttHitProb, iI4) *
							std::pow(fDefHitProb, (iMaxRounds - iI3) - iI4);
				}
				/*	Multiply these together, round them properly, and add
					the result to the total iOdds */
				iOdds += (int)((1000 * fOddsEvent * fOddsAfterEvent *
						LFB_ODDS_EXTRA_ACCURACY) + 0.5f);
			}
		}
	}
	return iOdds;
}


int LFBlookupCombatOdds(LFBoddsAttOdds* pOdds, int iOddsIndex, int iFirstStrikes,
	int iNeededRoundsAttacker, int iNeededRoundsDefender, int iAttackerOdds)
{
	// Index==0 => AttackerOdds==0 => no chance to win
	if (iOddsIndex == 0)
		return 0;
	/*	We don't store all possible indices, just what we need/use.
		So use position 0 to keep track of what index we start with */
	int iFirstIndex = iOddsIndex;
	if (pOdds->empty())
		pOdds->push_back(iFirstIndex);
	else iFirstIndex = (*pOdds)[0];
	int iRealIndex = iOddsIndex - iFirstIndex + 1;
	int iNotComputed = -1;
	// Index is before the start of our array
	int iInsert = -iRealIndex + 1;
	if (iInsert > 0)
	{
		pOdds->insert(pOdds->begin() + 1, iInsert, iNotComputed);
		iFirstIndex -= iInsert;
		iRealIndex = 1;
		(*pOdds)[0] = iFirstIndex;
	}
	// Index is past the end of our array
	iInsert = iRealIndex - (int)pOdds->size() + 1;
	if (iInsert > 0)
		pOdds->insert(pOdds->end(), iInsert, iNotComputed);
	// Retrieve the odds from the array
	int iOdds = (*pOdds)[iRealIndex];
	// Odds aren't cached yet - need to actually calculate them
	if (iOdds == iNotComputed)
	{
		iOdds = LFBcalculateCombatOdds(iFirstStrikes, iNeededRoundsAttacker,
				iNeededRoundsDefender, iAttackerOdds);
		(*pOdds)[iRealIndex] = iOdds;
	}

	return iOdds;
}


int LFBlookupCombatOdds(LFBoddsFirstStrike* pOdds, int iFSIndex, int iFirstStrikes,
	int iNeededRoundsAttacker, int iNeededRoundsDefender, int iAttackerOdds)
{
	// Grow the arrays as needed
	// First dimension is the first strikes
	int iInsert = iFSIndex - (int)pOdds->size() + 1;
	if (iInsert > 0)
	{
		LFBoddsAttRounds pAdd;
		pOdds->insert(pOdds->end(), iInsert, pAdd);
	}
	// Second dimension is the attacker rounds (starting at 1)
	LFBoddsAttRounds* pAttRounds = &((*pOdds)[iFSIndex]);
	iInsert = iNeededRoundsAttacker - (int)pAttRounds->size();
	if (iInsert > 0)
	{
		LFBoddsDefRounds pAdd;
		pAttRounds->insert(pAttRounds->end(), iInsert, pAdd);
	}
	// Third dimension is the defender rounds (starting at 1)
	LFBoddsDefRounds* pDefRounds = &((*pAttRounds)[iNeededRoundsAttacker-1]);
	iInsert = iNeededRoundsDefender - (int)pDefRounds->size();
	if (iInsert > 0)
	{
		LFBoddsAttOdds pAdd;
		pDefRounds->insert(pDefRounds->end(), iInsert, pAdd);
	}
	// Fourth (last) dimension is the odds index (odds/16)
	LFBoddsAttOdds* pAttOdds = &((*pDefRounds)[iNeededRoundsDefender-1]);
	// Round down to the nearest interval
	int iMinOddsIndex = iAttackerOdds / LFB_ODDS_INTERVAL_SIZE;
	int iMinOddsValue = iMinOddsIndex * LFB_ODDS_INTERVAL_SIZE;
	// Lookup the odds for the rounded down value
	int iOdds = LFBlookupCombatOdds(pAttOdds, iMinOddsIndex, iFirstStrikes,
			iNeededRoundsAttacker, iNeededRoundsDefender, iMinOddsValue);
	// If we happened to hit an interval exactly, we're done
	if (iMinOddsValue < iAttackerOdds)
	{
		/*	'Round up' to the nearest interval - we don't actually need to compute it,
			we know it's one more than the rounded down interval */
		int iMaxOddsIndex = iMinOddsIndex + 1;
		int iMaxOddsValue = iMinOddsValue + LFB_ODDS_INTERVAL_SIZE;
		// Lookup the odds for the rounded up value
		int iMaxOdds = LFBlookupCombatOdds(pAttOdds, iMaxOddsIndex, iFirstStrikes,
				iNeededRoundsAttacker, iNeededRoundsDefender, iMaxOddsValue);
		// Do a simple weighted average on the two odds
		iOdds += ROUND_DIVIDE( // K-Mod: rounded rather than truncated
				(iAttackerOdds - iMinOddsValue) * (iMaxOdds - iOdds),
				LFB_ODDS_INTERVAL_SIZE);
	}
	return iOdds;
}

// lookup the combat odds in the cache for a specific sub-result
int LFBlookupCombatOdds(int iFirstStrikes, int iNeededRoundsAttacker,
	int iNeededRoundsDefender, int iAttackerOdds)
{
	int iOdds = 0;
	/*	We actually maintain two caches - one for positive first strikes (plus zero)
		and one for negative.
		This just makes the indices (and growing the array as needed) easy */
	if (iFirstStrikes < 0)
	{
		iOdds = LFBlookupCombatOdds(&pOddsCacheFSNeg, (-iFirstStrikes) - 1, iFirstStrikes,
				iNeededRoundsAttacker, iNeededRoundsDefender, iAttackerOdds);
	}
	else
	{
		iOdds = LFBlookupCombatOdds(&pOddsCacheFSPos, iFirstStrikes, iFirstStrikes,
				iNeededRoundsAttacker, iNeededRoundsDefender, iAttackerOdds);
	}
	return iOdds;
}

/*	gets the combat odds using precomputed attacker/defender values
	[advc: Now stored in objects] instead of unit pointers */
int LFBcalculateCombatOdds(Combatant const& att, Combatant const& def)
{
	// (advc: 0-hitsToWin checks moved into setupCombatants)

	int iOdds = 0;
	/*	If attacker has better than even chance to hit, we just flip it
		and calculate defender's chance to win.
		This reduces how much we cache considerably (by half just from the fact
		that we're only dealing with half the odds - but additionally,
		iNeededRounds'Defender' is guaranteed to stay low -
		at most 5 with standard settings). */
	bool const bFlip = (att.odds() > def.odds());
	/*	This is basically the two outside loops at the end of BtS's getCombatOdds
		We just call our cache lookup in the middle (flipped if necessary)
		instead of the actual computation */
	for (int i = att.lowFS(); i < att.highFS() + 1; i++)
	{
		for (int j = def.lowFS(); j < def.highFS() + 1; j++)
		{
			int iFirstStrikes = i - j;
			if (bFlip)
			{
				iOdds += LFBlookupCombatOdds(-iFirstStrikes, def.hitsToWin(),
						att.hitsToWin(), def.odds());
			}
			else
			{
				iOdds += LFBlookupCombatOdds(iFirstStrikes, att.hitsToWin(),
						def.hitsToWin(), att.odds());
			}
		}
	}
	/*	Odds are a straight average of all the FS combinations
		(since all are equally possible) */
	iOdds /= (att.FSChances() + 1) * (def.FSChances() + 1);
	// Now that we have the final odds, we can remove the extra accuracy
	iOdds = ROUND_DIVIDE(iOdds, LFB_ODDS_EXTRA_ACCURACY);
	// If we flipped the perspective in the computation/lookup, need to flip it back now.
	if (bFlip)
		iOdds = 1000 - iOdds;
	return iOdds;
}
// Lead From Behind by UncutDragon (end)

/*	advc: Cut from getCombatOdds (probably to be deleted -
	I don't think the LFB changes need to be optional) */
int calculateCombatOddsLegacy(Combatant const& att, Combatant const& def)
{
	int iOdds = 0;
	int const iMaxRounds = att.hitsToWin() + def.hitsToWin() - 1;
	/*	For every possible first strike event, calculate the odds of combat.
		Then, add these to the total, weighted by the chance of that first
		strike event occurring */
	// advc.opt>
	float const fAttHitProb = att.odds() / (float)GC.getCOMBAT_DIE_SIDES();
	float const fDefHitProb = 1 - fAttHitProb; // </advc.opt>
	for (int iI1 = att.lowFS(); iI1 < att.highFS() + 1; iI1++)
	{
		for (int iI2 = def.lowFS(); iI2 < def.highFS() + 1; iI2++)
		{
			// for every possible combination of fs results, calculate the chance
			if (iI1 >= iI2)
			{
				// Attacker gets more or equal first strikes than defender
				int const iAttFS = iI1 - iI2;
				/*	For every possible first strike getting hit, calculate both
					the chance of that event happening, as well as the rest of
					the chance assuming the event has happened. Multiply these
					together to get the total chance (Bayes rule).
					iI3 counts the number of successful first strikes */
				for (int iI3 = 0; iI3 < iAttFS + 1; iI3++)
				{
					// event: iI3 first strikes hit the defender
					/*	calculate chance of iI3 first strikes hitting: fOddsEvent
						f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
						this needs to be in floating point math */
					float fOddsEvent = fBinomial(iAttFS, iI3) *
							std::pow(fAttHitProb, iI3) *
							std::pow(fDefHitProb, iAttFS - iI3);
					// calculate chance assuming iI3 first strike hits: fOddsAfterEvent
					float fOddsAfterEvent = 0;
					if (iI3 >= att.hitsToWin())
						fOddsAfterEvent = 1;
					else
					{
						/*	odds for _at_least_ (iNeededRoundsAttacker - iI3)
							(the remaining hits the attacker needs to make) out of
							(iMaxRounds - iI3) (the left over rounds) is the sum of
							each _exact_ draw */
						for (int iI4 = att.hitsToWin() - iI3;
							iI4 < iMaxRounds - iI3 + 1; iI4++)
						{
							/*	odds of exactly iI4 out of (iMaxRounds - iI3) draws.
								f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
								this needs to be in floating point math */
							fOddsAfterEvent +=
									fBinomial((iMaxRounds - iI3), iI4) *
									std::pow(fAttHitProb, iI4) *
									std::pow(fDefHitProb, (iMaxRounds - iI3) - iI4);
						}
					}
					/*	Multiply these together, round them properly, and add
						the result to the total iOdds */
					iOdds += (int)(1000 * fOddsEvent * fOddsAfterEvent + 0.5f);
				}
			}
			else // (iI1 < iI2)
			{
				// Attacker gets fewer first strikes than defender
				int const iDefFS = iI2 - iI1;

				/*	For every possible first strike getting hit, calculate both
					the chance of that event happening, as well as the rest of
					the chance assuming the event has happened. Multiply these
					together to get the total chance (Bayes rule).
					iI3 counts the number of successful first strikes */
				for (int iI3 = 0; iI3 < iDefFS + 1; iI3++)
				{
					// event: iI3 first strikes hit the defender
					/*	First of all, check if the attacker is still alive.
						Otherwise, no further calculations need to occur */
					if (iI3 < def.hitsToWin())
					{
						/*	calculate chance of iI3 first strikes hitting: fOddsEvent
							f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
							this needs to be in floating point math */
						float fOddsEvent = fBinomial(iDefFS, iI3) *
								std::pow(fDefHitProb, iI3) *
								std::pow(fAttHitProb, iDefFS - iI3);
						// calculate chance assuming iI3 first strike hits: fOddsAfterEvent
						float fOddsAfterEvent = 0;
						/*	odds for _at_least_ att.hitsToWin()
							(the remaining hits the attacker needs to make) out of
							(iMaxRounds - iI3) (the left over rounds)
							is the sum of each _exact_ draw */
						for (int iI4 = att.hitsToWin(); iI4 < iMaxRounds - iI3 + 1; iI4++)
						{
							/*	odds of exactly iI4 out of (iMaxRounds - iI3) draws.
								f(k;n,p)=C(n,k)*(p^k)*((1-p)^(n-k))
								this needs to be in floating point math */
							fOddsAfterEvent +=
									fBinomial(iMaxRounds - iI3, iI4) *
									std::pow(fAttHitProb, iI4) *
									std::pow(fDefHitProb, iMaxRounds - iI3 - iI4);
						}

						/*	Multiply these together, round them properly
							and add the result to the total iOdds */
						iOdds += (int)(1000 * fOddsEvent * fOddsAfterEvent + 0.5f);
					}
				}
			}
		}
	}
	// Weigh the total to the number of possible combinations of first strikes events
	return ROUND_DIVIDE(iOdds, (att.FSChances() + 1) * (def.FSChances() + 1));
}

// advc.test:
#if MONTE_CARLO_ODDS_TEST
/*	Based on CvUnit::resolveCombat, setCombatFirstStrikes
	(ignoring withdrawal chance; not ignoring damage limit).
	Returns true if the attacker wins. Reaching its damage limit counts as a win. */
bool simulateCombat(CvUnit const& kAttacker, CvUnit const& kDefender)
{
	// Odds of defender destroying attacker, per-round damage to(!) attacker, to defender.
	int iDefenderOdds=0, iAttackerDamage=0, iDefenderDamage=0;
	{
		int iDefenderStrength=0;
		kAttacker.getDefenderCombatValues(kDefender, kDefender.plot(),
				kAttacker.currCombatStr(), 
				kAttacker.currFirepower(),
				iDefenderOdds, iDefenderStrength,
				iAttackerDamage, iDefenderDamage);
	}
	int iAttackerTotalDamage = kAttacker.getDamage();
	int iDefenderTotalDamage = kDefender.getDamage();
	int iAttackerTotalCombatFS = (kDefender.immuneToFirstStrikes() ? 0 :
			(kAttacker.firstStrikes() + GC.getASyncRand().get(
			kAttacker.chanceFirstStrikes() + 1, "First Strike Sim Att")));
	int iDefenderTotalCombatFS = (kAttacker.immuneToFirstStrikes() ? 0 :
			(kDefender.firstStrikes() + GC.getASyncRand().get(
			kDefender.chanceFirstStrikes() + 1, "First Strike Sim Def")));
	while (iAttackerTotalDamage < kAttacker.maxHitPoints() &&
		iDefenderTotalDamage < kDefender.maxHitPoints())
	{
		if (GC.getASyncRand().get(
			GC.getCOMBAT_DIE_SIDES(), "Combat Roll Sim") < iDefenderOdds)
		{
			if (iAttackerTotalCombatFS == 0)
				iAttackerTotalDamage += iAttackerDamage;
		}
		else
		{
			if (iDefenderTotalCombatFS == 0)
			{
				if (std::min(GC.getMAX_HIT_POINTS() - 1, // (advc.001l: see resolveCombat)
					iDefenderTotalDamage + iDefenderDamage) >= kAttacker.combatLimit())
				{
					iDefenderTotalDamage = kAttacker.combatLimit();
					break;
				}
				iDefenderTotalDamage += iDefenderDamage;
			}
		}
		if (iAttackerTotalCombatFS > 0)
			iAttackerTotalCombatFS--;
		if (iDefenderTotalCombatFS > 0)
			iDefenderTotalCombatFS--;
	}
	return (iAttackerTotalDamage < kAttacker.maxHitPoints());
}

// Estimates the attacker's victory (cf. simulateCombat) odds at permille precision
int estimateCombatOdds(CvUnit const& kAttacker, CvUnit const& kDefender, int iSamples)
{
	FAssert(iSamples > 0);
	int iWins = 0;
	for (int i = 0; i < iSamples; i++)
	{
		if (simulateCombat(kAttacker, kDefender))
			iWins++;
	}
	return ROUND_DIVIDE(iWins * 1000, iSamples);
}
#endif // MONTE_CARLO_ODDS_TEST
} // (end of unnamed namespace)

// Unlike setupCombatants, this is guaranteed to initialize the combatants.
void combat_odds::initCombatants(CvUnit const& kAttacker, CvUnit const& kDefender,
	Combatant& att, Combatant& def)
{
	setupCombatantsImpl<true>(kAttacker, kDefender, att, def);
}

/*	advc: Replacement I wrote for CvUnit::LFBgetDefenderCombatOdds, which used to be
	called from CvUnit::LFBgetDefenderOdds. Computes the victory odds of the defender.
	But it turns out that we can just use 1000 minus calculateCombatOdds insetad.
	The results can differ by 1 point, but I'm not sure which is more correct, and
	defender odds aren't even shown by the UI. */
/*int LFBcalculateDefenderCombatOdds(CvUnit const& kDefender, CvUnit const& kAttacker) {
	Combatant att, def;
	int iOdds = setupCombatants(kAttacker, kDefender, att, def);
	// Here's where we invert stuff
	if (iOdds >= 0)
		iOdds = 1000 - iOdds;
	else iOdds = LFBcalculateCombatOdds(def, att);
	#ifdef FASSERT_ENABLE
		int iAltOdds = 1000 - calculateCombatOdds(kAttacker, kDefender);
		FAssert(abs(iOdds - iAltOdds) <=
				(iOdds == 0 || iAltOdds == 0 || iOdds == 1000 || iAltOdds==1000 ? 0 : 1));
	#endif
	return iOdds;
}*/

/*	Calculates combat odds, given two units
	Returns value from 0-1000
	Written by DeepO (advc: gutted) */
int calculateCombatOdds(CvUnit const& kAttacker, CvUnit const& kDefender)
{
	PROFILE_FUNC(); // advc: OK - not called all that frequently.
	// setup battle, calculate strengths and odds
	Combatant att, def;
	// Odds for trivial cases get computed during setup
	int iOdds = setupCombatants(kAttacker, kDefender, att, def);
	if (iOdds < 0)
	{
		// UncutDragon
		if (GC.getDefineBOOL(CvGlobals::LFB_ENABLE))
			iOdds = LFBcalculateCombatOdds(att, def);
		// /UncutDragon
		// advc: Move this into a subroutine too
		else iOdds = calculateCombatOddsLegacy(att, def);
	}
	#if MONTE_CARLO_ODDS_TEST // advc.test
	int iEstimate=0; // To allow inspection in debugger
	FAssert(abs(iOdds - (iEstimate = estimateCombatOdds(kAttacker, kDefender, 500000))) <= 2 ||
			// On fail, run calculation again, just so that we can immediately step into it.
			(setupCombatants(kAttacker, kDefender, att, def) < 0 &&
			(GC.getDefineBOOL(CvGlobals::LFB_ENABLE) ?
			LFBcalculateCombatOdds(att, def) :
			calculateCombatOddsLegacy(att, def)) < 0)); // Not going to be true
	// While we're at it: also verify that the BtS and LFB calculations are consistent
	int iOtherMethod=0;
	FAssert(abs(iOdds - (iOtherMethod = (GC.getDefineBOOL(CvGlobals::LFB_ENABLE) ?
			calculateCombatOddsLegacy(att, def) :
			LFBcalculateCombatOdds(att, def)))) <= 2);
	#endif
	return iOdds;
}
