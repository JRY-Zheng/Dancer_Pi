import threading
from display import *
from music import *
from config import configs

music_player = MusicPlayer('Lost star')

init_screen(configs.user, configs.version, configs.server)
music_player.start()
# handle command
music_player.join()
print ('Bye!')
