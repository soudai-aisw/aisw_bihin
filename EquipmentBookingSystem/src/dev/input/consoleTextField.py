#!/usr/bin/env python


if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')


import dev.display.Console as Console
import dev.input as input


class ConsoleTextField(input.IUserInputReader):
    def __init__(self):
        self.__pressed_key = input.PressedKey()
        self.__string = ""
        self.__submitted = False
        self.__is_real_time_display_mode = True

    def capture(self):
        self.__pressed_key.capture()

        if self.__pressed_key.exists():

            if self.__pressed_key.is_enter():
                # Submit keyboard input
                self.__submitted = True
                if self.__is_real_time_display_mode:
                    Console.puts("")  # New line

            elif self.__pressed_key.is_escape():
                # Clear buffer
                self.__string = ""
                if self.__is_real_time_display_mode:
                    Console.remove_line()

            elif self.__pressed_key.is_delete():
                # Remove a last charcter
                if ( len(self.__string) > 0 ):
                    self.__string = self.__string[:-1]
                    if self.__is_real_time_display_mode:
                        Console.remove_char()
            else:
                # Join a character to last position
                key = chr(ord(self.__pressed_key.get()))
                if key.isascii():
                    self.__string += key
                    if self.__is_real_time_display_mode:
                        Console.puts(key, end='')

        else:
            self.__updated = False

    def get_string(self):
        return self.__string

    def submitted(self):
        return self.__submitted

    def display_in_real_time(self, enabled):
        self.__is_real_time_display_mode = enabled


def debug_this_module():
    Console.clear()

    text_field = ConsoleTextField()

    while not text_field.submitted():
        text_field.capture()
        time.sleep(0.010)

    Console.puts("Your input is :", text_field.get_string())
    time.sleep(3)

    del text_field


if __name__ == "__main__":
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
