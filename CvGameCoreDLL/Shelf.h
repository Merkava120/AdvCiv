#pragma once

#ifndef SHELF_H
#define SHELF_H

#include <utility>
#include <vector>

class CvPlot;
class CvUnit;


/* <advc.300> New class representing a continental shelf, akin to a CvArea
   (but I don't want to inherit from that class). Used for spawning
   barbarian sea units. */
class Shelf {

public:

	void add(CvPlot* plot);
	CvPlot* randomPlot(int restrictionFlags, int unitDistance) const;
	int size() const;
	int countUnownedPlots() const;
	int countBarbarians() const;
	CvUnit* randomBarbCargoUnit() const; // advc.306
	bool killBarb(); // Just any one barb ship; false if none


private:

	std::vector<CvPlot*> plots;

public:
	// Just to avoid nested pairs in map types
	class Id : public std::pair<int,int> {
	public: Id(int landId, int waterId); };
};

// </advc.300>

#endif
