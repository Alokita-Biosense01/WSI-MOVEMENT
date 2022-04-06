import wx
from HomePanel import *

class MyFrame(wx.Frame):
    # main frame for all operations in hublite
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(900,800))
        self.currentPanel = HomePanel(self)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="Hublite")
        self.frame.Show()
        return True


app = MyApp()
app.MainLoop()