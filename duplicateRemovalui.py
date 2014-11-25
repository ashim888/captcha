#-------------------------------------------------------------------------------
# Name:        dupremovalui
# Purpose:
#
# Author:      Jangedoo
#
# Created:     13/05/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx, os, sys
import duplicateRemoval

class DuplicateRemovalUI(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        font=wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(20)
        lblTitle = wx.StaticText(self,label="Duplicate Removal", pos=(20,35))
        lblTitle.SetFont(font)
        lblUrl = wx.StaticText(self,label="File",size=(60,30))
        lblUrl.ToolTipString = 'File that contains urls/email or anything from which to remove the duplicates'
        self.urlFile_txt=wx.TextCtrl(self)
        self.urlFile_txt.ToolTipString = 'File that contains urls/email or anything from which to remove the duplicates'
        self.btnBrowseUrl = wx.Button(self,label="Browse")
        self.btnBrowseUrl.ToolTipString = 'File that contains urls/email or anything from which to remove the duplicates'


        self.btnStart = wx.Button(self,label="Start",size=(280,40))

        self.Bind(wx.EVT_BUTTON,self.file_browse,self.btnBrowseUrl)
        self.Bind(wx.EVT_BUTTON,self.start,self.btnStart)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        fileSizer = wx.BoxSizer(wx.HORIZONTAL)
        actionBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(lblTitle)
        fileSizer.Add(lblUrl,0,wx.ALL,5)
        fileSizer.Add(self.urlFile_txt,1,wx.ALL|wx.EXPAND,5)
        fileSizer.Add(self.btnBrowseUrl,0,wx.ALL,5)

        actionBtnSizer.Add(self.btnStart,0,wx.ALL,5)

        topSizer.Add(titleSizer,0,wx.CENTER,5)
        topSizer.Add((-1,10))
        topSizer.Add(fileSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(actionBtnSizer,0,wx.CENTER,5)
        self.SetSizer(topSizer)
        topSizer.Fit(self)

    def file_browse(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.urlFile_txt.SetValue(f)
        dlg.Destroy()

    def start(self,event):
        dr = duplicateRemoval.DuplicateRemoval(self.urlFile_txt.GetValue())
        dr.removeAndSave()
        wx.MessageBox("Duplicates removed and saved. See the log for details","Duplicate Remover")