#-------------------------------------------------------------------------------
# Name:        backlinkcheckerui
# Purpose:
#
# Author:      Jangedoo
#
# Created:     24/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx, os, sys
import ConnectionManager
import thread
import backlinkchecker
import eventClass

class BacklinkCheckerUI(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(20)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.VERTICAL)
        yourSiteSizer = wx.BoxSizer(wx.HORIZONTAL)
        otherSiteSizer = wx.BoxSizer(wx.HORIZONTAL)
        proxySizer  = wx.BoxSizer(wx.HORIZONTAL)
        actionBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        threadSizer = wx.BoxSizer(wx.HORIZONTAL)

        lblTitle = wx.StaticText(self, label = "Backlink Checker")
        lblTitle.SetFont(font)
        titleSizer.Add(lblTitle, 0,wx.CENTER,5)

        lblYourSites = wx.StaticText(self, label="Your sites",size=(80,30))
        yourSiteSizer.Add(lblYourSites,0,wx.ALL,5)
        self.txtYourSite= wx.TextCtrl(self)
        yourSiteSizer.Add(self.txtYourSite,1,wx.ALL|wx.EXPAND,5)
        self.btnBrowseYourSite = wx.Button(self, label = 'Browse')
        self.Bind(wx.EVT_BUTTON,self.your_browse,self.btnBrowseYourSite)
        yourSiteSizer.Add(self.btnBrowseYourSite,0,wx.ALL,5)

        lblOtherSite = wx.StaticText(self, label="Sites to check",size=(80,30))
        otherSiteSizer.Add(lblOtherSite,0,wx.ALL,5)
        self.txtOtherSite = wx.TextCtrl(self)
        otherSiteSizer.Add(self.txtOtherSite,1,wx.ALL|wx.EXPAND,5)
        self.btnBrowseOtherSite = wx.Button(self, label='Browse')
        self.Bind(wx.EVT_BUTTON,self.other_browse,self.btnBrowseOtherSite)
        otherSiteSizer.Add(self.btnBrowseOtherSite,0,wx.ALL,5)

        lblProxy = wx.StaticText(self,label="Proxy File",size=(80,30))
        lblProxy.ToolTipString = 'File that contains proxies to use. Leave blank if you do not want to use proxies'
        self.proxyFile_txt=wx.TextCtrl(self)
        self.proxyFile_txt.ToolTipString='File that contains proxies to use. Leave blank if you do not want to use proxies'
        self.btnBrowseProxy = wx.Button(self,label="Browse")
        self.btnBrowseProxy.ToolTipString='File that contains proxies to use. Leave blank if you do not want to use proxies'
        self.Bind(wx.EVT_BUTTON,self.proxy_browse,self.btnBrowseProxy)

        proxySizer.Add(lblProxy,0,wx.ALL,5)
        proxySizer.Add(self.proxyFile_txt,1,wx.EXPAND|wx.ALL,5)
        proxySizer.Add(self.btnBrowseProxy,0,wx.ALL,5)


        lblThread = wx.StaticText(self,label='Number of threads')
        self.thread_slider = wx.Slider(self,value=5,minValue=1,maxValue=20, style=wx.SL_AUTOTICKS|wx.SL_LABELS)

        threadSizer.Add(lblThread,0,wx.ALL,5)
        threadSizer.Add(self.thread_slider,1,wx.EXPAND,5)

        self.btnStart = wx.Button(self,label="Start",size=(280,40))
        self.Bind(wx.EVT_BUTTON,self.start,self.btnStart)
        self.btnStop = wx.Button(self,label="Stop",size=(280,40))
        self.Bind(wx.EVT_BUTTON,self.stop,self.btnStop)

        actionBtnSizer.Add(self.btnStart,0,wx.ALL,5)
        actionBtnSizer.Add(self.btnStop,0,wx.ALL,5)

        topSizer.Add(titleSizer,0,wx.CENTER,5)
        topSizer.Add((-1,10))
        topSizer.Add(yourSiteSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(otherSiteSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(proxySizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(threadSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(actionBtnSizer,0,wx.CENTER,5)
        topSizer.Add((-1,10))

        self.SetSizer(topSizer)
        topSizer.Fit(self)

        self.evt = eventClass.EventClass(self.btnStart,self.btnStop,None,None)

    def your_browse(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.txtYourSite.SetValue(f)
        dlg.Destroy()


    def other_browse(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.txtOtherSite.SetValue(f)
        dlg.Destroy()

    def proxy_browse(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.proxyFile_txt.SetValue(f)
        dlg.Destroy()

    def start(self,event):
        yourSiteFile = self.txtYourSite.GetValue().replace('\\','/')
        otherSiteFile = self.txtOtherSite.GetValue().replace('\\','/')
        proxyFile = self.proxyFile_txt.GetValue().replace('\\','/')

        cm = ConnectionManager.ConnectionManager(proxyFile)
        self.datacontext = backlinkchecker.BacklinkChecher(otherSiteFile,yourSiteFile,cm,self.evt,self.thread_slider.GetValue())
        thread.start_new(self.datacontext.start, ())

    def stop(self,event):
        self.datacontext.stop()
        self.evt.onStop()


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='Dai Submitter v1 Beta')

        #now create panel and notebook on panel
        p=wx.Panel(self)
        nb=wx.Notebook(p)

        first_tab = BacklinkCheckerUI(nb)
        nb.AddPage(first_tab,"Proxy Harvester")

        #put notebook in sizer for managing the layout
        sizer=wx.BoxSizer()
        sizer.Add(nb,1,wx.EXPAND)
        p.SetSizer(sizer)
        log = wx.TextCtrl(p, wx.ID_ANY, size=(300,100), pos=(10,150),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        # redirect text here
        #redir=RedirectText(log)
        #sys.stdout=redir

if __name__=='__main__':
    app=wx.App(False)
    app.SetOutputWindowAttributes(title="Log")
    MainFrame().Show()
    app.MainLoop()
