from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import string
import CvScreensInterface
import PlatyOptions
gc = CyGlobalContext()

class CvCivicsScreen:
	def __init__(self):
		self.CANCEL_NAME = "CivicsCancel"
		self.EXIT_NAME = "CivicsExit"
		self.TITLE_NAME = "CivicsTitleHeader"
		self.DEBUG_DROPDOWN_ID =  "CivicsDropdownWidget"
		self.Y_TITLE = 8

		self.TEXT_MARGIN = 15
		self.BIG_BUTTON_SIZE = 64

		self.iActivePlayer = -1
		self.iSelectedCivic = -1
		self.m_paeDisplayCivics = []

	def setActivePlayer(self, iPlayer):
		self.iActivePlayer = iPlayer
		self.m_paeDisplayCivics = []
		for i in xrange (gc.getNumCivicOptionInfos()):
			self.m_paeDisplayCivics.append(gc.getPlayer(self.iActivePlayer).getCivics(i))

	def interfaceScreen (self):
		screen = CyGInterfaceScreen("CivicsScreen", CvScreenEnums.CIVICS_SCREEN)
		if screen.isActive(): return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.BOTTOM_LINE_HEIGHT = 60
		self.BOTTOM_LINE_TOP = screen.getYResolution() - self.BOTTOM_LINE_HEIGHT - 55 - 10
		self.CivicTable_X = 20
		self.BOTTOM_LINE_WIDTH = screen.getXResolution() - self.CivicTable_X * 2
		self.CivicTable_WIDTH = screen.getXResolution()/5
		self.CivicTable_Y = 70
		self.CivicTable_HEIGHT = (self.BOTTOM_LINE_TOP - self.CivicTable_Y - 20)
		self.ChangesTable_X = self.CivicTable_X + self.CivicTable_WIDTH + 10
		self.OriginalCivic_X = self.ChangesTable_X + self.CivicTable_WIDTH + 20
		self.Comparison_WIDTH = (screen.getXResolution() - self.OriginalCivic_X - 30) / 2
