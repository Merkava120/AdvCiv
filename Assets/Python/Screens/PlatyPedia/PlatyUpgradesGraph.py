import string
from CvPythonExtensions import *
import CvUtil
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()

#The exception list allow you to completely hide a unit from the upgrade graph.
#This is useful for mods that use an unreachable unit to keep others from expiring.
#unitExceptionList = [gc.getInfoTypeForString("UNIT_UNREACHABLE")]
unitExceptionList = []

unitButtonSize = 48
unitHorizontalMargin = 25
unitVerticalMargin = 25
unitHorizontalSpacing = 60
unitVerticalSpacing = 8

################################### BEGIN CLASS DEFINITIONS ###########################################

class Node:
	"This node holds all necessary information for a single unit"
	
	def __init__(self):
		self.x = 999
		self.y = 999
		self.upgradesTo = set()
		self.upgradesFrom = set()
		self.seen = False
		
	def __repr__(self):
		return "Node<x: %i, y: %i, to: %s, from: %s, seen: %s>"%(self.x, self.y, self.upgradesTo, self.upgradesFrom, self.seen)

class MGraph:
	"This Graph is a collection of unit Node's with multiple access methods for fast topological sorting"
	
	def __init__(self):
		self.graph = {}
		self.matrix = []
		self.depth = 0
		self.width = 0
	
	def __repr__(self):
		return "MGraph<depth: %i, width: %i, graph: %s, matrix: %s>"%(self.depth, self.width, self.graph, self.matrix)

