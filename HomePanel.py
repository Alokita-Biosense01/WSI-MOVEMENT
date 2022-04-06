import wx
import wx.lib.buttons as buts
import wx.lib.buttons as BitButton
from Autofocusing import *
from motor_controller import *


class HomePanel(wx.Panel):
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent, size  =(500,500))
        self.parent = parent
        self.SetBackgroundColour(wx.Colour(255,255,255))



        self.up_y = buts.GenBitmapTextButton(self, 100,
                                             bitmap=None, label='\u2191', size=(50, 100),
                                             style=2, pos=(150, 20))

        self.down_y = buts.GenBitmapTextButton(self, 101,
                                               bitmap=None, label='\u2193', size=(50, 100),
                                               style=2, pos=(150, 150))
        self.left_x = buts.GenBitmapTextButton(self, 102,
                                               bitmap=None, label='\u2190', size=(50, 100),
                                               style=2, pos=(100, 80))
        self.right_x = buts.GenBitmapTextButton(self, 103,
                                                bitmap=None, label='\u2192', size=(50, 100),
                                                style=2, pos=(200, 80))

        self.axis_label_z = wx.StaticText(self, wx.ID_ANY, "Z - Axis", style=wx.BU_LEFT,
                                          pos=(80, 250))

        self.up_z = buts.GenBitmapTextButton(self, 108,
                                             bitmap=None, label='\u2191', size=(50, 80),
                                             style=2, pos=(70, 280))

        self.down_z = buts.GenBitmapTextButton(self, 105,
                                               bitmap=None, label='\u2193', size=(50, 80),
                                               style=2, pos=(70, 360))

        self.axis_label_z_fine = wx.StaticText(self, wx.ID_ANY, "Z - Axis fine", style=wx.BU_LEFT,
                                               pos=(200, 250))

        self.axis_label_z_fine.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Roboto"))

        self.up_z_fine = buts.GenBitmapTextButton(self, 106,
                                                  bitmap=None, label='\u2191', size=(50, 80),
                                                  style=2, pos=(200, 280))

        self.down_z_fine = buts.GenBitmapTextButton(self, 107,
                                                    bitmap=None, label='\u2193', size=(50, 80),
                                                    style=2, pos=(200, 360))

        self.pattern_cap = buts.GenBitmapTextButton(self, 109,
                                                    bitmap=None, label='Pattern Capture', size=(100, 40),
                                                    style=2, pos=(300, 360))



        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.up_y)
        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.down_y)
        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.left_x)
        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.right_x)
        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.up_z)
        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.down_z)
        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.up_z_fine)
        self.Bind(wx.EVT_BUTTON, self.motor_communication, self.down_z_fine)
        self.Bind(wx.EVT_BUTTON, self.pattern, self.pattern_cap)

    def pattern(self, event):
        Patterncap_thred()


    def motor_communication(self, event):
        evtid = event.GetId()
        current_positions['x'] = serialconn.live_position(Xlive)
        current_positions['y'] = serialconn.live_position(Ylive)
        current_positions['z'] = serialconn.live_position(Zlive)
        print(f'current x position :{current_positions["x"]}')
        print(f'current y position :{current_positions["y"]}')
        ret = 0

        if evtid == 100:
            current_positions['y'], ret = serialconn.motor_movement(YMove, Step_size_y, DirMinus)

            # self.replace_image1(1)
            # print(self.Step_size_y)
            #
            # if snap['val'] == 1:
            #     self.replace_image2(1)
            #     snap['val'] = 0

            # replace_image(self, 3)

            # replace_image2(self, 3)
        elif evtid == 101:
            current_positions['y'], ret = serialconn.motor_movement(YMove, Step_size_y, DirPlus)
            #
            # # replace_image(self, 1)
            # self.replace_image1(3)
            # print(self.Step_size_y)
            #
            # if snap['val'] == 1:
            #     self.replace_image2(3)
            #     snap['val'] = 0
            #
            # # replace_image2(self, 1)
        elif evtid == 102:
            current_positions['x'], ret = serialconn.motor_movement(XMove, Step_size_x, DirMinus)
            # self.replace_image1(0)
            # print(self.Step_size_x)
            #
            # if snap['val'] == 1:
            #     self.replace_image2(0)
            #     snap['val'] = 0

            # replace_image(self, 2)
            # replace_image(self, 0)
            # replace_image2(self, 2)
        elif evtid == 103:
            current_positions['x'], ret = serialconn.motor_movement(XMove, Step_size_x, DirPlus)
            # print(self.Step_size_x)
            # self.replace_image1(2)
            # if snap['val'] == 1:
            #     self.replace_image2(2)
            #     snap['val'] = 0

            # replace_image(self, 0)
            # replace_image(self, 2)
            # replace_image2(self, 0)
        elif evtid == 108:
            print("Z UP AXISc")
            print(current_positions['z'])
            current_positions['z'], ret = serialconn.motor_movement(ZMove, Step_size_z, DirPlus)
        elif evtid == 105:

            print(current_positions['z'])
            current_positions['z'], ret = serialconn.motor_movement(ZMove, Step_size_z, DirMinus)
        elif evtid == 106:
            print(current_positions['z'])
            current_positions['z'], ret = serialconn.motor_movement(ZMove, Step_size_z_fine, DirPlus)
        elif evtid == 107:
            print(current_positions['z'])
            current_positions['z'], ret = serialconn.motor_movement(ZMove, Step_size_z_fine, DirMinus)
        else:
            pass

