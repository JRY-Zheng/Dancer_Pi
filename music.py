import threading
import time
from os import sys
from display import *
from config import configs

flag = 0


class MusicPlayer(threading.Thread):
    """docstring for MusicPlayer"""
    def __init__(self, music_name):
        threading.Thread.__init__(self)
        self.music_name = music_name
        self.lyric_displayer = LyricDisplayer()
    def run(self):
        pass
    def play_music(music_name):
        title(music_name)
        info('playing song %s' % music_name)
        # play music
        lyric_displayer.print_lyric(music_name)


class LyricDisplayer():
    """docstring for LyricDisplayer"""
    def __init__(self):
        pass

    def print_lyric(music_name):
        pass
        
