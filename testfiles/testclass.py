import time
import math
import serial
# some module-level definitions for the robot commands
START = chr(128)    # already converted to bytes...
BAUD = chr(129)     # + 1 byte
CONTROL = chr(130)  # deprecated for Create
SAFE = chr(131)
FULL = chr(132)
POWER = chr(133)
SPOT = chr(134)     # Same for the Roomba and Create
CLEAN = chr(135)    # Clean button - Roomba
COVER = chr(135)    # Cover demo - Create
MAX = chr(136)      # Roomba
DEMO = chr(136)     # Create
DRIVE = chr(137)    # + 4 bytes
MOTORS = chr(138)   # + 1 byte
LEDS = chr(139)     # + 3 bytes
SONG = chr(140)     # + 2N+2 bytes, where N is the number of notes
PLAY = chr(141)     # + 1 byte
SENSORS = chr(142)  # + 1 byte
FORCESEEKINGDOCK = chr(143)  # same on Roomba and Create
# the above command is called "Cover and Dock" on the Create
DRIVEDIRECT = chr(145)       # Create only
STREAM=chr(148)
#STREAM_DIS_ANG = [chr(148), chr(2) ,chr(19), chr (20)]       # Create only
QUERYLIST = chr(149)       # Create only
PAUSERESUME = chr (150)
#PAUSE = chr(150 0)       # Create only
#RESUME= chr(150 1)
#### Sean

SCRIPT = chr(152)
ENDSCRIPT = chr(153)
WAITDIST = chr(156)
WAITANGLE = chr(157)

# the four SCI modes
# the code will try to keep track of which mode the system is in,
# but this might not be 100% trivial...
OFF_MODE = 0
PASSIVE_MODE = 1
SAFE_MODE = 2
FULL_MODE = 3

# the sensors
BUMPS_AND_WHEEL_DROPS = 7
WALL_IR_SENSOR = 8
CLIFF_LEFT = 9
CLIFF_FRONT_LEFT = 10
CLIFF_FRONT_RIGHT = 11
CLIFF_RIGHT = 12
VIRTUAL_WALL = 13
LSD_AND_OVERCURRENTS = 14
DIRT_DETECTED = 15
INFRARED_BYTE = 17
BUTTONS = 18
DISTANCE = chr(19)
ANGLE = chr(20)
CHARGING_STATE = 21
VOLTAGE = 22
CURRENT = 23
BATTERY_TEMP = 24
BATTERY_CHARGE = 25
BATTERY_CAPACITY = 26
WALL_SIGNAL = 27
CLIFF_LEFT_SIGNAL = 28
CLIFF_FRONT_LEFT_SIGNAL = 29
CLIFF_FRONT_RIGHT_SIGNAL = 30
CLIFF_RIGHT_SIGNAL = 31
CARGO_BAY_DIGITAL_INPUTS = 32
CARGO_BAY_ANALOG_SIGNAL = 33
CHARGING_SOURCES_AVAILABLE = 34
OI_MODE = 35
SONG_NUMBER = 36
SONG_PLAYING = 37
NUM_STREAM_PACKETS = 38
REQUESTED_VELOCITY = 39
REQUESTED_RADIUS = 40
REQUESTED_RIGHT_VELOCITY = 41
REQUESTED_LEFT_VELOCITY = 42
ENCODER_LEFT = chr(43)
ENCODER_RIGHT = chr(44)
LIGHTBUMP = 45
LIGHTBUMP_LEFT = 46
LIGHTBUMP_FRONT_LEFT = 47
LIGHTBUMP_CENTER_LEFT = 48
LIGHTBUMP_CENTER_RIGHT = 49
LIGHTBUMP_FRONT_RIGHT = 50
LIGHTBUMP_RIGHT = 51
STASIS = chr(58)

# others just for easy access to particular parts of the data
POSE = 100
LEFT_BUMP = 101
RIGHT_BUMP = 102
LEFT_WHEEL_DROP = 103
RIGHT_WHEEL_DROP = 104
CENTER_WHEEL_DROP = 105
LEFT_WHEEL_OVERCURRENT = 106
RIGHT_WHEEL_OVERCURRENT = 107
ADVANCE_BUTTON = 108
PLAY_BUTTON = 109

#                    0 1 2 3 4 5 6 7 8 9101112131415161718192021222324252627282930313233343536373839404142434445464748495051
SENSOR_DATA_WIDTH = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,2,2,1,2,2,2,2,2,2,2,1,2,1,1,1,1,1,2,2,2,2,2,2,1,2,2,2,2,2,2]

#The original value was 258.0 but my roomba has 235.0
WHEEL_SPAN = 235.0
WHEEL_DIAMETER = 72.0
TICK_PER_REVOLUTION = 508.8 # original 508.8
TICK_PER_MM = TICK_PER_REVOLUTION/(math.pi*WHEEL_DIAMETER)

