import pygame, time, sys
import RPi.GPIO as GPIO
from queue import Empty

GPIO_PIR = 7

VOLUME = 1
file_list = []
rq = None
sq = None

SFX_MIN_DELAY = 10
last_motion_time = time.time()

def init(squeue, rqueue, filelist):
    global file_list, sq, rq
    setup_PIR()
    sq = squeue
    rq = rqueue
    print('initial rq')
    print(rq)
    file_list = sorted(filelist, key=lambda sfx: sfx['position'])
    pygame.mixer.init(22050, -16, 2, 4096*2)
    main()

def setup_PIR():
    global current_state, previous_state
    # Set pin as input
    GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Waiting for PIR to settle ...")
    # Loop until PIR output is 0
    while GPIO.input(GPIO_PIR)==1:
        pass
    current_state  = 0
    previous_state = 0
    print("Ready")

def main():
    while True:
        check_rqueue()
        check_PIR()
        time.sleep(.1)
        
def check_rqueue():
    try:
        global rq
        #check the rqueue
        if not rq.empty():
            event = rq.get()
            # print('I got an event')
            # print(event)
            if event == 'SOUND:NEXT':
                play(getNext())
            elif event == 'QUIT':
                # print('I got a quit')
                pygame.quit()
                sys.exit(0)

    except KeyboardInterrupt:
        # print('got an except in check_rqueue')
        qygame.quit()
        sys.exit(0)


def check_PIR():
    global current_state, previous_state, last_motion_time
    current_state = GPIO.input(GPIO_PIR)
    if current_state==1 and previous_state==0:
        # motion was detected
        if (time.time() - last_motion_time) > SFX_MIN_DELAY:
            play()
        last_motion_time = time.time()
        previous_state=1
    elif current_state==0 and previous_state==1:
        # PIR has returned to ready state
        previous_state=0

def send(event):
  global sq
  sq.put(event)

def play(sound=None):
    if sound:
        playSound(sound['filename'], sound['cuepoints'])
    else:
        play(getNext())


def playSound(filename,cuepoints):
    #main loop
    # load a sound file into memory
    current_cuepoints = sorted(cuepoints, key=lambda cpoint: cpoint['time'])
    sound = pygame.mixer.Sound(filename)
    send('MUTE:ON')
    channel = sound.play()
    channel.set_volume(VOLUME)
    #store the current time
    start_time = time.time()
    send(':'.join(('SFXUPDATE',file_list[0]['filename'])))
    # print(''.join(('Playing the sound file: ',filename)))
    while channel.get_busy():
        if len(current_cuepoints):
            current_time_ms = (time.time() - start_time) * 1000
            # check for cue points
            if current_time_ms > current_cuepoints[0]['time']:
                send(current_cuepoints.pop(0)['type'])
        check_rqueue()
        time.sleep(.1)
    send('MUTE:OFF')

def getNext():
    global file_list
    next = file_list[0]
    file_list = file_list[1:] + [file_list[0]] # move current song to the back of the list 
    return next
