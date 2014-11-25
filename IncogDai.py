import wx , os, sys
import eventClass
import wx.richtext as rt
import wx.lib.dialogs
import Executor
import DataManager
import ConnectionManager
import thread
import prcheckerui
import proxyharvesterui
import statuscheckerui
import googlescraperui
import backlinkcheckerui
import proxycheckerui
import extractorui
import duplicateRemovalui

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        menuinstance=MenuBar(self)
        self.ex = None

        #Sizers
        topSizer = wx.BoxSizer(wx.VERTICAL)
        urlSizer = wx.BoxSizer(wx.HORIZONTAL)
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        emailSizer = wx.BoxSizer(wx.HORIZONTAL)
        messageSizer  = wx.BoxSizer(wx.HORIZONTAL)
        websiteSizer  = wx.BoxSizer(wx.HORIZONTAL)
        proxySizer  = wx.BoxSizer(wx.HORIZONTAL)
        threadSizer = wx.BoxSizer(wx.HORIZONTAL)

        #Static Texts
        self.url=wx.StaticText(self,label='URL',size=(80,30))
        urlSizer.Add(self.url,0,wx.ALL,5)
        self.name=wx.StaticText(self,label='Name File',size=(80,30))
        nameSizer.Add(self.name,0,wx.ALL,5)
        self.msg=wx.StaticText(self,label='Message',size=(80,30))
        messageSizer.Add(self.msg,0,wx.ALL,5)
        self.email=wx.StaticText(self,label='Email',size=(80,30))
        emailSizer.Add(self.email,0,wx.ALL,5)
        self.web=wx.StaticText(self,label='Website File',size=(80,30))
        websiteSizer.Add(self.web,0,wx.ALL,5)
        self.proxy=wx.StaticText(self,label='Proxy File',size=(80,30))
        proxySizer.Add(self.proxy,0,wx.ALL,5)
        lblThread = wx.StaticText(self, label='Number of threads',size=(80,30))
        threadSizer.Add(lblThread,0,wx.ALL,5)
        self.thread_slider = wx.Slider(self,value=5,minValue=1,maxValue=20, style=wx.SL_AUTOTICKS|wx.SL_LABELS)
        threadSizer.Add(self.thread_slider,1,wx.ALL|wx.EXPAND,5)

        #TextBox
        self.url_txt=wx.TextCtrl(self)
        urlSizer.Add(self.url_txt,1,wx.ALL|wx.EXPAND,5)
        self.name_txt=wx.TextCtrl(self)
        nameSizer.Add(self.name_txt,1,wx.ALL|wx.EXPAND,5)
        self.msg_txt=wx.TextCtrl(self)
        messageSizer.Add(self.msg_txt,1,wx.ALL|wx.EXPAND,5)
        self.email_txt=wx.TextCtrl(self)
        emailSizer.Add(self.email_txt,1,wx.ALL|wx.EXPAND,5)
        self.web_txt=wx.TextCtrl(self)
        websiteSizer.Add(self.web_txt,1,wx.ALL|wx.EXPAND,5)
        self.prox_txt=wx.TextCtrl(self)
        proxySizer.Add(self.prox_txt,1,wx.ALL|wx.EXPAND,5)

        #TextBox Bind with Events
        self.url_txt.Bind(wx.EVT_LEFT_DCLICK,self.url_fnc)
        self.name_txt.Bind(wx.EVT_LEFT_DCLICK,self.name_fnc)
        self.msg_txt.Bind(wx.EVT_LEFT_DCLICK,self.msg_fnc)
        self.email_txt.Bind(wx.EVT_LEFT_DCLICK,self.email_fnc)
        self.web_txt.Bind(wx.EVT_LEFT_DCLICK,self.web_fnc)
        self.prox_txt.Bind(wx.EVT_LEFT_DCLICK,self.prox_fnc)

        #Buttons
        url_browse=wx.Button(self,label='Browse')
        urlSizer.Add(url_browse,0,wx.ALL,5)
        name_browse=wx.Button(self,label='Browse')
        nameSizer.Add(name_browse,0,wx.ALL,5)
        msg_browse=wx.Button(self,label='Browse')
        messageSizer.Add(msg_browse,0,wx.ALL,5)
        email_browse=wx.Button(self,label='Browse')
        emailSizer.Add(email_browse,0,wx.ALL,5)
        web_browse=wx.Button(self,label='Browse')
        websiteSizer.Add(web_browse,0,wx.ALL,5)
        prox_browse=wx.Button(self,label='Browse')
        proxySizer.Add(prox_browse,0,wx.ALL,5)

        topSizer.Add(urlSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(nameSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(emailSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(messageSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(websiteSizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(proxySizer,0,wx.EXPAND,5)
        topSizer.Add((-1,10))
        topSizer.Add(threadSizer,0,wx.EXPAND,5)

        self.SetSizer(topSizer)
        topSizer.Fit(self)

        #Button Bindings
        self.Bind(wx.EVT_BUTTON,self.url_fnc,url_browse)
        self.Bind(wx.EVT_BUTTON,self.name_fnc,name_browse)
        self.Bind(wx.EVT_BUTTON,self.msg_fnc,msg_browse)
        self.Bind(wx.EVT_BUTTON,self.email_fnc,email_browse)
        self.Bind(wx.EVT_BUTTON,self.web_fnc,web_browse)
        self.Bind(wx.EVT_BUTTON,self.prox_fnc,prox_browse)


        #main buttons function
        self.hit_btn=wx.Button(self,label='Start',size=(280,40),pos=(40,370))
        self.Bind(wx.EVT_BUTTON,self.mainStart,self.hit_btn)
        self.stop_btn=wx.Button(self,label='Stop',size=(280,40),pos=(350,370))
        self.Bind(wx.EVT_BUTTON,self.mainStop,self.stop_btn)


        #progress bar
        self.timer = wx.Timer(self)
        self.gauge = wx.Gauge(self, range=100, size=(655, 30),pos=(5,430))

        self.evt=eventClass.EventClass(self.hit_btn,self.stop_btn,self.gauge,None)

    """FINISHED INIT"""
    def mainStart(self,event):

        urlFile_test=self.url_txt.GetValue()
        urlFile=urlFile_test.replace('\\','/')

        nameFile_test =self.name_txt.GetValue()
        nameFile=nameFile_test.replace('\\','/')


        emailFile_test =self.email_txt.GetValue()
        emailFile=emailFile_test.replace('\\','/')

        websiteFile_test =self.web_txt.GetValue()
        websiteFile=websiteFile_test.replace('\\','/')

        commentFile_test =self.msg_txt.GetValue()
        commentFile=commentFile_test.replace('\\','/')

        proxyFile_test=self.prox_txt.GetValue()
        proxyFile=proxyFile_test.replace('\\','/')

        dm=DataManager.DataManager(nameFile,emailFile,websiteFile,commentFile)
        con=ConnectionManager.ConnectionManager(proxyFile)
        self.ex=Executor.Executor(urlFile,con,dm,self.evt,self.thread_slider.GetValue())
        thread.start_new_thread(self.ex.start,())




    def mainStop(self,event):
        if self.ex:
            self.ex.stop()
        #FINAL HIT BUTTON And Stop button



    #METHODS THAT SHOULD BE BINDED
    def url_fnc(self, event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.url_txt.SetValue(f)
        dlg.Destroy()



    def name_fnc(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.name_txt.SetValue(f)
        dlg.Destroy()

    def msg_fnc(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.msg_txt.SetValue(f)
        dlg.Destroy()

    def email_fnc(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.email_txt.SetValue(f)
        dlg.Destroy()
    def web_fnc(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.web_txt.SetValue(f)
        dlg.Destroy()
    def prox_fnc(self,event):
        self.dirname=''
        dlg=wx.FileDialog(self,'Choose a File',self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            f=os.path.join(self.dirname,self.filename)
            self.prox_txt.SetValue(f)
        dlg.Destroy()

class MenuBar(wx.Frame):
    def __init__(self,f):
        self.frame=f


    def onExit(self,event):
        self.frame.Close()
    def onAboutClick(self,event):
        info = wx.AboutDialogInfo()
        info.AddDeveloper("Team Dai")
        info.SetCopyright("(C) 2013 Team Dai")
        info.SetDescription("Handy utilities for simplifying your SEO endeavours")
        info.SetName("Incog Dai")
        info.SetVersion("1 Beta")
        box = wx.AboutBox(info)


##END OF FIRST TAB

##START OF NEW TAB

class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.txt_box=wx.TextCtrl(self,size=(668,450), style=wx.TE_MULTILINE)

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='Incog Dai v1 Beta',size=(680,560),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        #ICON
        self.Center()
        ico = wx.Icon('app.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        menuinstance=MenuBar(self)
        #now create panel and notebook on panel
        p=wx.Panel(self)
        nb=wx.Notebook(p)

        #creating Page

        first_tab=PageOne(nb)
        second_tab=PageTwo(nb)

        prchecker_tab = prcheckerui.PrCheckerUI(nb)

        proxyharvester_tab = proxyharvesterui.ProxyHarvesterUI(nb)
        proxychecker_tab = proxycheckerui.ProxyCheckerUI(nb)
        statuschecker_tab = statuscheckerui.StatusCheckerUI(nb)
        googlescraper_tab = googlescraperui.GoogleScraperUI(nb)
        backlinkchecker_tab = backlinkcheckerui.BacklinkCheckerUI(nb)
        extractor_tab = extractorui.ExtractorUI(nb)
        dupremover_tab = duplicateRemovalui.DuplicateRemovalUI(nb)
        #Add pages to the notebook
        nb.AddPage(first_tab,'Guestbook Submitter')
        nb.AddPage(prchecker_tab,'PR Checker')
        nb.AddPage(proxyharvester_tab,'Proxy Harvester')
        nb.AddPage(proxychecker_tab,'Proxy Checker')
        nb.AddPage(statuschecker_tab,'Site Status Checker')
        nb.AddPage(googlescraper_tab,'Google Scraper')
        nb.AddPage(backlinkchecker_tab,'Backlink Checker')
        nb.AddPage(extractor_tab,'Url/Email Scraper')
        nb.AddPage(dupremover_tab,'Duplicate Remover')
        nb.AddPage(second_tab,'Logs')


        #put notebook in sizer for managing the layout
        sizer=wx.BoxSizer()
        sizer.Add(nb,1,wx.EXPAND)
        p.SetSizer(sizer)
        #STATUS BAR AND MENUBAR
        statusbar= self.CreateStatusBar()
        menubar=wx.MenuBar()

        first=wx.Menu()

        about_menu=first.Append(wx.NewId(),'About','About the software and the developers')
        exit_menu=first.Append(wx.NewId(),'Exit','Will Exit')


        menubar.Append(first,"File")
        self.Bind(wx.EVT_MENU,menuinstance.onAboutClick,about_menu)
        self.Bind(wx.EVT_MENU,menuinstance.onExit,exit_menu)

        self.SetMenuBar(menubar)

        first_tab.evt.txt_box=second_tab.txt_box

        #Redirect std out and err
        redir = RedirectText(second_tab.txt_box)
        sys.stdout = redir
        sys.stderr = redir



if __name__=='__main__':
    app=wx.App(False)
    app.SetOutputWindowAttributes(title="Log")
    MainFrame().Show()
    app.MainLoop()
