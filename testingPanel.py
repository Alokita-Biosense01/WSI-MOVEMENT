import wx



class TestPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        super(TestPanel, self).__init__(parent, size  =(900,800))

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.staticbitmap = wx.StaticBitmap(self,pos = (50,0))

        self.browse = wx.Button(self, label='Browse', pos = (300,600))
        self.browse.Bind(wx.EVT_BUTTON, self.OnBrowse)

        self.ImageEnhancement  = wx.Button(self, label='enhancement ', pos = (400,600))
        self.ImageEnhancement.Bind(wx.EVT_BUTTON, self.OnEnhancement)

    def OnEnhancement(self, event):
        print("Write Image enhancement code")

    def OnBrowse(self, event):
        wildcard = 'PNG files (*.png)|*.png|BMP files (*.bmp)|*.bmp|JPEG files (*.jpg)|*.jpg'
        openFileDialog = wx.FileDialog(self, "Open", "", "", wildcard,
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        url = openFileDialog.GetPath()
        modification_bitmap1 = wx.Bitmap(url)
        modification_image1 = modification_bitmap1.ConvertToImage()
        modification_image1 = modification_image1.Scale(650, 490, wx.IMAGE_QUALITY_HIGH)
        self.staticbitmap.SetBitmap(wx.Bitmap(modification_image1))