class UnitUpgradesGraph:
	def __init__(self, pediaScreen):
		self.mGraphs = []
		self.pediaScreen = pediaScreen
		self.upgradesList = pediaScreen.UPGRADES_GRAPH_ID
		self.exceptionList = unitExceptionList

	def getNumberOfUnits(self):
		if self.pediaScreen.iSortTree == 1:
			return gc.getNumUnitClassInfos()
		elif self.pediaScreen.iSortTree == 2:
			return gc.getNumPromotionInfos()
		elif self.pediaScreen.iSortTree == 3:
			return gc.getNumBuildingClassInfos()
		elif self.pediaScreen.iSortTree == 4:
			return gc.getNumProjectInfos()
		else:
			return gc.getNumImprovementInfos()
		
	def getUnitNumber(self, item):
		if self.pediaScreen.iSortTree == 1:
			result = gc.getUnitClassInfo(item).getDefaultUnitIndex()
			if CyGame().getActivePlayer() > -1:
				result = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(item)
			return result
		elif self.pediaScreen.iSortTree == 2:
			return item
		elif self.pediaScreen.iSortTree == 3:
			result = gc.getBuildingClassInfo(item).getDefaultBuildingIndex()
			if CyGame().getActivePlayer() > -1:
				result = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationBuildings(item)
			return result
		else:
			return item
	
	def getUnitType(self, item):
		if self.pediaScreen.iSortTree == 1:
			return gc.getUnitInfo(item).getType()
		elif self.pediaScreen.iSortTree == 2:
			return gc.getPromotionInfo(item).getType()
		elif self.pediaScreen.iSortTree == 3:
			return gc.getBuildingInfo(item).getType()
		elif self.pediaScreen.iSortTree == 4:
			return gc.getProjectInfo(item).getType()
		else:
			return gc.getImprovementInfo(item).getType()

	def getGraphEdges(self, graph):
		iSortPromotion = self.pediaScreen.iSortPTree
		for item in graph.iterkeys():
			if self.pediaScreen.iSortTree == 1:
				if self.pediaScreen.iSortUTree > -1:
					if gc.getUnitInfo(item).getDomainType() != self.pediaScreen.iSortUTree: continue
				for numB in xrange(gc.getNumUnitClassInfos()):
					unitB = self.getUnitNumber(numB)
					if gc.getUnitInfo(item).getUpgradeUnitClass(numB):
						self.addUpgradePath(graph, item, unitB)
			elif self.pediaScreen.iSortTree == 2:
				if iSortPromotion > -1:
					if not gc.getPromotionInfo(item).getUnitCombat(iSortPromotion): continue
				iPromotion = gc.getPromotionInfo(item).getPrereqPromotion()
				if iPromotion > -1:
					if iSortPromotion == -1 or gc.getPromotionInfo(iPromotion).getUnitCombat(iSortPromotion):
						self.addUpgradePath(graph, iPromotion, item)
				iPromotion = gc.getPromotionInfo(item).getPrereqOrPromotion1()
				if iPromotion > -1:
					if iSortPromotion == -1 or gc.getPromotionInfo(iPromotion).getUnitCombat(iSortPromotion):
						self.addUpgradePath(graph, iPromotion, item)
				iPromotion = gc.getPromotionInfo(item).getPrereqOrPromotion2()
				if iPromotion > -1:
					if iSortPromotion == -1 or gc.getPromotionInfo(iPromotion).getUnitCombat(iSortPromotion):
						self.addUpgradePath(graph, iPromotion, item)
			elif self.pediaScreen.iSortTree == 3:
				Info = gc.getBuildingInfo(item)
				for i in xrange(gc.getNumBuildingClassInfos()):
					if Info.isBuildingClassNeededInCity(i) or Info.getPrereqNumOfBuildingClass(i) > 0:
						iPrereq = self.getUnitNumber(i)
						if iPrereq > -1:
							self.addUpgradePath(graph, iPrereq, item)
			elif self.pediaScreen.iSortTree == 4:
				Info = gc.getProjectInfo(item)
				iPrereq = Info.getAnyoneProjectPrereq()
				if iPrereq > -1:
					self.addUpgradePath(graph, iPrereq, item)
				for i in xrange(gc.getNumProjectInfos()):
					if Info.getProjectsNeeded(i) > 0:
						self.addUpgradePath(graph, i, item)
			else:
				iUpgrade = gc.getImprovementInfo(item).getImprovementUpgrade()
				if iUpgrade > -1:
					self.addUpgradePath(graph, item, iUpgrade)

	def placeOnScreen(self, item, iX, iY):
		screen = self.pediaScreen.getScreen()
		if self.pediaScreen.iSortTree == 1:
			screen.setImageButtonAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, gc.getUnitInfo(item).getButton(), iX, iY, unitButtonSize, unitButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item, 1)
		elif self.pediaScreen.iSortTree == 2:
			screen.setImageButtonAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, gc.getPromotionInfo(item).getButton(), iX, iY, unitButtonSize, unitButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item, 1)
		elif self.pediaScreen.iSortTree == 3:
			screen.setImageButtonAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, gc.getBuildingInfo(item).getButton(), iX, iY, unitButtonSize, unitButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, 1)
		elif self.pediaScreen.iSortTree == 4:
			screen.setImageButtonAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, gc.getProjectInfo(item).getButton(), iX, iY, unitButtonSize, unitButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, item, 1)
		else:
			screen.setImageButtonAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, gc.getImprovementInfo(item).getButton(), iX, iY, unitButtonSize, unitButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item, 1)
			
	################## Stuff to generate Unit Upgrade Graph ##################

	def addUpgradePath(self, graph, unitFrom, unitTo):

		# Check if unit numbers are valid
		if (unitFrom >= 0 and graph.has_key(unitFrom) and unitTo >= 0 and graph.has_key(unitTo)):
			graph[unitFrom].upgradesTo.add(unitTo)
			graph[unitTo].upgradesFrom.add(unitFrom)

	def getMedianY(self, mGraph, unitSet):
		"Returns the average Y position of the units in unitSet"
		
		if (len(unitSet) == 0):
			return -1
		sum = 0.0
		num = 0.0
		for unit in unitSet:
			sum += mGraph.graph[unit].y
			num += 1
		return sum/num
	
	def swap(self, mGraph, x, yA, yB):
		"Swaps two elements in a given row"
	
		unitA = mGraph.matrix[x][yA]
		unitB = mGraph.matrix[x][yB]
		if (unitA != "E"):
			mGraph.graph[unitA].y = yB
		if (unitB != "E"):
			mGraph.graph[unitB].y = yA
		mGraph.matrix[x][yA] = unitB
		mGraph.matrix[x][yB] = unitA
		return

	def getGraph(self):
		"Goes through all the units and adds upgrade paths to the graph.  The MGraph data structure is complete by the end of this function."
		
		self.mGraphs.append(MGraph())
		graph = self.mGraphs[0].graph
		
		for k in xrange(self.getNumberOfUnits()):
			unit = self.getUnitNumber(k)
			if unit == -1: continue
			if self.getUnitType(unit) in self.exceptionList: continue
			graph[unit] = Node()
		
		self.getGraphEdges(graph)
		
		#remove units that don't upgrade to or from anything
		for unit in graph.keys():
			if (len(graph[unit].upgradesTo) == 0 and len(graph[unit].upgradesFrom) == 0):
				del(graph[unit])
