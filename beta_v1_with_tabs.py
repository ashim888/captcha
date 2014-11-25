import wx , os, sys
import eventClass
import wx.richtext as rt
import  wx.lib.dialogs
import Executor
import DataManager
import ConnectionManager
import thread
import prcheckerui
import proxyharvesterui
import statuscheckerui
import googlescraperui

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        menuinstance=MenuBar(self)
        self.ex = None
        #Static Texts
        self.url=wx.StaticText(self,label='URL',pos=(20,35))
        self.name=wx.StaticText(self,label='Name File',pos=(20,88))
        self.msg=wx.StaticText(self,label='Message',pos=(20,135))
        self.email=wx.StaticText(self,label='Email',pos=(20,187))
        self.web=wx.StaticText(self,label='Website File',pos=(20,234))
        self.proxy=wx.StaticText(self,label='Proxy File',pos=(20,285))


        #TextBox
        self.url_txt=wx.TextCtrl(self,size=(400,30),pos=(90,30))
        self.name_txt=wx.TextCtrl(self,size=(400,30),pos=(90,80))
        self.msg_txt=wx.TextCtrl(self,size=(400,30),pos=(90,130))
        self.email_txt=wx.TextCtrl(self,size=(400,30),pos=(90,180))
        self.web_txt=wx.TextCtrl(self,size=(400,30),pos=(90,230))
        self.prox_txt=wx.TextCtrl(self,size=(400,30),pos=(90,280))

        #TextBox Bind with Events
        self.url_txt.Bind(wx.EVT_LEFT_DCLICK,self.url_fnc)
        self.name_txt.Bind(wx.EVT_LEFT_DCLICK,self.name_fnc)
        self.msg_txt.Bind(wx.EVT_LEFT_DCLICK,self.msg_fnc)
        self.email_txt.Bind(wx.EVT_LEFT_DCLICK,self.email_fnc)
        self.web_txt.Bind(wx.EVT_LEFT_DCLICK,self.web_fnc)
        self.prox_txt.Bind(wx.EVT_LEFT_DCLICK,self.prox_fnc)

        #Buttons
        url_browse=wx.Button(self,label='Browse',size=(55,30),pos=(500,30))
        name_browse=wx.Button(self,label='Browse',size=(55,30),pos=(500,80))
        msg_browse=wx.Button(self,label='Browse',size=(55,30),pos=(500,130))
        email_browse=wx.Button(self,label='Browse',size=(55,30),pos=(500,180))
        web_browse=wx.Button(self,label='Browse',size=(55,30),pos=(500,230))
        prox_browse=wx.Button(self,label='Browse',size=(55,30),pos=(500,280))

        #Button Bindings
        self.Bind(wx.EVT_BUTTON,self.url_fnc,url_browse)
        self.Bind(wx.EVT_BUTTON,self.name_fnc,name_browse)
        self.Bind(wx.EVT_BUTTON,self.msg_fnc,msg_browse)
        self.Bind(wx.EVT_BUTTON,self.email_fnc,email_browse)
        self.Bind(wx.EVT_BUTTON,self.web_fnc,web_browse)
        self.Bind(wx.EVT_BUTTON,self.prox_fnc,prox_browse)

        #Static lines
        self.lines=wx.StaticLine(self,style=wx.LI_HORIZONTAL,pos=(0,320),size=(600,3))

        self.lines=wx.StaticLine(self,style=wx.LI_HORIZONTAL,pos=(0,347),size=(600,3))


        ##main buttons function
        self.hit_btn=wx.Button(self,label='Start',size=(280,40),pos=(10,370))
        self.Bind(wx.EVT_BUTTON,self.mainStart,self.hit_btn)
        self.stop_btn=wx.Button(self,label='Stop',size=(280,40),pos=(300,370))
        self.Bind(wx.EVT_BUTTON,self.mainStop,self.stop_btn)


        #progress bar
        self.timer = wx.Timer(self)
        self.gauge = wx.Gauge(self, range=100, size=(580, 30),pos=(3,430))

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
        self.ex=Executor.Executor(urlFile,con,dm,self.evt)
        thread.start_new_thread(self.ex.execute,())




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
        self.txt_box=wx.TextCtrl(self,size=(580,450), style=wx.TE_MULTILINE)

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='Incog Dai v1 Beta',size=(650,560),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        #ICON
        ico = wx.Icon('edit.ico', wx.BITMAP_TYPE_ICO)
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
        statuschecker_tab = statuscheckerui.StatusCheckerUI(nb)
        googlescraper_tab = googlescraperui.GoogleScraperUI(nb)

        #Add pages to the notebook
        nb.AddPage(first_tab,'Guestbook Submitter')
        nb.AddPage(prchecker_tab,'PR Checker')
        nb.AddPage(proxyharvester_tab,'Proxy Harvester')
        nb.AddPage(statuschecker_tab,'Site Status Checker')
        nb.AddPage(googlescraper_tab,'Google Scraper')
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
    app=wx.App(True)
    app.SetOutputWindowAttributes(title="Log")
    MainFrame().Show()
    app.MainLoop()
