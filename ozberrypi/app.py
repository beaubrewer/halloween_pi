import os, sys, time
import json
import bgmusic, soundfx
import argparse
import webcontrol
from multiprocessing import Process, Queue
import fogcontrol as fog

def parseJSON(url):
  with open(url) as f:
    js = json.load(f)
  return js


def init_config(config):
  bg_music = config['background_music']
  fg_sounds = config['foreground_sounds']
  return (bg_music, fg_sounds)


def parse_event(event):
  # print(''.join(('Parsing event: '+event)))
  cls, method = event.lower().split(':')
  execute_method(cls, method)


def main(config_url):
  global fgsounds_rqueue
  bg_music_files, fg_sound_files = init_config(parseJSON(config_url))
  bgmusic_squeue = Queue()
  bgmusic_rqueue = Queue()
  bgprocess = Process(target=bgmusic.playMusic,args=(bgmusic_squeue, bgmusic_rqueue, bg_music_files,))
  bgprocess.daemon=True
  bgprocess.start()
  
  fgsounds_rqueue = Queue()
  fgsounds_squeue = Queue()
  fgprocess = Process(target=soundfx.init, args=(fgsounds_rqueue, fgsounds_squeue, fg_sound_files))
  fgprocess.daemon=True
  fgprocess.start()

  # start web application
  web_squeue = Queue()
  web_rqueue = Queue()
  webprocess = Process(target=webcontrol.startup, args=(web_squeue, web_rqueue))
  webprocess.daemon=True
  webprocess.start();

  try:
    while True:
      time.sleep(.02)
      if not web_rqueue.empty():
        parse_event(web_rqueue.get())
      if not  fgsounds_rqueue.empty():
        event = fgsounds_rqueue.get()
        event_category = event.lower().split(':')[0]
        if event_category == 'mute':
          bgmusic_squeue.put(event)
        elif event_category == 'sfxupdate':
          web_squeue.put(event)
        else:
          parse_event(event)

  except KeyboardInterrupt:
    fog.cleanup();
    web_squeue.put('QUIT')
    fgsounds_squeue.put('QUIT')
    bgprocess.join()
    fgprocess.join()
    webprocess.join()
    time.sleep(10)


def execute_method(class_name, method_name):
  # print(''.join(('executing ',class_name,'.',method_name)))
  cls = getattr(sys.modules[__name__], class_name)
  if cls:
    getattr(cls, method_name)()


if __name__ == '__main__':
  parse = argparse.ArgumentParser(description="Halloween Theatre")
  parse.add_argument('--config', required=False, default='config.json')
  args = parse.parse_args();
  main(args.config)
