#pragma once

#ifndef WAR_EVALUATOR_H
#define WAR_EVALUATOR_H

#include "CvTeamAI.h"
#include "WarEvalParameters.h"
#include "WarUtilityAspect.h"
#include "WarAndPeaceReport.h"

class WarUtilityAspect;

/* <advc.104>: New class. Computes the utility of a war between two teams:
   'agent' against 'target'. From the point of view of 'agent'.  */
class WarEvaluator {

public:

	// The cache should only be used for UI purposes; see comments in the .cpp file
	WarEvaluator(WarEvalParameters& warEvalParams, bool useCache = false);

	/*  Can be called repeatedly for different war plan types (w/o constructing
		a new object in between).
		If wp=NO_WARPLAN, the current war plan is evaluated. Limited if none.
		The default preparation time means that a preparation time matching
		the war plan, the war plan age and other circumstances is chosen.
		(The base values are defined in WarAndPeaceAI.h.)
		By using this evaluate function, the caller lets WarEvaluator decide whether
		naval war is preferrable.
		Stores in the WarEvalParamters object passed to the constructor which
		war plan type and preparation time are assumed and whether it'll be a
		naval war.
		Use 0 for wars that have to be declared immediately (e.g. sponsored).
		Caller may have to indicate switching of target -- not supposed to reset
		time limit. */
	int evaluate(WarPlanTypes wp = NO_WARPLAN, int preparationTime = -1);
	int evaluate(WarPlanTypes wp, bool isNaval, int preparationTime);
	int defaultPreparationTime(WarPlanTypes wp = NO_WARPLAN);

private:

	void reportPreamble();
	// Utility from pov of an individual team member
	void evaluate(PlayerTypes weId, std::vector<WarUtilityAspect*>& aspects);
	/*  Creates the top-level war utility aspects: war gains and war costs;
		the aspect objects create their sub-aspects themselves. */
	void fillWithAspects(std::vector<WarUtilityAspect*>& v);

	WarEvalParameters& params;
	TeamTypes agentId, targetId;
	CvTeamAI& target;
	CvTeamAI& agent;
	std::vector<PlayerTypes>& agentTeam;
	std::vector<PlayerTypes>& targetTeam;
	WarAndPeaceReport& report;
	bool peaceScenario;
	bool useCache;

	bool atTotalWarWithTarget() const;
	void gatherCivsAndTeams();

	static long lastCallParams[];
	static int lastCallResult[];
	static int lastIndex;
	static int cacheSz;
	/*  If (or while) set, all WarEvaluator objects use the cache, not just those
		with useCache=true. */
	public: static bool checkCache;
			static void clearCache();
};

// </advc.104>

#endif
