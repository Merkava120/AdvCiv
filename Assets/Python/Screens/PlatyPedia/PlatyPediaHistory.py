from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaHistory:
	def __init__(self, main):
		self.iType = -1
		self.iEntry = -1
		self.top = main

	def interfaceScreen(self, iEntryId):
		self.getEntryInfoFromId(iEntryId)
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()
		
		szHeader = self.getDescription(self.iEntry).upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sHelpIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sHelpIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_CONCEPT, -1)
		self.placeText()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_HISTORY and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_HISTORY

	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), "", "", true, true, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.top.W_ITEMS_PANE, self.top.H_ITEMS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.addMultilineText(self.top.getNextWidgetName(), self.getCivilopedia(), self.top.X_ITEMS_PANE + 10, self.top.Y_ITEMS_PANE + 30, self.top.W_ITEMS_PANE - 20, self.top.H_ITEMS_PANE - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)

		listSorted0 = self.top.sortConcepts()
		listSorted1 = self.top.sortNewConcepts()
		self.top.placePediaLinks(listSorted0, CyTranslator().getText(self.top.sHelpIcon, ()), self.iEntry, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, self.iType)
		iRow = screen.appendTableRow("PlatyTable")
		screen.setTableText("PlatyTable", 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		self.top.placePediaLinks(listSorted1, CyTranslator().getText(self.top.sHelpIcon, ()), self.iEntry, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, self.iType)

	def getDescription(self, iEntry):
		if self.iType == CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT:
			return gc.getConceptInfo(iEntry).getDescription()
		return gc.getNewConceptInfo(iEntry).getDescription()
										
	def getCivilopedia(self):
		if self.iType == CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT:
			return gc.getConceptInfo(self.iEntry).getCivilopedia()
		return gc.getNewConceptInfo(self.iEntry).getCivilopedia()
									
	def getEntryInfoFromId(self, iEntryId):
		self.iType = iEntryId % CivilopediaPageTypes.NUM_CIVILOPEDIA_PAGE_TYPES
		self.iEntry = iEntryId / CivilopediaPageTypes.NUM_CIVILOPEDIA_PAGE_TYPES

	def getIdFromEntryInfo(self, iCivilopediaPageType, iEntry):
		return (iEntry * CivilopediaPageTypes.NUM_CIVILOPEDIA_PAGE_TYPES + iCivilopediaPageType)

	def handleInput (self, inputClass):
		return 0