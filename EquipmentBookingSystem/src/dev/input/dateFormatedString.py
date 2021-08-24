#!/usr/bin/env python


import dev.display.Console as Console
import dev.input as input
import re
from datetime import datetime


class DateFormatedString(input.InputString):
    def __init__(self, userInput):
        super(DateFormatedString, self).__init__(userInput)

    def capture(self):
        self.user_input_reader.capture()

    def get_string(self):
        string = re.sub(
            '[.-]',
            '/',
            self.user_input_reader.get_string()
        )

        try:
            date = datetime.strptime(string, '%Y/%m/%d')
        except ValueError:
            try:
                date = datetime.strptime(
                    datetime.now().strftime('%Y/') + string, '%Y/%m/%d')
            except ValueError:
                date = datetime.strptime("1900/01/01", '%Y/%m/%d')

        return date.strftime('%Y/%m/%d')

    def submitted(self):
        return self.user_input_reader.submitted()
