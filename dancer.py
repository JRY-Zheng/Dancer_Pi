import threading
from display import *
from music import *
from config import configs
from handler import handle

music_player = MusicPlayer()

init_screen(configs.user, configs.version, configs.server)
play = threading.Thread(target=music_player.run_player, name='play music')
play.start()
while True:
    cmd = command()
    handle(cmd)
    if cmd=='quit' or cmd=='kill':
        break
play.join()
print('Bye!')
