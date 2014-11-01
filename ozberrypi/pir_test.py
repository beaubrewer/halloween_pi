#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# pir_2.py
# Measure the holding time of a PIR module
#
# Author : Matt Hawkins
# Date   : 20/02/2013

# Import required Python libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Define GPIO to use on Pi
GPIO_PIR = 7 #P7 on the cobbler
GPIO_FOG = 11 #P0 on the cobbler

print("PIR Module Holding Time Test (CTRL-C to exit)")

# Set pin as input
GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)      # Echo
GPIO.setup(GPIO_FOG, GPIO.OUT)

Current_State  = 0
Previous_State = 0

try:

  print("Waiting for PIR to settle ...")

  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0

  print("Ready")

  # Loop until users quits with CTRL-C
  while True :
    time.sleep(.1)
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      start_time = time.time()
      print("  Motion detected!")
      GPIO.output(GPIO_FOG, 1)
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      stop_time=time.time()
      print("  Ready "),
      elapsed_time=int(stop_time-start_time)
      print(" (Elapsed time : " + str(elapsed_time) + " secs)")
      GPIO.output(GPIO_FOG, 0)
      Previous_State=0

except KeyboardInterrupt:
  print("  Quit")
  # Reset GPIO settings
  GPIO.cleanup()