# on my floor, a full turn is measured as sth like 450 deg
# add an error to the computation to account for that.
ANGULAR_ERROR = 360.0/450.0

class Roomba:
    ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
    def _write(self,byte):
        self.ser.write(byte)
    
    def _start(self):
        self._write( START )
        # they recommend 20 ms between mode-changing commands
        time.sleep(0.25)
        # change the mode we think we're in...
        return
    
    def _safe(self):
        self._write( SAFE )
        time.sleep(0.25)
        return
    
    def _clean(self):
        self._write( CLEAN )
        time.sleep(0.25)
        return

    def getUnsignedNumber(self,number, bitLength):
        mask = pow(2,bitLength) - 1
        return number & mask
    
    def getSignedNumber(self,number, bitLength):
        mask = pow(2,bitLength) - 1
        if number & (1 << (bitLength - 1)):
            return number | ~mask
        else:
            return number & mask
    
    def bytes2valunsigned(self,highbyte, lowbyte):
        #ipdb.set_trace()
        number = (highbyte<<8)+lowbyte
        return self.getUnsignedNumber(number,16)
    
    def bytes2val(self,highbyte, lowbyte):
        #ipdb.set_trace()
        number = (highbyte<<8)+lowbyte
        return self.getSignedNumber(number,16)
    
    def _sensorstasis(self):
        self._write( SENSORS )
        self._write( STASIS)
        resp2=self.ser.read(1)
        s=(int((resp2).encode('hex'), 16))
        #print ('stasis='+str(s))
        return s
            
    def _sensors(self):
        self._write( SENSORS )
        self._write( DISTANCE )
        resp=self.ser.read(2)
        self._write( SENSORS )
        self._write( ANGLE )
        resp1=self.ser.read(2)
        d=self.bytes2val(ord(resp[0]),ord(resp[1]))
        print ('distance='+str(d))
        a=self.bytes2val(ord(resp1[0]),ord(resp1[1]))
        print ('angle='+str(a))
        return d,a

    def _sensEncoders(self):
        self._write( SENSORS )
        self._write( ENCODER_LEFT  )
        resp=self.ser.read(2)
        self._write( SENSORS )
        self._write( ENCODER_RIGHT )
        resp1=self.ser.read(2)
        #print (int((resp).encode('hex'), 16))
        #print (int((resp1).encode('hex'), 16))
        left=self.bytes2valunsigned(ord(resp[0]),ord(resp[1]))
        #print ('left='+str(left))
        right=self.bytes2valunsigned(ord(resp1[0]),ord(resp1[1]))
        #print ('right='+str(right))
        #diff = right-left
        #print ('diff =' +str(diff))
        #distr= (right*72*math.pi/508.8)
        #distl= (left*72*math.pi/508.8)
        #angle= (distr-distl)/258.8
        ##angle = ((diff*72*math.pi/508.8)/235)
        #print ('angle =' +str(angle))
        return left,right

    def _dataCalc(self):
        old_left,old_right =self._sensEncoders()
        time.sleep(0.8)
        #print ('old_left='+str(old_left))
        #print ('old_right='+str(old_right))
        cur_left,cur_right = self._sensEncoders()
        #print ('cur_left='+str(cur_left))
        #print ('cur_right='+str(cur_right))
        left = cur_left - old_left
        right = cur_right - old_right
        #print ('left='+str(left))
        #print ('right='+str(right))
        diff = right-left
        #print ('diff =' +str(diff))
        distr= (right*72*math.pi/508.8)
        distl= (left*72*math.pi/508.8)
        #print ('distl =' +str(distl))
        #print ('distr =' +str(distr))
        angle= ((distr-distl)*360)/(258.8*math.pi)
        print ('angle =' +str(angle))

        ''' if (angle>0):
                angleInterp = angle-90
        else:
                angleInterp = angle+90 

        print ('angleInterp = '+str(angleInterp))'''
	
    def toHex(self, value):
        """ returns two bytes (ints) in high, low order
        whose bits form the input value when interpreted in
        two's complement
        """
        if value >= 0:
            eqBitVal = value
        else:
            eqBitVal = (1<<16) + value

        return ( (eqBitVal >> 8) & 0xFF, eqBitVal & 0xFF )

    def forward(self):
        (vel_high, vel_low) = self.toHex(50)
        (radius_high, radius_low) = self.toHex(0)
        self._write( chr(137) )
        self._write( chr(vel_high) )
        self._write( chr(vel_low) )
        self._write( chr(radius_high) )
        self._write( chr(radius_low) )
        #time.sleep(0.25)
        return

