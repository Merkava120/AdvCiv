from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class TimeKeeper:
	def __init__(self):
		self.lMonths = ["TXT_KEY_MONTH_JANUARY", "TXT_KEY_MONTH_FEBRUARY", "TXT_KEY_MONTH_MARCH", "TXT_KEY_MONTH_APRIL", "TXT_KEY_MONTH_MAY", "TXT_KEY_MONTH_JUNE",
			"TXT_KEY_MONTH_JULY", "TXT_KEY_MONTH_AUGUST", "TXT_KEY_MONTH_SEPTEMBER", "TXT_KEY_MONTH_OCTOBER", "TXT_KEY_MONTH_NOVEMBER", "TXT_KEY_MONTH_DECEMBER"]

	def interfaceScreen(self):
		screen = CyGInterfaceScreen("TimeKeeper", CvScreenEnums.TIMEKEEPER)
		screen.addPanel( "MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN )
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setLabel("TimeKeeperHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_TIMEKEEPER", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setText("TimeKeeperExit", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 25, screen.getYResolution() - 40, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		iWidth = screen.getXResolution() - 40
		iHeight = (screen.getYResolution() - 100)/24 * 24 + 2
		iNumColumns = gc.getNumGameSpeedInfos() + 1
		screen.addTableControlGFC("TimeKeeperTable", iNumColumns, 20, 60, iWidth, iHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
		screen.setTableColumnHeader("TimeKeeperTable", 0, "", iWidth/iNumColumns)
		iMaxIncrements = 0
		for i in xrange(gc.getNumGameSpeedInfos()):
			SpeedInfo = gc.getGameSpeedInfo(i)
			screen.setTableColumnHeader("TimeKeeperTable", i + 1, SpeedInfo.getDescription(), iWidth/iNumColumns)
			iMaxIncrements = max(iMaxIncrements, SpeedInfo.getNumTurnIncrements())
		for i in xrange(iMaxIncrements * 6 + gc.getNumEraInfos() * 2 + 4):
			screen.appendTableRow("TimeKeeperTable")

		for i in xrange(gc.getNumGameSpeedInfos()):
			iStartYear = gc.getDefineINT("START_YEAR") * 12
			SpeedInfo = gc.getGameSpeedInfo(i)
			iTotalTurns = 0
			iRow = 0
			for j in xrange(SpeedInfo.getNumTurnIncrements()):
				iTurns = SpeedInfo.getGameTurnInfo(j).iNumGameTurnsPerIncrement
				iIncrement = SpeedInfo.getGameTurnInfo(j).iMonthIncrement
				sIncrement = self.separateYearMonth(iIncrement)
				iDuration = iTurns * iIncrement
				sDuration = self.separateYearMonth(iDuration)
				iTotalTurns += iTurns
				screen.setTableText("TimeKeeperTable", 0, iRow, "<font=3>" + CyTranslator().getText("TXT_KEY_WB_START_YEAR", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + CyTranslator().getText(self.lMonths[iStartYear%12], ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
				screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + self.getYear(iStartYear/12) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
				screen.setTableText("TimeKeeperTable", 0, iRow, "<font=3>" + CyTranslator().getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + str(iTurns) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
				screen.setTableText("TimeKeeperTable", 0, iRow, "<font=3>" + CyTranslator().getText("TXT_KEY_INCREMENT", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + sIncrement + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
				screen.setTableText("TimeKeeperTable", 0, iRow, "<font=3>" + CyTranslator().getText("TXT_KEY_DURATION", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + sDuration + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 2
				iStartYear += iDuration
			sColor = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ())
			iRow = iMaxIncrements * 6
			screen.setTableText("TimeKeeperTable", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_HALL_OF_FAME_SORT_BY_DATE", ()) + "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + sColor + CyTranslator().getText(self.lMonths[iStartYear%12], ()) + "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iRow += 1
			screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + sColor + self.getYear(iStartYear/12) + "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iRow += 1
			screen.setTableText("TimeKeeperTable", 0, iRow, "<font=3>" + sColor + CyTranslator().getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()) + "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + sColor + str(iTotalTurns) + "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			iRow += 2

			sColor = CyTranslator().getText("[COLOR_UNIT_TEXT]", ())
			for k in xrange(gc.getNumEraInfos()):
				iStartTurn = gc.getEraInfo(k).getStartPercent() * iTotalTurns / 100
				iStartYear = gc.getDefineINT("START_YEAR") * 12
				j = 0
				while iStartTurn > 0:
					iTurns = min(SpeedInfo.getGameTurnInfo(j).iNumGameTurnsPerIncrement, iStartTurn)
					iIncrement = SpeedInfo.getGameTurnInfo(j).iMonthIncrement
					iDuration = iTurns * iIncrement
					iStartYear += iDuration
					iStartTurn -= iTurns
					j += 1
				screen.setTableText("TimeKeeperTable", 0, iRow, "<font=3>" + sColor + gc.getEraInfo(k).getDescription() + "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + sColor + CyTranslator().getText(self.lMonths[iStartYear%12], ()) + "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
				screen.setTableText("TimeKeeperTable", i + 1, iRow, "<font=3>" + sColor + self.getYear(iStartYear/12)+ "</color></font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1

	def getYear(self, iYear):
		if iYear < 0:
			return str(- iYear) + " BC"
		else:
			return str(iYear) + " AD"

	def separateYearMonth(self, iValue):
		iValueYear = iValue /12
		iValueMonth = iValue %12
		sValue = ""
		if iValueYear > 0:
			sValue += str(iValueYear) + " YR"
		if iValueMonth > 0:
			sValue += str(iValueMonth) + " MTH"
		return sValue
	def handleInput (self, inputClass):
		return 0

	def update(self, fDelta):
		return 1