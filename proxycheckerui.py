#-------------------------------------------------------------------------------
# Name:        proxyCheckerUI
# Purpose:
#
# Author:      Jangedoo
#
# Created:     19/04/2013
# Copyright:   (c) Jangedoo 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx, os, sys
import ConnectionManager
import thread
import proxychecker
import eventClass


class ProxyCheckerUI(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.isRunning = False

        font=wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        lblTitle = wx.StaticText(self,label="Proxy Checker", pos=(20,35))
        lblTitle.SetFont(font)
        lblUrl = wx.StaticText(self,label="Url to connect",size=(60,30))
        lblUrl.ToolTipString = 'Enter url to connect to using the proxy. Must start with http://'
        self.urlFile_txt=wx.TextCtrl(self)
        self.urlFile_txt.ToolTipString = 'Enter url to connect to using the proxy. Must start with http://'


        lblProxy = wx.StaticText(self,label="Proxy File",size=(60,30))
        lblProxy.ToolTipString = 'File that contains proxies to check'
        self.proxyFile_txt=wx.TextCtrl(self)
        self.proxyFile_txt.ToolTipString='File that contains proxies to check'
        self.btnBrowseProxy = wx.Button(self,label="Browse")
        self.btnBrowseProxy.ToolTipString='File that contains proxies to check'

        lblThread = wx.StaticText(self,label='Number of threads')
        self.thread_slider = wx.Slider(self,value=5,minValue=1,maxValue=20, style=wx.SL_AUTOTICKS|wx.SL_LABELS)

        #Bind Buttons

        self.Bind(wx.EVT_BUTTON,self.proxy_browse,self.btnBrowseProxy)


        self.btnStart = wx.Button(self,label="Start",size=(280,40))
        self.Bind(wx.EVT_BUTTON,self.start,self.btnStart)
        self.btnStop = wx.Button(self,label="Stop",size=(280,40))
        self.Bind(wx.EVT_BUTTON,self.stop,self.btnStop)

        self.evt = eventClass.EventClass(self.btnStart, self.btnStop, None, None)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSixer = wx.BoxSizer(wx.HORIZONTAL)
        urlSizer = wx.BoxSizer(wx.HORIZONTAL)
        proxySizer = wx.BoxSizer(wx.HORIZONTAL)
        threadSizer = wx.BoxSizer(wx.VERTICAL)
        actionBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSixer.Add(lblTitle)

        urlSizer.Add(lblUrl,0,wx.ALL,5)
        urlSizer.Add(self.urlFile_txt,1,wx.ALL|wx.EXPAND,5)



        proxySizer.Add(lblProxy,0,wx.ALL,5)
        proxySizer.Add(self.proxyFile_txt,1,wx.EXPAND|wx.ALL,5)
        proxySizer.Add(self.btnBrowseProxy,0,wx.ALL,5)

        threadSizer.Add(lblThread,0,wx.ALL,5)
        threadSizer.Add(self.thread_slider,1,wx.EXPAND,5)

        actionBtnSizer.Add(self.btnStart,0,wx.ALL,5)
        actionBtnSizer.Add(self.btnStop,0,wx.ALL,5)

        topSizer.Add(titleSixer,0,wx.CENTER,5)
        topSizer.Add((-1,10))
        topSizer.Add(urlSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(proxySizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(threadSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(actionBtnSizer,0,wx.CENTER,5)
        topSizer.Add((-1,10))

        self.SetSizer(topSizer)
        topSizer.Fit(self)


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
        url = self.urlFile_txt.GetValue().replace('\\','/')
        proxyFile = self.proxyFile_txt.GetValue().replace('\\','/')

        cm = ConnectionManager.ConnectionManager(proxyFile)
        self.datacontext = proxychecker.ProxyChecker(url, proxyFile, self.evt, self.thread_slider.GetValue())
        thread.start_new(self.datacontext.start, ())


    def stop(self, event):
        self.datacontext.stop()
        self.evt.onStop()



class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='Dai Submitter v1 Beta')

        #now create panel and notebook on panel
        p=wx.Panel(self)
        nb=wx.Notebook(p)

        first_tab = ProxyCheckerUI(nb)
        nb.AddPage(first_tab,"Proxy Checker")

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