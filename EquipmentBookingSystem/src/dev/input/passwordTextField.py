#!/usr/bin/env python
import dev.display.Console as Console
import dev.input as input
from logging import getLogger


class PasswordTextField(input.ConsoleTextField):
    def __init__(self):
        super().__init__()

    def capture(self):
        self._pressed_key.capture()

        if self._pressed_key.exists():

            if self._pressed_key.is_enter():
                # Submit keyboard input
                self._submitted = True
                if self._is_real_time_display_mode:
                    Console.puts("")  # New line

            elif self._pressed_key.is_escape():
                # Clear buffer
                self._string = ""
                if self._is_real_time_display_mode:
                    Console.remove_line()

            elif self._pressed_key.is_delete():
                # Remove a last charcter
                if (len(self._string) > 0):
                    self._string = self._string[:-1]
                    if self._is_real_time_display_mode:
                        Console.remove_char()
            else:
                # Join a character to last position
                key = chr(ord(self._pressed_key.get()))
                if key.isascii():
                    self._string += key
                    if self._is_real_time_display_mode:
                        Console.puts('*', end='')

        else:
            self._updated = False
