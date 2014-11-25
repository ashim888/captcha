class EventClass():
    def __init__(self,start_btn,stop_btn,prg_bar,txt_box):
        self.start_btn=start_btn
        self.stop_btn=stop_btn
        self.prg_bar=prg_bar
        self.txt_box=txt_box

    def onLogMessage(self,log):
        self.txt_box.AppendText(log+'\n')

    def onProgressChange(self,value):
        self.prg_bar.SetValue(value)

    def onStart(self):
        self.start_btn.Disable()
        self.stop_btn.Enable()
    def onStop(self):
        self.stop_btn.Disable()
        self.start_btn.Enable()


