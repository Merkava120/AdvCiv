from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
gc = CyGlobalContext()

class CvPediaIntro:
	def __init__(self, main):
		self.top = main

	def interfaceScreen(self):
		self.top.deleteAllWidgets()		
		screen = self.top.getScreen()
		if not screen.isActive():
			self.top.setPediaCommonWidgets()
		
		szHeader = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_INTRO", ()).upper()
		szHeader = u"<font=4b>" + self.top.color4 + CyTranslator().getText(self.top.sHelpIcon, ()) + szHeader + " " + CyTranslator().getText(self.top.sHelpIcon, ()) + "</color></font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, self.top.PLATYPEDIA_CONCEPT, -1)
		self.placeText()

	def placeText(self):
		screen = self.top.getScreen()
		screen.addPanel(self.top.getNextWidgetName(), "", "", true, true, self.top.X_ITEMS_PANE, self.top.Y_ITEMS_PANE, self.top.W_ITEMS_PANE, self.top.H_ITEMS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		sText = CyTranslator().getText("TXT_KEY_PEDIA_INTRO_BODY", ())
		screen.addMultilineText(self.top.getNextWidgetName(), sText, self.top.X_ITEMS_PANE + 10, self.top.Y_ITEMS_PANE + 10, self.top.W_ITEMS_PANE - 20, self.top.H_ITEMS_PANE - 10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def handleInput (self, inputClass):
		return 0