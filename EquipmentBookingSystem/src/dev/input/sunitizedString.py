#!/usr/bin/env python


import dev.display.Console as Console
import dev.input as input
import re

class SunitizedString(input.InputString):
    def __init__(self, userInput):
        super(SunitizedString, self).__init__(userInput)

    def capture(self):
        self.user_input_reader.capture()

    def get_string(self):
        return re.sub(
            '[\[\]\\"\']',
            '',
            self.user_input_reader.get_string()
        )

    def submitted(self):
        return self.user_input_reader.submitted()