## Platy Fix ##
		if len(graph) == 0: return
## Platy Fix ##		
		#split the graph into several disconnected graphs, filling out the rest of the data structure as we go
		mGraphIndex = 0
		while (len(self.mGraphs) > mGraphIndex):
			mGraph = self.mGraphs[mGraphIndex]
			self.mGraphs.append(MGraph())
			newMGraph = self.mGraphs[mGraphIndex + 1]
			
			#Pick a "random" element and mark it as order 0, then make all its successors higher and predecessors lower
			#We can fix that to the range (0..depth) in a moment, and we've already marked everything that's connected
			unit = mGraph.graph.iterkeys().next()
			mGraph.graph[unit].x = 0
			map = {}
			map[0] = set([unit])
## Platy Fix ##
			bDone = False
			while not bDone:
				bDone = True
				for level in xrange(min(map.keys()), max(map.keys())+1):
					for unit in map[level].copy():
						node = mGraph.graph[unit]
						if node.x != level: continue
						for u in node.upgradesTo:
							nodeB = mGraph.graph[u]
							nodeB.x = level + 1
							if (not map.has_key(nodeB.x)):
								map[nodeB.x] = set()
							if not u in map[nodeB.x]:
								map[nodeB.x].add(u)
								bDone = False
				for level in xrange (max(map.keys()), min(map.keys()) - 1, -1):
					for unit in map[level].copy():
						node = mGraph.graph[unit]
						if node.x != level: continue
						for u in node.upgradesFrom:
							nodeB = mGraph.graph[u]
							nodeB.x = level - 1
							if (not map.has_key(nodeB.x)):
								map[nodeB.x] = set()
							if not u in map[nodeB.x]:
								map[nodeB.x].add(u)
								bDone = False
## Platy Fix ##
			highOrder = max(map.keys())
			lowOrder = min(map.keys())
			map = 0
			mGraph.depth = highOrder - lowOrder + 1
						
			#Now we can move anything that isn't marked with an order to the next MGraph
			#if there's nothing to move, we're done after this iteration
			for (unit, node) in mGraph.graph.items():
				if (node.x == 999):
					newMGraph.graph[unit] = node
					del(mGraph.graph[unit])
				else:
					node.x -= lowOrder
					
			if (len(newMGraph.graph) == 0):
				del(self.mGraphs[mGraphIndex + 1])

			mGraphIndex += 1
			
		for mGraph in self.mGraphs:
			#remove links that would otherwise have to jump 
			for (unit, node) in mGraph.graph.iteritems():
				for u in node.upgradesTo.copy():
					if (not mGraph.graph.has_key(u)):
						node.upgradesTo.remove(u)
				for u in node.upgradesFrom.copy():
					if (not mGraph.graph.has_key(u)):
						node.upgradesFrom.remove(u)
			

			nextDummy = -1
			#For any upgrade path that crosses more than one level, insert dummy nodes in between
			for (unitA, nodeA) in mGraph.graph.items():
				for unitB in nodeA.upgradesTo.copy():
					nodeB = mGraph.graph[unitB]
					if (nodeB.x - nodeA.x > 1):
						nodeA.upgradesTo.remove(unitB)
						nodeB.upgradesFrom.remove(unitA)
						n = nodeA.x + 1
						nodeA1 = nodeA # original node A
# Begin Promotions Graph fix for Warlords by Gaurav
						while (n < nodeB.x):
							nodeA.upgradesTo.add(nextDummy)
							mGraph.graph[nextDummy] = Node()
							nodeA = mGraph.graph[nextDummy]
							if n == nodeA1.x + 1:
								nodeA.upgradesFrom.add(unitA)
							else:
								nodeA.upgradesFrom.add(nextDummy + 1)
