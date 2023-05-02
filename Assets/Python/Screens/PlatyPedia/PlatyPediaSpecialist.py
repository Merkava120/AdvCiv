from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaSpecialist:
	def __init__(self, main):
		self.iSpecialist = -1
		self.top = main
		self.iSize = 48

	def interfaceScreen(self, iSpecialist):
		self.iSpecialist = iSpecialist
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_ICON = 150
		self.W_MAIN_PANE = (self.top.W_ITEMS_PANE - self.top.W_BORDER)/2
		self.H_MAIN_PANE = 210
		self.X_ICON = self.top.X_ITEMS_PANE + 30
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE
		self.X_LEADICON = self.top.X_ITEMS_PANE + self.W_MAIN_PANE - 30 - 64
		self.H_ARROW = 36
		self.X_ARROW = self.X_ICON + self.H_ICON + (self.X_LEADICON - self.X_ICON - self.H_ICON) / 2 - self.H_ARROW/2
		self.Y_ARROW = self.Y_ICON + self.H_ICON/2 - self.H_ARROW/2

		self.X_EFFECTS = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.Y_EFFECTS = self.top.Y_ITEMS_PANE - 20

		self.Y_SPECIAL = self.top.Y_ITEMS_PANE + self.H_MAIN_PANE + 10
		self.H_SPECIAL = screen.getYResolution() - self.top.Y_ITEMS_PANE - self.Y_SPECIAL
		self.W_YIELD = (self.top.W_ITEMS_PANE - self.top.W_BORDER * 2)/3
		self.X_YIELD = self.top.X_ITEMS_PANE + self.W_YIELD + self.top.W_BORDER
		self.X_HISTORY = self.X_YIELD + self.W_YIELD + self.top.W_BORDER
		self.H_EFFECTS = 110
		self.Y_GENERATE = self.Y_EFFECTS + self.H_EFFECTS + 10

		szHeader = gc.getSpecialistInfo(self.iSpecialist).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sSpecialistIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sSpecialistIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_SPECIALIST, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getSpecialistInfo(self.iSpecialist).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeSpecial()
		self.placeYield()
		self.placeText()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_SPECIALIST and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_SPECIALIST

	def placeSpecial(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false, self.X_EFFECTS, self.Y_EFFECTS, self.W_MAIN_PANE, self.H_MAIN_PANE + 20, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().getSpecialistHelp(self.iSpecialist, True)
## Help Tag ##
		if len(gc.getSpecialistInfo(self.iSpecialist).getHelp()) > 0:
			szSpecialText += CyTranslator().getText("[NEWLINE][ICON_BULLET]", ()) + gc.getSpecialistInfo(self.iSpecialist).getHelp()
## Help Tag ##
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_EFFECTS+5, self.Y_EFFECTS+10, self.W_MAIN_PANE-10, self.H_MAIN_PANE-15, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

	def placeYield(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_PROMOTION_UNITS", ()), "", False, True, self.top.X_ITEMS_PANE, self.Y_SPECIAL, self.W_YIELD, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_YIELDS", ()), "", False, True, self.X_YIELD, self.Y_SPECIAL, self.W_YIELD, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		panelName2 = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.top.X_ITEMS_PANE - 2, self.Y_SPECIAL + 20, self.W_YIELD + 4, self.H_SPECIAL - 46, PanelStyles.PANEL_STYLE_EMPTY)
		screen.addScrollPanel(panelName2, "", self.X_YIELD - 2, self.Y_SPECIAL + 20, self.W_YIELD + 4, self.H_SPECIAL - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY1 = 6
		iY2 = 6	
		
		lClass = []
		for i in xrange(gc.getNumUnitClassInfos()):
			item = gc.getUnitClassInfo(i).getDefaultUnitIndex()
			if CyGame().getActiveCivilizationType() > -1:
				item = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationUnits(i)
			if item == -1: continue
			Info = gc.getUnitInfo(item)
			if i == gc.getSpecialistInfo(self.iSpecialist).getGreatPeopleUnitClass():
				screen.setImageButton(self.top.getNextWidgetName(), Info.getButton(), self.X_LEADICON, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item, 1)
				screen.setButtonGFC(self.top.getNextWidgetName(), "", "", self.X_ARROW, self.Y_ARROW, self.H_ARROW, self.H_ARROW, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT)
			if Info.getGreatPeoples(self.iSpecialist):
				if i in lClass: continue
				lClass.append(i)

		for item in xrange(gc.getNumCivicInfos()):
			Info = gc.getCivicInfo(item)
			if Info.isSpecialistValid(self.iSpecialist):
				sText = CyTranslator().getText("TXT_KEY_PEDIA_UNLIMITED", ())
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, Info.getButton(), 0, iY1, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + Info.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1 + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY1 += (self.iSize + 4)
			sText = ""
			for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
				iCommerceChange = Info.getSpecialistExtraCommerce(j)
				if iCommerceChange != 0:
					sText += u"%+d%c" % (iCommerceChange, gc.getCommerceInfo(j).getChar())
			if len(sText):
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName2, Info.getButton(), 0, iY2, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName2, u"<font=3>" + Info.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName2, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY2 + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY2 += (self.iSize + 4)

		for item in xrange(gc.getNumSpecialistInfos()):
			Info = gc.getSpecialistInfo(item)
			if Info.getGreatPeopleUnitClass() in lClass:
				sText = u"%+d%s" % (Info.getGreatPeopleRateChange(), CyTranslator().getText("[ICON_GREATPEOPLE]", ()))
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, Info.getButton(), 0, iY1, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + Info.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1 + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY1 += (self.iSize + 4)

		for i in xrange(gc.getNumBuildingClassInfos()):
			item = gc.getBuildingClassInfo(i).getDefaultBuildingIndex()
			if CyGame().getActiveCivilizationType() > -1:
				item = gc.getCivilizationInfo(CyGame().getActiveCivilizationType()).getCivilizationBuildings(i)
			if item == -1: continue
			Info = gc.getBuildingInfo(item)
			iSlot = Info.getSpecialistCount(self.iSpecialist)
			if iSlot != 0:
				sText = u"%+d %s" % (iSlot, CyTranslator().getText("TXT_KEY_PEDIA_CAPACITY", ()))
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, Info.getButton(), 0, iY1, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + Info.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1 + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY1 += (self.iSize + 4)
			if Info.getGreatPeopleUnitClass() in lClass:
				sText = u"%+d%s" % (Info.getGreatPeopleRateChange(), CyTranslator().getText("[ICON_GREATPEOPLE]", ()))
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, Info.getButton(), 0, iY1, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + Info.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY1 + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY1 += (self.iSize + 4)
			sText = ""
			for j in xrange(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = Info.getSpecialistYieldChange(self.iSpecialist, j)
				if iYieldChange != 0:
					sText += u"%+d%c" % (iYieldChange, gc.getYieldInfo(j).getChar())
			if len(sText):
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName2, Info.getButton(), 0, iY2, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item, 1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName2, u"<font=3>" + Info.getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt(self.top.getNextWidgetName(), panelName2, u"<font=3>" + sText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY2 + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY2 += (self.iSize + 4)

	## For Mods with modular BuildingInfos files, add more file paths ##
		for item in self.checkFile("Assets/XML/Buildings/CIV4BuildingInfos.xml"):
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName2, gc.getBuildingInfo(item[0]).getButton(), 0, iY2, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[0], 1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName2, u"<font=3>" + gc.getBuildingInfo(item[0]).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt(self.top.getNextWidgetName(), panelName2, u"<font=3>" + item[1] + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize + 4, iY2 + self.iSize/2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iY2 += (self.iSize + 4)
	## For Mods with modular BuildingInfos files, add more file paths ##

	def checkFile(self, sFile):
		lList = []
		MyFile = open(sFile)
		iType = -1
		iCommerceType = -1
		sText = ""
		for sCurrent in MyFile.readlines():
			if "<Type>" in sCurrent:
				iType = gc.getInfoTypeForString(self.cutString(sCurrent))
				iCommerceType = -1
			if iType == -1: continue
			if "<SpecialistExtraCommerces>" in sCurrent:
				iCommerceType = 0
			if iCommerceType == -1: continue
			if "<iCommerce>" in sCurrent:
				iCommerceChange = int(self.cutString(sCurrent))
				if iCommerceChange != 0:
					sText += u"%+d%c" % (iCommerceChange, gc.getCommerceInfo(iCommerceType).getChar())
				iCommerceType += 1
			elif "</SpecialistExtraCommerces>" in sCurrent:
				iCommerceType = -1
				if len(sText):
					lList.append([iType, sText])
				sText = ""
		MyFile.close()
		return lList

	def cutString(self, string):   
		string = string[string.find(">") + 1:]
		string = string[:string.find("<")]
		return string

	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_SPECIAL, self.W_YIELD, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50)
		szText = ""
		sStrategy = gc.getSpecialistInfo(self.iSpecialist).getStrategy()
		if len(sStrategy) and sStrategy.find("TXT_KEY") == -1:
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += sStrategy + "\n\n"
			szText += CyTranslator().getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		sPedia = gc.getSpecialistInfo(self.iSpecialist).getCivilopedia()
		if sPedia.find("TXT_KEY") == -1:
			szText += sPedia	
		screen.addMultilineText(self.top.getNextWidgetName(), szText, self.X_HISTORY + 10, self.Y_SPECIAL + 30, self.W_YIELD - 20, self.H_SPECIAL - 30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortSpecialists(self.top.iSortSpecialists)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sSpecialistIcon, ()), self.iSpecialist, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, -1)

	def handleInput (self, inputClass):
		return 0