#!/usr/bin/env python


if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')

import dev.display.Console as Console
import dev.input as input


class UserInputReader(input.IUserInputReader):
    def __init__(self):
        self.__text_field = input.ConsoleTextField()
        self.__rfid_reader = input.RFIDReader()

    def capture(self):
        self.__text_field.capture()
        self.__rfid_reader.capture()

    def get_string(self):
        if self.__rfid_reader.submitted():
            device = self.__rfid_reader
        else:
            device = self.__text_field

        return device.get_string()

    def submitted(self):
        return (
            self.__text_field.submitted() or
            self.__rfid_reader.submitted()
        )


def debug_this_module():
    Console.clear()

    uir = UserInputReader()

    while not uir.submitted():
        uir.capture()
        time.sleep(0.010)

    Console.puts("Your input is :", uir.get_string())
    time.sleep(3)

    del uir


if __name__ == "__main__":
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
