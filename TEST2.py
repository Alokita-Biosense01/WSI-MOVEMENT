import wx

class Test2(wx.Panel):
    def __init__(self, parent):
        super(Test2, self).__init__(parent, size  =(500,500))
        self.parent =parent
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.button = wx.Button(self, wx.ID_ANY, "start", pos = (230,230))
        self.Bind(wx.EVT_BUTTON, self.DestroyPanel)
    def DestroyPanel(self, event):
        self.parent.mainTest2()
