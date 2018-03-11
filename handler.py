from display import *
import music

_handler = {}
_cmd_doc = {}

def add_cmd(cmd_text, func, doc):
    if cmd_text in _handler:
        warning('command %s exists in handler' % cmd_text, True)
        return
    _handler[cmd_text] = func
    _cmd_doc[cmd_text] = doc


def handle(cmd_argv):
    if len(cmd_argv)==0:
        warning('receive an invalid command', True)
        return
    if cmd_argv[0] not in _handler.keys():
        warning('command %s not found' % cmd_argv[0], True)
        return
    music.argv = cmd_argv[1:]
    _handler[cmd_argv[0]]()


def pause():
    music.flag = 1
    info('user try to pause', True)


def play():
    music.flag = 2
    info('user try to play', True)


def cycle():
    music.flag = 3
    info('user try to change to cycle mode', True)


def random():
    music.flag = 4
    info('user try to change to random mode', True)


def quit():
    music.flag = 5
    info('user try to quit', True)


def kill():
    music.flag = 6
    info('user try to kill the script', True)


def help():
    print('You can use following commands:')
    for key in _handler.keys():
        print('key %s is to %s' % (key, _cmd_doc[key]))

add_cmd('p', pause, 'let music pause')
add_cmd('P', play, 'let music play')
add_cmd('c', cycle, 'change to cycle mode')
add_cmd('r', random, 'change to random mode')
add_cmd('q', quit, 'quit softly')
add_cmd('k', kill, 'kill the script')
add_cmd('h', help, 'get the help for this script')
add_cmd('pause', pause, 'let music pause')
add_cmd('play', play, 'let music play')
add_cmd('cycle', cycle, 'change to cycle mode')
add_cmd('random', random, 'change to random mode')
add_cmd('quit', quit, 'quit softly')
add_cmd('kill', kill, 'kill the script')
add_cmd('help', help, 'get the help for this script')
