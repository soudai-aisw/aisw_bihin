#!/usr/bin/env python


if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')


import time
import threading

import dev.display.Console as Console
import dev.input as input
import cmn.des_pattern as despattern


# windows専用
import platform
if (platform.system() == 'Windows'):
    import msvcrt
    
else:
    import readchar
    from dev.input.pi_kbhit import *
    atexit.register(set_normal_term)
    set_curses_term()


# 入力ストリームは1つしかなくリソース競合するためSingletonで実装


class SingletonKeyboard(threading.Thread, despattern.Singleton):
    def __init__(self):
        super(SingletonKeyboard, self).__init__()
        self.__is_finished = False
        self.__last_pressed_key = 0
        self.__pressed_count = 0
        self.__lock = threading.Lock()

    def run(self):
        self.__is_finished = False

        while not self.__is_finished:
            # For Windows
            if (platform.system() == 'Windows'):
                with self.__lock:  # Excrusive area
                    if msvcrt.kbhit():  # The condition becomes true when any key is pressed
                        self.__pressed_count += 1
                        self.__last_pressed_key = msvcrt.getch()  # Get keyboard input
            else:
                with self.__lock:  # Excrusive area
                    if kbhit():
                        self.__pressed_count += 1
                        self.__last_pressed_key = getch()  # Get keyboard input

            time.sleep(0.010)

    def is_finished(self):
        return self.__is_finished

    def get_last_pressed_key(self):
        return self.__last_pressed_key

    def get_pressed_count(self):
        return self.__pressed_count

    def terminate(self):

        self.__is_finished = True

    def get_lock_object(self):
        return self.__lock


def debug_this_module():
    keyboard = SingletonKeyboard()
    keyboard.start()
    prev = 0
    while keyboard.get_pressed_count() < 30:
        keyboard.get_lock_object().acquire()
        now = keyboard.get_pressed_count()
        key = keyboard.get_last_pressed_key()
        keyboard.get_lock_object().release()
        if prev != now:
            Console.puts(chr(ord(key)), end="")
        prev = now
        time.sleep(0.010)

    keyboard.terminate()


if __name__ == "__main__":
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
