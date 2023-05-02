from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import math
import IconGrid
import re
import PlatyOptions
gc = CyGlobalContext()

class CvExoticForeignAdvisor:
	def __init__(self):
		self.iScreen = -1
		self.nWidgetCount = 0
		self.nLineCount = 0
		self.WIDGET_ID = "ForeignAdvisorWidget"
		self.LINE_ID = "ForeignAdvisorLine"
		self.DEBUG_DROPDOWN_ID =  "ForeignAdvisorDropdownWidget"
		self.Y_TITLE = 8
		self.X_LEADER = 80
		self.Y_LEADER = 115
		self.W_LEADER = 64

		self.SCREEN_DICT = {
			"BONUS": 0,
			"TECH": 1,
			"RELATIONS": 2,
			"ACTIVE_TRADE": 3,
			"INFO": 4,
			"GLANCE": 5,
			}
		
		self.Y_LEADER_CIRCLE_TOP = 87
		self.LINE_WIDTH = 6
		
		self.iSelectedLeader = -1
		self.iActiveLeader = -1
		self.listSelectedLeaders = []
		self.iShiftKeyDown = 0

		self.GLANCE_HEADER = "ForeignAdvisorGlanceHeader"
		self.GLANCE_BUTTON = "ForeignAdvisorPlusMinus"
		
		self.X_GLANCE_OFFSET = 10
		self.GLANCE_BUTTON_SIZE = 50
		self.bGlancePlus = True
## Surplus Type Start ##
		self.iSurplus = -1
## Surplus Type End ##
## Relations Start ##
		self.bContactLine = False
		self.bWarLine = False
		self.bDefensiveLine = False
		self.bOpenBorderLine = False
		self.bTeamLine = False
		self.bVassalLine = False
		self.bHideVassal = False
		self.bHideTeam = False
## Relations End ##
############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################

		###################
		# General options #
		###################
		
		# Show the names of the leaders if 'True'
		self.SHOW_LEADER_NAMES = False
		
		# Show a border around the rows
		self.SHOW_ROW_BORDERS = True
		
		# Minimum space at the top and bottom of the screen.
		self.MIN_TOP_BOTTOM_SPACE = 60
		
		# Minimum space at the left and right end of the screen.
		self.MIN_LEFT_RIGHT_SPACE = 25
		
		# Extra border at the left and right ends of the column groups (import/export)
		self.GROUP_BORDER = 8
		
		# Extra space before the label of the column groups (import/export)
		self.GROUP_LABEL_OFFSET = "   "
		
		# Minimum space between the columns
		self.MIN_COLUMN_SPACE = 5
		
		# Minimum space between the rows
		self.MIN_ROW_SPACE = 1
		
		##########################
		# Resources view options #
		##########################
		
		# If 'True', the resource columns are grouped as import and export.
		self.RES_SHOW_IMPORT_EXPORT_HEADER = True
		
		# If 'True', two extra columns are used to display resources that are traded in active deals.
		self.RES_SHOW_ACTIVE_TRADE = True
		
		# Height of the panel showing the surplus resources. If self.RES_SHOW_SURPLUS_AMOUNT_ON_TOP is 'False'
		# you'll need to set a higher value for this variable (110 is recommended).
## Platy Bonus Screen ##
		self.RES_SURPLUS_HEIGHT = 4 * 24 + 50
## Platy Bonus Screen ##
		
		self.RES_GOLD_COL_WIDTH = 25
		
		#############################
		# Technologies view options #
		#############################
		
		# If 'True', use icon size 32x32
		# If 'False', use icon size 64x64
		self.TECH_USE_SMALL_ICONS = True
		
		self.TECH_GOLD_COL_WITH = 60
		
		###############
		# End options #
		###############
		
		self.TITLE_HEIGHT = 24
 		self.TABLE_CONTROL_HEIGHT = 24
		self.RESOURCE_ICON_SIZE = 34
		self.SCROLL_TABLE_UP = 1
		self.SCROLL_TABLE_DOWN = 2
		
##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################
		

		self.REV_SCREEN_DICT = {}

		for key, value in self.SCREEN_DICT.items():
			self.REV_SCREEN_DICT[value] = key

		self.DRAW_DICT = {
			"BONUS": self.drawResourceDeals,
			"TECH": self.drawTechDeals,
			"RELATIONS": self.drawRelations,
			"ACTIVE_TRADE": self.drawActive,
			"INFO": self.drawInfo,
			"GLANCE": self.drawGlance,
			}

		self.TXT_KEY_DICT = {
			"BONUS": "TXT_KEY_FOREIGN_ADVISOR_RESOURCES",
			"TECH": "TXT_KEY_FOREIGN_ADVISOR_TECHS",
			"RELATIONS": "TXT_KEY_FOREIGN_ADVISOR_RELATIONS",
			"ACTIVE_TRADE": "TXT_KEY_FOREIGN_ADVISOR_ACTIVE",
			"INFO": "TXT_KEY_FOREIGN_ADVISOR_INFO",
			"GLANCE": "TXT_KEY_FOREIGN_ADVISOR_GLANCE",
			}

		self.ORDER_LIST = ["RELATIONS", "GLANCE", "ACTIVE_TRADE", "BONUS", "INFO", "TECH"]
		self.iDefaultScreen = self.SCREEN_DICT["RELATIONS"]
						
	def interfaceScreen (self, iScreen):
	
		self.ATTITUDE_DICT = {
			"COLOR_GREEN": re.sub (":", "|", CyTranslator().getText ("TXT_KEY_ATTITUDE_FRIENDLY", ())),
			"COLOR_CYAN" : re.sub (":", "|", CyTranslator().getText ("TXT_KEY_ATTITUDE_PLEASED", ())),
			"COLOR_MAGENTA" : re.sub (":", "|", CyTranslator().getText ("TXT_KEY_ATTITUDE_ANNOYED", ())),
			"COLOR_RED" : re.sub (":", "|", CyTranslator().getText ("TXT_KEY_ATTITUDE_FURIOUS", ())),
			}
		if iScreen < 0:
			iScreen = self.iScreen
			if self.iScreen < 0:
				iScreen = self.iDefaultScreen
		self.SCREEN_TITLE = u"<font=4b>" + CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_TITLE", ()).upper() + u"</font>"

		if self.iScreen != iScreen:	
			self.killScreen()
			self.iScreen = iScreen
		
		screen = self.getScreen()
		self.X_LEGEND = 20
		self.H_LEGEND = 180
		self.Y_LEGEND = screen.getYResolution() - self.H_LEGEND - 55

		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)
	
		self.iActiveLeader = CyGame().getActivePlayer()
		self.iSelectedLeader = self.iActiveLeader
		self.listSelectedLeaders = []
		
		# Set the background and exit button, and show the screen
		screen.setDimensions(0, 0, screen.getXResolution(), screen.getYResolution())
## Unique Background ##
		screen.addDrawControl("ForeignAdvisorBackground", PlatyOptions.getBackGround(), 0, 0, screen.getXResolution(), screen.getYResolution(), WidgetTypes.WIDGET_GENERAL, -1, -1 )
