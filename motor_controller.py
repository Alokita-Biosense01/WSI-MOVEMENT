import serial
import serial.tools.list_ports as port_list
import signal
from contextlib import contextmanager
#from pubsub import pub

import threading
try:
    ports = list(port_list.comports())
    total_coms = []
    for p in ports:
        total_ports = dict(zip(p,ports))
        print(total_ports)
        for i in total_ports.keys():
            if len(i) <= 5:
                total_coms.append(i)
    print(total_coms)
except:
    pass

current_positions = {'x':None,'y':None,'z':None}

# device = 'COM16'
device_settings = {'com':total_coms[-1],'cam':None}
# device_settings = {'com':total_coms[0],'cam':None}
Device = 100
DeviceAck = 50
XMove = 101
# Limit = 40
YMove = 111
ZMove = 121
OkAck = 10
DirPlus = 1       #left #up
DirMinus = 0      #right #down
motor_direction = 0
MoveCompleted = 170
X_home_reached = 84
X_far_reached = 85
Y_home_reached = 86
Y_far_reached = 87
Z_home_reached = 88
Z_far_reached = 89
ackok = 10
acknowledgement = {ackok:"Sucess",MoveCompleted:"Movement Completed",X_home_reached:"X Axis Home", X_far_reached:"X Axis Far",Y_home_reached:"Y Axis Home", Y_far_reached:"Y Axis Far",Z_home_reached:"Z Axis Home", Z_far_reached:"Z Axis Far", 0:""}
Stop = 131
AdcRead = 30
#Step_size_x = 686
#Step_size_y = 372
# Step_size_x = 530
# Step_size_y = 330
Step_size_x = 280
Step_size_y = 180
Step_size_z = 50
Step_size_z_fine = 3
# dynamic_step_size = 150
# // AdcReadAck = 131,
#
# // X_MOVEFULL = 120,
#-
# // Y_MOVEFULL = 121,
#
# // Z_MOVEFULL = 122,
MotorSpeedXy =81
Led1 = 82
Led2 = 91
XFar = 67
YFar = 68
ZFar = 69
XHome = 70
YHome = 71
ZHome = 72
MotorSpeedZ = 92
br = 9600
pos = None
Zlive = 52
Xlive = 54
Ylive = 56
Led2off = 93
Dcheck =100

@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)
    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError
def ack(ret):
    ack_var = acknowledgement[ret]
    return ack_var

