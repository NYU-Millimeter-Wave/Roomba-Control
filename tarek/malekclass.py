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
STREAM_DIS_ANG = '\x94\x02\x13\x14'       # Create only
QUERYLIST = chr(149)       # Create only
PAUSE = '\x96\x00'       # Create only
RESUME= '\x96\x01'
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
ENCODER_LEFT = 43
ENCODER_RIGHT = 44
LIGHTBUMP = 45
LIGHTBUMP_LEFT = 46
LIGHTBUMP_FRONT_LEFT = 47
LIGHTBUMP_CENTER_LEFT = 48
LIGHTBUMP_CENTER_RIGHT = 49
LIGHTBUMP_FRONT_RIGHT = 50
LIGHTBUMP_RIGHT = 51

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
	out=0
	ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
        def _write(self,byte):
        	self.ser.write(byte)
        
        def _writearray(self,bytearray):
        	self.ser.write(bytearray)
        
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
	def htosi(self,val):
    		uintval = int(val,16)
    		bits = 4 * (len(val) - 2)
    		if uintval >= math.pow(2,bits-1):
        		uintval = int(0 - (math.pow(2,bits) - uintval))
    		return uintval

	def getSignedNumber(self,number, bitLength):
   		mask = pow(2,bitLength) - 1
   		if number & (1 << (bitLength - 1)):
        		return number | ~mask
    		else:
        		return number & mask

	def bytes2val(self,highbyte, lowbyte):
    		#ipdb.set_trace()
    		number = (highbyte<<8)+lowbyte
    		return self.getSignedNumber(number, 16)
     
	def tarek(self,highbyte, lowbyte):
		number = (highbyte*256) + lowbyte
		return self.getSignedNumber(number,16)

	def _stream(self):
            	#self.ser.flushInput()
		self._write( STREAM_DIS_ANG )
            	resp=self.ser.read(9)
                #print int(resp.encode('hex'), 16)
		if len(resp) <9 :
                    print("Warning: getSensorsAll only received %d bytes, not 6"%len(resp))
                    return None
		print len(resp)
            	self.out=dict()
		self.out['0']=int((resp[0]).encode('hex'), 16)
		print ('header : ' + str( self.out['0']))
		self.out['1']=int((resp[1]).encode('hex'), 16)
		print ('n-bytes ' + str(self.out['1']))  # mm
                self.out['2']=int((resp[2]).encode('hex'), 16)
		print ('dist : ' + str( self.out['2']))  # mm or degrees?
		#self.out['3']=int((resp[3]).encode('hex'), 16)
		self.out['distance']=self.bytes2val(ord(resp[3]),ord(resp[4])) 
		print ('dist1 : ' + str(self.out['distance']))  # mm
                #self.out['4']=self.htosi(str(resp[4]))
		#print ('dist2 : ' + str(self.out['4']))  # mm or degrees?
            	self.out['5']=int((resp[5]).encode('hex'), 16)	
		print ('angle : ' + str(self.out['5']))  # mm
		#self.out['6']=int((resp[6]).encode('hex'), 16)
		self.out['angle']=self.bytes2val(ord(resp[6]),ord(resp[7]))
		print ('angle1 : ' + str(self.out['angle']))
		#self.out['7']=int((resp[7]).encode('hex'), 16)
		#print ('angle2 : ' + str(self.out['7']))
		self.out['8']=int((resp[8]).encode('hex'), 16)
		print ('checksum : ' + str(self.out['8']))
		#self.out['9']=int((resp[9]).encode('hex'), 16)
            	#print (str(self.out['9']))
		#self.out['10']=int((resp[10]).encode('hex'), 16)
		#print (str(self.out['10']))
		#self.out['11']=int((resp[11]).encode('hex'), 16)
		#print (str(self.out['11']))
		#self.out['12']=int((resp[12]).encode('hex'), 16)
		return 
	
	def _sensors(self):
		#self.ser.flushInput()
		self._write( SENSORS )
		self._write( DISTANCE )
		resp=self.ser.read(3)
		#self._write( SENSORS )
		#self._write( DISTANCE )
		#resp1=self.ser.read(3)
		print('distance')
		print (int((resp[0]).encode('hex'), 16))		
		print (int((resp[1]).encode('hex'), 16))		
		print (int((resp[2]).encode('hex'), 16))		
		print (self.bytes2val(ord(resp[0]),ord(resp[1])))

		print (self.bytes2val(ord(resp[1]),ord(resp[2])))
		#print('angle')
		#print (int((resp1[0]).encode('hex'), 16))
		#print (self.bytes2val(ord(resp1[1]),ord(resp1[2])))
		return 

       # def _pausestream(self):
        	#self._write( PAUSE )
        	#return

        #def _resumestream(self):
        	#self._write( RESUME )
        	#return

	
