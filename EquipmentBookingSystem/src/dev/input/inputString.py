#!/usr/bin/env python

import dev.input as input

class InputString(input.IUserInputReader):
    def __init__(self, userInput):
        self.user_input_reader = userInput
