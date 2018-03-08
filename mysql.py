import MySQLdb as sql
from config import configs, toDict
from display import *

_conn_kw = {
    'host': configs.server,
    'port': configs.port,
    'db': configs.catalog,
    'user': configs.user,
    'passwd': configs.password,
    'charset': 'utf8',
}

conn_kw = toDict(_conn_kw)


class MysqlConnector():
    """docstring for MysqlConnector"""
    def __init__(self, conn_kw=conn_kw):
        self.conn_kw = conn_kw
        self.table = dict()
 
    def sql_connect(self, command, ex_mes):
        print(command)
        try:
            conn = sql.connect(**conn_kw)
            cur = conn.cursor()
            cur.execute(command)
            conn.commit()
            return cur.fetchall(), True
        except Exception as e:
            return self.ex(e, ex_mes), False

    def ex(self, e, ex_mes, level=2):
        log(str({'e': e, 'ex_mes': ex_mes}), level)
        return -1

    def decorate(self, item, comma=True):
        return (', ' if comma else '')+"'%s'"  % item

    def add_new_song(self, music_name, singer, belong_to_list, other_singer='', album='', publish_year=0):
        sql = "SELECT count(*) FROM music WHERE user_name = '" + self.conn_kw.user + "' AND music_name = '" + music_name + "' AND singer = '" + singer + "';"
        count, success = self.sql_connect(sql, 'cannot judge whether song %s exists' % music_name)
        if not success:
            return
        elif count[0][0]!=0:
            ex('SongExistsWaring', 1)
            return
        # add_new_list(belong_to_list)
        _other_singer = '' if other_singer=='' else ', other_singer'
        _album = '' if album=='' else ', album'
        _publish_year = '' if publish_year==0 else ', publish_year'
        other_singer_ = '' if other_singer=='' else self.decorate(other_singer)
        album_ = '' if album=='' else self.decorate(album)
        publish_year_ = '' if publish_year==0 else self.decorate(str(publish_year))
        other_param_name = _other_singer + _album + _publish_year
        whole_param = self.decorate(self.conn_kw.user, False) + self.decorate(music_name) + self.decorate(singer) + self.decorate(belong_to_list) + other_singer_ + album_ + publish_year_
        sql = "INSERT INTO music(user_name, music_name, singer, belong_to_list" + other_param_name + ")VALUES(" + whole_param + ");"
        self.sql_connect(sql, 'cannot add song %s' % music_name)

    def get_song_list(self):
        sql = "SELECT music_name, singer FROM music WHERE user_name = '" + self.conn_kw.user + "'"
        all_songs_list, success = sql_connect(sql, 'cannot get all songs list')
        if success:
            self.table['all_songs'] = all_songs_list

    def add_new_list(self, list_name):
        sql = "SELECT count(*) FROM lists WHERE user_name = '" + self.conn_kw.user + "' AND list_name = '" + list_name + "'"
        count, success = self.sql_connect(sql, 'cannot judge whether song %s exists' % list_name)
        if not success:
            return
        elif count[0][0]!=0:
            ex('ListExistsWaring', 1)
            return
        sql = "INSERT INTO lists(user_name, list_name)VALUES(" + self.decorate(self.conn_kw.user, False) + self.decorate(list_name) + ")"
        self.sql_connect(sql, 'cannot add list %s' % list_name)

    def add_listening_record(self, music_name, singer):
        sql = "INSERT INTO listening(music_name, singer, where_to_listen, user_name)VALUES(" + self.decorate(music_name, False) + self.decorate(singer) + self.decorate("Python") + self.decorate(self.conn_kw.user) + ")"
        self.sql_connect(sql, 'cannot add listening record: listened song %s of %s' % (music_name, singer))

    def get_current_song(self):
        music_name = ''
        singer = ''
        ex_mes = 'cannot get current song'
        proc_name = 'get_current_song'
        try:
            conn = sql.connect(**conn_kw)
            cur = conn.cursor()
            cur.callproc(proc_name, (music_name, singer, self.conn_kw.user))
            cur.execute('SELECT @_%s_0, @_%s_1' % (proc_name,proc_name))
            res = cur.fetchall()
            return [res[0][i].decode('utf8') for i in range(2)], True
        except Exception as e:
            return self.ex(e, ex_mes), False
