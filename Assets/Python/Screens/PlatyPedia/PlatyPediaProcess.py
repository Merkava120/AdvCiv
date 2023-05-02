from CvPythonExtensions import *
import CvUtil
import ScreenInput
gc = CyGlobalContext()

class CvPediaProcess:
	def __init__(self, main):
		self.iProcess = -1
		self.top = main

	def interfaceScreen(self, iProcess):
		self.iProcess = iProcess
		self.top.deleteAllWidgets()									
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_ICON = 150
		self.W_MAIN_PANE = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.H_MAIN_PANE = 210
		self.X_ICON = (self.W_MAIN_PANE - self.H_ICON)/2 + self.top.X_ITEMS_PANE
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE

		self.H_REQUIRES = 110
		self.Y_REQUIRES = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.H_REQUIRES
		self.Y_EFFECTS = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_EFFECTS = self.Y_REQUIRES - self.Y_EFFECTS - 10
		self.X_PROCESS = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_PROCESS = self.top.Y_ITEMS_PANE - 20
		self.H_PROCESS = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_PROCESS

		szHeader = gc.getProcessInfo(self.iProcess).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sProcessIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sProcessIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_PROCESS, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getProcessInfo(iProcess).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeProcessSpecial()
		self.placeLinks(self.top.iLastScreen == self.top.PLATYPEDIA_PROCESS and screen.isActive())
		self.top.iLastScreen = self.top.PLATYPEDIA_PROCESS

	def placeProcessSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.top.X_ITEMS_PANE, self.Y_EFFECTS, self.W_MAIN_PANE, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50 )	
		ProcessInfo = gc.getProcessInfo(self.iProcess)
		szSpecialText = ""
		szText = ""
		for iCommerce in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			iConvert = ProcessInfo.getProductionToCommerceModifier(iCommerce)
			if iConvert > 0:
				szSpecialText += CyTranslator().getText("TXT_KEY_PEDIA_PROCESS_CONVERT",(iConvert,)) + (u"%c\n" % (gc.getCommerceInfo(iCommerce).getChar()))
				if iCommerce == CommerceTypes.COMMERCE_GOLD:
					szText = CyTranslator().getText("TXT_KEY_CONCEPT_WEALTH_PEDIA", ())
				elif iCommerce == CommerceTypes.COMMERCE_RESEARCH:
					szText = CyTranslator().getText("TXT_KEY_CONCEPT_RESEARCH_PEDIA", ())
				elif iCommerce == CommerceTypes.COMMERCE_CULTURE:
					szText = CyTranslator().getText("TXT_KEY_CONCEPT_CULTURE_PEDIA", ())
		
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.top.X_ITEMS_PANE+5, self.Y_EFFECTS+30, self.W_MAIN_PANE-10, self.H_EFFECTS-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()), "", true, false, self.X_PROCESS, self.Y_PROCESS, self.W_MAIN_PANE, self.H_PROCESS, PanelStyles.PANEL_STYLE_BLUE50 )	
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_PROCESS + 10, self.Y_PROCESS + 30, self.W_MAIN_PANE - 20, self.H_PROCESS - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true, self.top.X_ITEMS_PANE, self.Y_REQUIRES, self.W_MAIN_PANE, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		
		iTech = gc.getProcessInfo(self.iProcess).getTechPrereq()
		if (iTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortProcesses(self.top.iSortProcesses)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sProcessIcon, ()), self.iProcess, WidgetTypes.WIDGET_PYTHON, 6787)

	def handleInput (self, inputClass):
		return 0