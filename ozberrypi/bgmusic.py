import pygame, time
from queue import Empty

SONG_END = pygame.USEREVENT + 1
M_VOLUME = .05
N_VOLUME = .5

def playMusic(rqueue, squeue, file_list=[]):
    global filelist
    filelist = file_list
    pygame.mixer.init(22050, -16, 2, 4096*2)
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.set_volume(.5)
    play_next_song(squeue)
    pygame.init()
    q = None
    try:
        while True:
            try:
                q = rqueue.get(False)
                if q == 'MUTE:ON':
                    pygame.mixer.music.set_volume(M_VOLUME)
                elif q == 'MUTE:OFF':
                    pygame.mixer.music.set_volume(N_VOLUME)
                elif q == 'QUIT':
                    pygame.mixer.music.stop()
                    pygame.quit()
                    break
            except (Empty):
                pass
            for event in pygame.event.get():
                if event.type == SONG_END:
                    # print('song ended')
                    squeue.put('SONG:END')
                    play_next_song(squeue)
            time.sleep(.3)

    except (KeyboardInterrupt, SystemExit):
        raise
        
    pygame.quit()

def play_next_song(squeue):
    global filelist
    pygame.mixer.music.load(filelist[0]['filename'])
    filelist = filelist[1:] + [filelist[0]] # move current song to the back of the list 
    # print('starting bg music')
    pygame.mixer.music.play()
    squeue.put(str.join('SONG:START:', filelist[0]['filename']))