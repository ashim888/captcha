#-------------------------------------------------------------------------------
# Name:        captchasettingsui
# Purpose:
#
# Author:      Jangedoo
#
# Created:     21/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import predict


class ProxyHarvesterUI(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        lblTitle = wx.StaticText(self,label="Captcha Setting", pos=(20,35))

