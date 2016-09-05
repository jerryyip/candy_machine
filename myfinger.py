#coding=utf-8
import time, sys, signal, atexit
import pyupm_zfm20 as upmZfm20
import myoled

# Instantiate a ZFM20 Fingerprint reader on UART 1
myFingerprintSensor = upmZfm20.ZFM20(1)

## Exit handlers ##
# This stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
	raise SystemExit

# This function lets you run code on exit,
# including functions from myFingerprintSensor
def exitHandler():
	print "Exiting"
	sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

# make sure port is initialized properly.  57600 baud is the default.
if (not myFingerprintSensor.setupTty(upmZfm20.cvar.int_B57600)):
	print "Failed to setup tty port parameters"
	sys.exit(1)


# This example demonstrates registering a fingerprint on the zfm20
# module.  The procedure is as follows:
#
# 1. get an image, store it in characteristics buffer 1
# 2. get another image, store it in characteristics buffer 2
# 3. store the image, assuming the two fingerprints match

# first, we need to register our address and password

myFingerprintSensor.setPassword(upmZfm20.ZFM20_DEFAULT_PASSWORD)
myFingerprintSensor.setAddress(upmZfm20.ZFM20_DEFAULT_ADDRESS)

# now verify the password.  If this fails, any other commands
# will be ignored, so we just bail.
if (myFingerprintSensor.verifyPassword()):
	print "Password verified."
else:
	print "Password verification failed."
	sys.exit(1)

# how many valid stored templates (fingerprints) do we have?
print "Total stored templates: %d" % myFingerprintSensor.getNumTemplates()
print " "

def store_finger(number):
	print "Place a finger on the sensor."
	myoled.myLCD.clear()
	myoled.myLCD.setCursor(0,0)
	myoled.myLCD.write("Place finger")
	
	for i in range(20):
		if (myFingerprintSensor.generateImage() != upmZfm20.ZFM20.ERR_OK):
			time.sleep(0.2)
		else:
			break
		if (i == 19):
			return "ERROR"
	#while (myFingerprintSensor.generateImage() != upmZfm20.ZFM20.ERR_OK):
		#pass

# in theory, we have an image
	print "Image captured, converting..."
	rv = myFingerprintSensor.image2Tz(1)
	if (rv != upmZfm20.ZFM20.ERR_OK):
		print "Image conversion failed with error code %d" % rv
		#sys.exit(1)
		return "ERROR"

	print "Image conversion succeeded, remove finger."
	myoled.myLCD.setCursor(2,0)
	myoled.myLCD.write("Remove finger")
	time.sleep(0.5)
	
	for i in range(10):
		if (myFingerprintSensor.generateImage() != upmZfm20.ZFM20.ERR_NO_FINGER):
			time.sleep(0.5)
		else:
			break
		if (i == 9):
			return "ERROR"
	#while (myFingerprintSensor.generateImage() != upmZfm20.ZFM20.ERR_NO_FINGER):
	#	pass
	print "Now place the same finger on the sensor."
	myoled.myLCD.setCursor(4,0)
	myoled.myLCD.write("Same finger")	

	for i in range(10):
		if (myFingerprintSensor.generateImage() != upmZfm20.ZFM20.ERR_OK):
			time.sleep(0.5)
		else:
			break
		if (i == 9):
			return "ERROR"	
	#while (myFingerprintSensor.generateImage() == upmZfm20.ZFM20.ERR_NO_FINGER):
	#	pass
	print "Image captured, converting..."

	# save this one in slot 2
	rv = myFingerprintSensor.image2Tz(2)
	if (rv != upmZfm20.ZFM20.ERR_OK):
		print "Image conversion failed with error code %d" % rv
		#sys.exit(1)
		return "ERROR"

	print "Image conversion succeeded, remove finger."
	print "Storing fingerprint"
	myoled.myLCD.setCursor(6,0)
	myoled.myLCD.write("Storing...")	
# create the model
	rv = myFingerprintSensor.createModel()
	if (rv != upmZfm20.ZFM20.ERR_OK):
		if (rv == upmZfm20.ZFM20.ERR_FP_ENROLLMISMATCH):
			print "Fingerprints did not match."
		else:
			print "createModel failed with error code %d" % rv
		#sys.exit(1)
		myoled.myLCD.setCursor(7,0)
		myoled.myLCD.write("Fail!!!")
		return "ERROR"

# now store it, we hard code the id (second arg) to 1 here
	rv = myFingerprintSensor.storeModel(1, number)
	if (rv != upmZfm20.ZFM20.ERR_OK):
		print "storeModel failed with error code %d" % rv
		#sys.exit(1)
		return "ERROR"
	print "Fingerprint stored at id %d." % number
	myoled.myLCD.setCursor(7,0)
	myoled.myLCD.write("Success,NO:%d" % number)
	return "SUCCESS"
	
	
def check_finger():
	print "Waiting for finger print..."
	for i in range(6):
		if (myFingerprintSensor.generateImage() == upmZfm20.ZFM20.ERR_NO_FINGER):
			time.sleep(0.5)
		else:
			break
		if (i == 5):
			return "ERROR"
#	while (myFingerprintSensor.generateImage() == upmZfm20.ZFM20.ERR_NO_FINGER):
#		pass
	print "Image captured, converting..."
	rv = myFingerprintSensor.image2Tz(1)
	if (rv != upmZfm20.ZFM20.ERR_OK):
		print "Image conversion failed with error code %d" % rv
		#sys.exit(1)
		return "ERROR"
	
	print "Image conversion succeeded."
	print "Searching database..."
	
	myid = upmZfm20.uint16Array(0)
	myid.__setitem__(0, 0)
	myscore = upmZfm20.uint16Array(0)
	myscore.__setitem__(0, 0)
	
	# we search for a print matching slot 1, where we stored our last
	# converted fingerprint
	rv = myFingerprintSensor.search(1, myid, myscore)
	if (rv != upmZfm20.ZFM20.ERR_OK):
		if (rv == upmZfm20.ZFM20.ERR_FP_NOTFOUND):
			print "Finger Print not found"
			#sys.exit(0)
			return "NoThisFinger"
		else:
			print "Search failed with error code %d" % rv
			#sys.exit(1)
			return "ERROR"
	
	#print "Fingerprint found!"
	#print "ID: %d, Score: %d" % (myid.__getitem__(0), myscore.__getitem__(0))
	return myid.__getitem__(0)



if __name__ == "__main__":
	print(store_finger(3))