## Unique Background ##
## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
## Transparent Panels ##
		screen.addPanel( "TopPanel", u"", u"", True, False, 0, 0, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "BottomPanel", u"", u"", True, False, 0, screen.getYResolution() - 55, screen.getXResolution(), 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.showWindowBackground(False)
		screen.setText("ForeignAdvisorExitWidget", "", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 30, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		self.nWidgetCount = 0
		self.nLineCount = 0
		
		if CyGame().isDebugMode():
			self.szDropdownName = self.getWidgetName(self.DEBUG_DROPDOWN_ID)
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(gc.getMAX_PLAYERS()):
				if gc.getPlayer(j).isAlive():
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		CyInterface().setDirty(InterfaceDirtyBits.Foreign_Screen_DIRTY_BIT, False)
		
		# Draw leader heads
		self.drawContents(True)
				
	# Drawing Leaderheads
	def drawContents(self, bInitial):
	
		if self.iScreen < 0:
			return
						
		self.deleteAllWidgets()
		screen = self.getScreen()

		# Header...
		screen.setLabel(self.getNextWidgetName(), "", self.SCREEN_TITLE, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution() / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
	
		if self.REV_SCREEN_DICT.has_key(self.iScreen):
			self.DRAW_DICT[self.REV_SCREEN_DICT[self.iScreen]] (bInitial)
		else:
			return

		# Link to other Foreign advisor screens
		self.DX_LINK = (screen.getXResolution() - 30) / (len (self.SCREEN_DICT) + 1)
		xLink = self.DX_LINK / 2;
		for i in range (len (self.ORDER_LIST)):
			szTextId = self.getNextWidgetName()
			szScreen = self.ORDER_LIST[i]
			if (self.iScreen != self.SCREEN_DICT[szScreen]):
				screen.setText (szTextId, "", u"<font=4>" + CyTranslator().getText (self.TXT_KEY_DICT[szScreen], ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, self.SCREEN_DICT[szScreen], -1)
			else:
				screen.setText (szTextId, "", u"<font=4>" + CyTranslator().getColorText (self.TXT_KEY_DICT[szScreen], (), gc.getInfoTypeForString ("COLOR_YELLOW")).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, screen.getYResolution() - 42, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_FOREIGN_ADVISOR, -1, -1)
			xLink += self.DX_LINK
	
	def drawRelations(self, bInitial):
		screen = self.getScreen()
		if self.iShiftKeyDown == 1:
			if (self.iSelectedLeader in self.listSelectedLeaders):
				self.listSelectedLeaders.remove(self.iSelectedLeader)
			else:
				self.listSelectedLeaders.append(self.iSelectedLeader)
		else:
			self.listSelectedLeaders = []
			if (not bInitial):
				self.listSelectedLeaders.append(self.iSelectedLeader)	

		bNoLeadersSelected = (len(self.listSelectedLeaders) == 0)
		bSingleLeaderSelected = (len(self.listSelectedLeaders) == 1)
		if bSingleLeaderSelected:
			self.iSelectedLeader = self.listSelectedLeaders[0]

		# legend
		iButtonSize = 18
		ButtonArt = CyArtFileMgr().getInterfaceArtInfo("WORLDBUILDER_TOGGLE_UNIT_EDIT_MODE").getPath()
		ButtonBorder = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath()

		x = self.X_LEGEND
		y = self.Y_LEGEND
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1801, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bContactLine)
		sText = u"<font=3>" + CyTranslator().getText("[COLOR_WHITE]", ()) + CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_CONTACT", ()) + "</color></font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		y += 30
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1802, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bWarLine)
		sText = u"<font=3>" + CyTranslator().getText("[COLOR_RED]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WAR", ()) + "</color></font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		y += 30
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1803, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bDefensiveLine)
		sText = u"<font=3>" + CyTranslator().getText("[COLOR_BLUE]", ()) + CyTranslator().getText("TXT_KEY_TRADE_DEFENSIVE_PACT_STRING", ()) + "</color></font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		y += 30
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1804, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bOpenBorderLine)
		sText = u"<font=3>" + CyTranslator().getText("[COLOR_GREEN]", ()) + CyTranslator().getText("TXT_KEY_TRADE_OPEN_BORDERS_STRING", ()) + "</color></font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		y += 30
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1805, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bTeamLine)
		sText = u"<font=3>" + CyTranslator().getText("[COLOR_YELLOW]", ()) + CyTranslator().getText("TXT_KEY_PITBOSS_TEAM", ()) + "</color></font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		y += 30
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1806, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bVassalLine)
		sText = u"<font=3>" + CyTranslator().getText("[COLOR_CYAN]", ()) + CyTranslator().getText("TXT_KEY_MISC_VASSAL_SHORT", ()) + "</color></font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		x = self.X_LEGEND
		y = self.Y_TITLE + 50
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1807, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bHideVassal)
		sText = u"<font=3>" + CyTranslator().getText("TXT_KEY_HIDE_VASSALS", ()) + "</font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		y += 30
		sLineName = self.getNextWidgetName()
		screen.addCheckBoxGFC(sLineName, ButtonArt, ButtonBorder, x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, 1808, -1, ButtonStyles.BUTTON_STYLE_IMAGE)
		screen.setState(sLineName, self.bHideTeam)
		sText = u"<font=3>" + CyTranslator().getText("TXT_KEY_HIDE_TEAM", ()) + "</font>"
		screen.setLabel(self.getNextWidgetName(), "", sText, CvUtil.FONT_LEFT_JUSTIFY, x + iButtonSize, y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		iCount = 0
		leaderMap = { }
		for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
			player = gc.getPlayer(iPlayer)
			if (player.isAlive() and iPlayer != self.iActiveLeader and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode())):
				if self.bHideVassal and gc.getTeam(player.getTeam()).isAVassal(): continue
				if self.bHideTeam and gc.getTeam(player.getTeam()).getLeaderID() != iPlayer: continue
				leaderMap[iPlayer] = iCount
				iCount += 1
		fLeaderTop = self.Y_LEADER_CIRCLE_TOP
		fLeaderArcTop = fLeaderTop + self.W_LEADER + 10
		iRadius = min((screen.getXResolution() - self.W_LEADER)/2, (screen.getYResolution() - fLeaderArcTop - 55))
		fRadius = iRadius - self.W_LEADER
		
		iLeaderWidth = self.W_LEADER
		if iCount < 8:
			iLeaderWidth = int(3 * self.W_LEADER / 2)
	
		# angle increment in radians (180 degree range)
		if (iCount < 2):
			deltaTheta = 0
		else:
			deltaTheta = math.pi / (iCount - 1)

		playerActive = gc.getPlayer(self.iActiveLeader)
		szLeaderHead = self.getNextWidgetName()
		screen.addCheckBoxGFC(szLeaderHead, gc.getLeaderHeadInfo(playerActive.getLeaderType()).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), screen.getXResolution()/2 - iLeaderWidth/2, int(fLeaderTop), iLeaderWidth, iLeaderWidth, WidgetTypes.WIDGET_LEADERHEAD, self.iActiveLeader, -1, ButtonStyles.BUTTON_STYLE_LABEL)
		screen.setState(szLeaderHead, self.iActiveLeader in self.listSelectedLeaders)
		szName = self.getNextWidgetName()
		sColor = u"<color=%d,%d,%d,%d>" %(playerActive.getPlayerTextColorR(), playerActive.getPlayerTextColorG(), playerActive.getPlayerTextColorB(), playerActive.getPlayerTextColorA())
		szLeaderName = u"<font=3>" + sColor + playerActive.getName() + u"</color></font>"
		screen.setLabel(szName, "", szLeaderName, CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, fLeaderTop + iLeaderWidth, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		for iPlayer in leaderMap.keys():
			player = gc.getPlayer(iPlayer)

			if bSingleLeaderSelected:
				# attitudes shown are towards single selected leader
				iBaseLeader = self.iSelectedLeader
			else:
				# attitudes shown are towards active leader
				iBaseLeader = self.iActiveLeader
			playerBase = gc.getPlayer(iBaseLeader)

			fX = int(screen.getXResolution()/2 - fRadius * math.cos(deltaTheta * leaderMap[iPlayer]) - iLeaderWidth/2) 
			fY = int(fLeaderArcTop + fRadius * math.sin(deltaTheta * leaderMap[iPlayer]) - iLeaderWidth/2)

			szLeaderHead = self.getNextWidgetName()
			screen.addCheckBoxGFC(szLeaderHead, gc.getLeaderHeadInfo(player.getLeaderType()).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), int(fX), int(fY), iLeaderWidth, iLeaderWidth, WidgetTypes.WIDGET_LEADERHEAD, iPlayer, iBaseLeader, ButtonStyles.BUTTON_STYLE_LABEL)
			screen.setState(szLeaderHead, iPlayer in self.listSelectedLeaders)
				
			szName = self.getNextWidgetName()
			sColor = u"<color=%d,%d,%d,%d>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA())
			szText = u"<font=3>" + sColor + player.getName() + u"</color></font>"
			if (gc.getTeam(player.getTeam()).isVassal(playerBase.getTeam())):
				szText = CyTranslator().getText("[ICON_SILVER_STAR]", ()) + szText
			elif (gc.getTeam(playerBase.getTeam()).isVassal(player.getTeam())):
				szText = CyTranslator().getText("[ICON_STAR]", ()) + szText
			screen.setLabel(szName, "", szText, CvUtil.FONT_CENTER_JUSTIFY, fX + iLeaderWidth/2, fY + iLeaderWidth, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			# Leader attitude towards active player
			szName = self.getNextWidgetName()
			lVincent = ["INTERFACE_ATTITUDE_0", "INTERFACE_ATTITUDE_1", "INTERFACE_ATTITUDE_2", "INTERFACE_ATTITUDE_3", "INTERFACE_ATTITUDE_4"]
			
			if (gc.getTeam(player.getTeam()).isHasMet(playerBase.getTeam()) and iBaseLeader != iPlayer):
				sButton = lVincent[gc.getPlayer(iPlayer).AI_getAttitude(iBaseLeader)]
				iButtonWidth = iLeaderWidth/3
				screen.setImageButton(szName, CyArtFileMgr().getInterfaceArtInfo(sButton).getPath(), int(fX), int(fY) + iLeaderWidth - iButtonWidth, iButtonWidth, iButtonWidth, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		for iSelectedLeader in xrange(gc.getMAX_CIV_PLAYERS()):
			bDisplayed = (gc.getPlayer(iSelectedLeader).isAlive() and (gc.getGame().isDebugMode() or gc.getTeam(gc.getPlayer(self.iActiveLeader).getTeam()).isHasMet(gc.getPlayer(iSelectedLeader).getTeam())))
			if self.bHideVassal and gc.getTeam(gc.getPlayer(iSelectedLeader).getTeam()).isAVassal(): continue
			if self.bHideTeam and gc.getTeam(gc.getPlayer(iSelectedLeader).getTeam()).getLeaderID() != iSelectedLeader: continue
			if iSelectedLeader in self.listSelectedLeaders or (bNoLeadersSelected and bDisplayed):
				# get selected player and location
				if (iSelectedLeader in leaderMap):
					thetaSelected = deltaTheta * leaderMap[iSelectedLeader]
					fXSelected = screen.getXResolution()/2 - fRadius * math.cos(thetaSelected)
					fYSelected = fLeaderArcTop + fRadius * math.sin(thetaSelected)
				else:
					fXSelected = screen.getXResolution()/2
					fYSelected = fLeaderTop + iLeaderWidth/2
				
				for iPlayer in leaderMap.keys():
					player = gc.getPlayer(iPlayer)

					fX = screen.getXResolution()/2 - fRadius * math.cos(deltaTheta * leaderMap[iPlayer])
					fY = fLeaderArcTop + fRadius * math.sin(deltaTheta * leaderMap[iPlayer])

					# draw lines
					if (iSelectedLeader != iPlayer):
						if (player.getTeam() == gc.getPlayer(iSelectedLeader).getTeam()):
							if not self.bTeamLine:
								szName = self.getNextLineName()
								screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_YELLOW") )						
						elif (gc.getTeam(player.getTeam()).isVassal(gc.getPlayer(iSelectedLeader).getTeam()) or gc.getTeam(gc.getPlayer(iSelectedLeader).getTeam()).isVassal(player.getTeam())):
							if not self.bVassalLine:
								szName = self.getNextLineName()
								screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_CYAN") )						
						elif (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(iSelectedLeader).getTeam())):
							if (gc.getTeam(player.getTeam()).isAtWar(gc.getPlayer(iSelectedLeader).getTeam())):
								if not self.bWarLine:
									szName = self.getNextLineName()
									screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_RED") )
							else:
								bJustPeace = True
								if (gc.getTeam(player.getTeam()).isOpenBorders(gc.getPlayer(iSelectedLeader).getTeam())):
									if not self.bOpenBorderLine:
										fDy = fYSelected - fY
										fDx = fXSelected - fX
										fTheta = math.atan2(fDy, fDx)
										if (fTheta > 0.5 * math.pi):
											fTheta -= math.pi
										elif (fTheta < -0.5 * math.pi):
											fTheta += math.pi
										fSecondLineOffsetY = self.LINE_WIDTH * math.cos(fTheta)
										fSecondLineOffsetX = -self.LINE_WIDTH * math.sin(fTheta)
										szName = self.getNextLineName()
										screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected + fSecondLineOffsetX), int(fYSelected + fSecondLineOffsetY), int(fX + fSecondLineOffsetX), int(fY + fSecondLineOffsetY), gc.getInfoTypeForString("COLOR_CITY_GREEN") )
									bJustPeace = False
								if (gc.getTeam(player.getTeam()).isDefensivePact(gc.getPlayer(iSelectedLeader).getTeam())):
									if not self.bDefensiveLine:
										szName = self.getNextLineName()
										screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_BLUE") )
									bJustPeace = False
								if (bJustPeace):
									if not self.bContactLine:
										szName = self.getNextLineName()
										screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), int(fX), int(fY), gc.getInfoTypeForString("COLOR_WHITE") )

				player = gc.getPlayer(self.iActiveLeader)
				if (player.getTeam() == gc.getPlayer(iSelectedLeader).getTeam()):
					if not self.bTeamLine:
						szName = self.getNextLineName()
						screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), screen.getXResolution()/2, fLeaderTop + iLeaderWidth/2, gc.getInfoTypeForString("COLOR_YELLOW") )
				elif (gc.getTeam(player.getTeam()).isVassal(gc.getPlayer(iSelectedLeader).getTeam()) or gc.getTeam(gc.getPlayer(iSelectedLeader).getTeam()).isVassal(player.getTeam())):
					if not self.bVassalLine:
						szName = self.getNextLineName()
						screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), screen.getXResolution()/2, fLeaderTop + iLeaderWidth/2, gc.getInfoTypeForString("COLOR_CYAN") )
				elif (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(iSelectedLeader).getTeam())):
					if (gc.getTeam(player.getTeam()).isAtWar(gc.getPlayer(iSelectedLeader).getTeam())):
						if not self.bWarLine:
							szName = self.getNextLineName()
							screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), screen.getXResolution()/2, fLeaderTop + iLeaderWidth/2, gc.getInfoTypeForString("COLOR_RED") )
					else:
						bJustPeace = True
						if (gc.getTeam(player.getTeam()).isOpenBorders(gc.getPlayer(iSelectedLeader).getTeam())):
							if not self.bOpenBorderLine:
								fDy = fLeaderTop + iLeaderWidth/2 - fYSelected
								fDx = screen.getXResolution()/2 - fXSelected
								fTheta = math.atan2(fDy, fDx)
								if (fTheta > 0.5 * math.pi):
									fTheta -= math.pi
								elif (fTheta < -0.5 * math.pi):
									fTheta += math.pi
								fSecondLineOffsetY = self.LINE_WIDTH * math.cos(fTheta)
								fSecondLineOffsetX = -self.LINE_WIDTH * math.sin(fTheta)
								szName = self.getNextLineName()
								screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected + fSecondLineOffsetX), int(fYSelected + fSecondLineOffsetY), int(screen.getXResolution()/2 + fSecondLineOffsetX), int(fLeaderTop + iLeaderWidth/2 + fSecondLineOffsetY), gc.getInfoTypeForString("COLOR_CITY_GREEN") )
							bJustPeace = False
						if (gc.getTeam(player.getTeam()).isDefensivePact(gc.getPlayer(iSelectedLeader).getTeam())):
							if not self.bDefensiveLine:
								szName = self.getNextLineName()
								screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), int(screen.getXResolution()/2), int(fLeaderTop + iLeaderWidth/2), gc.getInfoTypeForString("COLOR_BLUE") )
							bJustPeace = False
						if (bJustPeace):
							if not self.bContactLine:
								szName = self.getNextLineName()
								screen.addLineGFC("ForeignAdvisorBackground", szName, int(fXSelected), int(fYSelected), int(screen.getXResolution()/2), int(fLeaderTop + iLeaderWidth/2), gc.getInfoTypeForString("COLOR_WHITE") )

	def drawActive(self, bInitial):
		screen = self.getScreen()

		# Get the Players
		playerActive = gc.getPlayer(self.iActiveLeader)
					
		# Put everything inside a main panel, so we get vertical scrolling
		mainPanelName = self.getNextWidgetName()
		screen.addPanel(mainPanelName, "", "", True, True, 50, 100, screen.getXResolution() - 100, screen.getYResolution() - 200, PanelStyles.PANEL_STYLE_EMPTY)

		# loop through all players and sort them by number of active deals
		listPlayers = [(0,0)] * gc.getMAX_PLAYERS()
		nNumPLayers = 0
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			if (gc.getPlayer(iLoopPlayer).isAlive() and iLoopPlayer != self.iActiveLeader and not gc.getPlayer(iLoopPlayer).isBarbarian() and  not gc.getPlayer(iLoopPlayer).isMinorCiv()):
				if (gc.getTeam(gc.getPlayer(iLoopPlayer).getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or gc.getGame().isDebugMode()):
					nDeals = 0				
					for i in range(gc.getGame().getIndexAfterLastDeal()):
						deal = gc.getGame().getDeal(i)
						if ((deal.getFirstPlayer() == iLoopPlayer and deal.getSecondPlayer() == self.iActiveLeader) or (deal.getSecondPlayer() == iLoopPlayer and deal.getFirstPlayer() == self.iActiveLeader)):
							nDeals += 1
					listPlayers[nNumPLayers] = (nDeals, iLoopPlayer)
					nNumPLayers += 1
		listPlayers.sort()
		listPlayers.reverse()

		# loop through all players and display leaderheads
		for j in range (nNumPLayers):
			iLoopPlayer = listPlayers[j][1]

			# Player panel
			playerPanelName = self.getNextWidgetName()
## Unique Background ##
			screen.attachPanel(mainPanelName, playerPanelName, gc.getPlayer(iLoopPlayer).getName(), "", False, True, self.PanelStyle)
## Unique Background ##
			screen.attachLabel(playerPanelName, "", "   ")

			screen.attachImageButton(playerPanelName, "", gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, -1, False)
						
			innerPanelName = self.getNextWidgetName()
			screen.attachPanel(playerPanelName, innerPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)

			dealPanelName = self.getNextWidgetName()
			screen.attachListBoxGFC(innerPanelName, dealPanelName, "", TableStyles.TABLE_STYLE_EMPTY)	
			screen.enableSelect(dealPanelName, False)

			iRow = 0
			for i in range(gc.getGame().getIndexAfterLastDeal()):
				deal = gc.getGame().getDeal(i)

				if (deal.getFirstPlayer() == iLoopPlayer and deal.getSecondPlayer() == self.iActiveLeader and not deal.isNone()) or (deal.getSecondPlayer() == iLoopPlayer and deal.getFirstPlayer() == self.iActiveLeader):
					screen.appendListBoxString(dealPanelName, CyGameTextMgr().getDealString(deal, iLoopPlayer), WidgetTypes.WIDGET_DEAL_KILL, deal.getID(), -1, CvUtil.FONT_LEFT_JUSTIFY)
					iRow += 1

	def drawInfo (self, bInitial):
		screen = self.getScreen()
		playerActive = gc.getPlayer(self.iActiveLeader)
		mainPanelName = self.getNextWidgetName()
		screen.addScrollPanel(mainPanelName, "", 30, 60, screen.getXResolution() - 60, screen.getYResolution() - 140, PanelStyles.PANEL_STYLE_EXTERNAL)

		iCount = 0
		for iLoopPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive() and iLoopPlayer != self.iActiveLeader and (gc.getTeam(pLoopPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActiveLeader).getTeam()) or CyGame().isDebugMode()) and not pLoopPlayer.isMinorCiv()):
				
				sText = u"<color=%d,%d,%d,%d>%s</color>" %(pLoopPlayer.getPlayerTextColorR(), pLoopPlayer.getPlayerTextColorG(), pLoopPlayer.getPlayerTextColorB(), pLoopPlayer.getPlayerTextColorA(), pLoopPlayer.getName())
				sTemp = ""
				bFirst = True
				for i in xrange(gc.getNumTraitInfos()):
					if pLoopPlayer.hasTrait(i):
						if bFirst:
							bFirst = False
						else:
							sTemp += "/"
						sTemp += CyTranslator().getText(gc.getTraitInfo(i).getShortDescription(), ())
				if len(sTemp) > 0:
					sText += " [" + sTemp + "]"
				sTemp = ""
				lTrade = self.calculateTrade(self.iActiveLeader, iLoopPlayer)
				for i in xrange(len(lTrade)):
					if lTrade[i] > 0:
						sTemp += u"%d%c" %(lTrade[i], gc.getYieldInfo(i).getChar())
				if len(sTemp) > 0:
					sText += " " + CyTranslator().getText("[ICON_TRADE]", ()) + ": "+ sTemp
				iStateReligion = pLoopPlayer.getStateReligion()
				if iStateReligion > -1:
					ReligionInfo = gc.getReligionInfo(iStateReligion)
					if pLoopPlayer.hasHolyCity(iStateReligion):
						sText = u"%c" %(ReligionInfo.getHolyCityChar()) + sText
					else:
						sText = u"%c" %(ReligionInfo.getChar()) + sText
				screen.setTextAt(self.getNextWidgetName(), mainPanelName, "<font=3>" + sText + "</font>", CvUtil.FONT_LEFT_JUSTIFY, 0, iCount * 105, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				playerPanelName = self.getNextWidgetName()
				iWidth = (3 + gc.getNumCivicOptionInfos()) * 64 + 20
				if not CyGame().isOption(GameOptionTypes.GAMEOPTION_RANDOM_PERSONALITIES):
					iWidth += 3 * 64
				screen.attachPanelAt(mainPanelName, playerPanelName, "", "", False, True, self.PanelStyle, 0,iCount * 105 + 25, iWidth, 80, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				
				iX = 8
				iY = 8
				if PlatyOptions.bTransparent:
					iX -= 5
					iY -= 5
				iCivilization = pLoopPlayer.getCivilizationType()
				screen.addDDSGFCAt(self.getNextWidgetName(), playerPanelName, gc.getCivilizationInfo(iCivilization).getButton(), iX, iY, 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCivilization, -1, False)
				iX += 64
				LeaderInfo = gc.getLeaderHeadInfo(pLoopPlayer.getLeaderType())
				screen.addDDSGFCAt(self.getNextWidgetName(), playerPanelName, LeaderInfo.getButton(), iX, iY, 64, 64, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, -1, False)
				iX += 128

				for i in xrange(gc.getNumCivicOptionInfos()):
					nCivic = pLoopPlayer.getCivics(i)
					screen.addDDSGFCAt(self.getNextWidgetName(), playerPanelName, gc.getCivicInfo(nCivic).getButton(), iX, iY, 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, nCivic, 1, False)
					iX += 64

				if not CyGame().isOption(GameOptionTypes.GAMEOPTION_RANDOM_PERSONALITIES):
					iX += 64
					screen.setTextAt(self.getNextWidgetName(), mainPanelName, "<font=3>" + CyTranslator().getText("TXT_KEY_PEDIA_FAVOURITES", ()) + "</font>", CvUtil.FONT_LEFT_JUSTIFY, iX, iCount * 105, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					iFavCivic = LeaderInfo.getFavoriteCivic()
					if iFavCivic > -1:
						screen.addDDSGFCAt(self.getNextWidgetName(), playerPanelName, gc.getCivicInfo(iFavCivic).getButton(), iX, iY, 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iFavCivic, 1, False)
					iX += 64
					iFavReligion = LeaderInfo.getFavoriteReligion()
					if iFavReligion > -1:
						screen.addDDSGFCAt(self.getNextWidgetName(), playerPanelName, gc.getReligionInfo(iFavReligion).getButton(), iX, iY, 64, 64, WidgetTypes.WIDGET_HELP_RELIGION, iFavReligion, 1, False)
				iCount += 1
					
	def calculateTrade (self, nPlayer, nTradePartner):
		lTrade = []
		for i in xrange(YieldTypes.NUM_YIELD_TYPES):
			lTrade.append(0)
		pPlayer = gc.getPlayer(nPlayer)
		(pLoopCity, iter) = pPlayer.firstCity(False)
		while(pLoopCity):
			for i in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
				pTradeCity = pLoopCity.getTradeCity(i)
				if pTradeCity:
					if pTradeCity.getOwner() == nTradePartner:
						for j in xrange( YieldTypes.NUM_YIELD_TYPES ):
							lTrade[j] = lTrade[j] + pLoopCity.calculateTradeYield(j, pLoopCity.calculateTradeProfit(pTradeCity))		 
				else:
					break
			(pLoopCity, iter) = pPlayer.nextCity(iter, False)
		return lTrade

	def drawGlance (self, bInitial):

		screen = self.getScreen()
		iActiveTeam = gc.getPlayer(self.iActiveLeader).getTeam()
					
		# Put everything inside a main panel, so we get vertical scrolling
		mainPanelName = self.getNextWidgetName()
		screen.addPanel(mainPanelName, "", "", True, True, 0, 60 + self.GLANCE_BUTTON_SIZE, screen.getXResolution(), screen.getYResolution() - 110 - self.GLANCE_BUTTON_SIZE, PanelStyles.PANEL_STYLE_EMPTY)
## Unique Background ##
		screen.attachPanel(mainPanelName, self.GLANCE_HEADER, "", "", False, True, self.PanelStyle)
## Unique Background ##
		# loop through all players and display leaderheads
		if bInitial:
			self.nCount = 0
			self.ltPlayerRelations = [[0] * gc.getMAX_PLAYERS() for i in xrange (gc.getMAX_PLAYERS())]
			self.ltPlayerMet = [False] * gc.getMAX_PLAYERS()

			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if not pLoopPlayer.isAlive(): continue
				if pLoopPlayer.isMinorCiv(): continue
				if pLoopPlayer.isBarbarian(): continue
				if gc.getTeam(pLoopPlayer.getTeam()).isHasMet(iActiveTeam) or CyGame().isDebugMode():
					self.ltPlayerMet [iLoopPlayer] = True

					for nHost in xrange(gc.getMAX_PLAYERS()):
						pHost = gc.getPlayer(nHost)
						if not pHost.isAlive(): continue
						if nHost == self.iActiveLeader: continue
						if pHost.isMinorCiv(): continue
						if pHost.isBarbarian(): continue
						if gc.getTeam(pHost.getTeam()).isHasMet(iActiveTeam) or CyGame().isDebugMode():
							nRelation = self.calculateRelations (nHost, iLoopPlayer)
							self.ltPlayerRelations [iLoopPlayer][nHost] = nRelation
					self.nCount += 1

			self.nSpread = screen.getXResolution() / self.nCount
## Unique Background ##
		screen.addPanel(self.GLANCE_HEADER, u"", u"", True, False, 0, 50, screen.getXResolution(), self.GLANCE_BUTTON_SIZE + 10, self.PanelStyle)
## Unique Background ##
		nCount = 0
		for iLoopPlayer in xrange (gc.getMAX_PLAYERS()):
			if self.ltPlayerMet[iLoopPlayer]:
				if iLoopPlayer != self.iActiveLeader:
					szName = self.getNextWidgetName()
					screen.addCheckBoxGFCAt(self.GLANCE_HEADER, szName, gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.X_GLANCE_OFFSET + (self.nSpread * nCount), 5, self.GLANCE_BUTTON_SIZE, self.GLANCE_BUTTON_SIZE, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, self.iActiveLeader, ButtonStyles.BUTTON_STYLE_LABEL, False)
					screen.setState(szName, self.iSelectedLeader == iLoopPlayer)

				else:
					nButtonStyle = ButtonStyles.BUTTON_STYLE_CITY_MINUS
					if self.bGlancePlus:
						nButtonStyle = ButtonStyles.BUTTON_STYLE_CITY_PLUS					
					screen.attachLabel(self.GLANCE_HEADER, "", "   ")
					screen.addCheckBoxGFCAt(self.GLANCE_HEADER, self.GLANCE_BUTTON, "", "", 6, 5, self.GLANCE_BUTTON_SIZE, self.GLANCE_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, nButtonStyle, False)
				nCount += 1
		self.drawGlanceRows (screen, mainPanelName, self.iSelectedLeader != self.iActiveLeader, self.iSelectedLeader)

	def calculateRelations (self, nPlayer, nTarget):
		if (nPlayer != nTarget and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
			nAttitude = 0
			szAttitude = CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
			ltPlusAndMinuses = re.findall ("[-+][0-9]+\s?: ", szAttitude)
			for i in xrange (len (ltPlusAndMinuses)):
				nAttitude += int (ltPlusAndMinuses[i][:-2])
		else:
			return None
		return nAttitude

	def drawGlanceRows (self, screen, mainPanelName, bSorted = False, nPlayer = 1):
		iPanelHeight = max(self.GLANCE_BUTTON_SIZE, ((screen.getYResolution() - 110 - self.GLANCE_BUTTON_SIZE) / self.nCount - 5))

		ltSortedRelations = [(None,-1)] * gc.getMAX_PLAYERS()
		if bSorted:
			self.loadColIntoList (self.ltPlayerRelations, ltSortedRelations, nPlayer)
			ltSortedRelations.sort()
			if (self.bGlancePlus):
				ltSortedRelations.reverse()
		else:
			self.loadColIntoList (self.ltPlayerRelations, ltSortedRelations, nPlayer)

		# loop through all players and display leaderheads
		for nOffset in xrange (gc.getMAX_PLAYERS()):
			if ltSortedRelations[nOffset][1] != -1:
				break
		
		for i in xrange (self.nCount):
			iLoopPlayer = ltSortedRelations[nOffset + i][1]

			playerPanelName = self.getNextWidgetName()
## Unique Background ##
			screen.attachPanel(mainPanelName, playerPanelName, "", "", False, True, self.PanelStyle)
## Unique Background ##
			szName = self.getNextWidgetName()
			screen.attachCheckBoxGFC(playerPanelName, szName, gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), self.GLANCE_BUTTON_SIZE, self.GLANCE_BUTTON_SIZE, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, self.iActiveLeader, ButtonStyles.BUTTON_STYLE_LABEL)
## War Attitude Info ##
			nCount = 0
			for j in xrange (gc.getMAX_PLAYERS()):
				if self.ltPlayerMet[j]:
					if j != self.iActiveLeader:
						szName = self.getNextWidgetName()
						szName2 = self.getNextWidgetName()
						nAttitude = self.ltPlayerRelations[iLoopPlayer][j]
						if nAttitude != None:
							if gc.getTeam(gc.getPlayer(j).getTeam()).canDeclareWar(gc.getPlayer(iLoopPlayer).getTeam()) and not gc.getPlayer(j).isHuman():
								iLeaderType = gc.getPlayer(j).getLeaderType()
								iNoWar = gc.getLeaderHeadInfo(iLeaderType).getNoWarAttitudeProb(gc.getPlayer(j).AI_getAttitude(iLoopPlayer))
								sColor = CyTranslator().getText("[COLOR_RED]", ())
								if iNoWar > 80:
									sColor = CyTranslator().getText("[COLOR_GREEN]", ())
								elif iNoWar > 60:
									sColor = CyTranslator().getText("[COLOR_CYAN]", ())
								elif iNoWar > 40:
									sColor = CyTranslator().getText("[COLOR_WHITE]", ())
								elif iNoWar > 20:
									sColor = CyTranslator().getText("[COLOR_MAGENTA]", ())
							
								szText = "<font=3>" + sColor + str(iNoWar) + "%</color></font>"
								screen.setTextAt (szName2, playerPanelName, szText, CvUtil.FONT_CENTER_JUSTIFY, self.X_GLANCE_OFFSET + (self.nSpread * nCount), iPanelHeight/8, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PYTHON, 3838, iLeaderType)
							szText = self.getAttitudeText (nAttitude, j, iLoopPlayer)
							screen.setTextAt (szName, playerPanelName, szText, CvUtil.FONT_CENTER_JUSTIFY, self.X_GLANCE_OFFSET + (self.nSpread * nCount), iPanelHeight /2 - 5, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_LEADERHEAD, j, iLoopPlayer)
						else:
							szText = CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_NONE", ())
							screen.setTextAt (szName, playerPanelName, szText, CvUtil.FONT_CENTER_JUSTIFY, self.X_GLANCE_OFFSET + (self.nSpread * nCount), iPanelHeight /2 - 10, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					nCount += 1
## War Attitude Info ##

	def loadColIntoList (self, ltPlayers, ltTarget, nCol):
		nCount = 0
		for i in xrange (len (ltTarget)):
			if (self.ltPlayerMet[i]):
				ltTarget[nCount] = (ltPlayers[i][nCol], i)
				nCount += 1

	def getAttitudeText (self, nAttitude, nPlayer, nTarget):
		szText = str (nAttitude)
		szAttitude = CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
		if nAttitude > 0:
			szText = "+" + szText
		for szColor, szSearchString in self.ATTITUDE_DICT.items():
			if re.search (szSearchString, szAttitude):
				color = gc.getInfoTypeForString(szColor)
				szText = CyTranslator().changeTextColor (szText, color)
		szText = "<font=4>" + szText + "</font>"
		return szText

	def handlePlusMinusToggle (self):
		self.bGlancePlus = not self.bGlancePlus
		self.drawContents (False)

############################################
### BEGIN CHANGES ENHANCED INTERFACE MOD ###
############################################

	def initTradeTable(self):
		screen = self.getScreen()
		
		if (self.RES_SHOW_ACTIVE_TRADE):
			columns = ( IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN
					  , IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN
					  , IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN )
		else:
			columns = ( IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN
					  , IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN )
		self.NUM_RESOURCE_COLUMNS = len(columns) - 1
		
		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + self.RES_SURPLUS_HEIGHT + self.TITLE_HEIGHT + 10
		gridWidth = screen.getXResolution() - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = screen.getYResolution() - self.MIN_TOP_BOTTOM_SPACE * 2 - self.RES_SURPLUS_HEIGHT - self.TITLE_HEIGHT - 20
		
		self.resIconGridName = self.getNextWidgetName()
		self.resIconGrid = IconGrid.IconGrid( self.resIconGridName, screen, gridX, gridY, gridWidth, gridHeight, columns, True, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS )

		self.resIconGrid.setGroupBorder(self.GROUP_BORDER)
		self.resIconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.resIconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.resIconGrid.setMinRowSpace(self.MIN_ROW_SPACE)
		
		self.leaderCol = 0
		self.surplusCol = 1
		self.usedCol = 2
		self.willTradeCol = 3
		self.wontTradeCol = 4
		self.canPayCol = 5
		self.activeExportCol = 6
		self.activeImportCol = 7
		self.payingCol = 8
		
		self.resIconGrid.setHeader( self.leaderCol, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_LEADER", ()) )
		self.resIconGrid.setHeader( self.surplusCol, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE_2", ()) )
		self.resIconGrid.setHeader( self.usedCol, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_NOT_FOR_TRADE_2", ()) )
		self.resIconGrid.setHeader( self.willTradeCol, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE_2", ()) )
		self.resIconGrid.setHeader( self.wontTradeCol, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_NOT_FOR_TRADE_2", ()) )
		self.resIconGrid.setHeader( self.canPayCol, (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) )
		self.resIconGrid.setTextColWidth(self.canPayCol, self.RES_GOLD_COL_WIDTH)
		
		if (self.RES_SHOW_ACTIVE_TRADE):
			self.resIconGrid.setHeader( self.activeExportCol, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_EXPORT", ()) )
			self.resIconGrid.setHeader( self.activeImportCol, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_IMPORT", ()) )
			self.resIconGrid.setHeader( self.payingCol, (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) )
			self.resIconGrid.setTextColWidth(self.payingCol, self.RES_GOLD_COL_WIDTH)
		if (self.RES_SHOW_IMPORT_EXPORT_HEADER):
			self.resIconGrid.createColumnGroup("", 1)
			self.resIconGrid.createColumnGroup(CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_EXPORT", ()), 2)
			self.resIconGrid.createColumnGroup(CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_IMPORT", ()), 3)
			if (self.RES_SHOW_ACTIVE_TRADE):
				self.resIconGrid.createColumnGroup(CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_ACTIVE", ()), 3)
		
		gridWidth = self.resIconGrid.getPrefferedWidth()
		gridHeight = self.resIconGrid.getPrefferedHeight()
		self.RES_LEFT_RIGHT_SPACE = (screen.getXResolution() - gridWidth - 20) / 2
		self.RES_TOP_BOTTOM_SPACE = (screen.getYResolution() - gridHeight - self.RES_SURPLUS_HEIGHT - self.TITLE_HEIGHT - 20) / 2
		gridX = self.RES_LEFT_RIGHT_SPACE + 10
		gridY = self.RES_TOP_BOTTOM_SPACE + self.RES_SURPLUS_HEIGHT + self.TITLE_HEIGHT + 10
		
		self.resIconGrid.setPosition(gridX, gridY)
		self.resIconGrid.setSize(gridWidth, gridHeight)
		
	def drawResourceDeals(self, bInitial):
		screen = self.getScreen()
		activePlayer = gc.getPlayer(self.iActiveLeader)
		self.initTradeTable()
		
		# Find all the surplus resources
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_RESOURCES
## Surplus Type Start ##
		self.SURPLUS_WIDTH = screen.getXResolution() - 2 * self.RES_LEFT_RIGHT_SPACE
		
		# Assemble the surplus panel
		self.mainAvailablePanel = self.getNextWidgetName()
	## Transparent Panels ##
		self.PanelStyle = PanelStyles.PANEL_STYLE_MAIN
		if PlatyOptions.bTransparent:
			self.PanelStyle = PanelStyles.PANEL_STYLE_IN
		screen.addPanel( self.mainAvailablePanel, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_SURPLUS_RESOURCES", ()), "", False, False, self.RES_LEFT_RIGHT_SPACE, self.RES_TOP_BOTTOM_SPACE, self.SURPLUS_WIDTH, self.RES_SURPLUS_HEIGHT, self.PanelStyle)
	## Transparent Panels ##

		szDropdownName = str("PlatySurplus")
		screen.addDropDownBoxGFC(szDropdownName, self.RES_LEFT_RIGHT_SPACE + 160, self.RES_TOP_BOTTOM_SPACE - 5, 100, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString(szDropdownName, CyTranslator().getText("TXT_KEY_WB_CITY_ALL",()), 0, 0, True)
		screen.addPullDownString(szDropdownName, CyTranslator().getText("TXT_KEY_GLOBELAYER_RESOURCES_GENERAL",()), 1, 1, 0 == self.iSurplus)
		iBonusClass = 1
		while not gc.getBonusClassInfo(iBonusClass) is None:
			sText = gc.getBonusClassInfo(iBonusClass).getType()
			sText = sText[sText.find("_") +1:]
			sText = sText.lower()
			sText = sText.capitalize()
			screen.addPullDownString(szDropdownName, sText, iBonusClass + 1, iBonusClass + 1, iBonusClass == self.iSurplus)
			iBonusClass += 1

		listSurplus = []
		for iLoopBonus in xrange(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(iLoopBonus).getBonusClassType() != self.iSurplus) and self.iSurplus > -1: continue
			tradeData.iData = iLoopBonus
			if activePlayer.getNumTradeableBonuses(iLoopBonus) < 2: continue
			for iLoopPlayer in xrange(gc.getMAX_CIV_PLAYERS()):
				currentPlayer = gc.getPlayer(iLoopPlayer)
				if currentPlayer.isMinorCiv(): continue
				if iLoopPlayer == self.iActiveLeader: continue
				if not currentPlayer.isAlive(): continue
				if gc.getTeam(currentPlayer.getTeam()).isHasMet(activePlayer.getTeam()) and activePlayer.canTradeItem(iLoopPlayer, tradeData, False):
					listSurplus.append(iLoopBonus)
					break
## Surplus Type End ##

## Platy Bonus Screen ##
		if len(listSurplus) > 0:
			self.availableTable = self.getNextWidgetName()
			iColumnWidth = 70
			iMaxColumn = self.SURPLUS_WIDTH / iColumnWidth
			iWidthSpace = (self.SURPLUS_WIDTH - (iMaxColumn * iColumnWidth)) /2
			iTable_Y = self.RES_TOP_BOTTOM_SPACE + 25
			iTable_H = self.RES_SURPLUS_HEIGHT - 50
			if self.PanelStyle == PanelStyles.PANEL_STYLE_MAIN:
				iTable_Y = self.RES_TOP_BOTTOM_SPACE + 36
				iTable_H = self.RES_SURPLUS_HEIGHT - 48
			screen.addTableControlGFC(self.availableTable, iMaxColumn, self.RES_LEFT_RIGHT_SPACE + iWidthSpace, iTable_Y, iMaxColumn * (iColumnWidth), iTable_H
				    , False, True, 24, 24, TableStyles.TABLE_STYLE_EMPTY )

			for i in xrange(iMaxColumn):
				screen.setTableColumnHeader(self.availableTable, i, "", iColumnWidth)
			nRows = (len(listSurplus) + iMaxColumn - 1) / iMaxColumn
			for i in xrange(nRows):
				screen.appendTableRow(self.availableTable)

			for i in xrange(len(listSurplus)):
				iRow = i / iMaxColumn
				iColumn = i % iMaxColumn
				sText = u"<font=4>%c<font=1> (%d)</font>" %(gc.getBonusInfo(listSurplus[i]).getChar(), activePlayer.getNumTradeableBonuses(listSurplus[i]) - 1)
				screen.setTableText(self.availableTable, iColumn, iRow, sText, "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, listSurplus[i], 1, CvUtil.FONT_LEFT_JUSTIFY )
## Platy Bonus Screen ##	
		
		# Assemble the panel that shows the trade table
		self.TABLE_PANEL_X = self.RES_LEFT_RIGHT_SPACE
		self.TABLE_PANEL_Y = self.RES_TOP_BOTTOM_SPACE + self.RES_SURPLUS_HEIGHT
		self.TABLE_PANEL_WIDTH = screen.getXResolution() - 2 * self.RES_LEFT_RIGHT_SPACE
		self.TABLE_PANEL_HEIGHT = screen.getYResolution() - self.TABLE_PANEL_Y - self.RES_TOP_BOTTOM_SPACE
		
		self.tradePanel = self.getNextWidgetName()
## Unique Background ##
		screen.addPanel( self.tradePanel, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_TRADE_TABLE", ()), ""
					   , True, True, self.TABLE_PANEL_X, self.TABLE_PANEL_Y, self.TABLE_PANEL_WIDTH, self.TABLE_PANEL_HEIGHT
					   , self.PanelStyle)
## Unique Background
		self.resIconGrid.createGrid()
		
		# find all players that need to be listed 
		self.resIconGrid.clearData()
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_RESOURCES
		currentRow = 0
		
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			currentPlayer = gc.getPlayer(iLoopPlayer)
			if ( currentPlayer.isAlive() and not currentPlayer.isBarbarian() and not currentPlayer.isMinorCiv() 
										 and gc.getTeam(currentPlayer.getTeam()).isHasMet(activePlayer.getTeam()) 
										 and iLoopPlayer != self.iActiveLeader ):
				message = ""
				if ( not activePlayer.canTradeNetworkWith(iLoopPlayer) ):
					message = CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_NOT_CONNECTED", ())
				
				self.resIconGrid.appendRow(currentPlayer.getName(), message)
				self.resIconGrid.addIcon( currentRow, self.leaderCol, gc.getLeaderHeadInfo(currentPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer )
				for iLoopBonus in xrange(gc.getNumBonusInfos()):
## Surplus Type ##
					if (gc.getBonusInfo(iLoopBonus).getBonusClassType() != self.iSurplus) and self.iSurplus > -1: continue
## Surplus Type ##
					if (gc.getTeam(activePlayer.getTeam()).isGoldTrading() or gc.getTeam(currentPlayer.getTeam()).isGoldTrading()):
						sAmount = str(gc.getPlayer(iLoopPlayer).AI_maxGoldPerTurnTrade(self.iActiveLeader))
						self.resIconGrid.setText(currentRow, self.canPayCol, sAmount)
					
					tradeData.iData = iLoopBonus
					if (activePlayer.canTradeItem(iLoopPlayer, tradeData, False)):
						if (activePlayer.canTradeItem(iLoopPlayer, tradeData, (not currentPlayer.isHuman()))): # surplus
							self.resIconGrid.addIcon( currentRow, self.surplusCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus )
						else: # used
							self.resIconGrid.addIcon( currentRow, self.usedCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus )
					if (currentPlayer.canTradeItem(self.iActiveLeader, tradeData, False)):
						if (currentPlayer.canTradeItem(self.iActiveLeader, tradeData, (not currentPlayer.isHuman()))): # will trade
							self.resIconGrid.addIcon( currentRow, self.willTradeCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus )
						else: # won't trade
							self.resIconGrid.addIcon( currentRow, self.wontTradeCol, gc.getBonusInfo(iLoopBonus).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iLoopBonus )
				if (self.RES_SHOW_ACTIVE_TRADE):
					amount = 0
					for iLoopDeal in range(gc.getGame().getIndexAfterLastDeal()):
						deal = gc.getGame().getDeal(iLoopDeal)
						if ( deal.getFirstPlayer() == iLoopPlayer and deal.getSecondPlayer() == self.iActiveLeader and not deal.isNone() ):
							for iLoopTradeItem in range(deal.getLengthFirstTrades()):
								tradeData2 = deal.getFirstTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount += tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeImportCol, gc.getBonusInfo(tradeData2.iData).getButton()	, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )
							for iLoopTradeItem in range(deal.getLengthSecondTrades()):
								tradeData2 = deal.getSecondTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount -= tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeExportCol, gc.getBonusInfo(tradeData2.iData).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )
						
						if ( deal.getSecondPlayer() == iLoopPlayer and deal.getFirstPlayer() == self.iActiveLeader ):
							for iLoopTradeItem in range(deal.getLengthFirstTrades()):
								tradeData2 = deal.getFirstTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount -= tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeExportCol, gc.getBonusInfo(tradeData2.iData).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )
							for iLoopTradeItem in range(deal.getLengthSecondTrades()):
								tradeData2 = deal.getSecondTrade(iLoopTradeItem)
								if (tradeData2.ItemType == TradeableItems.TRADE_GOLD_PER_TURN):
									amount += tradeData2.iData
								if (tradeData2.ItemType == TradeableItems.TRADE_RESOURCES):
									self.resIconGrid.addIcon( currentRow, self.activeImportCol	, gc.getBonusInfo(tradeData2.iData).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, tradeData2.iData )
					if (amount != 0):
						self.resIconGrid.setText(currentRow, self.payingCol, str(amount))
				currentRow += 1
		self.resIconGrid.refresh()
	
	
	def scrollTradeTableUp(self):
		if (self.iScreen == self.SCREEN_DICT["BONUS"]):
			self.resIconGrid.scrollUp()
		elif (self.iScreen == self.SCREEN_DICT["TECH"]):
			self.techIconGrid.scrollUp()


	def scrollTradeTableDown(self):
		if (self.iScreen == self.SCREEN_DICT["BONUS"]):
			self.resIconGrid.scrollDown()
		elif (self.iScreen == self.SCREEN_DICT["TECH"]):
			self.techIconGrid.scrollDown()
				
	def drawTechDeals(self, bInitial):
		screen = self.getScreen()
		activePlayer = gc.getPlayer(self.iActiveLeader)
		self.initTechTable()
		
		# Assemble the panel
		TECH_PANEL_X = self.TECH_LEFT_RIGHT_SPACE
		TECH_PANEL_Y = self.TECH_TOP_BOTTOM_SPACE
		TECH_PANEL_WIDTH = screen.getXResolution() - 2 * self.TECH_LEFT_RIGHT_SPACE
		TECH_PANEL_HEIGHT = screen.getYResolution() - 2 * self.TECH_TOP_BOTTOM_SPACE
## Unique Background ##	
		self.tradePanel = self.getNextWidgetName()
		screen.addPanel( self.tradePanel, "", "", True, True, TECH_PANEL_X, TECH_PANEL_Y, TECH_PANEL_WIDTH, TECH_PANEL_HEIGHT, self.PanelStyle)
## Unique Background ##		
		self.techIconGrid.createGrid()
		
		self.techIconGrid.clearData()
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
		currentRow = 0
		
		for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
			currentPlayer = gc.getPlayer(iLoopPlayer)
			if currentPlayer.getTeam() == gc.getPlayer(self.iActiveLeader).getTeam(): continue
			if currentPlayer.isMinorCiv(): continue
			if currentPlayer.isAlive() and gc.getTeam(currentPlayer.getTeam()).isHasMet(activePlayer.getTeam()):
				message = ""
				if ( not gc.getTeam(activePlayer.getTeam()).isTechTrading() and not gc.getTeam(currentPlayer.getTeam()).isTechTrading() ):
					message = CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_NO_TECH_TRADING", ())

				self.techIconGrid.appendRow(currentPlayer.getName(), message)
				self.techIconGrid.addIcon( currentRow, 0, gc.getLeaderHeadInfo(currentPlayer.getLeaderType()).getButton(), WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer )
				
				if (gc.getTeam(activePlayer.getTeam()).isGoldTrading() or gc.getTeam(currentPlayer.getTeam()).isGoldTrading()):
					sAmount = str(gc.getPlayer(iLoopPlayer).AI_maxGoldTrade(self.iActiveLeader))
					self.techIconGrid.setText(currentRow, 3, sAmount)
				
				if (gc.getTeam(activePlayer.getTeam()).isTechTrading() or gc.getTeam(currentPlayer.getTeam()).isTechTrading() ):

					for iLoopTech in xrange(gc.getNumTechInfos()):
					
						tradeData.iData = iLoopTech
						if (activePlayer.canTradeItem(iLoopPlayer, tradeData, False) and activePlayer.getTradeDenial(iLoopPlayer, tradeData) == DenialTypes.NO_DENIAL): # wants
							self.techIconGrid.addIcon( currentRow, 1, gc.getTechInfo(iLoopTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
						elif currentPlayer.canResearch(iLoopTech, False):
							self.techIconGrid.addIcon( currentRow, 2, gc.getTechInfo(iLoopTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
						if (currentPlayer.canTradeItem(self.iActiveLeader, tradeData, False)):
							if (currentPlayer.getTradeDenial(self.iActiveLeader, tradeData) == DenialTypes.NO_DENIAL): # will trade
								self.techIconGrid.addIcon( currentRow, 4, gc.getTechInfo(iLoopTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
							else: # won't trade
								self.techIconGrid.addIcon( currentRow, 5, gc.getTechInfo(iLoopTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
						elif (gc.getTeam(currentPlayer.getTeam()).isHasTech(iLoopTech) and activePlayer.canResearch(iLoopTech, False)):
							self.techIconGrid.addIcon( currentRow, 6, gc.getTechInfo(iLoopTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iLoopTech )
				currentRow += 1
		self.techIconGrid.refresh()

	def initTechTable(self):
		screen = self.getScreen()
		
		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + 10
		gridWidth = screen.getXResolution() - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = screen.getYResolution() - self.MIN_TOP_BOTTOM_SPACE * 2 - 20
		
		columns = ( IconGrid.GRID_ICON_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN
								, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_TEXT_COLUMN
								, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN, IconGrid.GRID_MULTI_LIST_COLUMN )
		self.techIconGridName = self.getNextWidgetName()
		self.techIconGrid = IconGrid.IconGrid( self.techIconGridName, screen, gridX, gridY, gridWidth, gridHeight, columns, self.TECH_USE_SMALL_ICONS, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS )

		self.techIconGrid.setGroupBorder(self.GROUP_BORDER)
		self.techIconGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.techIconGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.techIconGrid.setMinRowSpace(self.MIN_ROW_SPACE)
		
		self.techIconGrid.setHeader( 0, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_LEADER", ()) )
		self.techIconGrid.setHeader( 1, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_WANTS", ()) )
		self.techIconGrid.setHeader( 2, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_CAN_RESEARCH", ()) )
		self.techIconGrid.setHeader( 3, (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) )
		self.techIconGrid.setTextColWidth( 3, self.TECH_GOLD_COL_WITH )
		self.techIconGrid.setHeader( 4, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_FOR_TRADE_2", ()) )
		self.techIconGrid.setHeader( 5, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_NOT_FOR_TRADE_2", ()) )
		self.techIconGrid.setHeader( 6, CyTranslator().getText("TXT_KEY_FOREIGN_ADVISOR_CANT_TRADE", ()) )
		
		gridWidth = self.techIconGrid.getPrefferedWidth()
		gridHeight = self.techIconGrid.getPrefferedHeight()
		self.TECH_LEFT_RIGHT_SPACE = (screen.getXResolution() - gridWidth - 20) / 2
		self.TECH_TOP_BOTTOM_SPACE = (screen.getYResolution() - gridHeight - 20) / 2
		gridX = self.TECH_LEFT_RIGHT_SPACE + 10
		gridY = self.TECH_TOP_BOTTOM_SPACE + 10
		
		self.techIconGrid.setPosition(gridX, gridY)
		self.techIconGrid.setSize(gridWidth, gridHeight)
		
##########################################
### END CHANGES ENHANCED INTERFACE MOD ###
##########################################
					
	# Handles the input for this screen...
	def handleInput (self, inputClass):

## Platy Foreign Start ##
		if inputClass.getData1() > 1800 and  inputClass.getData1() < 1810:
			self.handlePlatyToggleRelationshipsCB(inputClass.getData1())
			return
## Platy Foreign End ##
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_LEADERHEAD):
				if (inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP):
					self.iSelectedLeader = inputClass.getData1()
					self.drawContents(False)
				elif (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
					if inputClass.getData1() != self.iActiveLeader:
						self.getScreen().hideScreen()
			elif (inputClass.getFunctionName() == self.GLANCE_BUTTON):
				self.handlePlusMinusToggle()
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.SCROLL_TABLE_UP):
					self.scrollTradeTableUp()
				elif (inputClass.getData1() == self.SCROLL_TABLE_DOWN):
					self.scrollTradeTableDown()
			 
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() + str(inputClass.getID()) == self.getWidgetName(self.DEBUG_DROPDOWN_ID)):
				print 'debug dropdown event'
				szName = self.getWidgetName(self.DEBUG_DROPDOWN_ID)
				iIndex = self.getScreen().getSelectedPullDownID(szName)
				self.iActiveLeader = self.getScreen().getPullDownData(szName, iIndex)
				self.drawContents(False)
## Surplus Type Start ##
			if (inputClass.getFunctionName() == "PlatySurplus"):
				self.handlePlatySurplus(inputClass.getData())
## Surplus Type End ##
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_LSHIFT) or inputClass.getData() == int(InputTypes.KB_RSHIFT)):
				self.iShiftKeyDown = inputClass.getID() 

		return 0


## Surplus Type ##
	def handlePlatySurplus ( self, argsList ) :
		self.iSurplus = int(argsList) - 1
		self.drawContents(True)
		return 1
## Platy Foreign Start ##

	def handlePlatyToggleRelationshipsCB ( self, iData1):
		if iData1 == 1801:
			self.bContactLine = not self.bContactLine
		elif iData1 == 1802:
			self.bWarLine = not self.bWarLine
		elif iData1 == 1803:
			self.bDefensiveLine = not self.bDefensiveLine
		elif iData1 == 1804:
			self.bOpenBorderLine = not self.bOpenBorderLine
		elif iData1 == 1805:
			self.bTeamLine = not self.bTeamLine
		elif iData1 == 1806:
			self.bVassalLine = not self.bVassalLine
		elif iData1 == 1807:
			self.bHideVassal = not self.bHideVassal
		elif iData1 == 1808:
			self.bHideTeam = not self.bHideTeam
		self.drawContents(True)
		return 1
## Platy Foreign End ##

	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount * 4 + self.iScreen)
		self.nWidgetCount += 1
		return szName
											
	def getNextLineName(self):
		szName = self.LINE_ID + str(self.nLineCount * 4 + self.iScreen)
		self.nLineCount += 1
		return szName
											
	def getWidgetName(self, szBaseName):
		szName = szBaseName + str(self.iScreen)
		return szName
		
	def clearAllLines(self):
		screen = self.getScreen()
		nLines = self.nLineCount
		self.nLineCount = 0
		for i in range(nLines):
			screen.removeLineGFC("ForeignAdvisorBackground", self.getNextLineName())
		self.nLineCount = 0	
		
	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0
		self.clearAllLines()

	def killScreen(self):
		if (self.iScreen >= 0):
			screen = self.getScreen()
			screen.hideScreen()
			self.iScreen = -1
		return

	def getScreen(self):
		return CyGInterfaceScreen("ForeignAdvisor" + str(self.iScreen), CvScreenEnums.FOREIGN_ADVISOR)

	def update(self, fDelta):
		if (CyInterface().isDirty(InterfaceDirtyBits.Foreign_Screen_DIRTY_BIT) == True):
			CyInterface().setDirty(InterfaceDirtyBits.Foreign_Screen_DIRTY_BIT, False)
			self.drawContents(False)
		return