class SerialCommunication:
    # device_settings = {'com': total_coms[-1], 'cam': None}
    def __init__(self,pos):
        #pub.subscribe(self.communicationHandler, communication.communication.motorControl)
        self.test = serial.Serial(
            # port=device,
            port=pos,
            baudrate=br,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        # try:
        #     self.test.open()
        # except:
        #     pass
        self.test.flushInput()
        self.test.flushOutput()
        print("Com:",pos)


    def Close(self):
        self.test.close()
    def MsbCsbLsb(self,data):
        print(self.test)
        value = int(data)
        outlsb = bytearray([(value % 65536) % 256])
        outcsb = bytearray([int((value % 65536) / 256)])
        outmsb = bytearray([int(value / 65536)])
        return outmsb,outcsb,outlsb

    def toint(self,arr):
        i = bytearray(arr)
        h = int.from_bytes(i, byteorder='big')
        return h

    def motor_movement(self,axis, data, dir):
        #print("motor_movement = ",axis,data,dir )
        global motor_direction
        msb, csb, lsb = self.MsbCsbLsb(data)
        val = 10
        move = [bytearray([axis]), msb, csb, lsb, bytearray([dir])]  # 0.5 mm 1 = left , 0 = right

        response = 0
        e_pos = 0

        for i in move:
          #print("The I value = ", i)
          self.test.write(i)
          response = self.test.read()
        #print("read data ack : ", int(response.hex(), 16))
          self.test.flushInput()
          self.test.flushOutput()

        # print("write data : ", ord(i))
        # time.sleep(0.5)

          ret = int(response.hex(), 16)
        if axis == ZMove:
            e_pos = self.live_position(Zlive)
        # if axis == XMove:
        #     e_pos = self.live_position(Xlive)
        # if axis == YMove:
        #     e_pos = self.live_position(Ylive)
        motor_direction = dir
        return e_pos,ret

    def single_instruction(self,destination):
        self.test.write(bytearray([destination]))
        with timeout(5):
            response = self.test.read()
            #print("read data ack : ", ret)
            self.test.flushInput()
            self.test.flushOutput()
            #print('-' * 20)
            ret = int(response.hex(), 16)
            return ret
    def limit_home(self,destination):
        self.test.write(bytearray([destination]))
        response = self.test.read()
        #print("read data ack : ", ret)
        self.test.flushInput()
        self.test.flushOutput()
        #print('-' * 20)
        ret = int(response.hex(), 16)
        return ret

    def speed_(self,axis,val):
        speed = [bytearray([axis]),bytearray([val])]
        response = 0
        for i in speed:
            self.test.write(i)
            #print("write data : ", ord(i))
            # time.sleep(0.5)
            response = self.test.read()
            #print("read data ack : ", int(response.hex(), 16))
            self.test.flushInput()
            self.test.flushOutput()
        ret = int(response.hex(), 16)
        return ret

    def led_control(self,led,val):
        intensity = [bytearray([led]),bytearray([val])]
        response = 0
        for i in intensity:
            self.test.write(i)
            # print("write data : ", ord(i))
            # time.sleep(2)
        response = self.test.read()
        # print("read data ack : ", int(response.hex(), 16))
        self.test.flushInput()
        self.test.flushOutput()
        ret = int(response.hex(), 16)
        return ret

    def live_position(self,destination):
        self.test.write(bytearray([destination]))
        # print("write data : ", destination)
        # time.sleep(0.5)
        arr = []
        while len(arr) != 3:
            response = self.test.read()
            ret = int(response.hex(), 16)
            arr.append(ret)
        val = self.toint(arr)
        self.test.flushInput()
        self.test.flushOutput()
        print('-' * 20)
        return (val / 3.2)

    def rel_position(self,axis,dir,data,ret):
        global sw_pos,el_pos
        el_pos = self.live_position(Zlive)
        if dir == DirMinus:
            if ret == 89:
                sw_pos = el_pos
            else:
                sw_pos = abs(sw_pos + data)
        else:
            if ret == 88:
                sw_pos = 0
            else:
                sw_pos = abs(sw_pos - data)
# def MsbCsbLsb(self,data):
#     print(self.test)
#     value = int(data)
#     outlsb = bytearray([(value % 65536) % 256])
#     outcsb = bytearray([int((value % 65536) / 256)])
#     outmsb = bytearray([int(value / 65536)])
#     return outmsb,outcsb,outlsb
# def motor_movement(axis, data, dir):
#     msb, csb, lsb = MsbCsbLsb(data)
#     move = [bytearray([axis]), msb, csb, lsb, bytearray([dir])]  # 0.5 mm 1 = left , 0 = right
#     response = 0
#     e_pos = 0
#     for i in move:
#       port.write(i)
#       #print("write data : ", ord(i))
#       # time.sleep(0.5)
#       response = port.read()
#       #print("read data ack : ", int(response.hex(), 16))
#       port.flushInput()
#       port.flushOutput()
#     ret = int(response.hex(), 16)
#     # if axis == ZMove:
#         # e_pos = self.live_position(Zlive)
#     # if axis == XMove:
#     #     e_pos = self.live_position(Xlive)
#     # if axis == YMove:
#     #     e_pos = self.live_position(Ylive)
#     return e_pos,ret
serialconn = SerialCommunication(device_settings['com'])
'''
Calling Class
device = SerialCommunication(pos)
print(device.test)
'''
