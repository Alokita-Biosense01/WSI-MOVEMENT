monolayer_region = {'width':3500,'height':3500,'match':0,'currentfocus':1, 'peak_fm':1000}
import threading
curr_position_mr = {'width':0,'height':0}
from motor_controller import *
dir_to_move = 1
def Patterncap_thred():
    print("Theradin 2")
    auto_thread = threading.Thread(target=Pattern_Cap, daemon=True)
    auto_thread.start()


def Pattern_Cap1():
    Step_size_x = 5000
    while True:

        if curr_position_mr['width'] <= monolayer_region['width']:
            _, ret = serialconn.motor_movement(XMove, Step_size_x, DirPlus)

        else:
            _, ret = serialconn.motor_movement(XMove, Step_size_y, DirPlus)



def Pattern_Cap():
    Step_size_y = 3500


    while True:

        global dir_to_move,stopbit, counter_
        # global intt, dir_to_move, motion,stopbit,p_clas,p_prob
        # ts = datetime.datetime.now()
        # intt_x=0
        # intt_y=0
        # p_clas = clas
        # p_prob = prob
        # dir_name = ts.strftime("%Y%m%d%H%M%S")
        # outpath = f'{IMAGES_BUFFER}/{dir_name}'
        # os.mkdir(outpath)
        # counter =

        if curr_position_mr['width'] <= monolayer_region['width']:  # or counter_w <= i_w:
            print("enter 1")
            ##get monolayer data

            #fm = live_feed_panel.Panel.FM['FM']
            fm = 0
            #prob, clas =  monolayer_detection(fm,  0)
            #val = prob_of_focussing(clas, prob, fm)
            val = 0

            if val == 0:  ##
                # print(int(ret))
                print("height: ", curr_position_mr['height'], monolayer_region['height'])
                print("width: ", curr_position_mr['width'], monolayer_region['width'])
                #snapshot(frame_)


                    #starttime = datetime.now()

                monolayer_region['currentfocus'] = 0
                if curr_position_mr['height'] >= monolayer_region['height']:  # or counter_h <= i_h:
                    #replace_image(self, 0)


                    if dir_to_move == 0:


                        _, ret = serialconn.motor_movement(XMove, Step_size_x,DirMinus)
                        print(ack(ret))
                        curr_position_mr['width'] += Step_size_x
                        # snapshot(frame)
                        dir_to_move = 1
                        curr_position_mr['height'] = 0


                        print('____________________________________x movem')
                        # plot_points.append((plot_points[-1][0] - w_fac,0))
                    else:
                        #time.sleep(0.1)
                        _, ret = serialconn.motor_movement(XMove, Step_size_x, DirMinus)
                        print(ack(ret))
                        curr_position_mr['width'] += Step_size_x
                        # snapshot()
                        # time.sleep(frame)
                        dir_to_move = 0
                        curr_position_mr['height'] = 0

                        print('________________________________x movem')

                        # plot_points.append((plot_points[-1][0] - w_fac,0))
                else:
                    print("Enter in Y")

                    _, ret = serialconn.motor_movement(YMove, Step_size_y, dir_to_move)


                    curr_position_mr['height'] += Step_size_y
                    print('_______________________________y movem')
                    # endtime = datetime.now()
                    # timing = calc_time(self.starttime, endtime)
                    # s, m, h = convertMillis(timing)
                    # message = f'images captured in {h}:{m}:{s} '
                    # print(message)
                    # # self.msg = wx.MessageDialog(self.panel_1, message, caption="Process Complete",
                    # #               style= wx.OK | wx.CENTRE)
                    # self.msg = wx.MessageBox(message, 'Complete', wx.OK)
                    # self.starttime = datetime.now()
                    if dir_to_move == 0:
                        pass


                    else:
                        pass


                    # plot_points.append(( 0 ,plot_points[-1][0] - h_fac))
            else:
                # move_limit_home(Stop)
                # automatic_focus(1)0
                monolayer_region['match'] += 1
                if monolayer_region['match'] == 5:
                    print('autofocusing .....')
                    #automatic_focus(1)
                    #AutoFocus_algo()
                    monolayer_region['currentfocus'] = 1
                    monolayer_region['match'] = 0
        else:
            break
            # endtime = datetime.now()
            # timing = calc_time(self.starttime, endtime)
            # s, m, h = convertMillis(timing)
            # message = f'{counter_} images captured in {h}:{m}:{s} '
            # print(message)
            # # self.msg = wx.MessageDialog(self.panel_1, message, caption="Process Complete",
            # #               style= wx.OK | wx.CENTRE)
            # self.msg = wx.MessageBox(message, 'Complete', wx.OK)