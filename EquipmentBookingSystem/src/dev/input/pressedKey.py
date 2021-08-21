#!/usr/bin/env python


if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')

import platform
import dev.display.Console as Console
import dev.input as input


class PressedKey():
    def __init__(self):
        self.__keyboard = input.SingletonKeyboard()
        self.__pressed_count = self.__keyboard.get_pressed_count()
        self.__pressed_key = ""

        if self.__keyboard.is_finished:
            self.__keyboard.setDaemon(True)
            self.__keyboard.start()

    def capture(self):
        self.__keyboard.get_lock_object().acquire()
        now = self.__keyboard.get_pressed_count()
        key = self.__keyboard.get_last_pressed_key()
        self.__keyboard.get_lock_object().release()

        if self.__pressed_count != now:
            self.__pressed_count = now
            self.__pressed_key = key
        else:
            self.__pressed_key = ""

    def get(self):
        return self.__pressed_key

    def exists(self):
        return self.__pressed_key != ""

    def is_escape(self):
        if (platform.system() == 'Windows'):
            return self.__pressed_key == b'\x1b'
        else:
            return self.__pressed_key == '\x1b'

    def is_enter(self):
        if (platform.system() == 'Windows'):
            return self.__pressed_key == b'\r'
        else:
            return self.__pressed_key == '\n'

    def is_delete(self):
        if (platform.system() == 'Windows'):
            return self.__pressed_key == b'\x08'
        else:
            return self.__pressed_key == '\x7f'


def debug_this_module():
    Console.clear()

    pressedKey = PressedKey()
    Console.clear()

    while True:
        pressedKey.capture()
        if pressedKey.is_escape():
            break
        if pressedKey.exists():
            key = pressedKey.get()
            Console.puts(key, "\t", ord(key), "\t", chr(ord(key)))

        time.sleep(0.010)
    del pressedKey


if __name__ == "__main__":
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
