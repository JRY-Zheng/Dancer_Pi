# -*-utf8-*-
import codecs
import re
import pygame
from pygame.mixer import music
from display import *
from config import configs
from mysql import MysqlConnector

# flag's status:
#   value       status
#   0           normally run
#   1           pause
#   2           play
#   3           cycle mode
#   4           random mode
#   5           soft quit
#   6           kill
# notice: once the command 2 3 4 5 is handled, the status should return to 0.
flag = 0
argv = []
quit = 0  # 0=>normal run, 1=>quit


class MusicPlayer():
    """docstring for MusicPlayer"""
    def __init__(self):
        self.root_music_path = configs.dir
        self.lyric_printer = LyricPrinter(self)
        self.songs = self._load_music(self.root_music_path)
        self.mysql_conn = MysqlConnector()
        self.cycle_music_name = ''
        self.cycle_singer = ''
        self.cur_music_name = ''
        self.cur_singer = ''
        pygame.mixer.init()
        pygame.time.delay(1000)

    def run_player(self):
        while quit==0:
            self._play_music(*self._prepare())

    def _load_music(self, music_path):
        if not os.path.exists(music_path):
            fatal('music does not exist!')
            raise IOError('cannot find path %s' % music_path)
        songs = []
        if len(os.listdir(music_path)) == 0:
            fatal('music lists do not exist!')
            raise IOError('cannot find any list')
        for path, dirs, files in os.walk(music_path):
            if path==music_path or path in configs.ignore:
                continue
            for file in files:
                match_nc = re.match(r'(.*?)\s-\s(.*)\.mp3', file)
                match_xm = re.match(r'(.*?)_(.*)\.mp3', file)
                if match_nc or match_xm:
                    nc_or_xm = 2 if match_nc else 1
                    match = match_nc if match_nc else match_xm
                    music_block = {
                        'music_path': music_path,
                        'music_name': match.group(nc_or_xm),
                        'file_name': re.match('(.*).mp3', file).group(1),
                        'belong_to_list': re.match(r'.*\\(.+?)$',path).group(1),
                    }
                    match_singer = re.match(r'(.*?)(、|&|\s|,)(.*)', match.group(3-nc_or_xm))
                    if match_singer:
                        music_block['singer'] = match_singer.group(1)
                        music_block['other_singer'] = match_singer.group(3)
                    else:
                        music_block['singer'] = match.group(3-nc_or_xm)
                    songs.append(music_block)
        return songs

    def _play_music(self, full_music_path, list_name, music_name):
        global flag, quit, argv
        title(music_name)
        info('playing song %s' % music_name)
        full_music_path = full_music_path
        music.load(full_music_path.replace('\\', '/'))
        music.play()
        START = time.time()
        gen_lyric = self.lyric_printer.print_lyric(full_music_path, music_name)
        lyric_printing = gen_lyric.send(None)
        while True:
            if music.get_busy() == 0:
                # gen_lyric.close()
                return
            if lyric_printing==1 and flag==0:
                lyric_printing = gen_lyric.send(time.time() - START)
            if flag==1:
                try:
                    music.pause()
                except Exception as e:
                    warning('command pause is forbidden, detail: %s' % str(e))
                    flag = 0
            elif flag==2:
                try:
                    music.unpause()
                except Exception as e:
                    warning('command play is forbidden, detail: %s' % str(e))
                finally:
                    flag = 0
            elif flag==3:
                if len(argv)==0:
                    self.cycle_music_name = self.cur_music_name
                    self.cycle_singer = self.cur_singer
                elif len(argv)==1:
                    self.cycle_music_name = argv[0]
                    self.cycle_singer = ''
                elif len(argv)==2:
                    self.cycle_music_name = argv[1]
                    self.cycle_singer = ''
                flag = 0
            elif flag==4:
                self.cycle_music_name = ''
                self.cycle_singer = ''
                flag = 0
            elif flag==5:
                quit = 1
                flag = 0
            elif flag==6:
                music.stop()
                quit = 1
                # gen_lyric.close()
                return



    def _prepare(self):
        music_name = self.cycle_music_name
        singer = self.cycle_singer
        if music_name == '' and singer == '':
            music_info, status = self.mysql_conn.get_current_song()
            if status:
                music_name, singer = music_info
        find_music = lambda x: x['music_name'] == music_name and\
                               (x['singer'] == singer)if singer else True
        found_music = self.__first__(self.songs, find_music)
        self.mysql_conn.add_listening_record(music_name, singer)
        self.cur_music_name = music_name
        self.cur_singer = singer
        return (os.path.join(found_music['music_path'],
                             found_music['belong_to_list'],
                             found_music['file_name']+'.mp3'),
                found_music['belong_to_list'],
                found_music['music_name'])

    def __first__(self, the_iterable, condition=lambda x: True):
        for i in the_iterable:
            if condition(i):
                return i
        error('cannot find such music that satisfies the given condition')


class LyricPrinter():
    """docstring for LyricPrinter"""
    def __init__(self, music_player):
        self.music_player = music_player

    def _load_lyric(self, music_path):
        lyrics = []
        full_music_path = str(music_path).replace('mp3', 'lrc')
        if not os.path.exists(full_music_path):
            return lyrics
        with codecs.open(full_music_path, 'r', 'utf8') as f:
            lyrics_text = f.readlines()
        for lyric_text in lyrics_text:
            match = re.match(r'(\[\d+:[\d.]+\])+(.*)', lyric_text)
            if not match:
                continue
            content = match.group(2)
            time_str = match.group(1)
            for time_match in re.findall(r'\[(\d+):([\d\.]+)\]', time_str):
                lyrics.append({
                    'position': float(time_match[0])*60 + float(time_match[1]),
                    'content': content,
                })
        lyrics.sort(key = lambda x:x['position'])
        return lyrics

    def print_lyric(self, music_path, music_name):
        """
        :rtype: int
        0 => lyrics printing is finished.
        1 => some lyrics is to print.
        """
        self.lyrics = self._load_lyric(music_path)
        cur_line = 0
        while True:
            if len(self.lyrics)==0:
                lyric('no valid lyric for this song')
                yield 0
            now = yield 1
            if(cur_line<len(self.lyrics) and now>self.lyrics[cur_line]['position']):
                if cur_line>=len(self.lyrics):
                    info('lyric for %s is all printed.' % music_name)
                    yield 0
                lyric(self.lyrics[cur_line]['content'])
                cur_line += 1
