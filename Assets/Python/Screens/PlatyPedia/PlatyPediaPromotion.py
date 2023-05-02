from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaPromotion:
	def __init__(self, main):
		self.iPromotion = -1
		self.top = main
		self.iSize = 48

	def interfaceScreen(self, iPromotion):	
		self.iPromotion = iPromotion
		self.top.deleteAllWidgets()			
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()

		self.H_ICON = 150
		self.W_MAIN_PANE = screen.getXResolution()/4
		self.H_MAIN_PANE = 210
		self.X_ICON = (self.W_MAIN_PANE - self.H_ICON)/2 + self.top.X_ITEMS_PANE
		self.Y_ICON = (self.H_MAIN_PANE - self.H_ICON)/2 + self.top.Y_ITEMS_PANE

		self.X_PREREQ_PANE = self.top.X_ITEMS_PANE + self.W_MAIN_PANE + self.top.W_BORDER
		self.W_PREREQ_PANE = self.top.W_ITEMS_PANE - self.W_MAIN_PANE - self.top.W_BORDER
		self.Y_PREREQ_PANE = self.top.Y_ITEMS_PANE - self.top.W_BORDER
		self.H_PREREQ_PANE = 110
		self.Y_LEADS_TO_PANE = self.Y_PREREQ_PANE + self.H_PREREQ_PANE + 10				
		self.Y_SPECIAL = self.Y_LEADS_TO_PANE + self.H_PREREQ_PANE + 10
		self.H_SPECIAL = screen.getYResolution() - self.Y_SPECIAL - self.top.Y_ITEMS_PANE

		szHeader = gc.getPromotionInfo(self.iPromotion).getDescription().upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sPromotionIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sPromotionIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_PROMOTION, -1)
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.H_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getPromotionInfo(self.iPromotion).getButton(), self.X_ICON + self.H_ICON/2 - 64/2, self.Y_ICON + self.H_ICON/2 - 64/2, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placePrereqs()
		self.placeLeadsTo()
		self.placeSpecial()
		self.placeUnitGroups()
		self.placeLinks(self.top.iLastScreen == CvScreenEnums.PEDIA_PROMOTION and screen.isActive())
		self.top.iLastScreen = CvScreenEnums.PEDIA_PROMOTION

	def placeLeadsTo(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_LEADS_TO", ()), "", False, True, self.X_PREREQ_PANE, self.Y_LEADS_TO_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		for j in xrange(gc.getNumPromotionInfos()):
			if (gc.getPromotionInfo(j).getPrereqPromotion() == self.iPromotion or gc.getPromotionInfo(j).getPrereqOrPromotion1() == self.iPromotion or gc.getPromotionInfo(j).getPrereqOrPromotion2() == self.iPromotion):
				screen.attachImageButton(panelName, "", gc.getPromotionInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, 1, False)

	def placePrereqs(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		ePromo = gc.getPromotionInfo(self.iPromotion).getPrereqPromotion()
		if (ePromo > -1):
			screen.attachImageButton( panelName, "", gc.getPromotionInfo(ePromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromo, 1, False )

		ePromoOr1 = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion1()
		ePromoOr2 = gc.getPromotionInfo(self.iPromotion).getPrereqOrPromotion2()
		if (ePromoOr1 > -1):
			if (ePromo > -1):
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_AND", ()))
			
				if (ePromoOr2 > -1):
					screen.attachLabel(panelName, "", "(")

			screen.attachImageButton( panelName, "", gc.getPromotionInfo(ePromoOr1).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromoOr1, 1, False )

			if (ePromoOr2 > -1):
				screen.attachLabel(panelName, "", CyTranslator().getText("TXT_KEY_OR", ()))
				screen.attachImageButton( panelName, "", gc.getPromotionInfo(ePromoOr2).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromoOr2, 1, False )

				if (ePromo > -1):
					screen.attachLabel(panelName, "", ")")
								
		eTech = gc.getPromotionInfo(self.iPromotion).getTechPrereq()
		if (eTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, eTech, 1, False )		
						
		eReligion = gc.getPromotionInfo(self.iPromotion).getStateReligionPrereq()
		if (eReligion > -1):
			screen.attachImageButton( panelName, "", gc.getReligionInfo(eReligion).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, eReligion, 1, False )		
						
	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, CyTranslator().getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_PREREQ_PANE, self.Y_SPECIAL, self.W_PREREQ_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		szSpecialText = CyGameTextMgr().getPromotionHelp(self.iPromotion, True)[1:]
		screen.addMultilineText(self.top.getNextWidgetName(), szSpecialText, self.X_PREREQ_PANE+5, self.Y_SPECIAL+30, self.W_PREREQ_PANE-10, self.H_SPECIAL-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

	def placeUnitGroups(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), CyTranslator().getText("TXT_KEY_PEDIA_PROMOTION_UNITS", ()), "", True, True, self.top.X_ITEMS_PANE, self.Y_SPECIAL, self.W_MAIN_PANE, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addScrollPanel(panelName, "", self.top.X_ITEMS_PANE - 2, self.Y_SPECIAL + 20, self.W_MAIN_PANE + 4, self.H_SPECIAL - 46, PanelStyles.PANEL_STYLE_EMPTY)

		iY = 6
		iAdjustment = (self.iSize - 16) /2 - iY
		
		for item in xrange(gc.getNumUnitCombatInfos()):
			if gc.getPromotionInfo(self.iPromotion).getUnitCombat(item):
				screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getUnitCombatInfo(item).getButton(), 0, iY, self.iSize, self.iSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, item, 1)
				screen.setTextAt(self.top.getNextWidgetName(), panelName, u"<font=3>" + gc.getUnitCombatInfo(item).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.iSize, iY + iAdjustment, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iY += (self.iSize + 4)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.show("PlatyTable")
			return
		screen.addTableControlGFC("PlatyTable", 1, self.top.X_PANEL, 55, self.top.W_PANEL, screen.getYResolution() - 110, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect("PlatyTable", True)
		screen.setTableColumnHeader("PlatyTable", 0, "", self.top.W_PANEL)
		listSorted = self.top.sortPromotions(self.top.iSortPromotions)
		self.top.placePediaLinks(listSorted, CyTranslator().getText(self.top.sPromotionIcon, ()), self.iPromotion, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, -1)

	def handleInput (self, inputClass):
		return 0