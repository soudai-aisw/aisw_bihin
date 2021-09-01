import sys, termios, atexit
from select import select

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def putch(ch):
    sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

def getche():
    ch = getch()
    putch(ch)
    return ch

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []     # ここだけ修正

if __name__ == '__main__':
    atexit.register(set_normal_term)
    set_curses_term()
    pressed_count = 0
    len_str = ""

    while 1:
        if kbhit():
            ch = getch()
            pressed_count += 1
            len_str = len_str + ch
        ###sys.stdout.write('.')
            print(ch)
        
        if pressed_count > 10:
            break
        

    print('done:'+len_str)
    print('cnt :'+str(pressed_count))