# End Promotions Graph fix for Warlords by Gaurav
							nodeA.x = n
							n += 1
							nextDummy -= 1
						nodeA.upgradesTo.add(unitB)
						nodeB.upgradesFrom.add(nextDummy + 1)
						

			#Now we can build the matrix from the order data
			#make sure the matrix is <depth> deep
			while(len(mGraph.matrix) < mGraph.depth):
				mGraph.matrix.append([])
			
			#fill out node.y and the matrix
			for (unit, node) in mGraph.graph.iteritems():
				node.y = len(mGraph.matrix[node.x])
				mGraph.matrix[node.x].append(unit)
				if (node.y >= mGraph.width):
					mGraph.width = node.y + 1

			#make all rows of the matrix the same width
			for row in mGraph.matrix:
				row.extend(["E"] * (mGraph.width - len(row)))
			
			#finally, do the Sugiyama algorithm: iteratively step through layer by layer, swapping
			#two units in layer i, if they cause fewer crosses or give a shorter line length from
			#layer i-1, then work back from the other end.  Repeat until no changes are made
			
			doneA = False
			iterlimit = 8
			while (not doneA and iterlimit > 0):
				doneA = True
				iterlimit -= 1
				for dir in [1, -1]:
					start = 1
					end = mGraph.depth
					if (dir == -1):
						start = mGraph.depth - 2
						end = -1
					for x in range(start, end, dir):
						doneB = False
						while (not doneB):
							doneB = True
							for y in range(mGraph.width - 1, 0, -1):
								medA = -1.0
								medB = -1.0
								unitA = mGraph.matrix[x][y-1]
								unitB = mGraph.matrix[x][y]
								nodeA = 0
								nodeB = 0
								setA = 0
								setB = 0
								if (unitA != "E"):
									nodeA = mGraph.graph[unitA]
									setA = nodeA.upgradesFrom
									if (dir == -1):
										setA = nodeA.upgradesTo
									medA = self.getMedianY(mGraph, setA)
								if (unitB != "E"):
									nodeB = mGraph.graph[unitB]
									setB = nodeB.upgradesFrom
									if (dir == -1):
										setB = nodeB.upgradesTo
									medB = self.getMedianY(mGraph, setB)

								if (medA < 0 and medB < 0):
									continue
								if (medA > -1 and medB > -1):
									if (medA > medB):
										self.swap(mGraph, x, y-1, y)
										doneB = False
								if (medA == -1 and medB < y):
									self.swap(mGraph, x, y-1, y)
									doneB = False
								if (medB == -1 and medA >= y):
									self.swap(mGraph, x, y-1, y)
									doneB = False
							if (doneB == False):
								doneA = False
						doneB = False
						while (not doneB):
							doneB = True
							for y in range(1, mGraph.width):
								unitA = mGraph.matrix[x][y-1]
								unitB = mGraph.matrix[x][y]
								if (unitA == "E" or unitB == "E"):
									continue
								nodeA = mGraph.graph[unitA]
								nodeB = mGraph.graph[unitB]
								setA = nodeA.upgradesFrom
								setB = nodeB.upgradesFrom
								if (dir == -1):
									setA = nodeA.upgradesTo
									setB = nodeB.upgradesTo
								crosses = 0
								crossesFlipped = 0
								for a in setA:
									yA = mGraph.graph[a].y
									for b in setB:
										yB = mGraph.graph[b].y
										if (yB < yA):
											crosses += 1
										elif (yB > yA):
											crossesFlipped += 1
								if (crossesFlipped < crosses):
									self.swap(mGraph, x, y-1, y)
									doneB = False
							if (doneB == False):
								doneA = False
						
						#this is a fix for median float->int conversions throwing off the list
						if (mGraph.matrix[x][-1] == "E"):
							sum = 0.0
							num = 0.0
							for y in range(mGraph.width - 1):
								unit = mGraph.matrix[x][y]
								if (unit != "E"):
									node = mGraph.graph[unit]
									seto = node.upgradesFrom
									if (dir == -1):
										seto = node.upgradesTo
									sum += y - self.getMedianY(mGraph, seto)
									num += 1
							if (num > 0 and sum / num < -0.5):
								for y in range(mGraph.width - 1, 0, -1):
									unit = mGraph.matrix[x][y-1]
									mGraph.matrix[x][y] = unit
									if (unit != "E"):
										mGraph.graph[unit].y = y
								mGraph.matrix[x][0] = "E"

		#one final step: sort the graphs with the biggest one at top
		done = False
		while (done == False):
			done = True
			for i in xrange(1, len(self.mGraphs)):
				if (len(self.mGraphs[i-1].graph) < len(self.mGraphs[i].graph)):
					done = False
					temp = self.mGraphs[i]
					self.mGraphs[i] = self.mGraphs[i-1]
					self.mGraphs[i-1] = temp
		return
		
	################## Stuff to lay out the graph in space ###################

	def getPosition(self, x, y, verticalOffset):
		xPos = unitHorizontalMargin + x * (unitButtonSize + unitHorizontalSpacing)
		yPos = unitVerticalMargin + y * (unitButtonSize + unitVerticalSpacing) + verticalOffset
		return (xPos, yPos)
	
	def drawGraph(self):
		offset = 0
		for mGraph in self.mGraphs:
			#draw arrows first so they'll go under the buttons if there is overlap
			self.drawGraphArrows(mGraph, offset)
			for x in range(mGraph.depth):
				for y in range (mGraph.width):
					unit = mGraph.matrix[x][y]
					(xPos, yPos) = self.getPosition(x, y, offset)
					if unit != "E" and unit > -1:
						self.placeOnScreen(unit, xPos, yPos)
			offset = self.getPosition(0, mGraph.width, offset)[1]

	####################### Stuff to draw graph arrows #######################
	
	def drawGraphArrows(self, mGraph, offset):
		matrix = mGraph.matrix
		for x in range(len(matrix) - 1, -1, -1):
			for y in range(len(matrix[x])):
				unit = matrix[x][y]
				if unit != "E":
					self.drawUnitArrows(mGraph, offset, unit)
		return
	
	def drawUnitArrows(self, mGraph, offset, unit):
		toNode = mGraph.graph[unit]
		for fromUnit in toNode.upgradesFrom:
			fromNode = mGraph.graph[fromUnit]
			posFrom = self.getPosition(fromNode.x, fromNode.y, offset)
			posTo = self.getPosition(toNode.x, toNode.y, offset)
			self.drawArrow(posFrom, posTo, fromUnit < 0, unit < 0)
		return
	
	def drawArrow(self, posFrom, posTo, dummyFrom, dummyTo):
		screen = self.pediaScreen.getScreen()
		
		LINE_ARROW = ArtFileMgr.getInterfaceArtInfo("LINE_ARROW").getPath()
		LINE_TLBR = ArtFileMgr.getInterfaceArtInfo("LINE_TLBR").getPath()
		LINE_BLTR = ArtFileMgr.getInterfaceArtInfo("LINE_BLTR").getPath()
		LINE_STRAIT = ArtFileMgr.getInterfaceArtInfo("LINE_STRAIT").getPath()
		
		if (dummyFrom):
			#return
			xFrom = posFrom[0] + unitButtonSize / 2
		else:
			xFrom = posFrom[0] + unitButtonSize
		if (dummyTo):
			#return
			xTo = posTo[0] + unitButtonSize / 2
		else:
			xTo = posTo[0] - 8
		yFrom = posFrom[1] + (unitButtonSize / 2)
		yTo = posTo[1] + (unitButtonSize / 2)
		
		if (yFrom == yTo):
			screen.addDDSGFCAt( self.pediaScreen.getNextWidgetName(), self.upgradesList, LINE_STRAIT, xFrom, yFrom - 3, xTo - xFrom, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
		else:
			xDiff = float(xTo - xFrom)
			yDiff = float(yTo - yFrom)

			iterations = int(max(xDiff, abs(yDiff)) / 80) + 1
			if (abs(xDiff/yDiff) >= 2 or abs(xDiff/yDiff) < 0.5):
				iterations = int(max(xDiff, abs(yDiff)) / 160) + 1

			line = LINE_TLBR
			if (yDiff < 0):
				line = LINE_BLTR
			for i in range(iterations):
				xF = int((xDiff / iterations) * max(i-0.1, 0)) + xFrom
				yF = int((yDiff / iterations) * max(i-0.1, 0)) + yFrom
				xT = int((xDiff / iterations) * (i + 1)) + xFrom
				yT = int((yDiff / iterations) * (i + 1)) + yFrom
				if (yT < yF):
					temp = yT
					yT = yF
					yF = temp
				screen.addDDSGFCAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, line, xF, yF, xT-xF, yT-yF, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
		
		if (dummyTo == False):
			screen.addDDSGFCAt( self.pediaScreen.getNextWidgetName(), self.upgradesList, LINE_ARROW, xTo, yTo - 6, 12, 12, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
		return