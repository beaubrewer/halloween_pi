import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Define GPIO to use on Pi
GPIO_PIR = 7 #P7 on the cobbler
GPIO_FOG = 11 #P0 on the cobbler


GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)      # Echo
GPIO.setup(GPIO_FOG, GPIO.OUT)

GPIO.output(GPIO_FOG, 0)

def start():
	GPIO.output(GPIO_FOG, 1)

def end():
	GPIO.output(GPIO_FOG, 0)

def cleanup():
	# print('calling cleanup on fogcontrol')
	GPIO.cleanup()