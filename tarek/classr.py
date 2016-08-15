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
STREAM = chr(148)       # Create only
QUERYLIST = chr(149)       # Create only
PAUSERESUME = chr(150)       # Create only

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
DISTANCE = 19
ANGLE = 20
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
	ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
		
	def _write(self,byte):
		self.ser.write(byte)
	
	def _start(self):
       		""" changes from OFF_MODE to PASSIVE_MODE """
        	self._write( START )
        	time.sleep(0.25)
        	return	
        
	def _safe(self):
       		self._write( SAFE )
        	time.sleep(0.25)
        	return	   

	def _clean(self):
        	self._write( CLEAN )
        	time.sleep(0.25)
        	return	  