## Unique Background ##
		screen.addDDSGFC("ScreenBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
		screen.addPanel( "CivicTopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "CivicBottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground(False)
		screen.setText(self.CANCEL_NAME, "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 35, -6.3, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)
		screen.setText("CivicsTitleHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.Y_TITLE, -6.3, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		self.setActivePlayer(CyGame().getActivePlayer())						

		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )
		self.drawComparison()
		self.drawCivics()
		self.drawChanges()
		self.updateAnarchy()

	def drawCivics(self):
		screen = CyGInterfaceScreen("CivicsScreen", CvScreenEnums.CIVICS_SCREEN)
		screen.setLabel("CivicsTableLabel", "Background",  u"<font=3b>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.CivicTable_X + self.CivicTable_WIDTH/2, self.CivicTable_Y + 10, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		iNumColumns = gc.getNumCivicOptionInfos()
		lCivicOptions = []
		screen.addTableControlGFC("CivicsTable", 1, self.CivicTable_X + 10, self.CivicTable_Y + 30, self.CivicTable_WIDTH, self.CivicTable_HEIGHT - 20, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
		screen.setTableColumnHeader("CivicsTable", 0, "", self.CivicTable_WIDTH)
		iMaxRow = (gc.getNumCivicOptionInfos() * 2 - 1) + gc.getNumCivicInfos()
		for i in xrange(iMaxRow):
			screen.appendTableRow("CivicsTable")

		iRow = 0
		pPlayer = gc.getPlayer(self.iActivePlayer)
		for i in xrange(gc.getNumCivicOptionInfos()):
			sColor = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ())
			screen.setTableText("CivicsTable", 0, iRow, sColor + "<font=3>" + gc.getCivicOptionInfo(i).getDescription() + "</font></color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iRow += 1
		
			for j in xrange(gc.getNumCivicInfos()):
				if gc.getCivicInfo(j).getCivicOptionType() != i: continue
				sColor = ""
				if not pPlayer.canDoCivics(j):
					sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if j in self.m_paeDisplayCivics:
					sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
				if pPlayer.isCivic(j):
					sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				screen.setTableText("CivicsTable", 0, iRow, sColor + "<font=3>" + gc.getCivicInfo(j).getDescription() + "</font></color>", gc.getCivicInfo(j).getButton(), WidgetTypes.WIDGET_PYTHON, 8205, j, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
			if i < gc.getNumCivicOptionInfos() - 1:
				iRow += 1

	def drawChanges(self):
		screen = CyGInterfaceScreen("CivicsScreen", CvScreenEnums.CIVICS_SCREEN)
		screen.setLabel("ChangesTableLabel", "Background",  u"<font=3b>" + CyTranslator().getText("TXT_KEY_ACTION_SHOW_CIVICS_SCREEN", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.ChangesTable_X + self.CivicTable_WIDTH/2, self.CivicTable_Y + 10, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addTableControlGFC("ChangesTable", 1, self.ChangesTable_X, self.CivicTable_Y + 30, self.CivicTable_WIDTH, self.CivicTable_HEIGHT - 20, False, False, 24, 24, TableStyles.TABLE_STYLE_EMPTY)
		screen.setTableColumnHeader("ChangesTable", 0, "", self.CivicTable_WIDTH)

		bFirst = True
		pPlayer = gc.getPlayer(self.iActivePlayer)
		for i in xrange(gc.getNumCivicOptionInfos()):
			iCivic = self.m_paeDisplayCivics[i]
			if pPlayer.isCivic(iCivic): continue
			if bFirst:
				bFirst = False
			else:
				iRow = screen.appendTableRow("ChangesTable")
			iCivicOption = gc.getCivicInfo(iCivic).getCivicOptionType()
			iRow = screen.appendTableRow("ChangesTable")
			sColor = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ())
			screen.setTableText("ChangesTable", 0, iRow, sColor + "<font=3>" + gc.getCivicOptionInfo(iCivicOption).getDescription() + "</font></color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			iRow = screen.appendTableRow("ChangesTable")
			iOriginalCivic = pPlayer.getCivics(iCivicOption)
			sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
			screen.setTableText("ChangesTable", 0, iRow, sColor + "<font=3>" + gc.getCivicInfo(iOriginalCivic).getDescription() + "</font></color>", gc.getCivicInfo(iOriginalCivic).getButton(), WidgetTypes.WIDGET_PYTHON, 8206, iOriginalCivic, CvUtil.FONT_LEFT_JUSTIFY)
			
			iRow = screen.appendTableRow("ChangesTable")
			sColor = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
			screen.setTableText("ChangesTable", 0, iRow, sColor + "<font=3>" + gc.getCivicInfo(iCivic).getDescription() + "</font></color>", gc.getCivicInfo(iCivic).getButton(), WidgetTypes.WIDGET_PYTHON, 8206, iCivic, CvUtil.FONT_LEFT_JUSTIFY)
			
	def drawComparison(self):
		screen = CyGInterfaceScreen("CivicsScreen", CvScreenEnums.CIVICS_SCREEN)
		pPlayer = gc.getPlayer(self.iActivePlayer)
		self.NewCivic_X = self.OriginalCivic_X + self.Comparison_WIDTH + 10
## Transparent Panels ##
		PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			PanelStyle = PanelStyles.PANEL_STYLE_IN
		screen.addPanel("CivicsBottomLine", "", "", True, True, self.CivicTable_X, self.BOTTOM_LINE_TOP, self.BOTTOM_LINE_WIDTH, self.BOTTOM_LINE_HEIGHT, PanelStyle)
		screen.addPanel("CivicPanel", "", "", True, True, self.CivicTable_X, self.CivicTable_Y, self.CivicTable_WIDTH * 2 + 20, self.CivicTable_HEIGHT + 20, PanelStyle)
		screen.addPanel("ComparisonPanel1", "", "", True, True, self.OriginalCivic_X, self.CivicTable_Y, self.Comparison_WIDTH, self.CivicTable_HEIGHT + 20, PanelStyle)
		screen.addPanel("ComparisonPanel2", "", "", True, True, self.NewCivic_X, self.CivicTable_Y, self.Comparison_WIDTH, self.CivicTable_HEIGHT + 20, PanelStyle)
## Transparent Panels ##
	
		iCivicOption = 0
		if self.iSelectedCivic > -1:
			iCivicOption = gc.getCivicInfo(self.iSelectedCivic).getCivicOptionType()
		iCivic = pPlayer.getCivics(iCivicOption)

		if ((gc.getCivicInfo(iCivic).getUpkeep() != -1) and not pPlayer.isNoCivicUpkeep(iCivicOption)):
			szHelpText = gc.getUpkeepInfo(gc.getCivicInfo(iCivic).getUpkeep()).getDescription()
		else:
			szHelpText = CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
		szHelpText += CyGameTextMgr().parseCivicInfo(iCivic, False, True, True)

		screen.setLabel("OriginalCivicName", "Background",  u"<font=3>" + gc.getCivicInfo(iCivic).getDescription().upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.OriginalCivic_X + self.Comparison_WIDTH/2, self.CivicTable_Y + self.BIG_BUTTON_SIZE + 20, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setImageButton("OriginalCivicButton", gc.getCivicInfo(iCivic).getButton(), self.OriginalCivic_X + self.Comparison_WIDTH/2 - self.BIG_BUTTON_SIZE/2, self.CivicTable_Y + 20, self.BIG_BUTTON_SIZE, self.BIG_BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1)
		screen.addMultilineText("OriginalCivicEffects", szHelpText, self.OriginalCivic_X+5, self.CivicTable_Y + self.BIG_BUTTON_SIZE + 40, self.Comparison_WIDTH-7, self.CivicTable_HEIGHT - self.BIG_BUTTON_SIZE - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		if self.iSelectedCivic > -1:
			iCivic = self.iSelectedCivic
		if ((gc.getCivicInfo(iCivic).getUpkeep() != -1) and not pPlayer.isNoCivicUpkeep(iCivicOption)):
			szHelpText = gc.getUpkeepInfo(gc.getCivicInfo(iCivic).getUpkeep()).getDescription()
		else:
			szHelpText = CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
		szHelpText += CyGameTextMgr().parseCivicInfo(iCivic, False, True, True)

		screen.setLabel("NewCivicName", "Background",  u"<font=3>" + gc.getCivicInfo(iCivic).getDescription().upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.NewCivic_X + self.Comparison_WIDTH/2, self.CivicTable_Y + self.BIG_BUTTON_SIZE + 20, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setImageButton("NewCivicButton", gc.getCivicInfo(iCivic).getButton(), self.NewCivic_X + self.Comparison_WIDTH/2 - self.BIG_BUTTON_SIZE/2, self.CivicTable_Y + 20, self.BIG_BUTTON_SIZE, self.BIG_BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1)
		screen.addMultilineText("NewCivicEffects", szHelpText, self.NewCivic_X+5, self.CivicTable_Y + self.BIG_BUTTON_SIZE + 40, self.Comparison_WIDTH-7, self.CivicTable_HEIGHT - self.BIG_BUTTON_SIZE - 20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def updateAnarchy(self):
		screen = CyGInterfaceScreen("CivicsScreen", CvScreenEnums.CIVICS_SCREEN)
		pPlayer = gc.getPlayer(self.iActivePlayer)

		bChange = False
		for i in xrange(gc.getNumCivicOptionInfos()):
			iCivic = self.m_paeDisplayCivics[i]
			if pPlayer.isCivic(iCivic): continue
			bChange = True	
		
		# Make the revolution button
		screen.deleteWidget(self.EXIT_NAME)
		if pPlayer.canRevolution(0) and bChange:			
			screen.setText(self.EXIT_NAME, "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_CONCEPT_REVOLUTION", ( )).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -2.3, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_REVOLUTION, 1, 0)
			screen.show(self.CANCEL_NAME)
		else:
			screen.setText(self.EXIT_NAME, "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ( )).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, -2.3, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, -1)
			screen.hide(self.CANCEL_NAME)

		# Anarchy		
		szText = CyGameTextMgr().setRevolutionHelp(self.iActivePlayer)
		if pPlayer.canRevolution(0):
			szText = CyTranslator().getText("TXT_KEY_ANARCHY_TURNS", (pPlayer.getCivicAnarchyLength(self.m_paeDisplayCivics), ))
		screen.setLabel("CivicsRevText", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.BOTTOM_LINE_TOP + self.TEXT_MARGIN/2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Maintenance		
		szText = CyTranslator().getText("TXT_KEY_CIVIC_SCREEN_UPKEEP", (pPlayer.getCivicUpkeep(self.m_paeDisplayCivics, True), ))
		screen.setLabel("CivicsUpkeepText", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.BOTTOM_LINE_TOP + self.BOTTOM_LINE_HEIGHT - 2 * self.TEXT_MARGIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def handleInput(self, inputClass):
		screen = CyGInterfaceScreen("CivicsScreen", CvScreenEnums.CIVICS_SCREEN)
		pPlayer = gc.getPlayer(self.iActivePlayer)
		if inputClass.getButtonType() == WidgetTypes.WIDGET_PYTHON:
			if inputClass.getData1() == 8205:
				self.iSelectedCivic = inputClass.getData2()
				for i in xrange(gc.getNumCivicOptionInfos()):
					iCivic = self.m_paeDisplayCivics[i]
					if gc.getCivicInfo(iCivic).getCivicOptionType() == gc.getCivicInfo(self.iSelectedCivic).getCivicOptionType():
						if pPlayer.canRevolution(0) and pPlayer.canDoCivics(self.iSelectedCivic):
							self.m_paeDisplayCivics[i] = self.iSelectedCivic
						break
				self.drawComparison()
				self.drawCivics()
				self.drawChanges()
				self.updateAnarchy()
			elif inputClass.getData1() == 8206:
				for i in xrange(gc.getNumCivicOptionInfos()):
					iCivic = self.m_paeDisplayCivics[i]
					if gc.getCivicInfo(iCivic).getCivicOptionType() == gc.getCivicInfo(inputClass.getData2()).getCivicOptionType():
						self.m_paeDisplayCivics[i] = pPlayer.getCivics(gc.getCivicInfo(iCivic).getCivicOptionType())
						break
				self.drawComparison()
				self.drawCivics()
				self.drawChanges()
				self.updateAnarchy()
			return
		if inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID:
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.setActivePlayer(screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex))
			self.iSelectedCivic = -1
			self.drawComparison()
			self.drawCivics()
			self.drawChanges()
			self.updateAnarchy()
			return 1
		if inputClass.getFunctionName() == self.CANCEL_NAME:
			for i in xrange(gc.getNumCivicOptionInfos()):
				self.m_paeDisplayCivics[i] = pPlayer.getCivics(i)
			self.iSelectedCivic = -1
			self.drawComparison()
			self.drawCivics()
			self.drawChanges()
			self.updateAnarchy()
			return 1
		if inputClass.getFunctionName() == self.EXIT_NAME:
			if pPlayer.canRevolution(0):
				CyMessageControl().sendUpdateCivics(self.m_paeDisplayCivics)
			screen.hideScreen()
		return 0
		
	def update(self, fDelta):
		return