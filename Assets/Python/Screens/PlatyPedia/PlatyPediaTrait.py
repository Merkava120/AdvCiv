from CvPythonExtensions import *
import CvUtil
import ScreenInput
gc = CyGlobalContext()

class CvPediaTrait:
	def __init__(self, main):
		self.iTrait = -1
		self.iLeader = -1
		self.top = main

	def interfaceScreen(self, iTrait):
		self.iTrait = iTrait
		self.top.deleteAllWidgets()			
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_LEADER = (screen.getYResolution() /3 - 55) / 65 * 65 + 55
		self.Y_LEADER = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_LEADER
		
		self.W_EFFECTS = (self.top.W_ITEMS_PANE - self.top.W_BORDER) /2
		self.X_CONCEPT = self.top.X_ITEMS_PANE + self.W_EFFECTS + self.top.W_BORDER
		self.Y_CONCEPT = self.top.Y_ITEMS_PANE - 20
		self.H_CONCEPT = self.Y_LEADER - self.Y_CONCEPT - 10

		szHeader = gc.getTraitInfo(self.iTrait).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sTraitIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sTraitIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_TRAIT, -1)
		self.placeLeaders()
		self.placeSpecial()
		self.placeText()
		self.placeLinks(self.top.iLastScreen == self.top.PLATYPEDIA_TRAIT and screen.isActive())
		self.top.iLastScreen = self.top.PLATYPEDIA_TRAIT

	def placeLeaders(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_LEADER, self.top.W_ITEMS_PANE, self.H_LEADER, PanelStyles.PANEL_STYLE_BLUE50 )
		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.top.X_ITEMS_PANE + 10, self.Y_LEADER + 30, self.top.W_ITEMS_PANE - 20, self.H_LEADER - 30, 1, 64, 64, TableStyles.TABLE_STYLE_STANDARD)
		for iLeader in xrange(gc.getNumLeaderHeadInfos()):
			LeaderInfo = gc.getLeaderHeadInfo(iLeader)
			if LeaderInfo.hasTrait(self.iTrait):
				self.iLeader = iLeader
				screen.appendMultiListButton(rowListName, gc.getLeaderHeadInfo(iLeader).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, 0, false )
				
	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_CONCEPT, self.W_EFFECTS, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )	
		TraitInfo = gc.getTraitInfo(self.iTrait)
		if self.iLeader > -1:
			szText = CyGameTextMgr().parseLeaderTraits(self.iLeader, -1, False, True)
			szSpecialText = ""
			bFirst = True
			bFound = False
			bSkip = True
			for line in szText.splitlines():
				if not line.startswith(" "):
					if line.find(">%s<" % gc.getLeaderHeadInfo(self.iLeader).getDescription()) > -1:
						continue
					elif line.find(">%s<" % TraitInfo.getDescription()) > -1:
						bFound = True
						bSkip = False
					else:
						if bFound: break
						bSkip = True
				else:
					if not bSkip:
						if bFirst:
							bFirst = False
						else:
							szSpecialText += "\n"
						szSpecialText += line[2:]
			if bFound:
				screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_CONCEPT+30, self.W_EFFECTS-10, self.H_CONCEPT-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, false, self.X_CONCEPT, self.Y_CONCEPT, self.W_EFFECTS, self.H_CONCEPT, PanelStyles.PANEL_STYLE_BLUE50 )
		szText = CyTranslator().getText("TXT_KEY_CONCEPT_LEADERS_PEDIA", ())
		sPedia = "TXT_KEY_" + gc.getTraitInfo(self.iTrait).getType() + "_PEDIA"
		sPedia = CyTranslator().getText(sPedia, ())
		if sPedia.find("TXT_KEY_") == -1:
			szText = sPedia
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_CONCEPT+10, self.Y_CONCEPT+30, self.W_EFFECTS -20, self.H_CONCEPT- 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortTraits()
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sTraitIcon, ()), self.iTrait, WidgetTypes.WIDGET_PYTHON, 6789)

	def handleInput (self, inputClass):
		return 0