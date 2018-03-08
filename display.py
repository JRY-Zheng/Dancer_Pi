#-*- coding: utf-8 -*-
import os
import time

#   格式：\033[显示方式;前景色;背景色m
#   说明:
#
#   前景色            背景色            颜色
#   ---------------------------------------
#     30                40              黑色
#     31                41              红色
#     32                42              绿色
#     33                43              黃色
#     34                44              蓝色
#     35                45              紫红色
#     36                46              青蓝色
#     37                47              白色
#
#   显示方式           意义
#   -------------------------
#      0           终端默认设置
#      1             高亮显示
#      4            使用下划线
#      5              闪烁
#      7             反白显示
#      8              不可见
#
#   例子：
#   \033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
#   \033[0m          <!--采用终端默认设置，即取消颜色设置-->]]]


STYLE = {
        'fore':
        {   # 前景色
            'black'    : 30,   #  黑色
            'red'      : 31,   #  红色
            'green'    : 32,   #  绿色
            'yellow'   : 33,   #  黄色
            'blue'     : 34,   #  蓝色
            'purple'   : 35,   #  紫红色
            'cyan'     : 36,   #  青蓝色
            'white'    : 37,   #  白色
        },

        'back' :
        {   # 背景
            'black'     : 40,  #  黑色
            'red'       : 41,  #  红色
            'green'     : 42,  #  绿色
            'yellow'    : 43,  #  黄色
            'blue'      : 44,  #  蓝色
            'purple'    : 45,  #  紫红色
            'cyan'      : 46,  #  青蓝色
            'white'     : 47,  #  白色
        },

        'mode' :
        {   # 显示模式
            'mormal'    : 0,   #  终端默认设置
            'bold'      : 1,   #  高亮显示
            'underline' : 4,   #  使用下划线
            'blink'     : 5,   #  闪烁
            'invert'    : 7,   #  反白显示
            'hide'      : 8,   #  不可见
        },

        'default' :
        {
            'end' : 0,
        },
}

# 说明：
#   LEVEL     输出
#   --------------------------------------
#   0         INFO WARNING ERROR FATAL
#   1         WARNING ERROR FATAL
#   2         ERROR FATAL
#   3         FATAL      

LEVEL = 0

WELCOME = '''Dear %s, Welcome to Dancer %s. You have logged in remote server %s.
Date: %s, login time: %s. 
'''

user = ''
version = ''
server = ''

def _use_style(string, mode = '', fore = '', back = ''):
    mode  = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'] else ''
    fore  = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'] else ''
    back  = '%s' % STYLE['back'][back] if back in STYLE['back'] else ''
    style = ';'.join([s for s in [mode, fore, back] if s])
    style = '\033[%sm' % style if style else ''
    end   = '\033[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)



def _test_color( ):

    print(_use_style('正常显示'))
    print('')

    print("测试显示模式")
    print(_use_style('高亮',   mode = 'bold'),end='')
    print(_use_style('下划线', mode = 'underline'),end='')
    print(_use_style('闪烁',   mode = 'blink'),end='')
    print(_use_style('反白',   mode = 'invert'),end='')
    print(_use_style('不可见', mode = 'hide'))
    print('')


    print("测试前景色")
    print(_use_style('黑色',   fore = 'black'),end='')
    print(_use_style('红色',   fore = 'red'),end='')
    print(_use_style('绿色',   fore = 'green'),end='')
    print(_use_style('黄色',   fore = 'yellow'),end='')
    print(_use_style('蓝色',   fore = 'blue'),end='')
    print(_use_style('紫红色', fore = 'purple'),end='')
    print(_use_style('青蓝色', fore = 'cyan'),end='')
    print(_use_style('白色',   fore = 'white'))
    print('')


    print("测试背景色")
    print(_use_style('黑色',   back = 'black'),end='')
    print(_use_style('红色',   back = 'red'),end='')
    print(_use_style('绿色',   back = 'green'),end='')
    print(_use_style('黄色',   back = 'yellow'),end='')
    print(_use_style('蓝色',   back = 'blue'),end='')
    print(_use_style('紫红色', back = 'purple'),end='')
    print(_use_style('青蓝色', back = 'cyan'),end='')
    print(_use_style('白色',   back = 'white'))
    print('')


def _clear_line():
    print('\r'+''.join([' ' for i in range(100)]), end='\r')


def _clear_screen():
    os.system('cls')


def command(rt = True):
    print(_use_style('%s@%s $ ' % (user, server), fore = 'cyan'), end='')
    if rt: return input().split(' ')


def lyric(lyric_text, indent=10):
    _clear_line()
    print(''.join([' 'for i in range(indent)])+lyric_text)
    command(False)


def info(info_text):
    if LEVEL<=0:
        _clear_line()
        print(_use_style('INFO    :'+info_text, fore = 'green'))
        command(False)


def warning(warning_text):
    if LEVEL<=1:
        _clear_line()
        print(_use_style('WARNING :'+warning_text, fore = 'yellow'))
        command(False)


def error(error_text):
    if LEVEL<=2:
        _clear_line()
        print(_use_style('ERROR   :'+error_text, fore = 'red'))
        command(False)


def fatal(fatal_text):
    if LEVEL<=3:
        _clear_line()
        print(_use_style('FATAL   :'+fatal_text, back = 'red'))
        command(False)


def init_screen(_user, _version, _server):
    _clear_screen()
    global user, version, server
    user = _user
    version = _version
    server = _server
    print(WELCOME % (user, version, server, time.strftime("%a %b %d %Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())))


def title(title_text, indent=10):
    _clear_line()
    print(_use_style(''.join([' 'for i in range(indent)])+title_text, mode = 'invert'))
    command(False)

if __name__ == '__main__':

    _test_color( )

